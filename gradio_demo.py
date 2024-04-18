import gradio as gr
from PIL import Image

test_img = Image.open("test_img.jpg")
def text2image(text):
    return test_img

t2i_demo = gr.Interface(fn=text2image, inputs=gr.Textbox(), outputs=gr.Image())
t2i_demo.launch()

