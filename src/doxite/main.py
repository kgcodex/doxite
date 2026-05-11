from doxite.node import HTMLNode, LeafNode, ParentNode, TextNode, TextType


def main() -> None:
    link = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")

    print(link)

    node = LeafNode("p", "This is a p tag.")
    print(repr(node))
    node3 = HTMLNode("p", "This is a p tag.")
    print(repr(node3))

    node1 = ParentNode(
        "p",
        [
            ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text in P"),
                    LeafNode(None, "Normal text in P"),
                    LeafNode("i", "italic text in P"),
                    LeafNode(None, "Normal text in P"),
                ],
            ),
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    print(node1.to_html())


if __name__ == "__main__":
    main()
