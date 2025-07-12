from enum import Enum
from htmlnode import (ParentNode, LeafNode, text_node_to_html_node)
from textnode import (TextNode, TextType)
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARA = "ParaGraph"
    HEAD = "Heading"
    CODE = "Code Block"
    QUOTE = "Quote Block"
    U_LIST = "Unordered List"
    O_LIST = "Ordered List"


def markdown_to_blocks(markdown: str):
    blocks = []
    current_block = []
    
    for line in markdown.split('\n'):
        if line.strip():
            current_block.append(line)
        elif current_block:
            blocks.append('\n'.join(current_block))
            current_block = []
    
    if current_block:
        blocks.append('\n'.join(current_block))
    
    return [block.strip() for block in blocks if block.strip()]

def normalize_text(text):

    """Normalize text by removing extra whitespace and indentation"""

    lines = text.split('\n')

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()


    if lines:
        min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
        lines = [line[min_indent:] if line.strip() else line for line in lines]
    return ' '.join(line.strip() for line in lines)

def block_to_block_type(block):


    if block.startswith("#"):
        if any(block.startswith(h + " ") for h in ["#", "##", "###", "####", "#####", "######"]):
            return BlockType.HEAD
        return BlockType.PARA 
    
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    
    elif all(line.startswith(("* ", "- ")) for line in block.split("\n")):
        return BlockType.U_LIST
    
    elif all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == idx + 1 
            for idx, line in enumerate(block.split("\n"))):
        return BlockType.O_LIST
    
    else:
        return BlockType.PARA


def extract_heading_level(block):

    """Extract heading level from a heading block (e.g., # -> 1, ## -> 2)"""

    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    return level

def extract_text_content(block, block_type):

    """Extract the actual text content from different block types"""

    if block_type == BlockType.HEAD:
        return block.lstrip('#').strip()
    
    elif block_type == BlockType.CODE:


        lines = block.split('\n')

        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        

        if lines and lines[0].strip().startswith('```'):
            lines = lines[1:]

        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]


        if lines:
            indent_size = min(len(line) - len(line.lstrip()) 
                              for line in lines if line.strip())
            lines = [line[indent_size:] if line.strip() else '' for line in lines]
        
        return '\n'.join(lines) + '\n'
    
    elif block_type == BlockType.QUOTE:
        lines = [line.lstrip('>').strip() for line in block.split('\n')]
        return normalize_text('\n'.join(lines))
    
    elif block_type in [BlockType.U_LIST, BlockType.O_LIST]:
        lines = block.split('\n')
        items = []
        for line in lines:
            if '.' in line:
                items.append(line.split('. ', 1)[-1].strip())
            else:
                items.append(line.lstrip('- *').strip())
        return '\n'.join(items)
    
    return normalize_text(block)

def text_to_textnode(text):
    """Convert markdown text with inline formatting to TextNode"""

    if "**" in text:
        parts = text.split("**")
        if len(parts) >= 3:
            return TextNode(parts[1], TextType.BOLD)
    

    if "_" in text:
        parts = text.split("_")
        if len(parts) >= 3:
            return TextNode(parts[1], TextType.ITALIC)
    

    if "`" in text:
        parts = text.split("`")
        if len(parts) >= 3:
            return TextNode(parts[1], TextType.CODE)
    
    return TextNode(text, TextType.TEXT)

def text_to_children(text):
    """Convert text with inline markdown to list of HTMLNodes"""

    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def markdown_to_html_node(markdown):

    """
    Convert a full markdown document into a single parent HTMLNode (<div>).
    Each block is converted to the appropriate HTMLNode and added as a child.
    """


    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)
        content = extract_text_content(block, block_type)

        if block_type == BlockType.HEAD:
            level = extract_heading_level(block)
            node = ParentNode(f"h{level}", text_to_children(content))

        elif block_type == BlockType.CODE: 
            text_node = TextNode(content, TextType.TEXT)
            node = ParentNode("pre", [LeafNode("code", text_node.text)])

        elif block_type == BlockType.QUOTE:
            node = ParentNode("blockquote", [ParentNode("p", text_to_children(content))])

        elif block_type == BlockType.U_LIST:
            items = [ParentNode("li", text_to_children(line.strip()))
                     for line in content.split('\n')]
            node = ParentNode("ul", items)

        elif block_type == BlockType.O_LIST:
            items = [ParentNode("li", text_to_children(line.strip()))
                     for line in content.split('\n')]
            node = ParentNode("ol", items)

        else:  
            node = ParentNode("p", text_to_children(content))

        parent_node.children.append(node)

    return parent_node



def extract_title(markdown):
    
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    return None
    
