import requests as requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from loguru import logger

app = FastAPI()


class Query(BaseModel):
    role: str
    prompt: str  # 用户或者AImodel的Prompt
    api_key: str  # 是否为多轮对话


def openai_response(query):
    prompt = query.prompt
    role = query.role
    api_key = query.api_key
    params = {
        "messages": [{"role": role, "content": prompt}],
        # 如果需要切换模型，在这里修改
        "model": "gpt-3.5-turbo",
    }
    headers = {
        "Authorization": "Bearer " + api_key,
    }
    response = requests.post(
        "https://aigptx.top/v1/chat/completions",
        headers=headers,
        json=params,
        stream=False,
    )
    res = response.json()
    res_content = res["choices"][0]["message"]["content"]
    return res_content


@app.post("/chatgpt")
async def get_chatgpt_response(query: Query):
    response = openai_response(query)
    ret = {"response": response}
    return ret


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port="8002")
