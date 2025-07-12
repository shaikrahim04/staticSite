from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Please Override")
    
    def props_to_html(self):
        if isinstance(self.props, dict):
            ans = ""
            for key, value in self.props.items():
                ans += f' {key}=\"{value}\"'

            return ans
        elif self.props is None:
            return ""
        raise ValueError(f"Excepting Dict type received {type(self.props)}")
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        return (self.children == other.children and self.props == other.props
                and self.tag == other.tag and self.value == other.value)
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value Cannot be None")
        
        if self.tag is None:
            return f'{self.value}'
        
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
            

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is Mandatory")
        
        if self.children is None:
            raise ValueError("ParentNode should contain atleast 1 children node.")
        
        return f'<{self.tag}{self.props_to_html()}>{"".join([child_tag.to_html() for child_tag in self.children])}</{self.tag}>'

def text_node_to_html_node(text_node):
    if isinstance(text_node, TextNode):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
        else:
            raise ValueError(f"Unhandled TextType: {text_node.text_type}")
    else:
        raise ValueError(f"Expecting type TextNode but received {type(text_node)}")
            