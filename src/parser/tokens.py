import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Change this to INFO to not have the debug and DEBUG for debugging


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

# Representation of the DOM
class DOM:

    def __init__(self, tokens):
        self.root = None
        self.tokens = tokens
        self.current_node = None

    def add(self):
        pass

    # Private method to iterate through the tree
    def _recurse_tree(self, node:Node, dom:str, tabs:int):
        with_children = '\n'+ (('   ' * tabs) + node.get_attribute() + '\n' if node.get_attribute() != "" else "")
        dom = dom + node.get_opening_tab() + (with_children if len(node.children) != 0 else node.get_attribute())
        tabs += 1
        for n in node.children:
            dom += ('   ' * tabs)
            dom = self._recurse_tree(node=n, dom = dom, tabs=tabs)
        space = ('   ' * (tabs - 1)) + node.get_closing_tag() + ('\n' if node.get_parent() is not None else "") if len(node.children) != 0 else node.get_closing_tag() + ('\n' if node.get_parent() is not None else "")
        dom = dom + space
        return dom

    def recurse_tree(self, dom:str, tabs:int):
        return self._recurse_tree(self.root, dom=dom, tabs=tabs)


    def get_dom(self):
        # logging.debug(self.root)
        dom = self.recurse_tree(dom="", tabs=0)
        #logging.debug(dom)
        print(dom)

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
                    node.set_parent(self.current_node)
                    self.current_node.add(node=node)
                    self.current_node = node
                

            if token.get_name() == "ATTRIBUTE":
                self.current_node.set_attribute(token.get_attribute())


            if token.get_name() == "CLOSING_TAG":
                self.current_node.set_closing_tag(token.get_attribute())
                self.current_node.set_tag(self.current_node.opening_tag + self.current_node.attribute + self.current_node.closing_tag)
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

    

