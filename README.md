# Agent RAG Qdrant

AI Agent & Qdrant is a small experimental monorepo that brings together basic Model Context Protocol (MCP) components and a Qdrant vector store. The project’s goal is to explore how to build a simple Retrieval-Augmented Generation (RAG) setup in one place, where tools, agents, and workflows can be tested and updated without managing multiple repos.

---

Quickstart: MCP example with Qdrant, ai_service (stub), backend (FastAPI), frontend (Vite React)

1) Build and run (requires Docker Compose):
   docker compose up --build

2) Services
   - Backend (FastAPI): http://localhost:8000
     - Health: http://localhost:8000/api/health/
     - AI endpoint: http://localhost:8000/api/ai/query (POST)

   - AI Service (stub): http://localhost:8001
     - Health: http://localhost:8001/health
     - Query: http://localhost:8001/v1/query (POST)

   - Qdrant: http://localhost:6333 (used in stub)

3) Example curl:
   curl -X POST http://localhost:8000/api/ai/query -H "Content-Type: application/json" -d '{"query":"hello"}'

Notes:
 - The `frontend_builder` service builds the Vite frontend and copies the build into a NGINX container.

---

MCP Monorepo project structure with AI service, FastAPI, Redaction Gate MCP, and React UI

- A Python AI service (e.g., using LangChain/OpenAI)
- A Python FastAPI backend (providing API endpoints)
- A React frontend

```
agent_rag_qdrant/
│
├── .github/
│   └── workflow/
│       └── github-actions.yml
│
├── ai_service/                # Python AI service (LangChain/OpenAI logic)
│   ├── main.py
│   ├── requirements.txt
│   └── ... (other modules)
│
├── backend/                   # FastAPI backend (serves API)
│   ├── main.py
│   ├── requirements.txt
│   └── ... (routers, models, etc.)
│
├── frontend/                  # React UI
│   ├── package.json
│   ├── public/
│   └── src/
│
├── redaction_gate/                # Python Redact FastMCP/FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── ... (other modules)
│
├── docker-compose.yml
└── README.md
```

**Details:**

- `ai_service/`: Contains the core AI logic, can be run as a separate service or imported by the backend.
- `backend/`: FastAPI app, can serve API endpoints.
- `frontend/`: React app (created with Create React App, Vite, or similar).
- docker-compose.yml: Orchestrates all services (Qdrant, AI service, FastAPI backend, React frontend in NGINX).
- `redaction_gate/`: FastMCP service, can serve MCP.

**Key Points:**
- The `frontend` service builds the React app and outputs to `frontend/build`.
- The `backend` serves API endpoints.
- The `ai_service` can be a separate microservice or imported by the backend.


---

**Before Deploy**

- Add `.env` file under *./ai_service/* and define **OPENAI_API_KEY=[API_KEY]** to enable access to OpenAI. 

----

# Development Environment

- Execute deploy dev mode with the following docker compose command:

```bash
docker compose -f docker-compose.yml -f docker-compose.overwrite.dev.yml up -d --build
```