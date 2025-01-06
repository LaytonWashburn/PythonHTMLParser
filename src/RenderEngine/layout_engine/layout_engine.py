"""
    Python File: layout_engine.py
    Purpose: Take in the render tree and arrange elements visual on the screen
    Notes:
"""

from RenderEngine.layout_engine.phases import size, position
from RenderEngine.render_tree.render_tree import RenderTree, TreeNode
import logging

class LayoutEngine:

    def __init__(self, screen_width = 1366, screen_height = 786, root:TreeNode = None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.root:TreeNode|None = root

        if self.root is not None:
            self.root.set_content_height = screen_height
            self.root.set_content_width = screen_width

    def compute_total_height(self, node:TreeNode):

        height = node.get_style("height") if node.get_style("height") is not None else node.get_content_height()

        _pt = node.get_style("padding-top") if node.get_style("padding-top") is not None else node.get_padding_top()
        node.set_padding_top(_pt)
        _pb = node.get_style("padding-bottom") if node.get_style("padding-bottom") is not None else node.get_padding_bottom()
        node.set_padding_bottom(_pb)
        _mt = node.get_style("margin-top") if node.get_style("margin-top") is not None else node.get_margin_top()
        node.set_padding_right(_mt)
        _mb = node.get_style("margin-bottom") if node.get_style("margin-bottom") is not None else node.get_margin_bottom()
        node.set_padding_right(_mb)

        if isinstance(height, str) and height.endswith("%"):
            # Multiply the parent height by the percentage
            _parent_height = node.get_parent_height() if node.get_parent() is not None else self.screen_height
            _removed_height = height.replace("%", "")
            _removed_height = float(_removed_height)
            _height = _parent_height * float(_removed_height * 0.01)
            node.set_content_height(content_height=_height)
            # Calculate the total height
            total_height = _height + _pt + _pb + _mt + _mb
            node.set_total_height(total_height=total_height)

        elif isinstance(height, str) and height.endswith("px"):
            _height = float(height.replace("px", ""))
            _height = _height if _height <= self.screen_height else self.screen_height
            node.set_content_height(_height)
            total_height = _height + node.get_padding_top() + node.get_padding_bottom() + node.get_margin_top() + node.get_margin_bottom()
            node.set_total_height(total_height=total_height)

        else:
            logging.debug(f"=============== height format not recognized {height} ===============")

        return node

    def compute_total_width(self, node:TreeNode):
        
        width = node.get_style("width") if node.get_style("width") is not None else node.get_content_width()

        _pr = float(node.get_style("padding-right").replace("px", "")) if node.get_style("padding-right") is not None else node.get_padding_right()
        node.set_padding_right(_pr)
        _pl = float(node.get_style("padding-left").replace("px", "")) if node.get_style("padding-left") is not None else node.get_padding_left()
        node.set_padding_right(_pl)
        _mr = float(node.get_style("margin-right").replace("px", "")) if node.get_style("margin-right") is not None else node.get_margin_right()
        node.set_padding_right(_mr)
        _ml = float(node.get_style("margin-left").replace("px", "")) if node.get_style("margin-left") is not None else node.get_margin_left()
        node.set_padding_right(_ml)

        if isinstance(width, str) and width.endswith("%"):
            # Multiply the parent height by the percentage
            _parent_width = node.get_parent_width() if node.get_parent() is not None else self.screen_width
            _removed_width = width.replace("%", "")
            _removed_width = float(_removed_width)
            _width = _parent_width * float(_removed_width * 0.01)
            node.set_content_width(content_width=_width)
            # Calculate the total height
            total_width = _width + _pr + _pl + _mr + _ml
            node.set_total_width(total_width=total_width)

        elif isinstance(width, str) and width.endswith("px"):
            _width = float(width.replace("px", ""))
            _width if _width <= self.screen_width else self.screen_width
            node.set_content_width(content_width=_width)
            total_width = _width + _pl + _pr + _ml + _mr
            node.set_total_width(total_width=total_width)

        else:
            logging.debug(f"=============== Width format not recognized {width} ===============")

        return node


    def compute_margin(self):
        pass

    def computer_padding(self):
        pass

    def compute_x_pos(self, node:TreeNode):
        
        # This handles the root
        if node.get_parent() is None:
            logging.debug("=============== In the compute x pos parent if none ===============")
            node.set_x_pos(x_pos=0)
        else:
            logging.debug("=============== In the compute x pos parent custom ===============")
            _pml = node.get_parent().get_margin_left()
            _ppl = node.get_parent().get_padding_left()
            _ml = node.get_margin_left()
            _pl = node.get_padding_left()
            _x_pos = _pml + _ppl + _ml + _pl
            node.set_x_pos(x_pos=_x_pos)

        return node

    def compute_y_pos(self, node:TreeNode):

        # This handles the root
        if node.get_parent() is None:
            logging.debug("=============== In the compute y pos parent if none ===============")
            node.set_y_pos(y_pos=0)
        else:
            logging.debug("=============== In the compute y pos parent custom ===============")
            _pmt = node.get_parent().get_margin_top()
            _ppt = node.get_parent().get_padding_top()
            _mt = node.get_margin_top()
            _pt = node.get_padding_top()
            _plcyp = node.get_parent().get_last_child_y_pos()
            _y_pos = _pmt + _ppt + _mt + _pt + _plcyp
            node.set_y_pos(y_pos=_y_pos)

        return node
    
    def _compute_layout(self, node:TreeNode|None):

        logging.debug(f"=============== Starting {node.get_name()} parent = {node.get_parent_name()} ===============")
        node = self.compute_total_height(node=node)
        node = self.compute_total_width(node)
        node = self.compute_x_pos(node=node)
        node = self.compute_y_pos(node=node)
        for child in node.get_children():
            child = self._compute_layout(child)
            node.set_last_child_x_pos(last_child_x_pos=node.get_last_child_x_pos())
            node.set_last_child_y_pos(last_child_y_pos=node.get_last_child_y_pos() + child.get_total_height())

        logging.debug(f"=============== Finished {node.get_name()} width = {node.get_total_width()} height = {node.get_total_height()} x = {node.get_x_pos()} y = {node.get_y_pos()} ===============")
        return node
    
    def compute_layout(self, root:TreeNode|None):
        logging.debug(f"=============== Start to Compute Layout ===============")
        n = self._compute_layout(node=root)
        logging.debug(f"=============== Finished Computing Layout ===============")
        return n