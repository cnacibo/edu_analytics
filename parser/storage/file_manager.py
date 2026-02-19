import json
import pandas as pd
from datetime import datetime
import os


class FileManager:
    @staticmethod
    def ensure_directory(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    @staticmethod
    def save_json(data, filename):
        FileManager.ensure_directory(filename)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'scraped_at': datetime.now().isoformat(),
                'total_items': len(data),
                'data': data
            }, f, ensure_ascii=False, indent=2)

    @staticmethod
    def save_parquet(data, filename):
        """Сохраняет данные в Parquet"""
        FileManager.ensure_directory(filename)
        df = pd.DataFrame(data)
        df.to_parquet(filename, engine='pyarrow')

    @staticmethod
    def save_csv(data, filename):
        """Сохраняет данные в CSV"""
        FileManager.ensure_directory(filename)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')