from .StoryGen import StoryGen
from ..Helper import Logger

class FileStoryGen(StoryGen):

    def __init__(self, fname):

        super().__init__(fname)
        

    def generate_story_text(self):
        Logger.log(f"Reading The Story From File: {self.story_prompt}")
        with open(self.story_prompt, "r") as f:
            return [f.read()]