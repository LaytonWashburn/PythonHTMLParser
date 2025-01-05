"""
    Python File: css_nodes.py
    Purpose: Provide class to create structure for the CSSOM
    Notes: Definitions are ordered from specific to general
"""

from __future__ import annotations # Must be at beginning of file
from DOM.parser.node import Node
import logging

'''
    Class: CSSStyleDeclaration
    Purpose: Provide a collection of properties, values, and corresponding/appropriate methods
    Dependencies: 
    Notes: 
'''
class CSSStyeDeclaration:

    def __init__(self):
        self.style_declarations = {}

    def set_style_declaration(self, style_declaration:str):
        key, value = style_declaration.split(":") # Split the style on colon
        key = key.strip() # Strip whitespace from either side of the key
        value = value.replace(";", "", 1) # Replace the semi colon at the end of the css rule
        self.style_declarations[key] =  value

    def set_style_declarations(self, style_declarations:dict):
        self.style_declarations = style_declarations
    
    def get_styles(self) -> dict:
        return self.style_declarations


'''
    Class: CSSRule
    Purpose: Provide an object to hold StyleDeclarations and corresponding/appropriate methods
    Dependencies: CSSStyleDeclaration(Class)
    Notes:
'''
class CSSRule:

    def __init__(self):
        self.style_declaration = None
        self.css_text:str = "" # string with the entire rule set
        self.parent_rule:CSSRule = None 
        self.parent_style_sheet:CSSStyleSheet = None
        self.selector_text:str = None
        self.access_selector = None # # (id), . (class)
        self.style:CSSStyeDeclaration = CSSStyeDeclaration() # Collection of properties and values

    def add_declaration(self, style_declaration:str):
        self.style.set_style_declaration(style_declaration=style_declaration)
    
    def set_style_declaration(self, style_declaration:CSSStyeDeclaration):
        self.style_declaration = style_declaration
    
    def get_style_declaration(self):
        return self.style_declaration

    def set_css_text(self, css_text:str):
        self.css_text = css_text
    
    def get_css_text(self) -> str:
        return self.css_text
    
    def set_parent_rule(self, parent_rule:CSSRule): 
        self.parent_rule = parent_rule
    
    def get_parent_rule(self) -> CSSRule:
        return self.parent_rule

    def set_parent_style_sheet(self, parent_style_sheet:CSSStyleSheet):
        self.parent_style_sheet = parent_style_sheet
    
    def get_parent_sytle_sheet(self) -> CSSStyleSheet:
        return self.parent_style_sheet
    
    def set_selector_text(self, selector_text:str):
        self.selector_text = selector_text
    
    def get_selector_text(self):
        return self.selector_text
    
    def set_style(self, style:CSSStyeDeclaration):
        self.style = style

    def get_style(self) -> CSSStyeDeclaration:
        return self.style
    
    def set_access_selector(self, access_selector:str):
        self.access_selector = access_selector
    
    def get_access_selector(self):
        return self.access_selector

'''
    Class: CSSRuleList
    Purpose: Provide an object to hold all CSSRule objects and corresponding/appropriate methods
    Dependencies: CSSRule(Class)
    Notes:
'''
class CSSRuleList:

    def __init__(self):
        self.rule_list:list = []
    
    def add_rule(self, rule:CSSRule):
        self.rule_list.append(rule)
    
    def set_rule_list(self, rule_list):
        self.rule_list = rule_list
    
    def get_rule_list(self) -> list:
        return self.rule_list
'''
    Class: MediaList
    Purpose: 
    Dependencies: 
    Notes:
'''
# Not exactly sure what this is for
class MediaList:

    def __init__(self):
        pass


'''
    Class: CSSStyleSheet
    Purpose: Provide an object to hold CSSRuleList and corresponding/appropriate methods
    Dependencies: CSSRuleList(Class)
    Notes:
'''
class CSSStyleSheet:

    def __init__(self, name:str):
        self.css_rule_list:CSSRuleList = None
        self.disabled:bool = True
        self.href:str = None
        self.media:MediaList = None
        self.owner_node:Node = None
        self.parent_style_sheet:CSSStyleSheet = None
        self.rules:CSSRuleList = None # Identical to the css.rule_list
        self.title:str = None # Title of the node in the stylesheet
        self.type:str = None # Type of styles
        self.selector_look_up:dict = {} # Look up table for O(1) search
        # self.name = name
        # self.parent = None
    
    def set_rule_list(self, rule_list:CSSRuleList):
        self.css_rule_list = rule_list
        # self.css_rule_list.add_rule(rule_list)
    
    def get_rule_list(self):
        return self.css_rule_list

    def set_disabled(self, boolean:bool):
        self.disabled = boolean

    def get_disabled(self):
        return self.disabled

    def set_href(self, href:str):
        self.href = href
    
    def get_href(self):
        return self.href

    def set_media(self, media:MediaList):
        self.media = media
    
    def get_media(self):
        return self.media

    def set_owner_node(self, owner_node:Node):
        self.owner_node = owner_node
    
    def get_owner_node(self):
        return self.owner_node

    def set_parent_style_sheet(self, parent_style_sheet):
        self.parent_style_sheet = parent_style_sheet
    
    def get_parent_style_sheet(self):
        return self.parent_style_sheet

    def set_rules(self, rules:CSSRuleList):
        self.rules = rules
    
    def get_rules(self):
        return self.rules

    def set_title(self, title:str):
        self.title = title
    
    def get_title(self):
        return self.title
    
    def set_type(self, type:str):
        self.type = type
    
    def get_type(self):
        return self.type
    
    def set_selector_look_up(self, key:str, value:str):
        if  key in self.selector_look_up:
            logging.debug(f"=============== Overriding Current Selector: {key} ===============")
            self.selector_look_up[key] = value
        else:
            logging.debug(f"=============== Setting Current Selector: {key} ===============")
            self.selector_look_up[key] = value
            
    def get_selector_look_up(self) -> dict:
        return self.selector_look_up
    
    def look_up_selector(self, selector:str) -> str | None:
        return self.selector_look_up.get(selector, None)

    # def set_name(self, name:str):
    #     self.name = name
    
    # def get_name(self):
    #     return self.name


'''
    Class: DocumentStyleSheets
    Purpose: Provide an object to hold all CSSStyleSheet objects and corresponding/appropriate methods
    Dependencies: CSSStyleSheet(Class)
    Notes: This is the root, can be the only root, and only one instance of this class
'''
class DocumentStyleSheet:

    instance_count = 0 # Global instance count

    def __init__(self):

        # Prevent more than one instantiation of the class
        if DocumentStyleSheet.instance_count >= 1:
            raise Exception("Cannot create more instances of class DocumentStyleSheets")
        
        self.css_style_sheets:list[CSSStyleSheet] = [] # Container to hold all style sheets

        DocumentStyleSheet.instance_count += 1

        print("=============== Created Document Style Sheet ===============")

    def add_style_sheet(self, style_sheet:CSSStyleSheet):
        self.css_style_sheets.append(style_sheet)
    
    def get_style_sheets(self):
        return self.css_style_sheets
    