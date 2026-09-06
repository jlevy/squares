#!/usr/bin/env python3
"""Check the explainer as GitHub Pages serves it, against the commit it should be built from.

`pages.yml` renders the page, its Markdown edition and its PDF from `main` and deploys
them. Nothing is checked in, so nothing in the repository says whether a deploy landed
or what the page it served links to; this asks the live site. From `packing/`:

    uv run --frozen --group dev python -m devtools.check_published_site --commit <sha>

With no `--commit` the checkout's `origin/main` is the expectation, which is the commit
the last deploy built from once `git fetch` has run. One line per check, `ok` or
`FAIL`, and the exit status is 0 only when every check passes:

- the page is served and carries the edition stamp `sqpack.release` names;
- every repository link in the page and in the Markdown edition names the expected
  commit, and each resolves on GitHub;
- the Markdown edition, the PDF and the composite assets are served beside the page,
  and the PDF is a PDF, its page count reported.

Network only, so nothing here is a step of the gate; `tests/test_check_published_site.py`
covers the parsing on fixtures.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Sequence

from devtools.render_explainer import (
    COMPOSITE_ASSETS,
    MARKDOWN_OUTPUT,
    OUTPUT,
    REPO,
    REPO_URL,
    SITE_URL,
)
from devtools.render_explainer_pdf import OUTPUT as PDF_OUTPUT
from sqpack.release import PUBLICATION_STATUS, PUBLICATION_VERSION

#: A link into this repository as GitHub spells one: the ref, then the path, under
#: `blob/` for a file and `tree/` for a directory.
REPOSITORY_LINK = re.compile(re.escape(REPO_URL) + r"/(blob|tree)/([^/\s\"<>)]+)/([^\s\"<>)]*)")

#: Every file the deploy serves beside `index.html`, by name.
SERVED = (
    MARKDOWN_OUTPUT.name,
    PDF_OUTPUT.name,
    *(asset.name for asset in COMPOSITE_ASSETS),
)

USER_AGENT = "squares-check-published-site (+https://github.com/jlevy/squares)"


def repository_links(text: str) -> set[tuple[str, str, str]]:
    """Every (kind, ref, path) the text links into the repository, scripts and styles aside."""
    markup = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return {
        (kind, ref, path.rstrip("/")) for kind, ref, path in REPOSITORY_LINK.findall(markup)
    }


def pdf_pages(data: bytes) -> int:
    """The number of page objects a PDF declares; 0 when the bytes are not a PDF."""
    if not data.startswith(b"%PDF"):
        return 0
    return len(re.findall(rb"/Type\s*/Page(?![s])", data))


def fetch(url: str, *, head: bool = False, timeout: float = 30.0) -> tuple[int, bytes]:
    """The status and body of a GET (or the status alone of a HEAD); 0 when unreachable."""
    if not url.startswith("https://"):
        raise ValueError(f"refusing to fetch a non-https URL: {url}")
    request = urllib.request.Request(
        url, method="HEAD" if head else "GET", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, b"" if head else response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except urllib.error.URLError:
        return 0, b""


def expected_commit() -> str:
    """`origin/main` as the checkout knows it, which is what the last deploy built from."""
    found = subprocess.run(
        ("git", "rev-parse", "origin/main"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        raise SystemExit("no --commit given and origin/main cannot be resolved here")
    return found.stdout.strip()


def check(site: str, commit: str, *, timeout: float) -> list[tuple[bool, str]]:
    """Every check as (passed, line), in the order they are printed."""
    results: list[tuple[bool, str]] = []
    site = site.rstrip("/") + "/"

    status, page = fetch(site + OUTPUT.name, timeout=timeout)
    text = page.decode("utf-8", errors="replace")
    results.append(
        (status == 200, f"page {site}{OUTPUT.name}: HTTP {status}, {len(page)} bytes")
    )
    edition = " ".join(
        part for part in (PUBLICATION_STATUS, f"{PUBLICATION_VERSION}-{commit[:8]}") if part
    )
    stamped = edition in text
    results.append(
        (
            stamped,
            f"edition stamp {edition!r} is {'' if stamped else 'not '}on the page",
        )
    )

    status, markdown = fetch(site + MARKDOWN_OUTPUT.name, timeout=timeout)
    results.append(
        (
            status == 200,
            f"Markdown edition {MARKDOWN_OUTPUT.name}: HTTP {status}, {len(markdown)} bytes",
        )
    )

    links = repository_links(text) | repository_links(
        markdown.decode("utf-8", errors="replace")
    )
    refs = sorted({ref for _, ref, _ in links})
    results.append(
        (
            refs == [commit],
            f"repository links name {refs} against expected {commit}"
            if links
            else "no repository links found",
        )
    )
    for kind, ref, path in sorted(links):
        url = f"{REPO_URL}/{kind}/{ref}/{path}"
        status, _ = fetch(url, head=True, timeout=timeout)
        results.append((status == 200, f"link HTTP {status}: {url}"))

    for name in SERVED:
        if name == MARKDOWN_OUTPUT.name:
            continue
        head_only = name != PDF_OUTPUT.name
        status, body = fetch(site + name, head=head_only, timeout=timeout)
        line = f"served {name}: HTTP {status}"
        ok = status == 200
        if name == PDF_OUTPUT.name:
            pages = pdf_pages(body)
            ok = ok and pages > 0
            line += f", {len(body)} bytes, {pages} pages"
        results.append((ok, line))
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--site", default=SITE_URL, help=f"the deployed site (default {SITE_URL})"
    )
    parser.add_argument("--commit", help="the full commit the deploy should have built from")
    parser.add_argument("--timeout", type=float, default=30.0, help="seconds per request")
    args = parser.parse_args(argv)
    commit = args.commit or expected_commit()
    results = check(args.site, commit, timeout=args.timeout)
    failed = 0
    for passed, line in results:
        print(f"{'ok  ' if passed else 'FAIL'} {line}", flush=True)
        failed += not passed
    print(f"{len(results) - failed} of {len(results)} checks passed", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
