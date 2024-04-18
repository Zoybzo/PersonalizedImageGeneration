import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from config import server_config as config

app = FastAPI()


class ListQuery(BaseModel):
    api_key: str  # 是否为多轮对话
    id_list: list
    prompt: str


class IDQuery(BaseModel):
    api_key: str  # 是否为多轮对话
    user_id: str
    prompt: str


def _generate_image_list(query):
    pass


def _generate_image_id(query):
    pass


@app.post("/generateByList")
async def generate_image_list(query: ListQuery):
    response = _generate_image_list(query)
    ret = {"response": response}
    return ret


@app.post("/generateByID")
async def generate_image_id(query: IDQuery):
    response = _generate_image_id(query)
    ret = {"response": response}
    return ret


if __name__ == "__main__":
    logger.info("Server Config: ")
    logger.info(config)

    logger.info("Starting server")
    uvicorn.run(app, host=config["host"], port=config["port"])
