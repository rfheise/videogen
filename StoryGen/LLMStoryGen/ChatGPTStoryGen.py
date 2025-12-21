import os
from ...Utilities import ChatGPTQuery
from ..StoryGen import StoryGen

class ChatGPTStoryQuery(ChatGPTQuery):

    def __init__(self, story_prompt):
        sys_prompt_file = os.path.join(os.path.dirname(__file__), "llm_data","llm_sys_prompt.txt")
        log_msg = "Calling ChatGPT to generate script"
        super().__init__(system_prompt_file=sys_prompt_file, user_prompt=story_prompt,log_message=log_msg)
    
    @property
    def output_format(self):
        return {
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
    
class ChatGPTStoryGen(StoryGen):

    def generate_story_text(self):
        gpt_query = ChatGPTStoryQuery(self.story_prompt)
        text = gpt_query.query_api()
        return [text['story'].replace("\n","")]
        

if __name__ == "__main__":

    story_gen = ChatGPTStoryGen("Marcus Aurelius Teaching Commodus How To Ride A Horse")
    story = story_gen.generate_story()
    print(str(story))