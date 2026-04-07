import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)


class SeleniumScraper(ABC):
    """Базовый класс для скраперов с использованием Selenium"""

    def __init__(self, base_url, name=None, headless=True):
        self.base_url = base_url
        self.name = name or self.__class__.__name__
        self.driver = None
        self.headless = headless
        self.wait = None

    def setup_driver(self):
        """Настройка WebDriver"""
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--start-maximized")  # Добавляем для лучшей видимости
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.wait = WebDriverWait(self.driver, 10)

    def fetch_page(self, url, delay=2):
        """Загружает страницу через Selenium и возвращает BeautifulSoup объект"""
        try:
            self.driver.get(url)

            if (
                "captcha" in self.driver.page_source.lower()
                or "решите капчу" in self.driver.page_source.lower()
            ):
                logger.info(
                    "\n Обнаружена капча! Необходимо решить её вручную в открытом браузере, "
                    "затем нажмите ENTER..."
                )
                input("✅ После решения капчи нажмите ENTER для продолжения...")
                self.driver.refresh()
                time.sleep(3)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "blockNewItem")))
            self.scroll_page()
            time.sleep(delay)
            return BeautifulSoup(self.driver.page_source, "html.parser")
        except Exception as e:
            logger.error(f"Ошибка загрузки {url}: {e}")
            return (
                BeautifulSoup(self.driver.page_source, "html.parser")
                if self.driver.page_source
                else None
            )

    def scroll_page(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError("Метод parse должен быть реализован в дочернем классе")

    def run(self, *args, **kwargs):
        logger.info(f"[{self.name}] Запуск парсинга...")
        start_time = datetime.now()

        try:
            self.setup_driver()
            result = self.parse(*args, **kwargs)
            elapsed = (datetime.now() - start_time).total_seconds()

            if result is None:
                logger.debug(f"[{self.name}] Парсинг вернул None")
                return []

            logger.info(f"[{self.name}] Парсинг завершен за {elapsed:.2f} секунд")
            logger.info(
                f"[{self.name}] Собрано элементов: "
                f"{len(result) if isinstance(result, list) else 'N/A'}"
            )
            return result

        except Exception as e:
            logger.error(f"[{self.name}] Ошибка при выполнении парсинга: {e}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

    def save_to_file(self, data, filename, format="json"):
        """Сохраняет данные в файл"""
        import sys

        if str(PROJECT_ROOT) not in sys.path:
            sys.path.append(str(PROJECT_ROOT))

        from storage.file_manager import FileManager

        path = Path(filename)
        if not path.is_absolute() and "storage" not in str(path):
            path = PROJECT_ROOT / "storage" / "files" / path

        if format == "json":
            FileManager.save_json(data, str(path))
        elif format == "csv":
            FileManager.save_csv(data, str(path))
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")
