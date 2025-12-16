from ..Helper import CacheList, CacheItem, Logger
from pydub import AudioSegment


        
class AudioClip():

    def __init__(self, fname):
        self.fname = fname 
        self.audio_segment = AudioSegment.from_wav(fname)
        
class AudioCacheItem(CacheItem):

    def __init__(self, fname):
        self.fname = fname
        super().__init__(None)

    def load(self):

        super().load()
        self.item = AudioClip(self.fname)
        #load file into memory
    
    def free(self):

        super().free()
        self.item = None
        #free file from memory

class AudioList(CacheList):
    def __init__(self, size=10):
        super().__init__(size, AudioCacheItem)
    def merge_clips(self, outfile):
        Logger.log(f"Exporting Audio to {outfile}")
        out = AudioSegment.empty()
        for i in range(len(self)):
            out += self.get_item(i).audio_segment
        out.export(outfile, format="wav")