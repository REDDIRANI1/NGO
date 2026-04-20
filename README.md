# NGO Monthly Reporting (Take‑Home)

Web app for NGOs to submit monthly reports (single + bulk CSV) and for admins to view an aggregated dashboard.

## Tech stack
- **Frontend**: Next.js (TypeScript)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Async jobs**: Celery + Redis

## Local setup (Docker)
Prereqs: Docker Desktop

1. Create env file:
   - Copy `.env.example` to `.env`
2. Start services:
   - `docker compose up --build`
3. Backend health check:
   - `GET http://localhost:8000/health`

## Local setup (Frontend)
Prereqs: Node.js 18+

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:3000`

## Project structure
- `frontend/`: Next.js app
- `backend/`: FastAPI app + Celery worker + Alembic migrations

