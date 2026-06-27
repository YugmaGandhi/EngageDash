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
# 1. Configure environment (backend/.env is the source of truth)
cp backend/.env.example backend/.env   # then set AI_API_KEY and a strong JWT_SECRET_KEY

# 2. Build and launch the full stack (the backend runs DB migrations on startup)
docker compose up --build -d

# 3. Load demo data so you can try every feature
docker compose exec backend python -m app.seed

# 4. Stop it
docker compose down                     # add -v to also drop the Postgres volume (wipes data)
```

The stack starts four services with healthchecks; the frontend waits for the backend, which
waits for Postgres and Redis to be healthy. The backend applies database migrations automatically
on startup.

### Demo data & what to try

After running the seed (step 3 above), open http://localhost:3000 and sign in with any of these:

| Role | Email | Password | What they can do |
|------|-------|----------|------------------|
| Admin | `admin@engagedash.com` | `Admin@123` | Everything + the **Users** page (change roles, activate/deactivate) |
| Manager | `manager@engagedash.com` | `Manager@123` | See **all** customers/interactions; can delete customers |
| CSM | `csm@engagedash.com` | `Csm@12345` | Only their **own** assigned customers |

Suggested walkthrough:

1. **Log in as the CSM** → the **Dashboard** shows KPIs, a status breakdown, a sentiment breakdown
   (from seeded insights), and recent interactions — all scoped to this user.
2. **Customers** → search/filter, open **Acme Corp** (active) or **Globex** (at risk), **edit** one,
   and **create** a new customer. Notice the CSM has **no delete** button.
3. Open an interaction (e.g. Acme's "Quarterly business review") → **AI Insights** card → click
   **Generate insight**. With a valid `AI_API_KEY` you get a real analysis; without one it stores a
   graceful **fallback** (still no errors).
4. **Log in as the Manager** → you now also see **Umbrella Co** (churned, owned by the manager) and
   can **delete** customers.
5. **Log in as the Admin** → the sidebar shows **Users**; change a user's role or deactivate them.
6. Create a customer, then return to the **Dashboard** → the numbers update immediately (the Redis
   cache is invalidated on changes, so no stale data).

| Service     | URL                          | Notes                          |
|-------------|------------------------------|--------------------------------|
| Frontend    | http://localhost:3000        | Next.js app                    |
| Backend API | http://localhost:8000        | FastAPI                        |
| Swagger UI  | http://localhost:8000/docs   | Interactive API docs           |
| ReDoc       | http://localhost:8000/redoc  | Alternative API docs           |
| PostgreSQL  | localhost:5432               | user/db from `backend/.env`    |
| Redis       | localhost:6379               | cache                          |

> **Ports** 3000/8000/5432/6379 must be free on the host. If one is taken, stop the
> conflicting process or adjust the port mapping in `docker-compose.yml`.

### Environment variables

Configuration is per app, with no root env file:

- **`backend/.env`** — the backend's single source of truth (Postgres, Redis, JWT, AI provider,
  cache TTL). Written for local dev (hosts = `localhost`); when running via Docker, compose
  overrides only `POSTGRES_HOST`/`REDIS_HOST` with the service names. See
  [`backend/.env.example`](./backend/.env.example).
- **`frontend/.env.local`** — only `NEXT_PUBLIC_API_URL` (for running `npm run dev` outside Docker).
  See [`frontend/.env.example`](./frontend/.env.example). In Docker this is baked in at build time.

Env files are gitignored; never commit real secrets. The AI provider is DeepSeek V4 Flash via
NVIDIA's free OpenAI-compatible endpoint — set `AI_API_KEY` in `backend/.env`.

### Run locally without Docker

```bash
# Postgres + Redis via Docker, apps run directly
docker compose up -d postgres redis
cd backend && cp .env.example .env && ./.venv/Scripts/python -m alembic upgrade head \
  && ./.venv/Scripts/python -m uvicorn app.main:app --reload   # http://localhost:8000
cd frontend && cp .env.example .env.local && npm run dev        # http://localhost:3000
```

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
