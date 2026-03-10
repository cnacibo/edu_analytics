import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from runners.hse_runner import HSERunner
from runners.programm_runner import HSEProgramRunner
from runners.vyzopedia_runner import VuzopediaRunner

"""Логирование парсинга"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("hse_parser.log"), logging.StreamHandler()],
)


def main():
    """Основной скрипт - запуск всех парсеров"""
    os.makedirs("storage/files/hse_programs", exist_ok=True)
    os.makedirs("storage/files/vyzopedia_programs", exist_ok=True)
    os.makedirs("storage/files/hse_courses", exist_ok=True)

    hse_runner = HSERunner()
    hse_runner.run()

    vuzo_runner = VuzopediaRunner()
    vuzo_runner.run()

    programm_runner = HSEProgramRunner()
    programm_runner.run()


if __name__ == "__main__":
    main()
