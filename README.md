# DataSherlock 
**Autonomous AI agent that ingests raw datasets, profiles data quality, detects anomalies, and generates interactive dashboards with zero manual intervention.**

---

## Tech Stack
| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Data Processing | Polars + DuckDB |
| LLM | Groq API (Llama 3.1 70B) + Ollama fallback |
| Agent Framework | LangChain + LangGraph |
| Task Queue | Dramatiq + Redis |
| Dashboard | Apache Superset |
| ML / Stats | scikit-learn, SciPy, statsmodels, PyOD |

---

## Prerequisites
- Python 3.11+
- Redis (local or Docker)
- Docker & Docker Compose (for full stack)
- A Groq API key → https://console.groq.com

---

## Option A — Run Locally (without Docker)

### 1. Clone & set up environment
```bash
git clone <your-repo>
cd datasherlock
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Open .env and set your GROQ_API_KEY
```

### 3. Start Redis (required for Dramatiq worker)
```bash
# If you have Redis installed locally:
redis-server

# OR use Docker just for Redis:
docker run -d -p 6379:6379 redis:7-alpine
```

### 4. Start the API server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the Dramatiq worker (separate terminal)
```bash
dramatiq worker.celery_worker
```

### 6. Visit the API docs
Open: http://localhost:8000/docs

---

## Option B — Run with Docker Compose (recommended)

### 1. Configure environment variables
```bash
cp .env.example .env
# Set your GROQ_API_KEY in .env
```

### 2. Build and start all services
```bash
cd docker
docker-compose up --build
```

This starts:
- **API** → http://localhost:8000
- **API Docs** → http://localhost:8000/docs
- **Redis** → localhost:6379
- **Superset** → http://localhost:8088

### 3. Initialize Superset (first time only)
```bash
docker exec -it datasherlock_superset superset fab create-admin \
    --username admin --firstname Admin --lastname User \
    --email admin@example.com --password admin

docker exec -it datasherlock_superset superset db upgrade
docker exec -it datasherlock_superset superset init
```

---

## Running Tests
```bash
# Install test deps (already in requirements.txt)
pytest tests/ -v

# With coverage
pytest tests/ -v --tb=short
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/upload/` | Upload a dataset (CSV/Excel/JSON/Parquet) |
| GET | `/api/v1/upload/{dataset_id}` | Get dataset info |
| GET | `/api/v1/profiling/{dataset_id}` | Full data profiling + DQI score |
| GET | `/api/v1/profiling/{dataset_id}/drift?reference_id=X` | Drift detection |
| GET | `/api/v1/insights/{dataset_id}` | Rule-based insights + feature suggestions |
| POST | `/api/v1/ask/` | Ask AI a question about your dataset |
| POST | `/api/v1/dashboard/{dataset_id}/generate` | Auto-generate dashboard |

---

## Quick Usage Example

```bash
# 1. Upload a CSV
curl -X POST http://localhost:8000/api/v1/upload/ \
  -F "file=@your_data.csv"

# Returns: { "dataset_id": "abc-123", "rows": 500, ... }

# 2. Get profiling + DQI
curl http://localhost:8000/api/v1/profiling/abc-123

# 3. Ask AI about your data
curl -X POST http://localhost:8000/api/v1/ask/ \
  -H "Content-Type: application/json" \
  -d '{"dataset_id": "abc-123", "question": "What columns have the most missing data?"}'

# 4. Generate dashboard
curl -X POST http://localhost:8000/api/v1/dashboard/abc-123/generate
```

---

## Project Structure
```
datasherlock/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── config.py            # Settings from .env
│   ├── api/routes/          # Upload, Profiling, Insights, Ask, Dashboard
│   ├── core/
│   │   ├── ingestion/       # Loader, validator, schema inference
│   │   ├── profiling/       # DQI, missing, outliers, correlation, drift
│   │   ├── insights/        # Rule engine, root cause, feature suggestions
│   │   ├── llm/             # Groq agent, Ollama fallback, tools
│   │   ├── dashboard/       # Chart selector, Superset client, builder
│   │   └── tasks/           # Dramatiq actors
│   ├── db/                  # DuckDB connection & queries
│   ├── schemas/             # Pydantic models
│   └── utils/               # Logger, constants, helpers
├── worker/                  # Dramatiq worker entry
├── tests/                   # pytest test suite
├── docker/                  # Dockerfile + docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

## LLM Configuration

**Primary: Groq (recommended)**
```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama3-70b-8192
```

**Fallback: Ollama (local/offline)**
```bash
# Install Ollama: https://ollama.com
ollama pull llama3
```
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```
The system automatically falls back to Ollama if Groq is unavailable.

