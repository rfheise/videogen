from .Logger import Logger
from .Queue import LRU


class CacheItem():

    def __init__(self, item):
        self.item = item 
        self.loaded = False
    
    def load(self):

        if self.loaded:
            return
        self.loaded = True
        # the inherited class should do the rest

    def free(self):

        if not self.loaded:
            return
        
        self.loaded = False 
        # the inherited class should do the rest



#list with indexing as LRU cache
class CacheList():

    def __init__(self, size, cache_class=CacheItem):
        self.items = []
        self.buffer = LRU(size)
        self.cache_class = cache_class
    
    def add_item(self, item):

        cache_item = self.cache_class(item)
        self.items.append(cache_item)
        if cache_item.loaded:
            self.add_to_buffer(len(self.items) - 1)
        return len(self.items) - 1
        
    def add_to_buffer(self, item):
        ret = self.buffer.add(item)
        if ret is not None:
            self.items[ret].free()

    def get_item(self, idx):
        item = self.items[idx]
        item.load()
        self.add_to_buffer(idx)
        return item.item

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        for i in range(len(self)):
            yield self.get_item(i)






    