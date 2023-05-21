from fastapi import APIRouter
from typing import List
from app.models.documents import (
    Document, 
    UploadDocumentResponse, 
    GetAllDocumentsMetadataResponse
    )
import datetime as dt

docs_router = APIRouter(
    prefix="/documents"
)

@docs_router.get("/")
async def get_all_docs_metadata() -> GetAllDocumentsMetadataResponse:
    pass


@docs_router.get("/{doc_id}")
async def get_doc_by_id(doc_id: int) -> Document:
    pass

@docs_router.post("/")
async def upload_doc(doc: Document) -> UploadDocumentResponse:
    pass


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: int)-> dict: 
    pass
