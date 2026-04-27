import os
import re
from collections import Counter
from typing import Optional

import pandas as pd


class AnalysisCareerProspects:
    def __init__(self, input_path: Optional[str] = None):
        if input_path is None:
            script_dir = os.path.dirname(__file__)
            base_path = os.path.normpath(
                os.path.join(script_dir, "../..", "storage/files/vuzopedia_programs")
            )
            bachelor_path = os.path.join(base_path, "vuzopedia_bachelor_programs.csv")
            master_path = os.path.join(base_path, "vuzopedia_master_programs.csv")
            try:
                df_bachelor = pd.read_csv(bachelor_path)
                df_bachelor["level"] = "bachelor"
                df_master = pd.read_csv(master_path)
                df_master["level"] = "master"
                self.df = pd.concat([df_bachelor, df_master], ignore_index=True)
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Один из файлов не найден: {e}")
            except Exception as e:
                raise Exception(f"Ошибка чтения CSV: {e}")
        else:
            self.input_path = input_path
            try:
                self.df = pd.read_csv(self.input_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {self.input_path}")
            except Exception as e:
                raise Exception(f"Ошибка чтения CSV: {e}")

    def get_professions_wordcloud_data(self, top_n=100):
        """
        Извлекает профессии из столбца career_prospects, очищает,
        считает частоты. Возвращает список словарей [{"text": prof, "value": count}, ...]
        для передачи на фронтенд (или для локальной генерации).
        """
        professions = []
        excess_words = ["остальн", "другие", "и др", "и т.д"]
        for text in self.df["career_prospects"].dropna():
            parts = re.split(r"[,;]", text)
            for p in parts:
                p = p.strip().lower()
                if p and len(p) > 2 and not any(word in p for word in excess_words):
                    professions.append(p)

        freq = Counter(professions)
        most_common = freq.most_common(top_n)
        return dict(most_common)
