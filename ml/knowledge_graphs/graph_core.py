from collections import defaultdict

import networkx as nx
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def load_and_process_data(csv_path, count_pi=136):
    """
    - Загружает файл CSV
    - Разделяет на направления count_pi = 136 (от 0 до 136 - ПИ, остаьное - ПМИ)
    - возвращает subjects_info
    """
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df = df.dropna(subset=["title"])
    df_pi = df.iloc[:count_pi].copy()
    df_pmi = df.iloc[count_pi:].copy()

    subjects_info = defaultdict(lambda: {"tags": set(), "directions": set()})

    def process(df, direction_name):
        for _, row in df.iterrows():
            title = row["title"].strip()
            tags_str = row["tags_str"]
            subjects_info[title]["directions"].add(direction_name)
            if pd.notna(tags_str):
                tags = [t.strip().lower() for t in tags_str.split(",") if t.strip()]
                subjects_info[title]["tags"].update(tags)

    process(df_pi, "Программная инженерия")
    process(df_pmi, "Прикладная математика и информатика")
    return subjects_info


def build_base_graph(subjects_info):
    """
    Строит начальный граф с направлениями, предметами, тегами
    Связи:
        Направление -> предметы
        Предметы -> теги
        Теги -> теги (в методе "add_semantic_edges")

    Без семантических связей: только соединение элементов (тегов/предметов)
    с соотвествующими предметами/направлениями, взятые с файла
    """
    G = nx.Graph()
    directions = ["Программная инженерия", "Прикладная математика и информатика"]
    for d in directions:
        G.add_node(d, label=d, type="direction")
    for title, info in subjects_info.items():
        G.add_node(title, label=title, type="subject")
        for d in info["directions"]:
            G.add_edge(d, title, edge_type="explicit")
        for tag in info["tags"]:
            G.add_node(tag, label=tag, type="tag")
            G.add_edge(title, tag, edge_type="explicit")
    return G


def add_semantic_edges(
    G, threshold=0.8, max_edges_per_tag=5, model_name="cointegrated/rubert-tiny2"
):
    """
    Добавление новой связи "теги -> теги"
    Вычисляет связь на косинусного сходства эмбеддингов
    """
    all_tags = [node for node in G.nodes() if G.nodes[node]["type"] == "tag"]
    if not all_tags:
        print("Нет тегов для семантического анализа")
        return G
    model = SentenceTransformer(model_name)
    tag_embeddings = model.encode(all_tags, show_progress_bar=True)
    sim_matrix = cosine_similarity(tag_embeddings)

    for i, tag_i in enumerate(all_tags):
        similarities = []
        for j, tag_j in enumerate(all_tags):
            if i != j:
                sim = sim_matrix[i, j]
                if sim >= threshold:
                    similarities.append((j, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        for j, sim in similarities[:max_edges_per_tag]:
            tag_j = all_tags[j]
            if not G.has_edge(tag_i, tag_j):
                G.add_edge(tag_i, tag_j, edge_type="semantic", weight=sim)
    return G
