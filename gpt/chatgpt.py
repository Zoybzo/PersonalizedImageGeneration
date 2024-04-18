import json
from typing import Any, List, Mapping, Optional

import requests
from langchain import HuggingFaceHub
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from loguru import logger

from config import gpt_config as config


class ChatGPT(LLM):
    # max_token: int
    URL: str = config["url"]
    headers: dict = {"Content-Type": "application/json"}
    payload: dict = {"role": "", "prompt": "", "api_key": ""}
    llm_name: str = config["name"]
    logger: Any

    @property
    def _llm_type(self) -> str:
        return "ChatGPT"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        history: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        prompt, quest = prompt.split("quest:")
        quest = json.loads(quest)
        self.payload["role"] = quest["role"]
        self.payload["prompt"] = prompt
        self.payload["api_key"] = quest["api_key"]
        response = requests.post(
            self.URL, headers=self.headers, data=json.dumps(self.payload)
        )

        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            self.logger.error("ChatGPT error occurred with status code:", response.text)
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
