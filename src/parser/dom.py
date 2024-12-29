from lexer.tokens import Token
from parser.node import Node
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

            logging.debug("Tag not recognized")

    