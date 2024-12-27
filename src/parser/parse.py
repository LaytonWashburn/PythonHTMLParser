from parser.tokens import Token
from parser.tables import ClassifierTable, Transitiontable, TokenTypeTable
from parser.scan_stream import StreamReader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO) # Change this to INFO to not have the debug and DEBUG for debugging

class Parser:
    def __init__(self, html: str):
        self.html = html.replace("\n", "")
        self.tokens = []
        self.classifier_table = ClassifierTable('src/tables/classifier_table.csv')
        self.transition_table = Transitiontable('src/tables/transition_table_new.csv')
        self.token_type_table = TokenTypeTable('src/tables/token_type_table_new.csv')
        self.stream_reader = StreamReader(self.html)
        self.dom = None
    
    def add(self, token:Token):
        logging.debug(f"Adding token to list: token_type={token.get_name()}, lexeme={token.get_attribute()}")
        self.tokens.append(token)


    # Build token list from inputted html
    def build_token_list(self):
        logging.debug("=============== Building Token List ===============")
        while not self.stream_reader.eof:
            token:Token|None = self.next_token()
            if token is not None:
                self.add(token)
        logging.debug("=============== Finished Building Token List ===============")

    """
        Method: next_token
        Purpose:
        Notes: 
            + None is the error state
    """
    def next_token(self):
        logging.debug("=============== Getting Next Token ===============")
        state = "START" # Set initial state to start
        lexeme = "" # Set the lexeme to empty string
        current = "" # Get the first character
        category = ""
        stack = []

        stack.append("bad")

        while state is not None:
            try:
                current = self.stream_reader.next()
            except Exception as e:
                state = None
                current = ""
                logging.error(f"Error Occurred: {e}")
            if current is not None:
                lexeme += current # Append current character to the lexeme
            else:
                self.stream_reader.set_eof(True)
                break
            if self.token_type_table.getTokenType(state=state) is not None:
                stack.clear()
            
            stack.append(state) # Push current state onto stack
            category = self.classifier_table.getClassification(character=current) #getCategory(curr); // Get the current character's Category
            state = self.transition_table.getTransition(state=state, transition=category) # getNewState(state, cat); // Get the new State from the TransitionTable given the current state and cat

        while self.token_type_table.getTokenType(state=state) is None and state != "bad":
            if current is None and self.stream_reader.lookahead() is None:
                self.stream_reader.set_eof(True)
                if state == "STRING":
                    state = "END_STRING"
                    logging.debug("=============== Returning Token ===============")
                    return Token(name=self.token_type_table.getTokenType(state=state), attribute_value=lexeme)
                break
            state = stack.pop()
            try:
                lexeme = self.stream_reader.truncate(lexeme)
                self.stream_reader.rollback()
                self.stream_reader.set_eof(False) # This might break it
            except Exception as e:
                logging.error(f"Error Occurred: {e}")

        if self.token_type_table.getTokenType(state=state) is not None and state != "bad":
            if current is None and self.stream_reader.lookahead() is None:
                self.stream_reader.set_eof(True)
            logging.debug("=============== Returning Token ===============")
            if self.token_type_table.getTokenType(state=state) == "END_STRING":
                lexeme = self.stream_reader.truncate(lexeme)
                self.stream_reader.rollback()
                if current is not None or self.stream_reader.lookahead() is not None:
                    self.stream_reader.set_eof(False)
            if self.token_type_table.getTokenType(state=state) == "OPEN_TAG" and current == "/":
                lexeme += current
                self.stream_reader.next() # Consume the "/"
            if self.token_type_table.getTokenType(state=state) == "CLOSE_TAG" and current is None:
                self.stream_reader.set_eof(True)
            return Token(name=self.token_type_table.getTokenType(state=state), attribute_value=lexeme)
        else:
            logging.debug("=============== Returning None Token ===============")
            return None

        

        
        



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




