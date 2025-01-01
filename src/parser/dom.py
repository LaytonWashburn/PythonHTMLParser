from lexer.tokens import Token
from parser.node import Node
from tables.tables import TokenTypeTable,Transitiontable
import logging

class DOM:

    def __init__(self, tokens:list):
        self.tokens:list = tokens
        self.root:Node = None
        self.current_node:Node = None
        self.token_index:int = 0
        self.mode:str = None
        self.eof_tokens = False
        self.token_type_table:TokenTypeTable = TokenTypeTable('src/tables/parser_token_type_table.csv')
        self.transition_table:Transitiontable = Transitiontable('src/tables/parser_transition_table.csv')

    def get_next_token(self):
        if self.token_index < len(self.tokens):
            index = self.token_index
            self.token_index += 1
            return self.tokens[index]
        return None

    def rollback(self):
        if self.token_index == 0:
            self.token_index = 0
        self.token_index -= 1

    def truncate(self, lexeme:str, remove:str):
        if len(lexeme) == 0 or lexeme is None or lexeme == "":
            return ""
        return lexeme.removesuffix(remove)

    def add(self):
        pass

    # Private method to iterate through the tree
    def _recurse_tree(self, node:Node, dom:str, tabs:int):
        with_children = '\n'+ (('   ' * tabs) + node.get_token_value() + '\n' if node.get_token_value() != "" else "")
        dom = dom + node.get_opening_tab() + (with_children if len(node.children) != 0 else node.get_token_value())
        tabs += 1
        for n in node.children:
            dom += ('   ' * tabs)
            dom = self._recurse_tree(node=n, dom = dom, tabs=tabs)
        space = ('   ' * (tabs - 1)) + node.get_closing_tag() + ('\n' if node.get_parent() is not None else "") if len(node.children) != 0 else node.get_closing_tag() + ('\n' if node.get_parent() is not None else "")
        dom = dom + space
        return dom

    def recurse_tree(self, dom:str, tabs:int):
        return self._recurse_tree(self.root, dom=dom, tabs=tabs)


    def get_dom(self):
        # logging.debug(self.root)
        dom = self.recurse_tree(dom="", tabs=0)
        #logging.debug(dom)
        print(dom)
    
    def build(self):
        logging.debug("=============== Building DOM ===============")
        while self.eof_tokens is False:
            token = self.next_tag()
            _type = token.get_token_type()
            value = token.get_token_value()
            if token is None:
                raise Exception(f"Error in HTML parsing:")

            if _type == "close_start_tag":
                node = Node()
                node.set_open_tag(open_tag=value)
                if self.root is None:
                    self.root = node
                    self.current_node = self.root
                else:
                    if self.current_node is None:
                        raise Exception(f"Error in HTML parsing: {value} not valid html")
                    node.set_parent(self.current_node)
                    self.current_node.add_child(node=node)
                    self.current_node = node
            elif _type == "content":
                if self.current_node is None:
                    raise Exception(f"Error in HTML parsing: {value} not valid html")
                self.current_node.set_content(content=value)
            elif _type == "close_end_tag":
                if self.current_node is None:
                    raise Exception(f"Error in HTML parsing: {value} not valid html")
                self.current_node.set_close_tag(close_tag=value)
                self.current_node = self.current_node.get_parent()
            else:
                logging.debug("=============== No Tag Recognized ===============")
        logging.debug("=============== Finished Building the DOM ===============")

    # Build the DOM by iterating through the tokens
    def next_tag(self) -> Token:

        logging.debug("=============== Getting Next Tag ===============")
        stack = []
        curr = 0
        cat = None
        state = "START"
        lexeme = ""

        # Clear stack and push "bad" to the stack
        stack.append("bad")

        # While not in the error state
        while state != None:
            try:
                curr = self.get_next_token(); # This throws an eof error // Gets the next character
                if curr is None:
                    self.eof_tokens = True
            except Exception as e:
                state = None # "error" # This might need to be none
                curr = 0
        
            if curr is not None: # Append curr to the end of lexeme
                lexeme += curr.get_token_value(); 
            else:
                lexeme += " " # End of File Space to be able to rollback

            # If an accept state clear stack
            if self.token_type_table.getTokenType(state=state) is not None:
                stack.clear()
            

            stack.append(state); # Push state onto stack

            if curr is not None:
                cat = curr.get_token_type() #self.classifier_table.getClassification(curr) # Get the current character's Category
            else:
                cat = None
            state = self.transition_table.getTransition(state=state, transition=cat) # Get the new State from the TransitionTable given the current state and cat

        # While not an accept state and state is not "bad"
        while self.token_type_table.getTokenType(state=state) is None and state != "bad":
            state = stack.pop() # Pop the stack and set result as the new state

        # Try to remove the last character from lexeme and rollback the ss iterator or throw an exception and continue
        try: 
            
            if curr is not None:   
                lexeme = self.truncate(lexeme=lexeme, remove=curr.get_token_value() )
                self.rollback() 
        except Exception as e:
            print("Printing error in Exception")
            print(f"An error occurred: {e}")

        # If an accept state return a Token with the type and lexeme or return error
        if self.token_type_table.getTokenType(state=state) is not None and state != "bad":
            logging.debug(f"=============== Returning Tag : token_type={self.token_type_table.getTokenType(state=state)}, toekn_value={lexeme} ===============")
            return Token(token_type=self.token_type_table.getTokenType(state=state), token_value=lexeme) 
        else:
            logging.debug("=============== Returning None ===============")
            return None

    