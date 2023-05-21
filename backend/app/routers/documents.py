from fastapi import APIRouter
from app.models.documents import DocumentMetaData, Document
import datetime as dt

docs_router = APIRouter(
    prefix="/documents"
)


doc_list = [ DocumentMetaData(user_id="1", document_description="desc", 
                              document_title="title", document_id=1, creation_time=dt.datetime.now(),
                              document_size=12) ]

doc_sample = Document(user_id="1", document_id=1, document_title="sample_doc", document_content="content" )


@docs_router.get("/")
async def get_all_docs_metadata() -> list[DocumentMetaData]:
    return doc_list


@docs_router.get("/{doc_id}")
async def get_doc_by_id(doc_id: int) -> Document:
    if (doc_id != 1):
        return Document(document_id=-1, document_title="Not exist", document_content="...")
    return doc_sample


@docs_router.post("/")
async def upload_doc(doc: Document) -> DocumentMetaData:
    doc_metadata =  DocumentMetaData(user_id=doc.user_id, document_description="desc", 
                              document_title=doc.document_title, document_id=doc.document_id, creation_time=dt.datetime.now(),
                              document_size=12)
    doc_list.append(doc_metadata)
    return doc_metadata


@docs_router.delete("/{doc_id}")
async def delete_doc(doc_id: int)-> dict: 
    return {"ok": True}
