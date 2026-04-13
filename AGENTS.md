# Repository Guidelines

## Project Structure & Module Organization
This is a small Python CLI agent for travel queries. `main.py` is the local entry point. Core loop and response parsing live in `agent/` (`loop.py`, `parser.py`). Model access is isolated in `clients/`, prompts live in `prompts/`, and callable tools are in `tools/` (`weather.py`, `attraction.py`). Shared configuration is in `config.py`. Put new automated checks under `tests/` using files like `test_parser.py`.

## Build, Test, and Development Commands
Use the existing virtual environment when available: `source .venv/bin/activate`.

- `python main.py`: run the CLI and enter a travel request.
- `pytest`: run automated tests in `tests/`.
- `python -m compileall .`: quick syntax validation across the repo.

This repo does not fully pin dev dependencies yet, so install missing tools such as `pytest` into `.venv` before relying on them. If you add or change dependencies, update `requirements.txt` and reinstall with `pip install -r requirements.txt`.

## Coding Style & Naming Conventions
Follow current Python style: 4-space indentation, `snake_case` for functions and variables, `PascalCase` for classes, and type hints where they improve readability. Keep modules focused on one job, matching the existing split between `agent`, `clients`, `tools`, and `prompts`. Prefer short docstrings and comments only where the control flow is not obvious. Keep user-facing terminal text and inline comments consistent with the current Chinese-language style.

## Testing Guidelines
There is a `tests/` package but very little coverage today, so new behavior should ship with tests. Prefer `pytest` with filenames `test_*.py` and test names like `test_parse_llm_output_handles_code_fence`. Focus first on parser edge cases, tool error handling, and loop behavior around malformed model output. Before opening a PR, run `pytest` and at minimum `python -m compileall .`.

## Commit & Pull Request Guidelines
Recent history uses short Conventional Commit style prefixes such as `feat: 美化了日志` and `feat: 新增自定义提需求功能`. Keep that pattern: `feat:`, `fix:`, `refactor:`, `docs:`. PRs should explain what changed, why it changed, and how you verified it. Include a sample CLI interaction or terminal output when behavior or logs change.

## Security & Configuration Tips
`config.py` requires `.env` values for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL_ID`, and `TAVILY_API_KEY`. Never commit real secrets. If you change config loading or third-party integrations, document the required variables and test with a real prompt through `python main.py`.
