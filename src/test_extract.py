import unittest
from splitter import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_not_links(self):
        text = "This has a [link](https://boot.dev) but no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_not_images(self):
        text = "This has an ![image](https://img.com/pic.png) but we want links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        text = "Check out [Boot.dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Boot.dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_mixed(self):
        text = "A [link](https://a.com) and an ![image](https://b.com/img.png) together"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertListEqual([("link", "https://a.com")], links)
        self.assertListEqual([("image", "https://b.com/img.png")], images)


if __name__ == "__main__":
    unittest.main()