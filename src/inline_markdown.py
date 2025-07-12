from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes



def extract_markdown_images(text):
    image_node_contents = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return image_node_contents

def extract_markdown_links(text):
    link_node_contents = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return link_node_contents


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            temp = node.text
            image_nodes = extract_markdown_images(temp)
            for image_node in image_nodes:
                parted = temp.partition(f"![{image_node[0]}]({image_node[1]})")
                if parted[0]:  # Only add non-empty text before image
                    new_nodes.append(TextNode(parted[0], TextType.TEXT))
                new_nodes.append(TextNode(image_node[0], TextType.IMAGE, image_node[1]))
                temp = parted[2]  # Store remaining text for next iteration
            if temp:  # Only append remaining text if not empty
                new_nodes.append(TextNode(temp, TextType.TEXT))
        else:
            new_nodes.append(node)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            temp = node.text
            link_nodes = extract_markdown_links(temp)
            for link_node in link_nodes:
                parted = temp.partition(f"[{link_node[0]}]({link_node[1]})")
                if parted[0]:  # Only add non-empty text before link
                    new_nodes.append(TextNode(parted[0], TextType.TEXT))
                new_nodes.append(TextNode(link_node[0], TextType.LINK, link_node[1]))
                temp = parted[2]  # Store remaining text for next iteration
            if temp:  # Only append remaining text if not empty
                new_nodes.append(TextNode(temp, TextType.TEXT))
        else:
            new_nodes.append(node)
            
    return new_nodes

def text_to_textnodes(text):
    if not isinstance(text, TextNode):
        text = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([text], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


