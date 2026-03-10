"""
Метод, выполняющий
- Чтение CSV файл с колонками title, content и results
- Запуск процесса обработки текста и извлечение из него тегов-
- Сохранение результат в файл tags.csv.
"""

from pathlib import Path

import pandas as pd
from tag_extractor import TagExtractor


def process_csv_file(input_file: str, output_file: str = None):
    """
    Суть: Читает CSV, извлекает теги, сохраняет результат.

    Ожидает CSV с колонками:
    - title (название дисциплины)
    - content (содержание дисциплины)
    - results (планируемые результаты)

    Ожидаемый результат:
    - Файл tags.csv с двумя колонками title, tags
    """
    df = pd.read_csv(input_file)

    content_col = None
    results_col = None
    title_col = None
    program_type_col = None

    for col in df.columns:
        col_lower = col.lower()
        if "content" in col_lower:
            content_col = col
        elif "results" in col_lower:
            results_col = col
        elif "title" in col_lower:
            title_col = col
        elif "program_type" in col_lower:
            program_type_col = col

    if not content_col or not results_col:
        print("Не найдены нужные колонки! \nДоступные колонки: {list(df.columns)}")
        return

    extractor = TagExtractor()
    all_tags = []

    for idx, row in df.iterrows():
        description = row[results_col]

        if pd.isna(description) or not isinstance(description, str) or not description.strip():
            print("  Пустое описание, пропуск")
            all_tags.append([])
            continue

        tags = extractor.extract(description)
        all_tags.append(tags)
    df["tags"] = all_tags
    df["tags_str"] = df["tags"].apply(lambda x: ", ".join(x) if x else "")

    if output_file is None:
        script_dir = Path(__file__).parent
        output_file = script_dir / "tags.csv"

    if title_col is None:
        title_col = content_col
    df_to_save = df[[title_col, program_type_col, "tags_str"]].copy()
    df_to_save.to_csv(output_file, index=False, encoding="utf-8-sig")
    return df
