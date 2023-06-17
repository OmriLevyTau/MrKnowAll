# import pytest
# from tests.mock_runs.mock_file_handling import mock_upload, mock_get_chunks
# from app.config import EXPLORE_LOCAL_FILE
# from app.models.documents import Document,DocumentMetaData
# from tests.test_storage.test_vector_storage.test_pinecone import (
#     TEST_DOCUMENT_ID, TEST_DOCUMENT_METADATA, TEST_USER_ID)


# # to run these tests change the value of these to False, if SKIP = True skips all tests
# SKIP = True
# SKIP_UPLOAD = True
# SKIP_CHUNKS = True


# ARG_FILE_NAME = "test.pdf" #plceholder
# ARG_PATH = EXPLORE_LOCAL_FILE[:-15] + ARG_FILE_NAME # should be {user-path}//ARG_FILE_NAME
# ARG_METADATA = DocumentMetaData(user_id=TEST_USER_ID,document_id=TEST_DOCUMENT_ID)
# ARG = Document(document_metadata=ARG_METADATA,path=ARG_PATH)

# @pytest.mark.runningTime
# @pytest.mark.skipif(condition=SKIP or SKIP_UPLOAD,reason="")
# def test_upload_time():
#     mock_upload(ARG)

# @pytest.mark.runningTime
# @pytest.mark.skipif(condition=SKIP or SKIP_CHUNKS,reason="")
# def test_chunk_time():
#     mock_get_chunks(ARG)

