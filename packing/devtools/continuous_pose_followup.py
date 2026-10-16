"""Check a reported continuous-pose measure certificate kept outside Git, and price it.

wand125/square-packing's ``continuous_n28_L5745`` (commit 8530baf, 15 October 2026)
reports ``s(28) > 1149/200`` from a rectangle measure checked at every orientation, not
on a net: every closed square of side ``B`` in ``K = [0, L]^2``, at every centre and
every angle, is reported to capture mass at least ``tau``, and ``n tau > M`` then gives
``s(n) > L / B``. Two programs of the source decide that cover: its continuous-angle mode
of this repository's ``sqverify-fast`` crate (``sqverify_continuous``, "check1"), and a
driver around Guzhou0806's continuous-pose and integer-axis kernels of T-145
(``contpose_check3``, "check2"). The release asset that holds the candidate, both run
logs and the first program's source stays outside Git, as the fine-net assets of
`devtools.fine_net_followup` do; this tool reads a local copy of it beside the
certificate's documents from the pinned tree and writes the receipts a packet keeps.

- ``premises`` refuses the asset unless its size and SHA-256 are the pinned ones,
  unpacks it with `devtools.fine_net_followup`'s safe unpacker, lays the pinned
  documents beside it, and decides in exact rationals what needs no program of the
  source: the candidate's mass, rows and support; the claim's scalar chain
  (``X = L / B``, ``n tau - M``, ``L^2 - 2 B^2``, ``T^2 + 2T - 1``); each program's
  near-axis side ``A`` and containment margin ``B - A W(eps)``, by the rule each states;
  both check2 kernel inputs, regenerated here from the candidate with
  `devtools.audit_continuous_pose`'s builders (the pose input) and the dominated measure
  at the density scale the source chose (the axis input), against the digests the
  source's manifests and receipts name; the control candidate as the original with every
  mass times 985/1000; both run logs, root by root and slab by slab, against their
  summaries; the source digest of each program by the rule it states; and the sealed
  inner bundle against its ``files-sha256.json``. Files the packet pins by an identical
  copy elsewhere (``--record``) are laid from that copy. It decides no coverage.
- ``sample`` runs programs, one at a time and one thread each, and judges each run
  against the source's own log: chosen root boxes of ``sqverify_continuous``, the
  published control, and mutants with every mass scaled at one root, each recorded by
  where it was stopped (`mutant_outcome`); chosen slabs of a pose kernel on the input
  regenerated here; and an axis kernel on the regenerated main and control axis inputs.
  It prices a complete replay of each program from the ratio of this host's CPU to the
  source's on what it ran. A sample decides only what it ran and is not a replay; its
  status says so.

**What its author read** (an AI agent, Claude, the 15 October 2026 intake lane for the
n = 28 report, ``think-mq0k``): the certificate directory's documents at 8530baf
(``README.md``, ``REPRODUCE.md``, ``bundle.json``, ``ASSET.json``, ``files-sha256.json``,
``check1/summary.json``, ``check1/control-summary.json``, ``check2/manifest.json``,
``check2/src/README.md``, ``SPEC.md``, ``PROVENANCE.md``, ``CHANGES.md``,
``generator.py``, ``check.py``, ``make_control.py`` and the two kernels with their
``identity.h``), the asset's logs and receipts as data, and ``sqverify_continuous`` v4's
``build.rs``, ``main.rs``, and the head, premises and run function of ``slab.rs``, before
running it. The digests of check2's kernel inputs bind those inputs to the candidate
only if the builders here write the same bytes. The pose input is
`devtools.audit_continuous_pose`'s builder unchanged, on the conventions of the T-145
release's ``exact.py``; the axis input is that module's dominated measure at a density
scale chosen by the guard rule the source's ``generator.py`` states (coefficient total
below ``10^15``, evaluation bound below ``2^125``), which was read before
`axis_scale` was written. So this module shares with the source the density's
definition, its D4 order, the enclosure rule, the inward rounding and that guard rule,
and no code. Having read parts of ``sqverify_continuous``, its author is not clean-room
with respect to it, and should not write a first-party continuous-angle decider.

From ``packing/``::

    .venv/bin/python3 -m devtools.continuous_pose_followup premises \\
        --asset ASSET.tar.gz --sha256 HEX --bytes N --documents CERT_DIR \\
        --record PACKET/acquisition/sources.json --name continuous_n28_L5745 \\
        --n 28 --core 499/500 --claim 1149/200 --work WORK --out RECEIPT
    .venv/bin/python3 -m devtools.continuous_pose_followup sample \\
        --certificate WORK/certificates/continuous_n28_L5745 --n 28 --core 499/500 \\
        --claim 1149/200 --crate-binary CRATE --roots 0,1,2 --control \\
        --mutant-root 7 --mutant-scales 9999/10000,999/1000 \\
        --pose-binary POSE --slabs 0,14 --axis-binary AXIS --work SAMPLE --out RECEIPT
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.audit_clipped_corner_transfer import Density, Rect, area, d4_maps, image, merge
from devtools.audit_continuous_pose import (
    ENDPOINTS,
    RELEASE,
    Claim,
    Row,
    pose_input,
    quarter_terms,
)
from devtools.audit_wand125_declared_net import AuditError, load_json, require, utc_now
from devtools.fine_net_followup import (
    file_digest,
    inventory,
    lay_documents,
    sealed_bundle,
    unpack_asset,
)
from sqpack import retained_json

REPO = Path(__file__).resolve().parents[2]
#: The sealed inner bundle a continuous-pose directory ships.
BUNDLE_SUFFIX = "-continuous-bundle.tar.gz"
#: Where each program's source and logs sit in the certificate directory.
CHECK1_ARCHIVE = "check1/src/sqverify_continuous_v4.tgz"
CHECK1_LOG = "check1/run.jsonl.gz"
CHECK1_CONTROL_LOG = "check1/control.jsonl.gz"
CHECK2_SOURCE = "check2/src"
CHECK2_KERNELS = ("axis_integer_grid.cpp", "continuous_pose.cpp", "identity.h")
PREPUBLICATION = "verification/prepublication-receipt.json"
#: The control candidate and the factor the source states for it.
CONTROL = "control/candidate-mass0985.json"
CONTROL_FACTOR = Fraction(985, 1000)
#: The axis input's coordinate grid; the density scale is the source's choice.
GRID = 10**9
#: ``sqverify_continuous``'s defaults (main.rs): the branch-and-bound range of the
#: half-angle tangent, and the root boxes' interior cuts.
CRATE_EPS = Fraction(1, 10**7)
CRATE_LAST_T = Fraction(83, 200)
#: check2's slabs: integer numerators over this denominator.
SLAB_DENOMINATOR = 10**6
#: How long one sampled program may run before the sample is abandoned.
RUN_TIMEOUT = 3600
STATUS_HOLD = "EXACT_PREMISES_HOLD"
STATUS_FAIL = "EXACT_PREMISES_FAIL"


@dataclass(frozen=True, slots=True)
class Stated:
    """The claim as the source states it: the count, the core side, the threshold and
    the claimed side ``X = L / B``."""

    name: str
    n: int
    core: Fraction
    tau: Fraction
    claim: Fraction


@dataclass(frozen=True, slots=True)
class Check:
    name: str
    held: bool
    detail: str = ""


def text(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def extent(t: Fraction) -> Fraction:
    """``W(t) = cos + sin`` at half-angle tangent ``t``: a unit square's box side."""
    return (1 + 2 * t - t * t) / (1 + t * t)


def floor_div(p: int, q: int) -> int:
    return p // q


def ceil_div(p: int, q: int) -> int:
    return -(-p // q)


# --------------------------------------------------------------------------- the candidate


def read_candidate(raw: bytes, n: int) -> Density:
    """The candidate read exactly: its positive rows in file order, expanded through D4.

    Refused unless it states ``n``, has no point masses, every mass is nonnegative,
    every positive row is a nondegenerate rectangle in ``[0, L]^2``, and the masses sum
    to ``total_mass``. Each positive row of mass ``m`` on ``R`` puts ``m / (8 |R|)`` on
    each of its eight images, as both programs read it.
    """
    data = load_json(raw)
    require(data["n"] == n, f"the candidate is n = {data['n']}")
    require(data["points"] == [], "the candidate has point masses")
    side = Fraction(data["L"])
    rows: list[tuple[Rect, Fraction]] = []
    total = Fraction(0)
    for index, row in enumerate(data["rectangles"]):
        mass = Fraction(row["mass"])
        require(mass >= 0, f"row {index} has a negative mass")
        total += mass
        if mass == 0:
            continue
        x1, y1, x2, y2 = (Fraction(v) for v in row["rectangle"])
        require(
            0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side,
            f"row {index} is degenerate or outside [0, L]^2",
        )
        rows.append(((x1, y1, x2, y2), mass))
    require(total == Fraction(data["total_mass"]), "total_mass is not the sum of the masses")
    maps = d4_maps(side)
    terms = [(image(rect, f), w / (8 * area(rect))) for rect, w in rows for f in maps]
    return Density(
        sha256=hashlib.sha256(raw).hexdigest(),
        side=side,
        core=Fraction(data["B"]),
        n=n,
        listed=len(data["rectangles"]),
        rows=tuple(rows),
        terms=len(terms),
        merged=merge(terms),
    )


def mass(density: Density) -> Fraction:
    return sum((w for _, w in density.rows), Fraction(0))


def scaled_rows(original: Density, scaled: Density, factor: Fraction) -> bool:
    """Whether ``scaled`` is ``original`` with every mass times ``factor``, row by row."""
    return len(original.rows) == len(scaled.rows) and all(
        r == s and w * factor == v
        for (r, w), (s, v) in zip(original.rows, scaled.rows, strict=True)
    )


def mutant_bytes(raw: bytes, factor: Fraction) -> bytes:
    """The candidate with every mass and the total times ``factor``, exactly."""
    data = load_json(raw)
    for row in data["rectangles"]:
        row["mass"] = text(Fraction(row["mass"]) * factor)
    data["total_mass"] = text(Fraction(data["total_mass"]) * factor)
    return (json.dumps(data, indent=1) + "\n").encode()


# --------------------------------------------------------------------------- the premises


def crate_axis_side(core: Fraction, eps: Fraction) -> Fraction:
    """``sqverify_continuous``'s default ``A``: ``B / W(eps)`` rounded down to ``1/10^9``."""
    return Fraction(math.floor(core / extent(eps) * GRID), GRID)


def check2_axis_side(core: Fraction, eps: Fraction) -> Fraction:
    """check2's ``A``: the largest even multiple of ``1/10^9`` strictly below ``B / W(eps)``."""
    return Fraction(2 * (math.ceil(core / extent(eps) * GRID / 2) - 1), GRID)


def crate_cuts(eps: Fraction, last: Fraction) -> list[Fraction]:
    """``sqverify_continuous``'s default interior cuts of ``[eps, T]`` (main.rs)."""
    cuts = [Fraction(1, 10**5), Fraction(1, 10**4), Fraction(1, 10**3), Fraction(1, 200)]
    cuts += [Fraction(k, 200) for k in range(2, 83)]
    return [t for t in cuts if eps < t < last]


def scalar_chain(density: Density, stated: Stated) -> dict[str, Fraction]:
    """The claim's exact scalars."""
    side, core = density.side, stated.core
    return {
        "L": side,
        "B": core,
        "X": side / core,
        "M": mass(density),
        "counting_margin": stated.n * stated.tau - mass(density),
        "geometry_margin": side * side - 2 * core * core,
        "angle_coverage_polynomial": CRATE_LAST_T**2 + 2 * CRATE_LAST_T - 1,
    }


def axis_rows_at(density: Density, scale: int) -> list[Row]:
    """The dominated measure the axis kernel reads: each term in its order, support
    rounded inward to ``1/10^9`` and density rounded down to a multiple of ``1/scale``,
    keeping rows of positive area and density."""
    out: list[Row] = []
    for a, b, c, e, rho in quarter_terms(density):
        row = (
            ceil_div(a.numerator * GRID, a.denominator),
            ceil_div(b.numerator * GRID, b.denominator),
            floor_div(c.numerator * GRID, c.denominator),
            floor_div(e.numerator * GRID, e.denominator),
            floor_div(rho.numerator * scale, rho.denominator),
        )
        if row[0] < row[2] and row[1] < row[3] and row[4] > 0:
            out.append(row)
    return out


def axis_guards(rows: Sequence[Row], length: int, side: int) -> tuple[int, int, bool]:
    """The kernel's coefficient total, its evaluation bound and whether both guards hold
    (`weights < 10^15` and the bound below ``2^125``), as the source's generator states."""
    weights = sum(row[4] for row in rows)
    bound = 16 * weights * (2 * length + side // 2) ** 2
    return weights, bound, weights < 10**15 and bound < 2**125


def axis_scale(density: Density, side: Fraction) -> int:
    """The largest power of ten up to ``10^9`` at which both guards hold."""
    length = int(density.side * GRID)
    scale = GRID
    while not axis_guards(axis_rows_at(density, scale), length, int(side * GRID))[2]:
        require(scale > 1, "no density scale keeps the axis guards")
        scale //= 10
    return scale


def axis_bytes(density: Density, side: Fraction, tau: Fraction, scale: int) -> bytes:
    rows = axis_rows_at(density, scale)
    head = (
        f"{int(density.side * GRID)} {int(side * GRID)} {GRID} {scale} "
        f"{tau.numerator} {tau.denominator} {len(rows)}"
    )
    return ("\n".join([head, *(" ".join(map(str, row)) for row in rows)]) + "\n").encode()


def pose_bytes(density: Density, core: Fraction) -> bytes:
    """check2's ``certificate_input.txt``, by `devtools.audit_continuous_pose.pose_input`."""
    claim = Claim(n=density.n, L=density.side, B=core, X=density.side / core)
    return pose_input(density, claim, RELEASE)


def kernel_inputs(density: Density, stated: Stated, eps: Fraction) -> dict[str, Any]:
    """Both check2 kernel inputs regenerated here, with their digests and facts."""
    side = check2_axis_side(stated.core, eps)
    scale = axis_scale(density, side)
    pose = pose_bytes(density, stated.core)
    axis = axis_bytes(density, side, stated.tau, scale)
    rows = axis_rows_at(density, scale)
    weights, bound, held = axis_guards(rows, int(density.side * GRID), int(side * GRID))
    return {
        "certificate_input.txt": pose,
        "axis_input.txt": axis,
        "facts": {
            "terms": density.terms,
            "axis_terms": len(rows),
            "axis_side": text(side),
            "axis_density_denominator": scale,
            "axis_scale": str(scale * GRID * GRID),
            "axis_evaluation_bound": str(bound),
            "axis_weights": weights,
            "axis_guards_hold": held,
            "axis_containment_margin": text(stated.core - side * extent(eps)),
        },
    }


# --------------------------------------------------------------------------- the logs


def read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line, parse_float=str) for line in stream if line.strip()]


def log_row(rows: list[dict[str, Any]], kind: str) -> dict[str, Any]:
    """The log's first row of ``kind``; a log without one is refused, not a traceback."""
    found = next((r for r in rows if r.get("kind") == kind), None)
    if found is None:
        raise AuditError(f"the log has no {kind} row")
    return found


def crate_log_checks(
    rows: list[dict[str, Any]], density: Density, stated: Stated, *, control: bool
) -> list[Check]:
    """``sqverify_continuous``'s log against its own summary and the premises here."""
    premises = log_row(rows, "premises")["premises"]
    axis = log_row(rows, "axis-patch")
    roots = sorted((r for r in rows if r.get("kind") == "root"), key=lambda r: int(r["index"]))
    summary = log_row(rows, "sqverify-fast-continuous-summary/v1")
    side = crate_axis_side(stated.core, CRATE_EPS)
    ends = [CRATE_EPS, *crate_cuts(CRATE_EPS, CRATE_LAST_T), CRATE_LAST_T]
    spans = [[text(a), text(b)] for a, b in itertools.pairwise(ends)]
    expected = {
        "A": text(side),
        "B": text(stated.core),
        "L": text(density.side),
        "T": text(CRATE_LAST_T),
        "X": text(density.side / stated.core),
        "axis_containment_margin": text(stated.core - side * extent(CRATE_EPS)),
        "counting_margin": text(stated.n * stated.tau - mass(density)),
        "eps": text(CRATE_EPS),
        "input_sha256": density.sha256,
        "mass": text(mass(density)),
        "n": stated.n,
        "threshold": text(stated.tau),
    }
    stated_premises = {k: premises.get(k) for k in expected}
    verdict = "refused" if control else "verified"
    checks = [
        Check("premises as recomputed here", stated_premises == expected, json.dumps(expected)),
        Check(
            "near-axis containment A W(eps) <= B",
            stated.core - side * extent(CRATE_EPS) > 0,
            text(stated.core - side * extent(CRATE_EPS)),
        ),
        Check("roots are the default cuts of [eps, T]", [r["t"] for r in roots] == spans),
        Check("every root " + verdict, all(r["verdict"] == verdict for r in roots)),
        Check(
            "summary sums the roots",
            summary["nodes"] == sum(int(r["nodes"]) for r in roots)
            and summary["leaves"] == sum(int(r["leaves"]) for r in roots)
            and summary["roots"] == len(spans),
        ),
    ]
    if control:
        checks += [
            Check("summary REFUSED", summary["status"] == "REFUSED"),
            Check("axis patch refused", axis["verified"] is False),
            Check(
                "every root refused in the summary",
                summary["refused_roots"] == list(range(len(spans))),
            ),
        ]
    else:
        least = min(Fraction(float(r["min_certified_lower_bound"])) for r in roots)
        checks += [
            Check(
                "summary VERIFIED with the claim",
                summary["status"] == "VERIFIED"
                and summary["claim"] == f"s({stated.n}) > {text(stated.claim)}",
            ),
            Check(
                "axis patch verified at least tau",
                axis["verified"] is True
                and Fraction(float(axis["min_certified_lower_bound"])) >= stated.tau,
            ),
            Check(
                "every root's least bound at least tau", least >= stated.tau, str(float(least))
            ),
            Check(
                "every root a full binary cover (nodes = 2 leaves - 1)",
                all(int(r["nodes"]) == 2 * int(r["leaves"]) - 1 for r in roots),
            ),
        ]
    return checks


def slab_spans(endpoints: Sequence[int]) -> list[tuple[int, int]]:
    return list(itertools.pairwise(endpoints))


def check2_receipt_checks(
    receipt: dict[str, Any],
    manifest: dict[str, Any],
    stated: Stated,
    kernels: dict[str, str],
    *,
    control: bool,
) -> list[Check]:
    """check2's receipt against its manifest, its own acceptance rule and the pinned
    kernel sources."""
    files = manifest["files"]
    axis = receipt["axis"]["kernel"]
    minimum = Fraction(int(axis["minimum_numerator"]), int(axis["scale"]))
    checks = [
        Check("manifest bound to the receipt", receipt["manifest"] == manifest),
        Check(
            "axis input is the manifest's",
            receipt["axis"]["input_sha256"] == files["axis_input.txt"]
            and axis["input_sha256"] == files["axis_input.txt"],
        ),
        Check("axis scale is the manifest's", axis["scale"] == manifest["axis_scale"]),
        Check(
            "build sources are the pinned kernels",
            receipt["build"]["configuration"]["sources"] == kernels,
        ),
    ]
    if control:
        return [
            *checks,
            Check(
                "REFUSED at the axis",
                receipt["status"] == "REFUSED"
                and axis["status"] == "AXIS_TEST_REFUSED"
                and minimum < stated.tau,
                text(minimum),
            ),
            Check("no slab run", receipt["slabs"] == []),
        ]
    endpoints = [int(v) for v in receipt["endpoints"]]
    slabs = sorted(receipt["slabs"], key=lambda s: int(s["index"]))
    budget = slabs[0]["arguments"][5] if slabs else None
    argv = [
        [
            str(lo),
            str(hi),
            str(SLAB_DENOMINATOR),
            str(stated.tau.numerator),
            str(stated.tau.denominator),
            budget,
        ]
        for lo, hi in slab_spans(endpoints)
    ]
    last = Fraction(endpoints[-1], SLAB_DENOMINATOR)
    kernels_out = [s["kernel"] for s in slabs]
    least = min((Fraction(float(k["lower_bound"])) for k in kernels_out), default=Fraction(0))
    return [
        *checks,
        Check(
            "VERIFIED with the claim",
            receipt["status"] == "VERIFIED"
            and receipt["claim"] == f"s({stated.n}) > {text(stated.claim)}",
        ),
        Check("default endpoints", tuple(endpoints) == ENDPOINTS),
        Check(
            "last t past tan(pi/8)",
            last * last + 2 * last - 1 >= 0,
            text(last * last + 2 * last - 1),
        ),
        Check("every slab run with its arguments", [s["arguments"] for s in slabs] == argv),
        Check(
            "every slab accepted and verified",
            all(
                s["accepted"] and k["status"] == "verified"
                for s, k in zip(slabs, kernels_out, strict=True)
            ),
        ),
        Check(
            "every slab on the manifest's pose input",
            all(
                s["input_sha256"] == files["certificate_input.txt"] == k["input_sha256"]
                for s, k in zip(slabs, kernels_out, strict=True)
            ),
        ),
        Check(
            "every slab a full binary cover (nodes = 2 leaves - 1)",
            all(int(k["nodes"]) == 2 * int(k["leaves"]) - 1 for k in kernels_out),
        ),
        Check("every slab's least bound at least tau", least >= stated.tau, str(float(least))),
        Check(
            "axis proved at least tau",
            axis["status"] == "AXIS_COVERAGE_PROVED"
            and axis["direct_sum_matches"] is True
            and minimum >= stated.tau,
            text(minimum),
        ),
        Check(
            "summary sums the slabs",
            receipt["summary"]["nodes"] == sum(int(k["nodes"]) for k in kernels_out),
        ),
    ]


# --------------------------------------------------------------------------- the sources


def crate_source_digest(files: dict[str, bytes]) -> str:
    """``sqverify_continuous``'s ``source_sha256`` by its ``build.rs``: name, NUL, bytes,
    NUL over ``Cargo.toml``, ``Cargo.lock``, ``build.rs`` and the sorted ``src/*.rs``."""
    names = ["Cargo.toml", "Cargo.lock", "build.rs"]
    names += sorted(
        n for n in files if n.startswith("src/") and n.endswith(".rs") and n.count("/") == 1
    )
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode() + b"\0" + files[name] + b"\0")
    return digest.hexdigest()


def archive_files(archive: Path, top: str) -> dict[str, bytes]:
    """Every regular file of the crate directory ``top`` in the archive, by its path
    below it; refused if a member is not a plain file or directory under the archive's
    one top-level directory."""
    import tarfile  # noqa: PLC0415

    out: dict[str, bytes] = {}
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts
            require(
                not Path(member.name).is_absolute()
                and ".." not in parts
                and parts[:1] == ("sqverify_continuous",)
                and (member.isfile() or member.isdir()),
                f"unexpected archive member: {member.name}",
            )
            prefix = ("sqverify_continuous", top)
            if member.isfile() and parts[:2] == prefix:
                stream = tar.extractfile(member)
                require(stream is not None, f"{member.name} cannot be read")
                assert stream is not None
                out["/".join(parts[2:])] = stream.read()
    return out


def check2_source_digest(source: Path, listed: dict[str, str]) -> tuple[str, bool]:
    """check2's ``source_sha256`` by the rule its ``VERSION.json`` states, over the files
    it lists, and whether each listed file has its listed digest."""
    held = all(file_digest(source / name) == value for name, value in listed.items())
    lines = "".join(f"{listed[name]}  {name}\n" for name in sorted(listed))
    return hashlib.sha256(lines.encode()).hexdigest(), held


# --------------------------------------------------------------------------- premises


def restore_pinned(record: Path, directory: Path, name: str) -> list[dict[str, str]]:
    """Lay each file the acquisition record pins under the certificate directory by an
    identical copy, from that copy, refusing one whose bytes are not the pinned ones."""
    prefix = f"problems/square-lower-bounds/certificates/{name}/"
    restored: list[dict[str, str]] = []
    for source in load_json(record.read_bytes())["sources"]:
        for pin in source["pinned_only"]:
            if not pin["path"].startswith(prefix) or "identical_to" not in pin:
                continue
            data = (REPO / pin["identical_to"]).read_bytes()
            require(hashlib.sha256(data).hexdigest() == pin["sha256"], f"{pin['path']} differs")
            target = directory / pin["path"].removeprefix(prefix)
            require(not target.exists(), f"{pin['path']} is already laid")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            restored.append({"path": pin["path"], "from": pin["identical_to"]})
    return restored


def premises(
    asset: Path,
    stated: Stated,
    *,
    sha256: str,
    size: int,
    documents: Path,
    record: Path | None,
    work: Path,
) -> dict[str, Any]:
    """Every exact premise of the unpacked certificate, with its custody facts."""
    directory = unpack_asset(asset, sha256, size, stated.name, work)
    asset_files = sorted(
        p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()
    )
    laid = lay_documents(documents, directory)
    restored = restore_pinned(record, directory, stated.name) if record is not None else []
    listed = load_json((directory / "files-sha256.json").read_bytes())
    sealed = sealed_bundle(directory, listed, asset_files, suffix=BUNDLE_SUFFIX)
    bundle = load_json((directory / "bundle.json").read_bytes())
    start = time.perf_counter()

    raw = (directory / "candidate.json").read_bytes()
    density = read_candidate(raw, stated.n)
    control_raw = (directory / CONTROL).read_bytes()
    control = read_candidate(control_raw, stated.n)
    chain = scalar_chain(density, stated)
    check: list[Check] = [
        Check(
            "candidate digest is bundle.json's", density.sha256 == bundle["candidate"]["sha256"]
        ),
        Check("mass is bundle.json's", text(chain["M"]) == bundle["candidate"]["total_mass"]),
        Check("n tau > M", chain["counting_margin"] > 0, text(chain["counting_margin"])),
        Check("X = L / B is the claim", chain["X"] == stated.claim, text(chain["X"])),
        Check("L^2 > 2 B^2", chain["geometry_margin"] > 0, text(chain["geometry_margin"])),
        Check(
            "T^2 + 2T - 1 > 0, so T > tan(pi/8)",
            chain["angle_coverage_polynomial"] > 0,
            text(chain["angle_coverage_polynomial"]),
        ),
        Check(
            "control is every mass times 985/1000",
            scaled_rows(density, control, CONTROL_FACTOR)
            and mass(control) == mass(density) * CONTROL_FACTOR,
        ),
    ]

    # check1: sqverify_continuous's logs and its source digest.
    summary = load_json((directory / "check1/summary.json").read_bytes())
    control_summary = load_json((directory / "check1/control-summary.json").read_bytes())
    log = read_jsonl_gz(directory / CHECK1_LOG)
    control_log = read_jsonl_gz(directory / CHECK1_CONTROL_LOG)
    crate = archive_files(directory / CHECK1_ARCHIVE, "sqverify_fast")
    crate_digest = crate_source_digest(crate)
    check1 = [
        *crate_log_checks(log, density, stated, control=False),
        Check("log's summary is check1/summary.json", log[-1] == summary),
        *(
            Check("control: " + c.name, c.held, c.detail)
            for c in crate_log_checks(control_log, control, stated, control=True)
        ),
        Check(
            "control log's summary is check1/control-summary.json",
            control_log[-1] == control_summary,
        ),
        Check(
            "archive is bundle.json's",
            file_digest(directory / CHECK1_ARCHIVE) == bundle["check1"]["archive_sha256"],
        ),
        Check(
            "source digest by build.rs is the build's",
            crate_digest
            == summary["build"]["source_sha256"]
            == bundle["check1"]["source_sha256"],
            crate_digest,
        ),
    ]

    # check2: kernel inputs regenerated here, the receipts and the source digest.
    manifest = load_json((directory / "check2/manifest.json").read_bytes())
    control_manifest = load_json((directory / "check2/control-manifest.json").read_bytes())
    receipt = load_json((directory / "check2/receipt.json").read_bytes())
    control_receipt = load_json((directory / "check2/control-receipt.json").read_bytes())
    eps = Fraction(int(receipt["endpoints"][0]), SLAB_DENOMINATOR)
    inputs = kernel_inputs(density, stated, eps)
    control_inputs = kernel_inputs(control, stated, eps)
    shipped = {
        name: hashlib.sha256(
            gzip.decompress((directory / f"check2/{name}.gz").read_bytes())
        ).hexdigest()
        for name in ("certificate_input.txt", "axis_input.txt")
    }
    source = directory / CHECK2_SOURCE
    kernels = {name: file_digest(source / "kernel" / name) for name in CHECK2_KERNELS}
    version = load_json((source / "VERSION.json").read_bytes())
    check2_digest, listed_held = check2_source_digest(source, version["files"])
    facts = inputs["facts"]
    same_facts = {
        k: manifest.get(k)
        for k in (
            "terms",
            "axis_terms",
            "axis_side",
            "axis_density_denominator",
            "axis_scale",
            "axis_evaluation_bound",
            "axis_containment_margin",
        )
    }
    ours = {k: facts[k] for k in same_facts}
    check2 = [
        *(
            Check(
                f"{name} regenerated here is the manifest's",
                hashlib.sha256(inputs[name]).hexdigest()
                == manifest["files"][name]
                == shipped[name],
                hashlib.sha256(inputs[name]).hexdigest(),
            )
            for name in ("certificate_input.txt", "axis_input.txt")
        ),
        *(
            Check(
                f"control {name} regenerated here is the control manifest's",
                hashlib.sha256(control_inputs[name]).hexdigest()
                == control_manifest["files"][name],
                hashlib.sha256(control_inputs[name]).hexdigest(),
            )
            for name in ("certificate_input.txt", "axis_input.txt")
        ),
        Check("manifest's facts as derived here", same_facts == ours, json.dumps(ours)),
        Check("axis guards hold at the chosen scale", bool(facts["axis_guards_hold"])),
        Check(
            "near-axis containment B - A W(eps) > 0",
            Fraction(facts["axis_containment_margin"]) > 0,
            facts["axis_containment_margin"],
        ),
        Check(
            "candidate digests are the manifests'",
            manifest["candidate_sha256"] == density.sha256
            and control_manifest["candidate_sha256"] == control.sha256,
        ),
        *check2_receipt_checks(receipt, manifest, stated, kernels, control=False),
        *(
            Check("control: " + c.name, c.held, c.detail)
            for c in check2_receipt_checks(
                control_receipt, control_manifest, stated, kernels, control=True
            )
        ),
        Check("listed sources have VERSION.json's digests", listed_held),
        Check(
            "source digest by VERSION.json's rule is its own",
            check2_digest == version["source_sha256"] == bundle["check2"]["source_sha256"],
            check2_digest,
        ),
    ]
    wall = time.perf_counter() - start
    every = [*check, *check1, *check2]
    prepub = directory / PREPUBLICATION
    return {
        "kind": "continuous-pose-followup-premises/v1",
        "certificate": stated.name,
        "claim": f"s({stated.n}) > {text(stated.claim)}",
        "asset": {"sha256": sha256, "bytes": size, "files": inventory(directory, asset_files)},
        "documents": inventory(directory, laid),
        "restored_pinned_only": restored,
        "sealed_bundle": sealed,
        "candidate": {
            "sha256": density.sha256,
            "listed_rows": density.listed,
            "positive_rows": len(density.rows),
            "terms": density.terms,
            "distinct_images": len(density.merged),
            "side": text(density.side),
            "search_core": text(density.core),
        },
        "scalar_chain": {k: text(v) for k, v in chain.items()},
        "check2_inputs": {"facts": facts, "control_facts": control_inputs["facts"]},
        "sources": {
            "check1_source_sha256": crate_digest,
            "check1_files": len(crate),
            "check2_source_sha256": check2_digest,
            "check2_kernels": kernels,
        },
        "prepublication": load_json(prepub.read_bytes()) if prepub.is_file() else None,
        "checks": {
            "candidate": [vars_of(c) for c in check],
            "check1": [vars_of(c) for c in check1],
            "check2": [vars_of(c) for c in check2],
        },
        "failed": [c.name for c in every if not c.held],
        "wall_seconds": wall,
        "author_code_executed": False,
        "status": STATUS_HOLD if all(c.held for c in every) else STATUS_FAIL,
        "scope": (
            "Exact premises, the binding of check2's kernel inputs to the candidate, the"
            " consistency of both programs' logs with their summaries and the source"
            " digests, from the pinned asset and documents; no coverage is decided and no"
            " program of the source is run."
        ),
    }


def vars_of(check: Check) -> dict[str, Any]:
    return {"name": check.name, "held": check.held, "detail": check.detail}


# --------------------------------------------------------------------------- the sample


def spawn(argv: Sequence[str], cwd: Path) -> dict[str, Any]:
    """One program to its end in ``cwd``, killed past `RUN_TIMEOUT`.

    Its CPU is the change in this process's reaped-children usage across the run, which
    is the program's own because the sample runs one program at a time.
    """
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    load = os.getloadavg()[0]
    start = time.monotonic()
    try:
        done = subprocess.run(
            list(argv),
            cwd=cwd,
            capture_output=True,
            timeout=RUN_TIMEOUT,
            check=False,
            env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C"},
        )
    except subprocess.TimeoutExpired as error:
        raise AuditError(
            f"{Path(argv[0]).name} ran past {RUN_TIMEOUT} s and was killed"
        ) from error
    wall = time.monotonic() - start
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    lines: list[dict[str, Any]] = []
    for line in done.stdout.decode(errors="replace").splitlines():
        try:
            value = json.loads(line, parse_float=str)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            lines.append(value)
    return {
        "argv": [Path(argv[0]).name, *argv[1:]],
        "returncode": done.returncode,
        "process_cpu_seconds": (after.ru_utime + after.ru_stime)
        - (before.ru_utime + before.ru_stime),
        "children_max_rss_kib": after.ru_maxrss,
        "wall_seconds": wall,
        "load_before": load,
        "load_after": os.getloadavg()[0],
        "lines": lines,
        "stderr_tail": done.stderr.decode(errors="replace")[-400:],
    }


def crate_argv(binary: Path, candidate: Path, stated: Stated, roots: str | None) -> list[str]:
    argv = [
        str(binary.resolve()),
        "--candidate",
        str(candidate.resolve()),
        "--n",
        str(stated.n),
    ]
    argv += ["--continuous", "--core", text(stated.core), "--tau", text(stated.tau)]
    argv += ["--threads", "1", "--max-nodes", "200000000"]
    return [*argv, "--roots", roots] if roots is not None else argv


def root_row(run: dict[str, Any], index: int) -> dict[str, Any]:
    return next(
        (r for r in run["lines"] if r.get("kind") == "root" and r.get("index") == index), {}
    )


def same(ours: object, theirs: object) -> bool:
    """Equal, with two decimal texts equal when they name the same binary64: the kernel
    prints 17 significant digits, and the source's receipt holds Python's shortest form."""
    if isinstance(ours, str) and isinstance(theirs, str) and ours != theirs:
        try:
            return float(ours) == float(theirs)
        except ValueError:
            return False
    return ours == theirs


def compare_root(ours: dict[str, Any], theirs: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "verdict",
        "nodes",
        "leaves",
        "angle_splits",
        "max_depth",
        "min_certified_lower_bound",
    )
    return {
        "index": ours.get("index"),
        "t": ours.get("t"),
        **{k: ours.get(k) for k in keys},
        "thread_seconds": ours.get("seconds"),
        "source_seconds": theirs.get("seconds"),
        "agrees_with_source": all(same(ours.get(k), theirs.get(k)) for k in keys),
    }


def compare_slab(ours: dict[str, Any], theirs: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "status",
        "pl",
        "ph",
        "den",
        "nodes",
        "leaves",
        "lower_bound",
        "max_depth",
        "angle_splits",
    )
    return {
        **{k: ours.get(k) for k in keys},
        "kernel_seconds": ours.get("seconds"),
        "source_seconds": theirs.get("seconds"),
        "agrees_with_source": all(same(ours.get(k), theirs.get(k)) for k in keys),
    }


def sample(
    certificate: Path,
    stated: Stated,
    *,
    work: Path,
    crate: Path | None,
    roots: list[int],
    mutant_root: int | None,
    mutant_scales: Sequence[Fraction],
    control: bool,
    pose: Path | None,
    slabs: list[int],
    axis: Path | None,
) -> dict[str, Any]:
    """The chosen runs, one at a time and one thread each, judged against the source."""
    work.mkdir(parents=True, exist_ok=True)
    raw = (certificate / "candidate.json").read_bytes()
    density = read_candidate(raw, stated.n)
    log = read_jsonl_gz(certificate / CHECK1_LOG)
    source_roots = {int(r["index"]): r for r in log if r.get("kind") == "root"}
    receipt = load_json((certificate / "check2/receipt.json").read_bytes())
    source_slabs = {int(s["index"]): s["kernel"] for s in receipt["slabs"]}
    control_receipt = load_json((certificate / "check2/control-receipt.json").read_bytes())
    runs: dict[str, Any] = {}
    cpu: dict[str, float] = {}

    if crate is not None:
        rows = []
        for index in roots:
            run = spawn(
                crate_argv(crate, certificate / "candidate.json", stated, f"{index}-{index}"),
                Path(),
            )
            row = compare_root(root_row(run, index), source_roots[index])
            row["process_cpu_seconds"] = run["process_cpu_seconds"]
            row["axis_patch"] = next(
                (r for r in run["lines"] if r.get("kind") == "axis-patch"), None
            )
            row["summary_status"] = run["lines"][-1].get("status") if run["lines"] else None
            row["build"] = run["lines"][-1].get("build") if run["lines"] else None
            rows.append(row)
        runs["check1_roots"] = rows
        cpu["check1_roots"] = sum(r["process_cpu_seconds"] for r in rows)
        if control:
            run = spawn(crate_argv(crate, certificate / CONTROL, stated, None), Path())
            summary = run["lines"][-1] if run["lines"] else {}
            source = load_json((certificate / "check1/control-summary.json").read_bytes())
            keys = ("status", "refused_roots", "nodes", "axis_verified")
            runs["check1_control"] = {
                **{k: summary.get(k) for k in keys},
                "returncode": run["returncode"],
                "process_cpu_seconds": run["process_cpu_seconds"],
                "agrees_with_source": all(summary.get(k) == source.get(k) for k in keys),
            }
        mutants: list[dict[str, Any]] = []
        for scale in mutant_scales if mutant_root is not None else []:
            assert mutant_root is not None
            mutant = work / f"candidate-mutant-{scale.numerator}-{scale.denominator}.json"
            mutant.write_bytes(mutant_bytes(raw, scale))
            run = spawn(
                crate_argv(crate, mutant, stated, f"{mutant_root}-{mutant_root}"), Path()
            )
            row = root_row(run, mutant_root)
            patch = next((r for r in run["lines"] if r.get("kind") == "axis-patch"), {})
            mutants.append(
                {
                    "scale": text(scale),
                    "root": mutant_root,
                    "candidate_sha256": file_digest(mutant),
                    "verdict": row.get("verdict"),
                    "nodes": row.get("nodes"),
                    "min_certified_lower_bound": row.get("min_certified_lower_bound"),
                    "witness": row.get("witness"),
                    "axis_patch_verified": patch.get("verified"),
                    "axis_patch_min_certified_lower_bound": patch.get(
                        "min_certified_lower_bound"
                    ),
                    "process_cpu_seconds": run["process_cpu_seconds"],
                    "outcome": mutant_outcome(row, patch),
                }
            )
        if mutants:
            runs["check1_mutants"] = mutants

    folder = work / "kernel"
    folder.mkdir(exist_ok=True)
    eps = Fraction(int(receipt["endpoints"][0]), SLAB_DENOMINATOR)
    inputs = kernel_inputs(density, stated, eps)
    for name in ("certificate_input.txt", "axis_input.txt"):
        (folder / name).write_bytes(inputs[name])
    if pose is not None:
        rows = []
        endpoints = [int(v) for v in receipt["endpoints"]]
        for index in slabs:
            lo, hi = endpoints[index], endpoints[index + 1]
            argv = [
                str(pose.resolve()),
                str(lo),
                str(hi),
                str(SLAB_DENOMINATOR),
                str(stated.tau.numerator),
                str(stated.tau.denominator),
                "4000000000",
            ]
            run = spawn(argv, folder)
            ours = run["lines"][-1] if run["lines"] else {}
            row = {"index": index, **compare_slab(ours, source_slabs[index])}
            row["returncode"] = run["returncode"]
            row["process_cpu_seconds"] = run["process_cpu_seconds"]
            rows.append(row)
        runs["pose_slabs"] = rows
        cpu["pose_slabs"] = sum(r["process_cpu_seconds"] for r in rows)
    if axis is not None:
        control_folder = work / "kernel-control"
        control_folder.mkdir(exist_ok=True)
        control_density = read_candidate((certificate / CONTROL).read_bytes(), stated.n)
        control_inputs = kernel_inputs(control_density, stated, eps)
        (control_folder / "axis_input.txt").write_bytes(control_inputs["axis_input.txt"])
        out = {}
        for label, place, theirs in (
            ("main", folder, receipt["axis"]["kernel"]),
            ("control", control_folder, control_receipt["axis"]["kernel"]),
        ):
            run = spawn([str(axis.resolve()), "axis_input.txt"], place)
            ours = run["lines"][-1] if run["lines"] else {}
            keys = (
                "status",
                "x_nodes",
                "y_nodes",
                "minimum_numerator",
                "scale",
                "minimizer_x_integer",
                "minimizer_y_integer",
                "direct_sum_matches",
            )
            out[label] = {
                **{k: ours.get(k) for k in keys},
                "returncode": run["returncode"],
                "process_cpu_seconds": run["process_cpu_seconds"],
                "children_max_rss_kib": run["children_max_rss_kib"],
                "agrees_with_source": all(same(ours.get(k), theirs.get(k)) for k in keys),
            }
        runs["axis"] = out

    return {
        "kind": "continuous-pose-followup-sample/v1",
        "certificate": stated.name,
        "candidate_sha256": density.sha256,
        "binaries": {
            label: file_digest(path)
            for label, path in (("crate", crate), ("pose", pose), ("axis", axis))
            if path is not None
        },
        "runs": runs,
        "price": price(runs, log, receipt),
        "host": {"cpu_count": os.cpu_count(), "machine": platform.machine()},
        "ran_at": utc_now(),
        "status": sample_status(runs),
        "scope": (
            "A diagnostic sample, one program at a time at one thread: it decides only the"
            " roots, slabs and axis patches it ran, and is not a replay."
        ),
    }


def mutant_outcome(row: dict[str, Any], patch: dict[str, Any]) -> str:
    """Where a mutant was stopped: at the axis patch, at the root it ran, or nowhere.

    A mutant scaled so slightly that the axis patch still holds tests the oblique search
    alone; one refused at the axis never reaches it, as the source's 985/1000 control
    does not. ``REFUSED_AT_ROOT`` covers both of the root's stops, an exact capture below
    the threshold and an exhausted node budget; the row's ``witness`` says which
    (``exact_below_threshold``), and only the first is a refusal a control may count.
    """
    if patch.get("verified") is not True:
        return "REFUSED_AT_AXIS"
    return "REFUSED_AT_ROOT" if row.get("verdict") == "refused" else "VERIFIED_AT_ROOT"


def sample_status(runs: dict[str, Any]) -> str:
    """Whether every run that repeats the source's agrees with its log. A mutant repeats
    nothing of the source's, and its outcome is recorded beside the status, not in it."""
    agree = [r["agrees_with_source"] for r in runs.get("check1_roots", [])]
    agree += [r["agrees_with_source"] for r in runs.get("pose_slabs", [])]
    agree += [r["agrees_with_source"] for r in runs.get("axis", {}).values()]
    if "check1_control" in runs:
        agree.append(runs["check1_control"]["agrees_with_source"])
    return "DIAGNOSTIC_SAMPLE" if agree and all(agree) else "SAMPLE_DISAGREES"


def price(
    runs: dict[str, Any], log: list[dict[str, Any]], receipt: dict[str, Any]
) -> dict[str, Any]:
    """A complete replay of each program at this host's ratio to the source on what ran.

    check1's total is the sum of the source's per-root seconds (each root ran on one
    thread), check2's the sum of its per-slab seconds (each slab one kernel process).
    Each ratio is taken twice, from the program's own timing of the root or slab and from
    the process CPU here (which adds check1's axis patch and parsing to every root), and
    the larger prices the replay.
    """
    source_roots = sum(float(r["seconds"]) for r in log if r.get("kind") == "root")
    source_slabs = sum(float(s["seconds"]) for s in receipt["slabs"])
    out: dict[str, Any] = {
        "check1_source_cpu_seconds": source_roots,
        "check2_source_cpu_seconds": source_slabs,
    }
    for label, key, own, total in (
        ("check1", "check1_roots", "thread_seconds", source_roots),
        ("check2", "pose_slabs", "kernel_seconds", source_slabs),
    ):
        rows = runs.get(key, [])
        if not rows:
            continue
        theirs = sum(float(r["source_seconds"]) for r in rows)
        by_own = sum(float(r[own]) for r in rows) / theirs
        by_process = sum(float(r["process_cpu_seconds"]) for r in rows) / theirs
        out[f"{label}_ratio_by_own_timing"] = by_own
        out[f"{label}_ratio_by_process_cpu"] = by_process
        out[f"{label}_replay_cpu_hours"] = max(by_own, by_process) * total / 3600
    return out


# --------------------------------------------------------------------------- the command


def parse_list(value: str) -> list[int]:
    return [int(v) for v in value.split(",") if v.strip()] if value else []


def write(path: Path, value: object) -> None:
    """A receipt as retained JSON: a record per line, keys sorted."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(retained_json.dumps(value, sort_keys=True), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    first = commands.add_parser("premises", help="custody, exact premises and log consistency")
    second = commands.add_parser("sample", help="chosen roots, slabs and axis patches")
    for sub in (first, second):
        sub.add_argument("--name", default="continuous_n28_L5745")
        sub.add_argument("--n", type=int, required=True)
        sub.add_argument("--core", type=Fraction, required=True)
        sub.add_argument("--tau", type=Fraction, default=Fraction(1))
        sub.add_argument("--claim", type=Fraction)
        sub.add_argument("--out", type=Path, required=True)
        sub.add_argument("--work", type=Path, required=True)
    first.add_argument("--asset", type=Path, required=True)
    first.add_argument("--sha256", required=True)
    first.add_argument("--bytes", type=int, required=True)
    first.add_argument("--documents", type=Path, required=True)
    first.add_argument("--record", type=Path, help="the packet's acquisition/sources.json")
    second.add_argument("--certificate", type=Path, required=True)
    second.add_argument("--crate-binary", type=Path)
    second.add_argument("--roots", default="")
    second.add_argument("--control", action="store_true")
    second.add_argument("--mutant-root", type=int)
    second.add_argument("--mutant-scales", default="9999/10000", help="comma-separated factors")
    second.add_argument("--pose-binary", type=Path)
    second.add_argument("--slabs", default="")
    second.add_argument("--axis-binary", type=Path)
    args = parser.parse_args(argv)
    claim = args.claim
    try:
        if args.command == "premises":
            stated = Stated(args.name, args.n, args.core, args.tau, claim or Fraction(0))
            report = premises(
                args.asset,
                stated,
                sha256=args.sha256,
                size=args.bytes,
                documents=args.documents,
                record=args.record,
                work=args.work,
            )
        else:
            stated = Stated(args.name, args.n, args.core, args.tau, claim or Fraction(0))
            report = sample(
                args.certificate,
                stated,
                work=args.work,
                crate=args.crate_binary,
                roots=parse_list(args.roots),
                mutant_root=args.mutant_root,
                mutant_scales=[Fraction(v) for v in args.mutant_scales.split(",") if v.strip()],
                control=args.control,
                pose=args.pose_binary,
                slabs=parse_list(args.slabs),
                axis=args.axis_binary,
            )
    except (AuditError, KeyError, ValueError) as error:
        print(f"refused: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    write(args.out, report)
    print(json.dumps({"status": report["status"], "out": str(args.out)}))
    return 0 if report["status"] in {STATUS_HOLD, "DIAGNOSTIC_SAMPLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
