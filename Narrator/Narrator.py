from ..StoryGen import Story, TimePhrase, Phrase
import re
from ..Helper import Logger

class Narrator():

    def __init__(self, story):
        self.story = story
    
    def generate_audio(self):
        Logger.log("Generating Audio")
        self.story = self.split_story()
        audio_clips = self.call_audio_generator(self.story)
        Logger.log("Finished Generating The Audio\n")
        return self.story, audio_clips

    def call_audio_generator(self, story):
        #to be completed by inherited class
        return None
    
    def split_story(self):

        story = Story(TimePhrase)

        text = ""
        for t in self.story.phrases:
            text += t.s 
        
        text = re.split(r'(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bDr)(?<!\bSr)(?<!\bJr)(?<!\bvs)(?<!\betc)(?<!\be\.g)(?<!\bi\.e)(?<=[.!?])\s+', text)

        story.create_story(text)

        return story