import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .base_runner import BaseRunner
from scrapers.program import HSEProgramScraper


class HSEProgramRunner(BaseRunner):
    """Раннер для парсера курсов ВШЭ"""

    def __init__(self):
        super().__init__(output_subdir='hse_programs')

    def run(self):
        """Запустить парсинг и сохранить результаты"""
        start_time = time.time()

        scraper = HSEProgramScraper()
        programs = scraper.parse()

        elapsed_time = time.time() - start_time

        if not programs:
            print("HSE: Нет данных")
            return

        # Сохраняем результаты
        output_dir = self.get_output_dir()

        json_file = f"{output_dir}/hse_programs.json"
        csv_file = f"{output_dir}/hse_programs.csv"
        parquet_file = f"{output_dir}/hse_programs.parquet"

        scraper.save_to_file(programs, json_file, format='json')
        scraper.save_to_file(programs, csv_file, format='csv')
        scraper.save_to_file(programs, parquet_file, format='parquet')

        print(f"HSE: {len(programs)} программ, {elapsed_time:.2f} сек")