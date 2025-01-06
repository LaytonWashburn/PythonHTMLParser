from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Slot
from BrowserUserInterface.Workers.workers import DOMWorker, CSSOMWorker, RenderTreeWorker
import logging
from RenderEngine.layout_engine.layout_engine import LayoutEngine
from RenderEngine.lexer.lexer import Lexer
from tests import Test
from PySide6.QtCore import Slot
# from PySide6.QtOpenGL import QOpenGLWidget
# from OpenGL.GL import *

class BrowserUserInterface:
    def __init__(self, argv):
        self.app = QApplication(argv)  # sys.argv
        self.main_window = None
    
    # Greetings (Button click handler)
    @Slot()
    def say_hello(self):
        print("Button clicked, Hello!")
    
    def get_main_window_size(self):
        if self.main_window:
            size = self.main_window.size()  # QSize object
            print(f"Main window size: {size.width()}x{size.height()}")
            return size
        else:
            print("Main window is not created yet.")
            return None

    def run(self):
        # Create a QMainWindow (main window)
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("RedScale Browsing")  # Set the title of the window

        # Create a central widget (where the layout will go)
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Get the screen size using QScreen
        screen = self.app.primaryScreen()  # Get the primary screen (for multi-monitor setups, you can select another)
        screen_geometry = screen.geometry()  # Get screen geometry (width and height)
        print(f"Screen Size: {screen_geometry.width()}x{screen_geometry.height()}")  # Debugging

        # Set the window size to the screen size
        self.main_window.resize(screen_geometry.width(), screen_geometry.height())
        self.main_window.setStyleSheet("background-color: #FFFFFF;")  # You can change the color here

        # Create a layout (for organizing widgets inside the central widget)
        layout = QVBoxLayout(central_widget)

        # # Create a label and button
        # label = QLabel("Welcome to RedScale Browser!")
        # button = QPushButton("Click me")

        # # Connect the button's click event to the greeting function
        # button.clicked.connect(self.say_hello)

        # # Add widgets to the layout
        # layout.addWidget(label)
        # layout.addWidget(button)


        self.main_window.show()

        # Start the event loop
        self.app.exec()


class BrowserUserInterfaceApp:

    def __init__(self):
        self.app = BrowserUserInterface([])  # GUI initialization
        self.layout = LayoutEngine()  # Layout engine initialization

        # Create worker threads
        self.test = Test()
        self.html = self.test.get_html()

        html_lexer = Lexer(classifier='src/RenderEngine/tables/classifier_table.csv',
                           transition='src/RenderEngine/tables/html/transition_table.csv',
                           token_type='src/RenderEngine/tables/html/token_type_table.csv',
                           data=self.html)
        html_lexer.scan()
        html_tokens = html_lexer.get_tokens()

        # Start DOM worker
        self.dom_worker = DOMWorker(html_tokens)
        self.dom_worker.dom_ready.connect(self.on_dom_ready)
        self.dom_worker.start()

        # Start CSSOM worker
        self.css_lexer = Lexer(classifier='src/RenderEngine/tables/classifier_table.csv',
                               transition='src/RenderEngine/tables/css/transition_table.csv',
                               token_type='src/RenderEngine/tables/css/token_type_table.csv')
        self.css_lexer.read_data(file_path='src/RenderEngine/Data/css-tests/index.css')
        self.css_lexer.scan()
        css_tokens = self.css_lexer.get_tokens()

        self.cssom_worker = CSSOMWorker(css_tokens)
        self.cssom_worker.cssom_ready.connect(self.on_cssom_ready)
        self.cssom_worker.start()

        # Start the GUI
        self.app.run()

    @Slot(object)
    def on_dom_ready(self, dom):
        self.dom = dom
        logging.info("DOM parsing complete.")
        # Proceed to next task if required or update the UI
        if hasattr(self, 'cssom'):
            self.start_render_tree_worker()

    @Slot(object)
    def on_cssom_ready(self, cssom):
        self.cssom = cssom
        logging.info("CSSOM parsing complete.")
        # Proceed to next task if required or update the UI
        if hasattr(self, 'dom'):
            self.start_render_tree_worker()

    @Slot(object)
    def on_render_tree_ready(self, render_tree):
        self.render_tree = render_tree
        logging.info("Render Tree construction complete.")
        # Here you can update the UI with the render tree, or proceed to the next steps like layout and painting.

    def start_render_tree_worker(self):
        logging.info("Starting render tree construction.")
        # Only start the render tree construction once both DOM and CSSOM are ready
        self.render_tree_worker = RenderTreeWorker(self.dom, self.cssom)
        self.render_tree_worker.render_tree_ready.connect(self.on_render_tree_ready)
        self.render_tree_worker.start()

    def get_main_window_size(self):
        # Retrieve main window size if needed (e.g., once render tree is complete)
        pass