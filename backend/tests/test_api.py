import pytest
from httpx import AsyncClient, ASGITransport
from pytest_mock import MockerFixture

# Patch LLM and embedding calls BEFORE importing the app
@pytest.fixture(autouse=True, scope="module")
def patch_llm_and_embedding(mocker: MockerFixture):
    # Patch OllamaAdapter
    mocker.patch(
        "app.services.llm_provider_factory.OllamaAdapter.generate_response",
        return_value="This is a mocked Ollama answer."
    )
    mocker.patch(
        "app.services.llm_provider_factory.OllamaAdapter.create_embedding",
        return_value=[0.1, 0.2, 0.3]
    )
    # Patch OpenAIAdapter
    mocker.patch(
        "app.adapters.openai_adapter.OpenAIAdapter.generate_response",
        return_value="This is a mocked OpenAI answer."
    )
    mocker.patch(
        "app.adapters.openai_adapter.OpenAIAdapter.create_embedding",
        return_value=[0.4, 0.5, 0.6]
    )

# Now import the app after the client is mocked
from app.main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post("/api/chat/", json={"query": "What is this project about?", "provider": "openai"})
        assert response.status_code == 200
        assert "mocked" in response.json().get("answer", "")

@pytest.mark.asyncio
async def test_upload_document(monkeypatch, mocker: MockerFixture):
    # You can mock the ingestion_service.ingest_document here if needed
    pass  # Implement as needed