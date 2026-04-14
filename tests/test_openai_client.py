from types import SimpleNamespace

from clients.openai_client import OpenAIClient, STRUCTURED_OUTPUT_SCHEMA


class DummyResponses:
    def __init__(self):
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return SimpleNamespace(output_text='{"thought":"测试","action":{"type":"finish","answer":"完成"}}')


class DummyOpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.responses = DummyResponses()


def test_init_uses_default_environment_client(monkeypatch):
    monkeypatch.setattr("clients.openai_client.OpenAI", DummyOpenAI)
    monkeypatch.setattr(
        "clients.openai_client.load_openai_settings",
        lambda: ("test-model", None),
    )

    client = OpenAIClient()

    assert client.model == "test-model"
    assert client.client.kwargs == {}


def test_generate_uses_responses_api(monkeypatch):
    monkeypatch.setattr("clients.openai_client.OpenAI", DummyOpenAI)
    monkeypatch.setattr(
        "clients.openai_client.load_openai_settings",
        lambda: ("test-model", None),
    )

    client = OpenAIClient()
    result = client.generate("用户问题", "系统提示")

    assert result == '{"thought":"测试","action":{"type":"finish","answer":"完成"}}'
    assert client.client.responses.last_kwargs == {
        "model": "test-model",
        "reasoning": {"effort": "medium"},
        "instructions": "系统提示",
        "input": "用户问题",
        "text": {
            "format": {
                "type": "json_schema",
                "name": "travel_agent_action",
                "schema": STRUCTURED_OUTPUT_SCHEMA,
                "strict": True,
            }
        },
    }


def test_generate_rejects_invalid_json(monkeypatch):
    monkeypatch.setattr("clients.openai_client.OpenAI", DummyOpenAI)
    monkeypatch.setattr(
        "clients.openai_client.load_openai_settings",
        lambda: ("test-model", None),
    )

    client = OpenAIClient()
    client.client.responses.create = lambda **kwargs: SimpleNamespace(output_text="not json")

    result = client.generate("用户问题", "系统提示")

    assert result == "错误:调用大语言模型服务时出错。"
