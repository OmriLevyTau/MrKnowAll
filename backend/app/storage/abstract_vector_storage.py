from abc import ABC, abstractmethod
from app.models.documents import Document, DocumentMetaData, DocumentMetaDataFilter
from app.models.query import Query, QueryResult
from app.services.document_proccessing import get_documents_chunks
from app.services.embeddings import get_embeddings


"""
An abstract class defining basic functionallity each
vector database provider should implement
"""
class AbstractVectorStorage(ABC):

    MAX_CHUNK_SIZE = 100
    
    async def upload(self, user_id: str, document: Document) -> str:
        """
        Given a document, uploads it into a vector database.
        Args:
            user_id (str): unique id which identifies the user.
            document (Document): pdf document object
        Returns:
            str: id of the inserted document (if succsseful), otherwise None.
        """
        chunks = get_documents_chunks(document, AbstractVectorStorage.MAX_CHUNK_SIZE)
        embeddings = get_embeddings(chunks)
        doc_metadata = document.get_document_metadata()
        
        return await self._upload(user_id, doc_metadata, embeddings)
    
    @abstractmethod
    async def _upload(user_id: str, doc_metadata: DocumentMetaData, vectors: list[float]) -> str:
        """
        Given a user_id, document metadata and list of floats (vectors),
        inserts it to vector database.
        Returns:
            str: document id (if succsseful), otherwise None.
        """
        raise NotImplementedError
    

    @abstractmethod
    async def delete(self, user_id: str, document_id: str, filter: DocumentMetaDataFilter) -> bool:
        """
        Given a document id, deletes it from the database.
        Args:
            user_id (str): unique id which identifies the user
            document_id (str): unique id which identifies the document
        Returns:
            bool: True is deleted successfully, False otherwise (failed or not exists).
        """
        raise NotImplementedError    
    
    async def query (self, user_id: str, query: Query) -> QueryResult:
        if not self._validate_query(query):
            raise ValueError(f"Query should not be empty and must not exceed {AbstractVectorStorage.MAX_CHUNK_SIZE} characters.")
        
        query_embedding = get_embeddings([query.get_query_content()])
        return await self._query(user_id, query_embedding[0])

    async def _query(self, user_id: str, search_vector: list[float]) -> QueryResult:
        raise NotImplementedError
        
    @staticmethod
    def _validate_query(query: Query):
        content_length = len(query.get_query_content())
        not_empty_check = content_length > 0
        max_length_check = content_length <= AbstractVectorStorage.MAX_CHUNK_SIZE
        return (not_empty_check and max_length_check)
    
    
    