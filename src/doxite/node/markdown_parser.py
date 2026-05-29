import os
import re
from pathlib import Path
from typing import TextIO

from doxite.node.parent_node import ParentNode
from doxite.node.text_node import TextNode
from doxite.node.text_type import TextType

# fmt:off
MARKDOWN_PATTERN = re.compile(
    r"^(?:"
    r"(?P<heading>#+)|"             # 1 or many #
    r"(?P<blockquote>>)|"                # >
    r"(?P<unordered_list>-\s)|"     # - and then space
    r"(?P<ordered_list>\d+\.\s)|"   # a num then . then space
    r"(?P<code_block>```)|"         # ```
    r"(?P<paragraph>.+)"            # paragraph
    r")"
)
# fmt:on


class MarkdownParser:
    def __init__(self, file: os.PathLike[str] | str):
        self.file = Path(file)

    def get_md_block(
        self, md_file: TextIO, category: str, current_line: str | None = None
    ) -> list[str]:
        block = []

        if current_line:
            block.append(current_line)

        while True:
            line = md_file.readline()

            if category != "code_block":
                match = MARKDOWN_PATTERN.match(line)

                if match is None:
                    break

                if match.lastgroup != category:
                    block.append(line)
                    break

                block.append(line[match.end() :])

            else:
                if line.startswith("```") or not line:
                    break

                block.append(line)

        return block

    def parse_markdown(self) -> list[ParentNode]:
        nodes = []

        with Path.open(self.file, encoding="utf-8") as md_file:
            while line := md_file.readline():
                if not line.strip():
                    continue

                match = MARKDOWN_PATTERN.match(line)
                assert match is not None
                category = match.lastgroup

                if category == "heading":
                    count = len(match.group("heading"))

                    nodes.append(
                        ParentNode(
                            f"h{count}",
                            [
                                leaf.to_leaf_node()
                                for leaf in TextNode(
                                    line[match.end() :].strip(), TextType.TEXT
                                ).split()
                            ],
                        )
                    )
                    continue

                if category == "blockquote":
                    blocks = self.get_md_block(
                        md_file,
                        "blockquote",
                        line[match.end() :],
                    )

                    nodes.append(
                        ParentNode(
                            "pre",
                            [
                                ParentNode(
                                    "blockquote",
                                    [
                                        leaf.to_leaf_node()
                                        for leaf in TextNode(
                                            "".join(blocks),
                                            TextType.TEXT,
                                        ).split()
                                    ],
                                )
                            ],
                        )
                    )

                if category == "code_block":
                    lang = line[match.end() :].strip()
                    blocks = self.get_md_block(
                        md_file,
                        "code_block",
                    )

                    nodes.append(
                        ParentNode(
                            "pre",
                            [
                                TextNode("".join(blocks), TextType.CODE).to_leaf_node(
                                    {"class": f"language-{lang}"}
                                )
                            ],
                        )
                    )

                if category in ["ordered_list", "unordered_list"]:
                    list_tag = "ol" if category == "ordered_list" else "ul"
                    blocks = self.get_md_block(md_file, category, line[match.end() :])

                    nodes.append(
                        ParentNode(
                            list_tag,
                            [
                                ParentNode(
                                    "li",
                                    [
                                        leaf.to_leaf_node()
                                        for leaf in TextNode(
                                            element.strip(), TextType.TEXT
                                        ).split()
                                    ],
                                )
                                for element in blocks
                            ],
                        )
                    )

                if category == "paragraph":
                    nodes.append(
                        ParentNode(
                            "p",
                            [
                                leaf.to_leaf_node()
                                for leaf in TextNode(
                                    line.strip(), TextType.TEXT
                                ).split()
                            ],
                        )
                    )

        return nodes
