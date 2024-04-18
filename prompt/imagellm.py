import json
from typing import Any, List, Mapping, Optional

import requests
from langchain import HuggingFaceHub
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from loguru import logger as loguru_logger

from config import prompt_config as config


class ImageExtractorLLM(LLM):
    # max_token: int
    URL: str = config["image_extractor_url"]
    headers: dict = {"Content-Type": "application/json"}
    payload: dict = {"prompt": "", "image": "", "is_history": False}
    llm_name: str = config["image_extractor_llm_name"]
    logger: Any

    @property
    def _llm_type(self) -> str:
        return "ImageExtractorLLM"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        history: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        # prompt 是问题和图片路径的拼接
        prompt, image = prompt.split("Image:")
        self.payload["prompt"] = prompt
        self.payload["image"] = image
        response = requests.post(
            self.URL, headers=self.headers, data=json.dumps(self.payload)
        )

        if response.status_code == 200:
            result = response.json()
            print(result)
            return result["response"]
        else:
            self.logger.error(
                "ImageExtractorLLM error occurred with status code:", response.text
            )
        return response.text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "URL": self.URL,
            "llm_name": self.llm_name,
            "headers": self.headers,
            "payload": self.payload,
        }
