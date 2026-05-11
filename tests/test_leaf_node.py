from typing import cast

import pytest

from doxite.node import LeafNode


def test_leaf_node_without_value() -> None:
    node = LeafNode("p", cast(str, None))

    with pytest.raises(ValueError):
        node.to_html()


def test_leaf_node_with_tag() -> None:
    node = LeafNode(
        "a", "this is an a tag.", {"href": "www.gmail.com", "target": "_blank"}
    )
    assert (
        node.to_html()
        == '<a href="www.gmail.com" target="_blank">this is an a tag.</a>'
    )


def test_leaf_node_without_tag() -> None:
    node = LeafNode(None, "this is a simple text.")
    assert node.to_html() == "this is a simple text."
