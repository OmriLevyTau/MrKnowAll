import pytest
from fastapi.testclient import TestClient
import json
from app.main import app
from app.models.api_models import Status

client = TestClient(app)


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
    print('hello')
    print(data['response'])
    assert (data['status'] == Status.Ok)
    assert (data['response'] is not None)
    # Cannot predict what chatGPT answer will look like
    assert (data['response']['status'] is not None)
    assert (data['response']['content'] is not None)
    