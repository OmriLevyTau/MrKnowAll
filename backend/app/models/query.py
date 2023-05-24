from typing import List, Optional

from pydantic import BaseModel


class Query(BaseModel):
    """
    all not Null.
    """
    user_id: str
    query_id: int
    query_content: str
    top_k: Optional[int] = None
    embedding: Optional[List[float]] = None

    def get_query_content(self) -> str:
        return self.query_content

    def get_embedding(self) -> Optional[List[float]]:
        return self.embedding


class QueryResult(BaseModel):
    user_id: str
    query_id: int
    answer: str
