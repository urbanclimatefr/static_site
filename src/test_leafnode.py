import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_no_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_repr(self):
        node = LeafNode("p", "Text", {"class": "paragraph"})
        repr_str = repr(node)
        self.assertIn("tag=p", repr_str)
        self.assertIn("value=Text", repr_str)
        self.assertIn("class", repr_str)


if __name__ == "__main__":
    unittest.main()