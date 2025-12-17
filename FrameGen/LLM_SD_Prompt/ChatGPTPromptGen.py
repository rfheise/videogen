from .LLMPrompt import LLMSDPrompt
import os
from ...Helper import Logger 
from openai import OpenAI
import json 

class ChatGPTPromptGen(LLMSDPrompt):
    def __init__(self, story, style=None, model="gpt-5-mini"):
        self.story = story.copy()
        self.style = style
        self.client = OpenAI()
        self.model = model
        self.output_format = {
        "format": {
            "type": "json_schema",
            "name": "storyline",
            "schema": {
                "type": "object",
                "properties": {
                    "prompts": {
                        "type": "array",
                        "items": {
                            "type":"string"
                        },
                        "minItems":len(self.story.phrases)
                    }
                },
                "required": ["prompts"],
                "additionalProperties": False
            }
        }
        }

    def get_model_input(self, sys_prompt, story_prompt):
        model_input = [
            {
            "role": "system",
            "content": [
                {
                "type": "input_text",
                "text": sys_prompt
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": story_prompt
                }
            ]
            },

        ]
        return model_input
    
    def query_api(self, sys_prompt, user_prompt):
        model_input = self.get_model_input(sys_prompt, user_prompt)
        Logger.log("Calling ChatGPT To Generate The Stable Diffusion Prompts")
        response = self.client.responses.create(
            model=self.model,
            input=model_input,
            text=self.output_format
            
        )
        return json.loads(response.output_text)['prompts']

