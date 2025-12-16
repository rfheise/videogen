from .Narrator import Narrator
from ..StoryGen import Story, FileStoryGen,ChatGPTStoryGen,Phrase
from kokoro import KPipeline
import soundfile as sf
import os
from .Audio import AudioClip, AudioList
from ..Helper import Logger
import warnings
from tqdm import tqdm
from pydub import AudioSegment

warnings.filterwarnings("ignore")

class KokoruNarrator(Narrator):

    voices = ['af_heart','am_michael','am_fenrir','af_bella','bf_emma','jf_alpha','zm_yunjian','ef_dora','ff_siwis','hf_alpha','im_nicola','pm_santa']
    
    def __init__(self, story, voice='am_michael'):
        super().__init__(story)

        if voice not in KokoruNarrator.voices:
            Logger.err(f"voice does not exist using {KokoruNarrator.voices[0]} instead")
            voice = KokoruNarrator.voices[0]
        self.voice = voice 

    @staticmethod
    def get_folder():
        return os.path.join(os.path.dirname(__file__),"tmp")
    
    def call_audio_generator(self, story):
        Logger.log("Using Kokoru To Generate The Audio")
        tmp_file_dir = os.path.join(self.get_folder(),'tmp_audio')
        pipeline = KPipeline(lang_code='a',repo_id="hexgrad/Kokoro-82M")
        text = [p.s for p in story.phrases]
        generator = pipeline(text, voice=self.voice)
        audio_clips = AudioList()
        id_to_fname = lambda x:os.path.join(tmp_file_dir, f'{self.voice}-audio-{x}.wav')
        for i, (gs, ps, audio) in tqdm(enumerate(generator), total=len(text)):
            # print(i, gs, ps)
            # display(Audio(data=audio, rate=24000, autoplay=i==0))
            audio_file = id_to_fname(self.story.phrases[i].id)
            sf.write(audio_file, audio, 24000)
            audio_clips.add_item(audio_file)
        self.annotate_story(audio_clips)
        return audio_clips
    
    def annotate_story(self, audio_clips):
        
        clips = {int(clip.fname.strip(".wav").split("-")[-1]):i for i,clip in enumerate(audio_clips)}
        start = 0
        for phrase in self.story.phrases:
            phrase_clip = audio_clips.get_item(clips[phrase.id])
            end = start + len(phrase_clip.audio_segment) / 1000
            phrase.start = start 
            phrase.end = end 
            start = end



if __name__ == "__main__":
    prompt = "Marcus Aurelius teaching Commodus how to ride a horse"
    # story = ChatGPTStoryGen(prompt).generate_story()
    story_path = os.path.join(KokoruNarrator.get_folder(), "tmp_story","rome.txt")
    story = FileStoryGen(story_path).generate_story()
    n = KokoruNarrator(story)
    story, audio_list = n.generate_audio()
    out_file = os.path.join(KokoruNarrator.get_folder(),"out.wav")
    audio_list.merge_clips(out_file)
