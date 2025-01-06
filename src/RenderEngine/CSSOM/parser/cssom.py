from RenderEngine.tables.tables import ClassifierTable, Transitiontable, TokenTypeTable
from RenderEngine.lexer.tokens import Token
from RenderEngine.CSSOM.parser.css_nodes import (CSSStyeDeclaration, 
                                    CSSRule, 
                                    CSSRuleList, 
                                    MediaList, 
                                    CSSStyleSheet, 
                                    DocumentStyleSheet)
import logging 

class CSSOM:

    def __init__(self, tokens:list = None):
        self.tokens = tokens
        self.eof_tokens = False
        self.token_index:int = 0
        self.current_sheet:CSSStyleSheet = None
        self.current_rule_list:CSSRuleList = None
        self.current_rule:CSSRule = None
        self.root = DocumentStyleSheet()
        self.classifier_table:ClassifierTable = ClassifierTable('src/RenderEngine/tables/classifier_table.csv')
        self.token_type_table:TokenTypeTable = TokenTypeTable('src/RenderEngine/tables/css/parser_token_type_table.csv')
        self.transition_table:Transitiontable = Transitiontable('src/RenderEngine/tables/css/parser_transition_table.csv')
    
    def get_root(self):
        return self.root

    def get_document_style_sheets(self):
        return self.root
    
    # This method will need revision to account for css rule precedence
    def get_document_styles(self):
        sheets = self.root.get_style_sheets()
        curr_dict = {}
        # Can I do this in a more advanced way
        for sheet in sheets:
            curr_dict.update(sheet.get_selector_look_up())

        print(f"=============== Returning dict: {curr_dict} ===============")
        return curr_dict

    def set_current_sheet(self, current_sheet:CSSStyleSheet):
        self.current_sheet = current_sheet
    
    def get_current_sheet(self) -> CSSStyleSheet:
        return self.current_sheet
    
    def set_current_rule_list(self, current_rule_list:CSSRuleList):
        self.current_rule_list = current_rule_list
    
    def get_current_rule_list(self) -> CSSRuleList:
        return self.current_rule_list

    def set_current_rule(self, current_rule:CSSRule):
        self.current_rule = current_rule
    
    def get_current_rule(self) -> CSSRule:
        return self.current_rule

    def set_tokens(self, tokens:list):
        self,tokens = tokens

    def get_tokens(self):
        return self.tokens
    
    def print_tokens(self):
        logging.debug("=============== Started Printing Tokens ===============")
        for token in self.tokens:
            logging.debug(f"Token: {token.get_token_type()} : {token.get_token_value()}")
        logging.debug("=============== Finished Printing Tokens ===============")

    def rollback(self):
        if self.token_index == 0:
            self.token_index = 0
        self.token_index -= 1

    def truncate(self, lexeme:str, remove:str):
        if len(lexeme) == 0 or lexeme is None or lexeme == "":
            return ""
        return lexeme.removesuffix(remove)
    
    def get_next_token(self):
        if self.token_index < len(self.tokens):
            index = self.token_index
            self.token_index += 1
            return self.tokens[index]
        return None
    
    # Build the DOM by iterating through the tokens
    def next_rule(self) -> Token:

        logging.debug("=============== Getting Next Rule ===============")
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
                logging.debug(e)
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
        _debug = self.token_type_table.getTokenType(state=state)
        while _debug is None and state != "bad":
            state = stack.pop() # Pop the stack and set result as the new state
            _debug = self.token_type_table.getTokenType(state=state)

        # Try to remove the last character from lexeme and rollback the ss iterator or throw an exception and continue
        try: 
            
            if curr is not None:   
                lexeme = self.truncate(lexeme=lexeme, remove=curr.get_token_value() )
                self.rollback() 

        except Exception as e:
            logging.debug("Printing error in Exception")
            logging.debug(f"An error occurred: {e}")

        # If an accept state return a Token with the type and lexeme or return error
        _temp = self.token_type_table.getTokenType(state=state)
        if _temp is not None and state != "bad":
            logging.debug(f"=============== Returning Rule : token_type={self.token_type_table.getTokenType(state=state).strip()}, token_value={lexeme.strip()} ===============")
            return Token(token_type=self.token_type_table.getTokenType(state=state).strip(), token_value=lexeme.strip()) 
        else:
            logging.debug("=============== Returning None Rule ===============")
            return None


    def build(self):
        logging.debug("=============== Building CSSOM ===============")
        while self.eof_tokens is False:
            token = self.next_rule()
            _type = token.get_token_type()
            value = token.get_token_value()

            if token is None:
                raise Exception(f" =============== Error in CSS parsing ===============")
            
            # Checks
            if self.current_sheet is None:
                raise Exception(f"=============== No Active Sheet Available ===============")
            else:
                if self.current_rule_list is None:
                    logging.debug("=============== No Current Rule List Available, Creating One ===============")
                    rule_list = CSSRuleList()
                    self.set_current_rule_list(current_rule_list=rule_list)
                    self.current_sheet.set_rule_list(self.current_rule_list)
                else:
                    pass
                if self.current_rule is None:
                    logging.debug("=============== No Current Rule Available, Creating One ===============")
                    rule = CSSRule()
                    self.set_current_rule(current_rule=rule) # Set current rule
                    self.current_rule_list.add_rule(self.current_rule) # Add current rule to rule list
            
            # Add the current token's value to the css_text of the current rule
            css_text = self.current_rule.get_css_text()
            self.current_rule.set_css_text(css_text=(css_text + value))

            # Figure Out what to do with each token
            if _type == "access_selector": # Add the access to the rule
                self.current_rule.set_access_selector(access_selector=value)

            elif _type == "selector": # Set the current rule's name
                self.current_rule.set_selector_text(selector_text=value)

            elif _type == "colon":
                pass

            elif _type == "declaration":
                self.current_rule.add_declaration(style_declaration=value)

            elif _type == "start_declaration_block":
                pass

            elif _type == "end_rule":
                # Set selector lookup for selector and the rule
                _selector = "" if self.current_rule.get_access_selector() is None else self.current_rule.get_access_selector()
                _selector += self.current_rule.get_selector_text()
                self.current_sheet.set_selector_look_up(key=_selector, value=self.current_rule)

                self.current_rule = None # Set to None
            else:
                logging.debug("=============== No Tag Recognized ===============")
        logging.debug("=============== Finished Building the CCSOM ===============")


