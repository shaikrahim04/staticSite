import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title

class TestMarkdownBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = markdown_to_blocks(
        """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
    )
            
        self.assertEqual(
            md,
            [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
            ]
        )

    def test_block_type_heading(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6"
        ]
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertEqual(block_to_block_type(heading), BlockType.HEAD)

    def test_block_type_paragraph(self):
        paragraphs = [
            "This is a simple paragraph",
            "This is a paragraph\nwith multiple lines\nof text",
            "Paragraph with **bold** and _italic_"
        ]
        for para in paragraphs:
            with self.subTest(para=para):
                self.assertEqual(block_to_block_type(para), BlockType.PARA)

    def test_block_type_code(self):
        code_blocks = [
            "```\nprint('hello')\n```",
            "```python\ndef func():\n    pass\n```"
        ]
        for code in code_blocks:
            with self.subTest(code=code):
                self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_block_type_quote(self):
        quotes = [
            "> Single line quote",
            "> Multi-line\n> quote block\n> here"
        ]
        for quote in quotes:
            with self.subTest(quote=quote):
                self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        lists = [
            "* First item\n* Second item",
            "- First item\n- Second item\n- Third item"
        ]
        for lst in lists:
            with self.subTest(list=lst):
                self.assertEqual(block_to_block_type(lst), BlockType.U_LIST)

    def test_block_type_ordered_list(self):
        lists = [
            "1. First item\n2. Second item",
            "1. First\n2. Second\n3. Third"
        ]
        for lst in lists:
            with self.subTest(list=lst):
                self.assertEqual(block_to_block_type(lst), BlockType.O_LIST)

    def test_block_type_invalid_heading(self):
        invalid_headings = [
            "#Invalid heading",  # No space after #
            "##Invalid heading"  # No space after ##
        ]
        for heading in invalid_headings:
            with self.subTest(heading=heading):
                self.assertEqual(block_to_block_type(heading), BlockType.PARA)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title_basic(self):
        md = "# My Title\n\nSome content here."
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_with_leading_spaces(self):
        md = "   # My Title\n\nSome content here."
        self.assertEqual(extract_title(md.lstrip()), "My Title")

    def test_extract_title_multiline(self):
        md = """
# First Title

Some text

# Second Title
"""
        self.assertEqual(extract_title(md), "First Title")

    def test_extract_title_no_title(self):
        md = "This is just text.\n\n## Subtitle"
        self.assertIsNone(extract_title(md))

    def test_extract_title_not_h1(self):
        md = "## Not a main title\n\n# Main Title"
        self.assertEqual(extract_title(md), "Main Title")

        


