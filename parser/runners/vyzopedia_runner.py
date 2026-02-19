import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .base_runner import BaseRunner
from scrapers.vyzopedia import VyzoPediaScraper


class VuzopediaRunner(BaseRunner):
    """Раннер для парсера Vuzopedia"""

    def __init__(self):
        super().__init__(output_subdir='vyzopedia')

    def run(self):
        """Запустить парсинг Vuzopedia"""
        start_time = time.time()

        scraper = VyzoPediaScraper()
        programs = scraper.parse(retry_on_timeout=True)

        elapsed_time = time.time() - start_time

        if not programs:
            print(f"Vuzopedia: Нет данных")
            return

        # Сохраняем результаты
        output_dir = self.get_output_dir()

        json_file = f"{output_dir}/vuzopedia.json"
        csv_file = f"{output_dir}/vuzopedia.csv"
        parquet_file = f"{output_dir}/vuzopedia.parquet"

        scraper.save_to_file(programs, json_file, format='json')
        scraper.save_to_file(programs, csv_file, format='csv')
        scraper.save_to_file(programs, parquet_file, format='parquet')

        print(f"Vuzopedia: {len(programs)} программ, {elapsed_time:.2f} сек")