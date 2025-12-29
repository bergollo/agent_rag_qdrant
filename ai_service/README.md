# Agent RAG Qdrant AI Service

FastAPI microservice that powers semantic search and LLM orchestration for the Agent RAG Qdrant stack. It exposes health probes, a `/v1/query` endpoint that enriches prompts with Qdrant hits, and a `/v1/vectorstore/upload` route that embeds uploaded documents before storing them in the vector DB.

## Features
- Async router set built on FastAPI with permissive CORS for local prototyping.
- `OpenAIClient` wrapper that streams chat completions, creates embeddings, and keeps the `documents` collection ready in Qdrant.
- Document ingestion pipeline that extracts text (PDF + plain text), generates embeddings, and writes payloads/metadata into Qdrant.
- Semantic search helper used by `/v1/query` to build context-aware prompts before calling the chat model.
- Pytest suite covering routers, service helpers, and error handling for both LLM and vectorstore flows.

## Requirements
- Python 3.11+
- OpenAI API key with access to `gpt-3.5-turbo` and `text-embedding-3-small` (swap models in `OpenAIClient` as needed).
- Reachable Qdrant instance (Docker Compose stack provides one on `http://qdrant:6333`).
- Optional: Docker to run via `docker compose up ai_service`.

## Setup

```bash
cd ai_service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # create your own if missing
```

Environment variables (loaded through `pydantic-settings`):

| Variable | Description | Default |
| --- | --- | --- |
| `APP_NAME` | FastAPI title | `AI Service Stub` |
| `HOST` / `PORT` | Uvicorn bind address | `0.0.0.0` / `8001` |
| `OPENAI_API_KEY` | Required for chat + embedding calls | unset |
| `QDRANT_URL` | Base URL for vector store | `http://qdrant:6333` |

## Scripts
| Command | Description |
| --- | --- |
| `uvicorn app.main:app --reload --port 8001` | Start the dev server with hot reload. |
| `pytest` | Execute unit tests under `tests/`. |
| `docker build -t ai_service .` | Build the production image (used in Compose). |

## API surface
- `GET /healthz/` – readiness probe used by the backend proxy.
- `POST /v1/vectorstore/upload` – accepts `multipart/form-data` (`file`) and stores embeddings/payloads in Qdrant.
- `POST /v1/query/` – body `{ "query": "..." }`; performs semantic search + OpenAI completion and returns `{ "answer": "..." }`.

## Project layout

```
ai_service/
├── app/
│   ├── api/
│   │   ├── deps.py            # DI helpers (OpenAI client)
│   │   └── routers/           # health, vectorstore, llm
│   ├── core/config.py         # Settings + env handling
│   ├── services/open_ai.py    # OpenAI + Qdrant integration
│   └── main.py                # FastAPI factory
├── tests/                     # pytest coverage for routers + services
├── requirements.txt
└── Dockerfile(.dev)
```

## Troubleshooting
- **401 from OpenAI:** ensure `OPENAI_API_KEY` is present in `.env` or container env vars.
- **Qdrant timeouts:** confirm `QDRANT_URL` is reachable from the ai_service container; Compose defaults to the `qdrant` service hostname.
- **Empty embeddings:** binary/non-text uploads must be PDF or UTF-8/Latin-1 decodable; otherwise `_extract_text` returns an empty string and triggers a 400.

Run this service alongside the FastAPI backend (`/api/ai/*` proxies) and Vite frontend via `docker compose up --build` from the repo root for the full RAG workflow.
