import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from prompt.beauty import Beauty
from prompt.imagellm import ImageExtractorLLM
from gpt import ChatGPT
from config import prompt_config as config


app = FastAPI()


class Query(BaseModel):  # 定义请求参数, 用于接收前端传来的参数
    id_list: list
    api_key: str  # 是否为多轮对话


def user_profile(query):
    # Parameters
    id_list = query.id_list
    api_key = query.api_key
    # Data
    # meta = "/home/ubuntu/os/lllrrr/Item_Agent/amazon/raw/Beauty.json"
    meta = config["amazon_beauty_raw_path"]
    # tree = "/home/ubuntu/os/lllrrr/Item_Agent/Planning_Tree/item_tree.json"
    tree = config["item_tree_path"]
    # Models
    # Needed to deploy before calling
    image_llm = ImageExtractorLLM(config)
    gpt = ChatGPT(config)
    bea = Beauty(meta, tree, api_key, image_llm, gpt)
    # Get results
    result = bea.get_user_profile(id_list)
    return result


@app.post("/user_profile")
async def get_user_profile(query: Query):
    response = user_profile(query)
    ret = {"response": response}
    return ret


if __name__ == "__main__":
    logger.info("Prompt Server Config: ")
    logger.info(config)

    logger.info("Starting prompt server")
    uvicorn.run(app, host=config["host"], port=config["port"])
