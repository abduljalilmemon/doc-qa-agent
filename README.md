
# Doc Q&A AI Agent

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)

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
curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d '{"q":"What is FastAPI?","top_k":3}'
```

## API
- GET /stats
- POST /upload
- POST /query
- POST /reset

## Extend
Replace naive answer with an LLM call, add tools, auth, rate limits, and monitoring.


## Publish to GitHub (quick guide)

```bash
git init
git add .
git commit -m "init: doc qa agent"
git branch -M main
# create a new empty repo on GitHub named: doc-qa-agent
git remote add origin https://github.com/abduljalilmemon/doc-qa-agent.git
git push -u origin main
```
