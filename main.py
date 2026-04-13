from agent.loop import run_agent


if __name__ == "__main__":
    user_prompt = input("请输入你的旅行需求: ").strip()
    run_agent(user_prompt=user_prompt)
