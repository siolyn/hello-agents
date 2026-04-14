from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


def require_env(name: str, value: str) -> str:
    """
    校验环境变量是否存在
    如果 value 为空字符串、None 等，就直接报错
    """
    if not value:
        raise ValueError(f"缺少环境变量: {name}")
    return value


def get_env(name: str, default: str = "", required: bool = True) -> str:
    """
    统一读取环境变量。
    - name: 环境变量名
    - default: 默认值
    - required: 是否必须存在
    """
    value = os.getenv(name, default)
    if required:
        return require_env(name, value)
    return value


OPENAI_API_KEY = get_env("OPENAI_API_KEY")
OPENAI_BASE_URL: str | None = get_env("OPENAI_BASE_URL", required=False) or None
OPENAI_MODEL_ID = get_env("OPENAI_MODEL_ID")
TAVILY_API_KEY = get_env("TAVILY_API_KEY")
