from .StoryGen import ChatGPTStoryGen, FileStoryGen
from .Narrator import KokoruNarrator
from .FrameGen import SDFrameGen
from .Render import Render
import os 

def main():

    prompt =  prompt = """Write a vivid, detailed narrative retelling of the biblical event in which Jesus turns water into wine at the wedding in Cana.
    Focus on sensory details (sounds, textures, expressions, atmosphere), the social and cultural context of a first-century Jewish wedding, and the quiet tension created when the wine runs out. Portray the human reactions of Mary, the servants, the steward, and the guests, emphasizing uncertainty, humility, and awe.
    Present Jesus calmly and understated, allowing the miracle to unfold subtly rather than theatrically. Let the transformation of water into wine feel intimate and mysterious, revealed first through the servants’ experience before the broader celebration notices the change.
    Maintain a reverent but literary tone, grounded in historical realism rather than modern language. Do not quote scripture directly; instead, reinterpret the event as a self-contained short story that conveys wonder, restraint, and quiet significance."""
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
    frame_gen = SDFrameGen(story, audio_clips, fps=fps)
    frames = frame_gen.generate_frames()

    #render
    render = Render(frames, audio_clips, fps)
    outfile = os.path.join(os.path.dirname(__file__), "video.mp4")
    render.render(outfile)

    #get extras from user
    # extras = []
    # for extra in extras:
    #     extra.generate(story, audio, frames)

if __name__ == "__main__":
    main()
