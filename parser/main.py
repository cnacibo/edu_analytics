# #main.py
# import sys
# import os
# import logging
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#
# from scrapers.hse_fcs import HSEFCSGraper
#
# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('parser.log'),
#         logging.StreamHandler()
#     ]
# )
#
# logger = logging.getLogger(__name__)
#
#
# def main():
#     try:
#         scraper = HSEFCSGraper()
#         print(f"Создан скрапер: {scraper}")
#         print("\nПарсинг списка программ...")
#         programs = scraper.run(parse_details=True, parse_prices=True)
#
#         if not programs:
#             print("Не удалось получить данные. Проверьте логи.")
#             return
#
#
#         by_type = {}
#         by_level = {}
#
#         for program in programs:
#             p_type = program.get('type', 'unknown')
#             p_level = program.get('level', 'unknown')
#
#             by_type[p_type] = by_type.get(p_type, 0) + 1
#             by_level[p_level] = by_level.get(p_level, 0) + 1
#
#         print("\nСохранение данных...")
#
#         output_dir = 'storage/files/hse_fcs'
#         os.makedirs(output_dir, exist_ok=True)
#
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#
#         json_file = f"{output_dir}/programs_hse.json"
#         scraper.save_to_file(programs, json_file, format='json')
#         print(f"JSON: {json_file}")
#
#         csv_file = f"{output_dir}/programs_hse.csv"
#         scraper.save_to_file(programs, csv_file, format='csv')
#         print(f"CSV: {csv_file}")
#
#         parquet_file = f"{output_dir}/programs_hse.parquet"
#         scraper.save_to_file(programs, parquet_file, format='parquet')
#         print(f"Parquet: {parquet_file}")
#
#         print("Парсинг успешно завершен!")
#     except KeyboardInterrupt:
#         print("\n\nПарсинг прерван пользователем")
#     except Exception as e:
#         logger.error(f"Критическая ошибка: {e}", exc_info=True)
#         print(f"\nПроизошла ошибка: {e}")
#
#
# if __name__ == "__main__":
#     from datetime import datetime
#     main()

import sys
import os
import time

from runners.programm_runner import HSEProgramRunner

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from runners.hse_runner import HSERunner
from runners.vyzopedia_runner import VuzopediaRunner


def main():
    """Запуск всех парсеров"""

    os.makedirs('storage/files/hse_fcs', exist_ok=True)
    os.makedirs('storage/files/vyzopedia', exist_ok=True)

    total_start_time = time.time()

    print("Запуск парсеров")
    print("-" * 40)

    # hse_runner = HSERunner()
    # hse_runner.run()
    #
    # vuzo_runner = VuzopediaRunner()
    # vuzo_runner.run()

    programm_runner = HSEProgramRunner()
    programm_runner.run()

    total_time = time.time() - total_start_time

    print("-" * 40)
    print(f"Общее время: {total_time:.2f} сек")


if __name__ == "__main__":
    main()