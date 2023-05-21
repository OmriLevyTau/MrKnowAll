import os
import numpy as np
from typing import List
import pinecone
from app.storage.abstract_vector_storage import AbstractVectorStorage
from app.models.documents import (DocumentVectorChunk)
from app.models.query import (QueryResult, Query)

# Note this values should be pre-configured by us.
# Only thing the client takes care of is maintaining a 
# dedicated Namespace in whithin this index for
# each user.
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")

if not all([PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX]):
        raise Exception(''' 
            Pinecone connection details not found.
            PINECONE_API_KEY and PINECONE_ENVIRONMENT environment varialbes must be set.
        ''')

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

class PineconeVectorStorage(AbstractVectorStorage):

    def __init__(self) -> None:
        self.index = PineconeVectorStorage._get_index()

    @staticmethod
    def _get_index():
        if not PINECONE_INDEX in pinecone.list_indexes():
             raise ValueError(f"Pinecone Index does not exists: {PINECONE_INDEX}")
        try:
            index = pinecone.index(PINECONE_INDEX)
            return index
        except Exception as e:
            print(f"PINECONE: Error in connecting to pinecone index: {PINECONE_INDEX}")
    

    async def _upload(self, user_id: str, payload: List[DocumentVectorChunk]) -> str:
        """
        A method for uploading vectors into pinecone. Vectors will be inserted into the existing
        index, in a dedicated Namespace for that particular user. If such  namespace doesn't exist, 
        it is created implicitly.

        Args:
            user_id (str): uniqely identifies a user
            payload (List[DocumentVectorChunk]): see parent class for reference

        Returns:
            str: document_id if successful, otherwise None
        """
        batch_size = 100

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
            upsert_response = self.index.upsert(vectors=objects_to_insert, namespace=user_id)

        return str(upsert_response)


    async def delete(self, user_id: str, document_id: str) -> bool:
        # TODO: maybe should add delete_all=True
        delete_response = self.index.delete(
            filter={
                "document_id": {"$eq": document_id}
            },
            namespace=user_id
        )
        #TODO: validate which object is delete_response
        return delete_response

    async def _query(self, user_id: str, query: Query) -> QueryResult:
        query_response = self.index.query(
            vector = query.embedding,
            top_k = 5,
            namespace=user_id,
            include_metadata=True
        )
        #TODO: assemble QueryResult from query_response
        return query_response
    
