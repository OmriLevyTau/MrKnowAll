import datetime as dt
from typing import List, Optional

from pydantic import BaseModel


class DocumentMetaData(BaseModel):
    """"
    This represents the object that is finally
    shown in the UI workspace.
    """
    user_id: str
    document_id: str
    document_title: Optional[str] = None
    document_description: Optional[str] = None
    document_size: Optional[str] = None
    creation_time: Optional[dt.datetime] = None

    def get_document_id(self) -> str:
        return self.document_id

    def get_document_title(self) -> Optional[str]:
        return self.document_title

    def get_user_id(self) -> str:
        return self.user_id

    class Config:
        allow_mutation = True


class Document(BaseModel):
    """
    @@@ How to hold pdf?
    meanwhile a path
    """
    document_metadata: DocumentMetaData
    path: Optional[str] = None
    pdf_encoding: Optional[str] = None

    def get_document_metadata(self) -> DocumentMetaData:
        return self.document_metadata

    class Config:
        allow_mutation = True


class DocumentVectorChunkMetadata(BaseModel):
    user_id: str
    document_id: str
    original_content: str


class DocumentVectorChunk(BaseModel):
    """"
    This represents the object that is finally
    stored in the vector database.
    """
    vector_id: Optional[str] = None
    embedding: Optional[List[float]] = None
    metadata: Optional[DocumentVectorChunkMetadata] = None


class VectorContextQuery(BaseModel):
    """
    This model represents a vector context query. That is,
    given a vector_id='c' represents original sentence:='C',
    get its context, that is sentence A,B,D,E
    """
    user_id: str
    document_id: str
    vector_id: str
    context_window: Optional[int] = 2

    def get_document_id(self) -> str:
        return self.document_id

    def get_vector_id(self) -> str:
        return self.vector_id

    def get_context_window(self) -> Optional[int]:
        return self.context_window
