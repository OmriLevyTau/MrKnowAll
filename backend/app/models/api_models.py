from pydantic import BaseModel
from typing import List
from enum import Enum
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


class DeleteDocumentResponse(BaseModel):
    status: Status


class OpenAIResponse(BaseModel):
    status: Status
    content: str


class QueryResponse(BaseModel):
    status: Status
    response: OpenAIResponse
