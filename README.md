# NGO Monthly Reporting (Take‑Home)

Web app for NGOs to submit monthly reports (single + bulk CSV) and for admins to view an aggregated dashboard.

## Tech stack
- **Frontend**: Next.js (TypeScript)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Async jobs**: Celery + Redis

## Features
- **Single report submission**: `POST /report` (idempotent upsert by `(ngo_id, month)`)
- **Bulk CSV upload**: `POST /reports/upload` returns a `job_id` and processes rows asynchronously
- **Job progress**: `GET /job-status/{job_id}` for progress + partial failures
- **Admin dashboard**: `GET /dashboard?month=YYYY-MM` aggregates totals for a month

## Pages
- `http://localhost:3000/submit`
- `http://localhost:3000/bulk-upload`
- `http://localhost:3000/admin/dashboard`

## Local setup (Docker)
Prereqs: Docker Desktop

1. Create env file:
   - Copy `.env.example` to `.env` (in repo root)
2. Start services:
   - `docker compose up --build`
3. Start the frontend (separate terminal):
   - `cd frontend && npm install && npm run dev`
4. Backend health check:
   - `GET http://localhost:8000/health`

## Local setup (Frontend)
Prereqs: Node.js 18+

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:3000`

Set the API base URL (optional):
- `frontend/.env.local`:
  - `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

## Local setup (Backend without Docker)
Prereqs: Python 3.12+, PostgreSQL, Redis

1. `cd backend`
2. `python -m venv .venv`
3. Activate venv
4. `pip install -r requirements.txt`
5. Set env vars (example):
   - `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ngo_reports`
   - `REDIS_URL=redis://localhost:6379/0`
6. Run migrations:
   - `alembic upgrade head`
7. Run API:
   - `uvicorn app.main:app --reload --port 8000`
8. Run worker (separate terminal):
   - `celery -A app.celery_app.celery_app worker --loglevel=INFO`

## API examples
### Submit a single report
```bash
curl -X POST "http://localhost:8000/report" \
  -H "content-type: application/json" \
  -d "{\"ngo_id\":\"NGO-123\",\"month\":\"2026-04\",\"people_helped\":120,\"events_conducted\":4,\"funds_utilized\":15000.50}"
```

### Get dashboard totals for a month
```bash
curl "http://localhost:8000/dashboard?month=2026-04"
```

### Bulk upload
CSV header must be:
`ngo_id,month,people_helped,events_conducted,funds_utilized`

```bash
curl -X POST "http://localhost:8000/reports/upload" \
  -F "file=@reports.csv"
```

Then poll:
```bash
curl "http://localhost:8000/job-status/<job_id>"
```

## Project structure
- `frontend/`: Next.js app
- `backend/`: FastAPI app + Celery worker + Alembic migrations

## Deployment notes (recommended)
- **Frontend**: Vercel (set `NEXT_PUBLIC_API_BASE_URL` to your API URL)
- **Backend**: Render (FastAPI web service) + Render worker (Celery) + managed Postgres + Redis (Render/Upstash)

## Where AI tools helped
- Used Cursor for scaffolding and iterating on backend/Next.js wiring and API ergonomics.

