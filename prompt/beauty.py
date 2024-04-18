"""
通过beauty类实现根据商品ID获取商品描述，然后把商品ID序列拼接成用户描述
"""

import os
import json

from loguru import logger as loguru_logger

from gpt import ChatGPT
from data.amazon import get_data_from_id, load_json_to_tree
from prompt.create_prompt import (
    create_template_chain,
    beauty_item_template,
    descript_single_beauty,
    user_profiler_templete,
    descript_user_profile,
)
from config import prompt_config as config


class Beauty:
    def __init__(self, meta_json, tree_json, api_key, image_llm, brain_llm=None):
        """
        init

        Args:
            meta_json: str, path to the meta data json file
            tree_json: str, path to the tree json file
            api_key: str, api key for the models
            image_llm: ImageExtractorLLM, image model
            brain_llm: ChatGPT, brain model
        """
        with open(meta_json, "r") as f:
            self.meta_data = json.load(f)
        self.tree_path = tree_json
        self.attribute_list = self.get_attr_list()
        self.api_key = api_key
        self.image_llm = image_llm
        self.brain_llm = brain_llm

    def get_attr_list(self):
        attribute_list = []
        tree = load_json_to_tree(self.tree_path)
        for node in tree.children("Beauty"):
            attribute_list.append(node.tag)

        return attribute_list

    def get_data_from_id(self, id):
        meta_data, item_image = get_data_from_id(id, self.meta_data)
        return meta_data, item_image

    def get_image_description(self, ID):
        _, item_image = self.get_data_from_id(ID)
        father_path = os.path.abspath(os.curdir)
        image_path = os.path.join(father_path, "../amazon", item_image)
        chains = create_template_chain("Beauty", self.attribute_list, self.image_llm)
        result = chains(image_path)
        return result

    def get_beauty_description(self, ID):
        meta_data, _ = self.get_data_from_id(ID)
        # 显卡被占用时，使用Title作为描述
        if self.image_llm is None:
            result = meta_data["title"]
        else:
            result = self.get_image_description(ID)
            item = "Beauty"
            prompt = beauty_item_template(result, meta_data, item)
            result = descript_single_beauty(
                "user", prompt, self.api_key, self.brain_llm
            )
        return result

    def from_idseq_get_history(self, id_seq):
        result = []
        for id in id_seq:
            single_des = self.get_beauty_description(id)
            result.append(single_des)
        return result

    def get_user_profile(self, id_seq):
        history = self.from_idseq_get_history(id_seq)
        item = "Beauty"
        prompt = user_profiler_templete(item, history)
        result = descript_user_profile("user", prompt, self.api_key, self.brain_llm)
        return result


def get_Beauty_instance():
    meta = config["amazon_beauty_raw_path"]
    tree = config["item_tree_path"]
    # llm = ImageExtractorLLM()
    api = ChatGPT()
    bea = Beauty(meta, tree, config["api_key"], None, api)
    return bea


if __name__ == "__main__":
    # Data Path
    meta = config["beauty_raw_path"]
    tree = config["beauty_item_tree_path"]
    # Models
    # llm = ImageExtractorLLM()
    api = ChatGPT()
    bea = Beauty(meta, tree, config["api_key"], None, api)
    # id_seq = ["B00390DN34", "B002T5B4T0", "B000O2TBEK", "B00CZE9YHO"]
    id_seq = ["B00LU0LTOU", "B00LCLFMDG", "B00L8GFJJC", "B00L5YAROY", "B00L4R2RLI"]
    result = bea.get_user_profile(id_seq)
    print(result)
