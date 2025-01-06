"""
    Python File: painter.py
    Purpose: 
    Arguments:  
    Notes:
"""

import skia

class Painter:

    def __init__(self, height=800, width=600):
        self.surface = skia.Surface(height, width)
        self.canvas = self.surface.getCanvas()
        self.paint = skia.Paint()
    
    
    """ Initialize Skia Canvas with the width and height from layout. """
    def init_canvas(self, width, height):
        self.surface = skia.Surface(width, height)
        self.canvas = self.surface.getCanvas()
    
    def draw_rect(self, x, y, width, height, color):
        # Drawing a rectangle with a solid color
        self.paint.setColor(skia.Color(*color))  # Expecting (r, g, b, a)
        self.canvas.drawRect(skia.Rect(x, y, x + width, y + height), self.paint)

    def draw_text(self, text, x, y, font_size, color):
        # Create a font object and set the font size
        font = skia.Font(skia.Typeface('sans-serif'), font_size)
        
        # Set text color
        self.paint.setColor(skia.Color(*color))  # Expecting (r, g, b, a)
        
        # Draw text: correct order of arguments
        self.canvas.drawString(text, x, y, font, self.paint)


    """ Render a single element from the layout using Skia. """
    def render_element(element, painter):
        # Dispatch method to route the rendering based on element type
        if element.tag_name == "button":
            element.render(painter)
        else:
            # Default case for other tags
            element.render(painter)

    # """ Render the entire layout using Skia. """
    # def render(self, render_tree):
    #     for element in render_tree:
    #         self.render_element(element)
            
            
    """ Get the final image from the canvas. """
    def get_image(self):
        return self.surface.makeImageSnapshot()
            