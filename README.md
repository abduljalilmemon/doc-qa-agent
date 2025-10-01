# Doc Q&A AI Agent

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Upload `.txt/.md/.csv/.pdf` files and ask questions via API. Retrieval is powered by scikit-learn TF-IDF; no external services are required.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

**Upload:**
```bash
curl -F "file=@sample_data/sample.txt" http://127.0.0.1:8000/upload
```

**Query:**
```bash
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"query":"What is FastAPI?","max_results":3}'
```

## API
- GET /stats
- POST /upload
- POST /query
- POST /reset

## Extend
Replace naive answer with an LLM call, add tools, auth, rate limits, and monitoring.