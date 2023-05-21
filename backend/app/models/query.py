from typing import Optional
from pydantic import BaseModel


class Query(BaseModel):
    """
    all not Null.
    """
    user_id: int
    query_id: int
    query_content: str

    def get_query_content(self) -> str:
        return self.query_content

class QueryResult(BaseModel):
    user_id: int
    query_id: int
    answer: str
    