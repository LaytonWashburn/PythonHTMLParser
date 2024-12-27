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
            return ""
        return string[:-1]

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


        while current != "EOF": 
            logging.debug("=============== STARTING INTERATION ===============")
            logging.debug(f"Current State: {state}")
            logging.debug(f"Current Character: {current}")
            logging.debug(f"Current lexeme: {lexeme}")
            if current is None:
                current = "EOF"
                lexeme = self.stream_reader.truncate(lexeme)
                self.add(token_type="END_STRING", lexeme=lexeme)
                self.add(token_type="CLOSE_TAG", lexeme=">")
                continue
            token_type = self.token_type_table.getTokenType(state=state)
            if token_type is not None:
                logging.debug("In the Accept")
                if token_type == "END_STRING":
                    logging.debug("In END STRING")
                    lexeme = self.stream_reader.truncate(lexeme)
                    self.add(token_type=token_type, lexeme=lexeme)
                    self.stream_reader.rollback()
                    self.stream_reader.rollback()
                    state = "START"
                    lexeme = ""
                    current = self.stream_reader.next()
                    continue
                elif token_type == "OPEN_TAG":
                    logging.debug("In the OPEN TAG")
                    if current == "/":
                        logging.debug("In the LOOKAHEAD")
                        self.add(token_type=token_type, lexeme=lexeme + current)
                        current = self.stream_reader.next() # Consume the lookahead "/"
                        state = "START"
                        lexeme = ""
                        continue
                    else:
                        logging.debug("In the ELSE")
                        self.add(token_type=token_type, lexeme=lexeme)
                        state = "START"
                        lexeme = ""
                else:
                    logging.debug("Not an accept state")
                    self.add(token_type=token_type, lexeme=lexeme)
                    lexeme = ""
                    state = "START"

            lexeme += current
            state = self.transition_table.getTransition(state=state, transition=self.classifier_table.getClassification(current))
            current = self.stream_reader.next()

            logging.debug(f"New lexeme: {lexeme}")
            logging.debug(f"New State: {state}")
            logging.debug(f"New Character: {current}")
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




