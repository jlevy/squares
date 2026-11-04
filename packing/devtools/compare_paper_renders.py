"""Render the papers a record change could reach and say whether any output moved.

`devtools.check_release_impact` asks a change to a paper's inputs for a reviewed
no-public-change record (`packing/release-records/no-public-change/`), whose reason
states what was rendered and compared. Lanes wrote that comparison by hand each time
(#886 among them): render each paper into an empty site directory twice from the tree,
once more with the baseline's bytes of the changed inputs swapped in, and compare every
output byte for byte. This tool is that measurement (OR-1).

It renders each paper named with its own renderer at the fixed link revision
`0000000000000000000000000000000000000000`, so that a commit hash never differs between
renders: twice from the working tree, which shows the render is deterministic here, and
once with each ``--path`` replaced by its bytes at ``--baseline`` (`git show`), restored
afterwards whatever happens. A paper is unchanged when the three renders write the same
file names with the same bytes. The math passes need Chromium, named by
``SQPACK_CHROMIUM`` as the renderers read it. It runs no checker and decides no bound;
the record it supports is the reviewer's.

From `packing/`::

    SQPACK_CHROMIUM=/usr/bin/google-chrome \\
        .venv/bin/python3 -m devtools.compare_paper_renders \\
        --baseline origin/main --path packing/frontier/results.yaml \\
        --path packing/frontier/source-coverage.yaml
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
#: The fixed revision every render links to, so that renders of different trees compare.
LINK_REVISION = "0" * 40
#: Each paper's renderer and the arguments after ``--site DIR``.
RENDERERS: dict[str, tuple[str, tuple[str, ...]]] = {
    "paper:n11-lower-bounds-explainer": (
        "devtools.render_n11_lower_bounds_explainer",
        ("--prepare-math",),
    ),
    "paper:n11-optimality-review": (
        "devtools.render_n11_optimality_review",
        ("--revision", LINK_REVISION),
    ),
    "paper:n11-threshold-bound-review": (
        "devtools.render_n11_threshold_bound_review",
        ("--revision", LINK_REVISION),
    ),
    "paper:square-packing-methods-survey": (
        "devtools.render_packing_methods",
        ("--revision", LINK_REVISION),
    ),
}


def tree_files(root: Path) -> dict[str, bytes]:
    """Every file under ``root``, by its relative path."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def differences(first: dict[str, bytes], second: dict[str, bytes]) -> list[str]:
    """The relative paths whose presence or bytes differ between two renders."""
    return sorted(
        name for name in set(first) | set(second) if first.get(name) != second.get(name)
    )


def render(paper: str, site: Path) -> None:
    """One paper into an empty site directory, by its own renderer."""
    module, extra = RENDERERS[paper]
    site.mkdir(parents=True, exist_ok=False)
    subprocess.run(
        [sys.executable, "-m", module, "--site", str(site), *extra],
        cwd=PACKING,
        check=True,
        capture_output=True,
    )


@contextmanager
def baseline_inputs(baseline: str, paths: Sequence[str]) -> Iterator[None]:
    """The baseline's bytes of each repository-relative path, restored on leaving."""
    saved = {path: (REPO / path).read_bytes() for path in paths}
    try:
        for path in paths:
            old = subprocess.run(
                ["git", "show", f"{baseline}:{path}"],
                cwd=REPO,
                check=True,
                capture_output=True,
            ).stdout
            (REPO / path).write_bytes(old)
        yield
    finally:
        for path, data in saved.items():
            (REPO / path).write_bytes(data)


def compare(baseline: str, paths: Sequence[str], papers: Sequence[str]) -> dict[str, dict]:
    """Each paper rendered twice here and once on the baseline's inputs, compared."""
    results: dict[str, dict] = {}
    with tempfile.TemporaryDirectory(prefix="compare-paper-renders-") as scratch:
        root = Path(scratch)
        for paper in papers:
            name = paper.removeprefix("paper:")
            render(paper, root / name / "first")
            render(paper, root / name / "second")
            with baseline_inputs(baseline, paths):
                render(paper, root / name / "baseline")
            first = tree_files(root / name / "first")
            second = tree_files(root / name / "second")
            old = tree_files(root / name / "baseline")
            results[paper] = {
                "files": len(first),
                "deterministic": differences(first, second),
                "against_baseline": differences(first, old),
            }
    return results


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--baseline", required=True, help="the revision to compare against")
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="a repository-relative input whose baseline bytes are swapped in; repeatable",
    )
    parser.add_argument(
        "--paper",
        action="append",
        choices=sorted(RENDERERS),
        help="a paper to render; repeatable (default: all four)",
    )
    args = parser.parse_args(argv)
    papers = args.paper or sorted(RENDERERS)
    results = compare(args.baseline, args.path, papers)
    unchanged = True
    for paper, result in results.items():
        same = not result["deterministic"] and not result["against_baseline"]
        unchanged &= same
        print(
            f"{paper}: {result['files']} files, "
            + (
                "byte-identical across the three renders"
                if same
                else f"not deterministic at {result['deterministic'][:5]}, "
                f"differs from the baseline at {result['against_baseline'][:5]}"
            )
        )
    return 0 if unchanged else 1


if __name__ == "__main__":
    raise SystemExit(main())
