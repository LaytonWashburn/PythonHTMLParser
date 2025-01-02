from tables.tables import ClassifierTable, Transitiontable, TokenTypeTable
from lexer.tokens import Token
from CSS.parser.node import Node
import logging

class CSSOM:

    def __init__(self, tokens:list):
        self.tokens = tokens
        # self.classifier_table:ClassifierTable = ClassifierTable('src/tables/classifier_table.csv')
        # self.token_type_table:TokenTypeTable = TokenTypeTable('src/tables/css/parser_token_type_table.csv')
        # self.transition_table:Transitiontable = Transitiontable('src/tables/css/parser_transition_table.csv')

    def get_tokens(self):
        return self.tokens
    
    def print_tokens(self):
        for token in self.tokens:
            print(f"Token: {token.get_token_type()} : {token.get_token_value()}")

    def build(self):
        logging.debug("=============== Building CSSOM ===============")
        # while self.eof_tokens is False:
        #     token = self.next_tag()
        #     _type = token.get_token_type()
        #     value = token.get_token_value()
        #     if token is None:
        #         raise Exception(f"Error in HTML parsing:")

        #     if _type == "close_start_tag":
        #         node = Node()
        #         node.set_open_tag(open_tag=value)
        #         if self.root is None:
        #             self.root = node
        #             self.current_node = self.root
        #         else:
        #             if self.current_node is None:
        #                 raise Exception(f"Error in HTML parsing: {value} not valid html")
        #             node.set_parent(self.current_node)
        #             self.current_node.add_child(node=node)
        #             self.current_node = node
        #     # elif _type == "space":
        #     #     if self.current_node.get_open_tag() is not None and self.current_node is None:
        #     #         pass
        #     elif _type == "content":
        #         if self.current_node is None:
        #             raise Exception(f"Error in HTML parsing: {value} not valid html")
        #         self.current_node.set_content(content=value)
        #     elif _type == "close_end_tag":
        #         if self.current_node is None:
        #             raise Exception(f"Error in HTML parsing: {value} not valid html")
        #         self.current_node.set_close_tag(close_tag=value)
        #         self.current_node = self.current_node.get_parent()
        #     else:
        #         logging.debug("=============== No Tag Recognized ===============")
        logging.debug("=============== Finished Building the CCSOM ===============")


    def next_rule(self):
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
            logging.debug(f"=============== Returning Tag : token_type={self.token_type_table.getTokenType(state=state).strip()}, token_value={lexeme.strip()} ===============")
            return Token(token_type=self.token_type_table.getTokenType(state=state).strip(), token_value=lexeme.strip()) 
        else:
            logging.debug("=============== Returning None ===============")
            return None
