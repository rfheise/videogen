from .ImageFrameGen import ImageFrameGen
from .FrameGen import FrameGen
from ..StoryGen import FileStoryGen,ChatGPTStoryGen
from ..Narrator import KokoruNarrator
from ..Utilities import Logger, read_json
import os 
from .Frame import FrameList, FrameImageCacheItem
import torch
from diffusers import DiffusionPipeline
from .LLM_SD_Prompt import ChatGPTPromptGen, Styles, ChatGPTCanon
from compel import Compel, ReturnedEmbeddingsType
import json 

class SDFrameGen(ImageFrameGen):

    @staticmethod
    def get_cwd():
        path = os.path.join(os.path.dirname(__file__),"tmp")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path 
    
    def generate_prompts(self, style=None):

        canon_gen = ChatGPTCanon(self.story)
        canon = canon_gen.query_api()
        print(json.dumps(canon),"\n\n\n")
        prompt_gen = ChatGPTPromptGen(self.story, canon, style)
        prompts = prompt_gen.generate_prompts()
        # canon = read_json(os.path.join(os.path.dirname(__file__),"LLM_SD_Prompt","llm_data","tmp_canon.json"))
        # prompts = read_json(os.path.join(os.path.dirname(__file__),"LLM_SD_Prompt","llm_data","tmp_prompt.json"))['prompts']
        # prompt_gen = ChatGPTPromptGen(self.story,canon, style)
        # prompts = [prompt_gen.generate_prompt(p) for p in prompts]
        print(len(prompts), len(self.story.phrases),"\n\n\n\n\n\n")
        if len(prompts) < len(self.story.phrases):
            raise Exception("Not Enough Prompts Generated!")
        # exit()
        if style is not None:
            return [{"negative_prompt":style['negative'], "positive_prompt": p, } for p in prompts]
        else:
            return [{"negative_prompt":canon['negative_prompt'], "positive_prompt": p, } for p in prompts]
        
    
    def call_image_gen(self):
        prompts = []
        out_files = []
        
        # convert story to prompts 
        
        prompts = self.generate_prompts(Styles.sticks)
        

        for i,phrase in enumerate(self.story.phrases):
            out_file = os.path.join(self.get_cwd(), f"{phrase.id}.jpg")
            out_files.append(out_file)
            # prompts.append(prompts[i])

        images = self.generate_image(prompts, out_files)
        # images = out_files
        return images
        
    def generate_image(self, prompts, out_files):
        
        gs = 1
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
            pipe_res = self.generate_sd_pipe(prompts,'cuda')
            images = pipe_res
            for i,image in enumerate(images):
                image.save(out_files[start + i])
            start += len(images)

        return out_files

    def generate_sd_pipe(self, prompts, device="mps"):
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        pipe.to(device)
        # for prompt in prompts:
        pos_prompt = [p['positive_prompt'] for p in prompts]
        neg_prompt = [p['negative_prompt'] for p in prompts]
        width = 1344
        height = 768
        print(pos_prompt)
        print(neg_prompt)
        compel = Compel(tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
                text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
                returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
                requires_pooled=[False, True])
        p_conditioning, p_pooled = compel(pos_prompt)
        n_conditioning, n_pooled = compel(neg_prompt)
        ret = pipe(width=width,
            height=height,
            prompt_embeds=p_conditioning,
            pooled_prompt_embeds=p_pooled,
            negative_prompt_embeds=n_conditioning,
            negative_pooled_prompt_embeds=n_pooled,
            num_inference_steps=500)
        return ret.images
        

    
def main():
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

def call_sd():
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
    pipe.to("cuda")
    # for prompt in prompts:
    pos_prompt = """
       playful hand-drawn stick figure doodle style, thick smooth black marker lines, rounded flowing strokes, soft organic curves, circle heads with simple expressive faces, dot eyes and curved smiles, mitten-like hands and rounded feet, exaggerated dynamic poses, motion implied through curved limbs, casual sketch aesthetic, minimalist cartoon line art, pure white background, no color, no shading, no texture,

group of stick figures traveling north together, some pulling small sleds, others carrying sacks over shoulders, exaggerated walking poses showing effort and motion, one stick figure slightly ahead pointing forward, another lagging behind looking tired, simple cracked lines beneath feet suggesting icy ground, minimal horizon line only

    """
    neg_prompt = "realistic anatomy, thin lines, stiff straight limbs, detailed cartoon characters, color, shading, gradients, textures, background detail, perspective depth, realism, 3D, vector art"
    
    # pos_prompt = "Colorful Roaring Lion sitting on a victorian couch, flat icon, vector"
    # neg_prompt = "realistic, realism, photograph"
    
    width = 1344
    height = 768
    print(pos_prompt)
    print(neg_prompt)
    compel = Compel(tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
            text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
            returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
            requires_pooled=[False, True])
    p_conditioning, p_pooled = compel(pos_prompt)
    n_conditioning, n_pooled = compel(neg_prompt)
    ret = pipe(width=width,
        height=height,
        prompt_embeds=p_conditioning,
        pooled_prompt_embeds=p_pooled,
        negative_prompt_embeds=n_conditioning,
        negative_pooled_prompt_embeds=n_pooled,
        num_inference_steps=500)
    ret.images[0].save(os.path.join(os.path.dirname(__file__), "tmp","tmp_img.jpg"))

if __name__ == "__main__":
    
    call_sd()
    # main()