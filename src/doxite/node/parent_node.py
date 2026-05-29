from collections.abc import Sequence

from doxite.node.html_node import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode requires a tag")

        if self.children is None:
            raise ValueError("ParentNode's Children can't be None")

        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
