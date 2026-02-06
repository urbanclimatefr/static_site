import unittest
from splitter import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h2(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_no_space(self):
        # No space after # means it's not a heading
        self.assertEqual(block_to_block_type("#NotAHeading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline1\nline2\nline3\n```"), BlockType.CODE)

    def test_code_block_missing_end(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)

    def test_quote_multi_line(self):
        self.assertEqual(block_to_block_type(">Line 1\n>Line 2\n>Line 3"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)

    def test_quote_not_all_lines(self):
        self.assertEqual(block_to_block_type(">Line 1\nLine 2"), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- Single item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST)

    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. Only item"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. Second\n3. Third"), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_order(self):
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("Line 1\nLine 2\nLine 3"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()