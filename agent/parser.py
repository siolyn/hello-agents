import json


def strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped

    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def extract_json_object(text: str) -> str:
    stripped = strip_code_fence(text)
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped

    start = stripped.find("{")
    if start == -1:
        raise ValueError("未找到 JSON 对象起始位置。")

    depth = 0
    in_string = False
    escaped = False

    # 有些模型会在 JSON 前后夹带少量文本，这里按括号层级截出第一个完整对象。
    for index in range(start, len(stripped)):
        char = stripped[index]

        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return stripped[start : index + 1]

    raise ValueError("未找到完整的 JSON 对象。")


def parse_llm_output(llm_output: str) -> tuple[dict, bool]:
    json_text = extract_json_object(llm_output)
    parsed = json.loads(json_text)
    if not isinstance(parsed, dict):
        raise ValueError("模型返回的 JSON 顶层必须是对象。")
    # 第二个返回值用来提示“模型有额外文本，但已自动清理”。
    return parsed, json_text != llm_output.strip()


def extract_thought(payload: dict) -> str:
    thought = payload.get("thought")
    if not isinstance(thought, str) or not thought.strip():
        raise ValueError("缺少 thought 字段，或其值不是有效字符串。")
    return thought.strip()


def extract_action(payload: dict) -> dict:
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
