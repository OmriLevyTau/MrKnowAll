from fastapi import APIRouter

from app.config import OPENAI_API_KEY
from app.models.api_models import QueryResponse, Status
from app.models.documents import (DocumentMetaData, DocumentVectorChunk,
                                  VectorContextQuery)
from app.models.query import Query, QueryResult
from app.services.embeddings import get_embeddings
from app.services.openAIAPI import OpenAIAPI
from app.storage.abstract_vector_storage import AbstractVectorStorage
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage

chat_router = APIRouter(prefix="/api/v0")
openai_api = OpenAIAPI(api_key=OPENAI_API_KEY)
pinecone_client = PineconeVectorStorage()

@chat_router.post("/query")
async def query(query: Query) -> QueryResponse:
    """
    the flow of query:
    1. get the original question as a Query object
    2. convert the question into a vector and find the closest vectors based on the file credentials by query the vector DB
    4. retrieve the sentences and thier's context in the text
    5. engineer proper prompt and send to openAI API
    """
    user_id =  query.user_id
    query_id = query.query_id
    query_content = query.query_content

    try:
        # query vector DB 
        vector_db_query_response = await pinecone_client.query(user_id=user_id, query=query)
    
        # get the matches to the vector DB query
        top_k_closest_vectors = vector_db_query_response.get("matches")

        all_context = []
        map_vec_id_to_context = {}
        references = set()

        for vector_data in top_k_closest_vectors:
            cur_vec_doc_id = vector_data.get('metadata').get('document_id')
            references.add(cur_vec_doc_id)
            context_query = VectorContextQuery(user_id=user_id, document_id=cur_vec_doc_id, vector_id=vector_data.get('id'))
            context_response = await pinecone_client.get_context(user_id=user_id, context_query=context_query)

            vectors = context_response.get("vectors")

            for i,key in enumerate(vectors):
                # vec is a key to dict
                res = vectors.get(key)
                vec_id = res.get("id").split("@")[0]
                context = res.get("metadata").get("original_content")
                map_vec_id_to_context[vec_id] = context

        vec_ids_as_str = list(map_vec_id_to_context)
        vec_ids = [int(vec_id) for vec_id in vec_ids_as_str]
        vec_ids.sort()
        for vec_id in vec_ids:
            all_context.append(map_vec_id_to_context[str(vec_id)])

        references_str = ', '.join(references)
        prompt_prefix = "Please generate response based solely on the information I provide in this text. Do not reference any external knowledge or provide additional details beyond what I have given."
        all_context_as_str = ' '.join(all_context)
        prompt = prompt_prefix + '\n' + 'my question is: ' + query_content + '\n'+ 'the information is: ' + all_context_as_str + '\n'  + 'the documents referenced in the question are: ' + references_str
        AI_assistant_query = Query(user_id=user_id, query_id=query_id, query_content=prompt)
        answer = openai_api.generate_answer(AI_assistant_query)
        
        return QueryResponse(status=Status.Ok,
                            query_content=prompt_prefix + '\n' + 'my question is: ' + query_content,
                            context = all_context_as_str,
                            response=answer,
                            references=references)

    except Exception as e:
        return QueryResponse(status=Status.Failed,
                        query_content=query_content,
                        context = '',
                        response=str(e),
                        references='')