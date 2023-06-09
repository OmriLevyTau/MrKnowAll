from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import OPENAI_API_KEY

from app.models.api_models import QueryResponse, Status, OpenAIResponse, QueryResponseType
from app.models.query import Query
from app.models.chat_history import ClearChatRequest

from app.services.chat.openai_client import OpenAIAPI
from app.services.chat.chat_manager import build_all_context, validate_query, get_history_for_chat, compose_context_response, build_context_objects_for_top_k_closest_vectors, extract_context_from_context_vectors

from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from app.storage.chat_history_db import ChatHistoryManager

chat_router = APIRouter(prefix="/api/v0")
openai_api = OpenAIAPI(api_key=OPENAI_API_KEY)
pinecone_client = PineconeVectorStorage()

chat_history_manager = ChatHistoryManager("chat_history.db")

# the prefix of the query we send to the API. we ask to get answer based only our information and history
PROMPT_PREFIX = "Please return a response to the user's message " \
                "based solely on the information I provide in the text delimited by three dashes. \n1. If the " \
                "user's message does not make sense, simply say you can't answer. \n2. Otherwise, return a response " \
                "based on the information I provided and the previous messages. \nDo not refer to any external " \
                "knowledge or provide additional details beyond what I have given.\n"


def compose_response(query_content: str, response_type: QueryResponseType, open_ai_response: OpenAIResponse):
    return QueryResponse(status=Status.Ok,
                         response_type=response_type,
                         query_content=query_content,
                         response=open_ai_response,
                         references=[]
                         )


@chat_router.post("/query")
async def query(query_request: Query):
    """
    the flow of query:
    1. get the original question as a Query object
    2. convert the question into a vector and find the closest vectors based on the file credentials by query the vector DB
    4. retrieve the sentences and theirs context in the text
    5. engineering of proper prompt and send to openAI API

    the scheme of the actual prompt:
    0. history - the previous chat messages
    1. prompt prefix - what's the model task
    2. "my question is: " + the query content
    3. "the information is: " + the context of the relevant vectors
    """

    try:
        # get the relevant parameters of the current query
        user_id = query_request.user_id
        query_id = query_request.query_id
        query_content = query_request.query_content
        # validate query
        if not validate_query(query_request=query_request):
            return JSONResponse(status_code=400, content=QueryResponseType.TooLongQuery)

        # get most relevant sentences from then user's documents for answering this question
        vector_db_query_response = await pinecone_client.query(user_id=user_id, query=query_request)
        top_k_closest_vectors = vector_db_query_response.get("matches")

        # keep only the vectors which are similar by a specific threshold
        all_context = ""
        map_doc_id_to_context = {}

        # get the references and the VectorContextQuery for each relevant vector
        references, context_query_list = build_context_objects_for_top_k_closest_vectors(
            user_id=user_id, vectors=top_k_closest_vectors)

        # if there is no relevant sentence, we don't communicate with the AI assistant
        if len(context_query_list) == 0:
            return compose_response(
                query_content=query_content, response_type=QueryResponseType.NoMatchingVectors,
                open_ai_response=OpenAIResponse(
                    status=Status.Ok, content="No relevant data was found.")
            )

        # get all the context vectors for the relevant vectors
        context_response = await pinecone_client.get_context_for_list(user_id=user_id,
                                                                      context_query_list=context_query_list)

        vectors = context_response.get("vectors")

        map_doc_id_to_context = extract_context_from_context_vectors(vectors)

        # if we are here, it means that we have at least one sentence that is relevant to the question
        doc_ids = list(map_doc_id_to_context)

        all_context = build_all_context(
            doc_ids=doc_ids, map_doc_id_to_context=map_doc_id_to_context)

        question = "user: " + query_content
        prompt_prefix = PROMPT_PREFIX + question
        prompt_suffix = "\nThis is the text:\n---"+all_context+"\n---"
        prompt = prompt_prefix + prompt_suffix

        # build the query object that will be sent to the AI assistant
        ai_assistant_query = Query(
            user_id=user_id, query_id=query_id, query_content=prompt)

        # get the most recent chat history
        history = get_history_for_chat(
            user_id=user_id, query=ai_assistant_query)

        # get the response from the AI assistant API
        answer = openai_api.generate_answer(
            history=history, query=ai_assistant_query)

        # add the question and the response to the short-term chat history
        chat_history_manager.add_message(
            user_id=user_id, chat_id=user_id, user_message=query_content, chat_message=answer.content)

        modified_context = compose_context_response(map_doc_id_to_context)

        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.Valid,
                             query_content=prompt_prefix,
                             context=modified_context,
                             response=answer,
                             references=references)

    except Exception as e:
        return JSONResponse(status_code=500, content="Failed processing the query: " + str(e))


@chat_router.delete("/clear-chat", response_class=JSONResponse)
async def clear_chat(clear_chat_request: ClearChatRequest):
    try:
        chat_history_manager.delete_chat_history_by_user_id(
            clear_chat_request.user_id)
        return JSONResponse(status_code=200, content="Chat cleared.")
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
