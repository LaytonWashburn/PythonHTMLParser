from parser.dom import DOM
from lexer.lexer import Lexer
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
    lexer = Lexer(html)
    lexer.scan()
    lexer.print_tokens()
    tokens = lexer.get_tokens()
    
    # Make a dom and construct it from tokens
    dom = DOM(tokens=tokens)
    # dom.build()
    # print("Hello")
    # # dom.get_dom()

if __name__ == "__main__":
    main()