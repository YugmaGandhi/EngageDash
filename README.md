# EngageDash

> AI-powered **Customer Success Insights Dashboard** — manage customers and interactions,
> generate structured AI insights from meeting notes, and view operational metrics.

A full-stack platform with secure authentication, role-based access control, validation on both
ends, AI response handling, Redis caching, and a fully containerized setup.

## Tech Stack

- **Frontend:** Next.js (App Router) · TypeScript · Redux Toolkit · Tailwind CSS + shadcn/ui · Axios
- **Backend:** Python · FastAPI · SQLAlchemy 2.0 + Alembic · Pydantic v2
- **Data:** PostgreSQL · Redis
- **Auth:** JWT (access + refresh) · RBAC (`admin` / `manager` / `csm`)
- **AI:** DeepSeek V4 Flash via NVIDIA's OpenAI-compatible endpoint
- **DevOps:** Docker · Docker Compose

## Quick Start

### Prerequisites

- **Docker Desktop** (with Docker Compose v2) — the only requirement to run the full stack.
- For local development outside Docker: **Python 3.13+** (backend) and **Node.js 22+** (frontend).

### Run with Docker (recommended)

```bash
# 1. Configure environment
cp .env.example .env        # then edit .env and set AI_API_KEY (and a strong JWT_SECRET_KEY)

# 2. Build and launch the full stack
docker compose up --build   # add -d to run detached

# 3. Stop it
docker compose down          # add -v to also drop the Postgres volume (wipes data)
```

The stack starts four services with healthchecks; the frontend waits for the backend, which
waits for Postgres and Redis to be healthy.

| Service     | URL                          | Notes                          |
|-------------|------------------------------|--------------------------------|
| Frontend    | http://localhost:3000        | Next.js app                    |
| Backend API | http://localhost:8000        | FastAPI                        |
| Swagger UI  | http://localhost:8000/docs   | Interactive API docs           |
| ReDoc       | http://localhost:8000/redoc  | Alternative API docs           |
| PostgreSQL  | localhost:5432               | user/db from `.env`            |
| Redis       | localhost:6379               | cache                          |

> **Ports** 3000/8000/5432/6379 must be free on the host. If one is taken, stop the
> conflicting process or adjust the port mapping in `docker-compose.yml`.

### Environment variables

All configuration lives in the root **`.env`** (see [`.env.example`](./.env.example) for the full,
documented list — Postgres, Redis, JWT, AI provider, cache TTL, and frontend API URL).
`.env` is gitignored; never commit real secrets.

The AI provider is DeepSeek V4 Flash via NVIDIA's free OpenAI-compatible endpoint — set
`AI_API_KEY` to your NVIDIA key.

## Documentation

- **[docs/PLAN.md](./docs/PLAN.md)** — master plan: architecture, data model, RBAC matrix, phased roadmap.
- **[docs/phases/](./docs/phases)** — detailed per-phase stage breakdowns and progress tracking.

## Project Structure

```
EngageDash/
├── backend/    # FastAPI app
├── frontend/   # Next.js app
├── docs/       # planning & phase docs
└── docker-compose.yml
```
