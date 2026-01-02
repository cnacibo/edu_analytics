# 📊 Веб-приложение для анализа образовательных программ

### Исполнители:
- Власова Мария Андреевна 🎀
- Леденцова Виктория Алексеевна 🫦

### Цель проекта:

Создание веб-приложения для автоматического сбора, анализа
и визуализации данных об образовательных программах высших учебных
заведений с использованием современных технологий веб-разработки и
анализа данных.

### Структура:

```
edu_analytics/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── Dockerfile
├── db/
│   ├── base.py
│   ├── models.py
│   ├── session.py
│   ├── database.py
│   └── Dockerfile
├── ml/
│   ├── data/
│   ├── features/
│   ├── models
│   ├── notebooks/
│   ├── training_pipeline.py
│   └── Dockerfile
├── frontend/
│   ├── ...
│   └── Dockerfile
├── parser/
│   ├── scrapers/
│   ├── processors/
│   ├── storage/
│   ├── run.py
│   └── Dockerfile
├── .github/
│   ├── workflows/
│   │   └── ci.yaml
│   └──pull_request_template.md
├── docker-compose.yml
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── rules.md
└── README.md
```

### РБПО

#### Старт

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install ".[backend,ml,parser,dev]"
pre-commit install
```

#### Запуск
1.
```bash
uvicorn app.main:app --reload
```

2.
```bash
docker-compose up --build

docker-compose up backend frontend postgres # определенные сервисы

docker-compose down

docker-compose logs -f backend # просмотр логов
```

#### Шаги перед PR

```bash
ruff check . --fix
black .
isort .
pytest -q
pre-commit run --all-files
```
