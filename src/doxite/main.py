from doxite.node import MarkdownParser


def main() -> None:

    md_parser = MarkdownParser("tests/fixtures/markdown/combined.md")
    # print(md_parser.parse_markdown())
    # print("\n")

    with open("combined.html", "w") as f:
        for node in md_parser.parse_markdown():
            f.writelines(node.to_html())


if __name__ == "__main__":
    main()
