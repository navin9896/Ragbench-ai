# RAGBench AI

RAGBench AI is a full-stack Retrieval-Augmented Generation (RAG) evaluation and benchmarking platform. It includes:

- A FastAPI backend for querying the RAG pipeline and running evaluations.
- A React, TypeScript, and Vite dashboard for exploring results.
- Hybrid retrieval using vector search and BM25.
- Retrieval metrics including Recall@K, Precision@K, and MRR.
- Mock mode for running the project without an OpenAI API key.
- Small sample documents and a golden evaluation dataset.

## Project structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/          # Query, dashboard, and evaluation endpoints
│   │   ├── core/         # Application settings
│   │   ├── db/            # SQLAlchemy database and models
│   │   ├── evaluation/   # Evaluation harness and metrics
│   │   └── rag/          # Loading, chunking, retrieval, and generation
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── datasets/
│   ├── documents/        # Sample source documents
│   └── golden/           # Evaluation questions and expected results
├── frontend/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
└── scripts/
    ├── run_evaluation.py
    └── seed_demo.py
```

## Requirements

- Python 3.11 or newer
- Node.js 18 or newer
- npm

## Backend setup

From the project root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

The default configuration uses `MOCK_MODE=true`, so an OpenAI key is not required for a local demo. To use an OpenAI-backed provider, set the relevant values in `backend/.env`.

Start the API:

```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at http://127.0.0.1:8000. Interactive API documentation is available at http://127.0.0.1:8000/docs.

Health check:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/api/health
```

Run backend tests:

```powershell
cd backend
.\venv\Scripts\python.exe -m pytest tests
```

## Frontend setup

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173.

Production build and lint:

```powershell
cd frontend
npm run build
npm run lint
```

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/health` | Check API status |
| POST | `/api/query` | Run a RAG query |
| GET | `/api/dashboard/summary` | Read the latest evaluation summary |
| GET | `/api/evaluations` | List evaluation runs |
| GET | `/api/evaluations/{run_id}` | Read an evaluation run and its results |

Example query:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/query `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"query":"How long does standard shipping take?"}'
```

## Evaluation scripts

The sample dataset is in `datasets/golden/eval_dataset.json`. Evaluation and demo data scripts are in `scripts/`:

```powershell
cd backend
.\venv\Scripts\python.exe ..\scripts\seed_demo.py
.\venv\Scripts\python.exe ..\scripts\run_evaluation.py
```

## Configuration

Copy `backend/.env.example` to `backend/.env` and adjust:

- `MOCK_MODE`: use mock generation when `true`.
- `LLM_PROVIDER`: configured provider name.
- `OPENAI_API_KEY`: optional key for OpenAI-backed generation.
- `EMBEDDING_MODEL`: sentence-transformers embedding model.
- `DATABASE_URL`: SQLAlchemy database URL.
- `TOP_K`: number of chunks to retrieve.
- `RERANKER_ENABLED`: enable reranking when supported.

Local `.env` files and database files are intentionally ignored by Git.

## Current status

The backend test suite passes and the frontend production build succeeds. The frontend includes demo/mock presentation data for the dashboard and playground, while the backend exposes the production API routes for integration.

## License

Add the license that matches how you want this project to be used before distributing it publicly.
