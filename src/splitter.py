import re
from enum import Enum
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes on a given delimiter and create new nodes with the specified text type.
    
    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g., "**", "_", "`")
        text_type: TextType enum value for the delimited content
    
    Returns:
        List of TextNode objects with split nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's an odd number of parts, the closing delimiter is missing
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: closing delimiter '{delimiter}' not found")
        
        # Process the parts
        for i, part in enumerate(parts):
            # Even indices are TEXT type, odd indices are the specified text_type
            if i % 2 == 0:
                # Regular text
                if part:  # Only add non-empty parts
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Delimited text
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    """
    Split text nodes containing markdown images into separate nodes.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Split text around images
        for alt_text, url in images:
            parts = text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = parts[1] if len(parts) > 1 else ""
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    """
    Split text nodes containing markdown links into separate nodes.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Split text around links
        for anchor_text, url in links:
            parts = text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            text = parts[1] if len(parts) > 1 else ""
        
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    Processes bold, italic, code, images, and links in order.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    """
    Split a markdown document into blocks separated by blank lines.
    
    Args:
        markdown: Raw markdown string
    
    Returns:
        List of block strings
    """
    # Split on double newlines
    blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    result = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            result.append(stripped)
    
    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A single block of markdown text (already stripped)
    
    Returns:
        BlockType enum value
    """
    # Heading: starts with 1-6 # followed by a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code: starts with ``` and ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote: every line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with "N. " where N increments from 1
    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def extract_title(markdown):
    """
    Extract the h1 header from a markdown document.
    
    Args:
        markdown: Raw markdown string
    
    Returns:
        The title string (without the # and stripped of whitespace)
    
    Raises:
        ValueError: If no h1 header is found
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")

def text_to_children(text):
    """
    Convert markdown text into a list of HTMLNode children.
    Processes inline markdown (bold, italic, code, links, images).
    """
    from parentnode import ParentNode
    from textnode import text_node_to_html_node
    
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown: Full markdown document string
    
    Returns:
        A parent HTMLNode (div) containing all block HTMLNodes
    """
    from parentnode import ParentNode
    from leafnode import LeafNode
    
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            level = len(block.split(" ")[0])
            text = block[level + 1:]  # Remove the "# " prefix
            children_nodes = text_to_children(text)
            heading_node = ParentNode(f"h{level}", children_nodes)
            children.append(heading_node)
        
        elif block_type == BlockType.CODE:
            # Remove the ``` markers
            code_text = block[3:-3].strip()
            # Don't parse inline markdown in code blocks
            code_leaf = LeafNode("code", code_text)
            pre_node = ParentNode("pre", [code_leaf])
            children.append(pre_node)
        
        elif block_type == BlockType.QUOTE:
            # Remove > from each line and join with newlines
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                if line.startswith("> "):
                    quote_lines.append(line[2:])
                elif line.startswith(">"):
                    quote_lines.append(line[1:])
            quote_text = " ".join(quote_lines)
            children_nodes = text_to_children(quote_text)
            quote_node = ParentNode("blockquote", children_nodes)
            children.append(quote_node)
        
        elif block_type == BlockType.UNORDERED_LIST:
            # Create li items for each line
            lines = block.split("\n")
            list_items = []
            for line in lines:
                item_text = line[2:]  # Remove "- "
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ul_node = ParentNode("ul", list_items)
            children.append(ul_node)
        
        elif block_type == BlockType.ORDERED_LIST:
            # Create li items for each line
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove "N. " prefix
                dot_index = line.index(". ")
                item_text = line[dot_index + 2:]
                item_children = text_to_children(item_text)
                li_node = ParentNode("li", item_children)
                list_items.append(li_node)
            ol_node = ParentNode("ol", list_items)
            children.append(ol_node)
        
        elif block_type == BlockType.PARAGRAPH:
            # Replace newlines with spaces for paragraph text
            paragraph_text = block.replace("\n", " ")
            children_nodes = text_to_children(paragraph_text)
            p_node = ParentNode("p", children_nodes)
            children.append(p_node)
    
    return ParentNode("div", children)