from fastapi import APIRouter

from app.config import OPENAI_API_KEY
from app.models.api_models import QueryResponse, Status
from app.models.query import Query, QueryResult
from app.services.embeddings import get_embeddings
from app.services.openAIAPI import OpenAIAPI
from app.storage.abstract_vector_storage import AbstractVectorStorage

chat_router = APIRouter()
openai_api = OpenAIAPI(api_key=OPENAI_API_KEY)


@chat_router.post("/query")
async def query(query: Query) -> QueryResponse:
    answer = openai_api.generate_answer(query)
    # prompt_prefix = "Please generate responses based solely on the information I provide in this text. Do not reference any external knowledge or provide additional details beyond what I've given."
    return QueryResponse(status=Status.Ok, response=answer)
