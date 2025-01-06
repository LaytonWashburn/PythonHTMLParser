"""
    Python File: render_tree.py
    Purpose: Combines the DOM and the CSSOM into a singular data structure
    Notes: 
"""
from __future__ import annotations
from RenderEngine.DOM.parser.dom import DOM
from RenderEngine.DOM.parser.node import Node
from RenderEngine.CSSOM.parser.cssom import CSSOM
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
        self.content_height:str = "100%"
        self.total_height:int|None = None
        self.content_width:str = "100%"
        self.total_width:int|None = None
        self.padding:str|int = 0
        self.padding_left:str|int = 0
        self.padding_right:str|int = 0
        self.padding_top:str|int = 0
        self.padding_bottom:str|int = 0
        self.margin:str|int = 0
        self.margin_left:str|int = 0
        self.margin_right:str|int = 0
        self.margin_top:str|int = 0
        self.margin_bottom:str|int = 0
        self.x_pos = 0
        self.y_pos = 0
        self.last_child_x_pos = 0
        self.last_child_y_pos = 0
        self.position:int|None = None
        self.parent:TreeNode|Node = None
        self.children:list[TreeNode] = []
    
    def set_styles(self, key:str, value:str):
        self.styles[key] = value
    
    def get_style(self, key:str) -> str|None:
        return self.styles.get(key, None)

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
    
    def get_content_height(self):
        return self.content_height
    
    def set_content_height(self, content_height):
        self.content_height = content_height
    
    def get_total_height(self):
        return self.total_height

    def set_total_height(self, total_height):
        self.total_height = total_height
    
    def get_content_width(self):
        return self.content_width
    
    def set_content_width(self, content_width):
        self.content_width = content_width
    
    def get_total_width(self):
        return self.total_width

    def set_total_width(self, total_width):
        self.total_width = total_width
    
    def get_padding(self):
        return self.padding

    def set_padding(self, padding):
        self.padding = padding
    
    def set_padding_left(self, padding_left):
        self.padding_left = padding_left
    
    def get_padding_left(self):
        return self.padding_left

    def set_padding_right(self, padding_right):
        self.padding_right = padding_right
    
    def get_padding_right(self):
        return self.padding_right

    def set_padding_top(self, padding_top):
        self.padding_top = padding_top
    
    def get_padding_top(self):
        return self.padding_top 
    
    def set_padding_bottom(self, padding_bottom):
        self.padding_bottom = padding_bottom
    
    def get_padding_bottom(self):
        return self.padding_bottom
    
    def get_margin(self):
        return self.margin

    def set_margin(self, margin):
        self.margin = margin
    
    def set_margin_left(self, margin_left):
        self.margin_left = margin_left
    
    def get_margin_left(self):
        return self.margin_left

    def set_margin_right(self, margin_right):
        self.margin_right = margin_right
    
    def get_margin_right(self):
        return self.margin_right

    def set_padding_top(self, margin_top):
        self.margin_top = margin_top
    
    def get_margin_top(self):
        return self.margin_top 
    
    def set_margin_bottom(self, margin_bottom):
        self.margin_bottom = margin_bottom
    
    def get_margin_bottom(self):
        return self.margin_bottom
    
    def add_child(self, node:TreeNode):
        self.children.append(node)
    
    def set_x_pos(self, x_pos:str|int|float):
        self.x_pos = x_pos
    
    def get_x_pos(self) -> int|float:
        return self.x_pos

    def set_y_pos(self, y_pos:str|int|float):
        self.y_pos = y_pos
    
    def get_y_pos(self) -> int|float:
        return self.y_pos

    def get_last_child_x_pos(self) -> int|float:
        return self.last_child_x_pos
    
    def set_last_child_x_pos(self, last_child_x_pos:int|float):
        self.last_child_x_pos = last_child_x_pos
    
    def get_last_child_y_pos(self) -> int|float:
        return self.last_child_y_pos
    
    def set_last_child_y_pos(self, last_child_y_pos:int|float):
        self.last_child_y_pos = last_child_y_pos
    
    def get_parent(self) -> TreeNode:
        return self.parent
    
    def set_parent(self, node:TreeNode|None):
        self.parent = node
    
    def get_parent_name(self):
        return self.parent.get_name() if self.parent is not None else None

    def get_parent_height(self):
        return self.parent.get_content_height() if self.parent is not None else self.content_height
    
    def get_parent_width(self):
        return self.parent.get_content_width() if self.parent is not None else self.content_width
    
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
    
    def get_root(self) -> TreeNode:
        return self.root

    def add_styles(self, node:Node, render_node:TreeNode, lookup:dict):

        # Check regular

        if lookup.get(node.get_tag(), None) is not None:
            dict = lookup.get(node.get_tag()).get_style().get_styles()
            render_node.styles.update(dict)

        # Check class
        _class = node.get_attribute("class")
        if _class is not None and lookup.get("."+_class, None) is not None:
            dict = lookup.get("."+node.get_tag()).get_style().get_styles()
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
            child_render_node.set_parent(node=render_node)
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
