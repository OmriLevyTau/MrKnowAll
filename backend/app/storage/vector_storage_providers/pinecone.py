import os
from typing import Dict, List

import numpy as np
import pinecone
from pinecone import Index

from app.config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX
from app.models.documents import DocumentVectorChunk, VectorContextQuery
from app.models.query import Query
from app.storage.abstract_vector_storage import AbstractVectorStorage

# Note this values should be pre-configured by us.
# Only thing the client takes care of is maintaining a 
# dedicated Namespace in whithin this index for
# each user.

if not all([PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX]):
        raise Exception(''' 
            Pinecone connection details not found.
            PINECONE_API_KEY and PINECONE_ENVIRONMENT environment varialbes must be set.
        ''')

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

class PineconeVectorStorage(AbstractVectorStorage):


    def __init__(self) -> None:
        self._index = PineconeVectorStorage._get_index()

    @property
    def index(self) -> Index:
        return self._index # type: ignore

    @staticmethod
    def _get_index():
        if not PINECONE_INDEX in pinecone.list_indexes():
             raise ValueError(f"Pinecone Index does not exists: {PINECONE_INDEX}")
        try:
            index = pinecone.Index(PINECONE_INDEX)
            return index
        except Exception as e:
            print(f"PINECONE: Error in connecting to pinecone index: {PINECONE_INDEX}")
    
    async def _upload(self, user_id: str, payload: List[DocumentVectorChunk]):
        """
        A method for uploading vectors into pinecone. Vectors will be inserted into the existing
        index, in a dedicated Namespace for that particular user. If such  namespace doesn't exist, 
        it is created implicitly.

        Args:
            user_id (str): uniqely identifies a user.
                           Will be used if namespace will get availabe again.
                           Meanwhile it's part of the DocumentVectorChunkMetadata.
            payload (List[DocumentVectorChunk]): see parent class for reference

        Returns:
            str: document_id if successful, otherwise None
        """
        batch_size = 100
        upsert_response = None
        for i in range(0, len(payload), batch_size):
            objects_to_insert = []
            for j in range(i, min(i+batch_size, len(payload))):
                doc_vec_chunk = payload[j].dict()
                obj = (
                        doc_vec_chunk.get("vector_id"), 
                        doc_vec_chunk.get("embedding"), 
                        doc_vec_chunk.get("metadata")
                    )
                objects_to_insert.append(obj)
            # upsert_response = self.index.upsert(vectors=objects_to_insert, namespace=user_id)
            upsert_response = self.index.upsert(vectors=objects_to_insert)

        return upsert_response


    async def delete(self, user_id: str, document_id: str) -> Dict:
        """
        Given a user_id and a document_id, delete all vectors
        associated with this user and document.

        Returns:
            Dict: _description_
        """
        delete_response = self.index.delete(
            filter={
                "user_id": {"$eq": user_id},
                "document_id": {"$eq": document_id}
            },
        )
        #TODO: validate which object is delete_response
        return delete_response

    async def _query(self, user_id: str, query: Query):

        top = 5
        if (query.top_k):
            top = query.top_k
        
        query_response = self.index.query(
            vector = query.embedding,
            top_k = top,
            filter={
                "user_id": {"$eq": user_id}
            },
            include_metadata=True
        )
        #TODO: assemble QueryResult from query_response
        return query_response
    
    async def get_stats(self):
        return self.index.describe_index_stats()
    

    async def get_context(self, user_id: str, context_query: VectorContextQuery):
        """
        refer superclass for detalis.
        """

        target_vec_id = int(context_query.get_vector_id())
        window_size = context_query.get_context_window()
        ids_window = [str(i) for i in range(target_vec_id-window_size, target_vec_id+window_size+1)
                      if i!=target_vec_id ]
        context_response = self.index.fetch(
            ids=ids_window
        )
        return context_response
    
        