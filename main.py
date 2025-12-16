from .StoryGen import StoryGen

def main():
    prompt = "get story plot user"

    #generate the story line
    story_gen = StoryGen(prompt)
    story = story_gen.generate_story()

    # generate audio
    narrator = Narrator(story)
    story, audio_clips = narrator.generate_audio()
    
    # visual
    frame_gen = FrameGen(story, audio)
    frames = frame_gen.get_frames()

    #render
    render = Render(frames, audio)
    render.render_video("video.mp4")

    #get extras from user
    extras = []
    for extra in extras:
        extra.generate(story, audio, frames)

