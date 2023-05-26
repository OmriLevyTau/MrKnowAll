import pytest
import json
from app.main import app
from app.models.query import Query
from app.models.api_models import Status
from app.models.documents import Document, DocumentMetaData
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage
from app.routers.chat import query
from tests.test_storage.test_vector_storage.test_pinecone import TEST_DOCUMENT_ID, TEST_USER_ID, TEST_DOCUMENT_METADATA
from fastapi.testclient import TestClient


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
async def test_is_healthy():
    response = client.get("/")
    assert (response.status_code == 200)


@pytest.mark.asyncio
async def test_openai_integration():
    print('hello')
    query_response = client.post(url="/query", json={
        "user_id": 1,
        "query_id": 2,
        "query_content": "how are you today?"
    })
    assert (query_response.status_code == 200)
    query_response_content = query_response.content.decode('utf-8')
    data = json.loads(query_response_content)

    '''
    for example:
    {
        'status': 'Ok', 
        'response': {
            'status': 'Ok', 
            'content': 'As an AI language model, I do not have emotions, 
                        but I am always ready to assist you with your requests. 
                        How can I assist you today?'
        }
    }

    '''

    assert (data['status'] == Status.Ok)
    assert (data['response'] is not None)
    # Cannot predict what chatGPT answer will look like
    assert (data['response']['status'] is not None)
    assert (data['response']['content'] is not None)
    

@pytest.mark.asyncio
async def test_full_query_process():
    
    doc = Document(
        document_metadata=TEST_DOCUMENT_METADATA,
        path='C:\\Users\\idani\\Desktop\\dev\\MrKnowAll\\backend\\resources\\israel-gaza.pdf'
    )

    upload_response = await pinecone_client.upload(user_id=TEST_USER_ID, document=doc)
    
    query_to_be_sent = Query(user_id=TEST_USER_ID, query_id='1', query_content='what did the Islamic Jihad spokesman say?')
    AIasistant_response = await query(query=query_to_be_sent)
    assert(AIasistant_response.status == Status.Ok)
    

