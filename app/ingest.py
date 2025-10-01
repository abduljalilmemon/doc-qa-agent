import os
from pypdf import PdfReader
from .storage import DocumentStore, Chunk
from .utils import split_sentence

def get_text(path):
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
    buffer = ""
    for sentence in sentences:
        if not buffer:
            buffer = sentence
        elif len(buffer) + 1 + len(sentence) <= target_chars:
            buffer += " " + sentence
        else:
            chunks.append(buffer.strip())
            tail = buffer[-overlap:] if overlap else ""
            buffer = (tail + " " + sentence).strip()
    if buffer:
        chunks.append(buffer.strip())
    return chunks

def ingest_file(path: str, store: DocumentStore, doc_id: str):
    text = get_text(path)
    sents = split_sentence(text)
    chunk_texts = get_chunks(sents, target_chars=500, overlap=60)
    new_chunks = [Chunk(text=ct, doc_id=doc_id, pos=i, meta={"source_path": path}) for i, ct in enumerate(chunk_texts)]
    store.add_chunks_and_rebuild(new_chunks)
    store.save()
    return {"doc_id": doc_id, "chunks_added": len(new_chunks)}
