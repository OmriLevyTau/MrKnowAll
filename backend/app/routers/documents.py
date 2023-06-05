
from fastapi import APIRouter

from app.models.api_models import (GetAllDocumentsMetadataResponse, Status,
                                   UploadDocumentResponse)
from app.models.documents import Document
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage

docs_router = APIRouter(
    prefix="/api/v0/documents"
)

PDF_PREFIX = 'data:application/pdf;base64,'

pinecone_client = PineconeVectorStorage()


@docs_router.get("/")
async def get_all_docs_metadata() -> GetAllDocumentsMetadataResponse:
    """
    Get all documents metadata by the specified user_id

    Returns:
        GetAllDocumentsMetadataResponse:
    """
    raise NotImplementedError()

@docs_router.post("/")
async def upload_doc(doc: Document) -> UploadDocumentResponse:
    """
    Given a document it'll upload it to vector storage (after proccessing it)
    and to google-storage bucket as well.

    Args:
        doc (Document): With path *or* (exclusive) pdf_encoding defined

    Returns:
        UploadDocumentResponse:
    """
    user_id = doc.get_document_metadata().get_user_id()
    doc_encoding = doc.pdf_encoding
    
    if (doc_encoding is not None) and (doc_encoding.startswith(PDF_PREFIX)):
        doc.pdf_encoding = doc.pdf_encoding[len(PDF_PREFIX):]

    try:
        upload_response = await pinecone_client.upload(user_id=user_id, document=doc)
        return UploadDocumentResponse(status=Status.Ok, doc_metadata=doc.get_document_metadata(), uploaded_vectors_num=upload_response.get("upserted_count"))
    except Exception:
        return UploadDocumentResponse(status=Status.Failed, doc_metadata=doc.get_document_metadata(), uploaded_vectors_num=0)

@docs_router.get("/{doc_id}")
async def get_doc_by_id(doc_id: int) -> Document:
    """
    A stub method, still not sure we going to use this.
    """
    raise NotImplementedError()


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: str) -> dict:
    """
    Given user_id and doc_id, delete the document from the vector storage
    and google-storage as well.

    Args:
        doc_id (str)

    Raises:
        Exception: _description_
    """
    try:
        result = await pinecone_client.delete(user_id="test", document_id=doc_id)
        if len(result) == 0:
            return {'status': Status.Ok}
        raise Exception('delete failed')
    except Exception as e:
        return {'status': Status.Failed, 'error': str(e)}

