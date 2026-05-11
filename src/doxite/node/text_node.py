from __future__ import annotations

from doxite.node.leaf_node import LeafNode
from doxite.node.text_type import TextType


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.text},{self.text_type},{self.url})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def to_leaf_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT.value:
                return LeafNode(None, self.text)

            case TextType.BOLD.value:
                return LeafNode("b", self.text)

            case TextType.ITALIC.value:
                return LeafNode("i", self.text)

            case TextType.CODE.value:
                return LeafNode("code", self.text)

            case TextType.LINK.value:
                return LeafNode("a", self.text, {"href": self.url})

            case TextType.IMAGE.value:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})

            case _:
                raise NotImplementedError
