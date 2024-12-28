
class Node:

    def __init__(self):
        self.tag = ""
        self.opening_tag = ""
        self.closing_tag = ""
        self.attribute = ""
        self.styles = {}
        self.id = ""
        self._class = "" # Figure out a way to make this just class
        self.parent = None
        self.children = []
    
    def add(self, node):
        self.children.append(node)

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
        return self.opening_tag
    
    def set_closing_tag(self, tag:str):
        self.closing_tag = tag
    
    def get_closing_tag(self):
        return self.closing_tag

    def set_parent(self, node):
        self.parent = node
    
    def get_parent(self):
        return self.parent  

# Represents Lexical Token
class Token:

    def __init__(self, name: str, attribute_value: str):
        self.name = name.strip()
        self.attribute_value = attribute_value.strip()

    def get_name(self):
        return self.name
    
    def get_attribute(self):
        return self.attribute_value
    
    def parse_tag(self):
        return self.attribute_value.replace("</", "").replace("<", "").replace(">", "")

    

