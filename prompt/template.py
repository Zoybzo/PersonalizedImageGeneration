import json
from typing import Any

from langchain.prompts import ChatPromptTemplate, StringPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory


class ProfileTemplate(StringPromptTemplate):
    def format(self, **kwargs: Any) -> str:
        template = """You need to do two things based on the user's browsing history about the {item}: 
        Firstly, summarize the user's preferences, 
        Secondly, explain the summarized preferences in terms of what they are interested in about the product.

        The user's browsing history:{history}
        
        Here's an example which you can use as a reference:
            User preference: Luxury, high-performance cars with a special focus on red and black vehicles.
            Users' interest in automotive products: Interested in luxury cars with well-known brands and outstanding performance, focusing on the personality and style conveyed by the vehicle's appearance.
        
        Your response:"""
        history = kwargs.pop("history")
        history_template = "\n"
        a = 1
        for his in history:
            b = str(a)
            history_template += "\t\t\t" + b + ". " + his + "\n"
            a = a + 1

        kwargs["history"] = history_template
        return template.format(**kwargs)


class BeautyDescriptionTemplate(StringPromptTemplate):
    def format(self, **kwargs: Any) -> str:
        template = """You need to summarize the {item} in combination with the information which have already provided and the conversation about the image.
        
        Information in the dataset:
        Title: {title}
        Categories : {categories}
        Image: {Image}
        
        A conversation about the image of the item:
        Human: Whether there is text about Beauty in the image, and if so, extract it.
        AI: {image_text}
        Human: Please describe the beauty_color of Beauty in detail.
        AI: {beauty_color}
        Human: Please describe the beauty_type of Beauty in detail
        AI: {beauty_type}
        
        Please combine the above information about the item to give a concise description of this item.
        Requirements: The summary statement cannot exceed 50 words
        Your response:"""
        conversation = kwargs.pop("conversation")
        dataset = kwargs.pop("dataset")

        kwargs["title"] = dataset["title"]
        kwargs["categories"] = dataset["categories"]

        kwargs["Image"] = conversation["Image"]
        kwargs["beauty_color"] = conversation["beauty_color_result"]
        kwargs["image_text"] = conversation["image_text"]
        kwargs["beauty_type"] = conversation["beauty_type_result"]
        return template.format(**kwargs)
