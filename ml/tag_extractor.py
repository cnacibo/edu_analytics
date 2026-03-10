"""
- Выполняется подготовка перед обработкой: скачивание стоп-слов и пунктуации
- Реализуется класс TagExtractor:
    - Конструктор:
        language: str = "ru"      - язык текста для yake
        max_ngram: int = 3        - максмальная длина рассматриваемых слов
        num_keywords: int = 15):  - количество ключевых слов, которые yake возвращает до фильтрации

Далее класс выполняет следующее:
    - Очищает текста от цифр, спецсимволы
    - Извлекает подходящие слова с помощью YAKE
    - Фильтрует подходящие слова по длине, стоп-словам, частям речи
      (через библиотеку pymorphy2) и исключение глаголов
    - Добавление известных терминов из внутреннего словаря
      (garbage_phrases и self.known_terms)
    - Извлекает аббревиатуры
    - Удаляет дубликаты
"""

import re
from typing import List, Set, Tuple

import nltk
import pymorphy2
import yake

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")
from nltk.corpus import stopwords


class TagExtractor:
    def __init__(self, language: str = "ru", max_ngram: int = 3, num_keywords: int = 15):

        self.language = language
        self.yake_extractor = yake.KeywordExtractor(
            lan=language, n=max_ngram, dedupLim=0.5, top=num_keywords, windowsSize=1
        )
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = set(stopwords.words("russian"))

        self.garbage_phrases = {
            "в конце",
            "должен уметь",
            "быть в состоянии",
            "объяснить",
            "рассказать",
            "применять",
            "использовать",
            "сформулировать",
            "описать",
            "обосновать",
            "подготовиться",
            "понимать",
            "основной",
            "компетенция",
            "результат",
            "обучение",
            "лекция",
            "практика",
            "семинар",
            "лабораторный",
        }

        self.known_terms = {
            "agile",
            "safe",
            "scrum",
            "kanban",
            "devops",
            "wsjf",
            "art",
            "less",
            "xp",
            "saFe",
            "SAFe",
            "Agile",
            "бережливый",
            "гибкий",
            "портфель",
            "эпик",
            "lean",
            "поток ценности",
            "непрерывная поставка",
            "pi planning",
            "agile release trains",
            "кросс функциональный",
            "бережливое управление",
            "цифровые технологии",
        }
        self.known_terms_lower = {term.lower() for term in self.known_terms}

    def clean_text(self, text: str) -> str:
        """Очистка текста от мусора."""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"\d+[\)\.]", " ", text)
        text = re.sub(r"[^а-яa-z0-9\-]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_abbreviations(self, text: str) -> Set[str]:
        """Извлекает аббревиатуры типа SAFe, ART, WSJF."""
        abbr_pattern = r"\b([A-Z]{2,}|[A-Z][a-z]*[A-Z][A-Za-z]*)\b"
        matches = re.findall(abbr_pattern, text)
        abbreviations = set()
        for match in matches:
            if len(match) >= 2:
                if match.isupper():
                    abbreviations.add(match)
                elif len(match) > 3 and match[0].isupper():
                    abbreviations.add(match)
        return abbreviations

    def _is_valid_by_pos(self, phrase: str) -> bool:
        """
        Проверяет фразу по частям речи:
        - Если фраза есть в known_terms → пропускаем.
        - Одно слово: должно быть существительным или прилагательным.
        - Два слова: допустимые комбинации: прил+сущ, сущ+сущ.
        - Три слова и более: не пропускаем (кроме known_terms).
        """
        phrase_lower = phrase.lower()
        if phrase_lower in self.known_terms_lower:
            return True

        words = phrase.split()
        if not words:
            return False
        if phrase.isupper():
            return True

        pos_list = []
        for word in words:
            if len(word) < 2:
                return False
            parse = self.morph.parse(word)[0]
            pos = parse.tag.POS
            if pos is None:
                if word.endswith(("ing", "ed", "tion", "ать", "ить", "еть")):
                    return False
                pos_list.append("NOUN")
            else:
                pos_list.append(pos)

        if len(words) == 1:
            return pos_list[0] in ("NOUN", "ADJF", "ADJS")

        if len(words) == 2:
            if pos_list[0] in ("ADJF", "ADJS") and pos_list[1] == "NOUN":
                return True
            if pos_list[0] == "NOUN" and pos_list[1] == "NOUN":
                return True
            return False
        return False

    def filter_candidates(self, candidates: List[Tuple[str, float]]) -> List[str]:
        """Фильтрует кандидатов, оставляя только подходящие."""
        good_tags = []
        for phrase, score in candidates:
            phrase_lower = phrase.lower()
            if len(phrase_lower) < 3:
                continue
            if any(garbage in phrase_lower for garbage in self.garbage_phrases):
                continue
            if not any(c.isalpha() for c in phrase_lower):
                continue

            words = phrase_lower.split()
            if len(words) > 3:
                continue

            verb_endings = ("ать", "ить", "еть", "уть", "ють", "аются", "яются")
            if any(phrase_lower.endswith(ending) for ending in verb_endings):
                continue

            if len(words) == 2:
                word1, word2 = words
                if word1 in self.stop_words and word2 in self.stop_words:
                    continue
                if word1 in self.stop_words and len(word2) < 4:
                    continue

            if not self._is_valid_by_pos(phrase):
                continue

            good_tags.append(phrase_lower)
        return good_tags[:10]

    def enhance_with_vocabulary(self, tags: Set[str], text: str) -> Set[str]:
        """Добавляет известные термины."""
        enhanced = set(tags)
        text_lower = text.lower()
        for term in self.known_terms:
            term_lower = term.lower()
            if term_lower in text_lower:
                pattern = r"\b" + re.escape(term_lower) + r"\b"
                if re.search(pattern, text_lower):
                    enhanced.add(term)
        return enhanced

    def extract(self, text: str) -> List[str]:
        """Основной метод извлечения тегов."""
        original_text = text
        cleaned_text = self.clean_text(text)
        abbreviations = self.extract_abbreviations(original_text)

        try:
            yake_candidates = self.yake_extractor.extract_keywords(cleaned_text)
            yake_tags = self.filter_candidates(yake_candidates)
        except Exception as e:
            print(f"Ошибка YAKE: {e}")
            yake_tags = []

        all_tags = set(abbreviations) | set(yake_tags)
        all_tags = self.enhance_with_vocabulary(all_tags, original_text)

        final_set = set()
        for tag in all_tags:
            if tag.isupper():
                final_set.add(tag)
            else:
                final_set.add(tag.capitalize())
        return sorted(final_set)
