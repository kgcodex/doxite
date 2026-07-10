from pathlib import Path

import typer

from doxite.node.markdown_parser import MarkdownParser

app = typer.Typer()


@app.command()
def hello() -> None:
    print("Hello welcome to Doxite")


@app.command()
def init(project_name: str) -> None:
    """
    Initialize a new Doxite SSG Project.
    """
    project_dir = Path.cwd() if project_name == "." else Path(project_name)
    project_dir.mkdir(parents=True, exist_ok=True)

    (project_dir / "public").mkdir(exist_ok=True)
    (project_dir / "src").mkdir(exist_ok=True)

    (project_dir / "src" / "index.md").write_text(
        "# Welcome to Doxite", encoding="utf-8"
    )

    typer.echo(f"Initialized Doxite project at: {project_dir}")


@app.command()
def build() -> None:
    """
    Build the dist from src.
    """
    project_dir = Path.cwd()
    dist = project_dir / "dist"
    dist.mkdir(exist_ok=True)

    src = project_dir / "src"
    mds = [file for file in src.rglob("*.md") if file.is_file()]
    template = (Path(__file__).parent / "template" / "template.html").read_text("utf-8")

    for md_file in mds:
        parser = MarkdownParser(md_file)
        (dist / f"{md_file.stem}.html").write_text(
            f"""<!doctype html>
<html lang="en" data-theme="night">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    {"".join(node.to_html() for node in parser.parse_markdown())}
  </body>
</html>
"""
        )

    typer.echo(f"Project build at: {project_dir}/dist/ ")


if __name__ == "__main__":
    app()
