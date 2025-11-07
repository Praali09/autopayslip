# Automatic Salary Slip Generator (Gov Institute) - Starter Project
## Overview
This project is a production-ready **starter scaffold** for an Automatic Salary Slip Generator targeted at government institutes.
It includes:
- FastAPI backend with SQLAlchemy models
- Salary engine (configurable)
- Payslip HTML template -> PDF generation (WeasyPrint)
- Celery worker stub for asynchronous email sending
- React + Vite frontend (admin portal skeleton)
- Docker & docker-compose for local development
- Sample data and steps to run locally

IMPORTANT: This scaffold is intended as a full working starting point. You should review and secure it before production (secrets, email provider, TLS, PII handling).

## Project structure
```
auto_payslip_project/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ models.py
│  │  ├─ database.py
│  │  ├─ schemas.py
│  │  ├─ crud.py
│  │  ├─ salary_engine.py
│  │  ├─ payslip_template.html
│  │  ├─ mailer.py
│  │  └─ requirements.txt
│  ├─ Dockerfile
│  └─ docker-entrypoint.sh
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.js
│  └─ src/
│     ├─ main.jsx
│     └─ App.jsx
├─ docker-compose.yml
└─ README.md
```

## Quickstart (local, development)
Prereqs:
- Docker & docker-compose OR Python 3.10+, Node 18+
- (Optional) Redis for Celery if using real queue

Option A: Run with Docker (recommended)
1. Build and start containers:
   ```bash
   docker compose up --build
   ```
2. Backend API will be at http://localhost:8000
3. Frontend at http://localhost:5173

Option B: Run locally without Docker
Backend:
```bash
cd backend/app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Notes & Next Steps (for gov submission)
- Replace email stubs in `mailer.py` with a secure SMTP provider (use environment variables)
- Configure database credentials and enable encryption at rest on deployed DB
- Implement admin auth 2FA and secure secret management
- Add auditing, backups, and data retention policies
- Add unit/integration tests and a small sample dataset for UAT
- Consider replacing WeasyPrint with an approved PDF generator if required by policy

-- End of README --


## How to run seed & tests

- To seed sample employees:

```
# inside backend/app virtualenv or container
python -m app.seed
```

- To run unit tests (pytest):

```
# inside backend directory
pytest
```
