import json

from openai import OpenAI


def load_openai_settings() -> tuple[str, str | None]:
    """加载环境变量中的配置。"""
    from config import OPENAI_BASE_URL, OPENAI_MODEL_ID

    return OPENAI_MODEL_ID, OPENAI_BASE_URL


STRUCTURED_OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["thought", "action"],
    "properties": {
        "thought": {
            "type": "string",
            "description": "一句简短的当前判断或下一步计划。",
        },
        "action": {
            "type": "object",
            "additionalProperties": False,
            "required": ["type"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["tool", "finish"],
                },
                "name": {
                    "type": "string",
                    "description": "当 action.type 为 tool 时要调用的工具名。",
                },
                "args": {
                    "type": "object",
                    "description": "当 action.type 为 tool 时传给工具的参数。",
                    "additionalProperties": {
                        "type": ["string", "number", "boolean"]
                    },
                },
                "answer": {
                    "type": "string",
                    "description": "当 action.type 为 finish 时给用户的最终答案。",
                },
            },
        },
    },
}


class OpenAIClient:
    """
    一个用于调用 OpenAI API 的客户端。
    """

    def __init__(self):
        self.model, openai_base_url = load_openai_settings()
        client_kwargs = {}
        if openai_base_url:
            client_kwargs["base_url"] = openai_base_url
        self.client = OpenAI(**client_kwargs)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用 LLM API 来生成回应。"""
        try:
            response = self.client.responses.create(
                model=self.model,
                reasoning={"effort": "medium"},
                instructions=system_prompt,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "travel_agent_action",
                        "schema": STRUCTURED_OUTPUT_SCHEMA,
                        "strict": True,
                    }
                },
            )
            output_text = response.output_text or ""
            # 先做一次本地校验，尽早暴露不符合 schema 的异常输出。
            json.loads(output_text)
            return output_text
        except Exception as e:
            print(f"调用 LLM API 时发生错误: {e}")
            return "错误:调用大语言模型服务时出错。"
