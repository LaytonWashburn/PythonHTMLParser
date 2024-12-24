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

class Parser:
    def __init__(self, html: str):
        self.html = html.replace(" ", "").replace("\n", "")
        self.tokens = list()
        self.classifier_table = tables.ClassifierTable('src/classifier_table.csv')
        self.transition_table = tables.Transitiontable('src/transition_table.csv')
        self.token_type_table = tables.TokenTypeTable('src/token_type_table.csv')
        self.dom = T.DOM()

    def build_token_list(self) -> T.Token:
        state = "s0"
        lexeme = ""
        for char in self.html:
            print(f'Current: {char}')

            # Check if in the accept state
            if self.token_type_table.getTokenType(state=state) is not None:
                self.tokens.append(T.Token("Tag", lexeme, self.dom))
                state = "s0"
                lexeme = ""
                continue

            state = self.transition_table.getTransition(state=state, transition=self.classifier_table.getClassification(char))
            print(f'New State is: {state}')
            lexeme += char
            print(lexeme)

            # Check if in the accept state
            if self.token_type_table.getTokenType(state=state) is not None:
                self.tokens.append(T.Token("Tag", lexeme, self.dom))
                state = "s0"
                lexeme = ""
                continue

            
    def get_tokens(self) -> list:
        return self.tokens

# Main Method for the Parser
    def parse(self):
        self.build_token_list()
    
    def clear_parser(self):
        self.tokens = list()