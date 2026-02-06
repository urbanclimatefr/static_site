from htmlnode import HTMLNode
from typing import Optional, Dict

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Optional[Dict[str, str]] = None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        if value is None:
            raise ValueError("LeafNode must have a value")

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"