from clients.openai_client import OpenAIClient


class DummyOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


def test_init_uses_default_base_url_when_not_provided(monkeypatch):
    monkeypatch.setattr("clients.openai_client.OpenAI", DummyOpenAI)

    client = OpenAIClient(
        model="gpt-4.1-mini",
        api_key="test-key",
    )

    assert client.model == "gpt-4.1-mini"
    assert client.client.kwargs == {"api_key": "test-key"}


def test_init_passes_custom_base_url(monkeypatch):
    monkeypatch.setattr("clients.openai_client.OpenAI", DummyOpenAI)

    client = OpenAIClient(
        model="gpt-4.1-mini",
        api_key="test-key",
        base_url="https://example.com/v1",
    )

    assert client.client.kwargs == {
        "api_key": "test-key",
        "base_url": "https://example.com/v1",
    }
