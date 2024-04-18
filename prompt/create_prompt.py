"""
This module contains functions to create prompt templates for different tasks.
"""

import json
from typing import Any

from langchain.prompts import ChatPromptTemplate, StringPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from prompt.template import BeautyDescriptionTemplate, ProfileTemplate


def create_template_chain(item, item_attribute_list, llm):
    """
    Create a prompt template for beauty item task.
    """
    chain_list = []
    output_keys = []
    prompt = ChatPromptTemplate.from_template(
        "Whether there is text about "
        + item
        + " in the image, and if so, extract it. Image:{Image}"
    )
    print(prompt)
    output_key = "image_text"
    chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
    chain_list.append(chain)
    output_keys.append(output_key)
    for att in item_attribute_list:
        prompt = ChatPromptTemplate.from_template(
            "Please describe the "
            + att
            + " of "
            + item
            + " in detail"
            + " Image:{Image}"
        )
        print(prompt)
        output_key = att + "_result"
        chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
        chain_list.append(chain)
        output_keys.append(output_key)
    overall_chain = SequentialChain(
        chains=chain_list,
        input_variables=["Image"],
        output_variables=output_keys,
        verbose=True,
    )
    return overall_chain


def user_profile_templete(item, history):
    """
    Create a prompt template for user profile task.
    """
    promt_template = ProfileTemplate(input_variables=["item", "history"])
    prompt = promt_template.format(item=item, history=history)
    return prompt


def beauty_item_template(result, dataset, item):
    """
    Create a prompt template for beauty item task.
    """
    promt_template = BeautyDescriptionTemplate(
        input_variables=["item", "conversation", "dataset"]
    )
    prompt = promt_template.format(item=item, dataset=dataset, conversation=result)
    return prompt
