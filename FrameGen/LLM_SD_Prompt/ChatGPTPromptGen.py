from ...Utilities import ChatGPTQuery
import os
from ...Utilities import Logger 
from openai import OpenAI
from ...StoryGen import FileStoryGen
from ...Narrator import KokoruNarrator
from .ChatGPTCanon import ChatGPTCanon
import json 

class ChatGPTPromptGen(ChatGPTQuery):

    def __init__(self, story, canon, style=None):
        system_prompt_file = os.path.join(os.path.dirname(__file__), "llm_data", 'llm_sd_sys_prompt.txt')
        log_msg = "Calling ChatGPT To Generate The Stable Diffusion Prompts"
        super().__init__(system_prompt_file=system_prompt_file, log_message=log_msg, model='gpt-5-mini') 
        self.style = style
        self.canon = canon
        self.story = story
    
    @property
    def sys_prompt(self):
        text = super().sys_prompt
        # if self.style is not None:
        #     text += f"\n Generate the prompts with the following style: {self.style()}"
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
                                    "characters": {
                                        "type":"array",
                                        "items": {
                                            "type":"string",
                                            "description":"character name tag"
                                        },
                                        "description": "list of characters that appear in the story segment"
                                    },
                                    "location": {
                                        "type": "string",
                                        "description": "location name tag"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "detailed physical description of what is happening in the story segment"
                                    }
                                },
                                "required":["characters","location","description"],
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
    
    def format_story(self):
        text = ""
        for i,phrase in enumerate(self.story.phrases):
            t = phrase.s.replace("\n","")
            text += f"{i}:{t}\n"
        return text
    
    def format_canon(self):
        text = ""
        # text = "Style\n"
        # text += self.canon['style'] + "\n"
        if self.style:
            text += "Style\n"
            text += self.style['positive'] + '\n'
        text += "\nCharacters\n"
        for character in self.canon['characters']:
            text += f"{character['name']}: {character['description']}\n"
        text += "\nLocations\n"
        for location in self.canon['locations']:
            text += f"{location['name']}: {location['description']}\n"
        return text

    @property
    def user_prompt(self):
        text = "---CANON---\n"
        text += self.format_canon()
        text += "\n\n---STORY---\n"
        text += self.format_story()
        return text
    def clean_str(self, s):
        return s.lower().replace(" ", "")
    def generate_prompts(self):
        res = self.query_api()
        # with open(os.path.join(os.path.dirname(__file__), "llm_data","tmp_prompt.json")) as f:
            # res = json.loads(f.read())
        print(json.dumps(res))
        prompt_data = res['prompts']
        return [self.generate_prompt(p) for p in prompt_data]
    
    def clean_to_proper(self, s):
        s = s.split("_")
        t = ""
        for i,n in enumerate(s):
            if len(n) >= 2:
                t += n[0].upper()
                t += n[1:]
            else:
                t += n
            if i != len(s) - 1:
                t += " "
        return t

    def generate_prompt(self, prompt):

        text = ""
        self.characters = {self.clean_str(c['name']):c['description'] for c in self.canon['characters']}
        self.locations = {self.clean_str(l['name']):l['description'] for l in self.canon['locations']}
        if self.style is not None:
            text += self.style['positive'] + '\n'
        if len(prompt['characters']) > 0:
            for character in prompt['characters']:
                character = self.clean_str(character)
                text += f"{self.clean_to_proper(character)} {self.characters[character]}\n"
        text += "\n"
        location_name = self.clean_str(prompt['location'])
        text += self.locations[location_name] + '\n'
        text += "\n" + prompt['description']
        return text
        
        
if __name__ == "__main__":

    prompt = "Marcus Aurelius teaching Commodus how to ride a horse"
    # story = ChatGPTStoryGen(prompt).generate_story()
    story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    story = FileStoryGen(story_path).generate_story()
    n = KokoruNarrator(story)
    story, audio_list = n.generate_audio()
    out_file = os.path.join(KokoruNarrator.get_folder(),"out.wav")
    # canon_gen = ChatGPTCanon(story)
    # canon = canon_gen.query_api()
    fp = os.path.join(os.path.dirname(__file__),"llm_data","tmp_canon.json")
    with open(fp, "r") as f:
        text = f.read()
    canon = json.loads(text)
    prompt_gen = ChatGPTPromptGen(story, canon)
    res = prompt_gen.generate_prompts()
    for r in res:
        print(r + '\n')