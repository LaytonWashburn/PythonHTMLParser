# Token Class
# Types of tokens : html tags, html value

class Node:

    def __init__(self, name:str):
        self.tag_name = name
        self.parent = None
        self.children = []

# Representation of the DOM
class DOM:

    def __init__(self):
        self.root = None
        self.tree = []

    def add(self, node:Node):
        if self.root is None:
            self.root = node
            self.tree.append(node)
        self.tree.append(node)

# Represents Lexical Token
class Token:

    def __init__(self, name: str, attribute_value: str):
        self.name = name.strip()
        self.attribute_value = attribute_value.strip()
        #node_tag = self.attribute_value.replace("</"," ").replace(">", " ").replace("<", "").strip().split(" ")

    def get_name(self):
        return self.name
    
    def get_attribute(self):
        return self.attribute_value



    

