from .SDFrameGen import SDFrameGen
from openai import OpenAI
import base64

class ChatGPTFrameGen(SDFrameGen):

    
    def generate_image(self, prompts, out_files):
        

        for i,p in enumerate(prompts):
            client = OpenAI() 
            response = client.responses.create(
                model="gpt-5",
                input=p['positive_prompt'],
                tools=[
                    {
                        "type": "image_generation",
                        "quality": "low",
                        "size": "1024x1024"
                    }
                ],)
            image_data = [
                output.result
                for output in response.output
                if output.type == "image_generation_call"
            ]
            if image_data:
                image_base64 = image_data[0]
                with open(out_files[i], "wb") as f:
                    f.write(base64.b64decode(image_base64))
        
        return out_files