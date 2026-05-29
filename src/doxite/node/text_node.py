from __future__ import annotations

from typing import Literal

from doxite.node.html_node import HTMLNode
from doxite.node.leaf_node import LeafNode
from doxite.node.text_type import TextType


class TextNode(HTMLNode):
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

    def split_link_and_image(self) -> list[TextNode]:
        if self.text_type != TextType.TEXT.value:
            return [self]

        nodes: list[TextNode] = []

        text = self.text
        text_len = len(text)

        url = ""
        node_txt = ""
        node_type: Literal[TextType.IMAGE, TextType.LINK, None] = None

        curr_ptr = 0
        look_ahead_ptr = 0
        offset_ptr = 0

        while look_ahead_ptr < text_len:
            char = text[look_ahead_ptr]

            if char == "[" and node_type != TextType.IMAGE:
                node_type = TextType.LINK
                curr_ptr = look_ahead_ptr

            if (
                char == "!"
                and look_ahead_ptr + 1 < text_len
                and text[look_ahead_ptr + 1] == "["
            ):
                node_type = TextType.IMAGE
                curr_ptr = look_ahead_ptr

            if (
                char == "]"
                and look_ahead_ptr + 1 < text_len
                and text[look_ahead_ptr + 1] == "("
            ):
                if buff := text[offset_ptr:curr_ptr]:
                    nodes.append(TextNode(buff, TextType.TEXT))

                if node_type == TextType.LINK:
                    node_txt = text[curr_ptr + 1 : look_ahead_ptr]

                if node_type == TextType.IMAGE:
                    node_txt = text[curr_ptr + 2 : look_ahead_ptr]

                curr_ptr = look_ahead_ptr + 2

                while (
                    look_ahead_ptr < text_len
                    and text[look_ahead_ptr] != ")"
                    and text[look_ahead_ptr] != " "
                ):
                    look_ahead_ptr += 1

                url = text[curr_ptr:look_ahead_ptr]

                if node_txt and node_type:
                    nodes.append(TextNode(node_txt, node_type, url))
                    node_type = None

                offset_ptr = look_ahead_ptr + 1

            look_ahead_ptr += 1

        if buff := text[offset_ptr:look_ahead_ptr]:
            nodes.append(TextNode(buff, TextType.TEXT))

        return nodes

    def split(self) -> list[TextNode]:
        if self.text_type != TextType.TEXT.value:
            return [self]

        nodes: list[TextNode] = []

        text = self.text
        text_len = len(text)

        delimiter_map = {
            "`": TextType.CODE,
            "*": TextType.BOLD,
            "_": TextType.ITALIC,
        }

        inside_code_block = False

        curr_ptr = 0
        look_ahead_ptr = 0
        offset_ptr = 0

        while look_ahead_ptr < text_len:
            char = text[look_ahead_ptr]

            if char in delimiter_map:
                delimiter = delimiter_map[char]

                if char == "`":
                    inside_code_block = True

                if look_ahead_ptr != curr_ptr and char == text[curr_ptr]:
                    if buff := text[offset_ptr:curr_ptr]:
                        nodes.extend(
                            TextNode(buff, TextType.TEXT).split_link_and_image()
                        )

                    nodes.append(
                        TextNode(text[curr_ptr + 1 : look_ahead_ptr], delimiter)
                    )
                    if char == "`":
                        inside_code_block = False

                    curr_ptr = look_ahead_ptr + 1
                    offset_ptr = curr_ptr
                else:
                    if not (inside_code_block and text[curr_ptr] == "`"):
                        curr_ptr = look_ahead_ptr

            look_ahead_ptr += 1

        if buff := text[offset_ptr:look_ahead_ptr]:
            nodes.extend(TextNode(buff, TextType.TEXT).split_link_and_image())

        return nodes

    def to_leaf_node(self, props: dict[str, str | None] | None = None) -> LeafNode:
        match self.text_type:
            case TextType.TEXT.value:
                return LeafNode(None, self.text, props)

            case TextType.BOLD.value:
                return LeafNode("b", self.text, props)

            case TextType.ITALIC.value:
                return LeafNode("i", self.text, props)

            case TextType.CODE.value:
                return LeafNode("code", self.text, props)

            case TextType.LINK.value:
                return LeafNode("a", self.text, {"href": self.url, **(props or {})})

            case TextType.IMAGE.value:
                return LeafNode(
                    "img", "", {"src": self.url, "alt": self.text, **(props or {})}
                )

            case _:
                raise NotImplementedError
