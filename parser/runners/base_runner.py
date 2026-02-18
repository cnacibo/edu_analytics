import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class BaseRunner:
    """Базовый класс для всех раннеров"""

    def __init__(self, output_subdir):
        self.output_subdir = output_subdir

    def get_output_dir(self):
        """Получить путь для сохранения файлов"""
        output_dir = f'storage/files/{self.output_subdir}'
        os.makedirs(output_dir, exist_ok=True)
        return output_dir