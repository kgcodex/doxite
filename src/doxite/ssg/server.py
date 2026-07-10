import logging
from http.server import SimpleHTTPRequestHandler
from typing import Any

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, show_path=False, markup=True)],
)
logger = logging.getLogger("http_server")


class PrettifiedHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler to prettify HTTP server logs."""

    def log_message(self, format: str, *args: Any) -> None:

        if len(args) == 3 and not isinstance(args[0], int):
            request_line, status_code, _ = args
            status_str = str(status_code)

            if status_str.startswith("2"):
                status = f"[green]{status_str}[/green]"
            elif status_str.startswith("3"):
                status = f"[yellow]{status_str}[/yellow]"
            else:
                status = f"[red]{status_str}[/red]"

            logger.info(f"{status} — {request_line}")

        # Error/Warning logs match: format = "code %d, message %s"
        else:
            # Safely build the string using standard positional arguments
            # to bypass strict %d formatting restrictions.
            try:
                formatted_msg = format % args

            except TypeError:
                # Fallback if argument types don't align perfectly
                formatted_msg = " ".join(str(arg) for arg in args)

            if "404" in formatted_msg:
                logger.error(f"[red]404[/red] — [red]{formatted_msg}[/red]")
            else:
                logger.error(f"[red]ERROR[/red] — [red]{formatted_msg}[/red]")
