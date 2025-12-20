from ..Utilities import CacheList, CacheItem, Logger, LRU
from pydub import AudioSegment
import cv2

        
class Frame():

    def __init__(self, frame):
        self.frame = frame
        
class FrameImageCacheItem(CacheItem):

    lru = LRU(10)

    def __init__(self, fname):
        self.fname = fname
        super().__init__(None)

    def load(self):

        super().load()
        if FrameImageCacheItem.lru.get(self.fname) is not None:
            img = FrameImageCacheItem.lru.get(self.fname)[1]
        else:
            img = cv2.imread(self.fname)
            FrameImageCacheItem.lru.add((self.fname, img))
        self.item = Frame(img)
        #load file into memory
    
    def free(self):

        super().free()
        self.item = None
        #free file from memory

class FrameList(CacheList):
    pass