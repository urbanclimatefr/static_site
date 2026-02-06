import unittest
from splitter import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_multiline(self):
        md = """Some text

# My Title

More text"""
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_not_h2(self):
        md = """## Not a title

Some paragraph"""
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_header(self):
        md = "Just a paragraph of text"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_first_h1(self):
        md = """# First Title

# Second Title"""
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()