# Fit-M Hackathon Backend
## Технологический стэк
Python FastAPI, Async SQLAlchemy.
Для нахождения похожих тематик статей используется Word2Vec.
Визуализация тепловой карты с помощью библиотеки Seaborn.

## Компоненты системы
app/app/api/endpoints

- article.py - список рекомендованных статей по тэгу
- auth.py - JWT авторизация
- feature.py - список симптомов
- heatmap.py - агрегация данных по пройденным анектам и генерация тепловой карты
- quiz.py - составление анкеты, прохождение анкеты, получение пройденных анкет
- user.py - получение списка пользователей
- ws.py - WebSocket для чата между пользователем и доктором

# Установка и исползование

## Python version
3.11
## Local
### Installation
#### FastAPI app
1. Create venv
```bash
python3.11 -m venv .venv
```

2. Activate venv
```bash
source .venv/bin/activate
```

3. Install requirements
```bash
pip install -r app/requirements/local.txt
```

Run ``pip freeze`` after project's first requirements installation to pin requirements' versions.

4. Copy .env
```bash
cp app/app/local.example.env app/app/.env
```

#### Docker and Docker compose
Refer to:

https://docs.docker.com/engine/install/

### Deploy

Use the script to start PSQL, PGAdmin in Docker Compose, apply migrations and run uvicorn:
```bash
make local
```

## Migrations
Powered by Alembic
```bash
make migraions
```

## Swagger Docs
Go to http://127.0.0.1:8000/api/docs after running server

## Development

During development use Black formatter, Pylint, Flake8 and MyPy.

## Prod

### Installation
Copy .env:
```bash
cp app/app/production.example.env app/app/.env
```

### Deploy
Use shortcut script:
```bash
make up
```
