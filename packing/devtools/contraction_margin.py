"""How much of a certificate's side is padding: its exact uniform-contraction margin.

A certificate made with padding, such as a dilation or this repository's
``packing-witness promote --strategy robust-rational``, keeps every pair of squares apart
by about the padding. Scaling every centre by a factor ``lambda`` about the origin, with
every rotation fixed, scales each pair's projection on its four fixed edge normals by
``lambda`` and leaves its separating threshold ``T`` alone. Two unit squares at
orientations ``(a_i, b_i)`` and ``(a_j, b_j)`` have ``T = (1 + |a_i a_j + b_i b_j| +
|a_i b_j - b_i a_j|) / 2`` on each of those normals, so the pair stays interior-disjoint
iff ``lambda >= T / M``, ``M`` the largest ``|u . d|`` over the normals ``u`` and the
centre difference ``d``. The least feasible factor is therefore ``lambda* = max T / M``
over all pairs, an exact rational, at which the binding pair touches. The contracted
packing is translated into the corner and boxed: ``L' = max(Lx, Ly)``, each extent read
with every square's axis half-width ``(|a| + |b|) / 2``.

The **margin** is the side less ``L'``: what uniform contraction alone takes off the
certificate, with no square re-solved. A later certificate of the same packing whose side
lies at or above ``L'`` gains no more than the earlier one's padding. This is the
measurement the review of 31 October 2026 made at 130, 293 and 307 (think-ruu2's RV-3)
with a retained program of its own,
``cases/register_candidates/think-ruu2-2026-10-31/review/code/contract.py``; this module
is that measurement once (OR-1), and it reproduces that program's contracted side at 130
exactly. The owner's question it serves, whether such a re-certification is a new result,
is open (think-ruu2 RV-3, think-ikku); the module decides nothing about it.

A certificate that is no packing at its own side is refused before anything is
measured. Every square's exact axis extent must lie in its box, and ``lambda*`` must not
exceed 1, which on the four edge normals is exact for a pair of squares. Both maintained
exact routes (`upper_bound_sharp_controls.decide`) then decide the certificate as given,
and it is refused unless both accept. They decide the contracted packing too, so ``L'``
is a proved bound in its own right. ``--no-routes`` skips both route decisions and keeps
the exact wall and pair checks.

**Inputs** are `devtools.measure_identity`'s specs, ``[LABEL=]KIND:TARGET``: ``packet:NAME``
(an import packet's admitted certificate, held to its custody) or ``FORMAT:PATH`` with a
format of `devtools.upper_bound_reports.ADAPTERS`. ``--against`` names a later certificate
of the same count, held to the same exact wall and pair checks, whose gain over the first
is compared with the margin.

**Through an L step.** A certificate built by one L step, such as #938's and #939's at
199, has margin 0, since its grid squares touch; its padding is its base's. The base is
read with ``l-base:packet:NAME`` (`devtools.measure_identity.read_l_base`), at the base's
count. Contracting the base and writing the L on it gives a packing one larger, so the
base's margin is the margin the certificate carries through the step::

    python -m devtools.contraction_margin --n 172 \\
        'T-284=l-base:packet:ozden-s199-upper-bound-2026-11-09' \\
        --against 'T-285=l-base:packet:de-winter-s199-upper-bound-2026-11-09'

From ``packing/``, with the project interpreter::

    python -m devtools.contraction_margin --n 299 \\
        'T-277=packet:ozden-s299-upper-bound-2026-11-09' \\
        --against 'T-280=packet:yim-certificates-2026-11-09' \\
        --out resources/web/yim-certificates-2026-11-09/measure/contraction-n299.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_exact_certificates as legacy
from devtools import measure_identity as identity
from devtools import retained_data
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

FORMAT = "contraction-margin-v1"
#: The witness profile the routes are given; the contracted packing is no import's.
PROFILE = {
    "witness_prefix": "W-contraction-margin-n",
    "claim_limitations": (
        "A certificate's own packing contracted uniformly about the origin to first "
        "contact and boxed; a measurement of its padding, not a reported result."
    ),
}


class ContractionError(ValueError):
    """An input this module refuses."""


@dataclass(frozen=True)
class Read:
    """One certificate as read, with where it came from."""

    label: str
    source: dict[str, Any]
    certificate: legacy.Certificate


def read_certificate(spec: str, n: int) -> Read:
    """The certificate a `devtools.measure_identity` spec names at ``n``, exactly."""
    try:
        label, kind, target = identity.split_spec(spec)
    except identity.MeasureError as error:
        raise ContractionError(str(error)) from error
    plain = spec if label is None else spec.partition("=")[2]
    try:
        if kind == identity.PACKET:
            facts = reports.read_facts(reports.packet_path(target), {n})
            if n not in facts:
                raise ContractionError(f"{plain}: the packet declares no certificate at {n}")
            certificate = facts[n]
            source: dict[str, Any] = {"input": identity.PACKET, "packet": target}
        elif kind == identity.L_BASE:
            certificate, source = identity.read_l_base(target, n)
        elif kind in reports.ADAPTERS:
            path = Path(target)
            raw = retained_data.read_retained_bytes(path, limit=reports.MAX_SOURCE_BYTES)
            certificate = reports.parse_certificate(raw, n, kind)
            source = {"input": kind, **_where(path), "sha256": hashlib.sha256(raw).hexdigest()}
        else:
            raise ContractionError(f"{plain}: unknown kind {kind!r}")
    except (reports.ReportError, identity.MeasureError, OSError, ValueError) as error:
        if isinstance(error, ContractionError):
            raise
        raise ContractionError(f"{plain}: {error}") from error
    if certificate.n != n or len(certificate.poses) != n:
        raise ContractionError(f"{plain}: not a certificate of {n} squares")
    return Read(label or plain, source, certificate)


def _where(path: Path) -> dict[str, Any]:
    """The path repository-relative where it lies in the repository; else its name alone."""
    try:
        return {"path": path.resolve().relative_to(reports.REPO.resolve()).as_posix()}
    except ValueError:
        return {"path": path.name, "outside_repository": True}


def _basis(pose: legacy.Pose) -> tuple[Fraction, Fraction]:
    """``(cos theta, sin theta)`` from the half-angle tangent ``t``."""
    denominator = 1 + pose.t * pose.t
    return (1 - pose.t * pose.t) / denominator, 2 * pose.t / denominator


def _half_width(pose: legacy.Pose) -> Fraction:
    """Half the exact axis extent of a unit square at this pose, along x and along y."""
    a, b = _basis(pose)
    return (abs(a) + abs(b)) / 2


def check_walls(certificate: legacy.Certificate) -> None:
    """Refuse a certificate with a square outside its own box, read exactly."""
    side = certificate.side
    for index, pose in enumerate(certificate.poses, start=1):
        half = _half_width(pose)
        if min(pose.x, pose.y) - half < 0 or max(pose.x, pose.y) + half > side:
            raise ContractionError(
                f"no packing at its own side (square {index} outside the box)"
            )


def lambda_star(certificate: legacy.Certificate) -> tuple[Fraction, tuple[int, int]]:
    """The least factor that keeps every pair interior-disjoint, and the pair it binds."""
    rows = [(pose.x, pose.y, *_basis(pose)) for pose in certificate.poses]
    best, where = Fraction(0), (0, 0)
    for i, (xi, yi, ai, bi) in enumerate(rows):
        for j in range(i + 1, len(rows)):
            xj, yj, aj, bj = rows[j]
            dx, dy = xj - xi, yj - yi
            threshold = (1 + abs(ai * aj + bi * bj) + abs(ai * bj - bi * aj)) / 2
            reach = max(
                abs(ai * dx + bi * dy),
                abs(ai * dy - bi * dx),
                abs(aj * dx + bj * dy),
                abs(aj * dy - bj * dx),
            )
            if reach == 0:
                raise ContractionError(f"squares {i + 1} and {j + 1} share a centre")
            ratio = threshold / reach
            if ratio > best:
                best, where = ratio, (i + 1, j + 1)
    return best, where


def contract(certificate: legacy.Certificate, factor: Fraction) -> legacy.Certificate:
    """The packing scaled by ``factor`` about the origin, moved into the corner and boxed."""
    halves = [_half_width(pose) for pose in certificate.poses]
    xs = [factor * pose.x for pose in certificate.poses]
    ys = [factor * pose.y for pose in certificate.poses]
    left = min(x - h for x, h in zip(xs, halves, strict=True))
    bottom = min(y - h for y, h in zip(ys, halves, strict=True))
    width = max(x + h for x, h in zip(xs, halves, strict=True)) - left
    height = max(y + h for y, h in zip(ys, halves, strict=True)) - bottom
    poses = tuple(
        legacy.Pose(x - left, y - bottom, pose.t)
        for x, y, pose in zip(xs, ys, certificate.poses, strict=True)
    )
    return legacy.Certificate(certificate.n, max(width, height), poses)


def _float(value: Fraction) -> str:
    return f"{float(value):.6e}"


def _packing(read: Read) -> tuple[Fraction, tuple[int, int]]:
    """``lambda_star`` of a certificate whose every wall and pair holds exactly, or refused."""
    try:
        check_walls(read.certificate)
    except ContractionError as error:
        raise ContractionError(f"{read.label}: {error}") from error
    factor, pair = lambda_star(read.certificate)
    if factor > 1:
        raise ContractionError(
            f"{read.label}: no packing at its own side (pair {pair} needs factor {factor})"
        )
    return factor, pair


def margin(read: Read, *, routes: bool = True, against: Read | None = None) -> dict[str, Any]:
    """The receipt: the factor, the contracted side, the margin, and the routes' verdicts."""
    started = time.process_time()
    certificate = read.certificate
    factor, pair = _packing(read)
    if against is not None:
        if against.certificate.n != certificate.n:
            raise ContractionError("--against names a certificate of another count")
        _packing(against)
    given = sharp.decide(certificate, PROFILE) if routes else None
    if given is not None and not all(item["passed"] for item in given.values()):
        refusing = sorted(route for route, item in given.items() if not item["passed"])
        raise ContractionError(f"{read.label}: no packing at its own side ({refusing} refuse)")
    contracted = contract(certificate, factor)
    record: dict[str, Any] = {
        "format": FORMAT,
        "n": certificate.n,
        "certificate": {"label": read.label, **read.source},
        "side": legacy.literal(certificate.side),
        "lambda_star": legacy.literal(factor),
        "one_minus_lambda_star": _float(1 - factor),
        "binding_pair": list(pair),
        "contracted_side": legacy.literal(contracted.side),
        "margin": legacy.literal(certificate.side - contracted.side),
        "margin_float": _float(certificate.side - contracted.side),
    }
    if given is not None:
        record["certificate_routes"] = given
        verdicts = sharp.decide(contracted, PROFILE)
        record["routes"] = verdicts
        record["routes_accept"] = all(item["passed"] for item in verdicts.values())
    if against is not None:
        later = against.certificate
        gain = certificate.side - later.side
        record["against"] = {
            "certificate": {"label": against.label, **against.source},
            "side": legacy.literal(later.side),
            "gain": legacy.literal(gain),
            "gain_float": _float(gain),
            "gain_over_margin": f"{float(gain / (certificate.side - contracted.side)):.4f}"
            if certificate.side != contracted.side
            else None,
            "within_margin": later.side >= contracted.side,
        }
    record["cpu_seconds"] = round(time.process_time() - started, 2)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="How much of a certificate's side is padding: its contraction margin."
    )
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("certificate", help="[LABEL=]KIND:TARGET, as devtools.measure_identity")
    parser.add_argument("--against", help="a later certificate of the same count")
    parser.add_argument("--no-routes", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        record = margin(
            read_certificate(args.certificate, args.n),
            routes=not args.no_routes,
            against=read_certificate(args.against, args.n) if args.against else None,
        )
    except ContractionError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    text = json.dumps(record, indent=1, ensure_ascii=False) + "\n"
    if args.out is None:
        sys.stdout.write(text)
    else:
        with atomic_output_file(args.out) as temporary:
            Path(temporary).write_text(text, encoding="utf-8")
    return 0 if record.get("routes_accept", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
