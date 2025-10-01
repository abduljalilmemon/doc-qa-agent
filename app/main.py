import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from .schemas import QuerySchema
from .storage import DocumentStore
from .ingest import ingest_file
from .retriever import search

STORE_PATH = os.environ.get("STORE_PATH", "store.pkl")
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Doc Q&A Agent", version="1.0.0")
store = DocumentStore(persist_path=STORE_PATH)
store.load()

@app.get("/stats")
def get_stats():
    return store.stats()

@app.post("/upload")
async def upload(file: UploadFile = File(...), doc_id: str | None = None):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename.")
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".txt", ".md", ".csv", ".pdf"]:
        raise HTTPException(status_code=400, detail="Only .txt/.md/.csv/.pdf supported.")
    doc_id = doc_id or str(uuid.uuid4())
    dest = os.path.join(UPLOAD_DIR, f"{doc_id}{ext}")
    content = await file.read()
    with open(dest, "wb") as f:
        f.write(content)
    info = ingest_file(dest, store, doc_id=doc_id)
    return {"success": True, **info}

@app.post("/query")
def query(payload: QuerySchema):
    return search(store, payload.query, max_results=payload.max_results)

@app.post("/reset")
def reset():
    store.reset()
    return {"success": True, "message": "Cleared index."}
