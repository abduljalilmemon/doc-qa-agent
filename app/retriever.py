import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .storage import DocumentStore

def search(store: DocumentStore, query: str, max_results: int = 5):
    if not store.vectorizer or store.tfidf is None or not store.chunks:
        return {"answer": None, "matches": [], "note": "Index is empty. Upload documents first."}
    qv = store.vectorizer.transform([query])
    sims = cosine_similarity(qv, store.tfidf)[0]
    idxs = np.argsort(-sims)[:max_results]
    matches = []
    for rank, i in enumerate(idxs, 1):
        ch = store.chunks[int(i)]
        matches.append({
            "rank": rank,
            "score": float(sims[int(i)]),
            "doc_id": ch.doc_id,
            "pos": ch.pos,
            "text": ch.text[:500],
            "meta": ch.meta,
        })
    answer = matches[0]["text"] if matches else None
    return {"answer": answer, "matches": matches}
