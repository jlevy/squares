"""Exact target-blind proof records for the UnitSquare refusal-localization lane."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import BinaryIO, Literal

from cases.unitsquare_precision.refusal.verify import verify_proof

type Axis = Literal["cx", "cy", "t"]
type LeafStatus = Literal["retained", "rejected"]
type SourceModel = Literal["declared:svg-literal", "nearest-6", "truncate-6"]
type RunnerOutcome = Literal["compatible", "refused"]
type RunnerReason = Literal[
    "localized-compatible",
    "pose-compatibility-refusal",
    "serialization-refusal",
    "affine-transform-refusal",
    "unresolved",
]

MODEL_ORDER: tuple[SourceModel, ...] = (
    "declared:svg-literal",
    "nearest-6",
    "truncate-6",
)
EXP051_RESULT_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-051-h-053-n68-refusal-localization.json"
)
EXP051_PARENT_URL = "https://kingbird.myphotos.cc/packing/square-68.svg"
EXP051_PARENT_SHA256 = "558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d"

DIHEDRAL_CORRESPONDENCES = (
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
    (0, 3, 2, 1),
    (3, 2, 1, 0),
    (2, 1, 0, 3),
    (1, 0, 3, 2),
)


class ProofFormatError(ValueError):
    """Reject a malformed exact proof record before it reaches target data."""


class RunnerGuardError(ValueError):
    """Refuse a runner action at a bounded provenance or publication guard."""


@dataclass(frozen=True, slots=True)
class RunnerAuthorization:
    """One coordinator-opened W6 phase, bound to its exact clock."""

    session_id: str
    phase_started_at: str
    phase_deadline_at: str

    def to_document(self) -> dict[str, str]:
        return {
            "session_id": self.session_id,
            "phase_started_at": self.phase_started_at,
            "phase_deadline_at": self.phase_deadline_at,
        }


EXP051_AUTHORIZATION = RunnerAuthorization(
    session_id="session-069",
    phase_started_at="2026-09-01T13:46:55Z",
    phase_deadline_at="2026-09-01T14:11:55Z",
)


@dataclass(frozen=True, slots=True)
class RunnerContract:
    """Immutable source, result and authorization facts for one runner."""

    experiment_id: str
    session_id: str
    result_path: str
    authorization: RunnerAuthorization
    parent_url: str
    parent_sha256: str


EXP051_CONTRACT = RunnerContract(
    experiment_id="exp-051",
    session_id="session-069",
    result_path=EXP051_RESULT_PATH,
    authorization=EXP051_AUTHORIZATION,
    parent_url=EXP051_PARENT_URL,
    parent_sha256=EXP051_PARENT_SHA256,
)


@dataclass(frozen=True, slots=True)
class RunnerModelEvaluation:
    """One isolated model's sanitized proof or typed refusal."""

    model: str
    outcome: RunnerOutcome
    reason: RunnerReason
    proof: dict[str, object] | None = None
    expected_binding: dict[str, object] | None = None
    source_cells_sha256: str | None = None


type StructuralScan = Callable[[memoryview], Sequence[Mapping[str, object]]]
type RunnerModelEvaluator = Callable[[memoryview, str], RunnerModelEvaluation]
type ModelFactory = Callable[[str], RunnerModelEvaluator]
type ParentOpener = Callable[[str], BinaryIO]
type Publisher = Callable[[Path, bytes], None]


def _rational(value: str | int | Fraction) -> Fraction:
    if isinstance(value, bool):
        raise ProofFormatError("booleans are not rational values")
    try:
        return value if isinstance(value, Fraction) else Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ProofFormatError("invalid rational value") from error


def _text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True, slots=True)
class RationalInterval:
    """A closed interval with exact rational endpoints."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ProofFormatError("interval lower endpoint exceeds upper endpoint")

    @classmethod
    def from_strings(cls, lower: str, upper: str) -> RationalInterval:
        return cls(_rational(lower), _rational(upper))

    @classmethod
    def point(cls, value: str | int | Fraction) -> RationalInterval:
        rational = _rational(value)
        return cls(rational, rational)

    def contains(self, value: Fraction) -> bool:
        return self.lower <= value <= self.upper

    def add(self, other: RationalInterval) -> RationalInterval:
        return RationalInterval(self.lower + other.lower, self.upper + other.upper)

    def scale(self, coefficient: Fraction) -> RationalInterval:
        values = (self.lower * coefficient, self.upper * coefficient)
        return RationalInterval(min(values), max(values))

    def to_document(self) -> list[str]:
        return [_text(self.lower), _text(self.upper)]


@dataclass(frozen=True, slots=True)
class ExactPose:
    """One exact unit-square pose in rational half-angle coordinates."""

    cx: Fraction
    cy: Fraction
    t: Fraction

    @classmethod
    def from_strings(cls, cx: str, cy: str, t: str) -> ExactPose:
        return cls(_rational(cx), _rational(cy), _rational(t))

    def to_document(self) -> dict[str, str]:
        return {"cx": _text(self.cx), "cy": _text(self.cy), "t": _text(self.t)}


@dataclass(frozen=True, slots=True)
class SourceBinding:
    """The source, polygon, model, transform and container facts a proof is about."""

    model: SourceModel
    source_sha256: str
    polygon_sha256: str
    transform: RationalAffine
    container: tuple[Fraction, Fraction, Fraction, Fraction, Fraction]

    @classmethod
    def synthetic(cls) -> SourceBinding:
        return cls(
            model="declared:svg-literal",
            source_sha256="1" * 64,
            polygon_sha256="2" * 64,
            transform=RationalAffine.identity(),
            container=(Fraction(0), Fraction(0), Fraction(4), Fraction(4), Fraction(4)),
        )

    def to_document(self) -> dict[str, object]:
        x0, y0, width, height, side = self.container
        return {
            "model": self.model,
            "source_sha256": self.source_sha256,
            "polygon_sha256": self.polygon_sha256,
            "transform": self.transform.to_document(),
            "container": {
                "x0": _text(x0),
                "y0": _text(y0),
                "width": _text(width),
                "height": _text(height),
                "side": _text(side),
                "normalization": "x=L*(X-x0)/W;y=L*(y0+H-Y)/H",
            },
        }


@dataclass(frozen=True, slots=True)
class PoseBox:
    """A closed rational box in ``(cx, cy, t)`` coordinates."""

    cx: RationalInterval
    cy: RationalInterval
    t: RationalInterval

    @classmethod
    def from_strings(
        cls,
        cx: tuple[str, str],
        cy: tuple[str, str],
        t: tuple[str, str],
    ) -> PoseBox:
        return cls(
            RationalInterval.from_strings(*cx),
            RationalInterval.from_strings(*cy),
            RationalInterval.from_strings(*t),
        )

    def interval(self, axis: Axis) -> RationalInterval:
        return getattr(self, axis)

    def replace(self, axis: Axis, interval: RationalInterval) -> PoseBox:
        return PoseBox(
            cx=interval if axis == "cx" else self.cx,
            cy=interval if axis == "cy" else self.cy,
            t=interval if axis == "t" else self.t,
        )

    def split(self, axis: Axis, cut: str | Fraction) -> tuple[PoseBox, PoseBox]:
        interval = self.interval(axis)
        rational_cut = _rational(cut)
        if not interval.lower < rational_cut < interval.upper:
            raise ProofFormatError("cover split must be strictly inside its interval")
        return (
            self.replace(axis, RationalInterval(interval.lower, rational_cut)),
            self.replace(axis, RationalInterval(rational_cut, interval.upper)),
        )

    def to_document(self) -> dict[str, list[str]]:
        return {
            "cx": self.cx.to_document(),
            "cy": self.cy.to_document(),
            "t": self.t.to_document(),
        }


@dataclass(frozen=True, slots=True)
class CoverLeaf:
    """A terminal retained or rejected box in a complete cover tree."""

    region: PoseBox
    status: LeafStatus
    reason: str
    corner_images: tuple[tuple[RationalInterval, RationalInterval], ...] | None = None
    rejection: dict[str, object] | None = None

    def __post_init__(self) -> None:
        if self.status not in ("retained", "rejected"):
            raise ProofFormatError("unknown cover-leaf status")
        if not self.reason:
            raise ProofFormatError("cover leaf requires a bounded reason")

    def to_document(self) -> dict[str, object]:
        document: dict[str, object] = {
            "kind": "leaf",
            "region": self.region.to_document(),
            "status": self.status,
            "reason": self.reason,
        }
        if self.corner_images is not None:
            document["corner_images"] = [
                {"x": x.to_document(), "y": y.to_document()} for x, y in self.corner_images
            ]
        if self.rejection is not None:
            document["rejection"] = self.rejection
        return document


@dataclass(frozen=True, slots=True)
class CoverSplit:
    """A locally gap-free binary partition of a pose box."""

    region: PoseBox
    axis: Axis
    cut: str | Fraction
    lower: CoverLeaf | CoverSplit
    upper: CoverLeaf | CoverSplit

    def __post_init__(self) -> None:
        if self.axis not in ("cx", "cy", "t"):
            raise ProofFormatError("unknown cover split axis")
        rational_cut = _rational(self.cut)
        expected_lower, expected_upper = self.region.split(self.axis, rational_cut)
        if self.lower.region != expected_lower or self.upper.region != expected_upper:
            raise ProofFormatError("cover children do not form the declared partition")
        object.__setattr__(self, "cut", rational_cut)

    def to_document(self) -> dict[str, object]:
        if not isinstance(self.cut, Fraction):
            raise ProofFormatError("cover split cut was not normalized")
        return {
            "kind": "split",
            "region": self.region.to_document(),
            "axis": self.axis,
            "cut": _text(self.cut),
            "lower": self.lower.to_document(),
            "upper": self.upper.to_document(),
        }


@dataclass(frozen=True, slots=True)
class RationalAffine:
    """An exact SVG-style affine map acting on homogeneous column vectors."""

    a: Fraction
    b: Fraction
    c: Fraction
    d: Fraction
    e: Fraction
    f: Fraction

    @classmethod
    def identity(cls) -> RationalAffine:
        return cls(Fraction(1), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0))

    @classmethod
    def translation(cls, x: str, y: str) -> RationalAffine:
        return cls(
            Fraction(1), Fraction(0), Fraction(0), Fraction(1), _rational(x), _rational(y)
        )

    @classmethod
    def scale(cls, x: str, y: str) -> RationalAffine:
        return cls(
            _rational(x), Fraction(0), Fraction(0), _rational(y), Fraction(0), Fraction(0)
        )

    def compose(self, local: RationalAffine) -> RationalAffine:
        """Return ``self * local`` under the frozen transform convention."""

        return RationalAffine(
            a=self.a * local.a + self.c * local.b,
            b=self.b * local.a + self.d * local.b,
            c=self.a * local.c + self.c * local.d,
            d=self.b * local.c + self.d * local.d,
            e=self.a * local.e + self.c * local.f + self.e,
            f=self.b * local.e + self.d * local.f + self.f,
        )

    def apply(self, x: str | Fraction, y: str | Fraction) -> tuple[str, str]:
        rational_x = _rational(x)
        rational_y = _rational(y)
        return (
            _text(self.a * rational_x + self.c * rational_y + self.e),
            _text(self.b * rational_x + self.d * rational_y + self.f),
        )

    def to_document(self) -> list[str]:
        return [_text(value) for value in (self.a, self.b, self.c, self.d, self.e, self.f)]


def _corner_values(pose: ExactPose) -> tuple[tuple[Fraction, Fraction], ...]:
    denominator = 1 + pose.t * pose.t
    cosine = (1 - pose.t * pose.t) / denominator
    sine = 2 * pose.t / denominator
    offsets = (
        (Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(-1, 2), Fraction(1, 2)),
    )
    return tuple(
        (
            pose.cx + cosine * u - sine * v,
            pose.cy + sine * u + cosine * v,
        )
        for u, v in offsets
    )


def unit_corners(pose: ExactPose) -> tuple[tuple[str, str], ...]:
    """Return the four exact unit-square corners in canonical cyclic order."""

    return tuple((_text(x), _text(y)) for x, y in _corner_values(pose))


@dataclass(frozen=True, slots=True)
class ExactWitness:
    """An exact pose and one declared source-cell correspondence."""

    binding: SourceBinding
    pose: ExactPose
    source_cells: tuple[tuple[RationalInterval, RationalInterval], ...]
    correspondence: tuple[int, int, int, int]

    def to_document(self) -> dict[str, object]:
        denominator = 1 + self.pose.t * self.pose.t
        cosine = (1 - self.pose.t * self.pose.t) / denominator
        sine = 2 * self.pose.t / denominator
        return {
            "format": "UnitSquareExactWitness/v1",
            "binding": self.binding.to_document(),
            "pose": self.pose.to_document(),
            "rotation": {"c": _text(cosine), "s": _text(sine)},
            "correspondence": list(self.correspondence),
            "corners": [list(point) for point in unit_corners(self.pose)],
            "source_cells": [
                {"x": x.to_document(), "y": y.to_document()} for x, y in self.source_cells
            ],
            "source_cells_sha256": source_cells_sha256(self.source_cells),
        }


def build_exact_witness(
    binding: SourceBinding,
    pose: ExactPose,
    source_cells: tuple[tuple[RationalInterval, RationalInterval], ...],
    correspondence: tuple[int, int, int, int] = (0, 1, 2, 3),
) -> ExactWitness:
    """Build a witness only when all exact corners lie in their closed source cells."""

    if len(source_cells) != 4 or correspondence not in DIHEDRAL_CORRESPONDENCES:
        raise ProofFormatError("witness requires four cells and one dihedral correspondence")
    if not Fraction(-1, 2) <= pose.t <= Fraction(1, 2):
        raise ProofFormatError("witness half-angle lies outside the frozen quotient")
    corners = _corner_values(pose)
    for source_index, corner_index in enumerate(correspondence):
        x_cell, y_cell = source_cells[source_index]
        x, y = corners[corner_index]
        if not x_cell.contains(x) or not y_cell.contains(y):
            raise ProofFormatError("exact witness corner lies outside its source cell")
    return ExactWitness(binding, pose, source_cells, correspondence)


def source_cells_document(
    source_cells: tuple[tuple[RationalInterval, RationalInterval], ...],
) -> list[dict[str, list[str]]]:
    return [{"x": x.to_document(), "y": y.to_document()} for x, y in source_cells]


def source_cells_sha256(
    source_cells: tuple[tuple[RationalInterval, RationalInterval], ...],
) -> str:
    return hashlib.sha256(
        json.dumps(
            source_cells_document(source_cells), sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class ExactWallSigns:
    """Exact inward wall clearances for one point pose."""

    left: Fraction
    right: Fraction
    bottom: Fraction
    top: Fraction

    @property
    def minimum(self) -> str:
        return _text(min(self.left, self.right, self.bottom, self.top))

    @property
    def classification(self) -> Literal["positive", "zero", "negative"]:
        minimum = min(self.left, self.right, self.bottom, self.top)
        if minimum > 0:
            return "positive"
        if minimum < 0:
            return "negative"
        return "zero"

    def to_document(self) -> dict[str, str]:
        return {
            "left": _text(self.left),
            "right": _text(self.right),
            "bottom": _text(self.bottom),
            "top": _text(self.top),
            "minimum": self.minimum,
            "classification": self.classification,
        }


def exact_wall_signs(pose: ExactPose, container_side: str | Fraction) -> ExactWallSigns:
    """Evaluate exact inward wall signs for a point pose."""

    side = _rational(container_side)
    if side <= 0:
        raise ProofFormatError("container side must be positive")
    corners = _corner_values(pose)
    xs = tuple(x for x, _ in corners)
    ys = tuple(y for _, y in corners)
    return ExactWallSigns(min(xs), side - max(xs), min(ys), side - max(ys))


def _rotation_intervals(t: RationalInterval) -> tuple[RationalInterval, RationalInterval]:
    if t.lower < -1 or t.upper > 1:
        raise ProofFormatError("half-angle interval lies outside the monotone proof range")
    absolute_max = max(abs(t.lower), abs(t.upper))
    absolute_min = Fraction(0) if t.contains(Fraction(0)) else min(abs(t.lower), abs(t.upper))

    def cosine(value: Fraction) -> Fraction:
        return (1 - value * value) / (1 + value * value)

    def sine(value: Fraction) -> Fraction:
        return 2 * value / (1 + value * value)

    return (
        RationalInterval(cosine(absolute_max), cosine(absolute_min)),
        RationalInterval(sine(t.lower), sine(t.upper)),
    )


def outward_corner_intervals(
    region: PoseBox,
) -> tuple[tuple[RationalInterval, RationalInterval], ...]:
    """Return rational outer intervals for every corner over a pose box."""

    cosine, sine = _rotation_intervals(region.t)
    offsets = (
        (Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(-1, 2), Fraction(1, 2)),
    )
    return tuple(
        (
            region.cx.add(cosine.scale(u)).add(sine.scale(-v)),
            region.cy.add(sine.scale(u)).add(cosine.scale(v)),
        )
        for u, v in offsets
    )


def retained_leaf(region: PoseBox) -> CoverLeaf:
    return CoverLeaf(region, "retained", "outward-image", outward_corner_intervals(region))


def rejected_leaf(
    region: PoseBox,
    source_cells: tuple[tuple[RationalInterval, RationalInterval], ...],
    correspondence: tuple[int, int, int, int],
) -> CoverLeaf:
    """Reject a region only with one exact source-cell disjointness witness."""

    images = outward_corner_intervals(region)
    for source_index, corner_index in enumerate(correspondence):
        for coordinate, image, cell in (
            ("x", images[corner_index][0], source_cells[source_index][0]),
            ("y", images[corner_index][1], source_cells[source_index][1]),
        ):
            if image.upper < cell.lower:
                return CoverLeaf(
                    region,
                    "rejected",
                    "outside-source-cell",
                    rejection={
                        "source_index": source_index,
                        "corner_index": corner_index,
                        "coordinate": coordinate,
                        "relation": "below",
                    },
                )
            if image.lower > cell.upper:
                return CoverLeaf(
                    region,
                    "rejected",
                    "outside-source-cell",
                    rejection={
                        "source_index": source_index,
                        "corner_index": corner_index,
                        "coordinate": coordinate,
                        "relation": "above",
                    },
                )
    raise ProofFormatError("region has no checked source-cell rejection")


def _retained_regions(cover: CoverLeaf | CoverSplit) -> tuple[PoseBox, ...]:
    if isinstance(cover, CoverLeaf):
        return (cover.region,) if cover.status == "retained" else ()
    return _retained_regions(cover.lower) + _retained_regions(cover.upper)


def outward_wall_signs(cover: CoverLeaf | CoverSplit, side: Fraction) -> dict[str, object]:
    retained = _retained_regions(cover)
    if not retained:
        raise ProofFormatError("cover must retain at least one pose box")
    images = tuple(image for region in retained for image in outward_corner_intervals(region))
    xs = tuple(x for x, _ in images)
    ys = tuple(y for _, y in images)
    walls = {
        "left": RationalInterval(min(x.lower for x in xs), min(x.upper for x in xs)),
        "right": RationalInterval(
            side - max(x.upper for x in xs), side - max(x.lower for x in xs)
        ),
        "bottom": RationalInterval(min(y.lower for y in ys), min(y.upper for y in ys)),
        "top": RationalInterval(
            side - max(y.upper for y in ys), side - max(y.lower for y in ys)
        ),
    }
    minimum = RationalInterval(
        min(value.lower for value in walls.values()),
        min(value.upper for value in walls.values()),
    )
    if minimum.lower >= 0:
        decision = "nonnegative"
    elif minimum.upper < 0:
        decision = "negative"
    else:
        decision = "undecided"
    return {
        "walls": {name: value.to_document() for name, value in walls.items()},
        "minimum": minimum.to_document(),
        "decision": decision,
    }


def outward_pair_signs(first: PoseBox, second: PoseBox) -> dict[str, object]:
    """Return exact SAT gap intervals for two rational point-pose boxes."""

    poses = []
    for label, region in (("first", first), ("second", second)):
        if any(
            interval.lower != interval.upper for interval in (region.cx, region.cy, region.t)
        ):
            raise ProofFormatError(f"{label} pair control must be a point-pose box")
        poses.append(ExactPose(region.cx.lower, region.cy.lower, region.t.lower))

    rotations = []
    for pose in poses:
        denominator = 1 + pose.t * pose.t
        rotations.append(((1 - pose.t * pose.t) / denominator, 2 * pose.t / denominator))
    axes = (
        rotations[0],
        (-rotations[0][1], rotations[0][0]),
        rotations[1],
        (-rotations[1][1], rotations[1][0]),
    )
    delta = poses[1].cx - poses[0].cx, poses[1].cy - poses[0].cy
    gaps = []
    for nx, ny in axes:
        distance = abs(delta[0] * nx + delta[1] * ny)
        widths = []
        for cosine, sine in rotations:
            along_u = abs(nx * cosine + ny * sine)
            along_v = abs(-nx * sine + ny * cosine)
            widths.append((along_u + along_v) / 2)
        gaps.append(distance - widths[0] - widths[1])
    maximum = max(gaps)
    decision = "separated" if maximum > 0 else "overlap" if maximum < 0 else "possible-contact"
    return {
        "first": first.to_document(),
        "second": second.to_document(),
        "axis_gaps": [[_text(gap), _text(gap)] for gap in gaps],
        "maximum": [_text(maximum), _text(maximum)],
        "decision": decision,
    }


def synthetic_pair_controls() -> list[dict[str, object]]:
    first = PoseBox.from_strings(("1", "1"), ("1", "1"), ("0", "0"))
    controls = []
    for label, center_x in (("separated", "3"), ("tangent", "2"), ("overlap", "3/2")):
        second = PoseBox.from_strings((center_x, center_x), ("1", "1"), ("0", "0"))
        controls.append({"label": label, "signs": outward_pair_signs(first, second)})
    return controls


def build_proof_receipt(
    witness: ExactWitness,
    cover: CoverLeaf | CoverSplit,
) -> dict[str, object]:
    """Build a source-bound proof envelope with a replayable content digest."""

    side = witness.binding.container[4]
    proof: dict[str, object] = {
        "format": "UnitSquarePoseProof/v1",
        "binding": witness.binding.to_document(),
        "witness": witness.to_document(),
        "cover": cover.to_document(),
        "wall_signs": outward_wall_signs(cover, side),
        "pair_controls": synthetic_pair_controls(),
    }
    return {
        "proof": proof,
        "proof_sha256": hashlib.sha256(canonical_proof_bytes(proof)).hexdigest(),
    }


def _synthetic_receipt_for_binding(binding: SourceBinding) -> dict[str, object]:
    pose = ExactPose.from_strings("2", "2", "1/2")
    cells = synthetic_source_cells()
    witness = build_exact_witness(binding, pose, cells)
    root = PoseBox.from_strings(("8/5", "31/10"), ("8/5", "12/5"), ("-1/2", "1/2"))
    lower, upper = root.split("cx", "3")
    cover = CoverSplit(
        root,
        "cx",
        "3",
        retained_leaf(lower),
        rejected_leaf(upper, cells, witness.correspondence),
    )
    return build_proof_receipt(witness, cover)


def synthetic_receipt() -> dict[str, object]:
    """Return the fixed target-blind known-answer proof used by both CLI modes."""

    return _synthetic_receipt_for_binding(SourceBinding.synthetic())


def synthetic_source_cells() -> tuple[tuple[RationalInterval, RationalInterval], ...]:
    """Return source cells declared independently of the synthetic witness."""

    return (
        (
            RationalInterval.from_strings("2", "11/5"),
            RationalInterval.from_strings("6/5", "7/5"),
        ),
        (
            RationalInterval.from_strings("13/5", "14/5"),
            RationalInterval.from_strings("2", "11/5"),
        ),
        (
            RationalInterval.from_strings("9/5", "2"),
            RationalInterval.from_strings("13/5", "14/5"),
        ),
        (
            RationalInterval.from_strings("6/5", "7/5"),
            RationalInterval.from_strings("9/5", "2"),
        ),
    )


def canonical_proof_bytes(document: dict[str, object]) -> bytes:
    """Serialize a sanitized exact proof document deterministically."""

    return json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def canonical_runner_bytes(document: dict[str, object]) -> bytes:
    """Serialize a sanitized runner receipt without local or transient state."""

    try:
        return json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode()
    except (TypeError, ValueError) as error:
        raise RunnerGuardError("runner receipt is not canonical JSON") from error


def _check_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise RunnerGuardError(f"{label} must be 64 lowercase hexadecimal digits")
    return value


def _checked_record_path(contract: RunnerContract, record_path: str) -> str:
    if record_path != contract.result_path:
        raise RunnerGuardError(f"result path must be exactly {contract.result_path}")
    path = Path(record_path)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != record_path:
        raise RunnerGuardError("result path must be canonical and repository-relative")
    return record_path


def _scan_rows(
    rows: Sequence[Mapping[str, object]],
) -> tuple[tuple[str, str], ...]:
    if not rows:
        raise RunnerGuardError("structural scan found no square polygons")
    scanned: list[tuple[str, str]] = []
    identifiers: set[str] = set()
    for row in rows:
        if set(row) != {"stable_id", "vertex_count", "polygon_sha256"}:
            raise RunnerGuardError("structural scan row has an undeclared field")
        stable_id = row.get("stable_id")
        if not isinstance(stable_id, str) or not stable_id:
            raise RunnerGuardError("structural scan requires a nonempty stable id")
        try:
            stable_id.encode("utf-8")
        except UnicodeEncodeError as error:
            raise RunnerGuardError("stable id is not valid UTF-8") from error
        if stable_id in identifiers:
            raise RunnerGuardError(f"duplicate square id: {stable_id}")
        identifiers.add(stable_id)
        if row.get("vertex_count") != 4:
            raise RunnerGuardError(f"square {stable_id} does not have exactly four vertices")
        polygon_sha256 = _check_sha256(row.get("polygon_sha256"), "polygon SHA-256")
        scanned.append((stable_id, polygon_sha256))
    return tuple(sorted(scanned, key=lambda row: row[0].encode("utf-8")))


_FORBIDDEN_RETAINED_KEYS = {
    "buffer",
    "child",
    "gain",
    "header",
    "headers",
    "palette",
    "path",
    "raw",
    "response",
    "temp",
    "temporary",
    "xml",
}


def _check_sanitized(value: object) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise RunnerGuardError("retained proof has a non-string key")
            tokens = set(re.findall(r"[a-z0-9]+", key.lower()))
            forbidden = tokens & _FORBIDDEN_RETAINED_KEYS
            if forbidden:
                raise RunnerGuardError(f"forbidden retained key: {min(forbidden)}")
            _check_sanitized(item)
        return
    if isinstance(value, list):
        for item in value:
            _check_sanitized(item)
        return
    if isinstance(value, (bytes, bytearray, memoryview)):
        raise RunnerGuardError("retained proof contains raw bytes")
    if isinstance(value, str) and ("<svg" in value.lower() or "<?xml" in value.lower()):
        raise RunnerGuardError("retained proof contains source markup")
    if value is not None and not isinstance(value, (str, int, bool)):
        raise RunnerGuardError("retained proof contains a noncanonical value")


def _model_document(
    evaluation: RunnerModelEvaluation,
    *,
    expected_model: SourceModel,
    source_sha256: str,
    polygon_sha256: str,
) -> dict[str, object]:
    if evaluation.model != expected_model:
        raise RunnerGuardError("model evaluations are not in the frozen model order")
    if evaluation.outcome == "refused":
        if evaluation.reason == "localized-compatible" or any(
            value is not None
            for value in (
                evaluation.proof,
                evaluation.expected_binding,
                evaluation.source_cells_sha256,
            )
        ):
            raise RunnerGuardError("refused model carries undeclared proof state")
        return {
            "model": expected_model,
            "outcome": evaluation.outcome,
            "reason": evaluation.reason,
        }
    if evaluation.outcome != "compatible" or evaluation.reason != "localized-compatible":
        raise RunnerGuardError("model evaluation has an invalid outcome")
    if (
        evaluation.proof is None
        or evaluation.expected_binding is None
        or evaluation.source_cells_sha256 is None
    ):
        raise RunnerGuardError("compatible model lacks its proof verification inputs")
    expected_binding = evaluation.expected_binding
    if (
        expected_binding.get("model") != expected_model
        or expected_binding.get("source_sha256") != source_sha256
        or expected_binding.get("polygon_sha256") != polygon_sha256
    ):
        raise RunnerGuardError("proof binding does not match the selected parent polygon")
    _check_sha256(evaluation.source_cells_sha256, "source-cell SHA-256")
    _check_sanitized(evaluation.proof)
    errors = verify_proof(
        evaluation.proof,
        expected_binding,
        evaluation.source_cells_sha256,
    )
    if errors:
        raise RunnerGuardError("independent proof verification failed: " + errors[0])
    return {
        "model": expected_model,
        "outcome": evaluation.outcome,
        "reason": evaluation.reason,
        "proof": evaluation.proof,
    }


def _evaluate_parent(
    *,
    contract: RunnerContract,
    opener: ParentOpener,
    structural_scan: StructuralScan,
    model_factory: ModelFactory,
) -> dict[str, object]:
    _check_sha256(contract.parent_sha256, "expected parent SHA-256")
    response = opener(contract.parent_url)
    payload: bytearray | None = None
    try:
        raw = response.read()
        if not isinstance(raw, bytes):
            raise RunnerGuardError("parent response did not return bytes")
        payload = bytearray(raw)
        del raw
        observed_sha256 = hashlib.sha256(payload).hexdigest()
        if observed_sha256 != contract.parent_sha256:
            raise RunnerGuardError(
                "parent digest mismatch before structural scan: "
                f"expected {contract.parent_sha256}, observed {observed_sha256}"
            )
        view = memoryview(payload)
        rows = _scan_rows(structural_scan(view))
        selected_id, polygon_sha256 = rows[0]
        model_documents: list[dict[str, object]] = []
        evaluators: list[RunnerModelEvaluator] = []
        for model in MODEL_ORDER:
            evaluator = model_factory(model)
            if any(evaluator is existing for existing in evaluators):
                raise RunnerGuardError("model evaluator instances are not isolated")
            evaluators.append(evaluator)
            evaluation = evaluator(view, selected_id)
            model_documents.append(
                _model_document(
                    evaluation,
                    expected_model=model,
                    source_sha256=observed_sha256,
                    polygon_sha256=polygon_sha256,
                )
            )
        document: dict[str, object] = {
            "format": "UnitSquareRefusalRunner/v1",
            "experiment_id": contract.experiment_id,
            "session_id": contract.session_id,
            "authorization": contract.authorization.to_document(),
            "source": {
                "url": contract.parent_url,
                "expected_sha256": contract.parent_sha256,
                "observed_sha256": observed_sha256,
            },
            "selection": {
                "stable_id": selected_id,
                "polygon_sha256": polygon_sha256,
            },
            "model_order": list(MODEL_ORDER),
            "models": model_documents,
            "retention": "sanitized-provenance-and-proof-only",
            "blindness": "parent-only-input-interface",
        }
        canonical_runner_bytes(document)
        return document
    finally:
        if payload is not None:
            payload[:] = b"\0" * len(payload)
        response.close()
        if hasattr(response, "closed") and not response.closed:
            raise RunnerGuardError("parent response cleanup failed")


def atomic_publish_new(path: Path, content: bytes) -> None:
    """Flush a sibling temporary file and atomically publish without overwriting."""

    if path.exists():
        raise RunnerGuardError(f"existing result refuses publication: {path.name}")
    if not path.parent.is_dir():
        raise RunnerGuardError("result parent directory does not exist")
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise RunnerGuardError(
                f"existing result refuses publication: {path.name}"
            ) from error
    finally:
        temporary.unlink(missing_ok=True)


def run_authorized_runner(
    *,
    contract: RunnerContract,
    authorization: RunnerAuthorization,
    record_path: str,
    output_root: Path,
    opener: ParentOpener,
    structural_scan: StructuralScan,
    model_factory: ModelFactory,
    publisher: Publisher = atomic_publish_new,
) -> dict[str, object]:
    """Run one digest-bound parent through injected, child-blind dependencies."""

    checked_path = _checked_record_path(contract, record_path)
    if (
        authorization != contract.authorization
        or authorization.session_id != contract.session_id
    ):
        raise RunnerGuardError("W6 authorization does not match the frozen session phase")
    target = output_root / checked_path
    if target.exists():
        raise RunnerGuardError(f"existing result refuses publication: {target.name}")
    document = _evaluate_parent(
        contract=contract,
        opener=opener,
        structural_scan=structural_scan,
        model_factory=model_factory,
    )
    publisher(target, canonical_runner_bytes(document) + b"\n")
    return document


def run_exp051_runner(
    *,
    record_path: str,
    authorization: RunnerAuthorization,
    output_root: Path,
    opener: ParentOpener,
    structural_scan: StructuralScan,
    model_factory: ModelFactory,
    publisher: Publisher = atomic_publish_new,
) -> dict[str, object]:
    """Bind the generic injected runner to exp-051's immutable production facts."""

    return run_authorized_runner(
        contract=EXP051_CONTRACT,
        authorization=authorization,
        record_path=record_path,
        output_root=output_root,
        opener=opener,
        structural_scan=structural_scan,
        model_factory=model_factory,
        publisher=publisher,
    )


def _runner_selftest() -> dict[str, object]:
    payload = b"synthetic target-blind parent stream"
    source_sha256 = hashlib.sha256(payload).hexdigest()
    polygon_sha256 = "a" * 64
    authorization = EXP051_AUTHORIZATION
    contract = RunnerContract(
        experiment_id="exp-051",
        session_id="session-069",
        result_path=EXP051_RESULT_PATH,
        authorization=authorization,
        parent_url="https://example.invalid/synthetic-parent.svg",
        parent_sha256=source_sha256,
    )
    binding = SourceBinding(
        "declared:svg-literal",
        source_sha256,
        polygon_sha256,
        RationalAffine.identity(),
        (Fraction(0), Fraction(0), Fraction(4), Fraction(4), Fraction(4)),
    )
    proof = _synthetic_receipt_for_binding(binding)

    def scan(_payload: memoryview) -> Sequence[Mapping[str, object]]:
        return (
            {"stable_id": "square-b", "vertex_count": 4, "polygon_sha256": "b" * 64},
            {
                "stable_id": "square-a",
                "vertex_count": 4,
                "polygon_sha256": polygon_sha256,
            },
        )

    def factory(model: str) -> RunnerModelEvaluator:
        class Evaluator:
            def __call__(self, _payload: memoryview, _stable_id: str) -> RunnerModelEvaluation:
                if model == "declared:svg-literal":
                    return RunnerModelEvaluation(
                        model=model,
                        outcome="compatible",
                        reason="localized-compatible",
                        proof=proof,
                        expected_binding=binding.to_document(),
                        source_cells_sha256=source_cells_sha256(synthetic_source_cells()),
                    )
                return RunnerModelEvaluation(
                    model=model,
                    outcome="refused",
                    reason="pose-compatibility-refusal",
                )

        return Evaluator()

    with tempfile.TemporaryDirectory(prefix="unit-square-runner-selftest-") as root:
        output_root = Path(root)
        target = output_root / contract.result_path
        target.parent.mkdir(parents=True)
        document = run_authorized_runner(
            contract=contract,
            authorization=authorization,
            record_path=contract.result_path,
            output_root=output_root,
            opener=lambda _url: io.BytesIO(payload),
            structural_scan=scan,
            model_factory=factory,
        )
        retained = target.read_bytes()
        if retained != canonical_runner_bytes(document) + b"\n":
            raise RunnerGuardError("runner selftest publication mismatch")
    return {
        "format": "UnitSquareRefusalRunnerSelftest/v1",
        "runner_sha256": hashlib.sha256(canonical_runner_bytes(document)).hexdigest(),
        "guards": [
            "authorization-and-result-binding",
            "digest-before-scan",
            "four-vertex-unique-id-selection",
            "isolated-model-order",
            "independent-verification-before-publication",
            "sanitized-retention",
            "response-buffer-temporary-cleanup",
            "atomic-new-result-publication",
        ],
    }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true")
    mode.add_argument("--runner-selftest", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.runner_selftest:
        try:
            document = _runner_selftest()
        except (ProofFormatError, RunnerGuardError) as error:
            print(f"runner selftest failed: {error}", file=sys.stderr)
            return 2
        sys.stdout.buffer.write(canonical_runner_bytes(document) + b"\n")
        return 0
    receipt = synthetic_receipt()
    errors = verify_proof(
        receipt,
        SourceBinding.synthetic().to_document(),
        source_cells_sha256(synthetic_source_cells()),
    )
    if errors:
        print("proof selftest failed: " + "; ".join(errors), file=sys.stderr)
        return 2
    sys.stdout.buffer.write(canonical_proof_bytes(receipt) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
