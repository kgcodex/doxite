from doxite.node import TextNode, TextType


def main() -> None:

    node = TextNode(
        "this is a _ text block * and also `code block with _ and sometime * or ** inside as well` but _italic block_ are also there and *bold block* are also there.",
        TextType.TEXT,
    )

    node = TextNode("hello code`", TextType.TEXT)
    node = TextNode("hello `` world", TextType.TEXT)
    node = TextNode("`a``b`", TextType.TEXT)
    node = TextNode("kunal`s code and *boldy*", TextType.TEXT)

    print(node.split())


if __name__ == "__main__":
    main()
