from ..Utilities import Logger

class FrameGen():

    def __init__(self, story, audio_clips, fps=30):
        self.story = story 
        self.audio_clips = audio_clips 
        self.fps = fps
    
    def generate_frames(self):
        # to be implemented by inherited class
        pass

    