import pytest 
from logging import (getLogger,FileHandler,debug,Formatter,DEBUG)
from app.config import EXPLORE_LOCAL_FILE
from app.main import app
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from fastapi.testclient import TestClient
from tests.test_storage.test_vector_storage.test_pinecone import TEST_USER_ID
from app.models.documents import Document,DocumentMetaData

client = TestClient(app)
pinecone_client = PineconeVectorStorage()

skip = True

suffix = "resources\\israel-gaza.pdf"
log_output_path = EXPLORE_LOCAL_FILE[:-len(suffix)] + "run_time_test_output.log"

test_logger = getLogger(__name__)
test_logger.propagate = False
test_logger.setLevel(DEBUG)
test_handler = FileHandler(filename=log_output_path)
test_handler.setLevel(DEBUG)
log_format = ""
test_formatter = Formatter(log_format)
test_handler.setFormatter(test_formatter)
test_logger.addHandler(test_handler)

test_files_dir_path = EXPLORE_LOCAL_FILE[:-len(suffix)] + "//tests//test_run_times//resources//"
test_file_names = []






def test_run_time():
    if skip:
        return
    for file_name in test_file_names:
        file_path = test_files_dir_path+file_name + ".pdf"
        
        doc_metadata = DocumentMetaData(document_id=file_name,user_id=TEST_USER_ID)
        doc = Document(path=file_path,document_metadata=doc_metadata)
        upload_response = client.post(url="/api/v0/documents", json={
        'path': file_path,
        'document_metadata': {
            'user_id': TEST_USER_ID,
            'document_id': file_name
        }
    })










