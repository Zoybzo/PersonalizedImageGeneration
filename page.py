import os
import gradio as gr
from Retrival.Retrival_Tooler import IRTR_Tooler
from Caption.Captioner import Captioner


ret_api = IRTR_Tooler(dataset_dir="F:/Tonggan/database/coco/coco_image.json")
cap_api = Captioner()

def retrival_image_from_text(text):
    result = ret_api.image_retrival(text, None)
    return result

def retrival_image_from_image(image):
    result = ret_api.image_retrival(None, image)
    return result

def caption(image):
    caption_text = cap_api.caption(image)

    return caption_text




with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        #                  太一.通感
        The-One项目的多模态下游展示，欢迎体验，有项目表现不佳的例子，请联系我：2716635239（QQ） 、 zym18840630920(微信)
        """
    )
    with gr.Tab("检索图片"):
        with gr.Row():
            with gr.Column(scale=2):
                retrival_text_Tagi = gr.Textbox(placeholder="输入你想看到的图片描述")
                with gr.Row():
                    gr.ClearButton([retrival_text_Tagi])
                    t2i_button = gr.Button(value="检索")
                retrival_image_Tagi = gr.Image(type="filepath")
                i2i_button = gr.Button(value="检索")
            with gr.Column(scale=3):
                gallery = gr.Gallery(
                    label="Generated images", show_label=False, elem_id="gallery"
                    , columns=[3], rows=[2], object_fit="contain", height=600)
    with gr.Tab("图片字幕"):
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Column(scale=2):
                    caption_image_Tagt = gr.Image(type="filepath")
                    caption_button = gr.Button(value="生成图片解释")
            with gr.Column(scale=3):
                caption_text = gr.Textbox(lines=5)

    gr.Examples([
        ["A girl in red short and a white T-shirt underground looking out of a hole"],
        ["A man on the phone surrounded by stacks of books"],
        ["Two dogs run through the water with a rope in their mouths"],
    ], inputs=retrival_text_Tagi)
    gr.Examples([
        ["F:/Tonggan/Text-Image/test_data/Images/11220707.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/110595925.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/111737806.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/114052371.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/1022454332.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/1073444492.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/1129704496.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/1165334998.jpg"],
        ["F:/Tonggan/Text-Image/test_data/Images/1246239396.jpg"],
    ], inputs=caption_image_Tagt)

    t2i_button.click(fn=retrival_image_from_text, inputs=retrival_text_Tagi, outputs=gallery)
    i2i_button.click(fn=retrival_image_from_image, inputs=retrival_image_Tagi, outputs=gallery)
    caption_button.click(fn=caption, inputs=caption_image_Tagt, outputs=caption_text)

if __name__ == '__main__':
    demo.launch(share=True)