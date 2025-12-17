from .ImageFrameGen import ImageFrameGen
from .FrameGen import FrameGen
from ..StoryGen import FileStoryGen,ChatGPTStoryGen
from ..Narrator import KokoruNarrator
from ..Helper import Logger
import os 
from .Frame import FrameList, FrameImageCacheItem
import torch
from diffusers import DiffusionPipeline
from .LLM_SD_Prompt import ChatGPTPromptGen, Styles

class SDFrameGen(ImageFrameGen):

    @staticmethod
    def get_cwd():
        path = os.path.join(os.path.dirname(__file__),"tmp")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path 
    
    def call_image_gen(self):
        prompts = []
        out_files = []
        
        # convert story to prompts 
        prompt_gen = ChatGPTPromptGen(self.story,Styles.cartoon)
        story = prompt_gen.get_prompts()

        for phrase in story.phrases:
            out_file = os.path.join(self.get_cwd(), f"{phrase.id}.jpg")
            out_files.append(out_file)
            prompts.append(phrase.s)
        images = self.generate_image(prompts, out_files)
        # images = out_files
        return images
        
    def generate_image(self, prompts, out_files):
        
        gs = 5
        prompt_list = []
        #do five at at time
        for i in range(len(prompts)//gs + 1):
            start = i * gs
            end = min(i *gs + gs, len(prompts)) 
            if len(prompts[start:end]) == 0:
                continue
            prompt_list.append(prompts[start:end])

        start = 0
        for prompts in prompt_list:
            # pipe = DiffusionPipeline.from_pretrained("Qwen/Qwen-Image",use_safetensors=True)
            pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
            pipe.to("cuda")
            images = pipe(
                prompt=prompts
            ).images
            for i,image in enumerate(images):
                image.save(out_files[start + i])
            start += len(images)

        return out_files


        

    

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
