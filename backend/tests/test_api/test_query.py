import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_is_healthy():
    response = client.get("/")
    assert(response.status_code==200)
