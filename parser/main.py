import logging
import os
import sys

from runners.hse_runner import HSERunner
from runners.program_runner import HSEProgramRunner

from parser.runners.extract_cities_runner import CityExtractionRunner
from parser.runners.vuzopedia_runner import VuzopediaRunner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

"""Логирование парсинга"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("hse_parser.log"), logging.StreamHandler()],
)


def main():
    """Основной скрипт - запуск всех парсеров"""
    os.path.join(BASE_DIR, "../..", "storage/files/hse_programs")
    os.path.join(BASE_DIR, "../..", "storage/files/vyzopedia_programs")
    os.path.join(BASE_DIR, "../..", "storage/files/hse_courses")
    os.path.join(BASE_DIR, "../..", "storage/files/program_cities")
    BACHELOR_PATH = os.path.join(
        BASE_DIR, "storage/files/vuzopedia_programs/vuzopedia_bachelor_programs.csv"
    )
    MASTER_PATH = os.path.join(
        BASE_DIR, "storage/files/vuzopedia_programs/vuzopedia_master_programs.csv"
    )

    hse_runner = HSERunner()
    hse_runner.run()

    programm_runner = HSEProgramRunner()
    programm_runner.run()

    runner = VuzopediaRunner(headless=False)
    runner.run(max_programs=1000)

    runner = CityExtractionRunner(BACHELOR_PATH, MASTER_PATH, headless=False)
    runner.run()


if __name__ == "__main__":
    main()
