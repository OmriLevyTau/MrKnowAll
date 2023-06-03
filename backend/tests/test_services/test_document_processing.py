import os

import pytest

from app.models.documents import Document, DocumentMetaData
from app.services.document_proccessing import get_documents_chunks
from tests.test_services.services_test_constants import TEST_PDF_ENCODING

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test.pdf')
TEST_USER_ID = "test"
TEST_DOCUMENT_ID="test"
TEST_DOCUMENT_METADATA = DocumentMetaData(user_id=TEST_USER_ID, document_id=TEST_DOCUMENT_ID)


def test_read_pdf_file():
    doc = Document(
        document_metadata=TEST_DOCUMENT_METADATA,
        path=TESTDATA_FILENAME
    )
    chunks = get_documents_chunks(doc)
    assert (chunks is not None) and (len(chunks)>0)
    assert ("Hello world".lower() in chunks[0].lower())
    assert ("mr know all".lower() in chunks[1].lower())

def test_read_pdf_encoding():
    # TEST_PDF_ENCODING generated base64 encoding for test.pdf 
    # using https://base64.guru/converter/encode/pdf


    doc = Document(
        document_metadata=TEST_DOCUMENT_METADATA,
        pdf_encoding=TEST_PDF_ENCODING
    )

    chunks = get_documents_chunks(doc)
    assert (chunks is not None) and (len(chunks)>0)
    assert ("Hello world".lower() in chunks[0].lower())
    assert ("mr know all".lower() in chunks[1].lower())
    
