import os
from ...Helper import Logger 

class LLMSDPrompt():

    def __init__(self, story, style=None):
        self.story = story.copy()
        self.style = style
    
    @property
    def sys_prompt(self):
        dirname = os.path.dirname(__file__)
        sys_prompt_fname = os.path.join(dirname, "llm_data", 'llm_sd_sys_prompt.txt')
        with open(sys_prompt_fname, "r") as f:
            text = f.read()

        if self.style is not None:
            text += f"\n Generate the prompts with the following style: {self.style()}"
        return text 
    
    def generate_user_prompt(self):
        text = ""
        for i,phrase in enumerate(self.story.phrases):
            t = phrase.s.replace("\n","")
            text += f"{i}:{t}\n"
        return text

    def get_prompts(self):

        user_prompt = self.generate_user_prompt()
        prompts = self.query_api(self.sys_prompt, user_prompt)
        if len(prompts) < len(self.story.phrases):
            Logger.err("Prompt Lengths Don't Match")
            exit(1)

        # print(prompts)

        for i,phrase in enumerate(self.story.phrases):
            phrase.s = prompts[i]
        
        return self.story

    def query_api(self, sys_prompt, user_prompt):
        #TODO: implement by inherited class
        # returns string list of new prompts
        return []


        
        
        
    
