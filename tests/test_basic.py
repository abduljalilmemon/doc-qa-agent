import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class DocQATests(unittest.TestCase):
    def test_stats_initial(self):
        response = client.get("/stats")
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_chunks", response.json())

    def test_upload_and_query_txt(self):
        content = b"FastAPI makes it easy to build APIs. This agent answers questions about uploaded documents."
        files = {"file": ("sample.txt", content, "text/plain")}
        response = client.post("/upload", files=files, data={"doc_id": "doc1"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/query", json={"query": "What is FastAPI?", "max_results": 3})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("matches", data)
        self.assertGreaterEqual(len(data["matches"]), 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
