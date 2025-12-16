import os
from ..StoryGen import StoryGen

class LLMStoryGen(StoryGen):

    def __init__(self, story_prompt):
        super().__init__(story_prompt)
    
    def load_sys_prompt(self):
        sys_prompt_dir = os.path.dirname(__file__)
        sys_prompt_fname = os.path.join(sys_prompt_dir, "llm_data","llm_sys_prompt.txt")
        with open(sys_prompt_fname, "r") as f:
            return f.read()

    def generate_story_text(self):
        #generates the story text
        #should return a list of strings
        sys_prompt = self.load_sys_prompt()
        return self.prompt_llm(sys_prompt, self.story_prompt)

    def prompt_llm(self, sys_prompt, story_prompt):

        pass 
        # to be completed by the inherited class
