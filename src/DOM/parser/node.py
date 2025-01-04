class Node:

    def __init__(self):
        self.tag_type = None # 'Start' or 'End'
        self.open_tag = None # <
        self.close_tag = None # >
        self.tag_name = None # example: body
        self.tag = None
        self.attributes = {}
        self.content = None
        self.styles = {}
        self.parent = None
        self.self_closing_tag = False
        self.children = []
    
    def add_child(self, node):
        self.children.append(node)
    
    def get_children(self):
        return self.children
    
    def set_parent(self, node):
        self.parent = node
    
    def get_parent(self):
        return self.parent

    def set_attribute(self, key:str, value:str):
        self.attributes[key] = value
    
    def get_attributes(self):
        return self.attributes
    
    def get_attribute(self, key:str):
        return self.attributes.get(key, None)

    def set_tag_type(self, tag_type:str):
        self.tag_type = tag_type
    
    def set_open_tag(self, open_tag:str):
        self.open_tag = open_tag

    def get_open_tag(self):
        return self.open_tag
    
    def set_close_tag(self, close_tag:str):
        self.close_tag = close_tag
    
    def get_close_tag(self):
        return self.close_tag

    def get_tag_name(self):
        return self.tag_name
    
    def set_tag_name(self, tag_name:str):
        self.tag_name = tag_name
    
    def get_tag(self):
        return self.tag

    def set_tag(self, tag:str):
        self.tag = tag
    
    def set_content(self, content:str):
        self.content = content

    def get_content(self):
        return self.content
    
    def set_styles(self, key:str, value:str):
        self.styles[key] = value

    def get_style(self, key):
        if self.styles.get(key) is None:
            return None
        self.styles[key]

    def set_self_closing_tag_true(self):
        self.self_closing_tag = True
    
    def set_self_closing_tag_false(self):
        self.self_closing_tag = False
    
    def get_self_closing_tag(self):
        return self.self_closing_tag