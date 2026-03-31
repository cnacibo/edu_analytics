import os

from graph_core import add_semantic_edges, build_base_graph, load_and_process_data
from graph_vizualization import compute_positions, export_to_json


def main():
    """
    - Загружаем и обрабатываем данные
    - Построение графа с явными и семантическими связями
    - Визуализируем (для проверки работоспособности) и экспортируем в json
    """
    script_dir = os.path.dirname(__file__)
    print(script_dir)
    csv_path = os.path.join(script_dir, "..", "tags.csv")
    export_path = os.path.normpath(
        os.path.join(script_dir, "../..", "storage/files/graphs/graph_data.json")
    )
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    subjects_info = load_and_process_data(csv_path, count_pi=136)
    G = build_base_graph(subjects_info)
    G = add_semantic_edges(G, threshold=0.8, max_edges_per_tag=5)
    pos = compute_positions(G, k=3.0, iterations=100)
    # fig = create_figure(G, pos, threshold=0.8)
    # fig.show() -> для проверки работоспособности
    export_to_json(G, pos, export_path)


if __name__ == "__main__":
    main()
