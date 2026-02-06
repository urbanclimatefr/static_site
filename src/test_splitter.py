import unittest
from textnode import TextNode, TextType
from splitter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold_delimiter(self):
        node = TextNode("This is text with a **bold phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ]
        )

    def test_split_italic_delimiter(self):
        node = TextNode("This is text with an _italic phrase_ in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.TEXT),
            ]
        )

    def test_multiple_delimiters(self):
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" blocks", TextType.TEXT),
            ]
        )

    def test_non_text_nodes_unchanged(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("Regular text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        # Bold node should pass through unchanged
        self.assertEqual(new_nodes[0], node1)

    def test_missing_closing_delimiter_raises(self):
        node = TextNode("This is text with a `code block without closing", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("closing delimiter", str(context.exception))

    def test_no_delimiters_in_text(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" at the start", TextType.TEXT),
            ]
        )

    def test_delimiter_at_end(self):
        node = TextNode("text ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text ends with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )

    def test_consecutive_delimiters(self):
        node = TextNode("text with ``double`` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text with ", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode("double", TextType.TEXT),
                TextNode("", TextType.CODE),
                TextNode(" code", TextType.TEXT),
            ]
        )

    def test_multiple_input_nodes(self):
        node1 = TextNode("Text with `code1`", TextType.TEXT)
        node2 = TextNode("More `code2` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode("More ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )


if __name__ == "__main__":
    unittest.main()