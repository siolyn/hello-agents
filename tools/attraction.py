from tavily import TavilyClient
from config import TAVILY_API_KEY

def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气，使用 Tavily Search API 搜索并返回优化后的景点推荐
    """
    # 初始化 Tavily 客户端
    tavily = TavilyClient(api_key=TAVILY_API_KEY)

    # 构造一个精确查询
    query = f"'{city}' 在'{weather}'天气下最值得去的景点及理由"

    try:
        # 调用 API
        response = tavily.search(query=query, search_depth="basic", include_answer=True)

        # 可以直接返回回答
        if response.get("answer"):
            return response["answer"]

        # 如果没有综合性回答，则拼接原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result['title']}: {result['content']}")

        if not formatted_results:
            return "抱歉，没有找到符合需求的相关景点推荐。"

        return "根据搜索，为您作出以下推荐:\n" + "\n".join(formatted_results)

    except Exception as e:
        return f"错误:执行 Tavily 搜索时出现问题 - {e}"
