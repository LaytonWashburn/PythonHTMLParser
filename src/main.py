from DOM.parser.dom import DOM
from lexer.lexer import Lexer
from CSSOM.parser.cssom import CSSOM
from CSSOM.parser.css_nodes import (CSSStyeDeclaration, 
                                    CSSRule, 
                                    CSSRuleList, 
                                    MediaList, 
                                    CSSStyleSheet, 
                                    DocumentStyleSheet)
from render_tree.render_tree import RenderTree
from tests import Test
import logging
# import multiprocessing

# Configure logging
logging.basicConfig(level=logging.DEBUG) # Change this to INFO to not have the debug and DEBUG for debugging


# Main Entry Point to the Basic HTML Parser
def main():    
    
    # Make a test Object
    test = Test()
    html = test.get_html()

    #### DOM ####

    # Make a parser object and parse
    html_lexer = Lexer(classifier='src/tables/classifier_table.csv',
                       transition='src/tables/html/transition_table.csv',
                       token_type='src/tables/html/token_type_table.csv',
                       data=html)

    html_lexer.scan()
    html_lexer.print_tokens()
    html_tokens = html_lexer.get_tokens()
    
    # Make a dom and construct it from tokens
    dom = DOM(tokens=html_tokens)
    dom.build() # Construct the DOM
    dom_str = dom.build_dom_str() # Build DOM str
    print(dom_str) # Print the DOM str

    css_lexer = Lexer(classifier='src/tables/classifier_table.csv',
                      transition='src/tables/css/transition_table.csv',
                      token_type='src/tables/css/token_type_table.csv')
    
    #### CSSOM ####

    css_lexer.read_data(file_path='src/Data/css-tests/index.css')
    css_lexer.scan()
    css_lexer.print_tokens()
    css_tokens=css_lexer.get_tokens()

    # This might need to be created before the DOM so that the DOM can use it to start parsing css if -
    # a style sheet is encountered
    cssom = CSSOM(tokens=css_tokens) 
    current_sheet = CSSStyleSheet(name="index.css")
    cssom.set_current_sheet(current_sheet=current_sheet)
    cssom.get_document_style_sheets().add_style_sheet(style_sheet=cssom.get_current_sheet())
    cssom.build()
    cssom.print_tokens()

    #### Render Tree ####
    render_tree = RenderTree(dom=dom, cssom=cssom)
    render_tree.build()



if __name__ == "__main__":
    main()