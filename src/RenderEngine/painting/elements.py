import skia
import sys


class HTMLElement:
    def __init__(self, tag_name, attributes):
        self.tag_name = tag_name
        self.attributes = attributes  # e.g., {'x': 10, 'y': 10, 'width': 100, 'height': 50, 'color': (255, 0, 0, 255)}
    
    def render(self, painter):
        # Default render method for most elements (like div, span, etc.)
        color = self.attributes.get('color', (0, 0, 0, 255))  # Default color is black
        painter.draw_rect(self.attributes["x"], self.attributes["y"], self.attributes["width"], self.attributes["height"], color)


class ButtonElement(HTMLElement):
    def __init__(self, attributes):
        super().__init__("button", attributes)
    
    def render(self, painter):
        # Custom render method for <button> element
        color = self.attributes.get('color', (0, 0, 255, 255))  # Default color is blue
        painter.draw_rect(self.attributes["x"], self.attributes["y"], self.attributes["width"], self.attributes["height"], color)
        painter.draw_text(self.attributes["text"], self.attributes["x"] + 10, self.attributes["y"] + 30, 30)


class DivElement(HTMLElement):
    def __init__(self, attributes):
        super().__init__("div", attributes)
