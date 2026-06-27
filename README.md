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

## Architecture

A monorepo with a FastAPI backend and a Next.js frontend, backed by PostgreSQL and Redis,
orchestrated with Docker Compose.

### Backend — layered

Requests flow through clear layers, so business rules live in one place and are easy to test:

```
router  →  service  →  repository  →  model (SQLAlchemy)
  │           │            │
  │           │            └─ DB access (queries, CRUD via a shared BaseRepository)
  │           └─ business rules + RBAC (e.g. CSM sees only own customers)
  └─ HTTP only: validate input (Pydantic schemas), call the service, return a response_model
```

- **`core/`** — cross-cutting setup: config (`pydantic-settings`), DB engine/session, Redis client,
  JWT/password security, centralized error handling (consistent `{error: {...}}` envelope),
  structured logging with request IDs, and the request middleware.
- **`deps/`** — FastAPI dependencies: `get_current_user`, and `require_roles(...)` for RBAC.
- **`schemas/`** — Pydantic request/response models (validation on the backend).
- **`alembic/`** — migrations (applied automatically on container startup).

### Frontend — Next.js App Router + Redux Toolkit

- **`store/slices/`** — one slice per feature (auth, customers, interactions, insights, dashboard).
  Async thunks call the typed API layer via **Axios**; the slice holds loading/error/data state.
- **`lib/axios.ts`** — single Axios instance: attaches the JWT, and on a 401 transparently refreshes
  the token once and retries.
- **`lib/api/`** — typed functions per resource; **`types/`** mirrors the backend schemas.
- **`components/`** — UI built with **shadcn/ui + Tailwind**, driven by a central design-token layer
  (semantic CSS variables for colors, customer-status and sentiment palettes, light/dark).
- Route protection + role-aware UI keep the frontend in step with the backend's RBAC.

### Data model

- **User** — `name, email, role (admin|manager|csm), is_active`
- **Customer** — `name, company, email, phone, status (prospect|active|at_risk|churned),
  health_score, assigned_csm_id → User, created_by_id → User`
- **Interaction** — `customer_id → Customer (cascade), type, title, notes, occurred_at`
- **Insight** — `interaction_id → Interaction, summary, sentiment, action_items[], risks[],
  status (success|fallback), model`

### RBAC

| Capability | Admin | Manager | CSM |
|------------|:-----:|:-------:|:---:|
| Manage users | ✅ | ❌ | ❌ |
| View / edit customers & interactions | all | all | own only |
| Delete customers | ✅ | ✅ | ❌ |
| Generate AI insights | ✅ | ✅ | own |
| Dashboard | global | global | scoped to own |

### AI insights

On request, an interaction's notes are sent to the model (DeepSeek V4 Flash via NVIDIA's
OpenAI-compatible endpoint, using the `openai` SDK). The response is **parsed** (handling code
fences / extra prose), **validated** against a schema, and stored. If anything fails — no API key,
network error, bad JSON — a neutral **fallback** insight is saved (`status="fallback"`) so the
request never errors.

### Caching

The **dashboard metrics** response is cached in Redis with a TTL, keyed by role scope. Any
customer / interaction / insight change **invalidates** the cache, so the dashboard never shows
stale data.

## Testing

```bash
# Backend (pytest, against an in-memory SQLite DB + fakeredis — no services needed)
cd backend && ./.venv/Scripts/python -m pytest

# Frontend (Vitest + React Testing Library, API mocked)
cd frontend && npm test
```

## Project Structure

```
EngageDash/
├── backend/
│   ├── app/
│   │   ├── core/          # config, db, redis, security, errors, logging, middleware
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── repositories/  # DB access (BaseRepository + per-entity)
│   │   ├── services/      # business logic + RBAC (incl. ai/ for insight generation)
│   │   ├── deps/          # auth + role-guard dependencies
│   │   ├── routers/       # API endpoints
│   │   ├── main.py        # app entrypoint (CORS, middleware, routers, OpenAPI)
│   │   └── seed.py        # demo data
│   ├── alembic/           # migrations
│   ├── tests/             # pytest suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js App Router pages ((auth) + (app) route groups)
│   │   ├── components/    # UI (ui/ = shadcn, layout/, customers/, insights/, ...)
│   │   ├── store/         # Redux store + slices + typed hooks
│   │   ├── lib/           # axios, api clients, helpers
│   │   ├── types/         # shared TS types
│   │   └── test/          # Vitest tests
│   └── Dockerfile
└── docker-compose.yml
```
