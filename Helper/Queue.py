from .Logger import Logger 


class Node():

    def __init__(self, val, prev, next):
        self.val = val
        self.prev = prev 
        self.next = next

#generic queue
class Queue():

    def __init__(self):
        self.root = None 
        self.tail = None
        self.size = 0
    
    def enqueue(self, val):

        self.size += 1
        if not self.root:
            self.root = Node(val, None, None)
            self.tail = self.root
            return 
        
        self.root = Node(val, None, self.root)
        self.root.next.prev = self.root
    
    def dequeue(self):

        if self.size == 0:
            return None 
        self.size -= 1
        if self.size == 0:
            ret = self.root.val 
            self.root = None
            self.tail = None
            return ret 

        ret = self.tail.val 
        self.tail = self.tail.prev
        self.tail.next = None
        return ret

class LRU():

    def __init__(self, size):
        self.queue = Queue()
        self.items = {}
        self.max_size = size
    
    #returns item kicked from LRU if applicable otherwise None
    def add(self, item):

        ret = None
        if item in self.items:
            self.remove(self.items[item])
        
        if self.queue.size == self.max_size:
            ret = self.queue.dequeue()
            if not ret:
                del self.items[ret]
        
        self.queue.enqueue(item)
        self.items[item] = self.queue.root

        return ret
    
    def remove(self, node):

        if self.queue.root.val == node.val:
            self.queue.root = self.queue.root.next
            if self.queue.root:
                self.queue.root.prev = None
        
        if node.val == self.queue.tail.val:
            self.queue.tail = node.prev 
            if self.queue.tail:
                self.queue.tail.next = None
        
        if node.prev != None:
            node.prev.next = node.next 
        
        if node.next != None:
            node.next.prev = node.prev 
        
        self.queue.size -= 1




    

        
