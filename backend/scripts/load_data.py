import csv
from pathlib import Path

from app.db.models import HseCourse, HseProgram, VuzopediaProgram
from app.db.session import AsyncSessionLocal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

DATA_DIR = Path("/app/storage/files")

PROGRAM_TYPE_TO_NAME = {
    "se": "Программная инженерия",
    "ami": "Прикладная математика и информатика",
}


async def map_hse_program_row(row, i, session):
    row.pop("id", None)
    return row


async def map_course_row(row, i, session):
    prog_type = row.get("program_type")
    if prog_type and prog_type in PROGRAM_TYPE_TO_NAME:
        name = PROGRAM_TYPE_TO_NAME[prog_type]
        result = await session.execute(
            text("SELECT id FROM hse_program WHERE name = :name"), {"name": name}
        )
        prog_id = result.scalar_one_or_none()
        if prog_id is None:
            print(f"⚠️  Warning: Program with code '{name}' not found for row {i}")
        else:
            row["program_id"] = prog_id
    else:
        print(f"⚠️  Warning: Unknown program_type '{prog_type}' at row {i}")
    row.pop("program_type", None)
    row.pop("url", None)
    row.pop("id", None)
    return row


async def map_vuzopedia_row(row, i, session):
    row.pop("id", None)
    row.pop("budget_places", None)
    return row


async def load_csv_to_db(
    dir_name: str, file_name: str, model_class, session: AsyncSession, extra_mapping=None
):
    file_path = DATA_DIR / dir_name / file_name

    if not file_path.exists():
        print(f"File {file_path} not found, skipping...")
        return

    table_name = model_class.__tablename__

    print(f"Loading {file_name} to {table_name}...")

    await session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        print(f"📊 Read {len(rows)} rows from CSV")
        if not rows:
            print("⚠️ No rows to insert")
            return

        model_fields = {c.name for c in model_class.__table__.columns}
        print(f"📋 Model fields: {model_fields}")

        records = []
        for i, row in enumerate(rows):
            if extra_mapping:
                row = await extra_mapping(row, i, session)

            filtered_row = {}

            for key, value in row.items():
                if key not in model_fields:
                    print(f"   Row {i}: skipping unknown field '{key}'")
                    continue

                if value == "":
                    filtered_row[key] = None

                elif key in [
                    "cost",
                    "budget_places",
                    "paid_places",
                    "credits",
                    "min_budget_score",
                    "min_paid_score",
                    "foreigners_places",
                ]:
                    try:
                        if value:
                            num = float(value)
                            col_type = model_class.__table__.columns[key].type.python_type
                            if col_type is int:
                                filtered_row[key] = int(num)
                            else:
                                filtered_row[key] = num
                        else:
                            filtered_row[key] = None
                    except (ValueError, TypeError):
                        print(f"   Row {i}: error converting {key}={value}")
                        filtered_row[key] = None
                else:
                    filtered_row[key] = value

            try:
                record = model_class(**filtered_row)
                records.append(record)
            except Exception as e:
                print(f"❌ Error creating record at row {i}: {e}")
                print(f"   Filtered row: {filtered_row}")
                raise

        session.add_all(records)
        print(f"➕ Added {len(records)} records")

    await session.commit()
    print(f"Successfully loaded {file_name}")


async def load_all_data():
    print("Starting data loading process...")
    async with AsyncSessionLocal() as session:
        try:
            await load_csv_to_db(
                "hse_programs",
                "hse_program.csv",
                HseProgram,
                session,
                extra_mapping=map_hse_program_row,
            )
            await load_csv_to_db(
                "hse_courses", "hse_course.csv", HseCourse, session, extra_mapping=map_course_row
            )
            await load_csv_to_db(
                "vuzopedia",
                "vuzopedia_program.csv",
                VuzopediaProgram,
                session,
                extra_mapping=map_vuzopedia_row,
            )
            print("All data loaded successfully!")

        except Exception as e:
            print(f"Error loading data: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(load_all_data())
