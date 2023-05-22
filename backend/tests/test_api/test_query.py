import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_is_healthy():
    response = client.get("/")
    assert (response.status_code == 200)


@pytest.mark.asyncio
async def test_openAI_integration():
    print('hello')
    response = client.post(url="/query", json={
        "user_id": 1,
        "query_id": 2,
        "query_content": "how are you today?"
    })
    assert (response.status_code == 200)
    print(response.json())
