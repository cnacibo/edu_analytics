import logging
import random
import time
from typing import Dict, List

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from parser.scrapers.selenium_scraper import SeleniumScraper
from parser.utils.geocoder import CityGeocoder

logger = logging.getLogger(__name__)


class ProgramCityScraper(SeleniumScraper):
    def __init__(self, headless: bool = False):
        super().__init__(
            base_url="https://vuzopedia.ru", name="ProgramCityScraper", headless=headless
        )
        self.geocoder = CityGeocoder()

    def fetch_page(self, url, delay=2):
        """Переопределённый метод для страниц программ – не ждёт blockNewItem"""
        try:
            self.driver.get(url)

            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#short, #full"))
                )
            except TimeoutException:
                logger.error("Не дождались блока городов, но продолжаем...")

            self.scroll_page()
            time.sleep(random.uniform(2, 5))
            return BeautifulSoup(self.driver.page_source, "html.parser")

        except Exception as e:
            logger.error(f"Ошибка загрузки {url}: {e}")
            return None

    def parse(self, programs: List[Dict]) -> List[Dict]:
        results = []
        total = len(programs)
        for idx, prog in enumerate(programs, 1):
            name = prog.get("name")
            url = prog.get("url")
            if not url:
                logger.info(f"[{idx}/{total}] Пропуск: нет URL для {name}")
                continue

            logger.info(f"[{idx}/{total}] Обработка: {name[:60]}... -> {url}")
            soup = self.fetch_page(url, delay=3)
            if soup is None:
                continue

            cities = self._extract_cities(soup)
            if not cities:
                logger.info("  Города не найдены")
                continue

            for city in cities:
                lat, lon = self.geocoder.get_coordinates(city)
                results.append(
                    {"program_name": name, "city": city, "latitude": lat, "longitude": lon}
                )
            logger.info(f"  Найдено городов: {len(cities)}")
            time.sleep(random.uniform(3, 7))
        return results

    @staticmethod
    def _extract_cities(soup: BeautifulSoup) -> List[str]:
        full_div = soup.find("div", id="full")
        if full_div:
            links = full_div.find_all("a", href=True)
            cities = [link.get_text(strip=True) for link in links if link.get_text(strip=True)]
            if cities:
                return cities
        short_div = soup.find("div", id="short")
        if short_div:
            links = short_div.find_all("a", href=True)
            cities = [link.get_text(strip=True) for link in links if link.get_text(strip=True)]
            return cities
        return []
