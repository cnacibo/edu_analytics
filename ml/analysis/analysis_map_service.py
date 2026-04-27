import math
import os
from typing import Optional

import pandas as pd


class AnalysisMapService:
    def __init__(self, input_path: Optional[str] = None):
        if input_path is None:
            script_dir = os.path.dirname(__file__)
            base_dir = os.path.normpath(os.path.join(script_dir, "../..", "storage/files"))

            cities_bachelor_path = os.path.join(
                base_dir, "program_cities", "programs_cities_bachelor.csv"
            )
            cities_master_path = os.path.join(
                base_dir, "program_cities", "programs_cities_master.csv"
            )

            cost_bachelor_path = os.path.join(
                base_dir, "vuzopedia_programs", "vuzopedia_bachelor_programs.csv"
            )
            cost_master_path = os.path.join(
                base_dir, "vuzopedia_programs", "vuzopedia_master_programs.csv"
            )

            try:
                df_cities_bachelor = pd.read_csv(cities_bachelor_path)
                df_cities_bachelor = df_cities_bachelor.rename(columns={"program_name": "name"})
                df_cities_bachelor["level"] = "bachelor"

                df_cities_master = pd.read_csv(cities_master_path)
                df_cities_master = df_cities_master.rename(columns={"program_name": "name"})
                df_cities_master["level"] = "master"

                df_cities = pd.concat([df_cities_bachelor, df_cities_master], ignore_index=True)

                df_cost_bachelor = pd.read_csv(cost_bachelor_path)
                df_cost_bachelor["level"] = "bachelor"

                df_cost_master = pd.read_csv(cost_master_path)
                df_cost_master["level"] = "master"

                required_cols = ["name", "level", "cost"]
                df_cost = pd.concat([df_cost_bachelor, df_cost_master], ignore_index=True)
                df_cost = df_cost[required_cols].drop_duplicates(subset=["name", "level"])
                self.df = df_cities.merge(df_cost, on=["name", "level"], how="left")
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

    def get_bachelor_programs_map(self):
        bachelor_df = self.bachelor.copy()
        bachelor_df["id"] = range(1, len(bachelor_df) + 1)
        avg_cost = bachelor_df["cost"].mean()
        bachelor_df["flag"] = bachelor_df["cost"] < avg_cost
        records = bachelor_df.to_dict(orient="records")
        return self.nan_processing(records)

    def get_master_programs_map(self):
        master_df = self.master.copy()
        master_df["id"] = range(1, len(master_df) + 1)
        avg_cost = master_df["cost"].mean()
        master_df["flag"] = master_df["cost"] < avg_cost
        records = master_df.to_dict(orient="records")
        return self.nan_processing(records)

    def get_avg_cost_of_cities(self):
        required_cols = ["name", "city", "cost"]
        missing = [col for col in required_cols if col not in self.df.columns]
        if missing:
            raise ValueError(f"Отсутствуют столбцы: {missing}")
        data = self.df[required_cols].dropna(subset=["city", "cost"])
        grouped = data.groupby("city")["cost"].mean().reset_index()
        grouped.columns = ["city", "avg_cost"]
        grouped["avg_cost"] = round(grouped["avg_cost"], 2)
        grouped["program_count"] = data.groupby("city").size().values
        top10 = grouped.sort_values("program_count", ascending=False).head(30)
        records = top10.to_dict(orient="records")
        return self.nan_processing(records)

    @staticmethod
    def nan_processing(records):
        for item in records:
            cost = item["cost"]
            if cost is None or (isinstance(cost, float) and math.isnan(cost)):
                item["cost"] = None
        return records

    @property
    def bachelor(self):
        return self.df[self.df["level"] == "bachelor"]

    @property
    def master(self):
        return self.df[self.df["level"] == "master"]


def main():
    service = AnalysisMapService()
    a = service.get_bachelor_programs_map()
    print(a[0:10])


if __name__ == "__main__":
    main()
