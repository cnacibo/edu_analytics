import logging
from pathlib import Path

from scrapers.vuzopedia_scraper import VuzopediaScraper

from .base_runner import BaseRunner

logger = logging.getLogger(__name__)


class VuzopediaRunner(BaseRunner):
    """Раннер для парсера бакалаврских и магистерских программ Vuzopedia.ru"""

    def __init__(self, headless=False, username=None, password=None):
        super().__init__(output_subdir="vuzopedia_programs")
        self.headless = headless
        self.project_root = Path(__file__).resolve().parent.parent

    def run(self, max_programs=1000):
        scraper = VuzopediaScraper(headless=self.headless)
        all_results = scraper.run(
            program_types=["bachelor", "master"], max_programs=max_programs, delay_between_pages=4
        )

        if not all_results:
            logging.error("\nНет данных о найдненных программах")
            return []

        output_dir = self.get_output_dir()

        if "bachelor" in all_results and all_results["bachelor"]:
            bachelor_file = output_dir / "vuzopedia_bachelor_programs.json"
            csv_bachelor = output_dir / "vuzopedia_bachelor_programs.csv"
            scraper.save_to_file(all_results["bachelor"], str(bachelor_file), format="json")
            scraper.save_to_file(all_results["bachelor"], str(csv_bachelor), format="csv")

        if "master" in all_results and all_results["master"]:
            master_file = output_dir / "vuzopedia_master_programs.json"
            csv_master = output_dir / "vuzopedia_master_programs.csv"
            scraper.save_to_file(all_results["master"], str(master_file), format="json")
            scraper.save_to_file(all_results["master"], str(csv_master), format="csv")

        return all_results
