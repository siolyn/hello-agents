import json

def parse_llm_output(llm_output: str) -> dict:
    """将 LLM 的输出转换成 JSON 对象"""
    parsed = json.loads(llm_output)
    if not isinstance(parsed, dict):
        raise ValueError("模型返回的 JSON 顶层必须是对象。")
    return parsed


def extract_thought(payload: dict) -> str:
    """获取 Thought"""
    thought = payload.get("thought")
    if not isinstance(thought, str) or not thought.strip():
        raise ValueError("缺少 thought 字段，或其值不是有效字符串。")
    return thought.strip()


def extract_action(payload: dict) -> dict:
    """获取 Action"""
    action = payload.get("action")
    if not isinstance(action, dict):
        raise ValueError("缺少 action 字段，或其值不是对象。")
    return action


def get_action_type(action: dict) -> str:
    action_type = action.get("type")
    if not isinstance(action_type, str) or not action_type.strip():
        raise ValueError("action.type 缺失或无效。")
    return action_type.strip()


def get_finish_answer(action: dict) -> str:
    answer = action.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("action.answer 缺失或无效。")
    return answer.strip()


def get_tool_name(action: dict) -> str:
    name = action.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("action.name 缺失或无效。")
    return name.strip()


def get_tool_args(action: dict) -> dict[str, str]:
    args = action.get("args", {})
    if not isinstance(args, dict):
        raise ValueError("action.args 必须是对象。")

    normalized_args: dict[str, str] = {}
    for key, value in args.items():
        if not isinstance(key, str):
            raise ValueError("action.args 的键必须是字符串。")
        normalized_args[key] = str(value)
    return normalized_args


def format_tool_call(tool_name: str, kwargs: dict[str, str]) -> str:
    if not kwargs:
        return f"{tool_name}()"

    parts = [f'{key}="{value}"' for key, value in kwargs.items()]
    return f"{tool_name}({', '.join(parts)})"
