import os
from app.storage.abstract_vector_storage import AbstractVectorStorage
from app.models.documents import (DocumentMetaData, DocumentMetaDataFilter)
from app.models.query import (QueryResult)

# Note this values should be pre-configured by us.
# Only thing the client takes care of is maintaining a 
# dedicated Namespace in whithin this index for
# each user.
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")

class PineconeVectorStorage(AbstractVectorStorage):

    def __init__(self) -> None:
        self.pinecone_api_key = PINECONE_API_KEY
        self.pinecone_env = PINECONE_API_KEY
        self.index = PINECONE_INDEX
        
        if not all([self.pinecone_api_key, self.pinecone_env, self.index]):
            raise Exception(''' Pinecone connection details not found.
                                PINECONE_API_KEY and PINECONE_ENVIRONMENT environment varialbes must be set.
                            ''')
    
    async def _upload(user_id: str, doc_metadata: DocumentMetaData, vectors: list[float]) -> str:
        raise NotImplementedError("Pinecone")

    async def delete(self, user_id: str, document_id: str, filter: DocumentMetaDataFilter) -> bool:
        raise NotImplementedError("Pinecone")

    async def _query(self, user_id: str, search_vector: list[float]) -> QueryResult:
        raise NotImplementedError("Pinecone")
