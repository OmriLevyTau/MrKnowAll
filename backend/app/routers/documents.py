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
    user_id = doc.get_document_metadata().get_user_id()
    try:
        upload_response = await pinecone_client.upload(user_id=user_id, document=doc)
        return UploadDocumentResponse(status=Status.Ok, doc_metadata=doc.get_document_metadata(), uploaded_vectors_num=upload_response.get("upserted_count"))
    except Exception as e:
        return UploadDocumentResponse(status=Status.Failed, doc_metadata=doc.get_document_metadata(), uploaded_vectors_num=0)

@docs_router.get("/{doc_id}")
async def get_doc_by_id(doc_id: int) -> Document:
    raise NotImplementedError()


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: int, user_id:str) -> dict:
    try:
        result = pinecone_client.delete(user_id=user_id, document_id=doc_id)
        if len(result) == 0:
            return {'status': Status.Ok}
        raise Exception('delete failed')
    except Exception as e:
        return {'status': Status.Failed, 'error': str(e)}

