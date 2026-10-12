"""Audit Guzhou0806's new-support bound, s(40) > 3359/500, and price its replay.

The comment of 2026-10-11 on jlevy/squares#485 claims ``s(40) > 3359/500 = 6.718`` from a
new rational density: 685 positive D4 rectangle orbits, 522 drawn from wand125's
``rect_n40_L67`` pool and 163 outside it, all with new weights, of mass ``3999/100``. The
continuous-pose and axis kernels of T-145's release decide it unchanged, byte for byte, at
new parameters: side ``B = 3350/3359``, threshold ``4999/5000``, the same 43 slabs of the
half-angle tangent, and the near-axis patch at ``A = 249329659/250000000``. The source is
retained in ``resources/web/guzhou-n40-new-supports-2026-10-11/``; T-145's review
(``docs/project/reviews/review-2026-10-10-guzhou-n40-continuous-pose-bound.md``) read
both kernels line by line and states the input formats this tool regenerates.

Four subcommands:

- ``derive`` writes the two kernel inputs, regenerated here from the retained density
  (`pose_input` and `axis_input` of `devtools.audit_continuous_pose`, ``B`` written as
  this release writes it), and the crate's near-axis input, and prints their SHA-256.
  Both release receipts name the kernel inputs by digest (`POSE_SHA256`,
  `AXIS_SHA256`), which is what binds them to the density.
- ``check`` decides the claim's finite steps in exact rationals (`check_report`): the
  density's orbit facts (`support_facts`: the 522 inherited boxes are rows of the
  original pool, the 163 generated ones are D4-equivalent to none of its 2,526
  rectangles, the 685 orbits are distinct, every box lies in ``K``, every weight is
  positive and they sum to ``M``), then the D4 expansion, both inputs' identity and the
  enclosure of every number, the dominated measure, the scalar chain, and every value
  of both release receipts, by the checks `devtools.audit_continuous_pose` makes of
  T-145's release, made of this one (`RELEASE`) rather than copied; it refuses the
  finite controls (`FINITE_CONTROLS`, `density_controls`) and prices the
  continuous-pose replay from the receipts and T-145's replay here (`price`).
- ``run-axis`` builds the release's axis kernel from the retained source with the
  release's flags in a scratch tree, runs it on the derived input and at two thresholds
  either side of its minimum, and, given a crate binary of reviewed source, decides the
  near-axis statement a second way with ``sqverify-fast``'s exact axis sweep. These are
  the quick parts of the replay; the 43 slabs are not run here.
- ``check-axis`` judges those receipts: the crate's decision must be on the input derived
  here (`crate_axis_input`) from the release's candidate, by its digest and its
  premises. It refuses receipts without that decision unless told ``--without-crate``,
  and a judgement without it says ``AXIS_KERNEL_HOLDS_WITHOUT_CRATE``, never the full
  stage's ``AXIS_STAGE_HOLDS``.

**What its author read** (its independence record, for the finite steps). Written on
2026-10-11 by an AI agent (Claude, lane E of the 2026-10-11 intake pass, ``think-tln9``)
from the release's ``README.md``, ``SOURCES.md``, ``VERIFICATION.md``,
``REPRODUCIBILITY.md``, ``OBSTRUCTION.md``, ``PROOF.md`` (for the density's definition and
the parameters), ``certificate/parameters.json``, the diff of ``verifier/run.py`` and the
workflow against T-145's pin (for the commands; the axis kernel is now built with the
pose kernel's flags), and the receipts and both densities as data; and from
`devtools.audit_continuous_pose`, whose input builders and finite checks it reuses. It
did not open ``verifier/exact.py``, ``verifier/audit.py``, ``obstruction/check.py``,
``obstruction/check.cpp``, ``obstruction/run.py`` or the release's tests. It shares with
``exact.py`` the definition of the density (weight ``w`` puts ``w / (8 |R|)`` on each of
the eight images), its D4 expansion, the kernels' input order, the enclosure rule and the
inward rounding, and no code.

Nothing here decides the continuous cover; the release's kernel does, over the 43 slabs,
and that replay waits for an owner budget (``price`` says what it costs).

Usage, from ``packing/``, each after ``uv run --frozen --all-extras --group dev``::

    python -m devtools.audit_n40_new_supports derive --out DIR
    python -m devtools.audit_n40_new_supports check [--output OUT.json]
    python -m devtools.audit_n40_new_supports run-axis --out DIR \\
        [--crate-binary sqverify_fast/target/release/sqverify-fast]
    python -m devtools.audit_n40_new_supports check-axis [--receipts DIR] [--output OUT] \\
        [--without-crate]
"""

from __future__ import annotations

import argparse
import gzip
import heapq
import json
import shutil
import subprocess
import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.audit_clipped_corner_transfer import (
    Density,
    Rect,
    area,
    d4_maps,
    image,
    merge,
    rational,
    sha256,
    text,
)
from devtools.audit_continuous_pose import CLAIM as T145_CLAIM
from devtools.audit_continuous_pose import (
    FLAGS,
    GRID,
    KERNEL_SOURCES,
    STAGES,
    Check,
    Claim,
    Facts,
    FiniteControl,
    Release,
    Replay,
    admission_block,
    axis_input,
    axis_rows,
    chain_checks,
    crate_input,
    crate_premises,
    extent,
    facts,
    finite_controls,
    identity_checks,
    input_checks,
    kernel_threshold,
    least_bound,
    manifest,
    pose_input,
    read_receipt,
    read_slabs,
    receipt_checks,
    replay_report,
    retained_json,
    run_replay,
    spawn,
    write_json,
)
from devtools.audit_continuous_pose import RELEASE as T145_RELEASE
from devtools.check_sqverify_fast import crate_source_sha256
from devtools.retained_data import read_retained_bytes
from devtools.sqverify_fast_census import REVIEWED_SOURCES

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
PACKET = WEB / "guzhou-n40-new-supports-2026-10-11"
SOURCE = PACKET / "source"
CANDIDATE = SOURCE / "certificate/certified_candidate.json"
#: The original pool, which the 2026-10-01 rectangle packet retains and this packet pins.
ORIGINAL = (
    WEB / "wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates"
    "/rect_n40_L67/certified_candidate.json"
)
PARAMETERS = SOURCE / "certificate/parameters.json"
RECEIPT_DIR = PACKET / "receipts"
#: T-145's packet: its kernels, its receipts and its replay here, the price's calibration.
T145 = T145_RELEASE.packet

PIN = "6a65957e6c5c51cdf267917d882dab7f5b4928dd"
CANDIDATE_SHA256 = "984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2"
ORIGINAL_SHA256 = "71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0"
POSE_SHA256 = "6c64a2d21207e7b65ea011dc7ca7a655418840defbf017340ce44ab7fc7b94fb"
AXIS_SHA256 = "10dd46b06f14144619bf9de03151c43215e43e34f7e60df440f4e27d6a594396"
CI_COMPILER = "g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
#: The CI run's binaries. The pose binary is T-145's CI binary, which `kernel_checks`
#: holds to T-145's records; the axis binary is new, since ``run.py`` now builds the
#: unchanged axis source with the pose kernel's flags.
CI_BINARIES = {
    "axis": "19288b2f9bcb1cfa86a0bde9db1e1fbb79d43dc8044bc7243af8f6ad405899af",
    "pose": "69bc9e6485102d3636db5377884ba6304f749be94d6ca913d82d80108f1ed4ab",
}
#: Files this release keeps byte for byte from T-145's, whose review read them.
SHARED_WITH_T145 = (
    "verifier/continuous_pose.cpp",
    "verifier/axis_integer_grid.cpp",
    "tests/kernel_harness.cpp",
    "tests/rounding_harness.cpp",
    "tests/oracle.py",
)

#: The claim's parameters, as ``parameters.json`` names them: T-145's but for the side,
#: the bound and the axis side.
CLAIM = replace(
    T145_CLAIM,
    B=Fraction(3350, 3359),
    X=Fraction(3359, 500),
    A=Fraction(249329659, 250000000),
)
#: T-145's bound, which this claim raises by `RAISE`.
EARLIER = Fraction(1340000, 199529)
RAISE = Fraction(217911, 99764500)
#: What PROOF.md section 6 states for ``B - A W(eps)``.
NEAR_AXIS_MARGIN = Fraction(424025836324581, 839750000000839750000000)
SCHEMA = "n40-expanded-rectangles/v1"
COUNTS = {"sites": 685, "inherited": 522, "generated": 163, "terms": 5480, "pool": 2526}
#: This release, as the finite checks of `devtools.audit_continuous_pose`, which this tool
#: shares rather than copies, judge it.
RELEASE = Release(
    packet=PACKET,
    claim=CLAIM,
    pin=PIN,
    ci_run="38120568498",
    pose_sha256=POSE_SHA256,
    axis_sha256=AXIS_SHA256,
    ci_binaries=CI_BINARIES,
    earlier=EARLIER,
    raises=RAISE,
    terms=COUNTS["terms"],
    distinct=5424,
    nodes=3293,
    source_files=30,
    results=("axis.json", "obstruction.json", "slabs.jsonl", "verification.json"),
    hex_b=True,
    axis_flags=FLAGS,
)
#: The release's two receipts: the producer's local run in the tree at the pin, and the
#: GitHub Actions run 38120568498 that the release ZIP carries instead.
RECEIPTS = RELEASE.receipts


# --------------------------------------------------------------------------- the density


@dataclass(frozen=True)
class Site:
    """One orbit of the new density, as the release lists it."""

    box: Rect
    weight: Fraction
    kind: str
    source_index: int | None


def as_rect(values: Sequence[object]) -> Rect:
    """Four JSON numbers or strings as an exact rectangle ``(x0, y0, x1, y1)``."""
    x0, y0, x1, y1 = (rational(v) for v in values)
    return (x0, y0, x1, y1)


def read_sites(raw: bytes) -> tuple[dict[str, Any], tuple[Site, ...]]:
    """The candidate's header and its sites, every number exact."""
    data = json.loads(raw, parse_float=Fraction)
    sites = tuple(
        Site(
            box=as_rect(item["box"]),
            weight=rational(item["weight"]),
            kind=str(item["kind"]),
            source_index=int(item["source_index"]) if "source_index" in item else None,
        )
        for item in data["sites"]
    )
    header = {key: value for key, value in data.items() if key != "sites"}
    return header, sites


def site_density(raw: bytes) -> Density:
    """The candidate as a density: weight ``w`` on box ``R`` puts ``w / (8 |R|)`` on each
    of its eight images, in site order, as PROOF.md section 1 defines it."""
    header, sites = read_sites(raw)
    side = rational(header["L"])
    rows = tuple((site.box, site.weight) for site in sites if site.weight > 0)
    maps = d4_maps(side)
    terms = [(image(rect, f), w / (8 * area(rect))) for rect, w in rows for f in maps]
    return Density(
        sha256=sha256(raw),
        side=side,
        core=rational(header["B"]),
        n=int(header["n"]),
        listed=len(sites),
        rows=rows,
        terms=len(terms),
        merged=merge(terms),
    )


def read_pool(raw: bytes) -> tuple[list[Rect], list[Fraction]]:
    """The original candidate's 2,526 rectangles and their weights, zero weights kept."""
    data = json.loads(raw, parse_float=Fraction)
    rects = [as_rect(r) for r in data["rectangles"]]
    return rects, [rational(w) for w in data["weights"]]


def canonical(rect: Rect, side: Fraction) -> Rect:
    """The least of a rectangle's eight images: one name per D4 orbit."""
    return min(image(rect, f) for f in d4_maps(side))


@dataclass(frozen=True)
class SupportFacts:
    """What the release says of its 685 orbits, decided on the retained bytes."""

    header: dict[str, Any]
    sites: int
    kinds: dict[str, int]
    positive: int
    in_k: int
    inherited_exact: int
    inherited_distinct: bool
    inherited_positive_before: int
    generated_outside_pool: int
    orbits: int
    mass: Fraction


def support_facts(raw: bytes, pool_raw: bytes) -> SupportFacts:
    header, sites = read_sites(raw)
    side = rational(header["L"])
    pool, weights = read_pool(pool_raw)
    pool_orbits = {canonical(rect, side) for rect in pool}
    inherited = [s for s in sites if s.kind == "inherited"]
    generated = [s for s in sites if s.kind == "generated"]
    indices = [s.source_index for s in inherited]
    return SupportFacts(
        header=header,
        sites=len(sites),
        kinds=dict(Counter(s.kind for s in sites)),
        positive=sum(s.weight > 0 for s in sites),
        in_k=sum(
            0 <= s.box[0] < s.box[2] <= side and 0 <= s.box[1] < s.box[3] <= side for s in sites
        ),
        inherited_exact=sum(
            s.source_index is not None
            and 0 <= s.source_index < len(pool)
            and pool[s.source_index] == s.box
            for s in inherited
        ),
        inherited_distinct=len(set(indices)) == len(indices),
        inherited_positive_before=sum(
            s.source_index is not None
            and 0 <= s.source_index < len(weights)
            and weights[s.source_index] > 0
            for s in inherited
        ),
        generated_outside_pool=sum(
            canonical(s.box, side) not in pool_orbits for s in generated
        ),
        orbits=len({canonical(s.box, side) for s in sites}),
        mass=sum((s.weight for s in sites), Fraction(0)),
    )


def load_candidate() -> bytes:
    return read_retained_bytes(CANDIDATE)


def load_pool() -> bytes:
    return read_retained_bytes(ORIGINAL)


# --------------------------------------------------------------------------- the checks


def support_checks(s: SupportFacts, density: Density, claim: Claim = CLAIM) -> list[Check]:
    """The density's orbit facts, against what the release states of them."""
    h = s.header
    expected_header = {
        "B": text(claim.B),
        "L": text(claim.L),
        "X": text(claim.X),
        "axis_side": text(claim.A),
        "epsilon": text(claim.eps),
        "mass": text(claim.mass),
        "threshold": text(claim.tau),
    }
    return [
        Check("density: the release's candidate", density.sha256 == CANDIDATE_SHA256, ""),
        Check(
            "density: its header is the claim's",
            h.get("schema") == SCHEMA
            and h.get("n") == claim.n
            and {k: str(h.get(k)) for k in expected_header} == expected_header
            and h.get("source_sha256") == ORIGINAL_SHA256,
            f"{h.get('schema')}, built on {str(h.get('source_sha256'))[:8]}...",
        ),
        Check(
            "density: 685 positive orbits, 522 inherited and 163 generated",
            (s.sites, s.positive) == (COUNTS["sites"], COUNTS["sites"])
            and s.kinds == {"inherited": COUNTS["inherited"], "generated": COUNTS["generated"]},
            f"{s.positive} of {s.sites} positive; {s.kinds}",
        ),
        Check(
            "density: every box is a proper rectangle in K",
            s.in_k == s.sites,
            f"{s.in_k} of {s.sites}",
        ),
        Check(
            "density: each inherited box is its pool row exactly, no row twice",
            s.inherited_exact == COUNTS["inherited"] and s.inherited_distinct,
            f"{s.inherited_exact} of {COUNTS['inherited']}; "
            f"{s.inherited_positive_before} of them positive in rect_n40_L67",
        ),
        Check(
            "density: no generated box is D4-equivalent to any of the 2526 pool rectangles",
            s.generated_outside_pool == COUNTS["generated"],
            f"{s.generated_outside_pool} of {COUNTS['generated']}",
        ),
        Check(
            "density: the 685 orbits are distinct",
            s.orbits == COUNTS["sites"],
            f"{s.orbits} canonical forms",
        ),
        Check("density: the weights sum to M", s.mass == claim.mass, text(s.mass)),
    ]


def release_admission(s: SupportFacts, f: Facts) -> dict[str, object]:
    """The receipts' ``admission`` block: `admission_block`'s keys, and the orbit counts
    and the pool's digest this release adds to them."""
    return {
        **admission_block(f),
        "generated_representatives": s.kinds.get("generated", 0),
        "inherited_representatives": s.kinds.get("inherited", 0),
        "original_sha256": str(s.header.get("source_sha256")),
    }


def retained_alike(release: Release, earlier: Release, path: str, digest: str) -> bool:
    """Whether this release's retained bytes at ``path`` have the manifest's ``digest``,
    and the earlier release retains the same bytes there."""
    data = read_retained_bytes(release.source / path)
    return sha256(data) == digest and read_retained_bytes(earlier.source / path) == data


def kernel_checks(release: Release = RELEASE, earlier: Release = T145_RELEASE) -> list[Check]:
    """What the release keeps byte for byte from T-145's, whose review read it: each
    shared file in both manifests with one digest, which its retained bytes have, and the
    pose binary of its CI run, as both CI receipts and T-145's replay build record it."""
    ours, theirs = manifest(release.manifest_path), manifest(earlier.manifest_path)
    kept = [
        path
        for path in SHARED_WITH_T145
        if path in ours
        and ours[path] == theirs.get(path)
        and retained_alike(release, earlier, path, ours[path])
    ]
    builds = retained_json(earlier.packet / "receipts/builds.json")
    rebuilt = builds["builds"]["pose"]["binary_sha256"]
    ran = (read_receipt(release.receipts["ci"]).get("binaries") or {}).get("pose")
    reran = (read_receipt(earlier.receipts["ci"]).get("binaries") or {}).get("pose")
    return [
        Check(
            "kernels: byte for byte T-145's, which its review read",
            kept == list(SHARED_WITH_T145),
            f"{len(kept)} of {len(SHARED_WITH_T145)}: {', '.join(kept)}",
        ),
        Check(
            "kernels: the CI run's pose binary is T-145's, which its replay rebuilt",
            builds.get("compiler") == CI_COMPILER
            and ran == reran == rebuilt == release.ci_binaries["pose"]
            and release.ci_binaries["pose"] == earlier.ci_binaries["pose"],
            f"{str(ran)[:12]}..., in both CI receipts and T-145's build with the CI compiler",
        ),
    ]


# --------------------------------------------------------------------------- controls


NEAR_AXIS = "near-axis: A W(eps) <= B"
FINITE_CONTROLS = (
    FiniteControl(
        "G",
        "A one step of 1/250000000 larger, 249329660/250000000",
        replace(CLAIM, A=Fraction(249329660, 250000000)),
        (NEAR_AXIS,),
    ),
    FiniteControl(
        "G2",
        "tau replaced by 3999/4000, where 40 tau = M",
        replace(CLAIM, tau=Fraction(3999, 4000)),
        ("counting: n tau - M > 0",),
    ),
    FiniteControl(
        "G3",
        "T replaced by 41/100, short of pi/4",
        replace(CLAIM, T=Fraction(41, 100)),
        ("slabs: T passes pi/4", "slabs: the endpoints partition [eps, T]"),
    ),
    FiniteControl(
        "G4",
        "eps replaced by 1/10^5",
        replace(CLAIM, eps=Fraction(1, 10**5)),
        (NEAR_AXIS, "slabs: the endpoints partition [eps, T]"),
    ),
)
#: The two checks that bind the density to what both kernels decided.
INPUT_DIGESTS = ("pose input: the receipts' input", "axis input: the receipts' input")


def density_controls(raw: bytes, pool_raw: bytes) -> list[dict[str, object]]:
    """Three altered densities, each refused: one generated site moved onto a pool
    rectangle's D4 image and one weight scaled by 99/100, which `support_checks` refuses,
    and a hundredth of site 0's weight moved to site 1, which keeps every orbit fact and
    the mass, so only `input_checks`' digests of the derived inputs can refuse it."""
    data = json.loads(raw)
    pool = json.loads(pool_raw)["rectangles"]
    first = next(i for i, site in enumerate(data["sites"]) if site["kind"] == "generated")
    side = Fraction(67, 10)
    x0, y0, x1, y1 = (Fraction(str(v)) for v in pool[0])
    mirrored = (side - x1, y0, side - x0, y1)
    moved = json.loads(raw)
    moved["sites"][first]["box"] = [text(v) for v in mirrored]
    scaled = json.loads(raw)
    weight = Fraction(scaled["sites"][0]["weight"]) * Fraction(99, 100)
    scaled["sites"][0]["weight"] = text(weight)
    shifted = json.loads(raw)
    step = Fraction(shifted["sites"][0]["weight"]) / 100
    for index, sign in ((0, -1), (1, 1)):
        shifted["sites"][index]["weight"] = text(
            Fraction(shifted["sites"][index]["weight"]) + sign * step
        )
    out: list[dict[str, object]] = []
    for name, change, value, expect in (
        (
            "D1",
            f"generated site {first} moved onto pool rectangle 0 reflected in x",
            moved,
            ("density: no generated box is D4-equivalent to any of the 2526 pool rectangles",),
        ),
        ("D2", "site 0's weight scaled by 99/100", scaled, ("density: the weights sum to M",)),
        ("D3", "a hundredth of site 0's weight moved to site 1", shifted, INPUT_DIGESTS),
    ):
        mutant = json.dumps(value).encode()
        density = site_density(mutant)
        checks = support_checks(support_facts(mutant, pool_raw), density)
        # A control is judged by the checks it names: the input checks only where it
        # names them, since only they can see a change that keeps every orbit fact.
        if any(item in INPUT_DIGESTS for item in expect):
            checks += input_checks(facts(density, CLAIM, RELEASE), CLAIM, RELEASE)
        failed = [c.name for c in checks if not c.held]
        out.append(
            {
                "control": name,
                "change": change,
                "expect_failed": list(expect),
                "failed": failed,
                "refused": all(item in failed for item in expect),
            }
        )
    return out


# --------------------------------------------------------------------------- the price


def lpt_makespan(times: Sequence[float], workers: int) -> float:
    """The wall time of the longest-first schedule on ``workers`` processes, as the
    release's runner and `devtools.audit_continuous_pose` hand out slabs."""
    loads = [0.0] * workers
    for t in sorted(times, reverse=True):
        heapq.heapreplace(loads, loads[0] + t)
    return max(loads)


def t145_calibration() -> dict[str, float]:
    """T-145's slabs as its two receipts timed them, and as its replay here did, on the
    host this record's replays run on (the packet's receipts)."""
    with gzip.open(T145 / "receipts/slabs.jsonl.gz", "rt", encoding="utf-8") as handle:
        here = sum(float(json.loads(line)["cpu_seconds"]) for line in handle if line.strip())
    local = sum(float(row["seconds"]) for row in read_slabs(T145 / "source/results"))
    ci = sum(float(row["seconds"]) for row in read_slabs(T145 / "release-ci/results"))
    return {
        "replay_cpu_seconds_here": round(here, 1),
        "local_receipt_slab_seconds": round(local, 1),
        "ci_receipt_slab_seconds": round(ci, 1),
        "here_over_local": round(here / local, 4),
        "here_over_ci": round(here / ci, 4),
    }


def price() -> dict[str, Any]:
    """What the continuous-pose replay costs here, from the two receipts' slab times
    scaled by T-145's measured ratio, and what the rest of the entry point costs."""
    calibration = t145_calibration()
    times = {name: [float(r["seconds"]) for r in read_slabs(f)] for name, f in RECEIPTS.items()}
    ratio = {"local": calibration["here_over_local"], "ci": calibration["here_over_ci"]}
    predicted = {name: [t * ratio[name] for t in ts] for name, ts in times.items()}
    central = [max(a, b) for a, b in zip(predicted["local"], predicted["ci"], strict=True)]
    receipts = {name: read_receipt(folder) for name, folder in RECEIPTS.items()}
    duals = {
        name: round(
            sum(
                float(stage["seconds"])
                for stage in read_receipt(folder, "obstruction.json").get("stages", [])
            ),
            1,
        )
        for name, folder in RECEIPTS.items()
    }
    return {
        "basis": (
            "each slab's time in both release receipts, scaled by T-145's replay here "
            "over the same receipt's time; the larger of the two predictions per slab"
        ),
        "receipt_slab_seconds": {name: round(sum(ts), 1) for name, ts in times.items()},
        "receipt_longest_slab_seconds": {name: round(max(ts), 1) for name, ts in times.items()},
        "t145_calibration": calibration,
        "predicted_slab_cpu_seconds_here": {
            name: round(sum(ts), 1) for name, ts in predicted.items()
        },
        "predicted_slab_cpu_hours_here": round(sum(central) / 3600, 2),
        "predicted_longest_slab_seconds_here": round(max(central), 1),
        "predicted_wall_seconds_here": {
            str(w): round(lpt_makespan(central, w), 1) for w in (1, 2, 4)
        },
        "receipt_full_entry": {
            name: {
                "seconds": round(float(r["full_entry_seconds"]), 1),
                "workers": r["workers"],
                "worker_seconds": round(float(r["full_entry_seconds"]) * int(r["workers"]), 1),
            }
            for name, r in receipts.items()
        },
        "receipt_dual_seconds": duals,
    }


# --------------------------------------------------------------------------- the report


def pool_check(pool_raw: bytes) -> Check:
    """The original pool, as the release pins it by digest."""
    return Check(
        "density: the pool is rect_n40_L67, as the release pins it",
        sha256(pool_raw) == ORIGINAL_SHA256,
        "the 2026-10-01 packet's copy",
    )


def statement_checks(parameters: dict[str, Any], claim: Claim = CLAIM) -> list[Check]:
    """The claim against what the release states of it: PROOF.md's near-axis margin and
    its retained ``parameters.json``."""
    return [
        Check(
            "near-axis: B - A W(eps) is PROOF.md's margin",
            claim.B - claim.A * extent(claim.eps) == NEAR_AXIS_MARGIN,
            "section 6",
        ),
        Check(
            "retained parameters.json is the claim",
            parameters == claim.parameters(),
            "all keys",
        ),
    ]


def check_report() -> dict[str, Any]:
    """The finite audit: the orbit facts here, then the checks `audit_continuous_pose`
    makes of T-145's release, made of this one (`RELEASE`), and the controls."""
    raw, pool_raw = load_candidate(), load_pool()
    density = site_density(raw)
    s = support_facts(raw, pool_raw)
    f = facts(density, CLAIM, RELEASE)
    least, at = least_bound(read_slabs(RECEIPTS["ci"]))
    parameters = json.loads(PARAMETERS.read_text(encoding="utf-8"))
    margin = CLAIM.B - CLAIM.A * extent(CLAIM.eps)
    checks = [
        pool_check(pool_raw),
        *support_checks(s, density),
        *input_checks(f, CLAIM, RELEASE),
        *chain_checks(CLAIM, f, least, RELEASE),
        *statement_checks(parameters),
    ]
    for name, folder in RECEIPTS.items():
        checks += receipt_checks(
            name, folder, CLAIM, f, release=RELEASE, admission=release_admission(s, f)
        )
    checks += identity_checks(RELEASE) + kernel_checks()
    controls = finite_controls(f, least, FINITE_CONTROLS, RELEASE)
    controls += density_controls(raw, pool_raw)
    held = all(c.held for c in checks) and all(item["refused"] for item in controls)
    minimum = Fraction(f.minimum, GRID**3)
    return {
        "kind": "n40-new-supports-finite-audit/v1",
        "claim": f"s(40) > {text(CLAIM.X)}",
        "candidate": str(CANDIDATE.relative_to(REPO)),
        "values": {
            "raise_over_T145": text(RAISE),
            "counting_margin": text(CLAIM.n * CLAIM.tau - CLAIM.mass),
            "near_axis_margin": text(margin),
            "near_axis_margin_decimal": f"{float(margin):.6g}",
            "kernel_threshold": float.hex(kernel_threshold(CLAIM.tau)),
            "least_leaf_bound": text(least),
            "least_leaf_bound_slab": at,
            "least_leaf_bound_minus_tau": f"{float(least - CLAIM.tau):.6g}",
            "axis_minimum": text(minimum),
            "axis_margin_decimal": f"{float(minimum - CLAIM.tau):.6g}",
            "axis_minimiser": [f.minimiser[0], f.minimiser[1]],
            "g_capture_at_axis_minimiser": f"{float(f.minimiser_capture_g):.15g}",
            "dominated_mass_deficit": f"{float(CLAIM.mass - f.dominated_mass):.6g}",
            "evaluation_bound": str(f.evaluation_bound),
            "distinct_rectangles": f.distinct,
            "inherited_positive_in_rect_n40_L67": s.inherited_positive_before,
            "pose_input_sha256": f.pose_sha256,
            "axis_input_sha256": f.axis_sha256,
        },
        "checks": [c.as_json() for c in checks],
        "controls": controls,
        "price": price(),
        "status": "FINITE_STEPS_HOLD" if held else "FINITE_AUDIT_FAILED",
    }


# --------------------------------------------------------------------------- the axis run


AXIS_SOURCE = KERNEL_SOURCES["axis"]
#: The thresholds either side of the reported minimum 1.0014864314...: the kernel must
#: refuse the first (exit 2) and prove the second, as T-145's control H did. The kernel
#: admits a threshold's numerator and denominator up to 10^6 each, so the one above is
#: 1.001488 = 62593/62500 (1001487/10^6 stops at its input bounds, exit 3).
AXIS_CONTROLS = (
    ("H-above", Fraction(1001488, 10**6), 2, "AXIS_TEST_REFUSED"),
    ("H-below", Fraction(1001486, 10**6), 0, "AXIS_COVERAGE_PROVED"),
)


#: The standard net the crate's near-axis input names: its step and its angle count.
CRATE_NET = (Fraction(83, 40000), 201)


def crate_axis_input(density: Density) -> bytes:
    """``sqverify-fast``'s near-axis input: the 685 rows with weights scaled by
    `CRATE_SCALE`, side ``A`` on the standard net, threshold one."""
    return crate_input(density, CLAIM.A, *CRATE_NET)


def run_axis(out: Path, crate: Path | None) -> dict[str, Any]:
    """Build the axis kernel from the retained source in ``out`` as ``run.py`` does,
    run it on the derived input and at the two control thresholds, and run the crate."""
    density = site_density(load_candidate())
    tree, build, logs = out / "tree", out / "build", out / "logs"
    for folder in (tree / "verifier", build, logs):
        folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / AXIS_SOURCE, tree / AXIS_SOURCE)
    binary = build / "axis"
    argv = ["g++", *FLAGS, AXIS_SOURCE, "-o", str(binary)]
    compiler = subprocess.run(
        ["g++", "--version"], capture_output=True, text=True, check=True
    ).stdout.splitlines()[0]
    built = spawn(argv, tree, logs / "build-axis")
    record: dict[str, Any] = {
        "kind": "n40-new-supports-axis-stage/v1",
        "compiler": compiler,
        "build": {
            "argv": [*argv[:-1], "axis"],
            "source_sha256": sha256((tree / AXIS_SOURCE).read_bytes()),
            "binary_sha256": sha256(binary.read_bytes()) if binary.exists() else None,
            **built,
        },
    }
    rows = axis_rows(density)
    runs: dict[str, Any] = {}
    for name, tau in (("axis", CLAIM.tau), *((n, t) for n, t, _, _ in AXIS_CONTROLS)):
        data = axis_input(rows, CLAIM, tau)
        (out / f"{name}-input.txt").write_bytes(data)
        result = spawn([str(binary), f"{name}-input.txt"], out, logs / name)
        runs[name] = {"tau": text(tau), "input_sha256": sha256(data), **result}
        print(f"{name}: exit {result['exit_code']}, {result['wall_seconds']} s", flush=True)
    record["runs"] = runs
    if crate is not None:
        source = crate_source_sha256()
        reviewed = REVIEWED_SOURCES.get(source)
        if reviewed is None or not reviewed.declared_nets:
            raise SystemExit(f"{source} is not reviewed source for a declared net")
        data = crate_axis_input(density)
        (out / "axis-A.json").write_bytes(data)
        argv = [str(crate), "--candidate", "axis-A.json", "--n", "40", "--side", "67/10"]
        argv += ["--directions", "0", "--threshold", "1", "--threads", "1", "--confirm"]
        result = spawn(argv, out, logs / "crate-axis-A")
        print(f"crate-axis-A: exit {result['exit_code']}, {result['wall_seconds']} s")
        record["crate"] = {
            "argv": ["sqverify-fast", *argv[1:]],
            "binary_sha256": sha256(crate.read_bytes()),
            "crate_source_sha256": source,
            "reviewed_source": {"commit": reviewed.commit, "review": reviewed.review},
            "input_sha256": sha256(data),
            **result,
        }
    receipts = out / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    write_json(receipts / "axis-stage.json", record)
    return record


def json_object(value: object) -> dict[str, Any]:
    """A program's output read as a JSON object, or an empty one when it printed anything
    else, so that a run which stops with other output fails its check rather than
    raising."""
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


#: The check that holds only on the crate's own decision of the near-axis statement.
CRATE_DECISION = "crate: the near-axis statement at side A by the exact vertex sweep"


def axis_stage_checks(
    record: dict[str, Any], density: Density, *, require_crate: bool = True
) -> list[Check]:
    """The axis stage's receipts against both release receipts and ``density``. The
    stage's second decision of the near-axis statement is the crate's, on the input
    derived here from ``density``, which must be the release's candidate
    (`CANDIDATE_SHA256`), so a record without it fails `CRATE_DECISION` unless
    ``require_crate`` is false, for a run made without the crate."""
    build, runs = record["build"], record["runs"]
    release = [
        json.loads(str(read_receipt(folder, "axis.json")["stdout"]))
        for folder in RECEIPTS.values()
    ]
    axis = runs["axis"]
    output = json_object(axis["stdout"]) if axis["exit_code"] == 0 else {}
    ci_compiler = record["compiler"] == CI_COMPILER
    checks = [
        Check(
            "axis build: the retained source, the release's flags",
            build["exit_code"] == 0 and build["argv"][1:5] == list(FLAGS),
            f"{record['compiler']}, binary {str(build['binary_sha256'])[:12]}...",
        ),
        Check(
            "axis build: with the CI run's compiler, the CI run's binary",
            not ci_compiler or build["binary_sha256"] == CI_BINARIES["axis"],
            "compared" if ci_compiler else "another compiler; not compared",
        ),
        Check(
            "axis run: the derived input, every output field both receipts'",
            axis["exit_code"] == 0
            and axis["input_sha256"] == AXIS_SHA256
            and all(output == r for r in release),
            f"{output.get('status')}, minimum {output.get('minimum_numerator')}, "
            f"{axis['wall_seconds']} s",
        ),
    ]
    for name, tau, code, status in AXIS_CONTROLS:
        run = runs[name]
        seen = json_object(run["stdout"]).get("status")
        checks.append(
            Check(
                f"axis control {name}: tau = {text(tau)} gives {status}",
                run["exit_code"] == code and seen == status and run["tau"] == text(tau),
                f"exit {run['exit_code']}, {seen}",
            )
        )
    if "crate" not in record:
        if require_crate:
            checks.append(
                Check(
                    CRATE_DECISION,
                    held=False,
                    detail="not in the record: run without --crate-binary",
                )
            )
        return checks
    crate = record["crate"]
    lines = [json_object(line) for line in crate["stdout"].splitlines() if line]
    row = next((x for x in lines if "r" in x), {})
    summary = next((x for x in lines if x.get("kind")), {})
    premises = summary.get("premises") or {}
    reviewed = REVIEWED_SOURCES.get(str((summary.get("build") or {}).get("source_sha256")))
    derived = sha256(crate_axis_input(density))
    return [
        *checks,
        Check(
            "crate: reviewed source for a declared net, the binary embeds it",
            reviewed is not None and reviewed.declared_nets,
            str((summary.get("build") or {}).get("source_sha256")),
        ),
        Check(
            CRATE_DECISION,
            crate["exit_code"] == 0
            and density.sha256 == CANDIDATE_SHA256
            and crate.get("input_sha256") == premises.get("input_sha256") == derived
            and premises.get("L") == text(CLAIM.L)
            and premises.get("n") == CLAIM.n
            and crate_premises(
                summary,
                CLAIM.A,
                *CRATE_NET,
                rows=COUNTS["sites"],
                expanded=len(density.merged),
                mass=CLAIM.mass,
            )
            and row.get("verdict") == "verified"
            and row.get("method") == "axis-vertex-sweep"
            and float(row.get("min_certified_lower_bound", 0)) >= 1,
            f"{row.get('verdict')} on the input derived here, {derived[:12]}..., "
            f"{row.get('vertices')} vertices, least {row.get('min_certified_lower_bound')!r} "
            f"at {row.get('argmin')}, {crate['wall_seconds']} s",
        ),
    ]


#: What the axis stage's judgement says when it holds without the crate's decision, which
#: never claims the full stage.
KERNEL_ONLY = "AXIS_KERNEL_HOLDS_WITHOUT_CRATE"
#: The statuses a judgement exits zero on.
HOLDS = frozenset({"FINITE_STEPS_HOLD", "AXIS_STAGE_HOLDS", KERNEL_ONLY, "REPLAY_HOLDS"})


# --------------------------------------------------------------------------- the replay


#: Control H in the complete replay: the contract's threshold as T-145's contract wrote
#: it, 1/2, which the kernel proves since it is below the minimum, and the pair either
#: side of this release's minimum that `AXIS_CONTROLS` names.
REPLAY_AXIS_CONTROLS = (
    ("H-tau-1-2", Fraction(1, 2)),
    *((name, tau) for name, tau, _, _ in AXIS_CONTROLS),
)
#: Control G on the release's own ``exact.py``: the one line that sets the axis side
#: (found by searching the retained file for ``axis_side``, which is all of it that was
#: read), and the mutant one step of 1/250000000 larger, the finite audit's control G.
RELEASE_G_CHANGE = (
    "'axis_side':'249329659/250000000'",
    "'axis_side':'249329660/250000000'",
)
#: What the contract states for the complete run, from both release receipts (the slab
#: totals, the least leaf bound and the axis minimum) and from the axis stage's crate
#: decision (`receipts/axis-stage.json`); the 401-direction values are this replay's own
#: first run, pinned so that a later run must reproduce them.
EXPECT: dict[str, Any] = {
    "nodes": 60_500_889,
    "leaves": 30_250_466,
    "angle_splits": 13_812_428,
    "least_bound": Fraction(9005397816695287, 2**53),
    "least_bound_slab": 40,
    "axis_minimum": Fraction(1001486431423867090847280653, GRID**3),
    "crate_axis_vertices": 10_929_636,
    "crate_axis_bound": 1.0016868361671276,
    "crate_net_nodes": 35_375_590,
    "crate_net_bound": 1.000000000310131,
    "crate_net_bound_r": 398,
}
#: This release's replay through T-145's runner and judge.
REPLAY = Replay(
    release=RELEASE,
    density=lambda: site_density(load_candidate()),
    axis_controls=REPLAY_AXIS_CONTROLS,
    release_g=RELEASE_G_CHANGE,
    expect=EXPECT,
    crate_rows=COUNTS["sites"],
    crate_expanded=5424,
)


#: The replay's stages: T-145's, then the release's two dual programs.
REPLAY_STAGES = (*STAGES, "duals")
#: The file the release pins by digest and does not carry, which its dual programs read:
#: wand125's pool, written into the scratch tree from the 2026-10-01 packet's copy.
POOL_UPSTREAM = "certificate/original_density.json"
#: The keys of the release's ``obstruction.json`` that time its runs or name a binary,
#: which differ between runs; every other field must equal both receipts'.
DUAL_TIMING = frozenset({"seconds", "binary_sha256", "stages"})
DUAL_STATUS = "EXACT_DUAL_CODE_DISTINCT_CHECKED"


def assemble_tree(root: Path) -> dict[str, str]:
    """A scratch copy of the retained tree at its upstream paths for the release's own
    programs: every retained file (the two compressed ones restored) and the pinned pool,
    each held to the manifest's digest. Returns the digests written."""
    digests = manifest(RELEASE.manifest_path)
    written: dict[str, str] = {}
    for path, digest in digests.items():
        data = load_pool() if path == POOL_UPSTREAM else read_retained_bytes(SOURCE / path)
        if sha256(data) != digest:
            raise SystemExit(f"{path}: the retained bytes are not the manifest's")
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        written[path] = digest
    return written


def run_duals(out: Path) -> dict[str, Any]:
    """The release's ``obstruction/run.py``, its own entry point for OBSTRUCTION.md's
    finite dual, on a scratch copy of the retained tree: the Python ``Fraction`` program,
    the C++ Boost program built as the release builds it, and its one-pose false dual.
    The result bears on no register value."""
    root = out / "tree-duals"
    tree = assemble_tree(root)
    target = out / "duals"
    if target.exists():
        shutil.rmtree(target)
    compiler = subprocess.run(
        ["g++", "--version"], capture_output=True, text=True, check=True
    ).stdout.splitlines()[0]
    argv = [sys.executable, "-B", "obstruction/run.py", "--output", str(target)]
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    result = spawn(argv, root, logs / "duals")
    print(f"duals: exit {result['exit_code']}, {result['wall_seconds']} s", flush=True)
    written = target / "obstruction.json"
    obstruction = json.loads(written.read_text(encoding="utf-8")) if written.exists() else None
    return {
        "kind": "n40-new-supports-replay-duals/v1",
        "argv": ["python", "-B", "obstruction/run.py", "--output", "duals"],
        "python": sys.version.split()[0],
        "compiler": compiler,
        "tree": tree,
        "obstruction": obstruction,
        **result,
    }


def dual_checks(record: dict[str, Any]) -> list[Check]:
    """The duals' receipt against both release receipts' ``obstruction.json``: the
    release's own status, and every field that neither times a run nor names a binary,
    equal; with the CI run's compiler, the CI run's dual binary."""
    ours = record.get("obstruction") or {}
    theirs = {
        name: read_receipt(folder, "obstruction.json") for name, folder in RECEIPTS.items()
    }

    def fixed(value: dict[str, Any]) -> dict[str, Any]:
        out = {k: v for k, v in value.items() if k not in DUAL_TIMING}
        for program in ("python", "cpp"):
            out[program] = {k: v for k, v in (out.get(program) or {}).items() if k != "seconds"}
        return out

    manifest_digests = manifest(RELEASE.manifest_path)
    checks = [
        Check(
            "duals: the retained tree at its upstream paths, every file the manifest's",
            record.get("tree") == manifest_digests,
            f"{len(record.get('tree') or {})} files",
        ),
        Check(
            "duals: the release's obstruction entry point, exit 0",
            record.get("exit_code") == 0 and ours.get("status") == DUAL_STATUS,
            f"{ours.get('status')}, {record.get('wall_seconds')} s",
        ),
    ]
    for name, receipt in theirs.items():
        checks.append(
            Check(
                f"duals: every non-timing field equals the {name} receipt's",
                fixed(ours) == fixed(receipt),
                f"column {ours.get('python', {}).get('max_column')}, "
                f"slack {ours.get('python', {}).get('strict_scaled_slack')}",
            )
        )
    ci_compiler = record.get("compiler") == CI_COMPILER
    checks.append(
        Check(
            "duals: with the CI run's compiler, the CI run's dual binary",
            not ci_compiler or ours.get("binary_sha256") == theirs["ci"].get("binary_sha256"),
            str(ours.get("binary_sha256")) if ci_compiler else "another compiler; not compared",
        )
    )
    return checks


def replay_check(folder: Path) -> dict[str, Any]:
    """The replay's receipts judged as `devtools.audit_continuous_pose.replay_report`
    judges T-145's, with this release's contract, and the duals' receipt after them."""
    shared = replay_report(folder, REPLAY)
    duals = dual_checks(retained_json(folder / "duals.json"))
    checks = [*shared["checks"], *(c.as_json() for c in duals)]
    held = all(c["held"] for c in checks)
    return {
        **shared,
        "kind": "n40-new-supports-replay-check/v1",
        "checks": checks,
        "status": "REPLAY_HOLDS" if held else "REPLAY_CHECK_FAILED",
    }


def axis_report(folder: Path, *, require_crate: bool = True) -> dict[str, Any]:
    """The axis stage's judgement: `AXIS_STAGE_HOLDS` only with the crate's decision on
    this density, and `KERNEL_ONLY` when the record has none and none was required."""
    record = json.loads((folder / "axis-stage.json").read_text(encoding="utf-8"))
    checks = axis_stage_checks(
        record, site_density(load_candidate()), require_crate=require_crate
    )
    held = all(c.held for c in checks)
    status = "AXIS_STAGE_HOLDS" if "crate" in record else KERNEL_ONLY
    return {
        "kind": "n40-new-supports-axis-check/v1",
        "checks": [c.as_json() for c in checks],
        "status": status if held else "AXIS_STAGE_FAILED",
    }


# --------------------------------------------------------------------------- the CLI


def emit(report: dict[str, Any], output: Path | None) -> int:
    if output is not None:
        write_json(output, report)
    for item in report.get("checks", []):
        print(f"{'ok  ' if item['held'] else 'FAIL'} {item['name']}: {item['detail']}")
    for item in report.get("controls", []):
        mark = "refused " if item["refused"] else "ADMITTED"
        print(f"{mark} control {item['control']} ({item['change']}): failed {item['failed']}")
    if "price" in report:
        print(json.dumps(report["price"], indent=2, sort_keys=True))
    print(report["status"])
    return 0 if report["status"] in HOLDS else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    derive = commands.add_parser("derive", help="write the kernel and crate inputs")
    derive.add_argument("--out", type=Path, required=True)
    check = commands.add_parser("check", help="the finite audit, its controls and the price")
    check.add_argument("--output", type=Path)
    run = commands.add_parser("run-axis", help="build and run the axis kernel and the crate")
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--crate-binary", type=Path)
    judge = commands.add_parser("check-axis", help="judge the axis stage's receipts")
    judge.add_argument("--receipts", type=Path, default=RECEIPT_DIR)
    judge.add_argument("--output", type=Path)
    judge.add_argument(
        "--without-crate",
        action="store_true",
        help="judge a stage run without --crate-binary: the crate's decision is not required",
    )
    replay = commands.add_parser("run-replay", help="build the kernels and run the replay")
    replay.add_argument("--out", type=Path, required=True)
    replay.add_argument("--workers", type=int, default=2)
    replay.add_argument("--stages", default=",".join(REPLAY_STAGES))
    replay.add_argument("--crate-binary", type=Path)
    judge_replay = commands.add_parser("check-replay", help="judge the replay's receipts")
    judge_replay.add_argument("--receipts", type=Path, default=RECEIPT_DIR)
    judge_replay.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if args.command == "run-replay":
        stages = [s for s in args.stages.split(",") if s]
        if not set(stages) <= set(REPLAY_STAGES) or not 1 <= args.workers <= 8:
            parser.error(f"--stages from {','.join(REPLAY_STAGES)}; --workers from 1 to 8")
        out = args.out.resolve()
        crate = args.crate_binary.resolve() if args.crate_binary else None
        run_replay(out, args.workers, [s for s in stages if s in STAGES], crate, REPLAY)
        if "duals" in stages:
            write_json(out / "receipts/duals.json", run_duals(out))
        return 0
    if args.command == "check-replay":
        return emit(replay_check(args.receipts), args.output)
    if args.command == "derive":
        density = site_density(load_candidate())
        args.out.mkdir(parents=True, exist_ok=True)
        files = {
            "certificate_input.txt": pose_input(density, CLAIM, RELEASE),
            "axis-input.txt": axis_input(axis_rows(density), CLAIM),
            "axis-A.json": crate_axis_input(density),
        }
        for name, data in files.items():
            (args.out / name).write_bytes(data)
            print(f"{sha256(data)}  {name}")
        return 0
    if args.command == "check":
        return emit(check_report(), args.output)
    if args.command == "run-axis":
        crate = args.crate_binary.resolve() if args.crate_binary else None
        run_axis(args.out.resolve(), crate)
        if crate is None:
            print("crate: not run; check-axis refuses these receipts without --without-crate")
        receipts = args.out.resolve() / "receipts"
        return emit(axis_report(receipts, require_crate=crate is not None), None)
    return emit(axis_report(args.receipts, require_crate=not args.without_crate), args.output)


if __name__ == "__main__":
    sys.exit(main())
