from typing import Literal

from doxite.node import TextNode, TextType

type BlockType = Literal["`code block`", "_italic block_", "*bold block*"]


def get_block_placement(block_type: BlockType) -> tuple[TextNode, TextNode, TextNode]:
    return (
        TextNode(f"{block_type} text block1 text block2", TextType.TEXT),
        TextNode(f"text block1 {block_type} text block2", TextType.TEXT),
        TextNode(f"text block1 text block2 {block_type}", TextType.TEXT),
    )


def get_block_splits(
    block_type: BlockType, text_type: TextType
) -> tuple[list[TextNode], list[TextNode], list[TextNode]]:
    block = block_type[1:-1]
    return (
        [
            TextNode(block, text_type, None),
            TextNode(" text block1 text block2", TextType.TEXT, None),
        ],
        [
            TextNode("text block1 ", TextType.TEXT, None),
            TextNode(block, text_type, None),
            TextNode(" text block2", TextType.TEXT, None),
        ],
        [
            TextNode("text block1 text block2 ", TextType.TEXT, None),
            TextNode(block, text_type, None),
        ],
    )


def test_init() -> None:
    node = TextNode("this is a text node", TextType.BOLD, "www.google.com")
    assert (
        repr(node)
        == f"TextNode(this is a text node,{TextType.BOLD.value},www.google.com)"
    )


def test_text_node_to_leaf_node() -> None:
    node = TextNode("This is a text node", TextType.TEXT).to_leaf_node()

    assert node.tag is None
    assert node.value == "This is a text node"


def test_split_plain_text() -> None:
    node = TextNode("just plain text", TextType.TEXT)

    assert node.split() == [
        TextNode("just plain text", TextType.TEXT),
    ]


def test_split_single_delimiter_as_text() -> None:
    node1 = TextNode("`", TextType.TEXT)
    node2 = TextNode("_", TextType.TEXT)
    node3 = TextNode("*", TextType.TEXT)

    assert node1.split() == [
        TextNode("`", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("_", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("*", TextType.TEXT),
    ]


def test_split_inline_code_block() -> None:
    node1, node2, node3 = get_block_placement("`code block`")
    node1_split, node2_split, node3_split = get_block_splits(
        "`code block`", TextType.CODE
    )

    assert node1.split() == node1_split
    assert node2.split() == node2_split
    assert node3.split() == node3_split


def test_split_inline_italic_block() -> None:
    node1, node2, node3 = get_block_placement("_italic block_")
    node1_split, node2_split, node3_split = get_block_splits(
        "_italic block_", TextType.ITALIC
    )

    assert node1.split() == node1_split
    assert node2.split() == node2_split
    assert node3.split() == node3_split


def test_split_inline_bold_block() -> None:
    node1, node2, node3 = get_block_placement("*bold block*")
    node1_split, node2_split, node3_split = get_block_splits(
        "*bold block*", TextType.BOLD
    )

    assert node1.split() == node1_split
    assert node2.split() == node2_split
    assert node3.split() == node3_split


def test_split_delimiter_at_text_boundaries() -> None:
    node1 = TextNode("`code`text", TextType.TEXT)
    node2 = TextNode("text`code`", TextType.TEXT)
    node3 = TextNode("_italic_text", TextType.TEXT)
    node4 = TextNode("text*bold*", TextType.TEXT)

    assert node1.split() == [
        TextNode("code", TextType.CODE),
        TextNode("text", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("text", TextType.TEXT),
        TextNode("code", TextType.CODE),
    ]

    assert node3.split() == [
        TextNode("italic", TextType.ITALIC),
        TextNode("text", TextType.TEXT),
    ]

    assert node4.split() == [
        TextNode("text", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
    ]


def test_split_all_inline_block() -> None:
    node = TextNode(
        "This is a text block `code block` and now *bold block* and then the _italic block_ and then text again",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("This is a text block ", TextType.TEXT, None),
        TextNode("code block", TextType.CODE, None),
        TextNode(" and now ", TextType.TEXT, None),
        TextNode("bold block", TextType.BOLD, None),
        TextNode(" and then the ", TextType.TEXT, None),
        TextNode("italic block", TextType.ITALIC, None),
        TextNode(" and then text again", TextType.TEXT, None),
    ]


def test_non_text_nodes_are_unchanged() -> None:
    node = TextNode("`only code block`", TextType.CODE)

    assert node.split() == [TextNode("`only code block`", TextType.CODE, None)]


def test_split_mixed_delimiters() -> None:
    node = TextNode(
        "this is a _ text block * and also `code block with _ and sometime * or ** inside as well` but _italic block_ are also there and *bold block* are also there.",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("this is a _ text block * and also ", TextType.TEXT, None),
        TextNode(
            "code block with _ and sometime * or ** inside as well", TextType.CODE, None
        ),
        TextNode(" but ", TextType.TEXT, None),
        TextNode("italic block", TextType.ITALIC, None),
        TextNode(" are also there and ", TextType.TEXT, None),
        TextNode("bold block", TextType.BOLD, None),
        TextNode(" are also there.", TextType.TEXT, None),
    ]


def test_split_unclosed_delimiter() -> None:
    node1 = TextNode("hello `code", TextType.TEXT)
    node2 = TextNode("hello _italic", TextType.TEXT)
    node3 = TextNode("hello *bold", TextType.TEXT)

    assert node1.split() == [TextNode("hello `code", TextType.TEXT, None)]
    assert node2.split() == [TextNode("hello _italic", TextType.TEXT, None)]
    assert node3.split() == [TextNode("hello *bold", TextType.TEXT, None)]


def test_split_malformed_then_valid_regions() -> None:
    node1 = TextNode("`broken hello `valid`", TextType.TEXT)
    node2 = TextNode("_broken text _valid_", TextType.TEXT)
    node3 = TextNode("*broken text *valid*", TextType.TEXT)

    assert node1.split() == [
        TextNode("broken hello ", TextType.CODE),
        TextNode("valid`", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("broken text ", TextType.ITALIC),
        TextNode("valid_", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("broken text ", TextType.BOLD),
        TextNode("valid*", TextType.TEXT),
    ]


def test_split_with_empty_inline_blocks() -> None:
    node = TextNode("hello `` world __ and ** universe", TextType.TEXT)

    assert node.split() == [
        TextNode("hello ", TextType.TEXT, None),
        TextNode("", TextType.CODE, None),
        TextNode(" world ", TextType.TEXT, None),
        TextNode("", TextType.ITALIC, None),
        TextNode(" and ", TextType.TEXT, None),
        TextNode("", TextType.BOLD, None),
        TextNode(" universe", TextType.TEXT, None),
    ]


def test_split_consecutive_inline_blocks() -> None:
    node1 = TextNode("`a``b`", TextType.TEXT)
    node2 = TextNode("*a**b*", TextType.TEXT)
    node3 = TextNode("_a__b_", TextType.TEXT)

    assert node1.split() == [
        TextNode("a", TextType.CODE, None),
        TextNode("b", TextType.CODE, None),
    ]
    assert node2.split() == [
        TextNode("a", TextType.BOLD, None),
        TextNode("b", TextType.BOLD, None),
    ]
    assert node3.split() == [
        TextNode("a", TextType.ITALIC, None),
        TextNode("b", TextType.ITALIC, None),
    ]


def test_split_weird_delimiter_placement() -> None:
    node1 = TextNode("`a`b`", TextType.TEXT)
    node2 = TextNode("_a_b_", TextType.TEXT)
    node3 = TextNode("*a*b*", TextType.TEXT)

    assert node1.split() == [
        TextNode("a", TextType.CODE),
        TextNode("b`", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("a", TextType.ITALIC),
        TextNode("b_", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("a", TextType.BOLD),
        TextNode("b*", TextType.TEXT),
    ]


def test_split_nested_like_input() -> None:
    node1 = TextNode("_italic *inside*_", TextType.TEXT)
    node2 = TextNode("*bold _inside_*", TextType.TEXT)
    node3 = TextNode("`code _inside_ *inside*`", TextType.TEXT)

    assert node1.split() == [
        TextNode("_italic ", TextType.TEXT),
        TextNode("inside", TextType.BOLD),
        TextNode("_", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("*bold ", TextType.TEXT),
        TextNode("inside", TextType.ITALIC),
        TextNode("*", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("code _inside_ *inside*", TextType.CODE),
    ]
