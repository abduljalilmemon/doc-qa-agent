import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class DocQATests(unittest.TestCase):
    def test_stats_initial(self):
        r = client.get("/stats")
        self.assertEqual(r.status_code, 200)
        self.assertIn("num_chunks", r.json())

    def test_upload_and_query_txt(self):
        content = b"FastAPI makes it easy to build APIs. This agent answers questions about uploaded documents."
        files = {"file": ("sample.txt", content, "text/plain")}
        r = client.post("/upload", files=files, data={"doc_id": "doc1"})
        self.assertEqual(r.status_code, 200)
        r2 = client.post("/query", json={"q": "What is FastAPI?", "top_k": 3})
        self.assertEqual(r2.status_code, 200)
        data = r2.json()
        self.assertIn("matches", data)
        self.assertGreaterEqual(len(data["matches"]), 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
