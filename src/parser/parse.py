import parser.tokens as tokens
import parser.tables as tables
import logging

# Configure logging
logging.basicConfig(level=logging.INFO) # Change this to INFO to not have the debug and DEBUG for debugging

class StreamReader:
    def __init__(self, data:str):
        self.data = data
        self.index = 0
    
    def next(self):
        if self.index < len(self.data):
            char = self.data[self.index]
            self.index += 1
            return char
        return None
    
    def lookahead(self):
        if self.index < len(self.data):
            char = self.data[self.index]
            return char
        return None

    def rollback(self):
        if self.index == 0:
            return 0
        self.index = self.index - 1
    
    def truncate(self, string:str):
        if len(string) == 0 or string is None or string == "":
            return "", ""
        return string[:-1], string[len(string)-1]

class Parser:
    def __init__(self, html: str):
        self.html = html.replace("\n", "")
        self.tokens = []
        self.classifier_table = tables.ClassifierTable('src/tables/classifier_table.csv')
        self.transition_table = tables.Transitiontable('src/tables/transition_table_new.csv')
        self.token_type_table = tables.TokenTypeTable('src/tables/token_type_table_new.csv')
        self.dom = None
        self.stream_reader = StreamReader(self.html)
    
    def add(self, token_type:str, lexeme:str):
        logging.debug(f"Adding token to list: token_type={token_type}, lexeme={lexeme}")
        self.tokens.append(tokens.Token(name=token_type, attribute_value=lexeme))

    # Rollback on END_TAG_NAME, 
    def build_token_list(self):

        state = "START" # Set initial state to start
        lexeme = "" # Set the lexeme to empty string
        current = self.stream_reader.next() # Get the first character
        lookahead = self.stream_reader.lookahead() # Get the lookahead
        lookahead_type = self.classifier_table.getClassification(lookahead)
        token_type = self.token_type_table.getTokenType(state=state)
        while current != "EOF":
            logging.debug("=============== STARTING INTERATION ===============")
            logging.debug(f"Token Type: {token_type}")
            logging.debug(f"Current Character: {current}")
            logging.debug(f"Current Character_Type: {self.classifier_table.getClassification(current)}")
            logging.debug(f"Current lookahead: {lookahead}")
            logging.debug(f"Current lookahead_type: {lookahead_type}")
            logging.debug(f"Current State: {state}")
            logging.debug(f"Current lexeme: {lexeme}")
            token_type = self.token_type_table.getTokenType(state=state)

            if current is None:
                lexeme, old_char = self.stream_reader.truncate(lexeme)
                self.add(token_type=token_type, lexeme=lexeme)
                self.add(token_type="IDK", lexeme=old_char)
                current = "EOF"
                break

            if token_type is not None: # If the state is an accept state
                logging.debug("In Accept")

                if self.classifier_table.getClassification(current) == "open_brace" and lookahead == self.classifier_table.getClassification("/"):
                    logging.debug("In the </ TAG")
                    logging.debug(f"Truncated parameter: {lexeme}")
                    lexeme, old_char = self.stream_reader.truncate(lexeme)
                    logging.debug(f"Truncated results are: {lexeme} and {old_char}")
                    self.add(token_type=token_type, lexeme=lexeme)
                    self.add(token_type="IDK", lexeme=old_char)
                    self.stream_reader.rollback()
                    lexeme = current + lookahead # Make the </ token
                    logging.debug(f"Lexeme: {lexeme}")
                    self.add(token_type=token_type, lexeme=lexeme)
                    self.stream_reader.next()
                    self.stream_reader.next()
                    current = self.stream_reader.next()
                    lookahead = self.stream_reader.lookahead()
                    lookahead_type = self.classifier_table.getClassification(lookahead_type)
                    lexeme = ""
                    state = "START"

                elif token_type == "END_CONTENT" and current == "/":
                    logging.debug("In the END_CONTENT </ TAG")
                    logging.debug(f"Truncated parameter: {lexeme}")
                    lexeme, old_char = self.stream_reader.truncate(lexeme)
                    logging.debug(f"Truncated results are: {lexeme} and {old_char}")
                    self.add(token_type=token_type, lexeme=lexeme)
                    self.add(token_type="IDK", lexeme=old_char+current)
                    self.stream_reader.rollback()
                    lexeme = lookahead # Make the </ token
                    logging.debug(f"Lexeme: {lexeme}")
                    self.add(token_type=token_type, lexeme=lexeme)
                    self.stream_reader.next()
                    self.stream_reader.next()
                    current = self.stream_reader.next()
                    lookahead = self.stream_reader.lookahead()
                    lookahead_type = self.classifier_table.getClassification(lookahead_type)
                    lexeme = ""
                    state = "START"

                elif token_type == "END_CONTENT":
                    logging.debug("In the END_CONTENT")
                    logging.debug(f"Truncated parameter: {lexeme}")
                    lexeme, old_char = self.stream_reader.truncate(lexeme)
                    logging.debug(f"Truncated results are: {lexeme} and {old_char}")
                    self.add(token_type=token_type,lexeme=lexeme)
                    self.stream_reader.rollback()
                    state = "START"
                    lexeme = ""
                    current = old_char

                else:
                    logging.debug("In the else")
                    self.add(token_type=token_type, lexeme=lexeme)
                    lexeme = ""
                    state = "START"
                
            else:
                logging.debug("Not an Accept State")
                
                # Get the new state, current character, lookahead, and update lexeme,
                lexeme += current
                transition = self.classifier_table.getClassification(current)
                current = self.stream_reader.next()
                state = self.transition_table.getTransition(state=state,transition=transition)
                lookahead = self.stream_reader.lookahead()
                lookahead_type = self.classifier_table.getClassification(lookahead)

            logging.debug(f"New character: {current}")
            logging.debug(f"New state: {state}")
            logging.debug(f"New lexeme: {lexeme}")
            logging.debug(f"Current lookahead: {lookahead}")
            logging.debug(f"Current lookahead_type: {lookahead_type}")
            logging.debug("=============== ENDING INTERATION ===============")


    def get_tokens(self) -> list:
        return self.tokens

    def print_tokens(self) -> None:
        logging.debug("=============== PRINTING TOKEN INFORMATION ===============")
        for token in self.tokens:
            logging.debug(f"Token: {token.get_name()} : {token.get_attribute()}")
    # Main Method for the Parser
    def parse(self):
        self.build_token_list()
        # self.dom = tokens.DOM(self.tokens)
        # self.dom.build()
        # self.dom.get_dom()
    
    def clear_parser(self):
        self.tokens = []




        # state = "START" # Set initial state to start
        # lexeme = "" # Set the lexeme to empty string
        # current = self.stream_reader.next() # Get the first character

        # while current != "END":

        #     logging.debug("=============== STARTING INTERATION ===============")
        #     logging.debug(f"Current character: {current}")
        #     logging.debug(f"Current state: {state}")
        #     logging.debug(f"Current lexeme: {lexeme}")
                
        #     token_type = self.token_type_table.getTokenType(state=state)

        #     if token_type is not None: # If the state is an accept state

        #         if token_type == "ATTRIBUTE":
        #             logging.debug(f"Token Type: Attribute")
        #             lexeme, old_char = self.stream_reader.truncate(lexeme) # Remove the last character and return new lexeme and removed character
        #             logging.debug(f"Lexeme is: {lexeme}")
        #             logging.debug(f"Old char: {old_char}")
        #             logging.debug(f"The old index is: {self.stream_reader.index}")
        #             self.stream_reader.rollback() # Move the stream reader's index back one
        #             logging.debug(f"The new index is: {self.stream_reader.index}")

        #             self.tokens.append(tokens.Token(name=self.token_type_table.getTokenType(state=state), 
        #                                         attribute_value=lexeme))
        #             lexeme = ""
        #             current = old_char
        #             logging.debug(f"Setting current to: {current}")

        #         elif current == None:
        #             self.tokens.append(tokens.Token(name=self.token_type_table.getTokenType(state=state), 
        #                                        attribute_value=lexeme))
        #             current = "END"
        #             logging.debug("=============== ENDING INTERATION ===============")
        #             continue # This will force the loop to the top and check the condition and then quit
        #         else:
        #             self.tokens.append(tokens.Token(name=self.token_type_table.getTokenType(state=state), 
        #                                        attribute_value=lexeme))
        #             lexeme = ""
        #             state = "START"

        #     lexeme += current # Update the lexeme

        #     # Update the state : get the new state from the transition table
        #     state = self.transition_table.getTransition(state=state, transition=self.classifier_table.getClassification(current))
        
        #     current = self.stream_reader.next() # Get next character

        #     logging.debug(f"New character: {current}")
        #     logging.debug(f"New state: {state}")
        #     logging.debug(f"New lexeme: {lexeme}")
        #     logging.debug("=============== ENDING INTERATION ===============")