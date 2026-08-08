# URL Shortener

A FastAPI microservice for shortening URLs with Redis caching, PostgreSQL storage, click statistics, and a simple web UI.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)](https://docker.com/)

## About

Shorten long URLs, share short links, and track how many times they were opened. Redirects are cached in Redis; persistent data lives in PostgreSQL. The same original URL always maps to the same short code (no duplicates).

## Tech Stack

| Layer | Technologies |
|-------|----------------|
| Backend | Python 3.13, FastAPI, Uvicorn, Pydantic |
| Database | PostgreSQL 16, SQLAlchemy 2 (async), Alembic, asyncpg |
| Cache | Redis 7 |
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Infra | Docker, Docker Compose |

## Features

- Shorten URLs via web UI or REST API
- Redirect by short code (`GET /{short_code}`)
- Optional link expiration (`expires_in` in seconds)
- Click statistics (`GET /api/v1/stats/{short_code}`)
- Redis caching for redirects
- Deterministic short codes (same URL → same code)
- Alembic migrations on container startup
- Swagger / OpenAPI docs at `/docs`

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

## How to Run on Your PC

### 1. Clone the repository

```bash
git clone https://github.com/Abdul4ik228/url_shortener.git
cd url_shortener
```

### 2. Start the stack

```bash
docker compose up --build -d
```

This starts three containers:

| Service | Role | Host port |
|---------|------|-----------|
| `web` | FastAPI app + UI | `8000` |
| `postgres` | Database | `5433` |
| `redis` | Cache | `6379` |

On first start, Alembic applies migrations automatically.

### 3. Open the app

| What | URL |
|------|-----|
| Web UI | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### 4. Stop

```bash
docker compose down
```

Remove containers **and** database volume:

```bash
docker compose down -v
```

### Useful commands

```bash
docker compose ps           # status
docker compose logs -f web  # app logs
```

## Configuration

Optional local overrides — copy the example env file:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Async PostgreSQL connection string |
| `REDIS_URL` | Redis connection URL |
| `SECRET_SALT` | Salt used for short-code generation |
| `BASE_DOMAIN` | Base URL used in generated short links |
| `REDIS_TTL` | Cache TTL in seconds (default `3600`) |

Docker Compose already sets these for the `web` service.

## API Examples

**Shorten a URL**

```bash
curl -X POST http://localhost:8000/api/v1/shorten \
  -H "Content-Type: application/json" \
  -d "{\"original_url\":\"https://example.com/very/long/path\",\"expires_in\":3600}"
```

`expires_in` is optional. Omit it for a non-expiring link.

**Redirect**

Open `http://localhost:8000/{short_code}` in a browser (HTTP 307).

**Stats**

```bash
curl http://localhost:8000/api/v1/stats/{short_code}
```

Example response:

```json
{
  "short_code": "49dX7vFV",
  "original_url": "https://example.com/very/long/path",
  "total_clicks": 3,
  "created_at": "2026-08-07T20:48:12.446322",
  "expires_at": "2026-08-07T21:48:12.449892"
}
```

## Project Structure

```text
url_shortener/
├── app/
│   ├── api/v1/          # HTTP endpoints
│   ├── core/            # short-code generator, exceptions
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # business logic
│   ├── static/          # web UI (HTML/CSS/JS)
│   ├── config.py
│   ├── database.py
│   ├── redis_client.py
│   └── main.py
├── migrations/          # Alembic migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
├── .env.example
└── main.py              # ASGI entry: uvicorn main:app
```

## License

Portfolio / learning project.
