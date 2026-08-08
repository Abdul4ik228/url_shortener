# 🔗 URL Shortener

> A microservice for shortening URLs with Redis caching and a web interface

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql)](https://postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker)](https://docker.com/)

---

## 📖 About The Project

This service allows you to shorten long URLs, get short links, and track click statistics. All requests are cached in Redis for maximum speed, while data is stored in PostgreSQL.

**Key Feature:** The same URL always generates the same short code — no duplicates!  
**Bonus:** A web interface for easy usage.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✂️ **URL Shortening** | Convert long URLs to short 6-character codes |
| ⏱️ **TTL Support** | Set expiration time for links (in seconds) |
| 📊 **Statistics** | Track click count for each short link |
| ⚡ **Caching** | Redis accelerates redirects by 10x+ |
| 🖥️ **Web Interface** | Beautiful UI to interact with the service |
| 📚 **Swagger Docs** | Auto-generated API documentation |

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.11 |
| **Framework** | FastAPI |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Migrations** | Alembic |
| **Containerization** | Docker + Docker Compose |
| **Frontend** | Vanilla HTML/CSS/JS |

---

## 🚀 Quick Start

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Abdul4ik228/url_shortener.git
cd url_shortener
