from collections.abc import Sequence
from typing import cast

import pytest

from doxite.node import HTMLNode, LeafNode, ParentNode

sub_nodes_set1 = [
    LeafNode("p", "p tag", {"style": "text-align:right"}),
    LeafNode("a", "a tag", {"href": "www.gmail.com", "target": "_blank"}),
    LeafNode(None, "Normal Text."),
    LeafNode("p", "p tag"),
]

sub_nodes_set2 = [
    ParentNode("p", sub_nodes_set1, {"style": "text-align:right"}),
    LeafNode("p", "p tag", {"style": "text-align:right"}),
    LeafNode("a", "a tag", {"href": "www.gmail.com", "target": "_blank"}),
    LeafNode(None, "Normal Text."),
    LeafNode("p", "p tag"),
]

sub_nodes_set1_html = '<p style="text-align:right">p tag</p><a href="www.gmail.com" target="_blank">a tag</a>Normal Text.<p>p tag</p>'
sub_nodes_set2_html = (
    '<p style="text-align:right">' + sub_nodes_set1_html + "</p>" + sub_nodes_set1_html
)


def test_parent_node_without_tag() -> None:
    node = ParentNode(cast(str, None), sub_nodes_set1)

    with pytest.raises(ValueError):
        node.to_html()


def test_parent_node_without_children() -> None:
    node = ParentNode("p", cast(Sequence[HTMLNode], None))

    with pytest.raises(ValueError):
        node.to_html()


# def test_parent_node_with_empty_children() -> None:
#     node = ParentNode("p", [])

#     with pytest.raises(ValueError):
#         node.to_html()


def test_parent_node_with_only_leaf_node() -> None:
    node = ParentNode("p", sub_nodes_set1)

    assert node.to_html() == f"<p>{sub_nodes_set1_html}</p>"


def test_parent_node_with_props() -> None:
    node = ParentNode(
        "div",
        [LeafNode(None, "Hello")],
        {"class": "container"},
    )

    assert node.to_html() == '<div class="container">Hello</div>'


def test_parent_node_with_nested_parent_node() -> None:
    node = ParentNode("p", sub_nodes_set2)

    print(node.to_html())

    assert node.to_html() == f"<p>{sub_nodes_set2_html}</p>"


def test_deeply_nested_parent_nodes() -> None:
    node = ParentNode(
        "div",
        [
            ParentNode(
                "section",
                [
                    ParentNode(
                        "p",
                        [LeafNode(None, "Hello")],
                    )
                ],
            )
        ],
    )

    assert node.to_html() == "<div><section><p>Hello</p></section></div>"
