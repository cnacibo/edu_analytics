import logging
import re
import time

from .selenium_scraper import SeleniumScraper

logger = logging.getLogger(__name__)


class VuzopediaScraper(SeleniumScraper):
    """
    Скрапер для программ бакалавриата/магистратуры Vuzopedia
    с использованием ручного входа на сайт
    """

    def __init__(self, headless=False):
        super().__init__(
            base_url="https://vuzopedia.ru", name="Vuzopedia_Master_Scraper", headless=headless
        )
        self.bachelor_url = "https://vuzopedia.ru/program/bakispec"
        self.master_url = "https://vuzopedia.ru/program/magistratura"

    def manual_login(self, username=None, password=None):
        """
        Ручной вход в браузере – открывает страницу и ждёт,
        пока пользователь войдёт.
        """
        try:
            logger.info(
                "Выполняется ручной ввод: Нажмите кнопнку войти в "
                "правом верхнем углу и введите email и пароль"
            )
            self.driver.get(self.base_url)
            time.sleep(2)
            input("\nПосле успешного входа нажмите ENTER для продолжения...\n")
            logger.info("Ручной вход выполнен успешно!")
            return True
        except Exception as e:
            logger.error(f"[{self.name}]Ошибка при ручном входе: {e}")
            return False

    def parse(self, program_type="master", max_programs=300, max_pages=None, delay_between_pages=3):
        """
        Парсит программы (бакалавриат или магистратура)

        Параметры:
            program_type: 'bachelor' или 'master'
            max_programs: максимум программ для сбора
            max_pages: максимум страниц для парсинга
            delay_between_pages: задержка между страницами (сек)
        """
        if program_type == "bachelor":
            base_url = self.bachelor_url
        elif program_type == "master":
            base_url = self.master_url
        else:
            logger.error(f"Unknown program_type: {program_type}")
            return []

        all_programs = []
        page_num = 1
        program_counter = 1

        while True:
            url = base_url if page_num == 1 else f"{base_url}?page={page_num}"

            soup = self.fetch_page(url, delay=delay_between_pages)
            if not soup:
                logger.info(f"[{self.name}] Не удалось загрузить страницу {page_num}")
                break

            page_programs = self._parse_page(soup, program_counter)
            if not page_programs:
                logger.info(f"[{self.name}] На странице {page_num} нет программ")
                break

            all_programs.extend(page_programs)
            program_counter += len(page_programs)

            if max_programs and len(all_programs) >= max_programs:
                all_programs = all_programs[:max_programs]
                logger.info(f"[{self.name}] Достигнут лимит в {max_programs} программ")
                break

            if max_pages and page_num >= max_pages:
                logger.info(f"[{self.name}] Достигнут лимит страниц")
                break

            if not self._has_next_page(soup):
                logger.debug(f"[{self.name}] Достигнут конец списка")
                break

            page_num += 1

        return all_programs

    def _parse_page(self, soup, start_counter):
        """
        Парсит одну страницу (BeautifulSoup - объект)
        """
        programs = []
        program_blocks = soup.find_all("div", class_="blockNewItem")
        logger.debug(f"[{self.name}] Найдено блоков программ: {len(program_blocks)}")

        for i, block in enumerate(program_blocks, start_counter):
            try:
                program = self._extract_program_data(block, i)
                if program and program.get("name"):
                    programs.append(program)
            except Exception as e:
                logger.error(f"Ошибка при парсинге программы {i}: {e}")
        return programs

    def _extract_program_data(self, block, program_id):
        """Извлекает все данные из одного блока программы"""
        program = {
            "id": program_id,
            "name": None,
            "code": None,
            "sphere": None,
            "career_prospects": None,
            "cost": None,
            "min_budget_score": None,
            "budget_places": None,
            "min_paid_score": None,
            "paid_places": None,
            "url": None,
        }

        title_elem = block.find("a", class_="spectittle")
        if title_elem:
            program["name"] = title_elem.get_text(strip=True)
            program["url"] = title_elem.get("href")
            if program["url"] and not program["url"].startswith("http"):
                program["url"] = self.base_url + program["url"]

        info_sm = block.find("div", class_="osnBlockInfoSm")
        if info_sm:
            text = info_sm.get_text(strip=True)
            program["code"] = self._extract_code(text)
            program["sphere"] = self._extract_sphere(text)

        low_reg = block.find("span", class_="lowReg")
        if low_reg:
            program["career_prospects"] = low_reg.get_text(strip=True)

        info_blocks = block.find_all("div", class_="mg10Prm")
        for info_block in info_blocks:
            header_tag = info_block.find("b")
            if not header_tag:
                continue
            header = header_tag.get_text(strip=True).lower()

            tooltip_links = info_block.find_all("a", class_="tooltipq")
            values = []
            for link in tooltip_links:
                text = link.get_text(strip=True)
                number = self._extract_number_from_text(text)
                if number is not None:
                    values.append(number)

            if header == "стоимость":
                if values:
                    program["cost"] = values[0]
            elif header == "бюджет":
                if len(values) >= 1:
                    program["min_budget_score"] = values[0]
                if len(values) >= 2:
                    program["budget_places"] = values[1]
            elif header == "платное":
                if len(values) >= 1:
                    program["min_paid_score"] = values[0]
                if len(values) >= 2:
                    program["paid_places"] = values[1]

        return program

    def _extract_code(self, text):
        """Извлекает код направления"""
        if not text:
            return None
        match = re.search(r"\d{2}\.\d{2}\.\d{2}", text)
        return match.group(0) if match else None

    def _extract_sphere(self, text):
        """Извлекает название направления после кода"""
        if not text:
            return None
        cleaned = re.sub(r"^\d{2}\.\d{2}\.\d{2}\s*", "", text)
        cleaned = re.sub(r"[|]\s*", "", cleaned)
        return cleaned.strip() if cleaned else None

    def _extract_number_from_text(self, text):
        """Извлекает целое число из текста"""
        if not text:
            return None
        numbers = re.findall(r"\d+", text)
        if numbers:
            return int(numbers[0])
        return None

    def _has_next_page(self, soup):
        """
        Проверяет наличие следующей страницы по пагинации в BeautifulSoup.
        Возвращает True, если есть следующий номер страницы.
        """
        pagination = soup.find("ul", class_="pagination")
        if not pagination:
            return False

        active = pagination.find("li", class_="active")
        if active:
            next_sibling = active.find_next_sibling("li")
            if next_sibling and next_sibling.find("a"):
                return True

        return False

    def run(
        self, username=None, password=None, use_manual_login=True, program_types=None, **kwargs
    ):
        """Запускает парсинг для одного или нескольких типов программ"""
        logger.info("Запускаем работу парсера Вузопедии")

        self.setup_driver()

        if not self.manual_login(username, password):
            logger.error("Не удалось выполнить вход")
            return {}

        if program_types is None:
            program_types = ["bachelor", "master"]
        elif isinstance(program_types, str):
            program_types = [program_types]

        results = {}
        for prog_type in program_types:
            logger.info(f"\n[{self.name}] Начинаю парсинг {prog_type} программ...")
            data = self.parse(program_type=prog_type, **kwargs)
            results[prog_type] = data
            logger.debug(f"[{self.name}] Для {prog_type} собрано {len(data)} программ")

        logger.info("Парсинг завершен")
        return results
