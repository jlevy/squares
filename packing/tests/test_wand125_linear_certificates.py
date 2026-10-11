"""Controls for the linear certificates of wand125/square-packing-bounds.

`devtools.audit_wand125_linear` audits and replays the two of jlevy/squares#294,
``mixed_n101_L1028`` and ``mixed_n83_L935``, and its later ``mixed_n82_L932``, pinned in a
packet of its own: measures of point masses, uniform segments and uniform rectangles
decided by ``unified_linear_verify.cpp``. Five families of check stand
between a certificate and a recorded replay, and each is held here to its positive case
and to mutated controls it must refuse:

- **the retained files**: the exact premises (digests, schema, counts, core side,
  containment, mass, D4 invariance, digest rule, net, checker, records, source audit);
- **the bundle**: its whole shape, its files' binding to the packet, the checker copies,
  the per-angle candidates and the summary, before any of its code runs;
- **the inputs**: each angle's exported input against the exact candidate, independently;
- **the replay receipts**: the mixed range driver's rows and merge, for linear records;
- **the controls**: the retained stage-4 receipt, its mutations regenerated here and their
  witness evaluated exactly.

No checker is run here. Coverage is the source checker's, replayed by ``linear-replay``.
"""

from __future__ import annotations

import dataclasses
import hashlib
import itertools
import json
import math
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_wand125_linear as linear
from devtools import audit_wand125_point_and_mixed as mixed
from devtools.audit_wand125_rectangles import CONTROL_FACTOR, net_rotation

NAMES = ("n101", "n83")
PACKET = linear.LINEAR_PACKET
N82 = linear.LINEAR["n82"]
CHECKER = (linear.LINEAR_CODE / "unified_linear_verify.cpp").read_bytes()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _changed(
    certificate: linear.LinearCertificate, name: str, change: Callable[[Any], None]
) -> tuple[dict[str, bytes], dict[Path, str]]:
    """The retained files with one JSON file changed, and a digest list repinned to it.

    A control built this way passes the pin check, so what refuses it is the content.
    """
    files = dict(linear.linear_retained(certificate))
    data = json.loads(files[name])
    change(data)
    files[name] = json.dumps(data).encode()
    tree = dict(mixed.read_subtree_manifest(certificate.subtree))
    tree[certificate.directory / name] = _sha256(files[name])
    return files, tree


def _refused(
    certificate: linear.LinearCertificate, name: str, change: Callable[[Any], None], match: str
) -> None:
    files, tree = _changed(certificate, name, change)
    with pytest.raises(ValueError, match=match):
        linear.linear_certificate(certificate, files, tree)


# --------------------------------------------------------------------------- retained files


@pytest.fixture(scope="module")
def audits() -> dict[str, dict[str, Any]]:
    return {name: linear.linear_certificate(linear.LINEAR[name]) for name in NAMES}


@pytest.mark.parametrize("name", NAMES)
def test_each_certificate_has_its_stated_exact_premises(
    audits: dict[str, dict[str, Any]], name: str
) -> None:
    certificate = linear.LINEAR[name]
    facts = audits[name]
    stated = {
        "rectangle": certificate.rectangles,
        "point": certificate.points,
        "segment": certificate.segments,
    }
    assert facts["orbits"] == stated
    assert facts["images"] == {kind: 8 * count for kind, count in stated.items()}
    assert Fraction(facts["total_mass"]) == certificate.n - Fraction(1, 100000)
    assert facts["candidate_digest"] == certificate.candidate_digest
    assert facts["checker_sha256"] == linear.LINEAR_CHECKER_SHA256
    assert facts["d4_invariant"]
    assert facts["code_files"] == 13
    assert Fraction(facts["centre_half_width_least"]) > 0
    assert facts["comparison"]["side_exceeds_green"]
    assert facts["comparison"]["side_exceeds_nagamochi"]


def test_the_node_counts_are_the_certificates(audits: dict[str, dict[str, Any]]) -> None:
    assert audits["n101"]["nodes"] == 55222823
    assert (audits["n101"]["most_nodes"], audits["n101"]["most_nodes_at"]) == (2072307, 0)
    assert audits["n83"]["nodes"] == 137090913


def test_the_n83_comparison_value_is_below_greens_bound(
    audits: dict[str, dict[str, Any]],
) -> None:
    """Like n = 84 and 85's, n = 83's audit compares with 92667/10000, below Green's value."""
    facts = audits["n83"]
    assert facts["source_audit"]["compared_with"] == "92667/10000"
    assert not facts["comparison"]["source_value_exceeds_green"]
    assert facts["comparison"]["green"] == "Theorem 9, k=9, from n = 82"


def test_the_n101_comparison_value_encloses_greens_bound_from_above(
    audits: dict[str, dict[str, Any]],
) -> None:
    facts = audits["n101"]
    assert facts["comparison"]["green"] == "Theorem 9, k=10, from n = 101"
    assert facts["comparison"]["source_value_exceeds_green"]


def test_the_packet_audit_recomputes_to_its_receipt() -> None:
    receipt = PACKET / "receipts/linear-audit.json"
    expected = json.dumps(linear.linear_audit(), indent=2, default=str) + "\n"
    assert receipt.read_text(encoding="utf-8") == expected


def test_the_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(PACKET, acquire_source.REPO) == []


# --------------------------------------------------------------------------- n = 82


@pytest.fixture(scope="module")
def n82() -> dict[str, Any]:
    return linear.linear_certificate(N82)


def test_n82_is_pinned_in_its_own_packet_at_the_later_revision() -> None:
    assert N82.packet == linear.N82_PACKET != PACKET
    assert N82.revision == linear.N82_REVISION
    assert {c.name for c in linear.LINEAR.values() if c.packet == PACKET} == set(NAMES)
    assert acquire_source.check(linear.N82_PACKET, acquire_source.REPO) == []
    receipt = linear.N82_PACKET / "receipts/linear-audit.json"
    expected = json.dumps(linear.linear_audit(linear.N82_PACKET), indent=2, default=str) + "\n"
    assert receipt.read_text(encoding="utf-8") == expected


def test_n82_has_its_stated_exact_premises(n82: dict[str, Any]) -> None:
    assert n82["orbits"] == {"rectangle": 774, "point": 86, "segment": 222}
    assert n82["images"] == {"rectangle": 6192, "point": 688, "segment": 1776}
    assert Fraction(n82["total_mass"]) == 82 - Fraction(1, 100000)
    assert n82["code_files"] == 13
    assert n82["checker_sha256"] == linear.LINEAR_CHECKER_SHA256
    assert n82["nodes"] == 153579479
    assert (n82["most_nodes"], n82["most_nodes_at"]) == (1178525, 199)
    assert n82["centre_half_width_least_at"] == linear.LAST
    assert n82["comparison"]["side_exceeds_green"]
    assert n82["comparison"]["side_exceeds_nagamochi"]


def test_n82_compares_with_the_upper_end_of_its_own_green_interval(n82: dict[str, Any]) -> None:
    """Its audit names ``green_upper``, a true upper bound, unlike n = 83's rounded value."""
    source = n82["source_audit"]
    assert source["compared_field"] == "green_upper"
    assert n82["comparison"]["source_value_exceeds_green"]
    assert Fraction(source["improvement_lower"]) == Fraction(233, 25) - Fraction(
        source["compared_with"]
    )
    n83 = linear.linear_certificate(linear.LINEAR["n83"])
    assert "compared_field" not in n83["source_audit"]


def test_an_n82_green_upper_off_its_interval_is_refused() -> None:
    def change(audit: dict[str, Any]) -> None:
        upper = Fraction(audit["green_upper"]) + Fraction(1, 10**6)
        audit["green_upper"] = str(upper)
        audit["improvement_lower"] = str(Fraction(233, 25) - upper)

    _refused(N82, "completion-audit.json", change, "interval")


def test_an_n82_audit_naming_another_bundle_is_refused() -> None:
    def change(audit: dict[str, Any]) -> None:
        audit["bundle"] = "n83-L9.35-proof-bundle.tar.gz"

    _refused(N82, "completion-audit.json", change, "another measure")


def test_n82s_support_is_n83s_scaled_by_the_ratio_of_the_sides() -> None:
    """Same primitives in the same order, every coordinate times 932/935; masses re-solved."""
    ours = json.loads(linear.linear_retained(N82)["candidate.json"])["primitives"]
    theirs = json.loads(linear.linear_retained(linear.LINEAR["n83"])["candidate.json"])[
        "primitives"
    ]
    scale = Fraction(932, 935)
    assert len(ours) == len(theirs) == 1082
    for a, b in zip(ours, theirs, strict=True):
        assert a["kind"] == b["kind"]
        scaled = [scale * Fraction(v) for v in b["geometry"]]
        assert [Fraction(v) for v in a["geometry"]] == scaled
    assert not any(a["mass"] == b["mass"] for a, b in zip(ours, theirs, strict=True))


def test_the_n82_pre_replay_receipt_is_bound_to_the_pin() -> None:
    record = json.loads((N82.receipts / "fetch.json").read_text())
    assert record["status"] == "BUNDLE_READY"
    assert (record["tarball"]["sha256"], record["tarball"]["bytes"]) == mixed.tarball_pin(N82)
    assert record["bindings"]["files"] == 810
    assert record["bindings"]["checker_copies"] == 202
    assert record["preconditions"]["candidate_digest"] == N82.candidate_digest
    assert record["inputs"]["status"] == "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"
    assert record["inputs"]["inputs"] == linear.LAST + 1


# --------------------------------------------------------------------------- n = 122

N122 = linear.LINEAR["n122"]


def test_n122_is_registered_from_its_own_packet_with_its_exact_premises() -> None:
    """mixed_n122_L1126 of wand125/square-packing, whose packet retains the five small
    files and the pins the route reads (`devtools.retain_wand125_release`)."""
    assert N122.packet == linear.N122_PACKET
    assert N122.revision == linear.N122_REVISION
    assert N122.directory == Path("certificates/mixed_n122_L1126")
    assert N122.tarball == "n122-L11.26-proof-bundle.tar.gz"
    audit = linear.linear_audit(linear.N122_PACKET)
    facts = audit["certificates"]["n122"]
    assert set(audit["certificates"]) == {"n122"}
    assert facts["orbits"] == {"rectangle": 3, "point": 502, "segment": 1268}
    assert facts["images"] == {"rectangle": 24, "point": 4016, "segment": 10144}
    assert facts["total_mass"] == "12199999/100000"
    assert facts["candidate_digest"] == N122.candidate_digest
    assert facts["nodes"] == 73694735
    assert (facts["most_nodes"], facts["most_nodes_at"]) == (2218683, 0)
    assert facts["code_files"] == 13
    assert facts["comparison"]["side_exceeds_green"]
    assert facts["comparison"]["side_exceeds_nagamochi"]
    receipt = linear.N122_PACKET / "receipts/linear-audit.json"
    expected = json.dumps(audit, indent=2, default=str) + "\n"
    assert receipt.read_text(encoding="utf-8") == expected


def test_n122s_proof_bundle_is_fetched_from_its_release_asset() -> None:
    """The source published the bundle in a release asset, not at the commit, so the
    route takes it from the asset the packet's record pins, and a plan says so."""
    manifest = json.loads((linear.N122_PACKET / "source-manifest.json").read_text())
    pin = mixed.release_pin(N122)
    assert pin is not None
    release = manifest["release"]
    assert (pin["url"], pin["bytes"], pin["sha256"]) == (
        release["url"],
        release["bytes"],
        release["sha256"],
    )
    bundle = manifest["proof_bundle"]
    assert mixed.tarball_pin(N122) == (bundle["sha256"], bundle["bytes"])
    assert pin["member"]["member"] == f"certificates/mixed_n122_L1126/{bundle['name']}"
    plan = linear.linear_plan(N122, 2)
    assert all("--via release" in row["command"] for row in plan["parts"])
    price = linear.linear_price()["certificates"]["n122"]
    assert [sample["index"] for sample in price["samples"]] == [37, 108]
    assert price["upstream_cpu_hours"] == 14.41


def test_a_tarball_is_checked_only_against_its_own_packet(tmp_path: Path) -> None:
    stray = tmp_path / N82.tarball
    stray.write_bytes(b"not the bundle")
    with pytest.raises(ValueError, match="is not a tarball"):
        linear.linear_audit_supplements([stray], PACKET)
    with pytest.raises(ValueError, match="the pin is"):
        linear.linear_audit_supplements([stray], linear.N82_PACKET)


def test_an_unpinned_change_is_refused() -> None:
    certificate = linear.LINEAR["n101"]
    files = dict(linear.linear_retained(certificate))
    files["candidate.json"] += b"\n"
    with pytest.raises(ValueError, match=r"candidate\.json is not the pinned file"):
        linear.linear_certificate(certificate, files)


def _heavier(data: Any) -> None:
    item = data["primitives"][0]
    item["mass"] = str(Fraction(item["mass"]) + Fraction(1, 10**9))


def _moved(data: Any) -> None:
    item = data["primitives"][0]
    item["geometry"][0] = str(Fraction(item["geometry"][0]) + Fraction(1, 10**6))


@pytest.mark.parametrize(
    ("change", "match"),
    [
        (_heavier, "total mass differs"),
        (_moved, "recomputed candidate digest differs"),
        (lambda data: data.__setitem__("B", "0.998"), "count, side or core"),
        (lambda data: data.__setitem__("L", "10.29"), "count, side or core"),
    ],
    ids=["heavier", "moved", "core", "side"],
)
def test_a_changed_measure_is_refused_even_when_repinned(
    change: Callable[[Any], None], match: str
) -> None:
    _refused(linear.LINEAR["n101"], "candidate.json", change, match)


def test_another_orbit_count_is_refused() -> None:
    certificate = dataclasses.replace(linear.LINEAR["n83"], points=87)
    with pytest.raises(ValueError, match="orbit counts"):
        linear.linear_certificate(certificate)


def test_a_net_the_manifest_and_certificate_disagree_on_is_refused() -> None:
    def change(data: Any) -> None:
        data["net"]["step"] = "1/500"

    _refused(linear.LINEAR["n83"], "manifest.json", change, "nets differ")


def test_a_net_that_is_not_the_recomputed_one_is_refused() -> None:
    certificate = linear.LINEAR["n83"]
    files = dict(linear.linear_retained(certificate))
    tree = dict(mixed.read_subtree_manifest(certificate.subtree))
    for name in ("manifest.json", "certificate.json"):
        data = json.loads(files[name])
        data["net"]["side_margin"] = "1/1000"
        files[name] = json.dumps(data).encode()
        tree[certificate.directory / name] = _sha256(files[name])
    with pytest.raises(ValueError, match="net record differs"):
        linear.linear_certificate(certificate, files, tree)


def test_another_checker_is_refused() -> None:
    def change(data: Any) -> None:
        data["source_sha256"] = "0" * 64

    _refused(linear.LINEAR["n101"], "manifest.json", change, "another measure or checker")


@pytest.mark.parametrize(
    "change",
    [
        lambda data: data["results"]["7"].__setitem__("status", "ANGLE_VERIFIED"),
        lambda data: data["results"]["7"].__setitem__("nodes", 0),
        lambda data: data["results"].pop("200"),
        lambda data: data["results"]["7"].__setitem__("lower", 1.0),
    ],
    ids=["status", "no-nodes", "missing", "extra-field"],
)
def test_a_record_that_is_not_a_replayed_angle_is_refused(
    change: Callable[[Any], None],
) -> None:
    _refused(linear.LINEAR["n101"], "certificate.json", change, "angle|201 net angles")


def test_an_audit_binding_another_certificate_is_refused() -> None:
    def change(data: Any) -> None:
        data["theorem"] = "another"

    _refused(linear.LINEAR["n101"], "certificate.json", change, "binds another certificate")


def test_an_audit_naming_another_tarball_is_refused() -> None:
    def change(data: Any) -> None:
        data["archive_sha256"] = "0" * 64

    _refused(linear.LINEAR["n83"], "completion-audit.json", change, "binds another tarball")


# --------------------------------------------------------------------------- the measure


def _toy() -> dict[str, Any]:
    """A two-square measure with one primitive of each kind, inside a 3/2 box."""
    return {
        "schema": linear.LINEAR_SCHEMA,
        "n": 2,
        "L": "3/2",
        "B": "0.9977",
        "net": {"step": "83/40000", "last": 200},
        "primitives": [
            {"kind": "point", "geometry": ["1/3", "1/2"], "mass": "1/2"},
            {"kind": "segment", "geometry": ["1/10", "1/5", "1", "1/5"], "mass": "1/4"},
            {"kind": "rectangle", "geometry": ["1/5", "1/5", "2/5", "3/10"], "mass": "1/4"},
        ],
        "total_mass": "1",
    }


@pytest.mark.parametrize(
    ("primitive", "match"),
    [
        ({"kind": "point", "geometry": ["2", "1/2"], "mass": "1"}, "outside"),
        ({"kind": "point", "geometry": ["1", "1/2"], "mass": "-1"}, "negative"),
        ({"kind": "segment", "geometry": ["1", "1", "1", "1"], "mass": "1"}, "length zero"),
        ({"kind": "rectangle", "geometry": ["1", "1", "1/2", "3/2"], "mass": "1"}, "empty"),
        ({"kind": "disk", "geometry": ["1", "1", "1/2"], "mass": "1"}, "unknown"),
        ({"kind": "point", "geometry": ["1"], "mass": "1"}, "coordinates"),
    ],
    ids=["outside", "negative", "segment", "rectangle", "kind", "short"],
)
def test_a_malformed_primitive_is_refused(primitive: dict[str, Any], match: str) -> None:
    data = _toy() | {"primitives": [primitive]}
    with pytest.raises(ValueError, match=match):
        linear.linear_measure(data)


def test_the_images_are_the_eight_d4_images_in_the_sources_order() -> None:
    measure = linear.linear_measure(_toy())
    third, half, side = Fraction(1, 3), Fraction(1, 2), Fraction(3, 2)
    assert [g for g, _ in measure.images["point"]] == [
        (third, half),
        (third, side - half),
        (side - third, half),
        (side - third, side - half),
        (half, third),
        (half, side - third),
        (side - half, third),
        (side - half, side - third),
    ]
    assert {w for _, w in measure.images["point"]} == {Fraction(1, 16)}


def test_the_images_are_d4_invariant_and_a_broken_orbit_is_not() -> None:
    measure = linear.linear_measure(_toy())
    side = measure.side
    assert linear.d4_invariant(measure.images, side)
    for kind in linear.KINDS:
        dropped = dict(measure.images) | {kind: measure.images[kind][1:]}
        assert not linear.d4_invariant(dropped, side)
        (geometry, weight), *rest = measure.images[kind]
        nudged = (tuple(v + Fraction(1, 10**9) for v in geometry), weight)
        assert not linear.d4_invariant(dict(measure.images) | {kind: [nudged, *rest]}, side)
        reweighted = (geometry, 2 * weight)
        assert not linear.d4_invariant(dict(measure.images) | {kind: [reweighted, *rest]}, side)


def test_the_exact_coverage_of_a_toy_measure() -> None:
    """At the axis angle a core centred at (1/2, 1/2) holds each kind as computed by hand."""
    data = _toy() | {
        "L": "2",
        "B": "1/2",
        "primitives": [
            {"kind": "point", "geometry": ["3/4", "1/2"], "mass": "8"},
            {"kind": "segment", "geometry": ["0", "1/2", "1", "1/2"], "mass": "8"},
            {"kind": "rectangle", "geometry": ["1/2", "1/2", "1", "1"], "mass": "8"},
        ],
    }
    measure = linear.linear_measure(data)
    found = linear.coverage_at(
        measure, (Fraction(1, 2), Fraction(1, 2)), Fraction(1), Fraction(0)
    )
    # The core is [1/4, 3/4]^2. Each image weighs 1. The point's images at (3/4, 1/2) and
    # (1/2, 3/4) are on its closed edge; the other six are outside.
    assert found["point"] == 2
    # The images on y = 1/2 and on x = 1/2 from 0 to 1 each have half their length
    # inside; the other six are outside.
    assert found["segment"] == 1
    # [1/2, 1]^2 is its own diagonal image, so two of the eight images are that square,
    # each of density 4, and the core holds a sixteenth of the unit area of each.
    assert found["rectangle"] == Fraction(1, 2)


# --------------------------------------------------------------------------- the bundle


def _bundle(root: Path, certificate: linear.LinearCertificate) -> dict[Path, str]:
    """A bundle with the source's shape around the toy candidate, and its digest list."""
    candidate = json.dumps(_toy(), indent=2).encode()
    records = {
        str(index): {"index": index, "status": "ANGLE_VERIFIED", "nodes": 1, "seconds": 0.5}
        for index in range(linear.LAST + 1)
    }
    summary = {
        "status": linear.LINEAR_STATUS,
        "globally_verified": True,
        "candidate_digest": certificate.candidate_digest,
        "complete_angles": linear.LAST + 1,
        "verified_angles": linear.LAST + 1,
        "records": records,
    }
    files = {
        "candidate.json": candidate,
        "certificate.json": b"{}",
        "manifest.json": b"{}",
        "replay-progress.json": json.dumps({"done": 201, "total": 201}).encode(),
        "summary.json": json.dumps(summary).encode(),
        "verify.cpp": CHECKER,
    }
    for index in range(linear.LAST + 1):
        folder = f"net{index:03}"
        files |= {
            f"{folder}/candidate.json": candidate,
            f"{folder}/input.txt": b"1\n",
            f"{folder}/result.json": b"{}",
            f"{folder}/verify.cpp": CHECKER,
        }
    for name, data in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(data)
    tree = {certificate.directory / name: _sha256(files[name]) for name in list(files)[:3]}
    tree[certificate.directory / "code/unified_linear_verify.cpp"] = _sha256(CHECKER)
    return tree


def test_a_bundle_of_the_sources_shape_is_bound(tmp_path: Path) -> None:
    certificate = linear.LINEAR["n101"]
    tree = _bundle(tmp_path, certificate)
    bound = linear.bundle_bindings(certificate, tmp_path, tree)
    assert bound["status"] == "BUNDLE_BOUND_TO_PACKET"
    assert (bound["files"], bound["checker_copies"]) == (810, 202)


@pytest.mark.parametrize(
    ("damage", "match"),
    [
        (lambda root: (root / "net007/extra.py").write_text("x"), "files differ"),
        (lambda root: (root / "net007/input.txt").unlink(), "files differ"),
        (lambda root: (root / "net150/verify.cpp").write_bytes(CHECKER + b"\n"), "checker"),
        (lambda root: (root / "net007/candidate.json").write_bytes(b"{}"), "another candidate"),
        (lambda root: (root / "candidate.json").write_bytes(b"{}"), "not the retained file"),
        (
            lambda root: (root / "replay-progress.json").write_text(
                '{"done": 200, "total": 201}'
            ),
            "progress",
        ),
    ],
    ids=["extra", "missing", "checker", "angle-candidate", "candidate", "progress"],
)
def test_a_damaged_bundle_is_refused(
    tmp_path: Path, damage: Callable[[Path], object], match: str
) -> None:
    certificate = linear.LINEAR["n101"]
    tree = _bundle(tmp_path, certificate)
    damage(tmp_path)
    with pytest.raises(ValueError, match=match):
        linear.bundle_bindings(certificate, tmp_path, tree)


def test_a_bundle_whose_summary_records_an_unverified_angle_is_refused(tmp_path: Path) -> None:
    certificate = linear.LINEAR["n101"]
    tree = _bundle(tmp_path, certificate)
    summary = json.loads((tmp_path / "summary.json").read_text())
    summary["records"]["99"]["status"] = "ANGLE_BELOW_GAMMA"
    (tmp_path / "summary.json").write_text(json.dumps(summary))
    with pytest.raises(ValueError, match="summary"):
        linear.bundle_bindings(certificate, tmp_path, tree)


# --------------------------------------------------------------------------- the inputs


def _interval(value: Fraction) -> list[str]:
    """The source's outward interval: the nearest double, widened by one ulp if inexact."""
    v = float(value)
    low = math.nextafter(v, -math.inf) if Fraction(v) > value else v
    high = math.nextafter(v, math.inf) if Fraction(v) < value else v
    return [low.hex(), high.hex()]


def _rows(data: dict[str, Any]) -> dict[str, list[tuple[Fraction, ...]]]:
    measure = linear.linear_measure(data)
    rows: dict[str, list[tuple[Fraction, ...]]] = {
        "rectangle": [
            (x0, y0, x1, y1, w / ((x1 - x0) * (y1 - y0)))
            for (x0, y0, x1, y1), w in measure.images["rectangle"]
        ],
        "point": [(*g, w) for g, w in measure.images["point"]],
        "segment": [(*g, w) for g, w in measure.images["segment"]],
    }
    return rows


def _write_angle(
    root: Path,
    data: dict[str, Any],
    index: int,
    shipped: dict[str, Any],
    lines: list[str] | None = None,
) -> None:
    """One angle folder as the shipped export writes it, unless ``lines`` replaces the input."""
    measure = linear.linear_measure(data)
    t = index * linear.STEP
    c, s = net_rotation(t)
    width = (measure.side - measure.core * (c + s)) / 2
    if lines is None:
        header = (measure.side, measure.core, width, c, s, Fraction(1))
        lines = [" ".join(_interval(value)) for value in header]
        for rows in _rows(data).values():
            lines.append(str(len(rows)))
            lines.extend(" ".join(token for v in row for token in _interval(v)) for row in rows)
    raw = ("\n".join(lines) + "\n").encode()
    spec = {
        "candidate_digest": linear.semantic_digest(data),
        "index": index,
        "t": str(t),
        "L": str(measure.side),
        "B": str(measure.core),
        "E": str(width),
        "gamma": "1",
        "mass": str(measure.total),
        "source_sha256": linear.LINEAR_CHECKER_SHA256,
        "input_sha256": _sha256(raw),
    }
    result = {
        "status": "ANGLE_VERIFIED",
        "nodes": 10,
        "frontier": [],
        "exact_witnesses": [],
        "manifest": spec,
    }
    folder = root / f"net{index:03}"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "input.txt").write_bytes(raw)
    (folder / "result.json").write_text(json.dumps(result))
    shipped[str(index)] = {"input_sha256": spec["input_sha256"], "nodes": 10}


def _inputs(root: Path, indices: list[int]) -> tuple[str, dict[str, Any]]:
    data = _toy()
    candidate = json.dumps(data, indent=2).encode()
    (root / "candidate.json").write_bytes(candidate)
    shipped: dict[str, Any] = {}
    for index in indices:
        _write_angle(root, data, index, shipped)
    return _sha256(candidate), shipped


def test_inputs_that_enclose_the_candidate_are_bound(tmp_path: Path) -> None:
    digest, shipped = _inputs(tmp_path, [0, 7, 200])
    found = linear.check_inputs(tmp_path, digest, [0, 7, 200], shipped)
    assert found["status"] == "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"
    assert found["images"] == {"rectangle": 8, "point": 8, "segment": 8}


def _lines(root: Path, index: int) -> list[str]:
    return (root / f"net{index:03}" / "input.txt").read_text().splitlines()


@pytest.mark.parametrize(
    ("edit", "match"),
    [
        (lambda lines: lines.__setitem__(8, lines[7]), "rectangle"),
        (lambda lines: lines.pop(), "segment|zip"),
        (
            lambda lines: lines.__setitem__(5, "0x1.fffffffffffffp-1 0x1.0000000000001p+0"),
            "gamma",
        ),
        (lambda lines: lines.__setitem__(2, "0x1.0p+0 0x1.0p+0"), "header"),
        (lambda lines: lines.append("0"), "extra lines"),
    ],
    ids=["rectangle", "missing-line", "gamma", "width", "extra"],
)
def test_an_input_that_does_not_enclose_the_candidate_is_refused(
    tmp_path: Path, edit: Callable[[list[str]], object], match: str
) -> None:
    digest, shipped = _inputs(tmp_path, [7])
    lines = _lines(tmp_path, 7)
    edit(lines)
    _write_angle(tmp_path, _toy(), 7, shipped, lines)
    with pytest.raises(ValueError, match=match):
        linear.check_inputs(tmp_path, digest, [7], shipped)


def test_an_input_that_is_not_the_recorded_one_is_refused(tmp_path: Path) -> None:
    digest, shipped = _inputs(tmp_path, [7])
    shipped["7"]["input_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="not the recorded one"):
        linear.check_inputs(tmp_path, digest, [7], shipped)


def test_an_angle_whose_stored_result_is_unresolved_is_refused(tmp_path: Path) -> None:
    digest, shipped = _inputs(tmp_path, [7])
    path = tmp_path / "net007/result.json"
    result = json.loads(path.read_text())
    result["frontier"] = [[0.5, 0.5, 0.25, 0.25]]
    path.write_text(json.dumps(result))
    with pytest.raises(ValueError, match="stored result"):
        linear.check_inputs(tmp_path, digest, [7], shipped)


# --------------------------------------------------------------------------- receipts


def _run(certificate: linear.LinearCertificate, run: str, **changes: Any) -> dict[str, Any]:
    digest, _ = mixed.tarball_pin(certificate)
    record: dict[str, Any] = {
        "run": run,
        "certificate": certificate.name,
        "tarball": {"sha256": digest},
        "bindings": {"status": "BUNDLE_BOUND_TO_PACKET"},
        "preconditions": {
            "status": "DRIVER_PRECONDITIONS_HOLD",
            "candidate_digest": certificate.candidate_digest,
        },
        "inputs": {"status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"},
        "environment": {"PYTHONOPTIMIZE": None},
        "host": {"cpu": "test host"},
    }
    return record | changes


def _row(run: str, index: int, report: dict[str, Any]) -> dict[str, Any]:
    """A direction row as the linear worker writes it."""
    return {
        "run": run,
        "index": index,
        "status": "REPLAYED",
        "report": report,
        "replayed_sha256": _sha256(json.dumps(report, indent=2).encode()),
        "cpu_seconds": 2.0,
    }


def _receipts(
    tmp_path: Path,
    certificate: linear.LinearCertificate,
    ranges: list[tuple[int, int]],
    **run_changes: Any,
) -> Path:
    shipped = mixed.shipped_results(certificate)
    receipts = tmp_path / "receipts"
    for first, last in ranges:
        folder = receipts / mixed.range_name(first, last)
        folder.mkdir(parents=True)
        run = f"run-{first}"
        (folder / "runs.jsonl").write_text(
            json.dumps(_run(certificate, run, **run_changes)) + "\n"
        )
        rows = [_row(run, index, shipped[str(index)]) for index in range(first, last + 1)]
        (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return receipts


def test_complete_linear_receipts_merge_into_a_full_replay(tmp_path: Path) -> None:
    certificate = linear.LINEAR["n83"]
    receipts = _receipts(tmp_path, certificate, [(0, 120), (121, 200)])
    merged = mixed.mixed_merge(certificate, receipts)
    assert merged["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert merged["angles_replayed"] == 201
    summary = mixed.range_summary(certificate, receipts / "range-121-200", 121, 200)
    assert summary["status"] == "RANGE_REPLAYED"


def test_a_linear_angle_with_another_node_count_is_refused(tmp_path: Path) -> None:
    certificate = linear.LINEAR["n83"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    folder = receipts / "range-000-200"
    rows = [json.loads(line) for line in (folder / "directions.jsonl").read_text().splitlines()]
    report = rows[50]["report"] | {"nodes": rows[50]["report"]["nodes"] + 1}
    rows[50] = _row(rows[50]["run"], 50, report)
    (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    merged = mixed.mixed_merge(certificate, receipts)
    assert merged["status"] == "DIFFERS"
    assert merged["refused"] == ["range-000-200: angle 50 REPLAYED"]


def test_a_linear_run_on_another_tarball_is_refused(tmp_path: Path) -> None:
    certificate = linear.LINEAR["n101"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)], tarball={"sha256": "0" * 64})
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        mixed.mixed_merge(certificate, receipts)


def test_each_committed_linear_receipt_merges_without_a_refusal() -> None:
    for certificate in linear.LINEAR.values():
        state = mixed.replay_receipts(certificate)
        assert state is None or state["status"] != "DIFFERS"


# --------------------------------------------------------------------------- plan and price


@pytest.mark.parametrize("parts", [1, 4, 7])
def test_a_plan_splits_every_angle_into_contiguous_ranges(parts: int) -> None:
    plan = linear.linear_plan(linear.LINEAR["n83"], parts)
    ranges = [row["range"] for row in plan["parts"]]
    assert len(ranges) == parts
    assert ranges[0][0] == 0
    assert ranges[-1][1] == linear.LAST
    assert all(b[0] == a[1] + 1 for a, b in itertools.pairwise(ranges))
    assert all("--via git" in row["command"] for row in plan["parts"])


def test_each_price_rests_on_its_own_samples() -> None:
    price = linear.linear_price()["certificates"]
    for name in NAMES:
        row = price[name]
        assert row["samples"], name
        assert 0 < row["host_over_upstream"] < 10
        assert row["cpu_hours"] > row["upstream_cpu_hours"] / 10
    # n = 82 has no sampled angle, so it is listed with the source's seconds and no estimate.
    assert price["n82"] == {"nodes": 153579479, "upstream_cpu_hours": 33.04}


# --------------------------------------------------------------------------- the control


def _control() -> dict[str, Any]:
    return json.loads((linear.LINEAR["n101"].receipts / "control.json").read_text())


def test_the_control_accepts_the_original_and_refuses_both_mutations() -> None:
    control = _control()
    assert control["status"] == "CONTROLS_REFUSED"
    verdicts = {run["name"]: run["run"]["verdict"] for run in control["runs"]}
    assert verdicts == {
        "original": "ACCEPTED",
        "scale-masses": "REFUSED",
        "drop-top-contributor": "REFUSED",
    }
    original = control["runs"][0]
    assert original["candidate_digest"] == linear.LINEAR["n101"].candidate_digest
    assert original["run"]["output"]["nodes"] == control["shipped_record"]["nodes"]
    assert control["checker"]["source_sha256"] == linear.LINEAR_CHECKER_SHA256


def test_the_mutations_are_regenerated_and_provably_uncovered() -> None:
    control = _control()
    data = json.loads(linear.linear_retained(linear.LINEAR["n101"])["candidate.json"])
    centre = tuple(Fraction(v) for v in control["witness"]["centre"])
    assert len(centre) == 2
    c, s = net_rotation(Fraction(control["witness"]["t"]))
    runs = {run["name"]: run for run in control["runs"]}
    row = runs["drop-top-contributor"]["mutation"]["row"]
    for kind in linear.LINEAR_MUTATIONS:
        mutated = linear.mutate_linear(data, kind, row)
        assert linear.semantic_digest(mutated) == runs[kind]["candidate_digest"]
        at = sum(
            linear.coverage_at(
                linear.linear_measure(mutated), (centre[0], centre[1]), c, s
            ).values(),
            Fraction(),
        )
        assert at < 1
        assert str(at) == runs[kind]["witness_coverage_exact"]
    assert Fraction(runs["scale-masses"]["mutation"]["factor"]) == CONTROL_FACTOR
