import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.vyzopedia import VyzoPediaScraper

from .base_runner import BaseRunner


class VuzopediaRunner(BaseRunner):
    """Раннер для парсера из сайта Vuzopedia.ru"""

    def __init__(self):
        super().__init__(output_subdir="vyzopedia_programs")

    def run(self):
        """Запуск парсинга и сохранение результатов"""
        start_time = time.time()

        scraper = VyzoPediaScraper()
        programs = scraper.parse(max_programs=300, retry_on_timeout=True)

        elapsed_time = time.time() - start_time

        if not programs:
            print("Vuzopedia: Нет данных")
            return

        output_dir = self.get_output_dir()

        json_file = f"{output_dir}/vuzopedia_program.json"
        csv_file = f"{output_dir}/vuzopedia_program.csv"

        scraper.save_to_file(programs, json_file, format="json")
        scraper.save_to_file(programs, csv_file, format="csv")

        print(f"Vuzopedia: {len(programs)} программ, {elapsed_time:.2f} сек")
