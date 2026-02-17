import csv
from pathlib import Path

from app.db.models import HseCourse, HseProgram, VuzopediaProgram
from app.db.session import AsyncSessionLocal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

DATA_DIR = Path("/app/parser/storage")


async def load_csv_to_db(file_name: str, model_class, session: AsyncSession):
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        print(f"File {file_path} not found, skipping...")
        return

    table_name = model_class.__tablename__

    print(f"Loading {file_name} to {table_name}...")

    await session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            for key, value in row.items():
                if value == "":
                    row[key] = None
                elif key in ["cost", "budget_places", "paid_places", "credits"]:
                    try:
                        row[key] = int(float(value)) if value else None
                    except (ValueError, TypeError):
                        row[key] = None
            records.append(model_class(**row))
        session.add_all(records)

    await session.commit()
    print(f"Successfully loaded {file_name}")


async def load_all_data():
    print("Starting data loading process...")
    async with AsyncSessionLocal() as session:
        try:
            await load_csv_to_db("vuzopedia_programs.csv", VuzopediaProgram, session)
            await load_csv_to_db("hse_programs.csv", HseProgram, session)
            await load_csv_to_db("hse_courses.csv", HseCourse, session)
            print("All data loaded successfully!")

        except Exception as e:
            print(f"Error loading data: {e}")
            await session.rollback()
            raise
