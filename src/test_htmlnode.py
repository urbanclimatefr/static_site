import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(
            tag="a",
            value="Click here",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        result = node.props_to_html()
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello")
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", value="Content", props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="Text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(tag="p", value="Hello", props={"class": "text"})
        repr_str = repr(node)
        self.assertIn("tag=p", repr_str)
        self.assertIn("value=Hello", repr_str)
        self.assertIn("class", repr_str)


if __name__ == "__main__":
    unittest.main()