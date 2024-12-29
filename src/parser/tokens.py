# Represents Lexical Token
class Token:

    def __init__(self, name: str, attribute_value: str):
        self.name = name.strip()
        self.attribute_value = attribute_value.strip()

    def get_name(self):
        return self.name
    
    def get_attribute(self):
        return self.attribute_value
    
    def parse_tag(self):
        return self.attribute_value.replace("</", "").replace("<", "").replace(">", "")

    

