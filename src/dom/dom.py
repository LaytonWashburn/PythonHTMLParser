from parser.tokens import Token
from dom.node import Node
import logging

class DOM:

    def __init__(self, tokens:list):
        self.tokens = tokens
        self.root = None
        self.current_node = None
        self.metadata = []

    def add(self):
        pass

    # Private method to iterate through the tree
    def _recurse_tree(self, node:Node, dom:str, tabs:int):
        with_children = '\n'+ (('   ' * tabs) + node.get_content() + '\n' if node.get_content() != "" else "")
        dom = dom + node.get_start_tag() + (with_children if len(node.children) != 0 else node.get_content())
        tabs += 1
        for n in node.children:
            dom += ('   ' * tabs)
            dom = self._recurse_tree(node=n, dom = dom, tabs=tabs)
        space = ('   ' * (tabs - 1)) + node.get_start_tag() + ('\n' if node.get_parent() is not None else "") if len(node.children) != 0 else node.get_end_tag() + ('\n' if node.get_parent() is not None else "")
        dom = dom + space
        return dom

    def recurse_tree(self, dom:str, tabs:int):
        return self._recurse_tree(self.root, dom=dom, tabs=tabs)


    def get_dom(self):
        logging.debug("=============== Starting to Print DOM ===============")
        # logging.debug(self.root)
        dom = self.recurse_tree(dom="", tabs=0)
        #logging.debug(dom)
        print(dom)
        logging.debug("=============== Finished Printing the DOM ===============")


    # Build the DOM by iterating through the tokens
    def build(self):

        logging.debug("=============== Starting to Build the Tree ===============")
        for token in self.tokens:
            
            logging.debug(token.get_name())
            logging.debug(token.get_attribute())

            if token is None:
                logging.debug("Token is None")
                continue

            if token.get_name() == "CONTENT":
                self.current_node.set_content(token.get_attribute())
            
            elif token.get_name() == "CLOSE_END_TAG":
                self.current_node.set_end_tag(token.get_attribute())
                self.current_node = self.current_node.get_parent()

            elif token.get_name() == "CLOSE_START_TAG":
                node = Node()
                node.set_start_tag(token.get_attribute())
                if self.root is None :
                    if token.get_attribute().startswith("<html"):
                        self.current_node = node
                        self.root = self.current_node
                    else:
                        node.set_start_tag(token.get_attribute())
                        self.metadata.append(node)
                else:
                    node.set_parent(node=self.current_node)
                    self.current_node.add_child(node=node)
                    self.current_node = node



            else:
                logging.debug("Tag not recognized")

    