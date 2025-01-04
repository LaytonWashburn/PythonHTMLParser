from lexer.tokens import Token
from DOM.parser.node import Node
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
        self.stylesheets = []
        self.void_elements = {"img":True, "br":True,"hr":True,"input":True,"link":True,"meta":True,
                              "area":True,"base":True,"col":True,"source":True,"track":True,"wbr":True}
        self.token_type_table:TokenTypeTable = TokenTypeTable('src/tables/html/parser_token_type_table.csv')
        self.transition_table:Transitiontable = Transitiontable('src/tables/html/parser_transition_table.csv')

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

    # Private method to iterate through the tree
    def _recurse_tree(self, node:Node, dom:str, tabs:int):

        dom += ('   ' * tabs)
        dom += ("<" + node.get_open_tag() + " ")

        for attribute in node.get_attributes().keys():
            dom += (node.get_attribute(key=attribute) + " ")

        dom += (">\n" if len(node.get_children()) else ">")
        dom += (('   ' * tabs) + node.get_content() + "\n" if node.get_content() is not None else "")
        for child in node.children:
            dom = self._recurse_tree(node=child, dom = dom, tabs=(tabs+1))

        dom += ('   ' * tabs)
        dom += ("</" + node.get_open_tag() + ">\n") if not node.get_self_closing_tag() else "\n"

        return dom

    def recurse_tree(self, dom:str, tabs:int):
        return self._recurse_tree(self.root, dom=dom, tabs=tabs)

    def build_dom_str(self) -> str:
        return self.recurse_tree(dom="", tabs=0)
        
    
    '''
        Method: process_tag
        Purpose: Process the start tag to pull the tag name and tag attributes out
    '''
    def process_tag(self, node:Node, value:str) -> Node:
        
        value_list:list = value.split() # Split on whitespace

        tag_name = value_list.pop(0)

        if self.void_elements.get(tag_name, False): # If in the void elements change boolean on node
            node.set_self_closing_tag_true()

        node.set_open_tag(open_tag=tag_name) # The first value should be the name

        attributes = [item.split('=') for item in value_list]
        
        for attribute in attributes:
            try:
                node.set_attribute(attribute[0], attribute[1])
            except Exception as e:
                print(f"Error occurred when setting attribute, {e}")

        return node
    
    def build(self):
        logging.debug("=============== Building DOM ===============")
        while self.eof_tokens is False:

            token = self.next_tag()
            _type = token.get_token_type()
            value = token.get_token_value()

            if token is None:
                raise Exception(f"Error in HTML parsing:")

            if _type == "close_start_tag":
                value = value.strip("<>") # Think about a different way todo this
                node = Node()
                node = self.process_tag(node=node, value=value)

                if self.root is None:
                    if node.get_self_closing_tag():
                        node.set_parent(self.current_node) # Set the node's parent
                        self.current_node.add_child(node=node) # Add node to current node's children list
                    else:
                        self.root = node
                        self.current_node = self.root

                elif node.get_self_closing_tag():
                    node.set_parent(self.current_node) # Set the node's parent
                    self.current_node.add_child(node=node) # Add node to current node's children list
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
                value = value.replace("</", "", 1).replace(">", "",1)
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
            logging.debug(f"=============== Returning Tag : token_type={self.token_type_table.getTokenType(state=state).strip()}, token_value={lexeme.strip()} ===============")
            return Token(token_type=self.token_type_table.getTokenType(state=state).strip(), token_value=lexeme.strip()) 
        else:
            logging.debug("=============== Returning None ===============")
            return None

    