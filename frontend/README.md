
# Agent RAG Qdrant Frontend

This package contains the React UI that talks to the FastAPI backend and AI service inside the Agent RAG Qdrant monorepo. It provides a lightweight chat client, health/connection telemetry, and a document uploader that pushes files into the vector store.

## Features
- Chat workspace backed by Redux Toolkit with optimistic user messages, AI streaming placeholder handling, and localStorage persistence for refreshing without losing context.
- Connection indicator that pings the backend (`/api/healthz`) and the AI service (`/api/ai/healthz`) on load and on demand.
- Document uploader wired to `/api/ai/vectorstore/upload` so users can push PDFs/text files to Qdrant before chatting.
- Tailwind 4 utility styling, Lucide icons, React Router (single route today), and Playwright end-to-end tests.

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh


## Requirements
- Node.js 20 LTS (npm 10+) and a running backend + AI service (see repo root README for Docker instructions).
- Optional: `npx playwright install --with-deps` if you plan to run the browser tests locally.


## Setup

```bash
cd frontend
npm install
# edit `.env` (the repo ships one for Docker; create a local override if needed)
```

Update the environment file as needed:


| Variable | Description | Default |
| --- | --- | --- |
| `NODE_ENV` | Build mode for Vite | `development` |
| `BACKEND_API_BASE_URL` | Base URL for `/api/*` calls | `http://localhost:8000` (Docker `.env` points to `http://backend:8000`) |
| `VITE_TIMEOUT_MS` | Optional fetch timeout for health checks | `5000` |
| `VITE_FEATURE_X` | Placeholder feature flag used in `config.ts` | unset |

> Vite exposes variables prefixed with `VITE_` to the browser. Restart the dev server after changing them.

## Scripts
| Command | Description |
| --- | --- |
| `npm run dev` | Start the Vite dev server on http://localhost:5173 (expects backend/AI services to be reachable). |
| `npm run build` | Type-check (via `tsc -b`) and emit the production build into `dist/`. |
| `npm run preview` | Serve the built assets locally to sanity-check the production bundle. |
| `npm run lint` | Run ESLint with the shared flat config. |
| `npm run test:e2e` | Execute Playwright specs in `tests/e2e/` (backend + AI responses must be available). |


### End-to-end testing
1. Install the required browsers once: `npx playwright install --with-deps`.
2. Start the backend stack (Docker Compose or `uvicorn`) so `/api/ai/query` responds.
3. Run `npm run test:e2e` (or `npx playwright test --ui` for the inspector).
Playwright artifacts (reports, traces) are written to `playwright-report/` and `test-results/`.


## Project layout (highlights)

```
frontend/
├── src/
│   ├── features/
│   │   ├── messages/            # Chat UI (header, list, input) + RTK slice/thunks
│   │   ├── connectionCheck/     # Health check button + selectors
│   │   └── storeDocument/       # Document upload UI + API thunk
│   ├── services/                # Fetch helpers for health, AI query, document upload
│   ├── app/                     # Redux store, hooks, reducers
│   └── config.ts                # Centralized runtime config (reads Vite env vars)
├── tests/e2e/                   # Playwright specs (chat flow)
└── Dockerfile(.dev)             # Optional image builds used by the monorepo compose stack
```


## API expectations
- `GET /api/healthz` – backend readiness check (used by the connection widget).
- `GET /api/ai/healthz` – AI service health (same widget).
- `POST /api/ai/query` – accepts `{ query: string }` and returns `{ id, answer | result }`.
- `POST /api/ai/vectorstore/upload` – expects multipart form-data with `file`.


These routes are defined in the FastAPI backend; adjust `config.API_BASE_URL` if you proxy them differently.


## Troubleshooting
- **CORS / network errors:** confirm `BACKEND_API_BASE_URL` matches how the frontend reaches the backend (Docker vs local dev).
- **Messages disappear:** ensure localStorage is enabled; clear `localStorage['messages']` if the shape changes.
- **Health widget stuck on “Partial”:** the backend is up but the AI service is unreachable; check the AI container logs.
