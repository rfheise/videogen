from .StoryGen import ChatGPTStoryGen, FileStoryGen
from .Narrator import KokoruNarrator
from .FrameGen import SDFrameGen, ChatGPTFrameGen, GeminiFrameGen
from .Render import Render
import os 

def main():
    
    # prompt = "The story of moses splitting the red sea"
    prompt = """
       The assassination of Julius Caesar and the fall of the Roman Republic
    """
    fps = 30
    # generate the story line
    story_gen = ChatGPTStoryGen(prompt)
    # story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    # story_gen = FileStoryGen(story_path)
    story = story_gen.generate_story()

    # generate audio
    narrator = KokoruNarrator(story)
    story, audio_clips = narrator.generate_audio()
    
    # visual
    frame_gen = GeminiFrameGen(story, audio_clips, fps=fps)
    frames = frame_gen.generate_frames()

    #render
    render = Render(frames, audio_clips, fps)
    outfile = os.path.join(os.path.dirname(__file__), "rome.mp4")
    render.render(outfile)

    #get extras from user
    # extras = []
    # for extra in extras:
    #     extra.generate(story, audio, frames)

if __name__ == "__main__":
    main()
