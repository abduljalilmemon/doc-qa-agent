
import os
import pickle
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

@dataclass
class Chunk:
    text: str
    doc_id: str
    pos: int
    meta: Dict[str, Any] = field(default_factory=dict)

class DocumentStore:
    def __init__(self, persist_path: str = "store.pkl"):
        self.persist_path = persist_path
        self.chunks: List[Chunk] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf: Optional[csr_matrix] = None

    def save(self):
        data = {
            "chunks": self.chunks,
            "vectorizer": self.vectorizer,
            "tfidf_data": self.tfidf.data if self.tfidf is not None else None,
            "tfidf_indices": self.tfidf.indices if self.tfidf is not None else None,
            "tfidf_indptr": self.tfidf.indptr if self.tfidf is not None else None,
            "tfidf_shape": self.tfidf.shape if self.tfidf is not None else None,
        }
        with open(self.persist_path, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        if not os.path.exists(self.persist_path):
            return
        with open(self.persist_path, "rb") as f:
            data = pickle.load(f)
        self.chunks = data["chunks"]
        self.vectorizer = data["vectorizer"]
        if data["tfidf_data"] is not None:
            self.tfidf = csr_matrix(
                (data["tfidf_data"], data["tfidf_indices"], data["tfidf_indptr"]),
                shape=data["tfidf_shape"]
            )
        else:
            self.tfidf = None

    def add_chunks_and_rebuild(self, new_chunks: List[Chunk]):
        self.chunks.extend(new_chunks)
        texts = [c.text for c in self.chunks]
        self.vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1,2), stop_words="english")
        self.tfidf = self.vectorizer.fit_transform(texts)

    def reset(self):
        self.chunks = []
        self.vectorizer = None
        self.tfidf = None
        if os.path.exists(self.persist_path):
            os.remove(self.persist_path)

    def stats(self):
        return {
            "num_docs": len(set(c.doc_id for c in self.chunks)),
            "num_chunks": len(self.chunks),
            "vocab_size": len(self.vectorizer.vocabulary_) if self.vectorizer else 0
        }
