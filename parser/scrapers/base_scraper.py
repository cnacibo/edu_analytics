# scrapers/base_scraper.py
import requests
from bs4 import BeautifulSoup
import time
import json
from abc import ABC, abstractmethod
from datetime import datetime


class BaseScraper(ABC):
    """Базовый класс для всех скраперов"""

    def __init__(self, base_url, name=None):
        """
        Args:
            base_url: Базовый URL сайта
            name: Название скрапера (опционально)
        """
        self.base_url = base_url
        self.name = name or self.__class__.__name__
        self.session = requests.Session()
        self.setup_session()

    def setup_session(self):
        """Настройка HTTP-сессии"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
        })

    def fetch_page(self, url, delay=1, timeout=10):
        """
        Загружает страницу и возвращает BeautifulSoup объект

        Args:
            url: URL для загрузки
            delay: Задержка между запросами (секунды)
            timeout: Таймаут запроса (секунды)

        Returns:
            BeautifulSoup объект или None при ошибке
        """
        try:
            # print(f"[{self.name}] Загружаю: {url}")
            response = self.session.get(
                url,
                timeout=timeout,
                allow_redirects=True
            )
            response.raise_for_status()

            # Автоматически определяем кодировку
            if response.encoding is None:
                response.encoding = 'utf-8'

            # Задержка для соблюдения политики сайта
            time.sleep(delay)

            return BeautifulSoup(response.text, 'lxml')

        except requests.exceptions.Timeout:
            print(f"[{self.name}] Таймаут при загрузке {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"[{self.name}] HTTP ошибка {e.response.status_code} при загрузке {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] Ошибка сети: {e}")
            return None
        except Exception as e:
            print(f"[{self.name}] Неожиданная ошибка при загрузке {url}: {e}")
            return None

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        Абстрактный метод парсинга.
        Должен быть реализован в дочерних классах.
        """
        raise NotImplementedError("Метод parse должен быть реализован в дочернем классе")

    def run(self, *args, **kwargs):
        """
        Запускает парсинг и возвращает данные.
        Можно переопределить в дочерних классах для дополнительной логики.

        Returns:
            Результат парсинга (обычно список данных)
        """
        print(f"[{self.name}] Запуск парсинга...")
        start_time = datetime.now()

        try:
            result = self.parse(*args, **kwargs)
            elapsed = (datetime.now() - start_time).total_seconds()

            if result is None:
                print(f"[{self.name}] Парсинг вернул None")
                return []

            print(f"[{self.name}] Парсинг завершен за {elapsed:.2f} секунд")
            print(f"[{self.name}] Собрано элементов: {len(result) if isinstance(result, list) else 'N/A'}")

            return result

        except Exception as e:
            print(f"[{self.name}] Ошибка при выполнении парсинга: {e}")
            raise

    def save_to_file(self, data, filename, format='json'):
        """
        Сохраняет данные в файл

        Args:
            data: Данные для сохранения
            filename: Имя файла
            format: Формат ('json', 'csv', 'parquet')
        """
        from storage.file_manager import FileManager

        if format == 'json':
            FileManager.save_json(data, filename)
        elif format == 'csv':
            FileManager.save_csv(data, filename)
        elif format == 'parquet':
            FileManager.save_parquet(data, filename)
        else:
            raise ValueError(f"Неподдерживаемый формат: {format}")

    def __repr__(self):
        return f"{self.__class__.__name__}(base_url='{self.base_url}')"