from enum import Enum

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold Text"
    ITALIC = "Italic Text"
    CODE = "Code Text"
    LINK = "Link"
    IMAGE = "Images"


class TextNode():

    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type if isinstance(text_type, TextType) else TextType[text_type]
        self.url = url

    def __eq__(self, other):
        if( self.text == other.text and 
           self.text_type == other.text_type and 
           self.url == other.url ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

        

