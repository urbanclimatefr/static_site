import unittest
from splitter import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block"])

    def test_markdown_to_blocks_multiple_blocks(self):
        md = """# Heading

Paragraph 1

Paragraph 2"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading", "Paragraph 1", "Paragraph 2"],
        )

    def test_markdown_to_blocks_with_leading_trailing_whitespace(self):
        md = "   This is a block   \n\n   Another block   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a block", "Another block"],
        )

    def test_markdown_to_blocks_empty_blocks(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])

    def test_markdown_to_blocks_list(self):
        md = """- Item 1
- Item 2
- Item 3

Next paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["- Item 1\n- Item 2\n- Item 3", "Next paragraph"],
        )

    def test_markdown_to_blocks_heading_and_code(self):
        md = "# Heading\n\n```\ncode block\n```\n\nText"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# Heading", "```\ncode block\n```", "Text"],
        )

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_multiline_paragraph(self):
        md = "Line 1\nLine 2\nLine 3\n\nNew block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line 1\nLine 2\nLine 3", "New block"],
        )


if __name__ == "__main__":
    unittest.main()