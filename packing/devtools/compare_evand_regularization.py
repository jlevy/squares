#!/usr/bin/env python3
"""Compare Evan Daniel's regularization lists with this project's regularized layer.

The assessment of Evan Daniel's ``search/regularize`` process
(``docs/project/research/research-2026-10-11-evand-regularization-assessment.md``) states
what the upstream best-choice lists change and how that meets this project's
``regularize_axis_components/2`` layer. Those figures are this module's output, so they
can be re-derived rather than trusted. Three subcommands, from ``packing/``:

``crosstab [--best PATH] [--index PATH] [--json]``
    Tally the upstream lists (``search/regularize/lists/best.json``: levels, variants,
    orientations, input sources, rotation groups, symmetries) and cross them with the
    project index (``atlas/known-best/regularized/index.json``): which records each side
    changes, and how the project's regularized, unchanged and refused records fall by
    upstream level. ``--best`` defaults to the copy vendored at its pin under
    ``vendor/evand-regularize/`` (its README names the commit); pass another path to
    tally the lists at a different revision.

``refused-tilts [--index PATH] [--json]``
    Classify each record the project layer refuses by the tilts its known-best witness
    holds: every tilted square at exactly 45 degrees, some other tilt, or axis-aligned
    only. Reads only committed records.

``angles CERT [CERT ...] [--json]``
    Each square's rotation ``2 atan(t)`` in degrees, and the same folded into (-45, 45],
    in one or more of Evan Daniel's exact certificates (``n S`` then ``x y t`` rows, plain
    or gzipped), indexed from 0 as the source's ``free`` lists are. A square written just
    past 45 degrees folds to just above -45; its class is still ``45``.

**The answers refuse what they cannot stand behind.** An index whose entries do not
recount to its own ``totals``, a list or index that misses or repeats a count, two inputs
that do not cover the same counts, and a tilt that lies within ``AMBIGUOUS_DEGREES`` of 0
or 45 without being within ``TOLERANCE_DEGREES`` of it are each refused with exit status
2 rather than counted one way or the other. A tilt is measured at ``DIGITS`` significant
digits from the witness's own scalars through `sqpack.witness.materialize_witness`, which
reads every scalar kind the record holds, the number-field witness included.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mpmath as mp

from devtools.evand_exact_certificates import CertificateError, parse
from sqpack.witness import materialize_witness
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
INDEX = REPO / "packing/atlas/known-best/regularized/index.json"
#: Upstream's best-choice list as vendored at its pin (vendor/evand-regularize/README.md).
VENDORED_BEST = REPO / "vendor/evand-regularize/search/regularize/lists/best.json"
INDEX_CONTRACT = "packing.squares:RegularizedAtlasIndex/v1"
STATUSES = ("regularized", "unchanged", "refused")
LEVELS = (0, 1, 2, 3)
#: Working precision for a tilt, in significant digits.
DIGITS = 50
#: A tilt this close to 0 or 45 degrees is that angle.
TOLERANCE_DEGREES = mp.mpf("1e-12")
#: A tilt further than the tolerance from 0 or 45 degrees but within this is refused: the
#: record holds a near-axis or near-45 pose that this module will not round either way.
AMBIGUOUS_DEGREES = mp.mpf("1e-6")
_GROUPS = re.compile(r"([1-9]\d*) -> ([1-9]\d*)")


class InputRefusedError(ValueError):
    """An input this module will not count from."""


@dataclass(frozen=True, slots=True)
class Pick:
    """One count's row of the upstream best-choice list, as far as the tallies need it."""

    n: int
    level: int
    variant: str
    orientation_g: int
    groups_before: int
    groups_after: int
    symmetry: tuple[int, ...]
    input: str


# --- reading ----------------------------------------------------------------------


def _counts_once(counts: Iterable[int], where: str) -> list[int]:
    seen = sorted(counts)
    repeated = sorted({n for n in seen if seen.count(n) > 1})
    if repeated:
        raise InputRefusedError(f"{where}: counts {repeated} appear more than once")
    return seen


def read_best(rows: Sequence[Mapping[str, Any]]) -> dict[int, Pick]:
    """The upstream list's rows by count, refusing a row the tallies cannot read."""
    picks: list[Pick] = []
    for place, row in enumerate(rows):
        where = f"best.json row {place}"
        try:
            n, level, variant = row["n"], row["level"], row["variant"]
            orientation, groups, symmetry, source = (
                row["orientation_g"],
                row["groups"],
                row["symmetry"],
                row["input"],
            )
        except KeyError as missing:
            raise InputRefusedError(f"{where}: no {missing} field") from None
        if not isinstance(n, int) or n < 1:
            raise InputRefusedError(f"{where}: n = {n!r} is not a positive integer")
        if level not in LEVELS:
            raise InputRefusedError(f"n = {n}: level {level!r} is not one of {LEVELS}")
        if not isinstance(orientation, int) or not 0 <= orientation <= 7:
            raise InputRefusedError(f"n = {n}: orientation_g {orientation!r} is not 0..7")
        match = _GROUPS.fullmatch(str(groups))
        if match is None:
            raise InputRefusedError(f"n = {n}: groups {groups!r} is not `A -> B`")
        if not isinstance(symmetry, list) or not all(
            isinstance(g, int) and 1 <= g <= 7 for g in symmetry
        ):
            raise InputRefusedError(f"n = {n}: symmetry {symmetry!r} is not a list of 1..7")
        if not isinstance(variant, str) or not isinstance(source, str):
            raise InputRefusedError(f"n = {n}: variant and input must be strings")
        picks.append(
            Pick(
                n=n,
                level=level,
                variant=variant,
                orientation_g=orientation,
                groups_before=int(match.group(1)),
                groups_after=int(match.group(2)),
                symmetry=tuple(symmetry),
                input=source,
            )
        )
    _counts_once((pick.n for pick in picks), "best.json")
    return {pick.n: pick for pick in picks}


def read_index(document: Mapping[str, Any]) -> dict[int, Mapping[str, Any]]:
    """The project index's entries by count, refusing one that disagrees with its totals."""
    if document.get("contract") != INDEX_CONTRACT:
        raise InputRefusedError(f"index.json: contract is not {INDEX_CONTRACT}")
    entries = document["entries"]
    _counts_once((entry["n"] for entry in entries), "index.json")
    statuses = Counter(entry["status"] for entry in entries)
    unknown = sorted(set(statuses) - set(STATUSES))
    if unknown:
        raise InputRefusedError(f"index.json: unknown statuses {unknown}")
    totals = document["totals"]
    if dict(statuses) != totals["statuses"] or len(entries) != totals["records"]:
        raise InputRefusedError(
            f"index.json: entries recount to {dict(statuses)} over {len(entries)}, "
            f"its totals say {totals['statuses']} over {totals['records']}"
        )
    refusals = Counter(
        entry["refusal"]["kind"] for entry in entries if entry["status"] == "refused"
    )
    if dict(refusals) != totals["refusals"]:
        raise InputRefusedError(
            f"index.json: refusals recount to {dict(refusals)}, "
            f"its totals say {totals['refusals']}"
        )
    return {entry["n"]: entry for entry in entries}


def load_index(path: Path = INDEX) -> dict[int, Mapping[str, Any]]:
    return read_index(json.loads(path.read_text(encoding="utf-8")))


# --- the cross-tabulation ---------------------------------------------------------


def crosstab(
    best: Mapping[int, Pick], index: Mapping[int, Mapping[str, Any]]
) -> dict[str, Any]:
    """What the upstream lists change, and how that meets the project's layer."""
    if set(best) != set(index):
        raise InputRefusedError(
            f"best.json and index.json cover different counts: {sorted(set(best) ^ set(index))}"
        )
    status = {n: entry["status"] for n, entry in index.items()}
    upstream_changed = {n for n, pick in best.items() if pick.level > 0}
    by_status = {name: {n for n in index if status[n] == name} for name in STATUSES}
    cells = Counter((status[n], best[n].level) for n in index)
    return {
        "records": len(best),
        "upstream": {
            "levels": {
                str(level): sum(p.level == level for p in best.values()) for level in LEVELS
            },
            "changed": len(upstream_changed),
            "variants": dict(sorted(Counter(p.variant for p in best.values()).items())),
            "fewest_counts": sorted(n for n, p in best.items() if p.variant == "fewest"),
            "orientation_kept": sum(p.orientation_g == 0 for p in best.values()),
            "orientation_changed": sum(p.orientation_g != 0 for p in best.values()),
            "inputs": dict(sorted(Counter(p.input for p in best.values()).items())),
            "rotation_groups_before": sum(p.groups_before for p in best.values()),
            "rotation_groups_after": sum(p.groups_after for p in best.values()),
            "fewer_groups_at": sum(p.groups_after < p.groups_before for p in best.values()),
            "symmetry_imposed_at": sum(bool(p.symmetry) for p in best.values()),
        },
        "project": {name: len(members) for name, members in by_status.items()},
        "status_by_upstream_level": {
            f"{name}/{level}": cells[(name, level)]
            for name in STATUSES
            for level in LEVELS
            if cells[(name, level)]
        },
        "project_changed_also_changed_upstream": len(
            by_status["regularized"] & upstream_changed
        ),
        "project_changed_unchanged_upstream": sorted(
            by_status["regularized"] - upstream_changed
        ),
        "refused_changed_upstream": len(by_status["refused"] & upstream_changed),
        "refused_unchanged_upstream": sorted(by_status["refused"] - upstream_changed),
        "unchanged_changed_upstream": sorted(by_status["unchanged"] & upstream_changed),
        "upstream_changes_beyond_project": len(upstream_changed - by_status["regularized"]),
    }


# --- tilts ------------------------------------------------------------------------


def fold_degrees(degrees: Any) -> Any:
    """An angle folded into (-45, 45] degrees: a square's rotation modulo its symmetry."""
    folded = mp.fmod(degrees + 45, 90)
    if folded <= 0:
        folded += 90
    return folded - 45


def tilt_class(tilt: Any, where: str) -> str:
    """``axis``, ``45`` or ``other`` for a tilt in [0, 45], refusing an ambiguous one."""
    for target, name in ((0, "axis"), (45, "45")):
        distance = abs(tilt - target)
        if distance <= TOLERANCE_DEGREES:
            return name
        if distance <= AMBIGUOUS_DEGREES:
            raise InputRefusedError(
                f"{where}: a tilt {mp.nstr(distance, 3)} degrees from {target} is neither "
                f"that angle within {mp.nstr(TOLERANCE_DEGREES, 3)} nor clear of it by "
                f"{mp.nstr(AMBIGUOUS_DEGREES, 3)}"
            )
    return "other"


def witness_tilts(path: Path) -> list[Any]:
    """Each square's tilt in [0, 45] degrees, from one edge of its materialized corners."""
    witness = safe_load(path.read_text(encoding="utf-8"))["witness"]
    squares, _side = materialize_witness(witness, digits=DIGITS)
    with mp.workdps(DIGITS):
        return [
            abs(
                fold_degrees(
                    mp.degrees(
                        mp.atan2(square[1][1] - square[0][1], square[1][0] - square[0][0])
                    )
                )
            )
            for square in squares
        ]


def record_class(classes: Iterable[str]) -> str:
    """``all-45`` when every tilted square is at 45, ``axis-only`` when none is tilted."""
    present = set(classes)
    if present <= {"axis"}:
        return "axis-only"
    return "all-45" if "other" not in present else "other-tilt"


def refused_tilts(index: Mapping[int, Mapping[str, Any]], root: Path = REPO) -> dict[str, Any]:
    """The refused records by the tilts their witnesses hold."""
    by_class: dict[str, list[int]] = {"all-45": [], "other-tilt": [], "axis-only": []}
    other_tilts: dict[str, list[str]] = {}
    for n in sorted(index):
        entry = index[n]
        if entry["status"] != "refused":
            continue
        tilts = witness_tilts(root / entry["source"]["witness"])
        classes = [tilt_class(tilt, f"n = {n}, square {k + 1}") for k, tilt in enumerate(tilts)]
        kind = record_class(classes)
        by_class[kind].append(n)
        if kind == "other-tilt":
            distinct = {
                str(mp.nstr(t, 6)) for t, c in zip(tilts, classes, strict=True) if c == "other"
            }
            other_tilts[str(n)] = sorted(distinct, key=mp.mpf)
    return {
        "refused": sum(len(counts) for counts in by_class.values()),
        "counts": {kind: len(counts) for kind, counts in by_class.items()},
        "records": by_class,
        "other_tilts_degrees": other_tilts,
        "tolerance_degrees": mp.nstr(TOLERANCE_DEGREES, 3),
        "ambiguous_degrees": mp.nstr(AMBIGUOUS_DEGREES, 3),
    }


def certificate_angles(path: Path) -> dict[str, Any]:
    """Each square's folded rotation in one of Evan Daniel's certificates."""
    raw = path.read_bytes()
    text = (gzip.decompress(raw) if path.suffix == ".gz" else raw).decode("utf-8")
    try:
        certificate = parse(text)
    except CertificateError as error:
        raise InputRefusedError(f"{path}: {error}") from None
    rows: list[dict[str, Any]] = []
    with mp.workdps(DIGITS):
        for place, pose in enumerate(certificate.poses):
            t = mp.mpf(pose.t.numerator) / pose.t.denominator
            rotation = mp.degrees(2 * mp.atan(t))
            folded = fold_degrees(rotation)
            rows.append(
                {
                    "square": place,
                    "rotation_degrees": mp.nstr(rotation, 8),
                    "folded_degrees": mp.nstr(folded, 8),
                    "class": tilt_class(abs(folded), f"{path}, square {place}"),
                }
            )
    return {"certificate": str(path), "n": certificate.n, "squares": rows}


# --- the command ------------------------------------------------------------------


def _table(result: Mapping[str, Any]) -> str:
    upstream, project = result["upstream"], result["project"]
    levels = "/".join(str(upstream["levels"][str(level)]) for level in LEVELS)
    statuses = "/".join(str(project[name]) for name in STATUSES)
    cells = ", ".join(f"{cell}: {n}" for cell, n in result["status_by_upstream_level"].items())
    groups = (upstream["rotation_groups_before"], upstream["rotation_groups_after"])
    lines = [
        f"records: {result['records']}",
        f"upstream levels 0/1/2/3: {levels}; changed (level > 0): {upstream['changed']}",
        f"upstream variants: {upstream['variants']}; fewest at {upstream['fewest_counts']}",
        (
            f"upstream orientation kept {upstream['orientation_kept']}, "
            f"changed {upstream['orientation_changed']}"
        ),
        f"upstream inputs: {upstream['inputs']}",
        (
            f"upstream rotation groups {groups[0]} -> {groups[1]}, fewer at "
            f"{upstream['fewer_groups_at']} records; symmetry imposed at "
            f"{upstream['symmetry_imposed_at']}"
        ),
        f"project regularized/unchanged/refused: {statuses}",
        f"project status x upstream level: {cells}",
        (
            "project-changed records upstream also changes: "
            f"{result['project_changed_also_changed_upstream']} of {project['regularized']}"
        ),
        (
            f"refused records upstream changes: {result['refused_changed_upstream']} of "
            f"{project['refused']} (not {result['refused_unchanged_upstream']})"
        ),
        f"unchanged records upstream changes: {result['unchanged_changed_upstream']}",
        f"upstream changes beyond the project's: {result['upstream_changes_beyond_project']}",
    ]
    return "\n".join(lines)


def _tilts_table(result: Mapping[str, Any]) -> str:
    counts, records = result["counts"], result["records"]
    lines = [
        f"refused records: {result['refused']}",
        f"every tilted square at 45 degrees: {counts['all-45']} {records['all-45']}",
        f"some other tilt: {counts['other-tilt']} {records['other-tilt']}",
        f"axis-aligned only: {counts['axis-only']} {records['axis-only']}",
        "other tilts, degrees: "
        + "; ".join(f"{n}: {', '.join(t)}" for n, t in result["other_tilts_degrees"].items()),
    ]
    return "\n".join(lines)


def _angles_table(result: Mapping[str, Any]) -> str:
    lines = [f"{result['certificate']} (n = {result['n']}): square, rotation, folded, class"]
    lines += [
        f"  {row['square']:>3}  {row['rotation_degrees']:>14}  {row['folded_degrees']:>14}  "
        f"{row['class']}"
        for row in result["squares"]
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    tab = commands.add_parser("crosstab", help="the upstream lists against the project index")
    tab.add_argument(
        "--best", type=Path, default=VENDORED_BEST, help="upstream lists/best.json"
    )
    tab.add_argument("--index", type=Path, default=INDEX)
    tab.add_argument("--json", action="store_true")
    tilts = commands.add_parser("refused-tilts", help="refused records by their witness tilts")
    tilts.add_argument("--index", type=Path, default=INDEX)
    tilts.add_argument("--json", action="store_true")
    angles = commands.add_parser("angles", help="each square's rotation in certificates")
    angles.add_argument("certificates", type=Path, nargs="+")
    angles.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "crosstab":
            best = read_best(json.loads(args.best.read_text(encoding="utf-8")))
            result: Any = crosstab(best, load_index(args.index))
            text = _table(result)
        elif args.command == "refused-tilts":
            result = refused_tilts(load_index(args.index))
            text = _tilts_table(result)
        else:
            result = [certificate_angles(path) for path in args.certificates]
            text = "\n".join(_angles_table(one) for one in result)
    except InputRefusedError as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=1, sort_keys=True) if args.json else text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
