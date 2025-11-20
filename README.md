# Agent RAG Qdrant

AI Agent & Qdrant is a small experimental monorepo that brings together basic Model Context Protocol (MCP) components and a Qdrant vector store. The project’s goal is to explore how to build a simple Retrieval-Augmented Generation (RAG) setup in one place, where tools, agents, and workflows can be tested and updated without managing multiple repos.

MCP Monorepo project structure with AI service, FastAPI, and React UI

- A Python AI service (e.g., using LangChain/OpenAI)
- A Python FastAPI backend to host a React UI (serving static files and providing API endpoints)
- A React frontend

```
agent_rag_qdrant/
│
├── ai_service/                # Python AI service (LangChain/OpenAI logic)
│   ├── main.py
│   ├── requirements.txt
│   └── ... (other modules)
│
├── backend/                   # FastAPI backend (serves API + React UI)
│   ├── main.py
│   ├── requirements.txt
│   └── ... (routers, models, etc.)
│
├── frontend/                  # React UI
│   ├── package.json
│   ├── public/
│   └── src/
│
├── docker-compose.yml
└── README.md
```

**Details:**

- `ai_service/`: Contains the core AI logic, can be run as a separate service or imported by the backend.
- `backend/`: FastAPI app, can serve API endpoints and static files from the built React app.
- `frontend/`: React app (created with Create React App, Vite, or similar).
- docker-compose.yml: Orchestrates all services (Qdrant, AI service, FastAPI backend, React frontend if needed).

**Key Points:**
- The `frontend` service builds the React app and outputs to `frontend/build`.
- The `backend` serves the built React UI as static files and exposes API endpoints.
- The `ai_service` can be a separate microservice or imported by the backend.
