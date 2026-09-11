"""The standalone threshold verifier, its generated claims, and hostile small inputs."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from random import Random
from typing import cast

import pytest

from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.threshold import ThresholdAtom, minimum_charge

PACKING = Path(__file__).resolve().parents[1]
CASE = PACKING / "cases" / "n11_threshold_certificate"
VERIFIER = CASE / "verify_claim.py"
T025_CERTIFICATE = CASE / "certificate.json"
T026_CERTIFICATE = CASE / "certificate-191-50-net1440.json"
T026_LIMIT = CASE / "t-026-dilation-limit-corollary.json"
T025_CLAIM = CASE / "t-025-verifiable-claim-191-50.md"
T026_CLAIM = CASE / "t-026-verifiable-claim-dilation-limit.md"


def load_verifier():
    spec = importlib.util.spec_from_file_location("threshold_claim_verifier", VERIFIER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def d4_set(points: tuple[tuple[str, str], ...]) -> list[tuple[tuple[str, str], ...]]:
    def images(point: tuple[str, str]) -> tuple[tuple[int, int], ...]:
        x, y = map(int, point)
        flips = [(p, q) for p in (x, 2 - x) for q in (y, 2 - y)]
        return *flips, *((q, p) for p, q in flips)

    per_point = [images(point) for point in points]
    return sorted(
        {
            tuple(sorted((str(images[g][0]), str(images[g][1])) for images in per_point))
            for g in range(8)
        }
    )


def small_certificate() -> dict[str, object]:
    atoms = [
        [str(Fraction(x, 5)), str(Fraction(y, 5)), "1"] for x in range(11) for y in range(11)
    ]
    threshold_atoms = [
        {"points": [list(point) for point in points], "threshold": 2, "weight": "1/10"}
        for points in d4_set((("0", "0"), ("0", "1"), ("1", "0")))
    ]
    threshold_budget = sum(len(item["points"]) // item["threshold"] for item in threshold_atoms)
    total = f"{1210 + threshold_budget}/{10}"
    return {
        "id": "small-two-of-three",
        "variant": "threshold",
        "n": 200,
        "claim": "s(200) >= 2",
        "outer_side": "2",
        "square_side": "1/2",
        "angle_limit": "21/50",
        "direction_steps": 2,
        "symmetry": "D4",
        "point_mass": "121",
        "threshold_budget": f"{threshold_budget}/10",
        "total_budget": total,
        "atoms": atoms,
        "threshold_atoms": threshold_atoms,
    }


def encoded(record: dict[str, object]) -> bytes:
    return (json.dumps(record, separators=(",", ":")) + "\n").encode()


def test_small_two_of_three_certificate_is_decided_exactly(
    capsys: pytest.CaptureFixture[str],
) -> None:
    verifier = load_verifier()
    holds, _, facts = verifier.check_certificate(encoded(small_certificate()))
    assert holds
    assert facts[6] >= 1
    assert "Condition 5' holds" in capsys.readouterr().out


def test_range_minimum_matches_a_naive_vector() -> None:
    verifier = load_verifier()
    random = Random(20260910)
    values = [0] * 37
    tree = verifier.RangeMinimum(len(values))
    for _ in range(200):
        left = random.randrange(len(values))
        right = random.randrange(left, len(values))
        amount = random.randrange(-20, 21)
        tree.add(left, right, amount)
        for index in range(left, right + 1):
            values[index] += amount
        query_left = random.randrange(len(values))
        query_right = random.randrange(query_left, len(values))
        expected_value = min(values[query_left : query_right + 1])
        expected_index = values.index(expected_value, query_left, query_right + 1)
        assert tree.query(query_left, query_right) == (expected_value, expected_index)


def test_one_mixed_direction_matches_the_repository_direct_engine() -> None:
    verifier = load_verifier()
    loaded = verifier.load_certificate(encoded(small_certificate()))
    _, _, outer_side, square_side, angle_limit, steps, atoms, threshold_atoms, _ = loaded
    tangent = angle_limit / steps
    scale = 10
    standalone_value, witness, _ = verifier.least_charge(
        outer_side,
        square_side,
        tangent,
        atoms,
        threshold_atoms,
        scale,
    )
    project_atoms = tuple(
        Atom(f"p{index}", x, y, weight) for index, (x, y, weight) in enumerate(atoms)
    )
    project_threshold_atoms = tuple(
        ThresholdAtom(points, threshold, weight)
        for points, threshold, weight in threshold_atoms
    )
    direction = rotation_from_half_tangent("small", tangent)
    project_value, _project_witness = minimum_charge(
        project_atoms,
        project_threshold_atoms,
        direction,
        outer_side,
        square_side,
    )
    assert standalone_value == project_value
    assert (
        verifier.exact_charge(
            atoms,
            threshold_atoms,
            direction.ux,
            direction.uy,
            square_side / 2,
            witness,
        )
        == project_value
    )


def test_symmetric_undercoverage_reaches_and_fails_condition_five(capsys) -> None:
    verifier = load_verifier()
    record = small_certificate()
    atoms = cast(list[list[str]], record["atoms"])
    for atom in atoms:
        atom[2] = "1/100"
    threshold_budget = Fraction(cast(str, record["threshold_budget"]))
    record["point_mass"] = "121/100"
    record["total_budget"] = str(Fraction(121, 100) + threshold_budget)
    holds, *_ = verifier.check_certificate(encoded(record))
    output = capsys.readouterr().out
    assert not holds
    assert "Condition 5' fails" in output


def test_a_stale_least_charge_declaration_is_refused(capsys) -> None:
    verifier = load_verifier()
    record = small_certificate()
    record["least_cell_charge"] = "999"
    holds, *_ = verifier.check_certificate(encoded(record))
    assert not holds
    assert "wrong fields: least_cell_charge" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("mutate", "refusal"),
    [
        (lambda record: record["threshold_atoms"][0].update(threshold=3), "only two-of-three"),
        (lambda record: record["threshold_atoms"].pop(), "missing or unequal D4 image"),
        (lambda record: record.update(total_budget="1"), "wrong fields: total_budget"),
        (lambda record: record["atoms"][0].__setitem__(2, 0.1), "rationals must be strings"),
    ],
)
def test_hostile_small_certificates_are_refused(mutate, refusal, capsys) -> None:
    verifier = load_verifier()
    record = small_certificate()
    mutate(record)
    try:
        holds, *_ = verifier.check_certificate(encoded(record))
    except (TypeError, ValueError) as error:
        assert refusal in str(error)
    else:
        assert not holds
        assert refusal in capsys.readouterr().out


def test_malformed_shapes_and_duplicate_keys_are_refused(tmp_path: Path) -> None:
    verifier = load_verifier()
    for index, raw in enumerate((b"[]", b'{"variant":"threshold","variant":"threshold"}')):
        path = tmp_path / f"bad-{index}.json"
        path.write_bytes(raw)
        assert verifier.main([str(path)]) == 1


def test_a_changed_embedded_byte_is_refused_before_the_sweep(tmp_path: Path) -> None:
    verifier = load_verifier()
    text = T025_CLAIM.read_text(encoding="utf-8")
    marker = verifier.CERT_BEGIN + "\n```json\n"
    head, data = text.split(marker, 1)
    changed = head + marker + data.replace('"id": "C-n011', '"id": "X-n011', 1)
    path = tmp_path / "changed.md"
    path.write_text(changed, encoding="utf-8")
    assert verifier.main([str(path)]) == 1


def test_a_declared_limit_with_a_malformed_marker_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verifier = load_verifier()
    text = T026_CLAIM.read_text(encoding="utf-8")
    marker = f"\n{verifier.LIMIT_BEGIN}\n```json\n"
    assert marker in text
    changed = text.replace(
        marker,
        "\n<!-- BROKEN DILATION LIMIT RECORD -->\n```json\n",
        1,
    )
    path = tmp_path / "missing-limit-marker.md"
    path.write_text(changed, encoding="utf-8")
    monkeypatch.setattr(
        verifier,
        "sweep",
        lambda *_args, **_kwargs: pytest.fail("malformed limit marker reached the sweep"),
    )
    assert verifier.main([str(path)]) == 1


@pytest.mark.parametrize(
    ("document", "certificate", "limit"),
    [
        (T025_CLAIM, T025_CERTIFICATE, None),
        (T026_CLAIM, T026_CERTIFICATE, T026_LIMIT),
    ],
)
def test_generated_claims_embed_the_exact_verifier_and_data(
    document, certificate, limit
) -> None:
    verifier = load_verifier()
    text = document.read_text(encoding="utf-8")
    source = text.split("```python\n", 1)[1].split("\n```", 1)[0] + "\n"
    assert source.encode() == VERIFIER.read_bytes()
    cert_raw, limit_raw, declarations = verifier.read_input(document)
    assert cert_raw == certificate.read_bytes()
    assert declarations["certificate"] == (
        hashlib.sha256(cert_raw).hexdigest(),
        len(cert_raw),
    )
    if limit is None:
        assert limit_raw is None
    else:
        assert limit_raw == limit.read_bytes()
        assert declarations["limit record"] == (
            hashlib.sha256(limit_raw).hexdigest(),
            len(limit_raw),
        )


def test_t026_rederives_its_limit_without_invoking_t025(capsys) -> None:
    verifier = load_verifier()
    cert_raw = T026_CERTIFICATE.read_bytes()
    loaded = verifier.load_certificate(cert_raw)
    certificate, n, outer_side, square_side, angle_limit, steps, _, _, declared = loaded
    tangents = tuple(angle_limit * k / steps for k in range(steps + 1))
    half_gap = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    holds, theorem = verifier.check_limit_record(
        T026_LIMIT.read_bytes(),
        cert_raw,
        certificate,
        (
            n,
            outer_side,
            square_side,
            angle_limit,
            steps,
            declared["total_budget"],
            declared["least_cell_charge"],
            half_gap,
        ),
    )
    assert holds
    assert theorem == "s(11) >= 955000*sqrt(518400042893309449)/179696714646249"
    assert "Dilation limit holds" in capsys.readouterr().out
    claim = T026_CLAIM.read_text(encoding="utf-8")
    assert "without invoking T-025 as a theorem" in claim


def test_t026_data_are_an_exact_rescaling_and_the_sharp_family_is_larger() -> None:
    coarse = json.loads(T025_CERTIFICATE.read_text(encoding="utf-8"))
    fine = json.loads(T026_CERTIFICATE.read_text(encoding="utf-8"))
    normalization = Fraction(500000000, 498684619)

    def point_weights(record):
        return {
            (Fraction(x), Fraction(y)): Fraction(weight) for x, y, weight in record["atoms"]
        }

    def threshold_weights(record):
        return {
            (
                tuple(sorted((Fraction(x), Fraction(y)) for x, y in atom["points"])),
                atom["threshold"],
            ): Fraction(atom["weight"])
            for atom in record["threshold_atoms"]
        }

    coarse_points, fine_points = point_weights(coarse), point_weights(fine)
    assert coarse_points.keys() == fine_points.keys()
    assert all(
        fine_points[key] == weight * normalization for key, weight in coarse_points.items()
    )
    coarse_thresholds = threshold_weights(coarse)
    fine_thresholds = threshold_weights(fine)
    assert coarse_thresholds.keys() == fine_thresholds.keys()
    assert all(
        fine_thresholds[key] == weight * normalization
        for key, weight in coarse_thresholds.items()
    )

    outer_side, core_side, angle_limit = (
        Fraction(fine[key]) for key in ("outer_side", "square_side", "angle_limit")
    )
    steps = fine["direction_steps"]
    tangents = [angle_limit * index / steps for index in range(steps + 1)]
    half_gap = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    bounded_side_squared = (
        outer_side
        * outer_side
        * (1 + half_gap * half_gap)
        / (core_side * core_side * (1 + half_gap) ** 2)
    )
    assert bounded_side_squared == Fraction(
        472793799119770550224225000000,
        32290909254655439869209770001,
    )
    control = Fraction(100168777, 100000000)
    sharp_slack = 1 + half_gap * half_gap - control**2 * core_side**2 * (1 + half_gap) ** 2
    assert control * core_side * (1 + half_gap) > 1
    assert sharp_slack > 0
    assert bounded_side_squared > outer_side * outer_side


@pytest.mark.parametrize(
    ("section", "field", "replacement", "refusal"),
    [
        (
            "conclusion",
            "bounded_side_defining_polynomial",
            "x^2 - 1",
            "bounded-side polynomial",
        ),
        (
            "strict_dilation_family",
            "factor_domain",
            (
                "q in Q with q > 0 and q^2 > "
                "32400002680831840562500000000/32290909254655439869209770001"
            ),
            "factor domain",
        ),
        (
            "sharpened_containment",
            "monotonicity_identity",
            "0 >= 1",
            "monotonicity identity",
        ),
    ],
)
def test_changed_limit_mathematics_is_refused(
    section: str,
    field: str,
    replacement: object,
    refusal: str,
    capsys,
) -> None:
    verifier = load_verifier()
    limit = deepcopy(json.loads(T026_LIMIT.read_text(encoding="utf-8")))
    limit[section][field] = replacement
    cert_raw = T026_CERTIFICATE.read_bytes()
    loaded = verifier.load_certificate(cert_raw)
    certificate, n, outer_side, square_side, angle_limit, steps, _, _, declared = loaded
    tangents = tuple(angle_limit * k / steps for k in range(steps + 1))
    half_gap = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    holds, _ = verifier.check_limit_record(
        encoded(limit),
        cert_raw,
        certificate,
        (
            n,
            outer_side,
            square_side,
            angle_limit,
            steps,
            declared["total_budget"],
            declared["least_cell_charge"],
            half_gap,
        ),
    )
    assert not holds
    assert refusal in capsys.readouterr().out


def test_threshold_claims_are_current() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "devtools.render_verifiable_claim", "--check"],
        cwd=PACKING,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.exhaustive_exact
@pytest.mark.parametrize(
    ("document", "first_minimum"),
    [(T025_CLAIM, "direction 69"), (T026_CLAIM, "direction 914")],
    ids=["t025", "t026"],
)
def test_retained_threshold_claims_pass_the_standalone_full_sweep(
    document: Path,
    first_minimum: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Deferred: the two raw claim files each run every exact event-cell slab."""
    verifier = load_verifier()
    assert verifier.main([str(document)]) == 0
    assert first_minimum in capsys.readouterr().out
