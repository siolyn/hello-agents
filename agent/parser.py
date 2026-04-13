import re


THOUGHT_ACTION_PATTERN = re.compile(
    r"(Thought:.*?Action:.*?)(?=(?:\s*Thought:|\s*Action:|\s*Observation:)|\Z)",
    re.DOTALL,
)
THOUGHT_PATTERN = re.compile(r"Thought:\s*(.*?)\s*Action:", re.DOTALL)
ACTION_PATTERN = re.compile(r"Action:\s*(.*)", re.DOTALL)
TOOL_NAME_PATTERN = re.compile(r"(\w+)\(")
ARGS_PATTERN = re.compile(r"\((.*)\)")
KWARGS_PATTERN = re.compile(r'(\w+)="([^"]*)"')
FINISH_PATTERN = re.compile(r"Finish\[(.*)\]", re.DOTALL)


def truncate_thought_action(llm_output: str) -> tuple[str, bool]:
    match = THOUGHT_ACTION_PATTERN.search(llm_output)
    if not match:
        return llm_output.strip(), False

    truncated = match.group(1).strip()
    return truncated, truncated != llm_output.strip()


def extract_action(llm_output: str) -> str | None:
    match = ACTION_PATTERN.search(llm_output)
    if not match:
        return None
    return match.group(1).strip()


def extract_thought(llm_output: str) -> str | None:
    match = THOUGHT_PATTERN.search(llm_output)
    if not match:
        return None
    return match.group(1).strip()


def extract_finish_answer(action_str: str) -> str | None:
    match = FINISH_PATTERN.fullmatch(action_str)
    if not match:
        return None
    return match.group(1)


def parse_tool_call(action_str: str) -> tuple[str | None, dict[str, str]]:
    tool_name_match = TOOL_NAME_PATTERN.search(action_str)
    args_match = ARGS_PATTERN.search(action_str)

    if not tool_name_match or not args_match:
        return None, {}

    tool_name = tool_name_match.group(1)
    args_str = args_match.group(1)
    kwargs = dict(KWARGS_PATTERN.findall(args_str))
    return tool_name, kwargs
