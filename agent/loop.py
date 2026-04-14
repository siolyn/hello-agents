from agent.parser import (
    extract_action,
    extract_thought,
    format_tool_call,
    get_action_type,
    get_finish_answer,
    get_tool_args,
    get_tool_name,
    parse_llm_output,
)
from clients.openai_client import OpenAIClient
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL_ID
from prompts.system_prompt import AGENT_SYSTEM_PROMPT
from tools import available_tools


def print_block(title: str, content: str) -> None:
    print(title)
    for line in content.strip().splitlines():
        print(f"  {line}")
    print()


def print_step_header(step: int) -> None:
    print(f"步骤 {step}")


def run_agent(
    user_prompt: str = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。",
    max_steps: int = 5,
) -> str | None:
    llm = OpenAIClient(
        model=OPENAI_MODEL_ID,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )

    # prompt_history 记录“用户请求 -> 模型决策 -> 工具观察”，多轮推理都靠它续上上下文。
    prompt_history = [f"用户请求: {user_prompt}"]
    print()
    print_block("你的请求", user_prompt)

    for i in range(max_steps):
        step = i + 1
        print_step_header(step)

        full_prompt = "\n".join(prompt_history)
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)

        try:
            payload, was_trimmed = parse_llm_output(llm_output)
            if was_trimmed:
                print_block("提示", "已自动提取模型返回中的 JSON 主体。")

            thought_str = extract_thought(payload)
            print_block("思考", thought_str)

            action = extract_action(payload)
            action_type = get_action_type(action)
            # 原始模型输出也要回灌给下一轮，否则模型会丢失自己上一轮的决策。
            prompt_history.append(llm_output)
        except (ValueError, TypeError) as e:
            observation = f"错误：模型返回的 JSON 无法解析 - {e}"
            observation_str = f"Observation: {observation}"
            print_block("异常", observation)
            prompt_history.append(observation_str)
            continue

        if action_type == "finish":
            try:
                final_answer = get_finish_answer(action)
            except ValueError as e:
                observation = f"错误：最终答案格式不正确 - {e}"
                observation_str = f"Observation: {observation}"
                print_block("异常", observation)
                prompt_history.append(observation_str)
                continue

            print_block("执行", 'action.type = "finish"')
            print_block("最终答案", final_answer)
            return final_answer

        if action_type != "tool":
            observation = f'错误：不支持的 action.type "{action_type}"'
            observation_str = f"Observation: {observation}"
            print_block("异常", observation)
            prompt_history.append(observation_str)
            continue

        try:
            tool_name = get_tool_name(action)
            kwargs = get_tool_args(action)
            action_display = format_tool_call(tool_name, kwargs)
            print_block("执行", action_display)
        except ValueError as e:
            observation = f"错误：工具调用格式不正确 - {e}"
            observation_str = f"Observation: {observation}"
            print_block("异常", observation)
            prompt_history.append(observation_str)
            continue

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 工具执行结果同样作为 Observation 放回上下文，供下一轮继续判断。
        observation_str = f"Observation: {observation}"
        print_block("结果", observation)
        prompt_history.append(observation_str)

    print_block("结束", "已达到最大循环次数，任务未完成。")
    return None
