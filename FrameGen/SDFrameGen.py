from .ImageFrameGen import ImageFrameGen
from .FrameGen import FrameGen
from ..StoryGen import FileStoryGen
from ..Narrator import KokoruNarrator
from ..Helper import Logger
import os 
from .Frame import FrameList, FrameImageCacheItem
import torch
from diffusers import DiffusionPipeline

class SDFrameGen(ImageFrameGen):

    @staticmethod
    def get_cwd():
        return os.path.join(os.path.dirname(__file__),"tmp")
    
    def call_image_gen(self):
        self.generate_image("cartoon dog running in a park", os.path.join(self.get_cwd(),"out.jpg"))
        return None
        images = []
        for phrase in self.story.phrases:
            out_file = os.path.join(self.get_cwd(), f"{phrase.id}.jpg")
            self.generate_image(phrase, out_file)
            images.append(out_file)
        return images
        
    def generate_image(self, phrase, out_file):
        model = "stabilityai/stable-diffusion-3.5-medium"
        # model = "Qwen/Qwen-Image"
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        pipe.to("mps")

        image = pipe(
            prompt="A capybara holding a sign that reads Hello World",
        ).images[0]
        image.save(out_file)


        

    

if __name__ == "__main__":
    prompt = "Marcus Aurelius teaching Commodus how to ride a horse"
    # story = ChatGPTStoryGen(prompt).generate_story()
    story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    story = FileStoryGen(story_path).generate_story()
    n = KokoruNarrator(story)
    story, audio_list = n.generate_audio()
    out_file = os.path.join(KokoruNarrator.get_folder(),"out.wav")
    # audio_list.merge_clips(out_file)
    frame_gen = SDFrameGen(story, audio_list)
    frame_gen.generate_frames()