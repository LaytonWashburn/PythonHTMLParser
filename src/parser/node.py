class Node:

    def __init__(self):
        self.tag = ""
        self.open_start_tag = None # <
        self.close_start_tag = None # >
        self.open_end_tag = None # </
        self.close_end_tag = None # >
        self.open_tag_name = None # example: body
        self.close_tag_name = None # example: body
        self.attribute = None
        self.content = None
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

    def set_attribute(self, attribute:str):
        self.attribute = attribute
    
    def get_attribute(self):
        return self.attribute
    
    def set_opening_tag(self, tag:str):
        self.opening_tag = tag
    
    def get_opening_tab(self):
        return self.open_start_tag
    
    def set_closing_tag(self, tag:str):
        self.closing_tag = tag
    
    def get_closing_tag(self):
        return self.closing_tag

    def set_open_tag_name(self, name:str):
        self.open_tag_name = name
    
    def get_open_tag_name(self):
        return self.open_tag_name
    
    def set_close_tag_name(self, name:str):
        self.set_close_tag_name = name
    
    def get_close_tag_name(self):
        return self.close_tag_name