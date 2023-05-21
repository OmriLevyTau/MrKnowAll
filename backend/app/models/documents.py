from pydantic import BaseModel
from typing import Optional, List
import datetime as dt


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
    
    def get_document_title(self) -> str:
        return self.document_title
    class Config:
        allow_mutation = True

class Document(BaseModel):
    """
    @@@ How to hold pdf?
    """
    document_metadata: DocumentMetaData

    def get_document_metadata(self) -> Optional[DocumentMetaData]:
        return self.document_metadata
    class Config:
        allow_mutation = True

class DocumentVectorChunkMetadata(BaseModel):
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
    

