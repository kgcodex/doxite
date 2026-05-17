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


def test_link_split() -> None:
    node1 = TextNode("text [link text](www.linktext.com) text", TextType.TEXT)
    node2 = TextNode("[link text](www.linktext.com) text", TextType.TEXT)
    node3 = TextNode("text [link text](www.linktext.com)", TextType.TEXT)

    assert node1.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "www.linktext.com"),
        TextNode(" text", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("link text", TextType.LINK, "www.linktext.com"),
        TextNode(" text", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "www.linktext.com"),
    ]


def test_image_split() -> None:
    node1 = TextNode("text ![img text](img.png) text", TextType.TEXT)
    node2 = TextNode("![img text](img.png) text", TextType.TEXT)
    node3 = TextNode("text ![img text](img.png)", TextType.TEXT)

    assert node1.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("img text", TextType.IMAGE, "img.png"),
        TextNode(" text", TextType.TEXT),
    ]

    assert node2.split() == [
        TextNode("img text", TextType.IMAGE, "img.png"),
        TextNode(" text", TextType.TEXT),
    ]

    assert node3.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("img text", TextType.IMAGE, "img.png"),
    ]


def test_link_and_image_split() -> None:
    node1 = TextNode(
        "![img text](img.png) text [link text](www.linktext.com) text ![img text](img.png)",
        TextType.TEXT,
    )
    node2 = TextNode(
        "[link text](www.linktext.com) text ![img text](img.png) text [link text](www.linktext.com)",
        TextType.TEXT,
    )

    assert node1.split() == [
        TextNode("img text", TextType.IMAGE, "img.png"),
        TextNode(" text ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "www.linktext.com"),
        TextNode(" text ", TextType.TEXT),
        TextNode("img text", TextType.IMAGE, "img.png"),
    ]

    assert node2.split() == [
        TextNode("link text", TextType.LINK, "www.linktext.com"),
        TextNode(" text ", TextType.TEXT),
        TextNode("img text", TextType.IMAGE, "img.png"),
        TextNode(" text ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "www.linktext.com"),
    ]


def test_split_link_and_image_with_inline_formatting() -> None:
    node = TextNode(
        "text *bold* [link](url) `code` ![img](img.png) _italic_",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" ", TextType.TEXT),
        TextNode("link", TextType.LINK, "url"),
        TextNode(" ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(" ", TextType.TEXT),
        TextNode("img", TextType.IMAGE, "img.png"),
        TextNode(" ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
    ]


def test_split_multiple_links_and_images() -> None:
    node = TextNode(
        "[a](1)[b](2)![c](3)![d](4)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("a", TextType.LINK, "1"),
        TextNode("b", TextType.LINK, "2"),
        TextNode("c", TextType.IMAGE, "3"),
        TextNode("d", TextType.IMAGE, "4"),
    ]


def test_split_links_and_images_inside_code_are_ignored() -> None:
    node = TextNode(
        "`[link](url)` and `![img](img.png)`",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("[link](url)", TextType.CODE),
        TextNode(" and ", TextType.TEXT),
        TextNode("![img](img.png)", TextType.CODE),
    ]


def test_split_unclosed_link_and_image() -> None:
    node1 = TextNode(
        "text [link text](url text ![image text](img.png text",
        TextType.TEXT,
    )

    node2 = TextNode(
        "[link](www.linktext.com",
        TextType.TEXT,
    )

    assert node1.split() == [
        TextNode("text ", TextType.TEXT),
        TextNode("link text", TextType.LINK, "url"),
        TextNode("text ", TextType.TEXT),
        TextNode("image text", TextType.IMAGE, "img.png"),
        TextNode("text", TextType.TEXT),
    ]

    assert node2.split() == [TextNode("link", TextType.LINK, "www.linktext.com")]


def test_split_empty_link_and_image_text() -> None:
    node = TextNode(
        "[]() and ![]()",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode(" and ", TextType.TEXT),
    ]


def test_split_nested_like_links() -> None:
    node = TextNode(
        "[outer [inner]](url)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("[outer ", TextType.TEXT),
        TextNode("inner]", TextType.LINK, "url"),
    ]


def test_split_broken_paren_structure() -> None:
    node = TextNode(
        "[link]url)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("[link]url)", TextType.TEXT),
    ]


def test_split_image_then_text_without_spacing() -> None:
    node = TextNode(
        "![img](img.png)text",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("img", TextType.IMAGE, "img.png"),
        TextNode("text", TextType.TEXT),
    ]


def test_split_text_then_link_without_spacing() -> None:
    node = TextNode(
        "text[link](url)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("text", TextType.TEXT),
        TextNode("link", TextType.LINK, "url"),
    ]


def test_split_adjacent_inline_and_links() -> None:
    node = TextNode(
        "*bold*[link](url)_italic_",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("bold", TextType.BOLD),
        TextNode("link", TextType.LINK, "url"),
        TextNode("italic", TextType.ITALIC),
    ]


def test_split_malformed_mixed_inline_regions() -> None:
    node = TextNode(
        "*bold [link](url) text",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("*bold ", TextType.TEXT),
        TextNode("link", TextType.LINK, "url"),
        TextNode(" text", TextType.TEXT),
    ]


def test_split_preserves_token_order() -> None:
    node = TextNode(
        "a [b](1) c *d* e `f` g ![h](2)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("a ", TextType.TEXT),
        TextNode("b", TextType.LINK, "1"),
        TextNode(" c ", TextType.TEXT),
        TextNode("d", TextType.BOLD),
        TextNode(" e ", TextType.TEXT),
        TextNode("f", TextType.CODE),
        TextNode(" g ", TextType.TEXT),
        TextNode("h", TextType.IMAGE, "2"),
    ]


def test_split_lone_image_marker() -> None:
    node = TextNode(
        "hello ! world",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("hello ! world", TextType.TEXT),
    ]


def test_split_broken_image_syntax() -> None:
    node = TextNode(
        "![broken",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("![broken", TextType.TEXT),
    ]


def test_split_url_with_nested_parens() -> None:
    node = TextNode(
        "[link](https://site.com/a(b)c)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("link", TextType.LINK, "https://site.com/a(b"),
        TextNode("c)", TextType.TEXT),
    ]


def test_split_adjacent_malformed_tokens() -> None:
    node = TextNode(
        "[a](1)![](`code`",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("a", TextType.LINK, "1"),
        TextNode("code", TextType.CODE),
    ]


def test_split_link_adjacent_to_inline() -> None:
    node = TextNode(
        "[link](url)*bold*",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("link", TextType.LINK, "url"),
        TextNode("bold", TextType.BOLD),
    ]


def test_split_is_stable() -> None:
    node = TextNode(
        "text *bold* [link](url)",
        TextType.TEXT,
    )

    split_nodes = node.split()

    for split_node in split_nodes:
        assert split_node.split() == [split_node]


def test_split_large_malformed_input() -> None:
    node = TextNode(
        "*bold [link](url `code ![img](src)",
        TextType.TEXT,
    )

    assert node.split() == [
        TextNode("*bold ", TextType.TEXT),
        TextNode("link", TextType.LINK, "url"),
        TextNode("`code ", TextType.TEXT),
        TextNode("img", TextType.IMAGE, "src"),
    ]
