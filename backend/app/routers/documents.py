import datetime as dt
from typing import List
import base64
import os

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from app.models.api_models import (GetAllDocumentsMetadataResponse, Status,
                                   UploadDocumentResponse)
from app.models.documents import Document, DocumentMetaData
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from app.storage.object_storage_providers.google_object_store import (
    deleteFile, uploadFile, convertDocToPdf, getFileContent, getFileList)

docs_router = APIRouter(
    prefix="/documents"
)

pinecone_client = PineconeVectorStorage()


@docs_router.get("/{user_id}")
async def get_all_docs_metadata(user_id: str) -> GetAllDocumentsMetadataResponse:
    response = GetAllDocumentsMetadataResponse(
        status=Status.Ok, docs_metadata=getFileList(user_id))
    return response


@docs_router.post("/")
async def upload_doc(doc: Document) -> dict:
    user_name = doc.get_document_metadata().get_user_id()
    file_name = doc.get_document_metadata().get_document_id()
    path = convertDocToPdf(doc, file_name)
    uploadFile(user_name, path, file_name)
    os.remove(path)
    return {"status": "ok"}


@docs_router.get("/{user_id}/{doc_id}")
async def get_doc(user_id: str, doc_id: str):
    # Retrieve the file content from GCS
    file_content = getFileContent(user_id, doc_id)

    if file_content is None:
        return Response(status_code=404)

    content_type = "application/pdf"

    # Stream the file content as the response body
    return StreamingResponse(
        iter([file_content]),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={doc_id}.pdf"},)


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: str, body: dict) -> dict:
    # Call the deleteFile function with the provided user name and file name
    print(body)
    deleteFile(body["user_id"], doc_id)
    return {"status": "ok", "message": "File deleted successfully"}
