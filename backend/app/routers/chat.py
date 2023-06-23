from fastapi import APIRouter
from typing import Optional

from app.config import OPENAI_API_KEY
from app.models.api_models import QueryResponse, Status, OpenAIResponse, QueryResponseType
from app.models.documents import VectorContextQuery
from app.models.query import Query
from app.services.openAIAPI import OpenAIAPI
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from app.storage.chat_history_db import ChatHistoryManager
from app.models.chat_history import Clear_chat_request
from app.storage.abstract_vector_storage import SEP
from app.param_tuning import MAX_NUM_OF_CHARS_IN_QUERY, MAX_NUM_OF_CHARS_IN_QUESTION, MAX_NUM_OF_WORDS_IN_QUERY, SCORE_THRESHOLD


chat_router = APIRouter(prefix="/api/v0")
openai_api = OpenAIAPI(api_key=OPENAI_API_KEY)
pinecone_client = PineconeVectorStorage()


# create a connection to the local DB for saving the chat history
chat_history_manager = ChatHistoryManager("chat_history.db")


def check_if_valid_query(query_request: Query) -> bool:
    try:
        query_content = query_request.query_content
        words_num = len(query_content.split(" "))
        chars_num = len(query_content)

        if words_num > MAX_NUM_OF_WORDS_IN_QUERY or chars_num > MAX_NUM_OF_CHARS_IN_QUESTION:
            return False

        return True
    except:
        return False


def get_history(user_id: str, query: Query) -> str:
    query_content = query.query_content
    query_content_len = len(query_content)
    returned_history = ""

    # get the last 6 questions and answers
    history_messages_combined, number_of_questions_and_answers = chat_history_manager.get_user_messages_with_answers(
        user_id=user_id)

    history_messages_list = history_messages_combined.split("user-question:")

    # if this is the first time there is no history
    if number_of_questions_and_answers < 1:
        return ""

    returned_history = history_messages_list[1]

    used_characters = 0 + len(returned_history)
    index = 2

    # in the loop we add history messages only if the entire message we send to openAI API is less then 4096 chars
    while (index < number_of_questions_and_answers and MAX_NUM_OF_CHARS_IN_QUERY - query_content_len - used_characters - len(history_messages_list[index]) >= 0):
        returned_history = returned_history + history_messages_list[index]
        used_characters = used_characters + len(history_messages_list[index])
        index = index + 1

    return returned_history


def return_query_response(query_content: str, response_type: str, e: Optional[Exception]) -> QueryResponse:

    if response_type == "TooLongQuery":
        without_API_communication_response = OpenAIResponse(
            status=Status.Ok,
            content='We apologize for the inconvenience, but to ensure a smoother experience, we kindly request that you limit your question to a maximum of 128 words and 512 characters. Please take a moment to edit your question accordingly. Your cooperation is greatly appreciated, and we thank you for your understanding!'
        )
        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.TooLongQuery,
                             query_content=query_content,
                             context='',
                             response=without_API_communication_response,
                             references=[])

    elif response_type == "NoMatchingVectors":
        without_API_communication_response = OpenAIResponse(
            status=Status.Ok, content='We are sorry, but it seems that there is no relevant sentences to your question in your files. You are more than welcome to ask a different question, or upload files which are relevant to your question')
        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.NoMatchingVectors,
                             query_content=query_content,
                             context='',
                             response=without_API_communication_response,
                             references=[])

    elif response_type == "Failed":
        return QueryResponse(status=Status.Failed,
                             response_type=QueryResponseType.Failed,
                             query_content=query_content,
                             context='',
                             response=OpenAIResponse(
                                 status=Status.Failed, content=str(e)
                             ),
                             references=[])


@chat_router.post("/query")
async def query(query_request: Query) -> QueryResponse:
    """
    the flow of query:
    1. get the original question as a Query object
    2. convert the question into a vector and find the closest vectors based on the file credentials by query the vector DB
    4. retrieve the sentences and their's context in the text
    5. engineering of proper prompt and send to openAI API
    """

    try:
        # get the relevant parameters of the current query
        user_id = query_request.user_id
        query_id = query_request.query_id
        query_content = query_request.query_content

        if not check_if_valid_query(query_request=query_request):
            return return_query_response(query_content=query_content, response_type="TooLongQuery", e=None)

        # query vector DB
        vector_db_query_response = await pinecone_client.query(user_id=user_id, query=query_request)

        # get the matches to the vector DB query
        top_k_closest_vectors = vector_db_query_response.get("matches")

        all_context = ""
        context_query_list = []
        map_doc_id_to_context = {}
        references = set()
        for vector_data in top_k_closest_vectors:
            # every vector has its own context
            map_vec_id_to_context = {}
            cur_vec_doc_id = vector_data.get('metadata').get('document_id')
            cur_vec_score = vector_data.get('score')
            # get context only for setnteces that are relevant to the question
            if (cur_vec_score >= SCORE_THRESHOLD):
                references.add(cur_vec_doc_id)
                context_query = VectorContextQuery(
                    user_id=user_id, document_id=cur_vec_doc_id, vector_id=vector_data.get('id'))
                context_query_list.append(context_query)

        # if there is no relevant sentence, we dont communicate with the AI assistant
        if len(context_query_list) == 0:
            return return_query_response(query_content=query_content, response_type="NoMatchingVectors", e=None)

        # get all the context vectors for the relevane vectors
        context_response = await pinecone_client.get_context_for_list(user_id=user_id, context_query_list=context_query_list)

        vectors = context_response.get("vectors")

        # we map every vector we have to all of it's context sentences, and than we save this mapping inside another map, from the document id to all of the (context) vectors it has for this query.
        for i, key in enumerate(vectors):
            # vec is a key to dict
            res = vectors.get(key)
            vec_id = res.get("id").split(SEP)[0]
            context = res.get("metadata").get("original_content")
            map_vec_id_to_context[vec_id] = context

            if not cur_vec_doc_id in map_doc_id_to_context:
                map_doc_id_to_context[cur_vec_doc_id] = map_vec_id_to_context
            else:
                map_doc_id_to_context[cur_vec_doc_id].update(
                    map_vec_id_to_context)

        # if we are here, it means that we have at least one sentence that is relevant to the question
        doc_ids = list(map_doc_id_to_context)

        # for each document, we get the context of all of the vectors that belongs to that document
        for doc_id in doc_ids:
            all_context = all_context + \
                "\n The following context is coming from the document: " + doc_id + '\n'
            cur_doc_id_dict = map_doc_id_to_context[doc_id]

            vec_ids = list(cur_doc_id_dict)

            vec_ids.sort()
            for vec_id in vec_ids:
                all_context = all_context + cur_doc_id_dict[vec_id]
                all_context = all_context + "\n"

        # the prefix of the query we send to the API. we ask to get answer based only our information and history
        prompt_prefix = "Please generate response based solely on the information I provide in this text. in your answer, you can use the previous messages from the AI and user for context, but dont base your answer on it. In your answer, dont mention what is the reference to your response. Do not reference any external knowledge or provide additional details beyond what I have given. \n"

        prompt = prompt_prefix + '\n' + 'my question is: ' + \
            query_content + '\n' + 'the information is: ' + all_context

        # build the query object that will be send to the AI assistant
        AI_assistant_query = Query(
            user_id=user_id, query_id=query_id, query_content=prompt)

        # get the last messages and responsed from sqlite DB
        history = get_history(user_id=user_id, query=AI_assistant_query)

        # get the response from the AI assistant API
        answer = openai_api.generate_answer(
            history=history, query=AI_assistant_query)

        # add the question and the response to the short-term memory
        chat_history_manager.add_message(
            user_id=user_id, chat_id=user_id, user_message=query_content, chat_message=answer.content)

        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.Valid,
                             query_content=prompt_prefix + '\n' + 'my question is: ' + query_content,
                             context=all_context,
                             response=answer,
                             references=references)

    except Exception as e:
        return return_query_response(query_content=query_content, response_type="Failed", e=e)


@chat_router.post("/clear_chat")
async def clear_chat(request: Clear_chat_request):
    try:
        # chat_history_manager.print_DB()

        chat_history_manager.delete_chat_history_by_user_id(request.user_id)
        # chat_history_manager.print_DB()

        if (len(chat_history_manager.get_user_messages_with_answers(request.user_id)) == 0):
            return {'status': Status.Ok}
        else:
            raise Exception

    except Exception as e:
        return {'status': Status.Failed, 'error': str(e)}
