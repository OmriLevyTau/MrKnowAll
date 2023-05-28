from enum import Enum
from typing import List

from pydantic import BaseModel

from app.models.documents import DocumentMetaData


class Status(str, Enum):
    Ok = "Ok"
    Failed = "Failed"


class GetAllDocumentsMetadataResponse(BaseModel):
    status: Status
    docs_metadata: List[DocumentMetaData]


class GetDocumentByIdResponse(BaseModel):
    status: Status
    doc_metadata: List[DocumentMetaData]


class UploadDocumentResponse(BaseModel):
    status: Status  # change to enum
    doc_metadata: DocumentMetaData
    uploaded_vectors_num: int


class DeleteDocumentResponse(BaseModel):
    status: Status


class OpenAIResponse(BaseModel):
    status: Status
    content: str


class QueryResponse(BaseModel):
    status: Status
    response: OpenAIResponse
    query_content: str
    context: str
    references: list[str]
