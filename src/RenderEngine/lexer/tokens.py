# Represents Lexical Token
class Token:

    def __init__(self, token_type: str, token_value: str):
        if token_type == "space":
            self.token_type = token_type
            self.token_value = token_value
        else:
            self.token_type = token_type.strip()
            self.token_value = token_value.strip()

    def get_token_type(self):
        return self.token_type
    
    def get_token_value(self):
        return self.token_value
    
    def parse_tag(self):
        return self.token_value.replace("</", "").replace("<", "").replace(">", "")

    

