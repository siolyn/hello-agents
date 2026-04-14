from openai import OpenAI


class OpenAIClient:
    """
    一个用于调用 OpenAI API 的客户端。
    """

    def __init__(self, model: str, api_key: str, base_url: str | None = None):
        self.model = model
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用 LLM API 来生成回应。"""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            parts = []
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    parts.append(delta.content)

            answer = "".join(parts)
            return answer or ""
        except Exception as e:
            print(f"调用 LLM API 时发生错误: {e}")
            return "错误:调用大语言模型服务时出错。"
