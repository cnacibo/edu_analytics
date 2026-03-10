import logging
import re
import time

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class VyzoPediaScraper(BaseScraper):
    def __init__(self, target_levels=None):
        super().__init__(base_url="https://vuzopedia.ru", name="VyzoPedia_Scraper")
        self.bachelor_url = "https://vuzopedia.ru/program/bakispec"
        self.master_base_url = "https://vuzopedia.ru/program/magistratura"
        self.program_counter = 1

    def parse(self, program_type="bachelor", max_pages=None, max_programs=None, retry_on_timeout=True):
        """
        Парсит страницы с программами

        Args:
            program_type: 'bachelor' или 'master'
            max_pages: максимальное количество страниц для парсинга (None - все)
            max_programs: максимальное количество программ для сбора (None - все)
            retry_on_timeout: делать ли повторные попытки при таймауте
        """
        if program_type == "bachelor":
            base_url = self.bachelor_url
        elif program_type == "master":
            base_url = self.master_base_url
        else:
            logger.error(f"Unknown program_type: {program_type}")
            return []

        all_programs = []
        page_num = 1

        while True:
            if page_num == 1:
                url = base_url
            else:
                url = f"{base_url}?page={page_num}"

            soup = None
            retry_count = 0
            max_retries = 3 if retry_on_timeout else 1

            while retry_count < max_retries:
                soup = self.fetch_page(url, delay=5)
                if soup:
                    break
                if retry_count < max_retries:
                    logger.warning(
                        f"Повторная попытка загрузки страницы {page_num} " f"({retry_count + 1}/{max_retries})"
                    )
                    time.sleep(5)
                retry_count += 1

            if not soup:
                logger.warning(f"Не удалось загрузить страницу {page_num}")
                break

            page_programs = self.parse_page(soup, page_num)
            if not page_programs:
                logger.info(f"Страница {page_num} пустая. Завершаем.")
                break

            all_programs.extend(page_programs)
            logger.info(f"Страница {page_num}: {len(page_programs)} программ. Всего: {len(all_programs)}")

            if max_programs and len(all_programs) >= max_programs:
                all_programs = all_programs[:max_programs]
                logger.info(f"Достигнут лимит в {max_programs} программ. Останавливаемся.")
                break

            if max_pages and page_num >= max_pages:
                logger.info(f"Достигнут лимит в {max_pages} страниц")
                break

            if not self._has_next_page(soup):
                logger.info("Это последняя страница. Завершаем.")
                break

            page_num += 1

        return all_programs

    def parse_page(self, soup, page_num):
        programs = []
        try:
            program_blocks = soup.find_all("div", class_="col-md-12 col-sm-6 blockNewItem")

            if not program_blocks:
                logger.warning(f"На странице {page_num} не найдено программ")
                return []
            logger.debug(f"На странице {page_num} найдено {len(program_blocks)} блоков")

            for i, block in enumerate(program_blocks, 1):
                try:
                    program_data = self._extract_program_data(block, page_num, i)
                    if program_data:
                        programs.append(program_data)
                except Exception as e:
                    logger.error(f"Ошибка при парсинге программы {i} на странице {page_num}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {page_num}: {e}")
        return programs

    def _extract_program_data(self, block, page_num, position):
        """
        Извлекает данные одной программы.
        """
        program = {
            "id": None,
            "name": None,
            "code": None,
            "cost": None,
            "min_budget_score": None,
            "min_paid_score": None,
            "sphere": None,
            "career_prospects": None,
            "budget_places": None,
        }

        title_elem = block.find("a", class_="spectittle")
        if title_elem:
            program["name"] = title_elem.text.strip()
        else:
            program["name"] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет названия")

        program["id"] = self.program_counter
        self.program_counter += 1

        info_blocks = block.find_all("div", class_="col-md-12 col-sm-4 col-xs-4 mg10Prm")
        for info_block in info_blocks:
            header_tag = info_block.find("center")
            if not header_tag:
                continue

            header_b = header_tag.find("b")
            if not header_b:
                continue

            block_type = header_b.text.strip().lower()

            has_no_data = False
            all_text = info_block.get_text(strip=True).lower()
            if "нет" in all_text and block_type not in all_text:
                has_no_data = True

            no_center = info_block.find("center", text=lambda t: t and "нет" in t.lower())
            if no_center:
                has_no_data = True

            for text_node in info_block.find_all(text=True):
                if text_node.strip().lower() == "нет":
                    has_no_data = True
                    break

            if has_no_data:
                continue

            tooltips = info_block.find_all("a", class_="tooltipq")

            if block_type == "стоимость" and tooltips:
                program["cost"] = self._extract_number(tooltips[0].text)
            elif block_type == "бюджет" and tooltips:
                if len(tooltips) > 0:
                    program["min_budget_score"] = self._extract_number(tooltips[0].text)
                if len(tooltips) > 1:
                    program["budget_places"] = self._extract_number(tooltips[1].text)
            elif block_type == "платное" and tooltips:
                program["min_paid_score"] = self._extract_number(tooltips[0].text)

        code_program = block.find_all("div", class_="osnBlockInfoSm")
        if code_program:
            program["code"] = self._extract_code(code_program[0].text.strip())
        else:
            program["code"] = None

        sphere_program = block.find_all("div", class_="osnBlockInfoSm")
        if sphere_program:
            program["sphere"] = self._extract_sphere(sphere_program[0].text.strip())
        else:
            program["sphere"] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет сферы")

        future_profession = block.find("span", class_="lowReg")
        if future_profession:
            program["career_prospects"] = future_profession.text.strip()
        else:
            program["career_prospects"] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет будущей профессии")

        return program

    def _extract_sphere(self, full_text):
        """Метод извлечения сферы программы"""
        if not full_text:
            return full_text
        match = re.search(r"[|\|]\s*(.+)$", full_text)
        if match:
            return match.group(1).strip()
        else:
            cleaned = re.sub(r"^\d+\.\d+\.\d+\s*", "", full_text)
        return cleaned.strip()

    def _extract_code(self, text):
        """Метод извлечения кода образовательной программы"""
        if not text:
            return None
        code_match = re.search(r"\d{2}\.\d{2}\.\d{2}", text)
        if code_match:
            return code_match.group(0)
        return None

    def _extract_number(self, text):
        """Извлекает число из текста"""
        if not text:
            return None
        numbers = re.findall(r"\d+", text)
        if numbers:
            return int(numbers[0])
        return None

    def _has_next_page(self, soup):
        """Проверяет, есть ли следующая страница в пагинации"""
        pagination = soup.find("ul", class_="pagination")
        if pagination:
            active_page = pagination.find("li", class_="active")
            if active_page:
                next_li = active_page.find_next_sibling("li")
                if next_li and next_li.find("a"):
                    return True
        return False

    def run(self):
        return self.parse()
