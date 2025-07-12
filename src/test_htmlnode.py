import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node1 = HTMLNode()
        self.assertEqual(node, node1)

    def test_eq1(self):
        node = HTMLNode("a", "LinkedIn")
        node1 = HTMLNode("a", "LinkedIn", None)
        self.assertEqual(node, node1)

    def test_eq_false(self):
        node = HTMLNode("p", "This is nice", ["b", "i"], {"target": "_blank"})
        node1 = HTMLNode("p", "This is nice", ["b"], {"target": "_blank"})
        self.assertNotEqual(node, node1)

    def test_props_to_html(self):
        node = HTMLNode("p", "This is nice", ["b", "i"], {"target": "_blank"})
        self.assertEqual(node.props_to_html(), " target=\"_blank\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Nothing bites", {"target": "_blank", "src":"./img.png"})
        self.assertNotEqual(node.to_html(), '<a target="_blank" src="./img.png">Nothing bites"</a>')

    def test_leaf_value_none(self):
        # Ensure ValueError is raised when value is None
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_tag_none_returns_value(self):
        # Confirm that LeafNode returns plain text when tag is None
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_sibling_no_tag(self):
        grandchild_node = LeafNode("b", "grandchild1")
        grandchild_node2 = LeafNode(None, value="grandchild2")
        child_node1 = ParentNode("p", [grandchild_node, grandchild_node2])
        child_node2 = LeafNode("a", "childnode2", {"href":"https://google.com"})
        node = ParentNode("p", [child_node2, child_node1], {"style":"border: dashed 1px"})
        self.assertEqual(
            node.to_html(),
            '<p style="border: dashed 1px"><a href="https://google.com">childnode2</a><p><b>grandchild1</b>grandchild2</p></p>'
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_text(self):
        node = TextNode("Normal Text", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Normal Text")

    def test_text_3(self):
        node = TextNode("WhiteBeards Image", TextType.IMAGE, "./whitebeard.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertNotEqual(html_node.value, "WhiteBeards Image")

