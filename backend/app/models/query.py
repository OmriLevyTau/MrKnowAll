from typing import Optional
from pydantic import BaseModel


class Query(BaseModel):
    user_id: int
    content: str
    query_id: int