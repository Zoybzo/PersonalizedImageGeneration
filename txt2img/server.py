import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from txt2img.image_generator import ImageGenerator
from config import txt2img_config as config


app = FastAPI()


class Query(BaseModel):  # 定义请求参数, 用于接收前端传来的参数
    prompt: str


def _generate_image(query):
    # Parameters
    prompt = query.prompt
    # Models
    image_generator = ImageGenerator(config)
    # Get results
    image_path, image_name, image = image_generator.generate(prompt)
    return image_path, image_name, image


@app.post("/generate_image")
async def generate_image(query: Query):
    response = _generate_image(query)
    ret = {"response": response}
    return ret


if __name__ == "__main__":
    logger.info("Image Server Config: ")
    logger.info(config)

    logger.info("Starting image server")
    uvicorn.run(app, host=config["host"], port=config["port"])
