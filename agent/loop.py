from agent.parser import (
    extract_action,
    extract_finish_answer,
    parse_tool_call,
    truncate_thought_action,
)
from clients.openai_compatible import OpenAICompatibleClient
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_ID
from prompts.system_prompt import AGENT_SYSTEM_PROMPT
from tools import available_tools


def run_agent(
    user_prompt: str = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。",
    max_steps: int = 5,
) -> str | None:
    llm = OpenAICompatibleClient(
        model=OPENAI_MODEL_ID,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    prompt_history = [f"用户请求: {user_prompt}"]
    print(f"用户输入: {user_prompt}\n" + "=" * 40)

    for i in range(max_steps):
        print(f"--- 循环 {i + 1} ---\n")

        full_prompt = "\n".join(prompt_history)
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)
        llm_output, was_truncated = truncate_thought_action(llm_output)
        if was_truncated:
            print("已截断多余的 Thought-Action 对。")

        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        action_str = extract_action(llm_output)
        if not action_str:
            observation = (
                "错误：未能解析到 Action 字段。"
                "请确保回复严格遵循 'Thought: ... Action: ...' 的格式。"
            )
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "=" * 40)
            prompt_history.append(observation_str)
            continue

        if action_str.startswith("Finish"):
            final_answer = extract_finish_answer(action_str)
            if final_answer is None:
                observation = "错误：Finish 格式不正确，应为 Finish[最终答案]。"
                observation_str = f"Observation: {observation}"
                print(f"{observation_str}\n" + "=" * 40)
                prompt_history.append(observation_str)
                continue

            print(f"任务完成，最终答案: {final_answer}")
            return final_answer

        tool_name, kwargs = parse_tool_call(action_str)
        if not tool_name:
            observation = f"错误:无法解析工具调用 '{action_str}'"
        elif tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)

    print("任务结束：已达到最大循环次数。")
    return None
