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

> _Detailed instructions land in Phase 0.7 / Phase 11. Outline below._

```bash
# 1. Configure environment
cp .env.example .env   # then fill in values (incl. AI_API_KEY)

# 2. Launch the full stack
docker compose up --build
```

Services (once running):

| Service     | URL                          |
|-------------|------------------------------|
| Frontend    | http://localhost:3000        |
| Backend API | http://localhost:8000        |
| Swagger UI  | http://localhost:8000/docs   |
| ReDoc       | http://localhost:8000/redoc  |

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
