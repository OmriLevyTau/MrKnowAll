from abc import ABC, abstractmethod
from typing import List

from app.models.documents import (Document, DocumentMetaData,
                                  DocumentVectorChunk,
                                  DocumentVectorChunkMetadata)
from app.models.query import Query, QueryResult
from app.services.document_proccessing import get_documents_chunks
from app.services.embeddings import get_embeddings

'''
An abstract class defining basic functionallity each
vector database provider should implement

'''


class AbstractVectorStorage(ABC):

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
        if not AbstractVectorStorage._validate_query(query):
            raise ValueError(f"Query must be non-empty")

        query_embedding = get_embeddings([query.get_query_content()])[0]
        query.embedding = query_embedding
        return await self._query(user_id, query)

    @abstractmethod
    async def _query(self, user_id: str, query: Query):
        pass

    @staticmethod
    def _validate_query(query: Query):
        return len(query.get_query_content())>0

    @staticmethod
    def assemble_documents_vector_chunks(user_id: str, doc_metadata: DocumentMetaData, text_chunks: List[str],
                                          embeddings) -> List[DocumentVectorChunk]:
        if (len(text_chunks) != len(embeddings)):
            raise ValueError('''AbstractVectorStorage: _assemble_vector_chunks:
                                chunks and embeddings must agree on size.''')

        doc_id = doc_metadata.get_document_id()
        payload = []

        for i, chunk in enumerate(text_chunks):
            meta = DocumentVectorChunkMetadata(
                user_id=user_id, document_id=doc_id, original_content=chunk)
            payload.append(
                DocumentVectorChunk(
                    vector_id=str(i),
                    embedding=embeddings[i],
                    metadata=meta
                )
            )

        return payload
