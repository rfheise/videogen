from ..Helper import Logger

class StoryGen():

    def __init__(self, story_prompt):

        self.story_prompt = story_prompt
    
    def generate_story(self):

        Logger.log("Generating the Storyline")

        texts = self.generate_story_text()
        story = Story()
        story.create_story(texts)

        Logger.log("Finished Generating The Story\n")

        return story
        

    def generate_story_text(self):
        #generates the story text
        #should return a list of strings
        pass

class Phrase():
    ID = -1
    def __init__(self,s):
        Phrase.ID += 1
        self.id = Phrase.ID
        self.s = s
    
    def get_phrase(self):
        return self.s 
    
    def __str__(self):
        return self.s

class TimePhrase(Phrase):

    def __init__(self, s, start=None, end=None):
        super().__init__(s)
        self.start = start 
        self.end = end 
    
    def setTimeStamp(self, start, end):
        self.start = start 
        self.end = end 
    
class Story():

    def __init__(self, phrase=Phrase):
        self.phrases = []
        self.phrase_class = phrase
    
    def create_story(self, texts):
        
        for t in texts:
            self.phrases.append(self.phrase_class(t))
    
    def add_phrase(self, s):
        self.phrases.append(self.phrase_class(t))
    
    def __str__(self):
        s = ""
        for p in self.phrases:
            s += str(p) + "\n"
        return s

    def copy(self, phrase_class=None):

        if phrase_class is None:
            phrase_class = self.phrase_class 
        other = Story(phrase_class)
        for i,p in enumerate(self.phrases):
            other.add_phrase(p.s)
            other.phrases[i].id = p.id
        return other





