import os 
from ..Helper import Logger
from .WriteVideo import write_video, combine_audio_video

class Render():

    def __init__(self, frames, audio, fps):
        
        self.frames = frames 
        self.fps = fps
        self.audio = audio 
    
    @property
    def tmp_path(self):
        path = os.path.join(os.path.dirname(__file__),"tmp")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path 
    
    def render(self, outfile):
        Logger.log("Rendering Visual Data")
        video_file = os.path.join(self.tmp_path, "tmp.mp4")
        audio_file = os.path.join(self.tmp_path, "tmp.wav")

        self.render_video(video_file)
        self.render_audio(audio_file)
        self.combine_av(outfile, video_file, audio_file)

        Logger.log("Rendering Complete")
        Logger.log(f"Video Saved To: {outfile}\n")
    
    def render_audio(self, audio_file):
        self.audio.merge_clips(audio_file)
    
    def render_video(self, video_file):
        write_video(self.frames, video_file, self.fps)

    def combine_av(self, outfile, video_file, audio_file):
        
        combine_audio_video(outfile, video_file, audio_file)
        