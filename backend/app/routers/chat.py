from fastapi import APIRouter
from app.models.query import Query
chat_router = APIRouter()

@chat_router.post("/query")
async def query(query: Query) -> dict:
    return {"ok":True,"content":query.content}
