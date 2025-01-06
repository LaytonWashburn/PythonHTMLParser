from RenderEngine.lexer.tokens import Token
from RenderEngine.tables.tables import ClassifierTable, Transitiontable, TokenTypeTable
from RenderEngine.lexer.stream_reader import StreamReader
import logging


class Lexer:
    def __init__(self, classifier:str, transition:str, token_type:str, data=None, current_file_name=None):
        self.data = data
        self.tokens = []
        self.classifier_table = ClassifierTable(classifier)
        self.transition_table = Transitiontable(transition)
        self.token_type_table = TokenTypeTable(token_type)
        self.stream_reader = None if self.data is None else StreamReader(data=self.data.replace("\n", ""))
        self.dom = None
        self.current_file_name:str = current_file_name

    def set_current_file_name(self, current_file_name:str):
        self.current_file_name = current_file_name
    
    def get_current_file_name(self):
        return self.current_file_name

    def set_data(self, data:str):
        self.data = data.replace("\n", "")
        self.stream_reader = StreamReader(data=self.data)


    def read_data(self, file_path:str):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = file.read()
        self.current_file_name = file_path
        self.data = self.data.replace('\n', '')
        self.stream_reader = StreamReader(data=self.data)


    def get_data(self):
        return self.data
    
    def add(self, token:Token):
        logging.debug(f"Adding token to list: token_type={token.get_token_type()}, lexeme={token.get_token_value()}")
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
        stack = []
        curr = 0
        cat = None
        state = "START"
        lexeme = ""

        # Clear stack and push "bad" to the stack
        stack.append("bad")

        # While not in the error state
        while state != None: # state.compareTo("error") != 0){
            try:
                curr = self.stream_reader.next(); # This throws an eof error // Gets the next character
                if curr is None:
                    self.stream_reader.set_eof(True)
                    
            except Exception as e:
                state = None # "error" # This might need to be none
                curr = 0
        
            if curr is not None: # Append curr to the end of lexeme
                lexeme += curr; 
            else:
                lexeme += " " # End of File Space to be able to rollback

            # If an accept state clear stack
            if self.token_type_table.getTokenType(state=state) is not None:
                stack.clear()
            

            stack.append(state); # Push state onto stack

            cat = self.classifier_table.getClassification(curr) # Get the current character's Category
            state = self.transition_table.getTransition(state=state, transition=cat) # Get the new State from the TransitionTable given the current state and cat

        # While not an accept state and state is not "bad"
        while self.token_type_table.getTokenType(state=state) is None and state != "bad":
            state = stack.pop() # Pop the stack and set result as the new state

        # Try to remove the last character from lexeme and rollback the ss iterator or throw an exception and continue
        try:
            lexeme = self.stream_reader.truncate(string=lexeme)
            self.stream_reader.rollback() 
        except Exception as e:
            print(f"An error occurred: {e}")

        # If an accept state return a Token with the type and lexeme or return error
        if self.token_type_table.getTokenType(state=state) is not None and state != "bad":
            logging.debug("=============== Returning Token ===============")
            return Token(token_type=self.token_type_table.getTokenType(state=state), token_value=lexeme) # new Token(getTokenType(state), lexeme)
        else:
            logging.debug("=============== Returning None ===============")
            return None

    def get_tokens(self) -> list:
        return self.tokens


    def print_tokens(self) -> None:
        logging.debug("=============== PRINTING TOKEN INFORMATION ===============")
        for token in self.tokens:
            logging.debug(f"Token: {token.get_token_type()} : {token.get_token_value()}")

    # Main Method for the Parser
    def scan(self):
        self.build_token_list()
    
    def clear_tokens(self):
        self.tokens = []




