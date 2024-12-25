import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Change this to INFO to not have the debug and DEBUG for debugging


class Node:

    def __init__(self):
        self.tag_name = None
        self.opening_tag = None
        self.closing_tag = None
        self.attribute = None
        self.parent = None
        self.children = []
    
    def add(self, node):
        self.children.append(node)

    def set_tag_name(self, name:str):
        self.tag_name = name

    def set_attribute(self, attribute:str):
        self.attribute = attribute
    
    def set_opening_tag(self, tag:str):
        self.opening_tag = tag
    
    def set_closing_tag(self, tag:str):
        self.closing_tag = tag

    def set_parent(self, node):
        self.parent = node

# Representation of the DOM
class DOM:

    def __init__(self, tokens):
        self.root = None
        self.tokens = tokens
        self.current_node = None

    def add(self):
        pass

    def get_dom(self):
        logging.debug(self.root)

    # Build the DOM by iterating through the tokens
    def build(self):
        logging.debug("=============== Starting to Build the Tree ===============")
        for token in self.tokens:
            
            logging.debug(token.get_name())
            logging.debug(token.get_attribute())

            node = Node() # Make a node
            
            if token.get_name() == "OPENING_TAG":
                node.set_opening_tag(token.get_attribute())

                if self.root is None: # If there's no root node make the current node the root
                    self.root = node
                    self.current_node = node

                else: # If there's a root, make it 
                    node.parent = self.current_node
                    self.current_node.add(node=node)
                    self.current_node = node
                

            if token.get_name() == "ATTRIBUTE":
                self.current_node.set_attribute(token.get_attribute())


            if token.get_name() == "CLOSING_TAG":
                self.current_node.set_closing_tag(token.get_attribute())
                if self.current_node.parent is not None:
                    self.current_node = self.current_node.parent
        

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

    

