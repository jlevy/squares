#!/usr/bin/env python3
"""Build the workbench as a standalone page under `site/workbench/`.

GitHub Pages serves `packing/site` whole, so a subdirectory is a URL: this puts the
workbench at `/workbench/` beside the explainer at `/`, without touching the explainer.
That separation is the point -- the explainer is already published and may be linked from
elsewhere, so nothing here moves `site/index.html`.

The page is already self-contained, which is what makes it deployable at all: one file,
no external script, stylesheet or font, so it works from any static host. This tool exists
to put it where the Pages artifact will find it, to check that self-containment rather than
assume it, and to declare its inputs so the workflow rebuilds when they move.

**It builds from the retained spike tree**, which is deliberate and temporary -- though
less of one than it was. The page's own code meets the project's floors now: its JavaScript
and CSS are at zero under Biome, its script type-checks, and its checkers run in
`packing-validate`. What has not happened is the move; the generator and the instruments
still sit under `atlas/known-best/video/spikes/`, which the video plan's Phase 6E finishes.

So the page no longer carries a banner calling itself unchecked, because it is checked. It
carries one quiet line saying what a reader does have to know -- that the animation model is
still moving, so a number it draws is not evidence -- and that line goes when the model
settles, which is a different question from where the code lives.

Usage, from `packing/`:
    uv run --frozen python -m devtools.build_workbench_site
    uv run --frozen python -m devtools.build_workbench_site --check
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
SPIKE = ROOT / "atlas/known-best/video/spikes/v2-transitions"
WORKBENCH_PACKAGE = REPO / "packages/workbench"
OUT = ROOT / "site/workbench"

RENDER_INPUTS = (
    Path(__file__),
    ROOT / "devtools/render_explainer.py",
    ROOT / "src/sqpack/render",
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    SPIKE / "build_candidate.py",
    SPIKE / "template.html",
    SPIKE / "assets/workbench.css",
    SPIKE / "assets/workbench.js",
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
    WORKBENCH_PACKAGE / "probes/bench-annealing.ts",
)
"""Everything the page is built from. The Pages workflow's path filter has to cover this
list, and `test_the_pages_filter_covers_every_render_input` is what says so -- which is what
stops a published page going stale when the data under it moves."""

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

EXTERNAL = re.compile(
    r"""(?:<script[^>]+\bsrc=|<link[^>]+\bhref=|@import\b|url\((?!['"]?data:))""",
    re.IGNORECASE,
)
REVISION = re.compile(r"[0-9a-f]{40}")


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


def build_metadata(revision: str) -> str:
    """The machine-readable source identity checked after deployment."""
    if REVISION.fullmatch(revision) is None:
        raise ValueError(f"invalid workbench source revision: {revision!r}")
    return f'<meta name="squares-workbench-revision" content="{revision}">'


def build(out: Path, *, revision: str | None = None) -> str:
    """Generate the page and return its text, refusing anything that reaches outside itself."""
    with tempfile.TemporaryDirectory() as scratch:
        # Captured so a working build stays quiet, but reported on failure: `check=True`
        # alone raises a CalledProcessError whose message is the exit status and the
        # argv, with the child's traceback sealed inside the exception object. A CI log
        # then says only "returned non-zero exit status 1", which is how a hard-coded
        # absolute path in the generator survived a whole run unnamed.
        built = subprocess.run(
            [sys.executable, str(SPIKE / "build_candidate.py"), "--out", scratch, "--all"],
            check=False,
            capture_output=True,
            text=True,
        )
        if built.returncode != 0:
            msg = (
                f"{SPIKE.name}/build_candidate.py exited {built.returncode}\n"
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

    reaching_out = EXTERNAL.findall(page)
    if reaching_out:
        msg = (
            f"the workbench references {len(reaching_out)} resource(s) outside itself; "
            "a page served from Pages has to carry everything it needs"
        )
        raise ValueError(msg)

    identity = build_metadata(revision or source_revision())
    marked = page.replace("</head>", f"{identity}\n</head>", 1)
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
    first = build(o.out, revision=revision)
    if o.check:
        again = build(o.out, revision=revision)
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
