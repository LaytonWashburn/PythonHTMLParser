"""
    Python File: render_tree.py
    Purpose: Combines the DOM and the CSSOM into a singular data structure
    Notes: 
"""
from __future__ import annotations
from DOM.parser.dom import DOM
from DOM.parser.node import Node
from CSSOM.parser.cssom import CSSOM
import logging

'''
    Class: TreeNode
    Purpose: Building block for the RenderTree
    Notes: 
'''
class TreeNode:

    def __init__(self):
        self.styles:dict = {}
        self.data:str|None = None
        self.name:str|None = None
        self.children:list[TreeNode] = []
    
    def set_styles(self, key:str, value:str):
        self.styles[key] = value
    
    def get_styles(self) -> dict:
        return self.styles
    
    def set_data(self, data:str):
        self.data = data
    
    def get_data(self) -> str:
        return self.data

    def set_name(self, name:str):
        self.name = name
    
    def get_name(self) -> str:
        return self.name
    
    def add_child(self, node:TreeNode):
        self.children.append(node)

    def get_children(self):
        return self.children
'''
    Class: RenderTree
    Purpose: Representation of the dom and cssom in one data structure
    Dependencies: TreeNode
    Notes:
'''
class RenderTree:

    def __init__(self, dom:DOM, cssom:CSSOM):
        self.dom = dom
        self.cssom = cssom
        self.root:TreeNode|None = None

    def add_styles(self, node:Node, render_node:TreeNode, lookup:dict):

        # Check regular

        if lookup.get(node.get_tag(), None) is not None:
            dict = lookup.get(node.get_tag()).get_style().get_styles()
            render_node.styles.update(dict)

        # Check class
        _class = node.get_attribute("class")
        if _class is not None and lookup.get("."+_class, None) is not None:
            dict = lookup.get("."+node.get_tag())
            render_node.styles.update(dict)

        # Check id
        _id = node.get_attribute("id")
        if _id is not None and lookup.get("#"+_id, None) is not None:
            dict = lookup.get("#"+_id).get_style().get_styles()
            render_node.styles.update(dict)

        return node, render_node
    
    # Private Method to recursively traverse the dom
    def _traverse_dom(self, node:Node, lookup:dict, render_node:TreeNode)-> tuple[Node, TreeNode]:
        logging.debug("=============== Started Traversing the Render Tree ===============")

        render_node.set_name(node.get_tag())
        # if node.get_tag() is None:
        #     return 
        logging.debug(f"=============== {node.get_tag()} ===============")

        # Actions before moving to children
        node, render_node = self.add_styles(node=node, render_node=render_node, lookup=lookup)

        # Traverse the children
        for child in node.get_children():
            child_render_node = TreeNode()
            child, child_render_node = self._traverse_dom(node=child, 
                                                          lookup=lookup, 
                                                          render_node=child_render_node)
            render_node.add_child(node=child_render_node) # Add the child render node to current render node's list of children

        # Actions after moving to children
        logging.debug("=============== Finished Traversing the Render Tree ===============")
        return node, render_node

    # Public Entry Method to recursively traverse the dom
    def traverse_dom(self, root:Node, lookup:dict, render_node:TreeNode) -> tuple[Node, TreeNode]:
        return self._traverse_dom(node=root, 
                                  lookup=lookup, 
                                  render_node=render_node)
    

    def build(self):
        logging.debug("=============== Started Building the Render Tree ===============")

        document_styles = self.cssom.get_document_styles()
        print(document_styles)
        # for key in document_styles.keys():
        #     print(document_styles[key])

        root = self.dom.get_root() # Get html root

        render_root = TreeNode() # Make Render Tree root

        root, self.root = self.traverse_dom(root=root, 
                                            lookup=document_styles,
                                            render_node=render_root)
        
        # print(css_root.get_style_sheets())
        # for sheet in css_root.get_style_sheets():
        #     print(sheet)
        #     for rule in sheet.get_rule_list().get_rule_list():
        #         print(rule)
        logging.debug("=============== Finished Building the Render Tree ===============")
    
