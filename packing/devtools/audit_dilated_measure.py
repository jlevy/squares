"""Audit a format M certificate made by dilating a retained one onto a declared net.

Doğa Özden's `s(94) >= 1993/200` (jlevy/squares#890) is Hiroaki Hosono's
`mixed_n94_L995` measure dilated about the origin by `λ = 1993/1990`, with a finer net
declared (`proof_net`) so that the dilated core still fits a unit square, and his
`s(94) >= 2493/250` (#910) is the same measure dilated by `λ = 4986/4975` onto a net of
4,972 half-angles of step `1/12000`. Each bound rests on a complete coverage decision by
`sqverify-fast`, which `devtools.sqverify_fast_census` runs and keeps; this tool is the
first-party premise check of their imports, the comparison of that decision with the
producer's receipts, and the audit of a producer's own receipt archive. It decides no
coverage. `DILATIONS` names each certificate it reads, by its packet, with the rule its
source's rescale tool states (`Dilation.canonical`, `Dilation.derived_from`).

- ``audit`` recomputes, from the packet's retained files and the base packet's, in exact
  rationals and apart from the crate:

  - the file: format M, rectangles only (each row exactly four coordinates and a mass),
    `scaling_factor` absent or 1, a `proof_net`
    with exactly `step` and `last` (and `count = last + 1` if given), no top-level
    `net`, and eight times the densest row's density at most `2^32` (item 1 of the
    records-lane checklist of the 6 October declared-net soundness review);
  - the measure: every mass nonnegative, every rectangle nondegenerate and inside the
    container, the masses totalling exactly the stated `total_mass`, `n - 1/100000`,
    below `n`;
  - lemma N0's (a) to (e) on the declared net (`sqverify_fast/SOUNDNESS.md`);
  - the dilation: `L = λ L₀` and `B = λ B₀`, the same row count, each rectangle `λ`
    times the base's row by row, and each mass equal;
  - the regeneration: the base rewritten as the source's `tools/rescale.py` says,
    serialized as that script writes it (Python's `json.dump` for #890, canonical JSON
    with sorted keys and compact separators for #910), is byte for byte the retained
    file's decompressed text. The receipt records each text's SHA-256 beside the one the
    source states, and the stored files' too where the source states them, as data: Git
    holds the retained bytes (OR-16), and the stage 2 custody check compared them once;
  - and, as observations its status requires nothing of, what the dilation does not
    carry: `λ B₀ (1 + D₀)` on the base's own net (its declared step, else the standard
    one), the direction-0 centre domain's growth `ρ₀ (1 - 1/λ)` in the base's
    coordinates, the growth `m₀(t) - m(t)/λ` at each node the two nets share, where
    `m(t) = rho(max(0, t - D/2))` is format M's per-bin wall margin on each net
    (`sqverify_fast/SOUNDNESS.md`, lemma D), the nodes the base's net does not have, the
    route's ceiling `L₀ / B₀`, and, where the source states its gzip encoding, whether
    that encoding of the regenerated text is the stored file.

- ``receipts`` audits a producer's receipt archive assembled from several native
  `sqverify-fast` runs (`ReceiptArchive`), from the retained files alone and without
  running the crate: every native stream's rows are exactly its declared scope, its
  summary is the separate summary file, refuses nothing and states the certificate's
  premises, as this tool recomputes them, and a build of crate source that a review
  accepted for declared nets (`sqverify_fast_census.REVIEWED_SOURCES`), with the same
  compiler, profile and target as the census binary's row (`REFERENCE_ROW`); the
  retained copy of the crate the producer built is that source by `build.rs`'s rule;
  the merged archive holds each direction of the net once, verified at threshold 1 with
  a finite certified bound of at least 1, and each of its lines is byte for byte the
  line of the stream the selection names; and the mass-scaled control is every mass
  times its factor, refused natively, with its exact witnesses' captures recomputed by
  `check_sqverify_fast.mixed_exact`, written apart from the crate, below 1 at centres in
  the per-bin domain. It records the nodes of the selected rows, which price a replay.

- ``compare`` reads the census capture (`census-mixed/PACKET/NAME.jsonl.gz`) and each
  receipt of the producer's own `sqverify-fast` runs, and compares them direction by
  direction on every field but the two timings (`cpu_seconds`, `seconds`), and their
  summaries on status, nodes, refused directions and premises. It also reads the
  producer's second checker's replay (`second-checker/full.jsonl`) for its verdicts and
  least bound, as a reading of the producer's output that decides nothing.

``--check`` recomputes a receipt and fails unless it equals the retained one and passes
(`PREMISES_HOLD`, `EVERY_DIRECTION_AGREES`, `RECEIPTS_HOLD`). A capture or receipt with
a line that is neither a direction row nor the summary, a direction twice, or no summary
or a second one, is refused, and so is a merged archive or selection with a direction
twice.

From ``packing/``::

    .venv/bin/python3 -m devtools.audit_dilated_measure audit \\
        ozden-s94-lower-bound-2026-11-03 --write
    .venv/bin/python3 -m devtools.audit_dilated_measure compare \\
        ozden-s94-lower-bound-2026-11-03 --write
    .venv/bin/python3 -m devtools.audit_dilated_measure audit \\
        ozden-s94-lower-bound-9972-2026-11-05 --check
    .venv/bin/python3 -m devtools.audit_dilated_measure receipts \\
        ozden-s94-lower-bound-9972-2026-11-05 --check
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_sqverify_fast import crate_source_sha256, mixed_exact
from devtools.retained_data import read_original_gzip_bytes, read_retained_bytes
from devtools.sqverify_fast_census import REVIEWED_SOURCES, domain_bounds
from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
CENSUS = PROJECT / "benchmarks/measure-verifier/census-mixed"
#: The census row whose build is this repository's census binary for format M on a
#: declared net (`567a0fd5...`, rustc 1.98.0, release): a producer's receipts of the
#: same compiler, profile, target and reviewed source are of the same build.
REFERENCE_ROW = "mixed_n94_L9965"

#: The keys a format M certificate may carry, beside the ones this audit reads.
FORMAT_M_KEYS = frozenset(
    {"n", "L", "B", "total_mass", "points", "rectangles", "proof_net", "derived_from"}
)
#: Lemma N0 (a)'s cap on a declared net's direction count.
MAX_DIRECTIONS = 2**16
#: Item 1's cap on eight times the densest row's density.
MAX_DENSITY = 2**32
#: The standard net's step and last index, on which the base certificate stands.
STANDARD_STEP = Fraction(83, 40000)
STANDARD_LAST = 200
#: The two timings a direction's row records, which no two runs share.
TIMINGS = frozenset({"cpu_seconds", "seconds"})
#: The premises a native summary states that this tool recomputes from the certificate.
RECOMPUTED_PREMISES = (
    "B",
    "D",
    "L",
    "angle_count",
    "centre_domain",
    "expanded_points",
    "expanded_segments",
    "format",
    "mass_below_n",
    "mass_exact",
    "n",
    "net_last_tangent",
    "net_origin",
    "shrink_bound",
    "source_rectangles",
)
#: The build facts besides the source digest that make two builds the same build.
BUILD_FACTS = ("profile", "rustc", "target")
#: The verdicts a native row gives a refusal on coverage: an oblique direction's
#: counterexample candidate and the axis vertex sweep's refusal.
REFUSALS = frozenset({"counterexample-candidate", "refused"})


@dataclass(frozen=True)
class ReceiptArchive:
    """A producer's receipts of every direction, assembled from several native runs.

    Each path is relative to the packet; a native stream's own paths are the index's,
    relative to the packet's archived source directory (`root`).
    """

    #: The archived source directory the index's paths are relative to.
    root: str
    #: The index of the native streams: their scopes, files and summaries.
    index: str
    #: The merged archive, one selected native line per direction.
    merged: str
    #: The CSV that names, for each direction, the stream its line was selected from.
    selection: str
    #: The certificate with every mass times `mutant_factor`.
    mutant: str
    mutant_factor: Fraction
    #: The native receipts of the mutant.
    mutant_receipts: str
    #: The producer's exact witness against the mutant (`exact_counterexample`).
    witness: str
    #: The producer's copy of the `sqverify-fast` crate it built.
    crate: str


@dataclass(frozen=True)
class Dilation:
    """One dilated certificate and the retained one it dilates."""

    #: The census name of the certificate (`sqverify_fast_census.MIXED_FILES`).
    name: str
    n: int
    side: Fraction
    #: The certificate, relative to its packet.
    candidate: str
    #: The base candidate, relative to `resources/web/`.
    base: str
    #: The SHA-256 the source states for the base's JSON text.
    base_sha256: str
    #: The SHA-256 the source states for the certificate's JSON text.
    text_sha256: str
    #: The SHA-256 the source states for the certificate as stored, its gzip.
    stored_sha256: str
    #: The producer's `sqverify-fast` receipts of a complete run, relative to the packet.
    receipts: tuple[str, ...] = ()
    #: The producer's second checker's replay, relative to the packet.
    second_checker: str = ""
    #: Whether the source's rescale writes canonical JSON: sorted keys, compact separators.
    canonical: bool = False
    #: The `derived_from` text the source's rescale writes; empty for #890's template.
    derived_from: str = ""
    #: The SHA-256 the source states for the base as it retains it, a gzip.
    base_stored_sha256: str = ""
    #: The gzip header's OS byte where the source states its encoding (level 9, mtime 0).
    gzip_os: int | None = None
    #: The producer's receipt archive of several native runs.
    archive: ReceiptArchive | None = None


DILATIONS: dict[str, Dilation] = {
    "ozden-s94-lower-bound-2026-11-03": Dilation(
        name="mixed_n94_L9965",
        n=94,
        side=Fraction(1993, 200),
        candidate="source/certificate/n94_L9965.json.gz",
        base=(
            "wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/"
            "mixed_n94_L995/candidate.json.gz"
        ),
        base_sha256="64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a",
        text_sha256="b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c",
        stored_sha256="116c83425959a943196287a910ad799b2fe1bb9dec433085ea222bd62d5a16f8",
        receipts=(
            "source/receipts/sqverify-fast-rustc1.98-full.jsonl",
            "source/receipts/sqverify-fast-rustc1.93-full.jsonl",
        ),
        second_checker="source/second-checker/full.jsonl",
    ),
    # #910: the same base dilated further, onto a finer net; its rescale writes
    # canonical JSON and a deterministic gzip, and its receipts are an archive of several
    # native runs, with a mass-scaled control at two directions.
    "ozden-s94-lower-bound-9972-2026-11-05": Dilation(
        name="mixed_n94_L9972",
        n=94,
        side=Fraction(2493, 250),
        candidate="source/certificate/n94-L9972.json.gz",
        base=(
            "wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/"
            "mixed_n94_L995/candidate.json.gz"
        ),
        base_sha256="64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a",
        text_sha256="d1df3bc69bb12c0eebcb51d6b3636593079fbb82ae1128938ec5c07c83cc951c",
        stored_sha256="f59d4c9562d7246f41c8c389a5bc118da9cf268a794e6416d146a195fb03360c",
        canonical=True,
        derived_from="Hiroaki Hosono (wand125), mixed_n94_L995; exact similarity 4986/4975",
        base_stored_sha256="df3ae678029f3da1f0fd4c9b1ba9d331c582478e46c453f238c36e476d9fd27c",
        gzip_os=255,
        archive=ReceiptArchive(
            root="source",
            index="source/receipts/INDEX.json",
            merged="source/receipts/directions.jsonl.gz",
            selection="source/receipts/selection.csv",
            mutant="source/controls/mass-99-100.json.gz",
            mutant_factor=Fraction(99, 100),
            mutant_receipts="source/controls/native-mutant.jsonl",
            witness="source/controls/control.json",
            crate="source/verifier/sqverify_fast",
        ),
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_of(path: Path) -> bytes:
    """A retained file's JSON text: decompressed when it is gzip."""
    raw = path.read_bytes()
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def as_text(value: Fraction) -> str:
    return str(value)


def rectangles(data: dict[str, Any]) -> list[tuple[list[Fraction], Fraction]]:
    return [
        ([Fraction(v) for v in row["rectangle"]], Fraction(row["mass"]))
        for row in data["rectangles"]
    ]


def file_checks(data: dict[str, Any], dilation: Dilation) -> dict[str, Any]:
    """Item 1 of the records-lane checklist, and the measure's own premises."""
    side = Fraction(data["L"])
    net = data.get("proof_net")
    net_keys = sorted(net) if isinstance(net, dict) else None
    # Each row is exactly a rectangle of four coordinates and a mass; the geometry is
    # read only when every row has that shape.
    shaped = all(
        isinstance(row, dict)
        and set(row) == {"rectangle", "mass"}
        and isinstance(row["rectangle"], list)
        and len(row["rectangle"]) == 4
        for row in data["rectangles"]
    )
    rows = rectangles(data) if shaped else []
    masses = [mass for _, mass in rows]
    densities = [
        mass / ((box[2] - box[0]) * (box[3] - box[1]))
        for box, mass in rows
        if box[2] > box[0] and box[3] > box[1]
    ] or [Fraction(0)]
    total = sum(masses, Fraction(0))
    stated = Fraction(data["total_mass"])
    return {
        "n_matches": int(data["n"]) == dilation.n,
        "side_matches": side == dilation.side,
        "format_m": data.get("points") == [] and "segments" not in data,
        "keys_known": sorted(set(data) - FORMAT_M_KEYS) == [],
        "every_row_a_rectangle_of_four_and_a_mass": shaped,
        "scaling_factor": data.get("scaling_factor"),
        "scaling_factor_absent_or_one": Fraction(str(data.get("scaling_factor", 1))) == 1,
        "proof_net_keys": net_keys,
        "proof_net_exact_keys": net_keys in (["last", "step"], ["count", "last", "step"]),
        "count_is_last_plus_one": (
            isinstance(net, dict)
            and int(net.get("count", int(net["last"]) + 1)) == int(net["last"]) + 1
        ),
        "no_top_level_net": "net" not in data,
        "no_certificate_metadata": "certificate" not in data,
        "rows": len(data["rectangles"]),
        "every_mass_nonnegative": shaped and all(mass >= 0 for mass in masses),
        "every_rectangle_nondegenerate": shaped
        and all(box[2] > box[0] and box[3] > box[1] for box, _ in rows),
        "every_rectangle_inside": shaped
        and all(
            box[0] >= 0 and box[2] <= side and box[1] >= 0 and box[3] <= side for box, _ in rows
        ),
        "total_mass": as_text(total),
        "total_mass_equals_stated": total == stated,
        "mass_gap": as_text(dilation.n - total),
        "mass_is_n_minus_1_100000": total == dilation.n - Fraction(1, 100000),
        "mass_below_n": total < dilation.n,
        "densest_row": as_text(max(densities)),
        "densest_row_approx": float(max(densities)),
        "eight_densest_within_2_32": 8 * max(densities) <= MAX_DENSITY,
    }


def lemma_n0(data: dict[str, Any]) -> dict[str, Any]:
    """Lemma N0's (a) to (e) on the file's declared net, in exact rationals."""
    core = Fraction(data["B"])
    step = Fraction(data["proof_net"]["step"])
    last = int(data["proof_net"]["last"])
    count = last + 1
    tangent = last * step
    shrink = core * (1 + step)
    endpoint = tangent**2 + 2 * tangent - 1
    tangent_form = core * (1 + step / (1 - step**2 / 4))
    return {
        "B": as_text(core),
        "D": as_text(step),
        "angle_count": count,
        "net_last_tangent": as_text(tangent),
        "a_step_positive_and_count_in_range": step > 0 and 2 <= count <= MAX_DIRECTIONS,
        "b_shrink": as_text(shrink),
        "b_shrink_below_one": shrink < 1,
        "c_endpoint": as_text(endpoint),
        "c_endpoint_positive": endpoint > 0,
        "d_last_tangent_at_most_half": tangent <= Fraction(1, 2),
        "e_tangent_form": as_text(tangent_form),
        "e_tangent_form_below_one": tangent_form < 1,
    }


def rescaled_text(
    base_text: bytes,
    side: Fraction,
    step: Fraction,
    last: int,
    *,
    canonical: bool = False,
    derived_from: str = "",
) -> bytes:
    """The base rewritten as the source's `tools/rescale.py` says, as that script writes it.

    The rule both retained scripts state: set `L` and `B`, add `proof_net`, scale every
    rectangle coordinate by `λ` and keep each mass as its text, write `n` as an integer,
    drop `scaling_source_digest` and `scaling_factor`, and add `derived_from`. Every
    number is read as its text, so nothing is rounded. #890's script keeps the base's keys
    in order, appends the new ones and writes as `json.dump` does, with a `derived_from`
    naming the base's side and `λ`; #910's writes canonical JSON (`canonical`: sorted
    keys, compact separators) with the `derived_from` text it states.
    """
    data = json.loads(base_text, parse_float=str, parse_int=str)
    scale = side / Fraction(data["L"])
    out = dict(data)
    out["L"] = str(side)
    out["B"] = str(Fraction(data["B"]) * scale)
    out["proof_net"] = {"step": str(step), "last": last}
    out["rectangles"] = [
        {"rectangle": [str(Fraction(v) * scale) for v in row["rectangle"]], "mass": row["mass"]}
        for row in data["rectangles"]
    ]
    out["n"] = int(data["n"])
    out.pop("scaling_source_digest", None)
    out.pop("scaling_factor", None)
    out["derived_from"] = derived_from or (
        f"published certificate at L={data['L']} scaled by lambda={scale}"
    )
    if canonical:
        return json.dumps(out, sort_keys=True, separators=(",", ":")).encode()
    return json.dumps(out).encode()


def stated_gzip(text: bytes, os_byte: int) -> bytes:
    """`text` as the source states its gzip: level 9, mtime 0, no name, its OS byte."""
    data = bytearray(gzip.compress(text, compresslevel=9, mtime=0))
    data[9] = os_byte
    return bytes(data)


def base_step(base: dict[str, Any]) -> Fraction:
    """The step of the base's own net: the one it declares, else the standard one."""
    net = base.get("proof_net")
    return Fraction(net["step"]) if isinstance(net, dict) else STANDARD_STEP


def base_last(base: dict[str, Any]) -> int:
    """The last index of the base's own net: the one it declares, else the standard one."""
    net = base.get("proof_net")
    return int(net["last"]) if isinstance(net, dict) else STANDARD_LAST


def wall_margin(tangent: Fraction, step: Fraction) -> Fraction:
    """Format M's per-bin wall margin at a node of half-angle tangent `tangent`.

    Lemma D of `sqverify_fast/SOUNDNESS.md`: the centre domain at node `r` is
    `[rho(a_r), L - rho(a_r)]` on each axis, with `a_r = max(0, t_r - D/2)` and
    `rho(a) = (1 + 2a - a²) / (2 (1 + a²))`.
    """
    low = max(Fraction(0), tangent - step / 2)
    return (1 + 2 * low - low * low) / (2 * (1 + low * low))


def shared_node_growth(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """The centre domain's outward growth, in the base's coordinates, at each node the
    certificate's net shares with the base's: `m₀(t) - m(t)/λ`, each margin on its own
    net (`wall_margin`). The other nodes of the certificate's net are new: the base's net
    has no domain there to grow from."""
    scale = Fraction(data["L"]) / Fraction(base["L"])
    step, last = Fraction(data["proof_net"]["step"]), int(data["proof_net"]["last"])
    step0, last0 = base_step(base), base_last(base)
    growth: list[tuple[Fraction, int]] = []
    for index in range(last + 1):
        tangent = index * step
        node = tangent / step0
        if node.denominator == 1 and node <= last0:
            margin0 = wall_margin(tangent, step0)
            growth.append((margin0 - wall_margin(tangent, step) / scale, index))
    least, most = min(growth), max(growth)
    return {
        "shared_nodes": len(growth),
        "new_nodes": last + 1 - len(growth),
        "least": as_text(least[0]),
        "least_approx": float(least[0]),
        "least_at": least[1],
        "most": as_text(most[0]),
        "most_approx": float(most[0]),
        "most_at": most[1],
    }


def dilation_checks(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """That the certificate is the base dilated, row by row, in exact rationals. Every
    boolean here is a condition the audit's status requires."""
    side, base_side = Fraction(data["L"]), Fraction(base["L"])
    scale = side / base_side
    rows, base_rows = rectangles(data), rectangles(base)
    paired = list(zip(rows, base_rows, strict=False))
    base_core = Fraction(base["B"])
    return {
        "lambda": as_text(scale),
        "core_is_lambda_times_base": Fraction(data["B"]) == scale * base_core,
        "same_row_count": len(rows) == len(base_rows),
        "every_rectangle_lambda_times_base": len(rows) == len(base_rows)
        and all(box == [scale * v for v in base_box] for (box, _), (base_box, _) in paired),
        "every_mass_equal": len(rows) == len(base_rows)
        and all(mass == base_mass for (_, mass), (_, base_mass) in paired),
        "total_mass_equal": Fraction(data["total_mass"]) == Fraction(base["total_mass"]),
    }


def dilation_observations(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """What the dilation does not carry, reported and required of nothing: the dilated
    core on the base's own net, the axis domain's growth in the base's coordinates, the
    growth at every node the two nets share and the count of new nodes, and the route's
    ceiling as the step goes to zero."""
    side, base_side = Fraction(data["L"]), Fraction(base["L"])
    scale = side / base_side
    base_core = Fraction(base["B"])
    step = base_step(base)
    base_shrink = scale * base_core * (1 + step)
    return {
        "base_net": base.get("proof_net", "standard"),
        "base_step": as_text(step),
        "dilated_core_on_base_net": as_text(base_shrink),
        "base_net_admits_dilated_core": base_shrink < 1,
        "axis_domain_growth_in_base_coordinates": as_text(Fraction(1, 2) * (1 - 1 / scale)),
        "shared_node_growth_in_base_coordinates": shared_node_growth(data, base),
        "route_ceiling": as_text(base_side / base_core),
        "side_below_ceiling": side < base_side / base_core,
    }


def audit(packet: str) -> dict[str, Any]:
    """The `audit` receipt of one packet's dilated certificate."""
    dilation = DILATIONS[packet]
    path = WEB / packet / dilation.candidate
    base_path = WEB / dilation.base
    text = text_of(path)
    base_text = text_of(base_path)
    data = json.loads(text, parse_float=str)
    base = json.loads(base_text, parse_float=str)
    step = Fraction(data["proof_net"]["step"])
    last = int(data["proof_net"]["last"])
    regenerated = rescaled_text(
        base_text,
        dilation.side,
        step,
        last,
        canonical=dilation.canonical,
        derived_from=dilation.derived_from,
    )
    file = file_checks(data, dilation)
    net = lemma_n0(data)
    if not file["every_row_a_rectangle_of_four_and_a_mass"]:
        message = f"{path}: a row is not a rectangle of four coordinates and a mass"
        raise SystemExit(message)
    scaled = dilation_checks(data, base)
    # The digests are recorded beside the source's stated ones, for a reader and the
    # test; Git holds the retained bytes (OR-16), so the gate is the byte comparison.
    stored = path.read_bytes()
    digests = {
        "candidate": str(path.relative_to(PROJECT.parent)),
        "candidate_sha256": sha256(stored),
        "candidate_sha256_stated": dilation.stored_sha256,
        "text_sha256": sha256(text),
        "text_sha256_stated": dilation.text_sha256,
        "base": str(base_path.relative_to(PROJECT.parent)),
        "base_stored_sha256": sha256(base_path.read_bytes()),
        "base_stored_sha256_stated": dilation.base_stored_sha256 or None,
        "base_text_sha256": sha256(base_text),
        "base_text_sha256_stated": dilation.base_sha256,
        "regenerated_text_sha256": sha256(regenerated),
    }
    scaled["regenerated_text_is_the_certificate"] = regenerated == text
    passes = (
        all(value is True for value in file.values() if isinstance(value, bool))
        and all(value is True for value in net.values() if isinstance(value, bool))
        and all(value is True for value in scaled.values() if isinstance(value, bool))
    )
    observations = dilation_observations(data, base)
    if dilation.gzip_os is not None:
        # The stored gzip's bytes depend on the deflate implementation as well as the
        # text; the text is what the certificate is, so this is an observation.
        observations["regenerated_gzip_is_the_stored_file"] = (
            stated_gzip(regenerated, dilation.gzip_os) == stored
        )
    return {
        "kind": "dilated-measure-audit/v1",
        "packet": packet,
        "certificate": dilation.name,
        "n": dilation.n,
        "L": as_text(dilation.side),
        "digests": digests,
        "file": file,
        "lemma_n0": net,
        "dilation": scaled,
        "observations": observations,
        "status": "PREMISES_HOLD" if passes else "PREMISES_FAIL",
        "decides": (
            "no coverage: the premises, the dilation and the regeneration only; the"
            " observations are reported and required of nothing"
        ),
    }


def direction_lines(text: bytes, where: str) -> tuple[dict[int, str], dict[str, Any] | None]:
    """A `sqverify-fast` stream's direction lines by index, each as its exact text, and its
    summary if it has one. A line that is neither, a direction twice or a second summary is
    refused."""
    lines: dict[int, str] = {}
    summary: dict[str, Any] | None = None
    for number, line in enumerate(text.decode().splitlines(), start=1):
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("kind") == "sqverify-fast-summary/v1":
            if summary is not None:
                message = f"{where}:{number}: a second summary"
                raise SystemExit(message)
            summary = record
        elif "r" in record:
            index = int(record["r"])
            if index in lines:
                message = f"{where}:{number}: direction {index} twice"
                raise SystemExit(message)
            lines[index] = line
        else:
            message = f"{where}:{number}: neither a direction row nor the summary"
            raise SystemExit(message)
    return lines, summary


def read_rows(path: Path) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    """A `sqverify-fast` capture's direction rows by index, and its summary."""
    lines, summary = direction_lines(text_of(path), str(path))
    if summary is None:
        message = f"{path}: no summary"
        raise SystemExit(message)
    return {index: json.loads(line) for index, line in lines.items()}, summary


def untimed(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in TIMINGS}


def compare_receipt(
    ours: dict[int, dict[str, Any]], summary: dict[str, Any], path: Path
) -> dict[str, Any]:
    """One producer receipt against the census capture, direction by direction."""
    theirs, their_summary = read_rows(path)
    differing = {
        str(index): sorted(
            key
            for key in set(untimed(ours.get(index, {}))) | set(untimed(theirs.get(index, {})))
            if untimed(ours.get(index, {})).get(key) != untimed(theirs.get(index, {})).get(key)
        )
        for index in sorted(set(ours) | set(theirs))
        if untimed(ours.get(index, {})) != untimed(theirs.get(index, {}))
    }
    fields = ("status", "nodes", "refused_directions", "directions", "premises", "threshold")
    return {
        "receipt": str(path.relative_to(PROJECT.parent)),
        "receipt_sha256": sha256(path.read_bytes()),
        "directions": len(theirs),
        "same_directions": sorted(theirs) == sorted(ours),
        "identical_directions": sum(
            1
            for index in ours
            if index in theirs and untimed(ours[index]) == untimed(theirs[index])
        ),
        "differing": differing,
        "summary_equal": {
            field: summary.get(field) == their_summary.get(field) for field in fields
        },
        "their_build": their_summary.get("build"),
        "their_threads": their_summary.get("threads"),
        "their_direction_cpu_seconds": their_summary.get("direction_cpu_seconds"),
        "their_status": their_summary.get("status"),
    }


def second_checker(path: Path, directions: int) -> dict[str, Any]:
    """The producer's second checker's verdicts and least bound, read and not run."""
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    indices = sorted(int(row["r"]) for row in rows)
    verdicts = sorted({str(row.get("verdict")) for row in rows})
    # Its rows state each direction's least certified bound in fixed-point units of
    # `scale` (2^42), as `min_bound_units`.
    bounds = [
        (Fraction(int(row["min_bound_units"]), int(row["scale"])), int(row["r"]))
        for row in rows
        if "min_bound_units" in row and "scale" in row
    ]
    least = min(bounds) if bounds else None
    return {
        "replay": str(path.relative_to(PROJECT.parent)),
        "replay_sha256": sha256(path.read_bytes()),
        "rows": len(rows),
        "every_direction_once": indices == list(range(directions)),
        "verdicts": verdicts,
        "nodes": sum(int(row.get("nodes") or 0) for row in rows),
        "least_bound": as_text(least[0]) if least else None,
        "least_bound_approx": float(least[0]) if least else None,
        "least_bound_direction": least[1] if least else None,
        "decides": "nothing here: the producer's output, read; the checker was not run",
    }


def compare(packet: str) -> dict[str, Any]:
    """The `compare` receipt: the census capture against the producer's receipts."""
    dilation = DILATIONS[packet]
    if not dilation.receipts or not dilation.second_checker:
        # With no complete producer receipt every comparison would hold vacuously.
        message = f"{packet}: no complete producer receipt to compare; see `receipts`"
        raise SystemExit(message)
    capture = CENSUS / packet / f"{dilation.name}.jsonl.gz"
    ours, summary = read_rows(capture)
    receipts = [
        compare_receipt(ours, summary, WEB / packet / path) for path in dilation.receipts
    ]
    count = int((summary.get("premises") or {}).get("angle_count") or 0)
    agree = all(
        item["same_directions"]
        and item["identical_directions"] == count
        and all(item["summary_equal"].values())
        for item in receipts
    )
    least = min(
        (row["min_certified_lower_bound"] for row in ours.values()),
        default=None,
    )
    return {
        "kind": "dilated-measure-replay-comparison/v1",
        "packet": packet,
        "certificate": dilation.name,
        "capture": str(capture.relative_to(PROJECT.parent)),
        "capture_sha256": sha256(capture.read_bytes()),
        "directions": count,
        "status": summary.get("status"),
        "nodes": summary.get("nodes"),
        "least_certified_bound": least,
        "build": summary.get("build"),
        "threads": summary.get("threads"),
        "direction_cpu_seconds": summary.get("direction_cpu_seconds"),
        "cpu_ratio_to_receipts": [
            round(
                float(summary["direction_cpu_seconds"])
                / float(item["their_direction_cpu_seconds"]),
                3,
            )
            if summary.get("direction_cpu_seconds") and item["their_direction_cpu_seconds"]
            else None
            for item in receipts
        ],
        "receipts": receipts,
        "second_checker": second_checker(WEB / packet / dilation.second_checker, count),
        "verdict": "EVERY_DIRECTION_AGREES" if agree else "DIRECTIONS_DIFFER",
        "compared": "every field of every direction row but cpu_seconds and seconds",
    }


def native_premises(data: dict[str, Any]) -> dict[str, Any]:
    """The premises a native summary states that this tool recomputes, from the file."""
    net = lemma_n0(data)
    total = sum((mass for _, mass in rectangles(data)), Fraction(0))
    n = int(data["n"])
    return {
        "B": net["B"],
        "D": net["D"],
        "L": as_text(Fraction(data["L"])),
        "angle_count": net["angle_count"],
        "centre_domain": "per-bin",
        "expanded_points": 0,
        "expanded_segments": 0,
        "format": "M",
        "mass_below_n": as_text(n - total),
        "mass_exact": as_text(total),
        "n": n,
        "net_last_tangent": net["net_last_tangent"],
        "net_origin": "proof_net",
        "shrink_bound": net["b_shrink"],
        "source_rectangles": len(data["rectangles"]),
    }


def build_checks(build: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Whether a native build is of reviewed source for declared nets, and the same build
    as the census binary's: the same compiler, profile and target, and the same source."""
    source = str(build.get("source_sha256", ""))
    review = REVIEWED_SOURCES.get(source)
    census_review = REVIEWED_SOURCES.get(str(reference.get("source_sha256", "")))
    return {
        "source_sha256": source,
        "reviewed_source_commit": review.commit if review is not None else None,
        "source_reviewed_for_declared_nets": review is not None and review.declared_nets,
        "same_build_as_census_binary": review is not None
        and review is census_review
        and all(build.get(fact) == reference.get(fact) for fact in BUILD_FACTS),
    }


def finite_bound_at_least_one(row: dict[str, Any]) -> bool:
    bound = row.get("min_certified_lower_bound")
    return isinstance(bound, int | float) and math.isfinite(bound) and bound >= 1


def stream_audit(
    root: Path, source: dict[str, Any], premises: dict[str, Any], reference: dict[str, Any]
) -> tuple[dict[str, Any], dict[int, str], dict[int, dict[str, Any]]]:
    """One native stream against its index entry: its report, its lines and its rows."""
    path = root / source["receipt_file"]
    raw = read_original_gzip_bytes(path)
    text = gzip.decompress(raw)
    lines, summary = direction_lines(text, str(path))
    if summary is None:
        message = f"{path}: no summary"
        raise SystemExit(message)
    rows = {index: json.loads(line) for index, line in lines.items()}
    scope = [int(index) for index in source["scope"]]
    summary_file = json.loads((root / source["summary_file"]).read_text(encoding="utf-8"))
    stated = summary.get("premises") or {}
    build = build_checks(summary.get("build") or {}, reference)
    report = {
        "id": source["id"],
        "receipt": str(path.relative_to(PROJECT.parent)),
        "archive_sha256": sha256(raw),
        "archive_sha256_stated": source.get("archive_sha256"),
        "uncompressed_sha256": sha256(text),
        "uncompressed_sha256_stated": source.get("uncompressed_sha256"),
        "rows": len(rows),
        "rows_are_the_scope": len(set(scope)) == len(scope) and sorted(rows) == sorted(scope),
        "row_count_as_stated": source.get("row_count") == len(rows),
        "summary_file_is_the_stream_summary": summary_file == summary,
        "summary_directions_are_the_rows": summary.get("directions") == len(rows),
        "status": summary.get("status"),
        "status_succeeded": summary.get("status") in ("PARTIAL", "VERIFIED"),
        "refuses_nothing": summary.get("refused_directions") == []
        and all(row.get("verdict") == "verified" for row in rows.values()),
        "no_fault_injected": summary.get("fault_injected_at_box") is None
        and all(row.get("fault_injected_at_box") is None for row in rows.values()),
        "threshold_one": summary.get("threshold") == "1"
        and all(row.get("threshold") == "1" for row in rows.values()),
        "every_bound_finite_and_at_least_one": all(
            finite_bound_at_least_one(row) for row in rows.values()
        ),
        "premises_recomputed": all(stated.get(key) == premises[key] for key in premises),
        "premises_differing": sorted(
            key for key in premises if stated.get(key) != premises[key]
        ),
        "input_sha256": stated.get("input_sha256"),
        "expanded_rectangles": stated.get("expanded_rectangles"),
        "build": summary.get("build"),
        **build,
        "returncode_stated": source.get("returncode"),
        "compacted": "compaction" in source,
        "compaction_original_sha256_stated": (source.get("compaction") or {}).get(
            "original_sha256"
        ),
        "selected_stated": source.get("selected"),
        "nodes": summary.get("nodes"),
        "direction_cpu_seconds": summary.get("direction_cpu_seconds"),
        "threads": summary.get("threads"),
    }
    return report, lines, rows


def read_selection(path: Path) -> dict[int, str]:
    """The selection: for each direction, the stream its line was taken from."""
    reader = csv.reader(io.StringIO(path.read_text(encoding="utf-8")))
    header = next(reader)
    if header != ["r", "source"]:
        message = f"{path}: the header is {header}, not r,source"
        raise SystemExit(message)
    chosen: dict[int, str] = {}
    for number, row in enumerate(reader, start=2):
        index = int(row[0])
        if index in chosen:
            message = f"{path}:{number}: direction {index} twice"
            raise SystemExit(message)
        chosen[index] = row[1]
    return chosen


def capture_report(
    raw: dict[str, Any], x: Fraction, y: Fraction, index: int, stated: Fraction | None
) -> dict[str, Any]:
    """The exact capture of `raw`'s core at one centre and node, by `mixed_exact`, beside
    the producer's stated value, and where the centre lies: the per-bin domain the claim
    is about at that node, and the quadrant `[L/2, U_r]^2` the crate searches."""
    capture = mixed_exact(raw, x, y, index)
    low, high = domain_bounds(raw, index)
    half = Fraction(raw["L"]) / 2
    return {
        "r": index,
        "x": as_text(x),
        "y": as_text(y),
        "capture": as_text(capture),
        "capture_approx": float(capture),
        "capture_below_one": capture < 1,
        "capture_equals_stated": None if stated is None else capture == stated,
        "in_per_bin_domain": all(low <= value <= high for value in (x, y)),
        "in_searched_quadrant": all(half <= value <= high for value in (x, y)),
    }


def mutant_checks(
    data: dict[str, Any], mutant: dict[str, Any], factor: Fraction
) -> dict[str, Any]:
    """That the mutant is the certificate with every mass times `factor` and nothing else
    but its `derived_from`, a label no checker reads, which is recorded."""
    rows, mutant_rows = rectangles(data), rectangles(mutant)
    same = len(rows) == len(mutant_rows)
    pairs = list(zip(rows, mutant_rows, strict=False))
    labels = ("rectangles", "total_mass", "derived_from")
    others = {key for key in set(data) | set(mutant) if key not in labels}
    return {
        "factor": as_text(factor),
        "derived_from": mutant.get("derived_from"),
        "same_row_count": same,
        "geometry_unchanged": same and all(box == box2 for (box, _), (box2, _) in pairs),
        "every_mass_times_factor": same
        and all(mass2 == factor * mass for (_, mass), (_, mass2) in pairs),
        "total_mass_times_factor": Fraction(mutant["total_mass"])
        == factor * Fraction(data["total_mass"]),
        "other_keys_unchanged": all(data.get(key) == mutant.get(key) for key in others),
    }


def control_audit(
    archive: ReceiptArchive, packet: Path, data: dict[str, Any], reference: dict[str, Any]
) -> dict[str, Any]:
    """The producer's mass-scaled control: the mutant, its native refusals, and its exact
    witnesses recomputed apart from the crate."""
    mutant = json.loads(
        gzip.decompress(read_original_gzip_bytes(packet / archive.mutant)), parse_float=str
    )
    path = packet / archive.mutant_receipts
    lines, summary = direction_lines(path.read_bytes(), str(path))
    if summary is None:
        message = f"{path}: no summary"
        raise SystemExit(message)
    rows = {index: json.loads(line) for index, line in lines.items()}
    stated = summary.get("premises") or {}
    premises = native_premises(mutant)
    witnesses: list[dict[str, Any]] = []
    for index, row in sorted(rows.items()):
        if row.get("method") == "axis-vertex-sweep":
            x, y = (Fraction(value) for value in row["argmin"])
            report = capture_report(mutant, x, y, index, None)
            report["kind"] = "axis vertex sweep's least vertex"
            bound = row.get("min_certified_lower_bound")
            report["certified_bound"] = bound
            report["bound_at_most_capture"] = isinstance(bound, float) and Fraction(
                bound
            ) <= Fraction(report["capture"])
        else:
            witness = row.get("witness") or {}
            # The crate's pose is binary64; its exact capture is at that double's value.
            x, y = (Fraction(float(value)) for value in witness["exact_pose"])
            report = capture_report(mutant, x, y, index, Fraction(witness["exact_coverage"]))
            report["kind"] = "native counterexample candidate's exact pose"
            report["exact_below_threshold_stated"] = witness.get("exact_below_threshold")
        witnesses.append(report)
    exact = json.loads((packet / archive.witness).read_text(encoding="utf-8"))
    counter = exact["exact_counterexample"]
    index = int(counter["r"])
    x, y = Fraction(counter["x"]), Fraction(counter["y"])
    producer = capture_report(mutant, x, y, index, Fraction(counter["capture"]))
    producer["kind"] = "the producer's exact rational witness"
    original = mixed_exact(data, x, y, index)
    producer["original_capture"] = as_text(original)
    producer["original_capture_approx"] = float(original)
    producer["original_capture_at_least_one"] = original >= 1
    producer["mutant_capture_is_factor_times_original"] = (
        Fraction(producer["capture"]) == archive.mutant_factor * original
    )
    witnesses.append(producer)
    checks = mutant_checks(data, mutant, archive.mutant_factor)
    build = build_checks(summary.get("build") or {}, reference)
    report = {
        "mutant": str((packet / archive.mutant).relative_to(PROJECT.parent)),
        "mutant_sha256": sha256(read_original_gzip_bytes(packet / archive.mutant)),
        **checks,
        "receipts": str(path.relative_to(PROJECT.parent)),
        "directions": sorted(rows),
        "status": summary.get("status"),
        "every_direction_refused_on_coverage": summary.get("status") == "REFUSED"
        and summary.get("refused_directions") == sorted(rows)
        and all(row.get("verdict") in REFUSALS for row in rows.values()),
        "premises_recomputed": all(stated.get(key) == premises[key] for key in premises),
        "input_sha256": stated.get("input_sha256"),
        **build,
        "witnesses": witnesses,
        "every_witness_holds": all(
            item["capture_below_one"]
            and item["in_per_bin_domain"]
            and item["capture_equals_stated"] is not False
            and item.get("bound_at_most_capture", True)
            for item in witnesses
        ),
        "scope": "the directions the producer ran the mutant at, not the whole net",
    }
    report["passes"] = all(
        report[key] is True
        for key in (
            "same_row_count",
            "geometry_unchanged",
            "every_mass_times_factor",
            "total_mass_times_factor",
            "other_keys_unchanged",
            "every_direction_refused_on_coverage",
            "premises_recomputed",
            "source_reviewed_for_declared_nets",
            "every_witness_holds",
        )
    ) and all(item.get("original_capture_at_least_one", True) for item in witnesses)
    return report


#: The stream checks every native stream must pass.
STREAM_CHECKS = (
    "rows_are_the_scope",
    "row_count_as_stated",
    "summary_file_is_the_stream_summary",
    "summary_directions_are_the_rows",
    "status_succeeded",
    "refuses_nothing",
    "no_fault_injected",
    "threshold_one",
    "every_bound_finite_and_at_least_one",
    "premises_recomputed",
    "source_reviewed_for_declared_nets",
    "same_build_as_census_binary",
)


def receipts(packet: str) -> dict[str, Any]:
    """The `receipts` receipt: a producer's native receipt archive, audited."""
    dilation = DILATIONS[packet]
    archive = dilation.archive
    if archive is None:
        message = f"{packet}: no receipt archive"
        raise SystemExit(message)
    folder = WEB / packet
    root = folder / archive.root
    data = json.loads(text_of(folder / dilation.candidate), parse_float=str)
    premises = native_premises(data)
    count = int(premises["angle_count"])
    census = json.loads((CENSUS / "census.json").read_text(encoding="utf-8"))
    reference = census["cases"][REFERENCE_ROW]["build"]
    index = json.loads(read_retained_bytes(folder / archive.index))
    streams: list[dict[str, Any]] = []
    stream_lines: dict[str, dict[int, str]] = {}
    stream_rows: dict[str, dict[int, dict[str, Any]]] = {}
    for source in index["sources"]:
        report, lines, rows = stream_audit(root, source, premises, reference)
        streams.append(report)
        stream_lines[source["id"]] = lines
        stream_rows[source["id"]] = rows
    merged_path = folder / archive.merged
    merged_raw = read_original_gzip_bytes(merged_path)
    merged_text = gzip.decompress(merged_raw)
    merged, merged_summary = direction_lines(merged_text, str(merged_path))
    merged_rows = {key: json.loads(line) for key, line in merged.items()}
    chosen = read_selection(folder / archive.selection)
    equal = [
        key
        for key, line in merged.items()
        if chosen.get(key) in stream_lines and stream_lines[chosen[key]].get(key) == line
    ]
    least = min(
        (
            (Fraction(row["min_certified_lower_bound"]), key)
            for key, row in merged_rows.items()
            if finite_bound_at_least_one(row)
        ),
        default=None,
    )
    selected = {item["id"]: 0 for item in streams}
    for source_id in chosen.values():
        selected[source_id] = selected.get(source_id, 0) + 1
    # The nodes of the selected rows: each row's own where it records them, and a
    # compacted stream's summary total where every one of its rows is selected.
    known = sum(
        int(stream_rows[chosen[key]][key].get("nodes") or 0)
        for key in merged
        if chosen.get(key) in stream_rows and "nodes" in stream_rows[chosen[key]].get(key, {})
    )
    compacted = [
        item
        for item in streams
        if item["compacted"] and selected.get(item["id"]) == item["rows"]
    ]
    unknown = sum(
        1
        for key in merged
        if chosen.get(key) in stream_rows
        and "nodes" not in stream_rows[chosen[key]].get(key, {})
        and stream_rows[chosen[key]][key].get("method") != "axis-vertex-sweep"
        and chosen[key] not in {item["id"] for item in compacted}
    )
    control = control_audit(archive, folder, data, reference)
    crate = crate_source_sha256(folder / archive.crate)
    crate_review = REVIEWED_SOURCES.get(crate)
    coverage = {
        "merged": str(merged_path.relative_to(PROJECT.parent)),
        "merged_sha256": sha256(merged_raw),
        "merged_sha256_stated": index.get("merged_gzip_sha256"),
        "merged_text_sha256": sha256(merged_text),
        "merged_text_sha256_stated": index.get("merged_jsonl_sha256"),
        "directions": len(merged),
        "net_directions": count,
        "no_summary_line": merged_summary is None,
        "every_index_once": sorted(merged) == list(range(count)),
        "every_row_verified": all(
            row.get("verdict") == "verified" for row in merged_rows.values()
        ),
        "threshold_one": all(row.get("threshold") == "1" for row in merged_rows.values()),
        "every_bound_finite_and_at_least_one": all(
            finite_bound_at_least_one(row) for row in merged_rows.values()
        ),
        "least_certified_bound": float(least[0]) if least else None,
        "least_bound_direction": least[1] if least else None,
        "methods": sorted({str(row.get("method")) for row in merged_rows.values()}),
        "selection_is_every_index_once": sorted(chosen) == list(range(count)),
        "selection_names_only_streams": set(chosen.values()) <= set(stream_lines),
        "selected_lines_equal_their_source": len(equal),
        "every_selected_line_is_its_source_line": len(equal) == count == len(merged),
        "selected_by_stream": selected,
        "selected_as_stated": all(
            selected.get(item["id"]) == item["selected_stated"] for item in streams
        ),
        "every_stream_row_verified": all(
            row.get("verdict") == "verified"
            for rows in stream_rows.values()
            for row in rows.values()
        ),
    }
    nodes = {
        "selected_rows_with_nodes": known,
        "fully_selected_compacted_streams": [item["id"] for item in compacted],
        "compacted_stream_nodes": sum(int(item["nodes"] or 0) for item in compacted),
        "selected_nodes": known + sum(int(item["nodes"] or 0) for item in compacted),
        "selected_oblique_rows_of_unknown_nodes": unknown,
        "all_stream_nodes": sum(int(item["nodes"] or 0) for item in streams),
        "all_stream_direction_cpu_seconds": round(
            sum(float(item["direction_cpu_seconds"] or 0) for item in streams), 3
        ),
        "all_stream_rows": sum(item["rows"] for item in streams),
    }
    crate_report = {
        "copy": str((folder / archive.crate).relative_to(PROJECT.parent)),
        "copy_source_sha256": crate,
        "copy_reviewed_source_commit": crate_review.commit if crate_review else None,
        "copy_is_reviewed_source_for_declared_nets": crate_review is not None
        and crate_review.declared_nets,
        "receipts_name_the_same_reviewed_source": all(
            REVIEWED_SOURCES.get(item["source_sha256"]) is crate_review for item in streams
        ),
    }
    passes = (
        all(item[key] is True for item in streams for key in STREAM_CHECKS)
        and all(
            coverage[key] is True
            for key in (
                "no_summary_line",
                "every_index_once",
                "every_row_verified",
                "threshold_one",
                "every_bound_finite_and_at_least_one",
                "selection_is_every_index_once",
                "selection_names_only_streams",
                "every_selected_line_is_its_source_line",
                "selected_as_stated",
                "every_stream_row_verified",
            )
        )
        and crate_report["copy_is_reviewed_source_for_declared_nets"] is True
        and crate_report["receipts_name_the_same_reviewed_source"] is True
        and control["passes"] is True
    )
    return {
        "kind": "dilated-measure-receipt-archive-audit/v1",
        "packet": packet,
        "certificate": dilation.name,
        "candidate_sha256": sha256((folder / dilation.candidate).read_bytes()),
        "premises": premises,
        "reference_build": {"row": REFERENCE_ROW, **reference},
        "crate": crate_report,
        "streams": streams,
        "coverage": coverage,
        "nodes": nodes,
        "control": control,
        "status": "RECEIPTS_HOLD" if passes else "RECEIPTS_FAIL",
        "decides": (
            "no coverage here: the producer's retained native receipts are read, held to"
            " their scopes, the certificate's premises and a reviewed build, and the"
            " control's witnesses recomputed exactly; no direction was run"
        ),
    }


RECEIPTS = {
    "audit": "dilation-audit.json",
    "compare": "replay-comparison.json",
    "receipts": "native-receipt-audit.json",
}


def receipt_path(packet: str, command: str) -> Path:
    return WEB / packet / "receipts" / RECEIPTS[command]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("command", choices=sorted(RECEIPTS))
    parser.add_argument("packet", choices=sorted(DILATIONS))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="write the packet's receipt")
    group.add_argument("--check", action="store_true", help="fail unless it is unchanged")
    args = parser.parse_args(argv)
    commands = {"audit": audit, "compare": compare, "receipts": receipts}
    receipt = commands[args.command](args.packet)
    path = receipt_path(args.packet, args.command)
    text = retained_json.dumps(receipt)
    passed = {
        "audit": lambda: receipt["status"] == "PREMISES_HOLD",
        "compare": lambda: receipt["verdict"] == "EVERY_DIRECTION_AGREES",
        "receipts": lambda: receipt["status"] == "RECEIPTS_HOLD",
    }[args.command]()
    if args.check:
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored != json.loads(text):
            sys.stderr.write(f"{path}: differs from the recomputed receipt\n")
            return 1
        if not passed:
            sys.stderr.write(f"{path}: unchanged, and it does not pass\n")
            return 1
        sys.stdout.write(f"{path.relative_to(PROJECT)}: unchanged, and it passes\n")
        return 0
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
