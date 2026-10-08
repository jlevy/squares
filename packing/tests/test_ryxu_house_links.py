"""Exact source presentation, complete house custody and actual worker admission."""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
from decimal import getcontext
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import pytest

from devtools import build_known_best_atlas as atlas
from devtools import confirm_ryxu_records as confirmation
from devtools import generate_frontier_case as generator
from devtools import refinement_packets
from devtools import register_ryxu_reports as register
from devtools import run_negative_controls as controls
from devtools import ryxu_house_links as houses
from sqpack.render import render_packing_svg
from sqpack.render.model import EvidenceTier, RenderSpec, ScalarKind
from sqpack.witness import materialize_exact_witness, witness_document
from sqpack.yamlio import safe_load

SOURCE = houses.REPO


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "private"
    packet = repo / houses.reports.PACKET.relative_to(SOURCE)
    shutil.copytree(houses.reports.PACKET, packet)
    original_metadata = houses.METADATA
    monkeypatch.setattr(houses.reports, "REPO", repo)
    monkeypatch.setattr(houses.reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", repo)
    monkeypatch.setattr(houses, "METADATA", repo / original_metadata.relative_to(SOURCE))
    monkeypatch.setattr(houses.shared.confirmation, "REPO", repo)
    monkeypatch.setattr(register, "REPO", repo)
    monkeypatch.setattr(
        register, "HISTORY", packet / "acquisition/frontier-prior-state.json.xz"
    )
    for n in houses.NUMBERS:
        path = houses.house_path(n)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(SOURCE / path.relative_to(repo))
    return repo


def test_exact_radical_projection_keeps_all_coefficient_geometry() -> None:
    witness = houses.expected_witness(51)
    original = copy.deepcopy(witness)
    frame = atlas.frame_from_witness(witness)
    assert frame.evidence is EvidenceTier.CERTIFIED_UPPER_BOUND
    assert json.loads(frame.container_side.source) == {
        "coefficients": ["16/3", "5/3"],
        "field": witness["scalar"],
    }
    _side, poses = houses.radical.inputs("positive")
    half = houses.radical.Q2(Fraction(1, 2))
    diagonal = houses.radical.Q2(b=Fraction(1, 2))
    for square, (x, y, angle) in zip(frame.squares, poses, strict=True):
        expected = (
            [
                (x - half, y - half),
                (x + half, y - half),
                (x + half, y + half),
                (x - half, y + half),
            ]
            if angle == "0"
            else [(x, y - diagonal), (x + diagonal, y), (x, y + diagonal), (x - diagonal, y)]
        )
        for point, (cx, cy) in zip(square.corners, expected, strict=True):
            assert point.x.kind is point.y.kind is ScalarKind.EXACT
            assert json.loads(point.x.source)["coefficients"] == cx.scalar()
            assert json.loads(point.y.source)["coefficients"] == cy.scalar()
    baseline = render_packing_svg(frame, spec=RenderSpec(overlays=frozenset()))
    decimal_precision, mp_precision = getcontext().prec, mp.mp.dps
    try:
        getcontext().prec = 5
        mp.mp.dps = 5
        projected = atlas.frame_from_witness(witness)
        assert render_packing_svg(projected, spec=RenderSpec(overlays=frozenset())) == baseline
        assert getcontext().prec == mp.mp.dps == 5
    finally:
        getcontext().prec, mp.mp.dps = decimal_precision, mp_precision
    assert witness == original


def test_rational_center_basis_corners_remain_exact() -> None:
    witness = houses.expected_witness(70)
    original = copy.deepcopy(witness)
    frame = atlas.frame_from_witness(witness)
    assert frame.container_side.kind is ScalarKind.RATIONAL
    assert Fraction(frame.container_side.source) == Fraction(witness["side"])
    for square, source in zip(frame.squares, witness["squares"], strict=True):
        cx, cy = map(Fraction, source["center"])
        c, s = map(Fraction, source["basis"])
        expected = [
            (cx - c / 2 + s / 2, cy - s / 2 - c / 2),
            (cx + c / 2 + s / 2, cy + s / 2 - c / 2),
            (cx + c / 2 - s / 2, cy + s / 2 + c / 2),
            (cx - c / 2 - s / 2, cy - s / 2 + c / 2),
        ]
        for point, pair in zip(square.corners, expected, strict=True):
            assert point.x.kind is point.y.kind is ScalarKind.RATIONAL
            assert (Fraction(point.x.source), Fraction(point.y.source)) == pair
    corners, side = materialize_exact_witness(witness)
    assert side == Fraction(witness["side"])
    assert all(isinstance(value, Fraction) for square in corners for p in square for value in p)
    assert witness == original


def test_full_house_admission_calls_no_geometric_predicate(
    private: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert private == houses.REPO

    def forbidden(*_args, **_kwargs):
        pytest.fail("house admission invoked a new geometric decider")

    monkeypatch.setattr(houses.radical, "exact_verify", forbidden)
    monkeypatch.setattr(houses.reports.legacy, "exact_verify", forbidden)
    monkeypatch.setattr(houses.reports.legacy.independent, "check_squares", forbidden)
    monkeypatch.setattr(houses.radical, "independent", forbidden)
    admitted = houses.check_houses()
    assert tuple(admitted) == houses.NUMBERS
    assert admitted[51]["side"] == ["16/3", "5/3"]
    assert admitted[51]["square_size"] == "1"


@pytest.mark.parametrize("n", [51, 70, 105, 108, 295])
@pytest.mark.parametrize("mutation", ["source", "claim", "result", "geometry", "extra"])
def test_complete_house_mutants_are_refused(
    private: Path, tmp_path: Path, n: int, mutation: str
) -> None:
    assert private == houses.REPO
    witness = houses.check_houses([n])[n]
    if mutation == "source":
        witness["source"]["revision"] = "wrong-source"
    elif mutation == "claim":
        witness["claim"]["limitations"] = "Global optimality has been proved."
    elif mutation == "result":
        witness["certificate"]["result"]["pairs_tested"] -= 1
    elif mutation == "extra":
        witness["certificate"]["result"]["global_optimality"] = True
    else:
        witness["squares"][0]["center"][0] = ["2", "0"] if n == 51 else "2"
    changed = tmp_path / "changed.yaml"
    changed.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    leaf = houses.house_path(n)
    leaf.unlink()
    leaf.symlink_to(changed)
    with pytest.raises((ValueError, RuntimeError), match=r"differs|schema-invalid"):
        houses.check_houses([n])


@pytest.mark.parametrize("n", houses.NUMBERS)
def test_each_linked_house_producer_refuses_before_write(private: Path, n: int) -> None:
    assert private == houses.REPO
    before = houses.house_path(n).read_bytes()
    with pytest.raises(ValueError, match="escapes"):
        houses.guard_house_outputs([n])
    assert houses.house_path(n).read_bytes() == before


def test_private_metadata_cannot_change_scope(private: Path) -> None:
    assert private == houses.REPO
    value = houses.reports.kernel.read_xz(houses.METADATA)
    value["cases"][0]["metadata"]["certificate"]["result"]["limitations"] = "Global optimality."
    houses.reports.save(houses.METADATA, value)
    with pytest.raises(ValueError, match="native result differs"):
        houses.check_houses([51])


def test_radical_upward_display_is_strictly_outward() -> None:
    side, _poses = houses.radical.inputs("positive")
    shown = Fraction(houses.radical_display())
    assert (houses.radical.Q2(shown) - side).sign() >= 0
    assert (houses.radical.Q2(shown - Fraction(1, 10**16)) - side).sign() < 0


@pytest.mark.slow
def test_actual_worker_keeps_full_scientific_inputs_and_refuses_producers(
    tmp_path: Path,
) -> None:
    carried = {*controls.COPY_SEPARATELY, *controls.snapshot_pruned_targets()}
    assert set(houses.private_input_paths()) <= carried
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    for path in houses.private_input_paths():
        private = tree / path.relative_to(SOURCE)
        assert private.is_file()
        assert not private.is_symlink()
        assert private.read_bytes() == path.read_bytes()
    script = """
from devtools import ryxu_house_links as h, build_known_best_atlas as a
from devtools import refinement_custody as old425
from devtools import squish_second_update_confirmation as old422
old425.check_index(old425.read_index()); old422.admit_certification(); h.check_houses()
paths=(a.MANIFEST,a.SOURCE_MANIFEST,a.MANIFEST.parent/'composite-figure.json')
def contents(): return tuple(path.read_bytes() if path.exists() else None for path in paths)
before=contents()
for producer in (lambda: a.update_selected([51]), a.update):
    try: producer()
    except ValueError as e: assert 'escapes' in str(e)
    else: raise AssertionError('producer followed an external geometry leaf')
assert before==contents()
for path, route in [(h.reports.receipt_path(),'rational'),
                    (h.reports.PACKET/'receipts/n051-radical-positive.json.xz','radical')]:
    original=path.read_bytes()
    value=h.reports.kernel.read_xz(path)
    if route=='rational': value['cases'][0]['exact_verify']['pairs_tested']-=1
    else: value['exact_verify']['minimum_best_pair_gap']='1'
    try:
        h.reports.save(path,value)
        try: h.check_houses()
        except ValueError: pass
        else: raise AssertionError('copied deciding receipt corruption was accepted')
    finally: path.write_bytes(original)
    assert path.read_bytes()==original
    h.check_houses()
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tree / controls.HERE,
        env=controls.control_environment(tree, tmp_path / "pycache"),
        capture_output=True,
        text=True,
        timeout=45,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES


def test_frontier_witness_field_parser_is_independent_of_key_order() -> None:
    case = atlas._frontier_case(51)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    updated = atlas._frontier_with_witness(case, "W-known-best-n051")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    original = safe_load(case.text.split("---\n", 2)[1])
    assert safe_load(updated.split("---\n", 2)[1]) == original


@pytest.mark.parametrize("n", [51, 105, 108])
@pytest.mark.parametrize("mutation", ["side", "credit", "body"])
def test_source_adoption_refuses_mutable_upper_geometry_claims(
    private: Path, n: int, mutation: str
) -> None:
    assert private == houses.REPO
    original = (SOURCE / f"packing/frontier/n-{n:03d}.md").read_text()
    prefix, front, body = original.split("---\n", 2)
    document = safe_load(front)
    if mutation == "side":
        document["packing"]["reported_upper_bound"]["value"] = "99"
        document["packing"]["reported_upper_bound"]["exact_form"] = "99"
    elif mutation == "credit":
        document["packing"]["reported_upper_bound"]["found_by"] = ["wrong-finder"]
    else:
        body = body.replace("displayed upward as", "global optimum exactly equals")
    changed = prefix + "---\n" + register.dump(document) + "---\n" + body
    history = houses.reports.kernel.read_xz(register.HISTORY)
    old = next(row for row in history["cases"] if row["n"] == n)["frontier"]
    if n < 101:
        # The first hundred are curated source records, outside the generic source map.
        # Give the publication adapter a declared lower-lane draft with the complete
        # retained original frontmatter; its upper mutation must not alter that lane.
        drafted = (
            "---\n"
            + old.split("---\n", 2)[1]
            + (
                "---\n\n## The lower bound\n\nRetained lower-lane draft.\n"
                "\n<!-- BEGIN verification code: written by "
                "devtools.render_case_verifiers -->\n"
                "<!-- END verification code -->\n"
            )
        )
    else:
        availability = generator.load_availability()
        catalogue = generator.load_drafting_catalogue([n], availability)
        drafted = generator.generate_record(
            n,
            availability=availability,
            catalogue=catalogue,
            review_date="2026-10-08",
            retrieved_date="2026-10-08",
        )
    adopted = register.adopt_case(n, changed, drafted)
    result = safe_load(adopted.split("---\n", 2)[1])["packing"]
    assert result["reported_upper_bound"] == register.reported_bound(n)
    before = safe_load(old.split("---\n", 2)[1])["packing"]
    original_case = safe_load(original.split("---\n", 2)[1])["packing"]
    confirmed = any(
        ref.startswith("E-ryxu-") for ref in original_case["verified_upper_bound"]["evidence"]
    )
    expected_upper = houses.bound(n) if confirmed else before["verified_upper_bound"]
    assert result["verified_upper_bound"] == expected_upper
    lower_draft = safe_load(drafted.split("---\n", 2)[1])["packing"]
    for field in ("reported_lower_bound", "verified_lower_bound", "status"):
        assert result[field] == lower_draft[field]
    assert "global optimum exactly equals" not in adopted


def test_unmapped_confirming_evidence_is_refused(private: Path) -> None:
    assert private == houses.REPO
    original = (SOURCE / "packing/frontier/n-051.md").read_text()
    prefix, front, body = original.split("---\n", 2)
    document = safe_load(front)
    document["packing"]["verified_upper_bound"]["evidence"] = ["E-ryxu-made-up-feasibility"]
    changed = prefix + "---\n" + register.dump(document) + "---\n" + body
    with pytest.raises(ValueError, match="unmapped confirming evidence"):
        register.adopt_case(51, changed, original)


@pytest.fixture
def original_pair(
    private: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, dict[int, str]]:
    monkeypatch.setattr(houses, "NUMBERS", (51, 70))
    monkeypatch.setattr(register, "FRONTIER", private / "packing/frontier")
    register.FRONTIER.mkdir(parents=True)
    rows = houses.reports.kernel.read_xz(register.HISTORY)["cases"]
    originals = {row["n"]: row["frontier"] for row in rows if row["n"] in houses.NUMBERS}
    for n, text in originals.items():
        (register.FRONTIER / f"n-{n:03d}.md").write_text(text)
    register.HISTORY.unlink()
    monkeypatch.setattr(register, "save", lambda path, text: path.write_text(text))
    return private, originals


def test_later_case_preflight_failure_never_changes_an_earlier_case(
    original_pair: tuple[Path, dict[int, str]],
) -> None:
    private, originals = original_pair
    assert private == houses.REPO
    path = register.FRONTIER / "n-070.md"
    original = safe_load(originals[70].split("---\n", 2)[1])
    original["packing"]["reported_upper_bound"]["value"] = "0"
    body = originals[70].split("---\n", 2)[2]
    path.write_text("---\n" + register.dump(original) + "---\n" + body)
    before = {n: (register.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in houses.NUMBERS}
    with pytest.raises(ValueError, match="not smaller"):
        register.record_cases()
    assert not register.HISTORY.exists()
    assert before == {
        n: (register.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in houses.NUMBERS
    }


def test_complete_original_history_survives_interrupted_writes_and_retry(
    original_pair: tuple[Path, dict[int, str]], monkeypatch: pytest.MonkeyPatch
) -> None:
    private, originals = original_pair
    assert private == houses.REPO

    def interrupt_second(path: Path, text: str) -> None:
        assert register.HISTORY.exists()
        rows = register.read_history()
        assert {r["n"]: r["frontier"] for r in rows} == originals
        if path.name == "n-070.md":
            raise OSError("simulated interrupted second write")
        path.write_text(text)

    monkeypatch.setattr(register, "save", interrupt_second)
    with pytest.raises(OSError, match="interrupted second write"):
        register.record_cases()
    original_boundary = register.HISTORY.read_bytes()
    assert (register.FRONTIER / "n-070.md").read_text() == originals[70]
    monkeypatch.setattr(register, "save", lambda path, text: path.write_text(text))
    register.record_cases()
    for n in houses.NUMBERS:
        case = safe_load(
            (register.FRONTIER / f"n-{n:03d}.md").read_text().split("---\n", 2)[1]
        )["packing"]
        assert case["reported_upper_bound"] == register.reported_bound(n)
    assert register.HISTORY.read_bytes() == original_boundary
    assert register.record_cases() == []
    assert register.HISTORY.read_bytes() == original_boundary


def test_existing_incomplete_history_is_refused_before_case_writes(
    original_pair: tuple[Path, dict[int, str]],
) -> None:
    private, originals = original_pair
    assert private == houses.REPO
    houses.reports.save(
        register.HISTORY, {"format": "ryxu-432-prior-frontier-and-house-v1", "cases": []}
    )
    with pytest.raises(ValueError, match="complete immutable"):
        register.record_cases()
    assert originals == {
        n: (register.FRONTIER / f"n-{n:03d}.md").read_text() for n in houses.NUMBERS
    }


def confirmation_frontier(private: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    frontier = private / "packing/frontier"
    frontier.mkdir(parents=True)
    monkeypatch.setattr(register, "FRONTIER", frontier)
    monkeypatch.setattr(refinement_packets, "REPO", private)
    for name in ("results.yaml", "evidence.yaml", "verifiers.yaml", "source-coverage.yaml"):
        shutil.copyfile(SOURCE / "packing/frontier" / name, frontier / name)
    for n in houses.NUMBERS:
        name = f"n-{n:03d}.md"
        shutil.copyfile(SOURCE / "packing/frontier" / name, frontier / name)
    review = private / confirmation.REVIEW
    review.parent.mkdir(parents=True)
    review.write_text(
        "## Full Production Integration\n**Decision: accepted.**\n**R3, closed:**\n"
    )
    return frontier


def test_confirmation_requires_actual_independent_acceptance(private: Path) -> None:
    review = private / confirmation.REVIEW
    review.parent.mkdir(parents=True)
    review.write_text("## Full Production Integration\n**Decision: pending.**\n")
    with pytest.raises(ValueError, match="accepted independent"):
        confirmation.confirm()
    assert not (private / "packing/frontier").exists()


def test_confirmation_refuses_later_case_before_any_record_write(
    private: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    frontier = confirmation_frontier(private, monkeypatch)
    path = frontier / "n-070.md"
    prefix, front, body = path.read_text().split("---\n", 2)
    value = safe_load(front)
    value["packing"]["reported_upper_bound"]["value"] = "0"
    path.write_text(prefix + "---\n" + register.dump(value) + "---\n" + body)
    before = {path.name: path.read_bytes() for path in frontier.iterdir()}
    with pytest.raises(ValueError, match="complete admitted facts"):
        confirmation.confirm()
    assert before == {path.name: path.read_bytes() for path in frontier.iterdir()}


def test_confirmation_preserves_complete_scope_history_and_lower_lanes(
    private: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    frontier = confirmation_frontier(private, monkeypatch)
    original_history = register.HISTORY.read_bytes()
    original_source = safe_load((frontier / "source-coverage.yaml").read_text())
    before = {
        n: safe_load((frontier / f"n-{n:03d}.md").read_text().split("---\n", 2)[1])["packing"]
        for n in houses.NUMBERS
    }
    native_houses = {n: houses.house_path(n).read_bytes() for n in houses.NUMBERS}
    confirmation.confirm()
    results = safe_load((frontier / "results.yaml").read_text())["results"]
    for identifier, numbers in (("T-125", houses.reports.NUMBERS), ("T-126", (51,))):
        row = next(row for row in results if row["id"] == identifier)
        assert row["verification"] == "V3"
        assert row["confirmation"] == "C3"
        assert row["scope"]["n_values"] == list(numbers)
        assert row["reviews"][0]["reviewer_kind"] == "ai"
        assert "human oversight" in row["next_rung"]
    for n in houses.NUMBERS:
        text = (frontier / f"n-{n:03d}.md").read_text()
        case = safe_load(text.split("---\n", 2)[1])["packing"]
        assert case["verified_upper_bound"] == houses.bound(n)
        for field in (
            "reported_lower_bound",
            "verified_lower_bound",
            "reported_status",
            "status",
        ):
            assert case[field] == before[n][field]
        assert case["conjectured_optimum"] is None
        assert case["rigidity"] is None
        assert "V3/C3" in text
        assert "191-touching-pair assertion" in text
    after_source = safe_load((frontier / "source-coverage.yaml").read_text())
    assert set(after_source) == set(original_source)
    for field in original_source.keys() - {"sources", "selected_overrides"}:
        assert after_source[field] == original_source[field]
    assert {n: houses.house_path(n).read_bytes() for n in houses.NUMBERS} == native_houses
    assert register.HISTORY.read_bytes() == original_history
    first = {path.name: path.read_bytes() for path in frontier.iterdir()}
    confirmation.confirm()
    assert first == {path.name: path.read_bytes() for path in frontier.iterdir()}
    assert register.HISTORY.read_bytes() == original_history
