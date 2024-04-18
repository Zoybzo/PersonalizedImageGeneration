import os
import time

from diffusers import DiffusionPipeline
import torch
from PIL import Image

from loguru import logger


class ImageGenerator:
    def __init__(self, config):
        self.model_path = config["model_path"]
        self.pipe = DiffusionPipeline.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16,
            variant="fp16",
        ).to("cuda")
        self.save_path = config["save_path"]

    def generate(
        self, prompt, saved_path=None, num_inference_steps=50, guidance_scale=3
    ):
        image = self.pipe(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        ).images[0]
        if saved_path is None:
            saved_path = self.save_path
        # Generate the unique image name by the time
        image_name = f"image_{str(time.time())}.png"
        image_path = os.path.join(saved_path, image_name)
        image.save(image_path)
        # Show the image
        image.show()
        logger.info(f"Image saved at {image_path}")
        return image_path, image_name, image
