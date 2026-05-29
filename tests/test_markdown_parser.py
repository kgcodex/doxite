from pathlib import Path

from bs4 import BeautifulSoup

from doxite.node.markdown_parser import MarkdownParser

FIXTURE_DIR_MD = Path("tests/fixtures/markdown")
FIXTURE_DIR_HTML = Path("tests/fixtures/html")
FIXTURE_DIR_DEBUG = Path("tests/fixtures/debug")


def normalize_html(html: str) -> str:
    return BeautifulSoup(html, "html.parser").prettify()


def render_markdown(md_file: Path) -> str:
    parser = MarkdownParser(md_file)

    return "".join(node.to_html() for node in parser.parse_markdown())


def save_debug(
    file_name: str, actual_html: str, prettified_actual: str, prettified_expected: str
) -> None:
    generated_path = FIXTURE_DIR_DEBUG / f"{file_name}-generated.html"
    generated_prettified_path = (
        FIXTURE_DIR_DEBUG / f"{file_name}-generated-prettified.html"
    )
    expected_prettified_path = FIXTURE_DIR_DEBUG / f"{file_name}-actual-prettified.html"

    FIXTURE_DIR_DEBUG.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_path.write_text(
        actual_html,
        encoding="utf-8",
    )

    generated_prettified_path.write_text(
        prettified_actual,
        encoding="utf-8",
    )

    expected_prettified_path.write_text(
        prettified_expected,
        encoding="utf-8",
    )


def run_fixture_test(file_name: str) -> None:
    md_path = FIXTURE_DIR_MD / f"{file_name}.md"
    html_path = FIXTURE_DIR_HTML / f"{file_name}.html"

    actual_html = render_markdown(md_path)
    expected_html = html_path.read_text(encoding="utf-8")

    prettified_actual = normalize_html(actual_html)
    prettified_expected = normalize_html(expected_html)

    save_debug(file_name, actual_html, prettified_actual, prettified_expected)

    assert prettified_actual == prettified_expected


def test_blockquote() -> None:
    run_fixture_test("blockquote")


def test_code_block() -> None:
    run_fixture_test("code_block")


def test_code_shielding() -> None:
    run_fixture_test("code_shielding")


def test_eof_code_block() -> None:
    run_fixture_test("eof_code_block")


def test_headings() -> None:
    run_fixture_test("headings")


def test_inline() -> None:
    run_fixture_test("inline")


def test_ordered_list() -> None:
    run_fixture_test("ordered_list")


def test_paragraph() -> None:
    run_fixture_test("paragraph")


def test_seperated_list() -> None:
    run_fixture_test("seperated_list")


def test_unordered_list() -> None:
    run_fixture_test("unordered_list")


def test_combined() -> None:
    run_fixture_test("combined")
