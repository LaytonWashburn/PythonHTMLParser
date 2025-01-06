from RenderEngine.DOM.parser.dom import DOM
from RenderEngine.CSSOM.parser.cssom import CSSOM
from RenderEngine.CSSOM.parser.css_nodes import CSSStyleSheet
from RenderEngine.render_tree.render_tree import RenderTree
from PySide6.QtCore import QThread, Signal, Slot
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


# Worker Threads for each task
class DOMWorker(QThread):
    # Signal to indicate task completion
    dom_ready = Signal(object)

    def __init__(self, html_tokens):
        super().__init__()
        self.html_tokens = html_tokens

    def run(self):
        # Perform DOM parsing
        dom = DOM(tokens=self.html_tokens)
        dom.build()  # Construct the DOM
        self.dom_ready.emit(dom)  # Emit signal with dom object

class CSSOMWorker(QThread):
    # Signal to indicate task completion
    cssom_ready = Signal(object)

    def __init__(self, css_tokens):
        super().__init__()
        self.css_tokens = css_tokens

    def run(self):
        # Perform CSSOM parsing
        cssom = CSSOM(tokens=self.css_tokens)
        current_sheet = CSSStyleSheet(name="index.css")
        cssom.set_current_sheet(current_sheet=current_sheet)
        cssom.get_document_style_sheets().add_style_sheet(style_sheet=cssom.get_current_sheet())
        cssom.build()
        self.cssom_ready.emit(cssom)  # Emit signal with cssom object

class RenderTreeWorker(QThread):
    # Signal to indicate task completion
    render_tree_ready = Signal(object)

    def __init__(self, dom, cssom):
        super().__init__()
        self.dom = dom
        self.cssom = cssom

    def run(self):
        # Perform render tree construction
        render_tree = RenderTree(dom=self.dom, cssom=self.cssom)
        render_tree.build()
        self.render_tree_ready.emit(render_tree)  # Emit signal with render_tree object
