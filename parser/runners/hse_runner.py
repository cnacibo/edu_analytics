import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.hse_fcs import HSEFCSGraper

from .base_runner import BaseRunner


class HSERunner(BaseRunner):
    """Раннер для парсера HSE"""

    def __init__(self):
        super().__init__(output_subdir="hse_program")

    def run(self):
        """Запуск парсинга и сохранение результатов"""
        start_time = time.time()

        scraper = HSEFCSGraper()
        programs = scraper.run(parse_details=True, parse_prices=True)

        elapsed_time = time.time() - start_time

        if not programs:
            print("HSE: Нет данных")
            return

        output_dir = self.get_output_dir()

        json_file = f"{output_dir}/hse_program.json"
        csv_file = f"{output_dir}/hse_program.csv"

        scraper.save_to_file(programs, json_file, format="json")
        scraper.save_to_file(programs, csv_file, format="csv")

        print(f"HSE: {len(programs)} программ, {elapsed_time:.2f} сек")
