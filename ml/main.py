"""
Запуск процесса работы с обработанных текстов, используя файлы:
- file_manager.py для чтения и записи данных
- tag_extractor.py для извлечения тегов из данных
"""

from file_manager import process_csv_file

if __name__ == "__main__":
    input_file = "../parser/storage/files/hse_programs/hse_programs.csv"
    process_csv_file(input_file)