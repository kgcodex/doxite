import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console

console = Console()

app = typer.Typer()


def gh_deploy() -> None:
    # Generate the Workflow File
    console.print("[yellow]🔨 Creating GitHub Actions deployment template...[/yellow]")

    workflow_dir = Path.cwd() / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_file = workflow_dir / "deploy.yml"

    deploy_yml = Path(__file__).parent.parent / "template" / "deploy.yml"
    shutil.copyfile(deploy_yml, workflow_file)

    # Commit and push the automation assets
    console.print(
        "[yellow]📦 Committing and pushing deployment configuration to GitHub...[/yellow]"
    )

    try:
        # current branch name
        branch_cmd = ["git", "branch", "--show-current"]
        current_branch = subprocess.run(
            branch_cmd, capture_output=True, text=True, check=True
        ).stdout.strip()

        # Add, commit, and push
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "doxite deploy: deploying to gh-pages"],
            capture_output=True,
        )

        push_result = subprocess.run(
            ["git", "push", "origin", current_branch], capture_output=True, text=True
        )
        if push_result.returncode != 0:
            console.print(
                f"[bold red]Failed to push code to branch '{current_branch}'.[/bold red]"
            )
            console.print(f"[dim]{push_result.stderr.strip()}[/dim]")
            raise typer.Exit(code=1)

        console.print(
            "\n[bold green]🚀 Deployment Configuration pushed successfully.[/bold green]"
        )
        # Site URL
        live_url = get_github_pages_url()
        if live_url:
            console.print(
                f"👉 [bold cyan]Site Live at: [link={live_url}]{live_url}[/link][/bold cyan]"
            )
        else:
            console.print(
                "👉 [bold cyan]Site Live at: https://<your-username>.github.io/<your-repo>/[/bold cyan]"
            )

    except Exception as e:
        console.print(f"[bold red]Error running git operations:[/bold red] {e}")
        raise typer.Exit(code=1) from None


def get_github_pages_url() -> str:
    """Extracts username and repo from git remote to build the public Pages URL."""
    try:
        cmd = ["git", "config", "--get", "remote.origin.url"]
        url = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        ).stdout.strip()

        # Clean up SSH or HTTPS URL formats
        url = url.replace("git@github.com:", "").replace("https://github.com/", "")
        if url.endswith(".git"):
            url = url[:-4]

        parts = url.split("/")
        if len(parts) >= 2:
            owner, repo = parts[-2], parts[-1]
            # GitHub Pages standard URL layout
            return f"https://{owner}.github.io/{repo}/"
    except Exception:
        pass
    return ""
