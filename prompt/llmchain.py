import json
from typing import Any

from langchain.prompts import ChatPromptTemplate, StringPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory

from prompt.template import BeautyDescriptionTemplate, ProfileTemplate


def descript_single_beauty(role, prompt, api_key, llm):
    prompt = ChatPromptTemplate.from_template(prompt + " quest:{quest}")
    quest = {"role": role, "api_key": api_key}
    quest = json.dumps(quest)
    output_key = "beauty_description"
    chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
    result = chain.run(quest)
    return result


def descript_user_profile(role, prompt, api_key, llm):
    prompt = ChatPromptTemplate.from_template(prompt + " quest:{quest}")
    quest = {"role": role, "api_key": api_key}
    quest = json.dumps(quest)
    output_key = "user_profile"
    chain = LLMChain(llm=llm, prompt=prompt, output_key=output_key)
    result = chain.run(quest)
    return result


def save_memory():
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    memory.save_context(
        {"input": " Please describe the car_shape of car in detail"},
        {
            "output": "The car in the image is a black Porsche 911 Carrera 4S, which is a two-door, four-seat sports car. It has a sleek and aerodynamic design, with a long hood and a low, wide stance. The car is driving down a city street, showcasing its sporty and aggressive appearance.\n"
        },
    )
    return memory
