# scrapers/vyzopedia.py (упрощенная версия)
import re
import time

from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class VyzoPediaScraper(BaseScraper):
    def __init__(self, target_levels=None):
        super().__init__(
            base_url='https://vuzopedia.ru',
            name='VyzoPedia_Scraper'
        )
        self.bachelor_url = 'https://vuzopedia.ru/program/bakispec'
        self.master_base_url = 'https://vuzopedia.ru/program/magistratura'
        self.program_counter = 1

    def parse(self, program_type='bachelor', max_pages=None, retry_on_timeout=True):
        """
        Парсит все страницы с программами

        Args:
            program_type: 'bachelor' или 'master'
            max_pages: максимальное количество страниц для парсинга (None - все)
        """

        if program_type == 'bachelor':
            base_url = self.bachelor_url
        elif program_type == 'master':
            base_url = self.master_base_url
        else:
            logger.error(f'Unknown program_type: {program_type}')
            return []

        all_programs = []
        page_num = 1
        while True:
            if page_num == 1:
                url = base_url
            else:
                url = f'{base_url}?page={page_num}'
            # logger.info(f'Парсис страницу {page_num}')
            soup = None
            retry_count = 0
            max_retries = 3 if retry_on_timeout else 1

            while retry_count < max_retries:
                soup = self.fetch_page(url, delay=2)
                if soup:
                    break
                if retry_count < max_retries:
                    logger.warning(f"Повторная попытка загрузки страницы {page_num} ({retry_count}/{max_retries})")
                    time.sleep(5)
            if not soup:
                logger.warning(f"Не удалось загрузить страницу {page_num}")
                break

            page_programs = self.parse_page(soup, page_num)
            if not page_programs:
                logger.info(f"Страница {page_num} пустая. Завершаем.")
                break

            all_programs.extend(page_programs)
            logger.info(f"Страница {page_num}: {len(page_programs)} программ. Всего: {len(all_programs)}")

            # if page_num % 5 == 0:
            #     self._save_intermediate_results(all_programs, page_num)

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
            program_blocks = soup.find_all('div', class_='col-md-12 col-sm-6 blockNewItem')

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
            НАЧИНАЕМ ТОЛЬКО С НАЗВАНИЯ, постепенно будем добавлять поля.
        """
        program = {
            'id': None,
            'program_name': None,
            'id_program': None,
            'min_cost': None,
            'min_point_for_budget': None,
            'min_point_for_paid': None,
            'sphere': None,
            'who_will_be_in_the_future': None
        }

        #extract program name
        title_elem = block.find('a', class_='spectittle')
        if title_elem:
            program['program_name'] = title_elem.text.strip()
        else:
            program['program_name'] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет названия")

        program['id'] = self.program_counter
        self.program_counter += 1

        # extract info blocks
        # info_blocks = block.find_all('div', class_='col-md-12 col-sm-4 col-xs-4 mg10Prm')
        # for info_block in info_blocks:
        #     header = info_block.find('center').find('b')
        #     header1 = info_block.select_one('center:has"нет"')
        #     if header:
        #         block_type = header.text.strip().lower()
        #         tooltips = info_block.find_all('a', class_='tooltipq')
        #         if block_type == 'стоимость' or 'нет' in header1.text:
        #             program['min_cost'] = self._extract_number(tooltips[0].text)
        #         elif block_type == 'бюджет' or 'нет' in header1.text :
        #             program['min_point_for_budget'] = self._extract_number(tooltips[0].text)
        #         elif block_type == 'платное' or 'нет' in header1.text:
        #             program['min_point_for_paid'] = self._extract_number(tooltips[0].text)
        #         else:
        #             logger.warning('Не удалось спарсить((')

        info_blocks = block.find_all('div', class_='col-md-12 col-sm-4 col-xs-4 mg10Prm')
        for info_block in info_blocks:
            # Находим заголовок блока
            header_tag = info_block.find('center')
            if not header_tag:
                continue

            header_b = header_tag.find('b')
            if not header_b:
                continue

            block_type = header_b.text.strip().lower()

            # Проверяем, есть ли в блоке текст "нет" (любой из вариантов)
            has_no_data = False

            # Вариант 1: Находим все текстовые узлы в блоке и проверяем на "нет"
            all_text = info_block.get_text(strip=True).lower()
            if 'нет' in all_text and block_type not in all_text:
                has_no_data = True

            # Вариант 2: Ищем <center> с текстом "нет"
            no_center = info_block.find('center', text=lambda t: t and 'нет' in t.lower())
            if no_center:
                has_no_data = True

            # Вариант 3: Ищем просто текст "нет" вне center
            for text_node in info_block.find_all(text=True):
                if text_node.strip().lower() == 'нет':
                    has_no_data = True
                    break

            # Если в блоке есть "нет", пропускаем его
            if has_no_data:
                continue

            # Если данных нет, парсим tooltips
            tooltips = info_block.find_all('a', class_='tooltipq')

            if block_type == 'стоимость' and tooltips:
                program['min_cost'] = self._extract_number(tooltips[0].text)
            elif block_type == 'бюджет' and tooltips:
                if len(tooltips) > 0:
                    program['min_point_for_budget'] = self._extract_number(tooltips[0].text)
                if len(tooltips) > 1:
                    program['budget_places'] = self._extract_number(tooltips[1].text)
            elif block_type == 'платное' and tooltips:
                program['min_point_for_paid'] = self._extract_number(tooltips[0].text)

        # cost_block = block.find('div', class_='col-md-12 col-sm-4 col-xs-4 mg10Prm')
        # if cost_block:
        #     header = cost_block.find('b')
        #     if header and 'стоимость' in header.text.lower():
        #         if not block_has_no_data(cost_block):
        #             tooltip = cost_block.find('a', class_='tooltipq')
        #             if tooltip:
        #                 program['min_cost'] = self._extract_number(tooltip.text)
        #
        # budget_block = block.find('div', class_='col-md-12 col-sm-4 col-xs-4 mg10Prm')
        # if budget_block:
        #     header = budget_block.find('b')
        #     if header and 'бюджет' in header.text.lower():
        #         if not block_has_no_data(budget_block):
        #             tooltip = budget_block.find_all('a', class_='tooltipq')
        #             if tooltip:
        #                 program['min_point_for_budget'] = self._extract_number(tooltip[0].text)
        #
        # paid_block = block.find('div', class_='col-md-12 col-sm-4 col-xs-4 mg10Prm')
        # if paid_block:
        #     header = paid_block.find('b')
        #     if header and 'платное' in header.text.lower():
        #         if not block_has_no_data(paid_block):
        #             tooltip = paid_block.find_all('a', class_='tooltipq')
        #             if tooltip:
        #                 program['min_point_for_paid'] = self._extract_number(tooltip[0].text)


        # extract id program
        code_program = block.find_all('div', class_='osnBlockInfoSm')
        if code_program:
            program['id_program'] = self._extract_code(code_program[0].text.strip())
        else:
            program['id_program'] = None

        # extract sphere
        sphere_program = block.find_all('div', class_='osnBlockInfoSm')
        if sphere_program:
            program['sphere'] = self._extract_sphere(sphere_program[0].text.strip())
        else:
            program['sphere'] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет сферы")



        # extract future_profession
        future_profession = block.find('span', class_='lowReg')
        if future_profession:
            program['who_will_be_in_the_future'] = future_profession.text.strip()
        else:
            program['who_will_be_in_the_future'] = None
            logger.warning(f"На странице {page_num}, позиция {position}: нет будущей профессии")


        return program

    def _extract_sphere(self, full_text):
        if not full_text:
            return full_text
        match = re.search(r'[|\|]\s*(.+)$', full_text)
        if match:
            return match.group(1).strip()
        else:
            cleaned = re.sub(r'^\d+\.\d+\.\d+\s*', '', full_text)
        return cleaned.strip()


    def _extract_code(self, text):
        if not text:
            return None
        code_match = re.search(r'\d{2}\.\d{2}\.\d{2}', text)
        if code_match:
            return code_match.group(0)
        return None

    def _extract_number(self, text):
        """Извлекает число из текста"""
        if not text:
            return None
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0])
        return None

    def _has_next_page(self, soup):
        """Проверяет, есть ли следующая страница в пагинации"""
        # Ищем элемент пагинации
        pagination = soup.find('ul', class_='pagination')
        if pagination:
            # Ищем активную страницу
            active_page = pagination.find('li', class_='active')
            if active_page:
                # Проверяем, есть ли следующая ссылка после активной
                next_li = active_page.find_next_sibling('li')
                if next_li and next_li.find('a'):
                    return True
        return False

    def run(self):
        return self.parse()


    def _save_intermediate_results(self, programs, current_page):
        """Сохраняет промежуточные результаты
        ПОКА ЧТО НЕ СОХРАНЯЮ (использовала для того чтобы увидеть промежуточные резы)"""
        try:
            import csv
            filename = f'intermediate_page_{current_page}.csv'

            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['id', 'program_name', 'id_program', 'min_cost', 'min_point_for_budget', 'min_point_for_paid', 'sphere', 'who_will_be_in_the_future']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

                for program in programs:
                    row = {field: program.get(field, '') for field in fieldnames}
                    writer.writerow(row)

            logger.info(f"Сохранены промежуточные результаты ({len(programs)} программ) в {filename}")

        except Exception as e:
            logger.error(f"Ошибка при сохранении промежуточных результатов: {e}")