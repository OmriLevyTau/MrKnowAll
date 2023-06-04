import json

import pytest
from fastapi.testclient import TestClient

from app.config import EXPLORE_LOCAL_FILE
from app.main import app
from app.models.api_models import Status
from app.models.documents import Document, DocumentMetaData
from app.models.query import Query
from app.routers.chat import query
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from tests.test_storage.test_vector_storage.test_pinecone import (
    TEST_DOCUMENT_ID, TEST_DOCUMENT_METADATA, TEST_USER_ID)

client = TestClient(app)
pinecone_client = PineconeVectorStorage()


def clear_all() -> None:
    delete_response = pinecone_client.index.delete(
        filter={
            "user_id": {"$eq": TEST_USER_ID},
            "document_id": {"$eq": TEST_DOCUMENT_ID}
        }
    )


@pytest.fixture(autouse=True)
def setup_and_teardown():
    '''
    Validates that no test data stored in the vector database. 
    '''
    # Will run before each test
    # save number of existing vectors
    # index.describe_index_stats()
    clear_all()
    # test will run at this point
    yield
    # will run after the test
    clear_all()
    # assert number of existing vectors.


@pytest.mark.asyncio
async def test_openai_integration():
    query_response = client.post(url="/api/v0/query", json={
        "user_id": 1,
        "query_id": 2,
        "query_content": "how are you today?"
    })
    assert (query_response.status_code == 200)
    query_response_content = query_response.content.decode('utf-8')
    data = json.loads(query_response_content)

    assert (data['status'] == Status.Ok)
    assert (data['response'] is not None)
    # Cannot predict what chatGPT answer will look like
    assert (data['response']['status'] is not None)
    assert (data['response']['content'] is not None)


@pytest.mark.asyncio
async def test_full_query_process():

    doc = Document(
        document_metadata=TEST_DOCUMENT_METADATA,
        path=EXPLORE_LOCAL_FILE
    )

    upload_response = client.post(url="/api/v0/documents", json={
        'path': EXPLORE_LOCAL_FILE,
        'document_metadata': {
            'user_id': TEST_USER_ID,
            'document_id': TEST_DOCUMENT_ID
        }
    })

    query_response = client.post(url="/query", json={
        "user_id": TEST_USER_ID,
        "query_id": 1,
        "query_content": 'what did the Islamic Jihad spokesman say?'
    })

    # ai_asistant_response = await query(query=query_to_be_sent)
    # assert(ai_asistant_response.status == Status.Ok)
    assert (query_response.status_code == 200)
    query_response_content = query_response.content.decode('utf-8')
    response_data = json.loads(query_response_content)
    assert (response_data['status'] == Status.Ok)
    assert (response_data['response'] is not None)
    response_content = response_data['response']
    assert (response_content is not None)
    assert (response_content['status'] is not None)
    assert (response_content['status'] == Status.Ok)
    assert (response_content['content'] is not None)
    assert ("The Islamic Jihad spokesman, Tareq Selmi".lower() in response_content['content'].lower(
    ) or "Islamic Jihad spokesman".lower() in response_content['content'].lower())

    assert (response_data['query_content'] is not None)
    original_query = response_data['query_content']
    assert (original_query is not None)
    prompt_start = "Please generate response based solely on the information I provide in this text. Do not reference any external knowledge or provide additional details beyond what I have given"
    assert (prompt_start in original_query)
    prompt_finish = "my question is: what did the Islamic Jihad spokesman say?"
    assert (prompt_finish in original_query)

    assert (response_data['references'] is not None)
    prompt_references = response_data['references']
    assert ('test' in prompt_references)

    assert (response_data['context'] is not None)
    context = response_data['context']

    prompt_important_sentence_1 = "\nIn Gaza, Islamic Jihad spokesman Tareq Selmi said Israel had agreed to halt its policy"
    prompt_important_sentence_2 = "or assassination by the \noccupation will be met with a response and the Zionist enemy bears the responsibility"

    assert (prompt_important_sentence_1 in context)
    assert (prompt_important_sentence_2 in context)
