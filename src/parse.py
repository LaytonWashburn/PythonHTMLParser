# Algorithm
'''
        state = "s0"
        lexeme = " "
        # clear stack;
        # push(bad)

        # while(state not equal to error state (s_e))
        # NextChar(Char);
        # lexeme <- lexeme + char

        # if state in accept State (S_A)
            # then clear stack;
        # push(state);

        # cat <- CharCat[char];
        # state <- S[state.cat];

        # end

        # while(state not in Accept state (S_A) and state not equal-to bad) do
        # state <- pop()
        # truncate lexeme;
        # Rollback();
        # end

        # if state in Accept state (S_A)
        # then return Type[state];
        # else return invalid
'''

import tokens as T
import tables

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

    def rollback(self):
        if self.index == 0:
            return 0
        self.index = self.index - 1
    
    def truncate(self, string:str):
        if len(string) == 0:
            return ""
        return string[:-1], string[len(string)-1]

class Parser:
    def __init__(self, html: str):
        self.html = html.replace("\n", "")#.replace(" ", "")
        self.tokens = []
        self.classifier_table = tables.ClassifierTable('src/classifier_table.csv')
        self.transition_table = tables.Transitiontable('src/transition_table.csv')
        self.token_type_table = tables.TokenTypeTable('src/token_type_table.csv')
        self.dom = T.DOM()
        self.stream_reader = StreamReader(self.html)
    


    def build_token_list(self):

        state = "START" # Set initial state to start
        lexeme = "" # Set the lexeme to empty string
        current = self.stream_reader.next() # Get the first character

        while current != "END":

            # print("=============== STARTING INTERATION ===============")
            # print(f"Current character: {current}")
            # print(f"Current state: {state}")
            # print(f"Current lexeme: {lexeme}")
                

            token_type = self.token_type_table.getTokenType(state=state)

            if token_type is not None:

                if token_type == "ATTRIBUTE":
                    # print(f"Token Type: Attribute")
                    lexeme, old_char = self.stream_reader.truncate(lexeme)
                    # print(f"Lexeme is: {lexeme}")
                    # print(f"Old char: {old_char}")
                    # print(f"The old index is: {self.stream_reader.index}")
                    self.stream_reader.rollback()
                    # print(f"The new index is: {self.stream_reader.index}")

                    self.tokens.append(T.Token(name=self.token_type_table.getTokenType(state=state), 
                                                attribute_value=lexeme))
                    lexeme = ""
                    current = old_char
                    # print(f"Setting current to: {current}")

                elif current == None:
                    self.tokens.append(T.Token(name=self.token_type_table.getTokenType(state=state), 
                                               attribute_value=lexeme))
                    current = "END"
                    continue
                else:
                    self.tokens.append(T.Token(name=self.token_type_table.getTokenType(state=state), 
                                               attribute_value=lexeme))
                    lexeme = ""
                    state = "START"

            lexeme += current # Update the lexeme

            # Update the state : get the new state from the transition table
            state = self.transition_table.getTransition(state=state, transition=self.classifier_table.getClassification(current))
        
            current = self.stream_reader.next() # Get next character

            # print(f"New character: {current}")
            # print(f"New state: {state}")
            # print(f"New lexeme: {lexeme}")
            # print("=============== ENDING INTERATION ===============")



            
    def get_tokens(self) -> list:
        return self.tokens

# Main Method for the Parser
    def parse(self):
        self.build_token_list()
    
    def clear_parser(self):
        self.tokens = []

