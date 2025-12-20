import sys

class Log():

    def __init__(self):
        pass 

    def log(self, s):
        pass 

    def err(self, s):
        pass 

    def debug(self, s):
        pass

class PrintLog(Log):

    def __init__(self):
        super().__init__()

    def log(self, s):
        print(s)

    def err(self, s):
        print(s, file = sys.stderr)
    
    def debug(self, s):
        self.log(f"Debug: {s}")


class Logger():
    logs = [PrintLog()]
    debug_mode = True

    @staticmethod
    def log(s=""):
        for l in Logger.logs:
            l.log(s)
    
    @staticmethod
    def debug(s=""):
        if not Logger.debug_mode:
            return
        
        for l in Logger.logs:
            l.debug(s)

    @staticmethod
    def err(s=""):
        for l in Logger.logs:
            l.err(s)