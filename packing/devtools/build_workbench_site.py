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

**It builds from the retained spike**, and that is a deliberate, temporary arrangement. The
spike is excluded from the lint floor and is not project code; the video plan's later phases
re-implement it under project conventions. Publishing it now is worth more than waiting for
that, provided the record says plainly which it is -- so the page carries a banner naming
itself a prototype.

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
SPIKE = ROOT / "atlas/known-best/video/spikes/v2-transitions"
OUT = ROOT / "site/workbench"

RENDER_INPUTS = (
    Path(__file__),
    SPIKE / "build_candidate.py",
    SPIKE / "template.html",
    SPIKE / "assets/workbench.css",
    SPIKE / "assets/workbench.js",
    SPIKE / "transition-stats.json",
    ROOT / "atlas/known-best/manifest.json",
)
"""Everything the page is built from. The Pages workflow's path filter has to cover this
list, and `test_the_pages_filter_covers_every_render_input` is what says so -- which is what
stops a published page going stale when the data under it moves."""

BANNER = (
    '<div style="background:#fff8e1;border-bottom:1px solid #e8d9a0;padding:.55rem 1rem;'
    'font:13px/1.4 system-ui;color:#5a4a1a">'
    "<strong>Prototype.</strong> This workbench is a retained spike, not project code: it "
    "is excluded from the repository's lint floor and its animation model is still moving. "
    'Figures it draws are not evidence. <a href="/" style="color:#5a4a1a">The explainer</a> '
    "is the published work.</div>"
)

EXTERNAL = re.compile(
    r"""(?:<script[^>]+\bsrc=|<link[^>]+\bhref=|@import\b|url\((?!['"]?data:))""",
    re.IGNORECASE,
)


def build(out: Path) -> str:
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
        page = (Path(scratch) / "workbench.html").read_text(encoding="utf-8")

    reaching_out = EXTERNAL.findall(page)
    if reaching_out:
        msg = (
            f"the workbench references {len(reaching_out)} resource(s) outside itself; "
            "a page served from Pages has to carry everything it needs"
        )
        raise ValueError(msg)

    marked = page.replace("<body>", f"<body>{BANNER}", 1)
    if BANNER not in marked:
        msg = "could not place the prototype banner; the page has no <body> to mark"
        raise ValueError(msg)

    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(marked, encoding="utf-8")
    return marked


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true", help="rebuild and require byte equality")
    o = ap.parse_args()

    first = build(o.out)
    if o.check:
        again = build(o.out)
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
