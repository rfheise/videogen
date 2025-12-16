from .LLMStoryGen import LLMStoryGen
from ...Helper import Logger 
from openai import OpenAI
import json 

class ChatGPTStoryGen(LLMStoryGen):

    def __init__(self, story_prompt, model = "gpt-4o-mini"):
        super().__init__(story_prompt)
        self.client = OpenAI()
        self.model = model
        self.output_format = {
        "format": {
            "type": "json_schema",
            "name": "storyline",
            "schema": {
                "type": "object",
                "properties": {
                    "story": {
                        "type": "string"
                    }
                },
                "required": ["story"],
                "additionalProperties": False
            }
        }
        }

    def prompt_llm(self, sys_prompt, story_prompt):
        model_input = self.get_model_input(sys_prompt, story_prompt)
        ret = self.call_api(model_input)
        Logger.debug(ret["story"])
        return [ret["story"]]
    
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
    
    def call_api(self, model_input):
        
        Logger.log("Calling ChatGPT To Generate The Story!")

        response = self.client.responses.create(
            model=self.model,
            input=model_input,
            text=self.output_format
            
        )

        return json.loads(response.output_text)

    
if __name__ == "__main__":

    story_gen = ChatGPTStoryGen("Marcus Aurelius Teaching Commodus How To Ride A Horse")
    story = story_gen.generate_story()
    print(str(story))