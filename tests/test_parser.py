import pytest

from agent.parser import parse_llm_output


def test_parse_llm_output_accepts_strict_json_object():
    payload = parse_llm_output('{"thought":"测试","action":{"type":"finish","answer":"完成"}}')

    assert payload == {
        "thought": "测试",
        "action": {
            "type": "finish",
            "answer": "完成",
        },
    }


def test_parse_llm_output_rejects_non_json_text():
    with pytest.raises(ValueError):
        parse_llm_output("```json\n{}\n```")
