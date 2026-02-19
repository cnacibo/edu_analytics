import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .base_runner import BaseRunner
from scrapers.hse_fcs import HSEFCSGraper


class HSERunner(BaseRunner):
    """Раннер для парсера HSE"""

    def __init__(self):
        super().__init__(output_subdir='hse_fcs')

    def run(self):
        """Запустить парсинг HSE"""
        start_time = time.time()

        scraper = HSEFCSGraper()
        programs = scraper.run(parse_details=True, parse_prices=True)

        elapsed_time = time.time() - start_time

        if not programs:
            print(f"HSE: Нет данных")
            return

        # Сохраняем результаты
        output_dir = self.get_output_dir()

        json_file = f"{output_dir}/hse.json"
        csv_file = f"{output_dir}/hse.csv"
        parquet_file = f"{output_dir}/hse.parquet"

        scraper.save_to_file(programs, json_file, format='json')
        scraper.save_to_file(programs, csv_file, format='csv')
        scraper.save_to_file(programs, parquet_file, format='parquet')

        print(f"HSE: {len(programs)} программ, {elapsed_time:.2f} сек")