class Node:

    def __init__(self):
        self.tag = ""
        self.start_tag = None
        self.end_tag = None
        self.attribute = None
        self.content = "" #None
        self.styles = {}
        self.id = None
        self._class = None # Figure out a way to make this just class
        self.parent = None
        self.children = []
    
    def add_child(self, node):
        self.children.append(node)
    
    def set_parent(self, node):
        self.parent = node
    
    def get_parent(self):
        return self.parent

    def set_tag(self, name:str):
        self.tag = name

    def get_tag(self):
        return self.tag
    
    def set_start_tag(self, start_tag:str):
        self.start_tag = start_tag
    
    def get_start_tag(self):
        return self.start_tag

    def set_end_tag(self, end_tag:str):
        self.end_tag = end_tag

    def get_end_tag(self):
        return self.end_tag

    def set_content(self, attribute:str):
        self.content = attribute
    
    def get_content(self):
        return self.content
    
