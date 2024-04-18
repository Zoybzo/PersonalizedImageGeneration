import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from gpt import ChatGPT
from txt2img.image_generator import ImageGenerator
from prompt.beauty import Beauty
from config import server_config as config

app = FastAPI()

TYPE_ID = "id"
TYPE_LIST = "seq"


class ListQuery(BaseModel):
    # api_key: str  # 是否为多轮对话
    id_list: list
    prompt: str


class IDQuery(BaseModel):
    # api_key: str  # 是否为多轮对话
    user_id: str
    prompt: str


class Query(BaseModel):
    type: str
    user_info: str
    prompt: str


def _generate_image_by_list(id_list, prompt):
    global brain_model, image_model

    if brain_model is None:
        brain_model = _get_brain_model()
    if image_model is None:
        image_model = _get_image_model()

    # Generate prompt
    prompt = brain_model.get_user_profile(id_list)
    # Generate image
    _, _, res_img = image_model.generate(prompt)
    return res_img


def _generate_image_by_id(user_id, prompt):
    pass


def _get_brain_model():
    brain = Beauty(
        config["beauty_raw_path"],
        config["beauty_item_tree_path"],
        config["api_key"],
        None,
        ChatGPT(),
    )
    return brain


def _get_image_model():
    return ImageGenerator(config)


def _generate_image(query):
    gen_type = query.gen_type
    user_info = query.user_info
    prompt = query.prompt

    response = None
    if gen_type is TYPE_ID:
        response = _generate_image_by_id(user_info, prompt)
    elif gen_type is TYPE_LIST:
        response = _generate_image_by_list(user_info, prompt)
    else:
        response = "Invalid type"
    return {"response": response}


@app.post("/generateByList")
async def generate_image_list(query: ListQuery):
    id_list = query.id_list
    prompt = query.prompt
    response = _generate_image_by_list(id_list, prompt)
    ret = {"response": response}
    return ret


@app.post("/generateByID")
async def generate_image_id(query: IDQuery):
    user_id = query.user_id
    prompt = query.prompt
    response = _generate_image_by_id(user_id, prompt)
    ret = {"response": response}
    return ret


@app.post("/generate")
async def generate_image(query: Query):
    response = _generate_image(query)
    ret = {"response": response}
    return ret


if __name__ == "__main__":
    logger.info("Server Config: ")
    logger.info(config)
    logger.info("Loading models")
    global image_model, brain_model
    brain_model = _get_brain_model()
    image_model = ImageGenerator(config)
    logger.info("Starting server")
    uvicorn.run(app, host=config["host"], port=config["port"])
