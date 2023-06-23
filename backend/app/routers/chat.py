from fastapi import APIRouter

from app.config import OPENAI_API_KEY
from app.models.api_models import QueryResponse, Status, OpenAIResponse
from app.models.documents import VectorContextQuery
from app.models.query import Query
from app.services.openAIAPI import OpenAIAPI
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage

from app.storage.abstract_vector_storage import  SEP


chat_router = APIRouter(prefix="/api/v0")
openai_api = OpenAIAPI(api_key=OPENAI_API_KEY)
pinecone_client = PineconeVectorStorage()

SCORE_THRESHOLD = 0.25


@chat_router.post("/query")
async def query(query_request: Query) -> QueryResponse:
    """
    the flow of query:
    1. get the original question as a Query object
    2. convert the question into a vector and find the closest vectors based on the file credentials by query the vector DB
    4. retrieve the sentences and their's context in the text
    5. engineering of proper prompt and send to openAI API
    """

    user_id = query_request.user_id
    query_id = query_request.query_id
    query_content = query_request.query_content

    try:
        # query vector DB
        vector_db_query_response = await pinecone_client.query(user_id=user_id, query=query_request)

        # get the matches to the vector DB query
        top_k_closest_vectors = vector_db_query_response.get("matches")

        all_context = ""

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
                context_response = await pinecone_client.get_context(user_id=user_id, context_query=context_query)

                vectors = context_response.get("vectors")

                for i, key in enumerate(vectors):
                    # vec is a key to dict
                    res = vectors.get(key)
                    vec_id = res.get("id").split(SEP)[0]
                    context = res.get("metadata").get("original_content")
                    map_vec_id_to_context[vec_id] = context

                if not cur_vec_doc_id in map_doc_id_to_context:
                    map_doc_id_to_context[cur_vec_doc_id] = map_vec_id_to_context
                else:
                    map_doc_id_to_context[cur_vec_doc_id].update(map_vec_id_to_context)

        # if there is no relevant sentence, we dont communicate with the AI assistant
        if len(map_doc_id_to_context) == 0:

            without_API_communication_response = OpenAIResponse(
                status=Status.Ok, content='We are sorry, but it seems that there is no relevant sentences to your question in your files. You are more than welcome to ask a different question, or upload files which are relevant to your question')
            return QueryResponse(status=Status.Ok,
                                 query_content=query_content,
                                 context='',
                                 response=without_API_communication_response,
                                 references=[])

        # if we are here, it means that we have at least one sentence that is relevant to the question
        doc_ids = list(map_doc_id_to_context)
        doc_ids.sort()

        for doc_id in doc_ids:
            all_context = all_context + \
                "The following context is coming from the document: " + doc_id + '\n'
            cur_doc_id_dict = map_doc_id_to_context[doc_id]

            vec_ids = list(cur_doc_id_dict)

            vec_ids.sort()
            for vec_id in vec_ids:
                all_context = all_context + cur_doc_id_dict[vec_id]
                all_context = all_context + "\n"

        prompt_prefix = "Please generate response based solely on the information I provide in this text, without saying what is the reference to your response. Do not reference any external knowledge or provide additional details beyond what I have given."

        prompt = prompt_prefix + '\n' + 'my question is: ' + \
            query_content + '\n' + 'the information is: ' + all_context
        AI_assistant_query = Query(
            user_id=user_id, query_id=query_id, query_content=prompt)
        answer = openai_api.generate_answer(AI_assistant_query)

        return QueryResponse(status=Status.Ok,
                             query_content=prompt_prefix + '\n' + 'my question is: ' + query_content,
                             context=all_context,
                             response=answer,
                             references=references)

    except Exception as e:
        return QueryResponse(status=Status.Failed,
                             query_content=query_content,
                             context='',
                             response=OpenAIResponse(
                                 status=Status.Failed, content=str(e)),
                             references=[])
