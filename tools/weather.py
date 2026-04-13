import requests

def get_weather(city: str) -> str:
    """
    通过调用 wttr.in API 查询真实的天气信息。
    """
    # format=j1 用来获取 JSON 格式的信息
    url = f"https://wttr.in/{city}?format=j1"

    try:
        # 调用 API
        response = requests.get(url, timeout=15)
        # 如果状态码不为 200 则触发异常
        response.raise_for_status()
        # 转换成 JSON 的字典结构
        try:
            data = response.json()
        except ValueError as e: # JSONDecodeError 的父类
            return f"错误:返回数据不是合法 JSON - {e}"

        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        temp_c = current_condition["temp_C"]

        return f"{city}当前天气:{weather_desc}，气温{temp_c}摄氏度"

    except requests.exceptions.RequestException as e:
        return f"错误:查询天气时遇到网络问题 - {e}"
    except (KeyError, IndexError, TypeError) as e:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"
