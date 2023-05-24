import datetime as dt
from typing import List

from fastapi import APIRouter

from app.models.api_models import (GetAllDocumentsMetadataResponse, Status,
                                   UploadDocumentResponse)
from app.models.documents import Document, DocumentMetaData
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage

docs_router = APIRouter(
    prefix="/documents"
)

pinecone_client = PineconeVectorStorage()

@docs_router.get("/")
async def get_all_docs_metadata() -> GetAllDocumentsMetadataResponse:
    raise NotImplementedError()

@docs_router.post("/")
async def upload_doc(doc: Document) -> UploadDocumentResponse:
    raise NotImplementedError()

@docs_router.get("/{doc_id}")
async def get_doc_by_id(doc_id: int) -> Document:
    raise NotImplementedError()


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: int) -> dict:
    raise NotImplementedError()

