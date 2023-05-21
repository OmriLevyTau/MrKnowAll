from typing import Optional, List
from pydantic import BaseModel


class Query(BaseModel):
    """
    all not Null.
    """
    user_id: int
    query_id: int
    query_content: str
    embedding: Optional[List[str]] = None

    def get_query_content(self) -> str:
        return self.query_content
    
    def get_embedding(self) -> Optional[List[str]]:
        return self.embedding

class QueryResult(BaseModel):
    user_id: int
    query_id: int
    answer: str
    