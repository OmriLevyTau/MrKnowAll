import os

from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse

from app.models.api_models import (GetAllDocumentsMetadataResponse, Status,
                                   UploadDocumentResponse)
from app.models.documents import Document
from app.storage.object_storage_providers.google_object_store import GoogleStorageClient
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from app.config import GC_JSON_PATH



docs_router = APIRouter(
    prefix="/api/v0/documents"
)

PDF_PREFIX = 'data:application/pdf;base64,'

pinecone_client = PineconeVectorStorage()
google_client = GoogleStorageClient(GC_JSON_PATH, "mr-know-all")



@docs_router.get("/{user_id}")
async def get_all_docs_metadata(user_id: str) -> GetAllDocumentsMetadataResponse:
    response = GetAllDocumentsMetadataResponse(
        status=Status.Ok, docs_metadata=google_client.get_file_list(user_id))
    return response


@docs_router.post("/")
async def upload_doc(doc: Document) -> UploadDocumentResponse:
    """
    Given a document it'll upload it to vector storage (after processing it)
    and to google-storage bucket as well.

    Args:
        doc (Document): With path *or* (exclusive) pdf_encoding defined

    Returns:
        UploadDocumentResponse:
    """
    user_id = doc.get_document_metadata().get_user_id()
    doc_id = doc.get_document_metadata().get_document_id()

    doc_encoding = doc.pdf_encoding
    path = doc.path

    if (path is None and doc_encoding is None) or (path is not None and doc_encoding is not None):
        raise ValueError("Document should consist of path or (exclusive) encoding only.")

    # if doc is defined by encoding
    if doc_encoding is not None:
        # make a local (temporary) copy
        if doc_encoding.startswith(PDF_PREFIX):
            doc.pdf_encoding = doc.pdf_encoding[len(PDF_PREFIX):]
        path = google_client.convert_doc_to_pdf(doc, doc_id)
        doc.path = path

    try:
        upload_response = await pinecone_client.upload(user_id=user_id, document=doc)
        google_client.upload_file(user_id, path, doc_id)

        return UploadDocumentResponse(
            status=Status.Ok,
            doc_metadata=doc.get_document_metadata(),
            uploaded_vectors_num=upload_response.get("upserted_count")
        )
    except Exception:
        return UploadDocumentResponse(
            status=Status.Failed,
            doc_metadata=doc.get_document_metadata(),
            uploaded_vectors_num=0
        )

    finally:
        if doc_encoding is not None:
            # it means we've created the temporary file. Hence, we should
            # clean it as well.
            os.remove(path)



@docs_router.get("/{user_id}/{doc_id}")
async def get_doc_by_id(user_id: str, doc_id: str):
    # Retrieve the file content from GCS
    file_content = google_client.get_file_content(user_id, doc_id)

    if file_content is None:
        return Response(status_code=404)

    content_type = "application/pdf"

    # Stream the file content as the response body
    return StreamingResponse(
        iter([file_content]),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={doc_id}.pdf"}, )


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: str, body: dict) -> dict:
    """
    Given user_id and doc_id, delete the document from the vector storage
    and google-storage as well.

    Args:
        doc_id (str)

    Raises:
        Exception: _description_
    """
    user_id = body["user_id"]
    try:
        result = await pinecone_client.delete(user_id=user_id, document_id=doc_id)
        google_client.delete_file(user_id, doc_id)
        if len(result) == 0:
            return {'status': Status.Ok}
        raise Exception('delete failed')
    except Exception as e:
        return {'status': Status.Failed, 'error': str(e)}
