import gradio as gr
from PIL import Image
import requests

base_url = "http://127.0.0.1:8001/text2image/"


def text2image(image_prompt, type, user_info):
    if type == "id":
        url = base_url + "generateByID"
        params = {
            "api_key": "123",
            "user_id": "123",
            "prompt": image_prompt
        }
        response = requests.post(url, data=params)
    else:
        url = base_url + "generateByList"
        params = {
            "api_key": "123",
            "id_list": ["123", "123"],
            "prompt": image_prompt
        }
        response = requests.post(url, data=params)
    return Image.open(response["response"])


t2i_demo = gr.Interface(
    fn=text2image,
    inputs=[
        gr.Textbox(placeholder="Enter prompt for image generation", label="Image Prompt"),
        # gr.Textbox(placeholder="Enter navigator prompt", label="Negative Prompt"),
        gr.Dropdown(choices=["id", "seq"], label="Choose the type of content"),
        gr.Textbox(placeholder="Enter user info", label="User Info Input")
    ],
    outputs=gr.Image()
)
t2i_demo.launch()
