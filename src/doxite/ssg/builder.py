from pathlib import Path
from string import Template

from doxite.node import MarkdownParser


def ssg_builder(src: Path, dist: Path) -> None:
    mds = [file for file in src.rglob("*.md") if file.is_file()]
    template = Template(
        (Path(__file__).parent.parent / "template" / "template.html").read_text("utf-8")
    )

    for md_file in mds:
        parser = MarkdownParser(md_file)
        nodes = parser.parse_markdown()

        file_name = md_file.stem
        content = "".join(node.to_html() for node in nodes)

        html_file = dist / f"{file_name}.html"
        html_file.write_text(template.substitute(title=file_name, content=content))
