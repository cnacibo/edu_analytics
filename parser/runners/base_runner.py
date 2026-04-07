import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


class BaseRunner:
    """Базовый класс для всех runner - запусков веб-скрапинга"""

    def __init__(self, output_subdir):
        """
        Параметры:
            output_subdir: корневая директория в storage/files/ для сохранения файлов
        """
        self.output_subdir = output_subdir
        self.project_root = PROJECT_ROOT

    def get_output_dir(self):
        output_dir = PROJECT_ROOT / "storage" / "files" / self.output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def get_output_path(self, filename):
        """Получить полный путь к файлу для сохранения"""
        output_dir = self.get_output_dir()
        return output_dir / filename

    @staticmethod
    def get_project_root():
        """Статический метод для получения корня проекта"""
        return PROJECT_ROOT
