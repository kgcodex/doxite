from doxite.node import HTMLNode


def test_html_node_with_props() -> None:
    node = HTMLNode(None, None, None, {"href": "www.gmail.com", "target": "_blank"})
    assert node.props_to_html() == ' href="www.gmail.com" target="_blank"'


def test_html_node_with_empty_props() -> None:
    node = HTMLNode(None, None, None, {})
    assert node.props_to_html() == ""


def test_html_node_without__props() -> None:
    node = HTMLNode(None, None, None, None)
    assert node.props_to_html() == ""
