import unittest
from textnode import TextNode, TextType
from splitter import text_to_textnodes


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_code(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_text_to_textnodes_image(self):
        text = "This is an ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        )

    def test_text_to_textnodes_link(self):
        text = "This is a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text with no formatting"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode(text, TextType.TEXT)])

    def test_text_to_textnodes_multiple_bold(self):
        text = "**bold1** and **bold2**"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("bold1", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
            ]
        )

    def test_text_to_textnodes_multiple_links(self):
        text = "Visit [site1](https://a.com) and [site2](https://b.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("site1", TextType.LINK, "https://a.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("site2", TextType.LINK, "https://b.com"),
            ]
        )


if __name__ == "__main__":
    unittest.main()