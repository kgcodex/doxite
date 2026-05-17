from doxite.node import TextNode, TextType


def main() -> None:

    # text = "This is **text** with  an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # text = "text [text link](google.com) text"

    # node = TextNode(text, TextType.TEXT)
    # print(node.split())
    # node2 = TextNode("[link text](www.linktext.com) text", TextType.TEXT)
    # node3 = TextNode("text [link text](www.linktext.com)", TextType.TEXT)

    # print(node2.split())
    # print(node3.split())

    # node1 = TextNode(
    #     "![img1 text](img1.png) text1 [link text](www.linktext.com) text2 ![img2 text](img2.png)",
    #     TextType.TEXT,
    # )
    # for x in node1.split():
    #     print(x)

    # node2 = TextNode("[link text](www.linktext.com) text", TextType.TEXT)
    # print(node2.split())

    node = TextNode(
        "text *bold* [link](url) `code` ![img](img.png) _italic_",
        TextType.TEXT,
    )
    node = TextNode(
        "[a](1)[b](2)![c](3)![d](4)",
        TextType.TEXT,
    )

    node = TextNode(
        "text [broken](url text ![broken](img.png text",
        TextType.TEXT,
    )

    node = TextNode(
        "[outer [inner]](url)",
        TextType.TEXT,
    )

    node = TextNode(
        "[link]url)",
        TextType.TEXT,
    )

    node = TextNode(
        "[link](broken",
        TextType.TEXT,
    )

    node = TextNode(
        "[a](1)![](`code`",
        TextType.TEXT,
    )

    node = TextNode(
        "*bold [link](url `code ![img](src)",
        TextType.TEXT,
    )

    for x in node.split():
        print(x)


if __name__ == "__main__":
    main()
