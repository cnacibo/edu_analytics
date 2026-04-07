import logging
import time
from functools import lru_cache

from geopy.geocoders import Nominatim

logger = logging.getLogger(__name__)


class CityGeocoder:
    def __init__(self, user_agent="edu_analytics_scraper", timeout=10):
        self.geolocator = Nominatim(user_agent=user_agent, timeout=timeout)

    @lru_cache(maxsize=1000)
    def get_coordinates(self, city_name: str):
        """
        Возвращает (latitude, longitude) или (None, None) если не найдено.
        """
        try:
            time.sleep(1)
            location = self.geolocator.geocode(city_name, language="ru")
            if location:
                return location.latitude, location.longitude
            else:
                logger.error(f"Не удалось найти координаты для города: {city_name}")
                return None, None
        except Exception as e:
            logger.error(f"Ошибка геокодинга для {city_name}: {e}")
            return None, None
