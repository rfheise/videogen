from ...Utilities import ChatGPTQuery
from ...StoryGen import FileStoryGen
from ...Narrator import KokoruNarrator
import os 

class ChatGPTCanon(ChatGPTQuery):

    def __init__(self, story):
        system_prompt_file = os.path.join(os.path.dirname(__file__),"llm_data","llm_canon_prompt.txt")
        super().__init__(log_message = "Generating Canon", system_prompt_file=system_prompt_file)
        self.story = story
    
    @property
    def user_prompt(self):
        text = ""
        for phrase in self.story.phrases:
            text += phrase.s + "\n"
        return text

    @property 
    def output_format(self):
        return {
            "format": {
                "type": "json_schema",
                "name": "cannon",
                "schema": {
                    "type": "object",
                    "properties": {
                        "style": {
                            "type": "string",
                            "description": "detailed global stable diffusion style"
                        },
                        "negative_prompt": {
                            "type":"string",
                            "description": "global negative prompt"
                        },
                        "characters": {
                            "type":"array",
                            "items": {
                                "type":"object",
                                "properties": {
                                    "name": {
                                        "type":"string",
                                        "description": "the name of the character"
                                    },
                                    "description": {
                                        "type":"string",
                                        "description":"detailed description of what the character looks like"
                                    }
                                },
                                "required":["name", "description"],
                                "additionalProperties":False
                            }   
                        },
                        "locations": {
                            "type":"array",
                            "items": {
                                "type":"object",
                                "properties": {
                                    "name": {
                                        "type":"string",
                                        "description": "the name of the location"
                                    },
                                    "description": {
                                        "type":"string",
                                        "description":"detailed description of what the location looks like"
                                    }
                                },
                                "required":["name", "description"],
                                "additionalProperties":False
                            }
                        }
                    },
                    "required": ["style", "negative_prompt","characters", "locations"],
                    "additionalProperties": False
                }
            }
        }
    

if __name__ == "__main__":

    prompt = "Marcus Aurelius teaching Commodus how to ride a horse"
    # story = ChatGPTStoryGen(prompt).generate_story()
    story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    story = FileStoryGen(story_path).generate_story()
    canon_gen = ChatGPTCanon(story)
    res = canon_gen.query_api()
    print(res)

    
