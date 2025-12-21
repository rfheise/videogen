from google import genai
from google.genai import types
from PIL import Image
from .SDFrameGen import SDFrameGen
from openai import OpenAI
import base64
import os 

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiFrameGen(SDFrameGen):

    
    def generate_image(self, prompts, out_files):
        
        max_tries = 3
        for i,p in enumerate(prompts):
            tries = 0
            img_created = False
            # print(out_files[i])
            # exit()
            if os.path.exists(out_files[i]):
                continue
            while tries < max_tries and img_created == False:
                client = genai.Client()
                prompt = p['positive_prompt']
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=[prompt],
                )
                for part in response.parts:
                    if part.text is not None:
                        print(part.text)
                    elif part.inline_data is not None:
                        image = part.as_image()
                        image.save(out_files[i])
                        img_created = True 
                if not img_created:
                    print(f"Image not generated {out_files[i]}")
                tries += 1
        return out_files

