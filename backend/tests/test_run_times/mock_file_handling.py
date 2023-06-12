
import json

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.api_models import Status
from app.models.documents import Document, DocumentMetaData

from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from tests.test_storage.test_vector_storage.test_pinecone import (
    TEST_DOCUMENT_ID, TEST_DOCUMENT_METADATA, TEST_USER_ID)
from app.storage import abstract_vector_storage 
from app.services.document_proccessing import get_documents_chunks



pinecone_client  = PineconeVectorStorage()

def clear_doc(document: Document) -> None:
    delete_response = pinecone_client.index.delete(
        filter={
            "user_id": {"$eq": TEST_USER_ID},
            "document_id": {"$eq": document.get_document_metadata().get_document_id}
        }
    )

def mock_upload(document: Document, delete_after: bool = True , user_id: str = TEST_USER_ID):
    pinecone_client.upload(document=document,user_id=TEST_USER_ID)
    if (delete_after):
        clear_doc(document=document)


def mock_get_chunks(document: Document):
    chunks = get_documents_chunks(document=document)
