from doxite.node.html_node import HTMLNode

VOID_TAGS = {
    "img",
    "br",
    "hr",
}


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value.")

        if self.tag in VOID_TAGS:
            return f"<{self.tag}{self.props_to_html()} />"

        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"{self.value}"
