from parser.tokens import Token
from dom.node import Node
import logging

class DOM:

    def __init__(self, tokens:list):
        self.tokens = tokens
        self.root = None
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
            logging.debug(f"Current token: {token.get_name()} : {token.get_attribute()}")

            tag_name = token.get_name()

            if tag_name == "OPEN_TAG":

                node = Node() # Make a node
                
                if self.root is None: # If there's no root node make the current node the root
                    node.open_start_tag = token.get_attribute()
                    self.root = node # Set current node to node
                    self.current_node = self.root # Set current node to root

                else: # If there's a root, make it 
                    if self.current_node.close_end_tag is None: # If needs to be placed as a child
                        self.current_node.add_child(node=node) # Add node as a child
                        node.set_parent(self.current_node) # Connet node to
                        self.current_node = node # Move current node to child
                    else: # If needs to be placed as a sibling
                        parent = self.current_node.get_parent()
                        parent.add_child(node=node)

            elif tag_name == "OPEN_END_TAG":
                self.current_node.close_start_tag = token.get_attribute()

            elif tag_name == "END_STRING":
                self.current_node.set_attribute(token.get_attribute())
                # if self.current_node.open_tag_name is not None:
                #     pass
            
            elif tag_name == "EQUAL":
                pass

            elif tag_name == "CLOSE_TAG":
                self.current_node.set_closing_tag(token.get_attribute())
                self.current_node.set_tag(self.current_node.attribute)
                if self.current_node.parent is not None:
                    self.current_node = self.current_node.parent

            else:
                logging.debug("Tag not recognized")

    