import csv
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Set

from parser.runners.base_runner import PROJECT_ROOT, BaseRunner
from parser.scrapers.extract_cities_scraper import ProgramCityScraper

logger = logging.getLogger(__name__)


class CityExtractionRunner(BaseRunner):
    def __init__(self, bachelor_csv_path: str, master_csv_path: str, headless: bool = False):
        super().__init__(output_subdir="program_cities")
        self.bachelor_csv = bachelor_csv_path
        self.master_csv = master_csv_path
        self.path = os.path.join(
            PROJECT_ROOT, "storage/files/vuzopedia_programs/programs_cities_bachelor.csv"
        )
        self.headless = headless

    def run(self):
        """
        Запускает процесс раннера для обработки каждой страницы программы.
        При случайной остановки программы реализована функция продолжения парсинга
        с i-ой программы
        :return:
        """
        files_to_process = [(self.bachelor_csv, "bachelor"), (self.master_csv, "master")]
        for csv_path, suffix in files_to_process:
            if not Path(csv_path).exists():
                logger.error(f"Файл не найден: {csv_path}, пропускаем")
                continue

            processed_names = self._load_processed_names(suffix)

            all_programs = self._read_programs_csv(csv_path)
            if not all_programs:
                logger.error(f"Нет данных в {csv_path}")
                continue
            pending_programs = [p for p in all_programs if p["name"] not in processed_names]
            logger.info(
                f"Всего программ: {len(all_programs)}, уже обработано: "
                f"{len(processed_names)}, осталось: {len(pending_programs)}"
            )

            if not pending_programs:
                logger.debug("Нет новых программ для обработки")
                continue

            scraper = ProgramCityScraper(headless=self.headless)
            new_results = scraper.run(pending_programs)

            old_results = self._load_existing_results(suffix)
            all_results = old_results + new_results

            self._save_results(all_results, suffix)

    def _load_processed_names(self, suffix: str) -> Set[str]:
        """Загружает названия уже обработанных программ из существующего JSON файла"""
        output_dir = self.get_output_dir()
        json_path = output_dir / f"programs_cities_{suffix}.json"
        if not json_path.exists():
            return set()
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {item["program_name"] for item in data if "program_name" in item}
        except Exception as e:
            logger.error(f"Ошибка при загрузке существующего файла {json_path}: {e}")
            return set()

    def _load_existing_results(self, suffix: str) -> List[Dict]:
        """Загружает все существующие результаты из JSON"""
        output_dir = self.get_output_dir()
        json_path = output_dir / f"programs_cities_{suffix}.json"
        if not json_path.exists():
            return []
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка при загрузке существующего файла {json_path}: {e}")
            return []

    def _read_programs_csv(self, filepath: str) -> List[Dict]:
        """Читает CSV и возвращает список {name, url}"""
        programs = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                url = row.get("url", "").strip()
                name = row.get("name", "").strip()
                if url and name:
                    programs.append({"name": name, "url": url})
        return programs

    def _save_results(self, data: List[Dict], suffix: str):
        """Сохраняет результаты (program_name, city, latitude, longitude) в JSON и CSV"""
        output_dir = self.get_output_dir()
        json_path = output_dir / f"programs_cities_{suffix}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранён JSON: {json_path} (всего записей: {len(data)})")

        csv_path = output_dir / f"programs_cities_{suffix}.csv"
        if data:
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["program_name", "city", "latitude", "longitude"]
                )
                writer.writeheader()
                writer.writerows(data)
        else:
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["program_name", "city", "latitude", "longitude"]
                )
                writer.writeheader()
        logger.info(f"Сохранён CSV: {csv_path}")
