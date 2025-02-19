import pytest

from fastapi.testclient import TestClient

from rag.entrypoints.rest import app

@pytest.fixture(scope="module")
def client(compose):
    return TestClient(app)


def test_send_messages(client: TestClient):
    response = client.post("/chat", json={"model": "mock", "messages": [{"role": "user", "content": "Hello, world!"}]}, params={"stream": False})
    assert response.status_code == 200
    assert response.json() == {"response": "Hello, world!"}

def test_send_messages_stream(client: TestClient):
    with client.stream("POST", "/chat", json={"model": "mock", "messages": [{"role": "user", "content": "Hello, world!"}]}, params={"stream": True}) as response:
        assert response.status_code == 200

        buffer = ""
        for text in response.iter_lines():
            buffer += text[7:-1]

        assert buffer == "Hello, world!"
