import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from gpt import ChatGPT
from config import server_config as config

app = FastAPI()

T2I_model = None
brain_model = None


class ListQuery(BaseModel):
    api_key: str  # 是否为多轮对话
    id_list: list
    prompt: str


class IDQuery(BaseModel):
    api_key: str  # 是否为多轮对话
    user_id: str
    prompt: str


def _generate_image_list(query):
    # todo: parse the query and get the item_seq
    item_seq = query.id_list

    #todo: get the models if exists   new models if not
    if T2I_model is None:
        T2I_model = _get_T2I_model()
    if brain_model is None:
        brain_model = _get_brain_model()

    prompt = brain_model.get_user_profile(item_seq)
    res_img = pipe(prompt=prompt, num_inference_steps=50, guidance_scale=3).images[0]
    return res_img


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



#todo: prepare the T2I model
def _get_T2I_model():
    pipe = DiffusionPipeline.from_pretrained(
        config["T2I_model_path"],
        torch_dtype=torch.float16,
        variant="fp16",
    ).to("cuda")
    return pipe

def _get_brain_model():
    brain = Beauty(config["beauty_raw_path"], config["beauty_item_tree_path"], config["api_key"], None, ChatGPT())
    return brain



if __name__ == "__main__":
    logger.info("Server Config: ")
    logger.info(config)
    logger.info("Starting server")
    T2I_model = _get_T2I_model()
    brain_model = _get_brain_model()
    uvicorn.run(app, host=config["host"], port=config["port"])
