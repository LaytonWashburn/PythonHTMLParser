# Token Class
# Types of tokens : html tags, html value

class Node:

    def __init__(self, name:str):
        self.tag_name = name
        self.parent = None
        self.children = list()

# Representation of the DOM
class DOM:

    def __init__(self):
        pass

    def add(node:Node):
        pass

class Token:

    def __init__(self, name: str, attribute_value: str, dom:DOM):
        self.name = name
        self.attribute_value = attribute_value
        node_tag = self.attribute_value.replace("</"," ").replace(">", " ").replace("<", "").strip().split(" ")[0]
        print(node_tag)

    def get_name(self):
        return self.name
    
    def get_attribute(self):
        return self.attribute_value



    

