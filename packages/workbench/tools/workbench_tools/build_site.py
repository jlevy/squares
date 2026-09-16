#!/usr/bin/env python3
"""Build the package workbench as a standalone page under `site/workbench/`.

GitHub Pages serves `packing/site` whole, so a subdirectory is a URL: this puts the
workbench at `/workbench/` beside the explainer at `/`, without touching the explainer.
That separation is the point -- the explainer is already published and may be linked from
elsewhere, so nothing here moves `site/index.html`.

The page is already self-contained, which is what makes it deployable at all: one file,
no external script, stylesheet or font, so it works from any static host. This tool exists
to put it where the Pages artifact will find it, to check that self-containment rather than
assume it, to give it a policy under which the browser refuses any network request, and to
declare its inputs so the workflow rebuilds when they move.

The page no longer carries a banner calling itself unchecked, because it is checked. It
carries one quiet line saying what a reader does have to know -- that the animation model is
still moving, so a number it draws is not evidence -- and that line goes when the model
settles, which is a different question from where the code lives.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m workbench_tools.build_site
    uv run --frozen --all-extras --group dev python -m workbench_tools.build_site --check
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from workbench_tools.self_contained import assert_self_contained_html

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO = PACKAGE_ROOT.parents[1]
ROOT = REPO / "packing"
WORKBENCH_PACKAGE = PACKAGE_ROOT
OUT = ROOT / "site/workbench"

RENDER_INPUTS = (
    Path(__file__),
    ROOT / "devtools/render_explainer.py",
    ROOT / "src/sqpack/render",
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    Path(__file__).with_name("build_candidate.py"),
    Path(__file__).with_name("self_contained.py"),
    WORKBENCH_PACKAGE / "assets/template.html",
    WORKBENCH_PACKAGE / "assets/workbench.css",
    WORKBENCH_PACKAGE / "src/application.js",
    ROOT / "witnesses/known-best",
    ROOT / "atlas/known-best/rendering",
    ROOT / "atlas/known-best/manifest.json",
    ROOT / "atlas/known-best/composite-figure.json",
    REPO / "vendor/kpress",
    REPO / "package.json",
    REPO / "package-lock.json",
    REPO / ".node-version",
    WORKBENCH_PACKAGE / "package.json",
    WORKBENCH_PACKAGE / "src",
    WORKBENCH_PACKAGE / "tools/bundle-browser.ts",
    WORKBENCH_PACKAGE / "tools/build-assets.ts",
    WORKBENCH_PACKAGE / "tools/check-candidate-corpus.ts",
    WORKBENCH_PACKAGE / "tools/render-katex.ts",
    WORKBENCH_PACKAGE / "probes/bench-annealing.ts",
)
"""Everything the page is built from. The Pages workflow's path filter has to cover this
list, and `test_the_pages_filter_covers_every_render_input` is what says so -- which is what
stops a published page going stale when the data under it moves. The list is written by
hand, so `test_build_site_inputs.py` derives what this module and `build_candidate` name --
imports, modules run, paths joined, Node tools and their imports -- and requires this list
to cover it."""

NOTE = """<style>
#site-note {
  position: fixed; right: 12px; bottom: 8px; z-index: 30;
  font-family: var(--sans); font-size: 11px; line-height: 1.4;
  color: var(--quiet); text-align: right; pointer-events: none;
}
#site-note a { color: inherit; text-decoration: underline; pointer-events: auto; }
body.capture #site-note { display: none; }
</style>
<div id="site-note">
The animation model is still moving, so a number here is not evidence
&mdash; <a href="../">the explainer</a> is the published work.
</div>"""
"""The one thing a reader of the published page has to know, said once and quietly.

It is **injected here rather than written into the template** because it is a property of
the published page and not of the page. The relative link reaches the project root from
`/squares/workbench/`, from a local static server, and from any other deployment subpath.

Where it sits and how it looks are both deliberate, and both are corrections. It was a
full-width strip in warning yellow at the top of `<body>` -- which put it outside
`#viewport`, the absolutely-positioned element that covers the whole window, so it showed
through against the chrome rather than sitting above the page. Now it is fixed to the
bottom right in the page's own `--quiet` grey at 11px, in the corner the timing readout
does not use, and `pointer-events` stay off everywhere but the link so it cannot swallow a
drag. `body.capture` hides it, because a note about the page does not belong in a frame of
the video.
"""

#: What the published page may load, which is nothing from the network. Scripts and styles
#: are inline, fonts and images are `data:` URIs, and exports are `blob:` downloads, so the
#: page needs no source beyond those. `default-src 'none'` covers every fetch the
#: self-contained scan cannot recognise -- a URL assembled at run time, a worker, a socket.
#: The browser enforces it; `self_contained` is the build-time half (#125 F21).
#:
#: No `'unsafe-eval'`: the page does not evaluate strings, and the public page is not
#: loosened for test tooling. A checker that hands Playwright an expression-string predicate,
#: which Playwright compiles in the page, opens its context with `bypass_csp`, and
#: `check_page_policy` loads the page without it to hold this policy to what the page needs.
CONTENT_SECURITY_POLICY = (
    "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
    "img-src data: blob:; font-src data:; base-uri 'none'; form-action 'none'"
)
POLICY_META = f'<meta http-equiv="Content-Security-Policy" content="{CONTENT_SECURITY_POLICY}">'
HEAD = re.compile(r"<head(?:\s[^>]*)?>", re.IGNORECASE)

REVISION = re.compile(r"[0-9a-f]{40}")


def with_policy(page: str) -> str:
    """Put the page's Content-Security-Policy first in `<head>`.

    A policy delivered by `<meta>` governs only what follows it, so it opens the head,
    before the inline style and script it has to cover.
    """
    head = HEAD.search(page)
    if head is None:
        raise ValueError("could not place the page's security policy; the page has no <head>")
    return f"{page[: head.end()]}\n{POLICY_META}{page[head.end() :]}"


def source_revision() -> str:
    """The exact checkout revision whose sources the page embeds."""
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or REVISION.fullmatch(revision) is None:
        raise ValueError("could not determine the workbench source revision")
    return revision


def source_dirty() -> bool:
    """Whether the checkout carries changes beyond its stamped commit."""
    found = subprocess.run(
        ("git", "status", "--porcelain", "--untracked-files=all"),
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    if found.returncode != 0:
        raise ValueError("could not determine whether the workbench source is dirty")
    return bool(found.stdout.strip())


def build_metadata(revision: str) -> str:
    """The machine-readable source identity checked after deployment."""
    if REVISION.fullmatch(revision) is None:
        raise ValueError(f"invalid workbench source revision: {revision!r}")
    return f'<meta name="squares-workbench-revision" content="{revision}">'


def dirty_metadata(*, dirty: bool) -> str:
    """The conservative source-state marker consumed by capture receipts."""
    return f'<meta name="squares-workbench-dirty" content="{str(dirty).lower()}">'


def build(
    out: Path,
    *,
    revision: str | None = None,
    dirty: bool | None = None,
) -> str:
    """Generate the page and return its text, refusing anything that reaches outside itself."""
    with tempfile.TemporaryDirectory() as scratch:
        # Captured so a working build stays quiet, but reported on failure: `check=True`
        # alone raises a CalledProcessError whose message is the exit status and the
        # argv, with the child's traceback sealed inside the exception object. A CI log
        # then says only "returned non-zero exit status 1", which is how a hard-coded
        # absolute path in the generator survived a whole run unnamed.
        built = subprocess.run(
            [
                sys.executable,
                "-m",
                "workbench_tools.build_candidate",
                "--out",
                scratch,
                "--all",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if built.returncode != 0:
            msg = (
                f"workbench_tools.build_candidate exited {built.returncode}\n"
                f"--- stderr ---\n{built.stderr.strip() or '(empty)'}\n"
                f"--- stdout ---\n{built.stdout.strip() or '(empty)'}"
            )
            raise ValueError(msg)
        candidate = Path(scratch) / "workbench.html"
        checked = subprocess.run(
            (
                "node",
                str(WORKBENCH_PACKAGE / "tools/check-candidate-corpus.ts"),
                str(candidate),
            ),
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        if checked.returncode != 0:
            msg = (
                f"generated workbench corpus check exited {checked.returncode}\n"
                f"--- stderr ---\n{checked.stderr.strip() or '(empty)'}\n"
                f"--- stdout ---\n{checked.stdout.strip() or '(empty)'}"
            )
            raise ValueError(msg)
        page = candidate.read_text(encoding="utf-8")

    assert_self_contained_html(page)

    identity = "\n".join(
        (
            build_metadata(revision or source_revision()),
            dirty_metadata(dirty=source_dirty() if dirty is None else dirty),
        )
    )
    marked = with_policy(page).replace("</head>", f"{identity}\n</head>", 1)
    if identity not in marked:
        raise ValueError("could not stamp the page; it has no </head> to close")

    # At the end of the body, so it is inside `#viewport`'s stacking context and after the
    # stylesheet that defines the custom properties it borrows.
    marked = marked.replace("</body>", f"{NOTE}</body>", 1)
    if NOTE not in marked:
        msg = "could not place the page's note; the page has no </body> to close"
        raise ValueError(msg)

    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(marked, encoding="utf-8")
    return marked


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true", help="rebuild and require byte equality")
    ap.add_argument("--revision", help="full source commit to stamp (default: checkout HEAD)")
    o = ap.parse_args()

    revision = o.revision or source_revision()
    dirty = source_dirty()
    first = build(o.out, revision=revision, dirty=dirty)
    if o.check:
        again = build(o.out, revision=revision, dirty=dirty)
        if again != first:
            msg = (
                "the workbench did not reproduce itself; a published page must be deterministic"
            )
            raise ValueError(msg)
        print(f"deterministic, self-contained, {len(first) / 1024 / 1024:.1f} MB")
        return 0

    print(f"{o.out / 'index.html'}: {len(first) / 1024 / 1024:.1f} MB, no external references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
