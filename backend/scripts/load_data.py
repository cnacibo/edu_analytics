import csv
from pathlib import Path

from app.db.models import City, CityVuzopediaProgram, HseCourse, HseProgram, VuzopediaProgram
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
    if "cost" in row and row["cost"] and row["cost"].strip():
        try:
            original_cost_str = row["cost"].strip()
            original_cost = float(original_cost_str)
            new_cost = original_cost * 1000
            row["cost"] = str(new_cost)
        except (ValueError, TypeError) as e:
            print(f"   Row {i}: error converting cost '{row['cost']}': {e}")
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
    row.pop("id", None)
    return row


async def map_vuzopedia_bachelor_row(row, i, session):
    row.pop("id", None)
    row["study_type"] = "Бакалавр"
    return row


async def map_vuzopedia_master_row(row, i, session):
    row.pop("id", None)
    row["study_type"] = "Магистр"
    return row


async def load_cities_and_relations_to_db(session: AsyncSession):
    print("\nLoading cities and relations to DB...")
    files = [
        ("program_cities", "programs_cities_bachelor.csv"),
        ("program_cities", "programs_cities_master.csv"),
    ]
    city_cache: dict[str, int] = {}
    relation_cache: set[tuple[int, int]] = set()
    created_cities = 0
    created_relations = 0

    table_name_city = City.__tablename__
    table_name_city_vuz = CityVuzopediaProgram.__tablename__

    await session.execute(
        text(
            f"TRUNCATE TABLE {table_name_city_vuz}, {table_name_city} " f"RESTART IDENTITY CASCADE"
        )
    )
    print(f"   Truncated tables {table_name_city_vuz} and {table_name_city}")

    for dir_name, file_name in files:
        file_path = DATA_DIR / dir_name / file_name

        if not file_path.exists():
            print(f"File {file_path} not found, skipping...")
            continue

        print(f"\nProcessing {file_name}...")
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"📊 Read {len(rows)} rows from CSV")
            if not rows:
                print("⚠️ No rows to insert")
                continue

            for i, row in enumerate(rows):
                program_name = row.get("program_name", "").strip()
                city_name = row.get("city", "").strip()
                lat_str = row.get("latitude", "").strip()
                lon_str = row.get("longitude", "").strip()

                if not program_name or not city_name:
                    continue

                result_program = await session.execute(
                    text("SELECT id FROM vuzopedia_program WHERE name = :name"),
                    {"name": program_name},
                )
                prog_row = result_program.first()
                if not prog_row:
                    print(f"⚠️ Program not found: '{program_name}'")
                    continue
                program_id = prog_row.id

                if city_name in city_cache:
                    city_id = city_cache[city_name]
                else:
                    result_city = await session.execute(
                        text("SELECT id FROM city WHERE name = :name"), {"name": city_name}
                    )
                    city_id = result_city.first()
                    if not city_id:
                        lat = float(lat_str) if lat_str else None
                        lon = float(lon_str) if lon_str else None
                        city = City(name=city_name, latitude=lat, longitude=lon)
                        session.add(city)
                        await session.flush()
                        city_id = city.id
                        created_cities += 1
                    city_cache[city_name] = city_id

                key = (city_id, program_id)
                if key not in relation_cache:
                    relation_cache.add(key)
                    session.add(
                        CityVuzopediaProgram(
                            city_id=city_id,
                            vuzopedia_program_id=program_id,
                        )
                    )
                    created_relations += 1
        print(f"Successfully loaded {file_name}")
    await session.commit()
    print(f"\n➕ Added {created_cities} cities and {created_relations} relations")


async def load_csv_to_db(
    dir_name: str,
    file_name: str,
    model_class,
    session: AsyncSession,
    extra_mapping=None,
    truncate_first: bool = True,
):
    file_path = DATA_DIR / dir_name / file_name

    if not file_path.exists():
        print(f"File {file_path} not found, skipping...")
        return

    table_name = model_class.__tablename__

    print(f"\nLoading {file_name} to {table_name}...")

    if truncate_first:
        await session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        print(f"   Truncated table {table_name}")

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
                "vuzopedia_programs",
                "vuzopedia_bachelor_programs.csv",
                VuzopediaProgram,
                session,
                extra_mapping=map_vuzopedia_bachelor_row,
            )
            await load_csv_to_db(
                "vuzopedia_programs",
                "vuzopedia_master_programs.csv",
                VuzopediaProgram,
                session,
                extra_mapping=map_vuzopedia_master_row,
                truncate_first=False,
            )
            await load_cities_and_relations_to_db(session)
            print("All data loaded successfully!")

        except Exception as e:
            print(f"Error loading data: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    import asyncio

    asyncio.run(load_all_data())
