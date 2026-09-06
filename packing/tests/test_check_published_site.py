"""The live-site check's parsing, on fixtures: the network half is not a unit of the gate."""

from __future__ import annotations

from devtools.check_published_site import SERVED, pdf_pages, repository_links
from devtools.render_explainer import COMPOSITE_ASSETS, MARKDOWN_OUTPUT, REPO_URL
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT


def test_repository_links_are_read_from_markup_and_markdown_but_not_from_scripts() -> None:
    sha = "0123456789abcdef0123456789abcdef01234567"
    text = (
        f'<a href="{REPO_URL}/blob/{sha}/packing/a.py">a</a>\n'
        f"[atlas]({REPO_URL}/tree/{sha}/packing/atlas/known-best/)\n"
        f'<script>const u = "{REPO_URL}/blob/main/packing/hidden.py";</script>\n'
        f"plain {REPO_URL}/blob/main/README.md text\n"
    )
    assert repository_links(text) == {
        ("blob", sha, "packing/a.py"),
        ("tree", sha, "packing/atlas/known-best"),
        ("blob", "main", "README.md"),
    }


def test_pdf_pages_counts_page_objects_and_refuses_what_is_not_a_pdf() -> None:
    pdf = b"%PDF-1.7\n1 0 obj << /Type /Pages /Kids [2 0 R 3 0 R] >> endobj\n"
    pdf += b"2 0 obj << /Type /Page >> endobj\n3 0 obj << /Type/Page >> endobj\n%%EOF"
    assert pdf_pages(pdf) == 2
    assert pdf_pages(b"<html>not a pdf</html>") == 0


def test_the_served_files_are_the_markdown_edition_the_pdf_and_the_composite_assets() -> None:
    assert SERVED[0] == MARKDOWN_OUTPUT.name
    assert SERVED[1] == PDF_OUTPUT.name
    assert set(SERVED[2:]) == {asset.name for asset in COMPOSITE_ASSETS}
