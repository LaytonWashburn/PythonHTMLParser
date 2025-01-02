from HTML.parser.dom import DOM
from lexer.lexer import Lexer
from CSS.parser.cssom import CSSOM
from tests import Test
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Change this to INFO to not have the debug and DEBUG for debugging


# Main Entry Point to the Basic HTML Parser
def main():    
    
    # Make a test Object
    test = Test()
    html, css = test.get_html()

    # Make a parser object and parse
    html_lexer = Lexer(html, 
                  classifier='src/tables/classifier_table.csv',
                  transition='src/tables/html/transition_table.csv',
                  token_type='src/tables/html/token_type_table.csv')
    html_lexer.scan()
    html_lexer.print_tokens()
    html_tokens = html_lexer.get_tokens()
    
    # Make a dom and construct it from tokens
    dom = DOM(tokens=html_tokens)
    dom.build()
    # print("Hello")
    # # dom.get_dom()

    css_lexer = Lexer(css,
                      classifier='src/tables/classifier_table.csv',
                      transition='src/tables/css/transition_table.csv',
                      token_type='src/tables/css/token_type_table.csv')
    css_lexer.scan()
    css_lexer.print_tokens()
    
    cssom = CSSOM(tokens=css_lexer.get_tokens())
    cssom.print_tokens()
    cssom.build()

    

if __name__ == "__main__":
    main()