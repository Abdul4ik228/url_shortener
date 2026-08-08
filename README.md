# URL Shortener

A small FastAPI service that shortens long URLs, redirects by short code, caches lookups in Redis, and tracks click stats. Includes a simple web UI and runs fully via Docker Compose.

## Features

- Create short links (`POST /api/v1/shorten`)
- Redirect by short code (`GET /{short_code}`)
- Optional link expiration
- Click statistics (`GET /api/v1/stats/{short_code}`)
- Redis caching for redirects
- Web UI at `/`
- PostgreSQL + Alembic migrations
- Docker Compose setup

## Tech Stack

- Python, FastAPI, SQLAlchemy (async), Alembic
- PostgreSQL, Redis
- Docker / Docker Compose
- Vanilla HTML/CSS/JS frontend

## Quick Start

### Requirements

- Docker Desktop

### Run

```bash
docker compose up --build -d
