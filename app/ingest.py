import os
from .storage import DocumentStore, Chunk
from .utils import split_sentence
from pypdf import PdfReader

def get_text(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in [".txt", ".md", ".csv"]:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext in [".pdf"]:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .txt/.md/.csv/.pdf")

def get_chunks(sentences = [], target_chars = 500, overlap = 60):
    chunks = []
    buf = ""
    for sent in sentences:
        if not buf:
            buf = sent
        elif len(buf) + 1 + len(sent) <= target_chars:
            buf += " " + sent
        else:
            chunks.append(buf.strip())
            tail = buf[-overlap:] if overlap else ""
            buf = (tail + " " + sent).strip()
    if buf:
        chunks.append(buf.strip())
    return chunks

def ingest_file(path: str, store: DocumentStore, doc_id: str):
    text = get_text(path)
    sents = split_sentence(text)
    chunk_texts = get_chunks(sents, target_chars=500, overlap=60)
    new_chunks = [Chunk(text=ct, doc_id=doc_id, pos=i, meta={"source_path": path}) for i, ct in enumerate(chunk_texts)]
    store.add_chunks_and_rebuild(new_chunks)
    store.save()
    return {"doc_id": doc_id, "chunks_added": len(new_chunks)}
