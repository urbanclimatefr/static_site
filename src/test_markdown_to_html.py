import unittest
from splitter import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
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
        md = "\n```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_heading_with_inline(self):
        md = "## This is **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is <b>bold</b> heading</h2></div>")

    def test_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_blockquote(self):
        md = """>This is a quote
>with multiple lines
>of quoted text"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines of quoted text</blockquote></div>",
        )

    def test_blockquote_with_space(self):
        md = """> Quote with space
> Multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote with space Multiple lines</blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """# Heading

This is a paragraph.

- List item 1
- List item 2"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>This is a paragraph.</p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>List item 1</li>", html)

    def test_list_with_inline_formatting(self):
        md = """- Item with **bold**
- Item with _italic_"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<li>Item with <b>bold</b></li>", html)
        self.assertIn("<li>Item with <i>italic</i></li>", html)


if __name__ == "__main__":
    unittest.main()