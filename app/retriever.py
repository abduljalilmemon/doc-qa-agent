import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .storage import DocumentStore

MONEY_HINTS = ["pay", "payment", "amount", "fee", "price", "total", "budget", "invoice", "contract value"]

def expand_query_terms(query):
    _query = query.lower().strip()
    if any(kw in _query for kw in ["how much", "pay", "payment", "price", "amount", "fee", "total"]):
        return query + " " + " ".join(MONEY_HINTS)
    return query

def search(store: DocumentStore, query, max_results = 5):
    if not store.vectorizer or store.tfidf is None or not store.chunks:
        return {"answer": None, "matches": [], "note": "Index is empty. Upload documents first."}

    qx = expand_query_terms(query)
    qv = store.vectorizer.transform([qx])
    sims = cosine_similarity(qv, store.tfidf)[0]
    idxs = np.argsort(-sims)[:max_results]
    
    matches = []
    for rank, i in enumerate(idxs, 1):
        chunk = store.chunks[int(i)]
        matches.append({
            "rank": rank,
            "score": float(sims[i]),
            "doc_id": chunk.doc_id,
            "pos": chunk.pos,
            "text": chunk.text,
            "meta": chunk.meta,
        })

    all_sentences, sent_meta = [], []
    for idx in idxs:
        chunk = store.chunks[int(idx)]
        for sentence in re.split(r'(?<=[.!?])\s+', (chunk.text or "").strip()):
            if sentence:
                all_sentences.append(sentence)
                sent_meta.append({"doc_id": chunk.doc_id, "pos": chunk.pos, "section_title": chunk.meta.get("section_title")})

    if not all_sentences:
        return {"answer": None, "matches": matches}

    sentence_vectors = store.vectorizer.transform(all_sentences)
    ssims = cosine_similarity(qv, sentence_vectors)[0]
    best_i = int(np.argmax(ssims))
    answer = all_sentences[best_i]
    source = sent_meta[best_i]

    return {"answer": answer, "source": source, "matches": matches}
