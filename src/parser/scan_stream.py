"""
    Class: Stream Reader Class
    Purpose:
    Notes:
"""
class StreamReader:
    def __init__(self, data:str):
        self.data = data
        self.index = 0
        self.eof = False

    def set_eof(self, boolean:bool):
        self.eof = boolean
    
    def next(self):
        if self.index < len(self.data):
            char = self.data[self.index]
            self.index += 1
            return char
        return None
    
    def lookahead(self):
        if self.index < len(self.data):
            char = self.data[self.index]
            return char
        return None

    def rollback(self):
        if self.index == 0:
            return 0
        self.index = self.index - 1
    
    def truncate(self, string:str):
        if len(string) == 0 or string is None or string == "":
            return ""
        return string[:-1]