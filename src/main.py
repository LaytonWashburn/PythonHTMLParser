from dom.dom import DOM
from parser.parse import Parser
from tests import Test
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Change this to INFO to not have the debug and DEBUG for debugging


# Main Entry Point to the Basic HTML Parser
def main():    
    
    # Make a test Object
    test = Test()
    html = test.get_html()

    # Make a parser object and parse
    parser = Parser(html)
    parser.parse()
    parser.print_tokens()
    tokens = parser.get_tokens()

    # Make a dom and construct it from tokens
    dom = DOM(tokens=tokens)
    dom.build()
    print("Hello")
    # dom.get_dom()

if __name__ == "__main__":
    main()