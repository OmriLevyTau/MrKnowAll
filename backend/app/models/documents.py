from typing import Optional
from pydantic import BaseModel
import datetime as dt


class DocumentMetaData(BaseModel):
    user_id: int
    document_id: int
    document_title: str
    document_description: str
    document_size: int    
    creation_time: dt.datetime


class Document(BaseModel):
    """
    placeholder
    """
    user_id: int
    document_id: int
    document_title: str
    document_content: str




