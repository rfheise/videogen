import os
from .Logger import Logger
from openai import OpenAI
import json 

class LLMQuery():
    def __init__(self, system_prompt_file = "", user_prompt="", log_message = ""):
        self._system_prompt = system_prompt_file
        self._user_prompt = user_prompt
        self.log_message = log_message
    
    @property
    def sys_prompt(self):
        with open(self._system_prompt, "r") as f:
            return f.read() 
    
    @property
    def user_prompt(self):
        return self._user_prompt
    
    def query_api(self):
        # to be implemented by inherited class
        raise Exception("Query Function Not Implemented")

class ChatGPTQuery(LLMQuery):
    def __init__(self, system_prompt_file = "", user_prompt="", log_message = "", model="gpt-5-mini"):
        super().__init__(system_prompt_file, user_prompt, log_message)
        self.client = OpenAI()
        self.model = model
        self._system_prompt = system_prompt_file
        self._user_prompt = user_prompt
        self.log_message = log_message
    
    @property
    def output_format(self):
        # to be implemented by inherited class
        raise Exception("Output Format Not Implemented")

    def get_model_input(self):
        model_input = [
            {
            "role": "system",
            "content": [
                {
                "type": "input_text",
                "text": self.sys_prompt
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": self.user_prompt
                }
            ]
            },

        ]
        return model_input
    
    def query_api(self):
        model_input = self.get_model_input()
        if self.log_message is not None and len(self.log_message) != 0:
            Logger.log(self.log_message)
        response = self.client.responses.create(
            model=self.model,
            input=model_input,
            text=self.output_format
            
        )
        return json.loads(response.output_text)


