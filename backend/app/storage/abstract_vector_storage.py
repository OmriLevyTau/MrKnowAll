'''
    An abstract class defining basic functionallity each
    vector database provider should implement
'''

from abc import ABC, abstractmethod
from typing import List

from app.models.documents import (Document, DocumentMetaData,
                                  DocumentVectorChunk,
                                  DocumentVectorChunkMetadata,
                                  VectorContextQuery)
from app.models.query import Query
from app.services.document_proccessing import get_documents_chunks
from app.services.embeddings import get_embeddings


class AbstractVectorStorage(ABC):
    """
    This class defines basic functionallity required from an Vector Storage.
    """

    async def upload(self, user_id: str, document: Document) -> str:
        """
        Given a document, uploads it into a vector database.
        Args:
            user_id (str): unique id which identifies the user.
            document (Document): pdf document object
        Returns:
            str: id of the inserted document (if succsseful), otherwise None.
        """
        # returns a list of sentences composing the document
        text_chunks = get_documents_chunks(document)
        # returns a list of embeddings corresponding to the previous list
        embeddings = get_embeddings(text_chunks)
        doc_metadata = document.get_document_metadata()
        payload = AbstractVectorStorage.assemble_documents_vector_chunks(
            user_id, doc_metadata, text_chunks, embeddings
        )

        return await self._upload(user_id, payload)

    @abstractmethod
    async def _upload(self, user_id: str, payload: List[DocumentVectorChunk]) -> str:
        """
        Given a user_id, document metadata and list of DocumentVectorChunk,
        inserts it to vector database.
        Returns:
            str: document id (if succsseful), otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: str, document_id: str) -> bool:
        """
        Given a document id, deletes it from the database.
        Args:
            user_id (str): unique id which identifies the user
            document_id (str): unique id which identifies the document
        Returns:
            bool: True is deleted successfully, False otherwise (failed or not exists).
        """
        raise NotImplementedError

    async def query(self, user_id: str, query: Query):
        """
        Given a user_id and a Query object, performs
        vector similarity search.

        Args:
            user_id (str): unique user identifier
            query (Query): A query object. Query.embedding expected to
                           be None and will be created here
        Raises:
            ValueError: Not valid query

        Returns:
            _type_: _description_
        """
        if not AbstractVectorStorage._validate_query(query):
            raise ValueError("Query must be non-empty")

        query_embedding = get_embeddings([query.get_query_content()])[0]
        query.embedding = query_embedding
        return await self._query(user_id, query)

    
    @abstractmethod
    async def _query(self, user_id: str, query: Query):
        raise NotImplementedError()
    

    @abstractmethod
    async def get_context(self, user_id: str, context_query: VectorContextQuery):
        '''
        Given user_id, docoument_id and a vector_id (id),
        get the context of the original sentence that represented
        by the vector_id.
        '''
        raise NotImplementedError()

    @staticmethod
    def _validate_query(query: Query):
        """
        Asserts a given Query is valid.

        Args:
            query (Query): _description_

        Returns:
            bool: True if valid, False otherwise
        """
        return len(query.get_query_content())>0

    @staticmethod
    def assemble_documents_vector_chunks(user_id: str, doc_metadata: DocumentMetaData, text_chunks: List[str],
                                          embeddings) -> List[DocumentVectorChunk]:
        """
        Given a user_id, metadata, text chunks and its corresponding embeddings,
        assemble a list of DocumentVectorChunks.
        Args:
            user_id (str): unique user_id
            doc_metadata (DocumentMetaData): additional information about the document
            text_chunks (List[str]): a list of sentences
            embeddings (_type_): a list of corresponding embeddings for the sentences

        Raises:
            ValueError: if number of text chunks != number of embeddings

        Returns:
            List[DocumentVectorChunk]: 
                ready to insert to db DocumentVectorChunk.
                each vector_id should be an integer represented as string.

        """
        # number of text chunks and emneddings must agree
        if (len(text_chunks) != len(embeddings)):
            raise ValueError('''AbstractVectorStorage: _assemble_vector_chunks:
                                chunks and embeddings must agree on size.''')

        
        doc_id = doc_metadata.get_document_id()
        payload = []

        for i, chunk in enumerate(text_chunks):
            meta = DocumentVectorChunkMetadata(
                user_id=user_id, document_id=doc_id, 
                original_content=chunk
                )
            payload.append(
                DocumentVectorChunk(
                    vector_id=str(i)+"@"+doc_id,
                    embedding=embeddings[i],
                    metadata=meta
                )
            )

        return payload

