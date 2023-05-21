from typing import Optional
from pydantic import BaseModel
import datetime as dt


class DocumentMetaData(BaseModel):
    user_id: str
    document_id: int
    document_title: Optional[str] = None
    document_description: Optional[str] = None
    document_size: Optional[str] = None    
    creation_time: dt.datetime

    class Config:
        allow_mutation = True



class Document(BaseModel):
    """
    placeholder
    """
    user_id: str
    document_id: int
    document_metadata: Optional[DocumentMetaData] = None

    def get_document_metadata(self) -> Optional[DocumentMetaData]:
        return self.document_metadata
    class Config:
        allow_mutation = True

class DocumentMetaDataFilter(BaseModel):
    user_id: Optional[str] = None
    document_id: Optional[int] = None




