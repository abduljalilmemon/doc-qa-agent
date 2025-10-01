from pydantic import BaseModel

class QuerySchema(BaseModel):
    query: str
    max_results: int = 5