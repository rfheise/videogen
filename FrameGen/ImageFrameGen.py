from .FrameGen import FrameGen
from ..StoryGen import FileStoryGen
from ..Narrator import KokoruNarrator
from ..Utilities import Logger
import os 
from .Frame import FrameList,FrameImageCacheItem

class ImageFrameGen():

    def __init__(self, story, audio_clips, fps=30, min_img_duration=5):
        self.story = story 
        self.audio_clips = audio_clips 
        self.fps = fps
        self.min_img_duration = min_img_duration
    
    def generate_frames(self):
        Logger.log("Generating Images")
        
        self.merge_story()
        self.convert_timestamps_to_frames()
        images = self.call_image_gen()
        frames = self.images_to_frames(images)
        Logger.log("Finished Generating\n")

        return frames
    
    def images_to_frames(self, images):
        frames = FrameList(10, FrameImageCacheItem)
        for i,phrase in enumerate(self.story.phrases):
            image = images[i]
            total = phrase.end - phrase.start + 1
            if not os.path.exists(image):
                print(image)
            for _ in range(total):
                
                frames.add_item(image)
        return frames

    def call_image_gen(self):
        #to be implemented by inherited class
        pass 

    def merge_story(self):
        # make sure each phrase is at least <min_img_duration> seconds 
        
        curr_phrase = None
        phrases = []
        curr = 0
        for phrase in self.story.phrases:

            if curr >= self.min_img_duration:
                phrases.append(curr_phrase)
                curr_phrase = None

            if curr_phrase is None:
                curr_phrase = phrase 
                curr = curr_phrase.total
                continue 

            curr_phrase.s += phrase.s 
            curr += phrase.total 
            curr_phrase.end = phrase.end
        if curr_phrase:
            phrases.append(curr_phrase)
        self.story.phrases = phrases
    
    def convert_timestamps_to_frames(self):

        start = 0
        for phrase in self.story.phrases:
            end = round(phrase.end*self.fps)
            phrase.start = start 
            phrase.end = end 
            start = end + 1


                
            

if __name__ == "__main__":
    prompt = "Marcus Aurelius teaching Commodus how to ride a horse"
    # story = ChatGPTStoryGen(prompt).generate_story()
    story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    story = FileStoryGen(story_path).generate_story()
    n = KokoruNarrator(story)
    story, audio_list = n.generate_audio()
    out_file = os.path.join(KokoruNarrator.get_folder(),"out.wav")
    audio_list.merge_clips(out_file)
    frame_gen = ImageFrameGen(story, audio_list)
    frame_gen.generate_frames()
