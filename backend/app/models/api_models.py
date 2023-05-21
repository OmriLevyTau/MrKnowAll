from typing import List
from enum import Enum
from app.models.documents import DocumentMetaData
from pydantic import BaseModel


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
    status: Status # change to enum
    doc_metadata: DocumentMetaData

class DeleteDocumentResponse(BaseModel):
    status: Status
