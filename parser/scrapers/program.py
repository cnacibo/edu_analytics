# import re
# import time
# import logging
# from .base_scraper import BaseScraper
#
# logger = logging.getLogger(__name__)
#
#
# class HSEProgramScraper(BaseScraper):
#     """Скрепер для курсов программ ВШЭ (SE и AMI)"""
#
#     def __init__(self):
#         super().__init__(
#             base_url='https://www.hse.ru',
#             name='HSE_Program_Scraper'
#         )
#         self.program_urls = {
#             'se': 'https://www.hse.ru/ba/se/courses',
#             'ami': 'https://www.hse.ru/ba/ami/courses'
#         }
#         self.prices_cache = {}
#
#     def parse(self):
#         """
#         Основной метод парсинга: обходит все программы и собирает данные по каждому курсу.
#         """
#         all_programs = []
#         for prog_type, list_url in self.program_urls.items():
#             logger.info(f"Парсинг списка курсов для {prog_type} с {list_url}")
#             soup = self.fetch_page(list_url, delay=2)
#             if not soup:
#                 logger.error(f"Не удалось загрузить страницу списка для {prog_type}")
#                 continue
#
#             detail_urls = self._extract_detail_urls(soup)
#             logger.info(f"Найдено {len(detail_urls)} курсов для {prog_type}")
#
#             for url in detail_urls:
#                 full_url = url if url.startswith('http') else self.base_url + url
#                 program_data = self._parse_detail_page(full_url, prog_type)
#                 if program_data:
#                     all_programs.append(program_data)
#                 time.sleep(1)
#
#         return all_programs
#
#     def _extract_detail_urls(self, soup):
#         """
#         Извлекает ссылки на детальные страницы курсов из общего списка.
#         """
#         urls = []
#         items = soup.find_all('div', class_='edu-events__item')
#         for item in items:
#             title_div = item.find('div', class_='edu-events_title')
#             if title_div:
#                 link = title_div.find('a', href=True)
#                 if link:
#                     urls.append(link['href'])
#         return urls
#
#     def _parse_detail_page(self, url, program_type):
#         """
#         Парсит детальную страницу курса и возвращает словарь с данными.
#         """
#         soup = self.fetch_page(url, delay=2)
#         if not soup:
#             logger.warning(f"Не удалось загрузить детальную страницу: {url}")
#             return None
#
#         data = {
#             # 'id': self._extract_id_from_url(url),
#             # 'program_type': program_type,
#             'url': url,
#             'title': self._extract_title(soup),
#             'year': None,
#             'module': None,
#             'status': self._extract_status(soup),
#             'language': self._extract_language(soup),
#             'credits': self._extract_credits(soup),
#             'content': self._extract_content(soup),
#             'results': self._extract_results(soup),
#         }
#
#         year, module = self._extract_year_and_module(soup)
#         data['year'] = year
#         data['module'] = module
#
#         return data
#
#     # ---------- Вспомогательные методы для извлечения отдельных полей ----------
#     def _extract_id_from_url(self, url):
#         """Извлекает числовой ID из URL (например, 1048849927)"""
#         match = re.search(r'/(\d+)\.html', url)
#         return match.group(1) if match else None
#
#     def _extract_title(self, soup):
#         """Название курса"""
#         h1 = soup.find('h1', class_='b-program__header-title')
#         return h1.get_text(strip=True) if h1 else None
#
#     def _extract_year_and_module(self, soup):
#         """
#         Извлекает год обучения и модули из блока "Когда читается:".
#         Возвращает кортеж (year, module).
#         """
#         dt = soup.find('dt', string=re.compile(r'Когда читается', re.IGNORECASE))
#         if dt:
#             dd = dt.find_next_sibling('dd')
#             if dd:
#                 text = dd.get_text(strip=True)
#                 parts = text.split(',')
#                 year = parts[0].strip() if len(parts) > 0 else None
#                 module = parts[1].strip() if len(parts) > 1 else None
#                 return year, module
#         return None, None
#
#     def _extract_status(self, soup):
#         """Статус курса (обязательный / по выбору)"""
#         dt = soup.find('dt', string=re.compile(r'Статус', re.IGNORECASE))
#         if dt:
#             dd = dt.find_next_sibling('dd')
#             if dd:
#                 return dd.get_text(strip=True)
#         return None
#
#     def _extract_language(self, soup):
#         """Язык преподавания"""
#         # Пробуем найти на детальной странице блок с языком
#         lang_span = soup.find('span', class_='b-program__lang1')
#         if lang_span:
#             return lang_span.get_text(strip=True)
#         # Если нет, ищем на странице списка (уже перешли на детальную, но на всякий случай)
#         return None
#
#     def _extract_credits(self, soup):
#         """Количество кредитов"""
#         credit_block = soup.find('div', class_='b-program_small', string=re.compile(r'Кредиты', re.IGNORECASE))
#         if credit_block:
#             parent = credit_block.find_parent('div', class_='b-program__header-info-block3')
#             if parent:
#                 big = parent.find('div', class_='b-program_big')
#                 if big:
#                     return self._extract_number(big.get_text(strip=True))
#         return None
#
#     def _extract_content(self, soup):
#         """Содержание учебной дисциплины (блок с id="sections")"""
#         section = soup.find(id='sections')
#         if section:
#             parent = section.find_parent('div', class_='pud__section')
#             if parent:
#                 content_div = parent.find('div', class_='pud__content')
#                 if content_div:
#                     return ' '.join(content_div.stripped_strings)
#         return None
#
#     def _extract_results(self, soup):
#         """Планируемые результаты обучения (блок с id="results")"""
#         section = soup.find(id='results')
#         if section:
#             parent = section.find_parent('div', class_='pud__section')
#             if parent:
#                 content_div = parent.find('div', class_='pud__content')
#                 if content_div:
#                     return ' '.join(content_div.stripped_strings)
#         return None
#
#     def _extract_number(self, text):
#         """Извлекает целое число из текста"""
#         if not text:
#             return None
#         numbers = re.findall(r'\d+', text)
#         return int(numbers[0]) if numbers else None

import re
import time
import logging
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class HSEProgramScraper(BaseScraper):
    """Скрепер для курсов программ ВШЭ (SE и AMI)"""

    def __init__(self):
        super().__init__(
            base_url='https://www.hse.ru',
            name='HSE_Program_Scraper'
        )
        self.program_urls = {
            'se': 'https://www.hse.ru/ba/se/courses',
            'ami': 'https://www.hse.ru/ba/ami/courses'
        }
        self.prices_cache = {}

    def parse(self, max_pages=None):
        """
        Основной метод парсинга: обходит все программы и собирает данные по каждому курсу.
        max_pages - максимальное количество страниц для каждого типа (None - все)
        """
        all_programs = []
        for prog_type, list_url in self.program_urls.items():
            logger.info(f"Парсинг списка курсов для {prog_type} с {list_url}")

            # Получаем первую страницу, чтобы узнать общее количество страниц
            soup = self.fetch_page(list_url, delay=2)
            if not soup:
                logger.error(f"Не удалось загрузить страницу списка для {prog_type}")
                continue

            total_pages = self._get_total_pages(soup)
            if max_pages:
                total_pages = min(total_pages, max_pages)

            logger.info(f"Всего страниц для {prog_type}: {total_pages}")

            # Парсим первую страницу
            detail_urls = self._extract_detail_urls(soup)
            logger.info(f"Страница 1/{total_pages}: найдено {len(detail_urls)} курсов")
            for url in detail_urls:
                full_url = url if url.startswith('http') else self.base_url + url
                program_data = self._parse_detail_page(full_url, prog_type)
                if program_data:
                    all_programs.append(program_data)
                time.sleep(1)

            # Парсим остальные страницы
            for page in range(2, total_pages + 1):
                page_url = self._build_page_url(list_url, page)
                logger.info(f"Загрузка страницы {page}/{total_pages}: {page_url}")
                soup_page = self.fetch_page(page_url, delay=2)
                if not soup_page:
                    logger.warning(f"Не удалось загрузить страницу {page} для {prog_type}")
                    continue

                detail_urls = self._extract_detail_urls(soup_page)
                logger.info(f"Страница {page}: найдено {len(detail_urls)} курсов")
                for url in detail_urls:
                    full_url = url if url.startswith('http') else self.base_url + url
                    program_data = self._parse_detail_page(full_url, prog_type)
                    if program_data:
                        all_programs.append(program_data)
                    time.sleep(1)

        return all_programs

    def _build_page_url(self, base_url, page_num):
        """Формирует URL для заданной страницы пагинации"""
        if page_num == 1:
            return base_url
        # Пример: https://www.hse.ru/ba/se/courses/page2.html?year=2025
        base = base_url.rstrip('/')
        return f"{base}/page{page_num}.html?year=2025"

    def _get_total_pages(self, soup):
        """Определяет общее количество страниц по пагинации"""
        pages_div = soup.find('div', class_='pages')
        if not pages_div:
            return 1
        page_links = pages_div.find_all('a', class_='pages__page')
        if not page_links:
            return 1
        max_page = 1
        for link in page_links:
            href = link.get('href', '')
            match = re.search(r'/page(\d+)\.html', href)
            if match:
                page_num = int(match.group(1))
                if page_num > max_page:
                    max_page = page_num
        # Также может быть активная страница с номером в тексте
        active = pages_div.find('span', class_='pages__page_active')
        if active:
            try:
                page_num = int(active.get_text(strip=True))
                if page_num > max_page:
                    max_page = page_num
            except:
                pass
        return max_page

    def _extract_detail_urls(self, soup):
        """Извлекает ссылки на детальные страницы курсов из общего списка"""
        urls = []
        items = soup.find_all('div', class_='edu-events__item')
        for item in items:
            title_div = item.find('div', class_='edu-events_title')
            if title_div:
                link = title_div.find('a', href=True)
                if link:
                    urls.append(link['href'])
        return urls

    def _parse_detail_page(self, url, program_type):
        """Парсит детальную страницу курса и возвращает словарь с данными"""
        soup = self.fetch_page(url, delay=2)
        if not soup:
            logger.warning(f"Не удалось загрузить детальную страницу: {url}")
            return None

        data = {
            'id': self._extract_id_from_url(url),
            'program_type': program_type,
            'url': url,
            'title': self._extract_title(soup),
            'year': None,
            'module': None,
            'status': self._extract_status(soup),
            'language': self._extract_language(soup),
            'credits': self._extract_credits(soup),
            'content': self._extract_content(soup),
            'results': self._extract_results(soup),
        }

        year, module = self._extract_year_and_module(soup)
        data['year'] = year
        data['module'] = module

        return data

    # ---------- Вспомогательные методы для извлечения отдельных полей ----------
    def _extract_id_from_url(self, url):
        match = re.search(r'/(\d+)\.html', url)
        return match.group(1) if match else None

    def _extract_title(self, soup):
        h1 = soup.find('h1', class_='b-program__header-title')
        return h1.get_text(strip=True) if h1 else None

    def _extract_year_and_module(self, soup):
        dt = soup.find('dt', string=re.compile(r'Когда читается', re.IGNORECASE))
        if dt:
            dd = dt.find_next_sibling('dd')
            if dd:
                text = dd.get_text(strip=True)
                parts = text.split(',')
                year = parts[0].strip() if len(parts) > 0 else None
                module = parts[1].strip() if len(parts) > 1 else None
                return year, module
        return None, None

    def _extract_status(self, soup):
        dt = soup.find('dt', string=re.compile(r'Статус', re.IGNORECASE))
        if dt:
            dd = dt.find_next_sibling('dd')
            if dd:
                return dd.get_text(strip=True)
        return None

    def _extract_language(self, soup):
        lang_span = soup.find('span', class_='b-program__lang1')
        return lang_span.get_text(strip=True) if lang_span else None

    def _extract_credits(self, soup):
        credit_block = soup.find('div', class_='b-program_small', string=re.compile(r'Кредиты', re.IGNORECASE))
        if credit_block:
            parent = credit_block.find_parent('div', class_='b-program__header-info-block3')
            if parent:
                big = parent.find('div', class_='b-program_big')
                if big:
                    return self._extract_number(big.get_text(strip=True))
        return None

    def _extract_content(self, soup):
        section = soup.find(id='sections')
        if section:
            parent = section.find_parent('div', class_='pud__section')
            if parent:
                content_div = parent.find('div', class_='pud__content')
                if content_div:
                    return ' '.join(content_div.stripped_strings)
        return None

    def _extract_results(self, soup):
        section = soup.find(id='results')
        if section:
            parent = section.find_parent('div', class_='pud__section')
            if parent:
                content_div = parent.find('div', class_='pud__content')
                if content_div:
                    return ' '.join(content_div.stripped_strings)
        return None

    def _extract_number(self, text):
        if not text:
            return None
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None