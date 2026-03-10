import logging
import re

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HSEFCSGraper(BaseScraper):
    def __init__(self, target_levels=None):
        super().__init__(base_url="https://cs.hse.ru", name="HSE_FCS_Scraper")
        self.target_levels = target_levels or ["Бакалаврские программы", "Магистерские программы"]
        self.price_bachelor_url = "https://ba.hse.ru/price"
        self.price_master_url = "https://ma.hse.ru/cost2025"

        self.prices_cache = {}

    def run(self, parse_details=False, parse_prices=False):
        """
        Запуск программы с параметрами
        Загрузка страницы с ценами на обучение (отдельный параметр)
        """
        if parse_prices:
            self._fetch_prices()
        programs = self.parse(parse_details=parse_details, parse_prices=parse_prices)
        return programs

    def parse(self, parse_details=False, parse_prices=False):
        """
        Основной скрипт, запускающий методы для парсинга:
            - Цены обучения по программе и извечения кода этой программы
            - Количетсва мест на данное направление
        """
        soup = self.fetch_page(self.base_url, delay=2)
        if not soup:
            return []

        programs = []
        try:
            program_links = self._extract_program_links(soup)

            for i, (name, url, level) in enumerate(program_links):
                program = {
                    "id": i + 1,
                    "name": name,
                    "code": None,
                    "cost": None,
                    "study_type": level,
                    "url": url,
                }
                if parse_details:
                    details = self._parse_program_details_item_places(url)
                    program.update(details)

                if parse_prices:
                    price_info = self._get_price_and_code_for_program(url, level)
                    if price_info:
                        program["cost"] = price_info.get("price")
                        program["code"] = price_info.get("code")

                programs.append(program)
        except Exception as e:
            logger.error(f"Ошибка при парсинге программ: {e}")
        return programs

    def _fetch_prices(self):
        """
        Загрузка страницы с ценами. Распределение на
        - цены бакалавриата
        - цены магистратуры
        """
        if not self.prices_cache:
            logger.info("Загружаем цены на обучение...")
            bachelor_prices = self._parse_bachelor_price_page()
            master_prices = self._parse_master_price_page()  # ← новый метод для магистратуры
            self.prices_cache = {**bachelor_prices, **master_prices}
            logger.info(f"Загружено {len(self.prices_cache)} цен на обучение")
        else:
            logger.info(f"Используем кэшированные цены ({len(self.prices_cache)} записей)")

    def _parse_bachelor_price_page(self):
        """
        Обработка цен и кода направлений бакалавриата
        """
        soup = self.fetch_page(self.price_bachelor_url, delay=1)
        if not soup:
            logger.warning(f"Не удалось загрузить страницу с ценами: {self.price_bachelor_url}")
            return {}

        prices_dict = {}
        try:
            table = soup.find("table", class_=lambda c: c and "bordered" in c.split())
            if not table:
                tables = soup.find_all("table")
                for t in tables:
                    if "bordered" in t.get("class", []):
                        table = t
                        break

            if not table:
                logger.warning("Не найдена таблица с ценами для бакалавриата")
                return {}

            rows = table.find_all("tr")
            current_code = None

            for row in rows:
                h5 = row.find("h5")
                if h5 and "НАПРАВЛЕНИЕ ПОДГОТОВКИ" in h5.text:
                    code_match = re.search(r"\d{2}\.\d{2}\.\d{2}", h5.text)
                    if code_match:
                        current_code = code_match.group(0)

                cells = row.find_all("td")
                if len(cells) == 2:
                    link = cells[0].find("a")
                    if link and link.get("href"):
                        program_url = self._normalize_url(link.get("href"))
                        price_text = cells[1].get_text(strip=True)
                        price = self._extract_price(price_text)

                        if price and current_code:
                            prices_dict[program_url] = {
                                "price": price,
                                "code": current_code,
                                "study_type": "Бакалавр",
                                "source_url": self.price_bachelor_url,
                                "program_name": link.get_text(strip=True),
                            }

            logger.info(f"Бакалавриат: найдено {len(prices_dict)} цен")
        except Exception as e:
            logger.error(f"Ошибка при парсинге цен бакалавриата: {e}")
        return prices_dict

    def _parse_master_price_page(self):
        """
        Обработка цен и кода направлений магистратуры
        """
        soup = self.fetch_page(self.price_master_url, delay=1)
        if not soup:
            return {}

        prices_dict = {}
        table = soup.find("table", class_=lambda c: c and "bordered" in c.split())
        if not table:
            for t in soup.find_all("table"):
                if "тыс. руб" in t.get_text():
                    table = t
                    break
        if not table:
            logger.warning("Не найдена таблица с ценами магистратуры")
            return {}

        rows = table.find_all("tr")
        current_code = None

        for row in rows:
            row_text = row.get_text()
            if "направление подготовки" in row_text.lower():
                match = re.search(r"\d{2}\.\d{2}\.\d{2}", row_text)
                if match:
                    current_code = match.group(0)
                continue

            cells = row.find_all("td")
            if len(cells) == 2:
                link = cells[0].find("a")
                if link and link.get("href"):
                    program_url = self._normalize_url(link.get("href"))
                    price_text = cells[1].get_text(strip=True)
                    price = self._extract_price(price_text)
                    if price and current_code:
                        prices_dict[program_url] = {
                            "price": price,
                            "code": current_code,
                            "study_type": "Магистр",
                            "source_url": self.price_master_url,
                            "program_name": link.get_text(strip=True),
                        }

        logger.info(f"Магистратура: найдено {len(prices_dict)} цен")
        return prices_dict

    def _normalize_url(self, url):
        """
        Метод, выполняющий нормализацию ссылок
        """
        if not url:
            return ""
        url = url.strip().lower()
        if url.startswith("https://"):
            url = url[8:]
        elif url.startswith("http://"):
            url = url[7:]
        if url.startswith("www."):
            url = url[4:]
        if url.endswith("/"):
            url = url[:-1]
        return url

    def _extract_price(self, text):
        """Извлекает цену из текста, возвращает в рублях"""
        try:
            text_clean = re.sub(r"[\s\u00A0]+", "", text)
            patterns = [
                r"(\d{2,4})000$",
                r"^(\d{3})$",
                r"(\d{3})тыс",
                r"(\d+)[.,](\d{3})",
            ]
            for pattern in patterns:
                match = re.search(pattern, text_clean)
                if match:
                    if len(match.groups()) == 1:
                        num = int(match.group(1))
                        if num < 1000:
                            return num * 1000
                        else:
                            return num
                    elif len(match.groups()) == 2:
                        return int(match.group(1) + match.group(2))
            return None
        except Exception as e:
            logger.debug(f"Не удалось извлечь цену из '{text}': {e}")
            return None

    def _get_price_and_code_for_program(self, program_url, program_level):
        """
        Заполнение в словарь данные о коде и цены направления
        """
        normalized_url = self._normalize_url(program_url)
        for price_key, price_data in self.prices_cache.items():
            if not price_key.startswith("name:") and self._urls_match(normalized_url, price_key):
                price = price_data.get("price")
                code = price_data.get("code")
                if price:
                    return {"price": price / 1000, "code": code}

        if program_level == "Магистр":
            match = re.search(r"/ma/([^/]+)", program_url)
            url_slug = match.group(1) if match else None
            for price_key, price_data in self.prices_cache.items():
                if price_key.startswith("name:"):
                    cached_name = price_data.get("program_name", "").lower()
                    if url_slug and (
                        url_slug.replace("-", " ") in cached_name or cached_name in url_slug.replace("-", " ")
                    ):
                        price = price_data.get("price")
                        code = price_data.get("code")
                        if price:
                            return {"price": price / 1000, "code": code}
        return None

    def _urls_match(self, url1, url2):
        """
        Метод, сравнивающий два нормальзированных url
        """
        if url1 == url2:
            return True
        u1 = self._normalize_url(url1)
        u2 = self._normalize_url(url2)
        if u1 == u2:
            return True
        if u1 in u2 or u2 in u1:
            return True
        return False

    def _extract_program_links(self, soup):
        """
        Метод, извлекающий с основной страницы НИУ ВШЭ данные:
        - название программы  (name)
        - ссылку на программу (url)
        - уровень программмы  (study_type)
        """
        links = []
        try:
            education = soup.find("span", class_="pk-menu__link", string="Образование")
            if not education:
                return links

            popup = education.find_next("div", class_="pk-submenu-popup")
            if not popup:
                return links

            main_items = popup.select("ul.pk-submenu > li.pk-submenu__item")
            for item in main_items:
                if "pk-submenu__item_with-menu" not in item.get("class", []):
                    continue
                title_span = item.find("span", class_="pk-submenu__link")
                if not title_span:
                    continue
                section_title = title_span.text.strip()
                if section_title not in self.target_levels:
                    continue

                inner_menu = item.find("ul", class_="pk-submenu__inner")
                if inner_menu:
                    li_items = inner_menu.find_all("li", class_="pk-submenu__item")
                    for li_item in li_items:
                        if "pk-submenu__item_heading" in li_item.get("class", []):
                            break
                        link = li_item.find("a", class_="pk-submenu__link")
                        if link:
                            level = self._format_level(section_title)
                            links.append((link.text.strip(), link.get("href"), level))
        except Exception as e:
            logger.error(f"Ошибка при извлечении ссылок: {e}")
        return links

    def _format_level(self, level_name):
        """
        Метод, корректирующий название уровня программы на корректное
        """
        if "Бакалавр" in level_name:
            return "Бакалавр"
        elif "Магистер" in level_name:
            return "Магистр"
        return level_name

    def _parse_program_details_item_places(self, url):
        """
        Парсит страницу программы и извлекает количество бюджетных, платных мест,
        а также общее количество мест для иностранцев (сумма бюджетных и платных).
        Возвращает словарь с ключами:
            budget_places, paid_places, foreigners_places
        """
        logger.debug(f"Парсим детали программы: {url}")
        soup = self.fetch_page(url, delay=1)
        if not soup:
            return {}

        places_header = soup.find("div", class_=lambda c: c and "b-program-item_places" in c.split())
        if not places_header:
            places_header = soup.find("div", class_="features-list")
            if not places_header or (
                "бюджетных мест" not in places_header.get_text() and "платных мест" not in places_header.get_text()
            ):
                logger.debug("Не найден блок с информацией о местах")
                return {}

        features_block = (
            places_header.find_next_sibling("div", class_="features-list")
            if places_header.name != "div" or "features-list" not in places_header.get("class", [])
            else places_header
        )
        if not features_block:
            features_block = places_header.find_next("div", class_="features-list")
        if not features_block:
            return {}

        budget = None
        paid = None
        foreign_budget = None
        foreign_paid = None

        paragraphs = features_block.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            match = re.search(r"(\d+)", text)
            if not match:
                continue
            number = int(match.group(1))
            text_lower = text.lower()

            if "бюджетных мест" in text_lower and "иностранцев" not in text_lower and "стипендий" not in text_lower:
                budget = number
            elif (
                ("бюджетных мест" in text_lower and "иностранцев" in text_lower)
                or "стипендий правительства рф" in text_lower
                or "государственных стипендий" in text_lower
            ):
                foreign_budget = number
            elif "платных мест" in text_lower and "иностранцев" not in text_lower:
                paid = number
            elif "платных мест" in text_lower and "иностранцев" in text_lower:
                foreign_paid = number

        details = {}
        if budget is not None:
            details["budget_places"] = budget
        if paid is not None:
            details["paid_places"] = paid

        foreigners = None
        if foreign_budget is not None and foreign_paid is not None:
            foreigners = foreign_budget + foreign_paid
        elif foreign_budget is not None:
            foreigners = foreign_budget
        elif foreign_paid is not None:
            foreigners = foreign_paid
        if foreigners is not None:
            details["foreigners_places"] = foreigners

        logger.debug(f"Извлечённые места для {url}: {details}")
        return details
