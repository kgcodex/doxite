from __future__ import annotations

from collections.abc import Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[HTMLNode] | None = None,
        props: dict[str, str | None] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.tag},{self.value},{self.children},{self.props})"

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return " " + " ".join(f'{attr}="{val}"' for attr, val in self.props.items())
