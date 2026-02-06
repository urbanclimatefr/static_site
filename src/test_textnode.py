import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_url(self):
        node = TextNode("Link text", TextType.LINK, "https://a.com")
        node2 = TextNode("Link text", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_none_url_vs_url_none(self):
        node = TextNode("Link text", TextType.LINK)
        node2 = TextNode("Link text", TextType.LINK, None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()