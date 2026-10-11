#!/usr/bin/env python3
"""Measure what the large generated assets cost: to build, and to keep in git.

Two questions, each a command rather than a paragraph someone wrote once (`OR-1`):

- `--timings` runs every build a release draws, one at a time, each in a process of its
  own, and reports its wall time beside the CPU time the process and the children it
  reaped were charged. Wall time alone says little on a loaded machine, so the load
  average is read before and after each build and printed with it. Nothing tracked is
  written: the atlas drawings and exports are made in memory and dropped, the pages go
  to `--scratch`, and the explainer goes to `packing/site/`, which is ignored. What a
  redraw costs is `composites from witnesses` and the two export phases together.
- `--history` reads what the re-pin commits cost the repository: for each of the last
  `--count` commits on `--ref` whose subject matches `--grep`, the bytes of every blob
  it added, as git stores a blob before packing and as the pack holds it now, and what
  each composite's drawing changed: nothing but its stamp, its frame, or a card.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.measure_release_assets --list
    uv run --frozen --all-extras --group dev python -m devtools.measure_release_assets --timings
    uv run --frozen --all-extras --group dev python -m devtools.measure_release_assets \
        --timings --only atlas --json attic/release-assets.json
    uv run --frozen --all-extras --group dev python -m devtools.measure_release_assets --history

The CPU figure is a lower bound, as `devtools.cpu_durations` says of its own: a
descendant its parent never waited for is charged to nobody this process can read.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
MODULE = "devtools.measure_release_assets"

#: The composite family: what a re-stamp rewrites. Repository-relative, as git names it.
COMPOSITE_FAMILY = re.compile(
    r"packing/atlas/known-best/(?:known-best-1-\d+[^/]*\.(?:svg|png|pdf)"
    r"|square-packings-\d+-\d{8}\.pdf)\Z"
)
#: The one text node a re-stamp is meant to change, whatever it says.
STAMP_NODE = re.compile(r'(<text\b[^>]*data-feature="release-stamp"[^>]*>)[^<]*(</text>)')
DEFAULT_GREP = "re-pin DATA_REVISION"


@dataclass(frozen=True)
class Phase:
    """One build, and how to run it: a module's own command, or a callable named here."""

    name: str
    group: str
    what: str
    #: Arguments after `python -m`, with `{scratch}` standing for the scratch directory.
    command: tuple[str, ...]


@dataclass(frozen=True)
class Reading:
    """What one build cost on this machine, now."""

    name: str
    group: str
    wall_seconds: float
    cpu_seconds: float
    load_before: float
    load_after: float
    returncode: int


def _atlas_rebuild() -> None:
    """Every case and both composite SVGs, rebuilt from their sources and held in memory.

    What the whole `--check` pays before it compares anything, and what a re-stamp paid
    until 2026-10-01, when `--update` drew the composites from a rebuilt corpus.
    """
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415
    from sqpack.workers import worker_count  # noqa: PLC0415

    workers = worker_count(atlas.CORPUS.count)
    outputs, _manifest = atlas.expected_outputs(workers)
    for canvas in atlas.COMPOSITES:
        identity = atlas.retained_identity(canvas.svg_path.read_text(encoding="utf-8"))
        atlas.expected_composite(canvas, identity, workers)
    print(f"rebuilt {len(outputs)} outputs and {len(atlas.COMPOSITES)} composites")


def _atlas_composites() -> None:
    """Both composite SVGs, drawn from the retained witnesses and dropped: the first
    part of `--update-composites`, which the two export phases complete."""
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415

    cases = atlas.retained_cases(atlas.CORPUS.numbers)
    for canvas in atlas.COMPOSITES:
        start = time.perf_counter()
        retained = canvas.svg_path.read_text(encoding="utf-8")
        drawn = atlas.render_known_best_summary_svg(
            [case for case in cases if case.frontier.n in set(canvas.spec.numbers)],
            canvas,
            atlas.retained_identity(retained),
        )
        print(
            f"{canvas.svg_path.name}: {len(drawn):,} characters, "
            f"{'the retained drawing' if drawn == retained else 'NOT the retained drawing'}, "
            f"{time.perf_counter() - start:.2f}s"
        )


def _atlas_rasters() -> None:
    """Every PNG of both composites, drawn from the retained SVG and dropped."""
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415

    for canvas in atlas.resolved_composites():
        svg_text = canvas.svg_path.read_text(encoding="utf-8")
        for export in canvas.rasters:
            start = time.perf_counter()
            drawn = atlas.png_export_bytes(export, svg_text)
            print(
                f"{export.path.name}: {len(drawn):,} bytes, {time.perf_counter() - start:.2f}s"
            )


def _atlas_pdfs() -> None:
    """Both composite PDFs, drawn from the retained SVG and dropped."""
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415
    from devtools import render_composite_pdf  # noqa: PLC0415

    for canvas in atlas.COMPOSITES:
        start = time.perf_counter()
        drawn = render_composite_pdf.render_pdf_bytes(canvas.spec.stem)
        print(
            f"{canvas.spec.pdf_name}: {len(drawn):,} bytes, {time.perf_counter() - start:.2f}s"
        )


def _site_pages(scratch: Path) -> None:
    """The site's own pages, result overviews, case record files, forwarders and
    link-preview card, as `preview_site.build` writes them."""
    from devtools import render_overview, social_card  # noqa: PLC0415

    pages = render_overview.render_all()
    fragments = render_overview.result_fragments()
    records = render_overview.case_records()
    forwarders = render_overview.forwarder_pages()
    render_overview.write_site(scratch, [*pages, *fragments, *records, *forwarders])
    card = social_card.write(scratch)
    print(
        f"wrote {len(pages)} pages, {len(fragments)} result overviews, "
        f"{len(records)} case records, {len(forwarders)} forwarders and {card.name}"
    )


def _preview_explainer(scratch: Path) -> None:
    from devtools import preview_site  # noqa: PLC0415

    preview_site.build_lower_bounds_explainer(scratch)


#: The builds that are a function here rather than a module's command.
INTERNAL: dict[str, Callable[[Path], None]] = {
    "atlas-rebuild": lambda _scratch: _atlas_rebuild(),
    "atlas-composites": lambda _scratch: _atlas_composites(),
    "atlas-rasters": lambda _scratch: _atlas_rasters(),
    "atlas-pdfs": lambda _scratch: _atlas_pdfs(),
    "site-pages": _site_pages,
    "preview-explainer": _preview_explainer,
}


def _internal(name: str) -> tuple[str, ...]:
    return (MODULE, "--run", name, "--scratch", "{scratch}")


PHASES: tuple[Phase, ...] = (
    Phase(
        "re-pin",
        "contributor",
        "release_pin --check: reads git and the pin, as --update does before it writes",
        ("devtools.release_pin", "--check"),
    ),
    Phase(
        "release pin and stamp tests",
        "contributor",
        "tests/test_release.py: what holds the pinned data revision to git",
        ("pytest", "-q", "-p", "no:cacheprovider", "tests/test_release.py"),
    ),
    Phase(
        "composite check, no rebuild",
        "contributor",
        "build_known_best_atlas --check-composites: the retained composites against "
        "the release and the figure record",
        ("devtools.build_known_best_atlas", "--check-composites"),
    ),
    Phase(
        "atlas records and sample",
        "atlas",
        "build_known_best_atlas --check --sample: the pull request's stand-in",
        ("devtools.build_known_best_atlas", "--check", "--sample"),
    ),
    Phase(
        "atlas rebuild",
        "atlas",
        "324 cases and both composite SVGs from their sources, in memory: --update, and "
        "what a re-stamp paid before 2026-10-01",
        _internal("atlas-rebuild"),
    ),
    Phase(
        "composites from witnesses",
        "atlas",
        "both composite SVGs from the retained witnesses: --update-composites, less exports",
        _internal("atlas-composites"),
    ),
    Phase(
        "atlas PNG exports",
        "atlas",
        "the four rasters, drawn by cairo from the retained SVGs",
        _internal("atlas-rasters"),
    ),
    Phase(
        "atlas PDF exports",
        "atlas",
        "the two PDFs, drawn by cairo from the retained SVGs",
        _internal("atlas-pdfs"),
    ),
    Phase(
        "explainer page",
        "papers",
        "render_n11_lower_bounds_explainer --prepare-math, into packing/site/",
        ("devtools.render_n11_lower_bounds_explainer", "--prepare-math"),
    ),
    Phase(
        "explainer PDF",
        "papers",
        "render_n11_lower_bounds_explainer_pdf --update, from the page above",
        ("devtools.render_n11_lower_bounds_explainer_pdf", "--update"),
    ),
    Phase(
        "threshold-bound review page",
        "papers",
        "render_n11_threshold_bound_review, HTML and Markdown only",
        (
            "devtools.render_n11_threshold_bound_review",
            "--site",
            "{scratch}/n11-threshold-page",
        ),
    ),
    Phase(
        "threshold-bound review page and PDF",
        "papers",
        "render_n11_threshold_bound_review --pdf",
        (
            "devtools.render_n11_threshold_bound_review",
            "--site",
            "{scratch}/n11-threshold",
            "--pdf",
        ),
    ),
    Phase(
        "optimality paper page",
        "papers",
        "render_n11_optimality_review, HTML and Markdown only",
        (
            "devtools.render_n11_optimality_review",
            "--site",
            "{scratch}/n11-optimality-page",
        ),
    ),
    Phase(
        "optimality paper page and PDF",
        "papers",
        "render_n11_optimality_review --pdf",
        (
            "devtools.render_n11_optimality_review",
            "--site",
            "{scratch}/n11-optimality",
            "--pdf",
        ),
    ),
    Phase(
        "preview: explainer",
        "preview",
        "preview_site's first build: the explainer page and its assets",
        _internal("preview-explainer"),
    ),
    Phase(
        "preview: site pages",
        "preview",
        "preview_site's second build: render_overview's pages, result overviews and "
        "forwarders, and the link-preview card",
        _internal("site-pages"),
    ),
    Phase(
        "preview: workbench",
        "preview",
        "preview_site's third build: workbench_tools.build_site",
        ("workbench_tools.build_site", "--out", "{scratch}/workbench"),
    ),
    Phase(
        "preview: threshold-bound review",
        "preview",
        "preview_site's fourth build: the threshold-bound review with its PDF",
        (
            "devtools.render_n11_threshold_bound_review",
            "--site",
            "{scratch}/n11-threshold",
            "--pdf",
        ),
    ),
    Phase(
        "preview: optimality paper",
        "preview",
        "preview_site's fifth build: the optimality paper with its PDF",
        (
            "devtools.render_n11_optimality_review",
            "--site",
            "{scratch}/n11-optimality",
            "--pdf",
        ),
    ),
)


def selected(only: Sequence[str]) -> tuple[Phase, ...]:
    """The phases whose name or group contains one of `only`; all of them for none."""
    if not only:
        return PHASES
    chosen = tuple(
        phase
        for phase in PHASES
        if any(text.lower() in f"{phase.group} {phase.name}".lower() for text in only)
    )
    if not chosen:
        raise SystemExit(f"--only {list(only)!r} names no phase; see --list")
    return chosen


def measure(phase: Phase, scratch: Path, log: Path) -> Reading:
    """Run one phase in a process of its own and read what the kernel charged it.

    `os.wait4` rather than `subprocess.run`, because it returns the child's own usage:
    the difference of two `RUSAGE_CHILDREN` readings would also be charged with any
    earlier child reaped in between.
    """
    command = [sys.executable, "-m", *(part.format(scratch=scratch) for part in phase.command)]
    load_before = os.getloadavg()[0]
    with log.open("ab") as output:
        output.write(f"\n== {phase.name}: {' '.join(command)}\n".encode())
        output.flush()
        start = time.perf_counter()
        process = subprocess.Popen(
            command, cwd=PACKING, stdout=output, stderr=subprocess.STDOUT
        )
        _pid, status, usage = os.wait4(process.pid, 0)
        wall = time.perf_counter() - start
        process.returncode = os.waitstatus_to_exitcode(status)
    return Reading(
        name=phase.name,
        group=phase.group,
        wall_seconds=round(wall, 2),
        cpu_seconds=round(usage.ru_utime + usage.ru_stime, 2),
        load_before=round(load_before, 2),
        load_after=round(os.getloadavg()[0], 2),
        returncode=process.returncode,
    )


def _git(*arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(REPO), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return done.stdout


def timings(only: Sequence[str], scratch: Path, receipt: Path | None) -> int:
    scratch.mkdir(parents=True, exist_ok=True)
    log = scratch / "measure-release-assets.log"
    log.write_bytes(b"")
    cpus = os.process_cpu_count() or 1
    head = _git("rev-parse", "HEAD").strip()
    print(f"machine: {cpus} cpus, load average {os.getloadavg()[0]:.2f}; source {head[:12]}")
    print(f"log: {log}")
    print(f"{'phase':<34} {'wall s':>9} {'cpu s':>9} {'load':>13}  exit")
    readings: list[Reading] = []
    for phase in selected(only):
        reading = measure(phase, scratch, log)
        readings.append(reading)
        load = f"{reading.load_before:.1f}->{reading.load_after:.1f}"
        print(
            f"{reading.name:<34} {reading.wall_seconds:>9.2f} {reading.cpu_seconds:>9.2f} "
            f"{load:>13}  {reading.returncode}",
            flush=True,
        )
    for group in dict.fromkeys(reading.group for reading in readings):
        members = [reading for reading in readings if reading.group == group]
        print(
            f"{'total: ' + group:<34} {sum(r.wall_seconds for r in members):>9.2f} "
            f"{sum(r.cpu_seconds for r in members):>9.2f}"
        )
    if receipt is not None:
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(
            json.dumps(
                {
                    "source": head,
                    "cpus": cpus,
                    "measured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "readings": [asdict(reading) for reading in readings],
                },
                indent=2,
            )
            + "\n"
        )
        print(f"receipt: {receipt}")
    return 1 if any(reading.returncode for reading in readings) else 0


@dataclass(frozen=True)
class CommitCost:
    """What one commit added to the repository."""

    commit: str
    date: str
    files: int
    family_files: int
    blob_bytes: int
    packed_bytes: int
    family_blob_bytes: int
    family_packed_bytes: int
    #: The composite SVGs in which a card changed: a bound, a badge, a square.
    redrawn: tuple[str, ...]
    #: The composite SVGs whose frame changed -- the title, the dateline, the legend, a
    #: footer sentence -- in anything but the stamp, and no card.
    reframed: tuple[str, ...] = ()

    @property
    def drawing(self) -> str:
        """What the commit changed in the drawings, in the words the table prints."""
        if self.redrawn:
            return "cards: " + ", ".join(self.redrawn)
        if self.reframed:
            return "frame, no card: " + ", ".join(self.reframed)
        return "stamp only"


#: Where a composite's cards begin: everything ahead of the first is its frame.
FIRST_CARD = '<g data-feature="packing-card"'


def frame_and_cards(svg_text: str) -> tuple[str, str]:
    """A composite cut in two: its frame, with the stamp emptied, and its cards."""
    frame, mark, cards = without_stamp(svg_text).partition(FIRST_CARD)
    return frame, mark + cards


def without_stamp(svg_text: str) -> str:
    """A composite with its stamp emptied, so two that differ only there compare equal."""
    return STAMP_NODE.sub(r"\1\2", svg_text)


def _blob_sizes(names: Sequence[str]) -> dict[str, tuple[int, int]]:
    """Each blob's size as an object and the bytes it occupies where git stores it now."""
    if not names:
        return {}
    done = subprocess.run(
        (
            "git",
            "-C",
            str(REPO),
            "cat-file",
            "--batch-check=%(objectname) %(objectsize) %(objectsize:disk)",
        ),
        input="\n".join(names) + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    sizes = {}
    for line in done.stdout.splitlines():
        name, size, disk = line.split()
        sizes[name] = (int(size), int(disk))
    return sizes


def commit_cost(commit: str) -> CommitCost:
    """The blobs `commit` added over its parent, and what its composites changed.

    A commit with no parent added everything in it. Merges are not read: `history`
    leaves them out, since a merge adds no blob its parents did not.
    """
    changed = []
    for line in _git(
        "diff-tree", "-r", "--root", "--no-commit-id", "--raw", "--no-abbrev", commit
    ).splitlines():
        meta, path = line.split("\t", 1)
        _old_mode, _new_mode, old, new, status = meta.lstrip(":").split()
        if status[0] != "D":
            changed.append((path, old, new))
    sizes = _blob_sizes([new for _path, _old, new in changed])
    family = [entry for entry in changed if COMPOSITE_FAMILY.search(entry[0])]
    redrawn = []
    reframed = []
    for path, old, new in family:
        if not path.endswith(".svg") or set(old) == {"0"}:
            continue
        frame, cards = frame_and_cards(_git("cat-file", "blob", old))
        new_frame, new_cards = frame_and_cards(_git("cat-file", "blob", new))
        if cards != new_cards:
            redrawn.append(Path(path).name)
        elif frame != new_frame:
            reframed.append(Path(path).name)
    return CommitCost(
        commit=commit[:9],
        date=_git("show", "-s", "--format=%ad", "--date=format:%m-%d %H:%M", commit).strip(),
        files=len(changed),
        family_files=len(family),
        blob_bytes=sum(sizes[new][0] for _path, _old, new in changed),
        packed_bytes=sum(sizes[new][1] for _path, _old, new in changed),
        family_blob_bytes=sum(sizes[new][0] for _path, _old, new in family),
        family_packed_bytes=sum(sizes[new][1] for _path, _old, new in family),
        redrawn=tuple(redrawn),
        reframed=tuple(reframed),
    )


def history(ref: str, grep: str, count: int, paths: Sequence[str], receipt: Path | None) -> int:
    commits = _git(
        "log", ref, f"--grep={grep}", f"-{count}", "--no-merges", "--format=%H", "--", *paths
    ).split()
    if not commits:
        raise SystemExit(f"no commit on {ref} matches {grep!r}")
    touching = f" and touching {', '.join(paths)}" if paths else ""
    print(f"{len(commits)} commits on {ref} matching {grep!r}{touching}, newest first")
    print(
        f"{'commit':<10} {'when':<12} {'files':>5} {'blob bytes':>12} {'packed':>11} "
        f"{'family':>6} {'family bytes':>13} {'packed':>11}  drawing"
    )
    costs = [commit_cost(commit) for commit in commits]
    for cost in costs:
        print(
            f"{cost.commit:<10} {cost.date:<12} {cost.files:>5} {cost.blob_bytes:>12,} "
            f"{cost.packed_bytes:>11,} {cost.family_files:>6} {cost.family_blob_bytes:>13,} "
            f"{cost.family_packed_bytes:>11,}  {cost.drawing}"
        )
    stamp_only = sum(1 for cost in costs if not cost.redrawn and not cost.reframed)
    reframed = sum(1 for cost in costs if cost.reframed and not cost.redrawn)
    print(
        f"total: {sum(c.blob_bytes for c in costs):,} blob bytes "
        f"({sum(c.packed_bytes for c in costs):,} as packed now), of which the composite "
        f"family is {sum(c.family_blob_bytes for c in costs):,} "
        f"({sum(c.family_packed_bytes for c in costs):,} as packed now)"
    )
    print(
        f"{stamp_only} of {len(costs)} changed nothing in a drawing but its stamp; "
        f"{reframed} changed a frame (title, dateline, legend or footer) and no card; "
        f"{len(costs) - stamp_only - reframed} changed a card"
    )
    print("repository, for scale:")
    print("  " + "\n  ".join(_git("count-objects", "-vH").strip().splitlines()))
    if receipt is not None:
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(
            json.dumps(
                {"ref": ref, "grep": grep, "commits": [asdict(cost) for cost in costs]},
                indent=2,
            )
            + "\n"
        )
        print(f"receipt: {receipt}")
    return 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--timings", action="store_true", help="run and time every build")
    mode.add_argument("--history", action="store_true", help="read what re-pins cost git")
    mode.add_argument("--list", action="store_true", help="name the phases --timings runs")
    mode.add_argument("--run", choices=sorted(INTERNAL), help=argparse.SUPPRESS)
    command.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="TEXT",
        help="with --timings: phases whose group or name contains TEXT; repeatable",
    )
    command.add_argument(
        "--scratch",
        type=Path,
        default=Path(tempfile.gettempdir()) / "squares-release-assets",
        help="where the pages and the log are written; reused between runs",
    )
    command.add_argument("--json", type=Path, help="also write the readings here")
    command.add_argument("--ref", default="origin/main", help="with --history: the branch")
    command.add_argument("--grep", default=DEFAULT_GREP, help="with --history: the subject")
    command.add_argument("--count", type=int, default=30, help="with --history: how many")
    command.add_argument(
        "--path",
        action="append",
        default=[],
        metavar="PATHSPEC",
        help="with --history: only commits that changed this path; repeatable. With "
        "--grep '' and the composite SVGs, this lists every commit that redrew one",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.list:
        for phase in PHASES:
            print(f"{phase.group:<12} {phase.name:<34} {phase.what}")
        return 0
    if arguments.run:
        INTERNAL[arguments.run](arguments.scratch.resolve())
        return 0
    if arguments.history:
        return history(
            arguments.ref, arguments.grep, arguments.count, arguments.path, arguments.json
        )
    return timings(arguments.only, arguments.scratch.resolve(), arguments.json)


if __name__ == "__main__":
    raise SystemExit(main())
