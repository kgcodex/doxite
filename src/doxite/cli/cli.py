import os
import shutil
import socketserver
from pathlib import Path

import typer
from rich.console import Console

from doxite.ssg import PrettifiedHTTPRequestHandler, gh_deploy, ssg_builder

console = Console()

app = typer.Typer()


@app.command()
def hello() -> None:
    print("Hello, welcome to Doxite. Use --help to know available commands.")


@app.command()
def init(project_name: str) -> None:
    """
    Initialize a new Doxite SSG Project.
    """
    project_dir = Path.cwd() if project_name == "." else Path(project_name)
    project_dir.mkdir(parents=True, exist_ok=True)

    (project_dir / ".doxite").mkdir(exist_ok=True)
    (project_dir / "public").mkdir(exist_ok=True)
    (project_dir / "src").mkdir(exist_ok=True)

    (project_dir / "src" / "index.md").write_text(
        "# Welcome to Doxite", encoding="utf-8"
    )
    (project_dir / ".doxite" / ".gitignore").write_text(
        "*\n!.gitignore\n", encoding="utf-8"
    )

    console.print(
        f"[cyan]Initialized Doxite project at: [italic]{project_dir}[/italic][/cyan]"
    )


@app.command()
def build() -> None:
    """
    Build the dist from src.
    """
    project_dir = Path.cwd()

    if not (project_dir / ".doxite").exists():
        console.print(
            f"[bold red]Error:[/bold red] {project_dir} is not a Doxite Project."
        )
        raise typer.Exit(code=1)

    dist = project_dir / "dist"
    dist.mkdir(exist_ok=True)

    src = project_dir / "src"
    public = project_dir / "public"
    shutil.copytree(public, dist / "public", dirs_exist_ok=True)

    ssg_builder(src, dist)

    console.print(
        f"[cyan]Project build at: [italic]{project_dir}/dist/[/italic][/cyan]"
    )


@app.command()
def serve(
    port: int = typer.Option(8000, help="The port to serve the files on."),
    host: str = typer.Option("127.0.0.1", help="The host interface to bind to."),
) -> None:
    """
    Serve the build from dist.
    """

    target_dir = Path.cwd() / "dist"
    if not target_dir.exists():
        console.print(
            f"[bold red]Error:[/bold red] The directory '{target_dir}' does not exist."
        )
        raise typer.Exit(code=1)

    # working dir -> dist/ for server
    os.chdir(target_dir)

    console.print(
        f"[bold green]🚀 Serving project at http://{host}:{port}[/bold green]"
    )
    console.print("[yellow]Press CTRL+C to stop[/yellow]\n")

    # Port reuse
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.ThreadingTCPServer(
            (host, port), PrettifiedHTTPRequestHandler
        ) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold red]👋 Server stopped by user.[/bold red]")
        raise typer.Exit(0) from None


@app.command()
def deploy(
    provide: str = typer.Option(
        "github", help="Site Hosting Provider defaults to GitHub."
    ),
) -> None:
    """Scaffold workflow and push code. GitHub handles the rest via gh-pages automatically."""

    if provide == "github":
        gh_deploy()
