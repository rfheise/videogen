from ...Utilities import ChatGPTQuery
import os
from ...Utilities import Logger 
from openai import OpenAI
import json 

class ChatGPTPromptGen(ChatGPTQuery):

    def __init__(self, story, style=None):
        system_prompt_file = os.path.join(os.path.dirname(__file__), "llm_data", 'llm_sd_sys_prompt.txt')
        log_msg = "Calling ChatGPT To Generate The Stable Diffusion Prompts"
        super().__init__(system_prompt_file=system_prompt_file, log_message=log_msg) 
        self.style = style
        self.story = story
    
    @property
    def sys_prompt(self):
        text = super().sys_prompt
        if self.style is not None:
            text += f"\n Generate the prompts with the following style: {self.style()}"
        return text 
    
    @property
    def output_format(self):
        return {
            "format": {
                "type": "json_schema",
                "name": "storyline",
                "schema": {
                    "type": "object",
                    "properties": {
                        "prompts": {
                            "type": "array",
                            "items": {
                                "type":"object",
                                "properties": {
                                    "positive_prompt":{
                                        "type":"string",
                                        "description":"detailed positive prompt for stable diffusion"
                                    },
                                    "negative_prompt":{
                                        "type":"string",
                                        "description":"negative prompt for stable diffusion"
                                    }
                                },
                                "required":["positive_prompt","negative_prompt"],
                                "additionalProperties":False
                            },
                            "minItems":len(self.story.phrases)
                        }
                    },
                    "required": ["prompts"],
                    "additionalProperties": False
                }
            }
        }
    
    @property
    def user_prompt(self):
        text = ""
        for i,phrase in enumerate(self.story.phrases):
            t = phrase.s.replace("\n","")
            text += f"{i}:{t}\n"
        return text
        
