import pytest # pyright: ignore[reportMissingImports]
from httpx import AsyncClient, ASGITransport
from pytest_mock import MockerFixture # pyright: ignore[reportMissingImports]

# Now import the app after the client is mocked
from app.main import app

@pytest.mark.asyncio
async def test_chat_endpoint(mocker: MockerFixture):
    # Mock LLM and embedding client methods to avoid real network calls
    mocker.patch("app.services.llm_provider_factory.OllamaAdapter.generate_response", return_value="This is a mocked answer.")
    mocker.patch("app.services.llm_provider_factory.OllamaAdapter.create_embedding", return_value=[0.1, 0.2, 0.3])
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post("/api/chat/", json={"query": "What is this project about?"})
        if response.status_code != 200:
            print("Response status:", response.status_code)
            print("Response content:", response.text)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)

@pytest.mark.asyncio
async def test_upload_document(monkeypatch, mocker: MockerFixture):
    # You can mock the ingestion_service.ingest_document here if needed
    pass  # Implement as needed