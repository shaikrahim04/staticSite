import unittest
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_links, extract_markdown_images,
    split_nodes_image, split_nodes_link, text_to_textnodes
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_to_textNode1(self):
        old_node = TextNode("This is a text type with `code block` word in it.", TextType.TEXT)
        old_node2 = TextNode("**Sample Block Text with any nested block of markdowns**", TextType.TEXT)
        temp = split_nodes_delimiter([old_node, old_node2], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(temp, "**", TextType.BOLD)
        output_expected = [
            TextNode("This is a text type with ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word in it.", TextType.TEXT),
            TextNode("Sample Block Text with any nested block of markdowns", TextType.BOLD)
        ]
        self.assertEqual(len(new_nodes), len(output_expected))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], output_expected[i])

    def test_to_textNode2(self):
        old_node = TextNode("This contains **block text** and _italic texts_ in it.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This contains ", TextType.TEXT),
            TextNode("block text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic texts", TextType.ITALIC),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "Multiple images: ![first](img1.jpg) and ![second](img2.png)"
        )
        self.assertListEqual([
            ("first", "img1.jpg"),
            ("second", "img2.png")
        ], matches)

    def test_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "Multiple links: [link1](http://one.com) and [link2](http://two.com)"
        ) 
        self.assertListEqual([
            ("link1", "http://one.com"),
            ("link2", "http://two.com")
        ], matches)

    def test_markdown_links_with_special_chars(self):
        matches = extract_markdown_links(
            "Links with special chars: [Test-Link_1](http://test.com/path?q=1) and [Link #2](http://example.com/page#section)"
        )
        self.assertListEqual([
            ("Test-Link_1", "http://test.com/path?q=1"),
            ("Link #2", "http://example.com/page#section") 
        ], matches)

    def test_image_vs_link_markdown(self):
        text = "![img](pic.jpg) and [link](url.com)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "pic.jpg")], img_matches)
        self.assertListEqual([("link", "url.com")], link_matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "![first](img1.jpg) Some text ![second](img2.png) more text ![third](img3.gif)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "img1.jpg"),
                TextNode(" Some text ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "img2.png"),
                TextNode(" more text ", TextType.TEXT),
                TextNode("third", TextType.IMAGE, "img3.gif"),
            ],
            new_nodes,
        )

    def test_split_images_with_special_chars(self):
        node = TextNode(
            "Image with special chars: ![test-image_1](https://example.com/img?id=1#preview)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with special chars: ", TextType.TEXT),
                TextNode("test-image_1", TextType.IMAGE, "https://example.com/img?id=1#preview"),
            ],
            new_nodes,
        )

    def test_split_links_basic(self):
        node = TextNode(
            "Here's a [simple link](https://example.com) in text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here's a ", TextType.TEXT),
                TextNode("simple link", TextType.LINK, "https://example.com"),
                TextNode(" in text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "[First](link1.com) middle [Second](link2.com) end [Third](link3.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First", TextType.LINK, "link1.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("Second", TextType.LINK, "link2.com"),
                TextNode(" end ", TextType.TEXT),
                TextNode("Third", TextType.LINK, "link3.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_basic(self):
        node = TextNode(
            "This is **bold** and *italic* text with `code`",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and *italic* text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_links_and_images(self):
        node = TextNode(
            "Here's a [link](https://boot.dev) and ![image](pic.jpg)",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("Here's a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "pic.jpg"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_complex(self):
        node = TextNode(
            "# **Bold** _italic_ `code` ![image](pic.jpg) [link](url.com)",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("# ", TextType.TEXT),
                TextNode("Bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "pic.jpg"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = text_to_textnodes(node)
        self.assertListEqual([], new_nodes)

if __name__ == "__main__":
    unittest.main()
