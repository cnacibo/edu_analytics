import os
import sys

from ml.extract_tags.file_manager import process_csv_file

"""
Запуск процесса работы с обработанных текстов, используя файлы:
- file_manager.py для чтения и записи данных
- tag_extractor.py для извлечения тегов из данных
"""
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    input_file = os.path.join(script_dir, "../..", "storage/files/hse_courses/hse_course.csv")
    input_file = os.path.normpath(input_file)
    process_csv_file(input_file)
