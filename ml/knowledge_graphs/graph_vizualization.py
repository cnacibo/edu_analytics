import json
import os

import networkx as nx
import numpy as np
import plotly.graph_objects as go


class NumpyJSONEncoder(json.JSONEncoder):
    """
    Обработка чисел при записи в json формат
    для корректоного сохранения файла
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def compute_positions(G, k=3.0, iterations=100, seed=42):
    return nx.spring_layout(G, seed=seed, k=k, iterations=iterations)


def create_figure(G, pos, threshold=0.8):
    """
    Создаёт Plotly Figure с узлами и рёбрами
        Явные ребра: направление -> предметы, предметы -> теги
        Семантические ребра: теги -> теги

    Разделяет узлы для визуализации
    """

    color_map = {"direction": "lightblue", "subject": "lightgreen", "tag": "orange"}

    main_x, main_y, main_labels, main_colors = [], [], [], []
    tag_x, tag_y, tag_labels, tag_colors = [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        ntype = G.nodes[node]["type"]
        if ntype in ["direction", "subject"]:
            main_x.append(x)
            main_y.append(y)
            main_labels.append(G.nodes[node]["label"])
            main_colors.append(color_map[ntype])
        else:
            tag_x.append(x)
            tag_y.append(y)
            tag_labels.append(G.nodes[node]["label"])
            tag_colors.append(color_map[ntype])

    explicit_x, explicit_y = [], []
    semantic_traces = []
    min_w = 0.5
    max_w = 3.0

    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        if data.get("edge_type") == "semantic":
            weight = data.get("weight", threshold)
            width = min_w + (weight - threshold) / (1.0 - threshold) * (max_w - min_w)
            trace = go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(width=width, color="red"),
                hoverinfo="text",
                showlegend=False,
            )
            semantic_traces.append(trace)
        else:
            explicit_x.extend([x0, x1, None])
            explicit_y.extend([y0, y1, None])

    trace_explicit = go.Scatter(
        x=explicit_x,
        y=explicit_y,
        line=dict(width=0.5, color="#aaa"),
        hoverinfo="none",
        mode="lines",
        name="Явные связи",
    )
    trace_main = go.Scatter(
        x=main_x,
        y=main_y,
        mode="markers+text",
        text=main_labels,
        textposition="top center",
        hoverinfo="text",
        marker=dict(size=10, color=main_colors, line=dict(width=0.5)),
        name="Направления и предметы",
    )
    trace_tags = go.Scatter(
        x=tag_x,
        y=tag_y,
        mode="markers",
        text=tag_labels,
        hoverinfo="text",
        marker=dict(size=5, color=tag_colors, line=dict(width=0.3)),
        name="Теги",
    )

    fig = go.Figure(data=[trace_explicit, trace_main, trace_tags] + semantic_traces)
    fig.update_layout(
        title="Граф знаний с семантическими связями между тегами",
        showlegend=True,
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(b=20, l=5, r=5, t=40),
    )
    return fig


def export_to_json(G, pos, filepath="graph_data.json"):
    """
    Сохранение графа в JSON формат
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    graph_json = {
        "nodes": [
            {
                "label": G.nodes[node]["label"],
                "type": G.nodes[node]["type"],
                "x": float(pos[node][0]),
                "y": float(pos[node][1]),
            }
            for node in G.nodes()
        ],
        "edges": [
            {
                "source": u,
                "target": v,
                "type": d.get("edge_type", "explicit"),
                "weight": d.get("weight", 1.0),
            }
            for u, v, d in G.edges(data=True)
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(graph_json, f, ensure_ascii=False, indent=2, cls=NumpyJSONEncoder)
