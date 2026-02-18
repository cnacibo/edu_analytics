# scrapers/hse_fcs_simple.py
from storage.file_manager import FileManager
from .base_scraper import BaseScraper
from datetime import datetime
import logging
import csv
import re
import time

logger = logging.getLogger(__name__)


class HSEFCSGraper(BaseScraper):
    def __init__(self, target_levels=None):
        super().__init__(
            base_url='https://cs.hse.ru',
            name='HSE_FCS_Scraper'
        )
        self.target_levels = target_levels or ['Бакалаврские программы', 'Магистерские программы']
        self.price_bachelor_url = 'https://ba.hse.ru/price'
        self.price_master_url = 'https://admissions.hse.ru/graduate-apply/fees'

        self.prices_cache = {}

    def run(self, parse_details=False, parse_prices=False):
        """
        Запускает парсинг. Реализация метода из BaseScraper.
        """
        if parse_prices:
            self._fetch_prices()
        programs = self.parse(parse_details=parse_details, parse_prices=parse_prices)
        return programs

    def parse(self, parse_details=False, parse_prices=False):
        """Основной метод парсинга"""
        soup = self.fetch_page(self.base_url, delay=2)
        if not soup:
            return []

        programs = []
        try:
            program_links = self._extract_program_links(soup)

            for i, (name, url, level) in enumerate(program_links):
                program = {
                    'id': i + 1,
                    'name': name,
                    'url': url,
                    'level': level,
                    'cost': None,
                    'budget_places': None,
                    'paid_places': None,
                    'foreign_places': None,
                    'number_of_program': None,
                }

                if parse_details:
                    details = self._parse_program_details_item_places(url)

                    for key in ['budget_places', 'paid_places', 'foreign_places']:
                        if key in details:
                            program[key] = details[key]

                if parse_prices:
                    price_info = self._get_price_and_code_for_program(url, level, name)
                    if price_info:
                        program['cost'] = price_info.get('price')
                        program['number_of_program'] = price_info.get('code')
                programs.append(program)

        except Exception as e:
            logger.error(f"Ошибка при парсинге цен программ бакалавриата : {e}")
        return programs

    def _fetch_prices(self):
        """Загружает цены для бакалавриата и магистратуры"""
        if not self.prices_cache:
            # logger.info("Загружаем цены на обучение...")
            bachelor_prices = self._parse_bachelor_price_page()
            master_prices = self._parse_master_price_page()
            # master_prices = self._parse_price_page(self.price_master_url, 'Магистр')

            bachelor_prices = bachelor_prices if isinstance(bachelor_prices, dict) else {}
            master_prices = master_prices if isinstance(master_prices, dict) else {}

            self.prices_cache = {**bachelor_prices, **master_prices}
            logger.info(f"Загружено {len(self.prices_cache)} цен на обучение")

    def _parse_bachelor_price_page(self):
        """Парсит страницу с ценами бакалавриата"""
        soup = self.fetch_page(self.price_bachelor_url, delay=1)
        if not soup:
            logger.warning(f"Не удалось загрузить страницу с ценами: {self.price_bachelor_url}")
            return {}

        prices_dict = {}

        try:
            table = soup.find('table', class_='bordered')
            if not table:
                tables = soup.find_all('table')
                for t in tables:
                    if 'bordered' in t.get('class', []):
                        table = t
                        break
            if not table:
                logger.warning("Не найдена таблица с ценами для бакалавриата")
                return {}

            rows = table.find_all('tr')
            current_code = None

            for row in rows:
                h5_element = row.find('h5')
                if h5_element and 'НАПРАВЛЕНИЕ ПОДГОТОВКИ' in h5_element.text:
                    code_match = re.search(r'\d{2}\.\d{2}\.\d{2}', h5_element.text)
                    if code_match:
                        current_code = code_match.group(0)
                        logger.debug(f"Найден код направления: {current_code}")
                cells = row.find_all('td')
                if len(cells) >= 2:
                    link = cells[0].find('a')
                    if link and link.get('href'):
                        program_url = self._normalize_url(link.get('href'))

                        if program_url in prices_dict:
                            continue
                        price_text = cells[1].get_text(strip=True)
                        price = self._extract_price(price_text, 'Bachelor')

                        if price and current_code:
                            prices_dict[program_url] = {
                                'price': price,
                                'code': current_code,
                                'source_url': self.price_bachelor_url,
                                'program_name': link.get_text(strip=True)
                            }
            logger.info(f"Бакалавриат: найдено {len(prices_dict)} цен")
        except Exception as e:
            logger.error(f"Ошибка при парсинге цен бакалавриата: {e}")
        return prices_dict

    def _parse_master_price_page(self):
        """Парсит страницу с ценами магистратуры"""
        soup = self.fetch_page(self.price_master_url, delay=1)
        if not soup:
            logger.warning(f"Не удалось загрузить страницу с ценами: {self.price_master_url}")
            return {}

        prices_dict = {}
        try:
            # Ищем все таблицы
            tables = soup.find_all('table')
            logger.info(f"Найдено таблиц: {len(tables)}")

            for table_idx, table in enumerate(tables):
                # Проверяем, что это таблица с ценами
                table_text = table.get_text()
                if 'Стоимость одного года обучения' in table_text:
                    logger.info(f"Таблица {table_idx + 1}: найдена таблица с ценами")

                    current_code = None
                    rows_processed = 0
                    programs_found = 0

                    for row in table.find_all('tr'):
                        rows_processed += 1
                        cells = row.find_all(['td', 'th'])

                        # Ищем код направления
                        if len(cells) == 1:
                            cell_text = cells[0].get_text(strip=True)
                            if 'Направление подготовки' in cell_text:
                                code_match = re.search(r'\d{2}\.\d{2}\.\d{2}', cell_text)
                                if code_match:
                                    current_code = code_match.group(0)
                                    logger.debug(f"Найден код направления: {current_code}")

                        # Ищем строки с программами (4 ячейки)
                        elif len(cells) == 4:
                            program_name = cells[0].get_text(strip=True)
                            price_text = cells[3].get_text(strip=True)

                            # Пропускаем заголовки
                            if not program_name or 'Стоимость' in program_name:
                                continue

                            # Извлекаем цену
                            price = self._extract_price(price_text, 'Master')

                            if price and current_code:
                                normalized_name = self._normalize_program_name(program_name)
                                key = f"master:{normalized_name}"

                                prices_dict[key] = {
                                    'price': price * 1000,
                                    'code': current_code,
                                    'original_name': program_name
                                }
                                programs_found += 1
                                logger.debug(f"Найдена программа: {program_name} - {price} тыс. руб.")

                    logger.info(
                        f"Таблица {table_idx + 1}: обработано {rows_processed} строк, найдено {programs_found} программ")

            logger.info(f"Магистратура: всего найдено {len(prices_dict)} цен")
            # Выведем все найденные программы для отладки
            for key, data in prices_dict.items():
                logger.debug(f"Магистратура: {data['original_name']} - {data['price']} руб., код: {data['code']}")

        except Exception as e:
            logger.error(f"Ошибка при парсинге цен магистратуры: {e}")
            return {}

        return prices_dict

    def _normalize_program_name(self, name):
        normalized = name.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized

    def _normalize_url(self, url):
        """Нормализует URL для сравнения"""
        if not url:
            return ""
        url = url.strip().lower()
        if url.startswith('https://'):
            url = url[8:]
        elif url.startswith('http://'):
            url = url[7:]
        if url.startswith('www.'):
            url = url[4:]
        if url.endswith('/'):
            url = url[:-1]
        return url

    def _extract_price(self, text, level):
        """Извлекает цену из текста"""
        try:
            if level == 'Master':
                text_clean = text.replace(' ', '').replace(',', '.')

                match = re.search(r'(\d+\.?\d*)', text_clean)
                if match:
                    return float(match.group(1))

            elif level == 'Bachelor':
                text_clean = re.sub(r'[\s\u00A0]+', '', text)
                patterns = [
                    r'(\d{2,4})000$',  # "490000"
                    r'^(\d{3})$',  # "490" (тысячи рублей)
                    r'(\d{3})тыс',  # "490тыс"
                    r'(\d+)[.,](\d{3})',  # "490,000" или "490.000"
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
            logger.info(f"Не удалось извлечь цену из '{text}': {e}")
            return None

    def _get_price_and_code_for_program(self, program_url, program_level, program_name):
        """Ищет цену для программы"""

        if program_level == 'Бакалавр':
            normalized_url = self._normalize_url(program_url)
            for price_key, price_data in self.prices_cache.items():
                if self._urls_match(normalized_url, price_key):
                    return {'price': price_data.get('price'), 'code': price_data.get('code')}

        elif program_level == 'Магистр':
            # Нормализуем название программы
            normalized_name = self._normalize_program_name(program_name)

            # Логируем что ищем
            logger.debug(f"Ищем цену для магистерской программы: {program_name}")
            logger.debug(f"Нормализованное название: {normalized_name}")

            # 1. Попробуем точное совпадение с префиксом
            search_key = f"master:{normalized_name}"
            if search_key in self.prices_cache:
                price_data = self.prices_cache[search_key]
                logger.debug(f"Найдено точное совпадение: {price_data}")
                return {'price': price_data.get('price'), 'code': price_data.get('code')}

            # 2. Попробуем точное совпадение без префикса
            if normalized_name in self.prices_cache:
                price_data = self.prices_cache[normalized_name]
                logger.debug(f"Найдено точное совпадение (без префикса): {price_data}")
                return {'price': price_data.get('price'), 'code': price_data.get('code')}

            # 3. Попробуем частичное совпадение (если искомое название содержится в ключе)
            for price_key, price_data in self.prices_cache.items():
                # Пропускаем не-магистерские записи
                if not isinstance(price_key, str) or not (
                        price_key.startswith('master:') or 'original_name' in price_data):
                    continue

                # Извлекаем оригинальное название из данных
                original_name = price_data.get('original_name', '')
                if not original_name:
                    continue

                # Нормализуем оригинальное название из таблицы цен
                normalized_original = self._normalize_program_name(original_name)

                # Проверяем различные варианты совпадения
                if (normalized_name in normalized_original or
                        normalized_original in normalized_name or
                        self._program_names_match(program_name, original_name)):
                    logger.debug(f"Найдено частичное совпадение: {original_name} -> {program_name}")
                    return {'price': price_data.get('price'), 'code': price_data.get('code')}

            logger.debug(f"Цена не найдена для магистерской программы: {program_name}")

        return None

    def _program_names_match(self, name1, name2):
        """Проверяет, совпадают ли названия программ с учетом незначительных различий"""

        # Убираем незначительные части в скобках
        def clean_name(name):
            # Убираем текст в скобках
            name = re.sub(r'\([^)]*\)', '', name)
            # Убираем "полностью онлайн" и другие указания
            name = name.replace('полностью онлайн', '').replace('(ранее', '').strip()
            # Нормализуем
            return self._normalize_program_name(name)

        cleaned1 = clean_name(name1)
        cleaned2 = clean_name(name2)

        return cleaned1 == cleaned2

    def _get_program_name_from_cache(self, program_url):
        """Пытается получить название программы из кэша"""
        normalized_url = self._normalize_url(program_url)

        for price_key, price_data in self.prices_cache.items():
            if price_key.startswith('http'):
                if self._urls_match(normalized_url, price_key):
                    return price_data.get('name')

        return None

    def _urls_match(self, url1, url2):
        """Проверяет, указывают ли URL на одну и ту же страницу"""
        if url1 == url2:
            return True

        def get_domain_and_path(url):
            parts = url.split('/', 1)
            domain = parts[0]
            path = parts[1] if len(parts) > 1 else ''
            return domain, path

        domain1, path1 = get_domain_and_path(url1)
        domain2, path2 = get_domain_and_path(url2)

        # Убираем возможные www.
        domain1 = domain1.replace('www.', '')
        domain2 = domain2.replace('www.', '')

        return domain1 == domain2 and path1 == path2

    def _extract_program_links(self, soup):
        """Извлекает ссылки на программы из меню"""
        links = []

        try:
            education = soup.find('span', class_='pk-menu__link', string='Образование')
            if not education:
                return links

            popup = education.find_next('div', class_='pk-submenu-popup')
            if not popup:
                return links

            main_items = popup.select('ul.pk-submenu > li.pk-submenu__item')

            for item in main_items:
                if 'pk-submenu__item_with-menu' not in item.get('class', []):
                    continue

                title_span = item.find('span', class_='pk-submenu__link')
                if not title_span:
                    continue

                section_title = title_span.text.strip()

                if section_title not in self.target_levels:
                    continue

                inner_menu = item.find('ul', class_='pk-submenu__inner')
                if inner_menu:
                    li_items = inner_menu.find_all('li', class_='pk-submenu__item')

                    for li_item in li_items:
                        if 'pk-submenu__item_heading' in li_item.get('class', []):
                            break

                        link = li_item.find('a', class_='pk-submenu__link')
                        if link:
                            level = self._format_level(section_title)
                            links.append((
                                link.text.strip(),
                                link.get('href'),
                                level
                            ))

        except Exception as e:
            logger.error(f"Ошибка при извлечении ссылок: {e}")

        return links

    def _format_level(self, level_name):
        """Форматирует название уровня программы"""
        if 'Бакалавр' in level_name:
            return 'Бакалавр'
        elif 'Магистер' in level_name:
            return 'Магистр'
        return level_name

    def _parse_program_details_item_places(self, url):
        """Парсит детальную информацию о программе"""

        normalized_url = self._normalize_url(url)
        target_normalized = self._normalize_url('https://digital.hse.ru')
        if normalized_url == target_normalized:
            logger.info(f"Найдена специальная программа: {url}, устанавливаем paid_places=100")
            return {
                'budget_places': None,
                'paid_places': 100,
                'foreign_places': None
            }
        soup = self.fetch_page(url, delay=1)
        if not soup:
            return self._empty_details()
        try:
            return self._parse_places_info(soup)
        except Exception as e:
            logger.error(f"Ошибка при парсинге мест для {url}: {e}")
            return self._empty_details()

    def _empty_details(self):
        """Возвращает пустые детали программы"""
        return {
            'budget_places': None,
            'paid_places': None,
            'foreign_places': None,
        }

    def _parse_places_info(self, soup):
        """Парсит информацию о количестве мест"""
        places_elem = soup.find(class_='b-program-item_places')

        if not places_elem:
            return self._empty_details()

        try:
            parent_container = places_elem.find_parent('div', class_='b-row__item')

            if not parent_container:
                return self._empty_details()

            explanation_div = parent_container.find('div', class_='features-list')

            if not explanation_div:
                return self._empty_details()

            places_text = places_elem.get_text(strip=True)
            explanation_text = explanation_div.get_text()

            numbers = self._extract_numbers(places_text)
            context = self._analyze_context(explanation_text)

            return self._assign_places(numbers, context)

        except Exception as e:
            logger.error(f"Ошибка при парсинге мест: {e}")
            return self._empty_details()

    def _extract_numbers(self, text):
        """Извлекает числа из текста"""
        cleaned = text.replace(' ', '').replace(' ', '')
        numbers = re.findall(r'\d+', cleaned)
        return [int(num) for num in numbers]

    def _analyze_context(self, text):
        """Анализирует контекст для понимания, какие места указаны"""
        text_lower = text.lower()

        return {
            'has_budget': any(word in text_lower for word in ['бюджет', 'бюджетных']),
            'has_paid': any(word in text_lower for word in ['платных', 'платно', 'коммерческих']),
            'has_foreign': any(word in text_lower for word in ['иностранцев', 'иностранцы'])
        }

    def _assign_places(self, numbers, context):
        """Распределяет числа по типам мест"""
        result = self._empty_details()

        try:
            if len(numbers) == 3:
                result['budget_places'] = numbers[0]
                result['paid_places'] = numbers[1]
                result['foreign_places'] = numbers[2]

            elif len(numbers) == 2:
                if context['has_budget'] and context['has_paid'] and not context['has_foreign']:
                    result['budget_places'] = numbers[0]
                    result['paid_places'] = numbers[1]
                elif context['has_paid'] and context['has_foreign'] and not context['has_budget']:
                    result['paid_places'] = numbers[0]
                    result['foreign_places'] = numbers[1]

            elif len(numbers) == 1:
                if context['has_budget']:
                    result['budget_places'] = numbers[0]
                elif context['has_paid']:
                    result['paid_places'] = numbers[0]
                elif context['has_foreign']:
                    result['foreign_places'] = numbers[0]

        except Exception as e:
            logger.error(f"Ошибка при распределении мест: {e}")

        return result

    def save_to_file(self, data, filename, format='json'):
        """
        Переопределяем метод сохранения для CSV, чтобы контролировать порядок колонок
        """

        if format == 'csv':
            # Определяем порядок колонок
            fieldnames = [
                'id',
                'name',
                'url',
                'level',
                'cost',
                'budget_places',
                'paid_places',
                'foreign_places',
                'number_of_program'  # Код программы в конце
            ]

            for item in data:
                for field in fieldnames:
                    if field not in item:
                        item[field] = None

            # Сохраняем CSV
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)

            logger.info(f"Данные сохранены в CSV: {filename}")
        else:
            super().save_to_file(data, filename, format)