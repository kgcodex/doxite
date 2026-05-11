from doxite.node import TextNode, TextType


def test_text_node_init() -> None:
    node = TextNode("this is a text node", TextType.BOLD, "www.google.com")
    assert (
        repr(node)
        == f"TextNode(this is a text node,{TextType.BOLD.value},www.google.com)"
    )


def test_text_node_are_eq() -> None:
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    assert node == node2
