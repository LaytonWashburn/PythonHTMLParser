# import skia

# def color_name_to_rgb(color_name):
#     """Convert color names to RGB values. If not recognized, return white."""
#     # Simple hardcoded color name to RGB mapping
#     colors = {
#         "lightblue": (173, 216, 230),
#         "black": (0, 0, 0),
#         "white": (255, 255, 255),
#         "red": (255, 0, 0),
#         "green": (0, 255, 0),
#         "blue": (0, 0, 255),
#         "yellow": (255, 255, 0),
#         "lightgreen": (144, 238, 144)
#     }
#     return colors.get(color_name.lower(), (255, 255, 255))  # Default to white if not found

# # Skia renderer
# class SkiaRenderer:
#     def __init__(self):
#         self.canvas = None
#         self.paint = skia.Paint()
#         self.paint.setAntiAlias(True)

#     def init_canvas(self, width, height):
#         """ Initialize Skia Canvas with the width and height from layout. """
#         self.surface = skia.Surface(width, height)
#         self.canvas = self.surface.getCanvas()
        
#     def render_element(self, element):
#         """ Render a single element from the layout using Skia. """
        
#         if element["type"] == "div":
#             # Draw the background of the element (if any)
#             if "background_color" in element:
#                 rgb = color_name_to_rgb(element["background_color"])
#                 self.paint.setColor(skia.Color(*rgb))
#                 self.canvas.drawRect(skia.Rect(element["x"], element["y"], 
#                                               element["x"] + element["width"], 
#                                               element["y"] + element["height"]), self.paint)
        
#         if element["type"] == "text":
#             # Draw text element using the skia.Font object to set font size
#             font = skia.Font(skia.Typeface('sans-serif'), element["font_size"])  # Create font with size
#             rgb = color_name_to_rgb(element["text_color"])
#             self.paint.setColor(skia.Color(*rgb))
            
#             self.canvas.drawString(element["text"], element["x"], element["y"], font, self.paint)
            
#         # Add more cases for other elements like images, borders, etc.

#     def render(self, render_tree):
#         """ Render the entire layout using Skia. """
#         for element in render_tree:
#             self.render_element(element)
        
#     def get_image(self):
#         """ Get the final image from the canvas. """
#         return self.surface.makeImageSnapshot()

# # Example of how layout and render tree might look
# render_tree = [
#     {"type": "div", "x": 10, "y": 10, "width": 200, "height": 100, "background_color": "lightblue"},
#     {"type": "text", "x": 20, "y": 40, "text": "Hello, Skia!", "font_size": 20, "text_color": "black"},
# ]

# # Initialize Skia Renderer
# renderer = SkiaRenderer()

# # Let's assume we get width and height of the layout from the layout engine
# width = 800
# height = 600

# # Initialize canvas with size
# renderer.init_canvas(width, height)

# # Render the entire render tree to the Skia canvas
# renderer.render(render_tree)

# # Get the final image after painting
# final_image = renderer.get_image()

# # Save the image to a file or display it (optional)
# final_image.save('output_image.png', skia.kPNG)

import skia

class Painter:
    def __init__(self):
        self.surface = skia.Surface(800, 600)
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
    
    # No need for a custom render method
    # It will inherit render from HTMLElement that simply draws a box


def render_element(element, painter):
    # Dispatch method to route the rendering based on element type
    if element.tag_name == "img":
        element.render(painter)
    elif element.tag_name == "button":
        element.render(painter)
    elif element.tag_name == "video":
        element.render(painter)
    else:
        # Default case for other tags
        element.render(painter)

def main():
    painter = Painter()
    
    # Define some sample elements
    div = {"x": 100, "y": 100, "width": 200, "height": 30, "color": (255, 255, 255, 255)}
    button = {"x": 140, "y": 120, "width": 200, "height": 30, "color": (255, 0, 0, 255), "text": "Click Me", "font_size": 20}
    
    # Render elements
    painter.draw_rect(div["x"], div["y"], div["width"], div["height"], div["color"])
    painter.draw_text(button["text"], button["x"], button["y"], button["font_size"], button["color"])
    
    # Finalize rendering
    # Create an empty GrFlushInfo object (required for flushing)
    # flush_info = skia.GrFlushInfo()
    # painter.surface.flush(skia.Surface.BackendSurfaceAccess.kRead_Write, flush_info)
    
    # Save the result to an image file
    image = painter.surface.makeImageSnapshot()
    image.save("output.png")

if __name__ == "__main__":
    main()
# import sys
# from PySide6.QtCore import Qt, QRect, QThread, Signal
# from PySide6.QtGui import QPainter, QImage, QColor
# from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
# import skia

# # Simulating the DOM, CSSOM, and Render Tree structures
# class DOM:
#     def __init__(self):
#         self.elements = ["<html>", "<body>", "<h1>Hello World!</h1>", "</body>", "</html>"]

#     def parse(self):
#         # Simulate some parsing work
#         print("DOM parsing started...")
#         # Simulating parsing delay
#         import time
#         time.sleep(2)  # Simulate delay
#         print("DOM parsed")
#         return self.elements

# class CSSOM:
#     def __init__(self):
#         self.styles = ["h1 { font-size: 40px; color: red; }"]

#     def parse(self):
#         # Simulate some parsing work
#         print("CSSOM parsing started...")
#         # Simulating parsing delay
#         import time
#         time.sleep(2)  # Simulate delay
#         print("CSSOM parsed")
#         return self.styles

# class RenderTree:
#     def __init__(self, dom, cssom):
#         self.dom = dom
#         self.cssom = cssom
#         self.render_elements = []

#     def build(self):
#         # Combine DOM and CSSOM to form the Render Tree
#         print("Building render tree")
#         self.render_elements.append({
#             'element': 'h1',
#             'text': "Hello World!",
#             'style': {'font-size': 40, 'color': 'red'}
#         })

#     def get_render_elements(self):
#         return self.render_elements

# # Worker Thread for Parsing HTML and CSS in Background
# class ParsingWorker(QThread):
#     # Signal that will be emitted once parsing is done
#     parsing_finished = Signal(object)

#     def __init__(self, dom, cssom):
#         super().__init__()
#         self.dom = dom
#         self.cssom = cssom

#     def run(self):
#         # Perform the parsing operations in the background
#         dom_data = self.dom.parse()  # Parse DOM
#         cssom_data = self.cssom.parse()  # Parse CSSOM

#         # Construct the render tree
#         render_tree = RenderTree(dom_data, cssom_data)
#         render_tree.build()

#         # Emit the result (render tree) back to the main thread
#         self.parsing_finished.emit(render_tree)


# class SkiaWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.image = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
#         self.image.fill(QColor(255, 255, 255))  # Start with white background
#         self.sk_canvas = None
#         self.painting = False

#         # Create DOM and CSSOM objects
#         self.dom = DOM()
#         self.cssom = CSSOM()

#         # Setup background worker for parsing
#         self.worker = ParsingWorker(self.dom, self.cssom)
#         self.worker.parsing_finished.connect(self.on_parsing_finished)
#         self.worker.start()

#     def on_parsing_finished(self, render_tree):
#         # Once parsing is finished, render tree is constructed
#         self.render_tree = render_tree
#         self.painting = True
#         self.update()  # Trigger widget repainting

#     # def paintEvent(self, event):
#     #     # Initialize Skia canvas
#     #     self.init_skia()

#     #     # Create a QPainter object to paint Skia canvas on QWidget
#     #     painter = QPainter(self)
#     #     painter.drawImage(0, 0, self.image)

#     # def init_skia(self):
#     #     if self.sk_canvas is None:
#     #         surface = skia.Surface(self.width(), self.height())
#     #         self.sk_canvas = surface.getCanvas()

#     #     if self.painting:
#     #         # Perform painting with Skia here
#     #         self.painting = False
#     #         self.sk_canvas.clear(skia.ColorWHITE)

#     #         # Render tree painting logic (based on DOM, CSSOM, Render Tree)
#     #         self.render_elements = self.render_tree.get_render_elements()
#     #         for element in self.render_elements:
#     #             if element['element'] == 'h1':
#     #                 paint = skia.Paint()
#     #                 paint.setColor(skia.ColorRED)  # Set color
#     #                 paint.textSize = element['style']['font-size']  # Set text size (Correct way)

#     #                 # Draw text using Skia's canvas
#     #                 self.sk_canvas.drawString(element['text'], 100, 150, paint)

#     #         # Copy Skia drawing to QImage for Qt painting
#     #         pixels = self.image.bits()
#     #         pixels.setsize(self.image.byteCount())
#     #         self.image = QImage(pixels, self.width(), self.height(), self.image.bytesPerLine(), QImage.Format_ARGB32_Premultiplied)

#     #         self.update()  # Trigger QWidget to re-paint with the updated Skia canvas

#     def start_rendering(self):
#         self.painting = True
#         self.update()  # Request the widget to re-render


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Skia and Qt with Background Parsing")

#         # Create the SkiaWidget (where we paint with Skia)
#         self.skia_widget = SkiaWidget()

#         # Set the widget for the main window
#         self.setCentralWidget(self.skia_widget)

#         # Add a button to start rendering
#         button = QPushButton("Start Rendering", self)
#         button.clicked.connect(self.start_rendering)
#         self.setMenuWidget(button)

#     def start_rendering(self):
#         self.skia_widget.start_rendering()


# def main():
#     app = QApplication(sys.argv)

#     window = MainWindow()
#     window.resize(800, 600)
#     window.show()

#     sys.exit(app.exec())

# if __name__ == '__main__':
#     main()


# # import skia

# # # Create a surface to draw on (width x height)
# # width, height = 800, 600
# # surface = skia.Surface(width, height)

# # # Get the canvas from the surface to draw
# # canvas = surface.getCanvas()

# # # Create a paint object for the text color
# # text_paint = skia.Paint(Color=skia.Color(255, 255, 255))   # White color for text

# # # Create a font object and set the text size
# # font = skia.Font(skia.Typeface('Arial'), 20)

# # # Draw the div (box model)
# # background_paint = skia.Paint(Color=skia.Color(255, 0, 0))  # Red background
# # canvas.drawRect(skia.Rect(100, 100, 300, 200), background_paint)  # Red div box

# # # Draw the text (using the font for text size)
# # canvas.drawString('Hello, Skia!', 120, 160, font, text_paint)

# # # Save to file
# # image = surface.makeImageSnapshot()
# # image.save('output.png', skia.kPNG)
