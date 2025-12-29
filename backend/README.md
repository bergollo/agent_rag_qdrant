# Agent RAG Qdrant Backend

FastAPI gateway that fronts the Agent RAG Qdrant stack. It exposes `/api/*` routes consumed by the Vite frontend, proxies AI calls to the `ai_service`, and offers a place to mount the compiled React app for production deployments.

## Features
- Router set for health checks, AI query forwarding, and document uploads that feed the vectorstore.
- Async `AIClient` built on httpx for delegating work to the AI microservice while handling file uploads and error propagation.
- Centralized configuration via `pydantic-settings`, making Docker/Compose overrides straightforward.
- CORS middleware enabled for local development; tighten in production by whitelisting frontend origins.
- Pytest coverage for routers and the HTTP client to guard against regressions.

## Requirements
- Python 3.11+
- Running `ai_service` instance (Docker Compose provides it on `http://ai_service:8001`).
- Optional: built frontend in `backend/static` if you want the backend to serve UI assets.
- Docker recommended for parity with the rest of the stack.

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # create one if you need overrides
```

Environment variables (loaded through `pydantic-settings`):

| Variable | Description | Default |
| --- | --- | --- |
| `APP_NAME` | FastAPI title | `MCP Backend` |
| `HOST` / `PORT` | Uvicorn bind address | `0.0.0.0` / `8000` |
| `AI_SERVICE_URL` | Base URL of the AI microservice | `http://ai_service:8001` |
| `QDRANT_URL` | Reserved for future direct DB calls | `http://qdrant:6333` |

## Scripts
| Command | Description |
| --- | --- |
| `uvicorn app.main:app --reload --port 8000` | Run the API locally with auto-reload. |
| `pytest` | Execute backend unit tests. |
| `docker build -t backend .` | Build the backend container image (used by Compose). |

## API surface
- `GET /api/healthz` – backend readiness probe.
- `GET /api/ai/healthz` – proxies the downstream AI service health check.
- `POST /api/ai/vectorstore/upload` – forwards `multipart/form-data` uploads to the AI service for ingestion.
- `POST /api/ai/query` – body `{ "query": "..." }`; returns `{ "answer": "..." }` supplied by the AI service.

## Project layout

```
backend/
├── app/
│   ├── core/config.py        # Settings + env handling
│   ├── api/
│   │   ├── deps.py           # FastAPI dependencies (settings, AI client)
│   │   └── routers/          # health + ai proxy routes
│   ├── services/ai_client.py # httpx wrapper for ai_service
│   └── main.py               # FastAPI factory + middleware
├── static/                   # Optional mount point for built frontend assets
├── tests/                    # pytest suites for routers + services
├── requirements.txt
└── Dockerfile(.dev)
```

## Troubleshooting
- **CORS errors in the browser:** update the allowed origins list in `app/main.py` when deploying to non-localhost domains.
- **500 from `/api/ai/*`:** verify `ai_service` is reachable (check `docker compose ps` or hit `http://localhost:8001/healthz` directly).
- **File uploads fail instantly:** FastAPI reads the file into memory before proxying; large files may need adjusted limits or chunked ingestion in future iterations.

Run this service together with `ai_service` and the frontend via `docker compose up --build` from the repo root to exercise the entire RAG workflow.
