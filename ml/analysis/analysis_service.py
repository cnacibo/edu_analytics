import math
import os
from typing import Any, Dict, List, Optional

import pandas as pd


class AnalysisService:
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
                self.input_path = None
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

    def get_max_budget_score(self) -> int:
        if "min_budget_score" not in self.df.columns:
            raise ValueError("Столбца 'min_budget_score' нет в датасете vuzopedia_program.csv")
        return int(self.df["min_budget_score"].max())

    def get_min_paid_score(self) -> int:
        if "min_paid_score" not in self.df.columns:
            raise ValueError("Столбца 'min_paid_score' нет в датасете vuzopedia_program.csv")
        return int(self.df["min_paid_score"].min())

    def get_average_cost(self) -> float:
        if "cost" not in self.df.columns:
            raise ValueError("Столбца 'cost' нет в датасете vuzopedia_program.csv")
        return self.df["cost"].mean()

    def get_all_programs(self) -> int:
        return self.df.shape[0]

    def _get_top_n_programs(self, n: int = 10) -> pd.DataFrame:
        """
        Возвращает DataFrame с топ-N программами по стоимости.
        Убирает строки, где стоимость неизвестна
        """
        required_cols = ["name", "cost", "min_budget_score", "min_paid_score", "level"]
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Отсутствуют столбцы: {missing}")

        data = self.df[required_cols].dropna(subset=["cost"])
        data_sorted = data.sort_values("cost", ascending=False)
        unique_programs = data_sorted.drop_duplicates(subset=["name"], keep="first")
        top_n = unique_programs.head(n)

        return top_n

    def get_top_ten_programs(self) -> List[Dict[str, Any]]:
        """
        Возвращает список словарей с топ-10 программами по стоимости.
        """
        top10_df = self._get_top_n_programs(10)
        records = top10_df.to_dict(orient="records")

        for record in records:
            for key, value in record.items():
                if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                    record[key] = None
        return records

    def get_avg_cost_top10(self) -> float:
        """
        Средняя стоимость среди топ-10 программ.
        """
        top10_df = self._get_top_n_programs(10)
        return top10_df["cost"].mean()

    def get_pie_chart(self):
        """
        Возвращает список словарей: {'sphere': название сферы, 'count': количество программ}
        для построения круговой диаграммы.
        """
        required_cols = ["name", "sphere"]
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Отсутствуют столбцы: {missing}")
        data = self.df[required_cols].dropna(subset=["sphere"])
        grouped = data.groupby("sphere").size().reset_index(name="count")
        top10 = grouped.sort_values("count", ascending=False).head(6)
        return top10.to_dict(orient="records")

    def get_bar_chart(self):
        """
        Возвращает список словарей:
        {  it: {
            bachelor: 600000,
            master: 700000,
            }
        }
        для каждой сферы средняя цена обучения по уровню программы
        """
        required_cols = ["sphere", "level", "cost"]
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Отсутствуют столбцы: {missing}")
        data = self.df.pivot_table(
            index="sphere",
            columns="level",
            values="cost",
            aggfunc="mean",
            fill_value=0,
        ).reset_index()
        program_counts = self.df.groupby("sphere").size().reset_index(name="count")
        data = data.merge(program_counts, on="sphere", how="left")
        data = data.sort_values("count", ascending=False).head(7)
        data = data.drop(columns=["count"])
        data = data.to_dict(orient="records")
        return {item.pop("sphere"): item for item in data}
