# -*-Coding =utf-8 -*-

# @Time :2024/3/30 23:20

# @Author :jiajia

# @File:gptdemo.py

import re

# @software：PyCharm
# 设置 OpenAI API 访问 Token
import requests

# 定义全局变量保存对话上下文
context = {}


def Gptdemo(msg: str) -> str:
    global context

    url = "http://rd-gateway.patsnap.io"
    api_token = "cmVuamlhamlhOmdZRlhFVGNUS2Y5cUhRUzRzY0VKOWk="
    headers = {
        "Authorization": f"Basic {api_token}",
        "Content-Type": "application/json",
        "X-Ai-Engine": "anthropic"
    }

    # 在数据中添加上下文信息
    data = {
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "message": msg,
        "model": "claude-3-sonnet",
        "n": 1,
        "presence_penalty": 0,
        "role": "assistant",
        "seed": 0,
        "stop": ["string"],
        "stream": False,
        "temperature": 0,
        "top_p": 1,
        "user": "",
        "context": context  # 将上下文信息添加到数据中
    }
    response = requests.post(
        f"{url}/compute/openai_chatgpt_turbo", json=data, headers=headers
    )
    response_data = response.json()["data"]["message"]

    # 提取并更新新的上下文信息
    new_context = response.json()["data"].get("context",
                                              {})  # 使用get方法获取上下文，如果没有则返回空字典.get("context", {})  # 使用get方法获取上下文，如果没有则返回空字典
    if new_context:
        context = new_context

    return response_data


def chat():
    patterns = {
        r'hi|hello|hey': 'Hello!',
        r'how are you?': "I'm doing well, thanks for asking!",
        r'what is your name?': "My name is Claude.",
        r'bye|goodbye': "Goodbye!"
    }

    history = []

    print("Welcome! Type 'bye' or 'goodbye' to exit.")

    while True:
        user_input = input("> ").lower()

        if user_input in ['bye', 'goodbye']:
            print(patterns[user_input])
            break

        response = None
        for pattern, reply in patterns.items():
            if re.search(pattern, user_input):
                response = reply
                break

        if response:
            print(response)
            history.append((user_input, response))
        else:
            response = Gptdemo(user_input)  # 调用GPT生成响应
            print(response)
            history.append((user_input, response))


if __name__ == "__main__":
    chat()
