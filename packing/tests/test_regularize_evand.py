"""The driver around Evan Daniel's vendored regularizer, on inputs small enough to check.

The generator itself is not run here (the spikes run it, and its cost is far above the
per-test ceiling). What is held: a witness becomes upstream's input text without losing
exactness; a regularized certificate is mapped back into the source frame, decided on both
maintained routes and measured, on a committed n = 26 fixture made by a real run; the side
relation is exact against rational and quadratic-surd register forms; and every refusal
path names its reason.
"""

from __future__ import annotations

import json
import shutil
import sys
import types
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import pytest

from devtools import evand_exact_certificates as certificates
from devtools import regularize_evand as driver
from devtools import regularize_evand_shim as shim
from sqpack.yamlio import load_yaml

FIXTURES = Path(__file__).parent / "fixtures" / "regularize-evand"
#: The register's verified bound at n = 26 when the fixture was made.
BOUND_26 = {"value": "5.62132034355964257320253308631455", "exact_form": "(7/2) + (3/2)sqrt(2)"}


def _witness(squares: list[dict[str, Any]], side: str, representation: str) -> dict[str, Any]:
    return {
        "id": "W-test",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": representation,
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
    }


def _rows(text: str) -> tuple[list[str], list[list[str]]]:
    lines = text.strip().splitlines()
    return lines[0].split(), [line.split() for line in lines[1:]]


# --- counts, directories, children ---------------------------------------------------


def test_counts_read_numbers_and_ranges_once_each() -> None:
    assert driver.parse_counts(["5", "3-4", "4,10"]) == [3, 4, 5, 10]


@pytest.mark.parametrize("value", ["0", "7-5", ""])
def test_counts_refuse_what_is_not_a_count(value: str) -> None:
    with pytest.raises(driver.DriverError):
        driver.parse_counts([value])


def test_the_per_count_timeout_follows_the_brief() -> None:
    assert (driver.default_timeout(200), driver.default_timeout(201)) == (1800, 3600)


@pytest.mark.parametrize(
    "inside",
    [driver.ROOT / "witnesses" / "x", driver.ROOT / "atlas", driver.VENDORED / "search"],
)
def test_a_run_never_writes_into_the_record_the_atlas_or_the_vendored_tree(
    inside: Path,
) -> None:
    with pytest.raises(driver.DriverError):
        driver.guard_run_dir(inside)


def test_the_defaults_name_a_variant_by_its_policy() -> None:
    assert driver.variant_name("conservative", "coincide", "source") == "conservative"
    assert driver.variant_name("fewest", "pretty", "upstream") == "fewest-pretty-upstream"


@pytest.mark.pool_heavy
def test_a_child_is_killed_at_its_timeout_and_timed_alone(tmp_path: Path) -> None:
    command = [sys.executable, "-I", "-c", "import time; time.sleep(30)"]
    run = driver.run_child(command, tmp_path / "log", cwd=tmp_path, timeout=0.3)
    assert run.timed_out
    assert run.returncode is None
    assert run.wall_seconds < 10


def test_a_finished_child_reports_its_exit_status(tmp_path: Path) -> None:
    command = [sys.executable, "-I", "-c", "print('ok'); raise SystemExit(3)"]
    run = driver.run_child(command, tmp_path / "log", cwd=tmp_path, timeout=60)
    assert (run.timed_out, run.returncode) == (False, 3)
    assert (tmp_path / "log").read_text(encoding="utf-8").strip() == "ok"


def test_the_replica_is_the_vendored_tree_and_a_changed_copy_is_refused(tmp_path: Path) -> None:
    search = driver.ensure_replica(tmp_path)
    assert (search / "regularize" / driver.SHIM.name).is_file()
    assert json.loads((search / "exact/batch/results.json").read_text()) == []
    (search / "regularize" / "reg.py").write_text("# edited\n", encoding="utf-8")
    with pytest.raises(driver.DriverError):
        driver.ensure_replica(tmp_path)


def test_the_shim_refuses_an_orientation_upstream_does_not_have(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        shim.main(["--n", "5", "--orient", "9", "--out", str(tmp_path)])


# --- witness input -------------------------------------------------------------------


def test_a_rational_witness_round_trips_through_the_input_text() -> None:
    """Centres exactly where their expansion ends, else to DIGITS; the side exactly; the
    angle of a Pythagorean basis to the working precision."""
    squares = [
        {"id": 1, "center": ["1/2", "1/2"], "basis": ["1", "0"]},
        {"id": 2, "center": ["7/4", "5/3"], "basis": ["3/5", "4/5"]},
    ]
    converted = driver.witness_input(_witness(squares, "5/2", "center-basis"))
    header, rows = _rows(converted.text)
    assert header == ["2", "2.5"]
    assert rows[0] == ["0.5", "0.5", "0"]
    assert Fraction(rows[1][0]) == Fraction(7, 4)
    assert abs(Fraction(rows[1][1]) - Fraction(5, 3)) < Fraction(1, 10 ** (driver.DIGITS - 1))
    mp.mp.dps = 90
    expected = mp.degrees(mp.atan2(mp.mpf(4) / 5, mp.mpf(3) / 5))
    assert abs(mp.mpf(rows[1][2]) - expected) < mp.mpf(10) ** (2 - driver.DIGITS)
    assert converted.info["centres_exact"] is False
    assert converted.info["exact_side"] == "5/2"


def test_corners_become_exact_centres_and_the_first_edge_angle() -> None:
    corners = [["1", "0"], ["2", "0"], ["2", "1"], ["1", "1"]]
    turned = [["5/2", "1"], ["31/10", "9/5"], ["23/10", "12/5"], ["17/10", "8/5"]]
    witness = _witness(
        [{"id": 1, "corners": corners}, {"id": 2, "corners": turned}], "4", "corners"
    )
    _header, rows = _rows(driver.witness_input(witness).text)
    assert rows[0] == ["1.5", "0.5", "0"]
    assert [Fraction(rows[1][0]), Fraction(rows[1][1])] == [Fraction(12, 5), Fraction(17, 10)]
    assert abs(float(rows[1][2]) - 53.13010235415598) < 1e-12


def test_every_terminating_centre_of_a_record_witness_prints_exactly() -> None:
    """Ryan Xu's rational n = 70: centres exact, side exact, square order kept."""
    witness = driver.load_known_best(70)
    converted = driver.witness_input(witness)
    header, rows = _rows(converted.text)
    side, placed = driver.source_placed(witness)
    assert Fraction(header[1]) == side
    assert [(Fraction(x), Fraction(y)) for x, y, _ in rows] == [
        (x, y) for x, y, _c, _s in placed
    ]
    assert converted.info["centres_exact"]


def test_decimal_degrees_pass_through_as_written() -> None:
    witness = load_yaml((FIXTURES / "n-026.yaml").read_text(encoding="utf-8"))["witness"]
    _header, rows = _rows(driver.witness_input(witness).text)
    written = [driver.plain_decimal(Decimal(square["angle"])) for square in witness["squares"]]
    assert [row[2] for row in rows] == written


# --- frames, decisions, measurements -------------------------------------------------


def _forward(side: Fraction, poses: list[certificates.Pose], g: int) -> list[certificates.Pose]:
    """`reg.d4` on exact poses: ``g & 3`` quarter turns, then the mirror when ``g & 4``."""
    out = []
    for pose in poses:
        x, y, t = pose.x, pose.y, pose.t
        for _ in range(g & 3):
            x, y = side - y, x
        if g & 4:
            x, t = side - x, -t
        out.append(certificates.Pose(x, y, t))
    return out


def _fixture_certificate() -> certificates.Certificate:
    return certificates.parse(
        (FIXTURES / "n-026.cert").read_text(encoding="utf-8"), expected_n=26
    )


@pytest.mark.parametrize("g", range(8))
def test_the_inverse_undoes_each_container_symmetry_exactly(g: int) -> None:
    certificate = _fixture_certificate()
    poses = list(certificate.poses)
    mapped = _forward(certificate.side, poses, g)
    assert driver.inverse_symmetry(certificate.side, mapped, g) == poses


def _run_dir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    certificate: certificates.Certificate,
    g: int,
) -> Path:
    variant = tmp_path / "regularize" / "conservative"
    variant.mkdir(parents=True)
    (variant / "n-026.cert").write_text(certificates.serialize(certificate), encoding="utf-8")
    record = json.loads((FIXTURES / "n-026.json").read_text(encoding="utf-8"))
    record["orientation_g"] = g
    (variant / "n-026.json").write_text(json.dumps(record), encoding="utf-8")
    known_best = tmp_path / "known-best"
    known_best.mkdir()
    shutil.copyfile(FIXTURES / "n-026.yaml", known_best / "n-026.yaml")
    monkeypatch.setattr(driver, "KNOWN_BEST", known_best)
    monkeypatch.setattr(driver, "verified_bound", lambda _n: dict(BOUND_26))
    monkeypatch.setattr(driver, "_same_side_module", lambda: None)
    return tmp_path


def test_the_fixture_is_decided_measured_and_classified(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_dir = _run_dir(tmp_path, monkeypatch, _fixture_certificate(), 0)
    row = driver.import_one((26, str(run_dir), "conservative"))
    assert row["decision"]["both"]
    identity = row["identity"]
    assert (identity["one_to_one"], identity["order_preserved"]) == (True, True)
    assert identity["best_symmetry"] == 0
    assert identity["visible_moved_ids"] == [9]
    assert abs(identity["max_move"] - 0.31066017177982) < 1e-9
    assert row["shades"]["house"]["light_before"] - row["shades"]["house"]["light_after"] == 1
    assert row["shades"]["regressions"]["stage"]["count"] == 0
    assert row["side"]["relation_to_witness"] == "above"
    assert row["side"]["relation_to_verified"] == {
        "relation": "above",
        "difference": pytest.approx(5.6213e-20, rel=1e-3),
        "by": "exact form",
    }
    assert row["same_side"]["status"] == "not attempted"
    assert row["classification"] == "solved"
    assert row["decision"]["area"]
    assert row["identity"]["unnamed_turn_ids"] == []
    assert (row["policy"]["certificate"]["row"], row["policy"]["same_side"]["row"]) == (4, 1)
    assert row["policy"]["drawing"]["record"] == "refused, dilated-side"
    view = load_yaml((run_dir / row["view"]).read_text(encoding="utf-8"))["witness"]
    assert view["certificate"]["label"] == "regularized"
    assert [square["id"] for square in view["squares"]] == list(range(1, 27))


def test_a_refitted_orientation_is_undone_before_measuring(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = _fixture_certificate()
    turned = certificates.Certificate(
        26, certificate.side, tuple(_forward(certificate.side, list(certificate.poses), 3))
    )
    row = driver.import_one(
        (26, str(_run_dir(tmp_path, monkeypatch, turned, 3)), "conservative")
    )
    assert row["isometry"]["inverse_applied"]
    assert row["identity"]["order_preserved"]
    assert row["identity"]["visible_moved_ids"] == [9]
    assert row["classification"] == "solved"


# --- the side relation ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("form", "expected"),
    [
        ("3 + (1/2)sqrt(2)", driver.Surd(Fraction(3), Fraction(1, 2), 2)),
        ("(16+5*sqrt(2))/3", driver.Surd(Fraction(16, 3), Fraction(5, 3), 2)),
        ("(11/2) + 3 sqrt(2)", driver.Surd(Fraction(11, 2), Fraction(3), 2)),
        ("(7/2) + (1/2)sqrt(7)", driver.Surd(Fraction(7, 2), Fraction(1, 2), 7)),
        ("88809603717088809603717/10000000000000000000000", None),
        ("root(P_trump11, 3.87708359002281417730789706010096)", None),
    ],
)
def test_register_exact_forms_parse_as_surds(form: str, expected: driver.Surd | None) -> None:
    parsed = driver.parse_surd(form)
    if expected is None and "root" in form:
        assert parsed is None
    elif expected is None:
        assert parsed == driver.Surd(Fraction(form))
    else:
        assert parsed == expected


def test_the_side_is_compared_exactly_with_a_surd() -> None:
    root_two = Fraction(Decimal("1.41421356237309504880168872420969807856967187537694"))
    near = 3 + root_two / 2
    tiny = Fraction(1, 10**45)
    form = "3 + (1/2)sqrt(2)"
    assert driver.compare_to(near + tiny, None, form)["relation"] == "above"
    assert driver.compare_to(near - tiny, None, form)["relation"] == "below"
    assert driver.compare_to(Fraction(3), None, "3")["relation"] == "equal"
    assert driver.surd_sign(Fraction(-1), driver.Surd(Fraction(0), Fraction(-1), 2)) == 1


def test_a_symbolic_form_falls_back_to_the_printed_value() -> None:
    form = "root(P_trump11, 3.87708359002281417730789706010096)"
    value = "3.87708359002281417730789706010096"
    above = Fraction(value) + Fraction(1, 10**20)
    assert driver.compare_to(above, value, form) == {
        "relation": "above",
        "difference": pytest.approx(1e-20),
        "by": "printed value",
    }
    within = Fraction(value) + Fraction(1, 10**34)
    assert driver.compare_to(within, value, form)["relation"] == "within-printed-precision"


# --- refusals and classification -----------------------------------------------------


def test_a_count_without_a_certificate_is_refused_with_the_solve_status(tmp_path: Path) -> None:
    driver.write_json(
        driver.exact_receipt_path(tmp_path), {"rows": [{"n": 261, "status": "timeout"}]}
    )
    row = driver.import_one((261, str(tmp_path), "conservative"))
    assert (row["classification"], row["reasons"]) == ("refused", ["exact solve: timeout"])


def test_an_overlapping_certificate_is_refused_on_every_route(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = _fixture_certificate()
    poses = list(certificate.poses)
    poses[0] = certificates.Pose(poses[1].x, poses[1].y, poses[0].t)
    broken = certificates.Certificate(26, certificate.side, tuple(poses))
    row = driver.import_one(
        (26, str(_run_dir(tmp_path, monkeypatch, broken, 0)), "conservative")
    )
    assert row["classification"] == "refused"
    assert row["reasons"][0] == "not exactly a packing on exact_verify, independent, area"
    assert row["policy"]["certificate"]["row"] == 2


def _measured_row(*, fell: int = 0, relation: str = "above") -> dict[str, Any]:
    clean = {
        "one_to_one": True,
        "order_preserved": True,
        "max_move": 0.1,
        "moved": {"0.001": 1},
    }
    shades = {"regressions": {"house": {"count": 0}, "stage": {"count": fell}}}
    return {
        "decision": {"exact_verify": True, "independent": True, "area": True},
        "identity": clean,
        "shades": shades,
        "side": {
            "relation": "solved",
            "relation_to_witness": "above",
            "view_minus_witness": 5e-20,
            "relation_to_verified": {"relation": relation, "difference": 5e-20},
        },
        "same_side": {"status": "not attempted"},
        "generator": {"policy": "conservative", "level": 2, "determined_merges": []},
    }


def _same_side(
    *, relation: str, difference: float, to_verified: str = "below"
) -> dict[str, Any]:
    return {
        "status": "same",
        "decision": {"exact_verify": True, "independent": True, "area": True},
        "identity": {
            "one_to_one": True,
            "order_preserved": True,
            "max_move": 0.2,
            "moved": {"0.001": 3},
        },
        "shades": {"regressions": {"house": {"count": 0}, "stage": {"count": 0}}},
        "pose_equals_witness": False,
        "side": {
            "relation": "same" if relation == "same" else "solved",
            "relation_to_witness": relation,
            "view_minus_witness": difference,
            "relation_to_verified": {"relation": to_verified},
        },
    }


def test_a_view_that_loses_contacts_is_refused() -> None:
    row = driver.classify(_measured_row(fell=2))
    assert (row["classification"], row["reasons"]) == (
        "refused",
        ["contact counts fell: {'stage': 2}"],
    )


@pytest.mark.parametrize(
    ("relation", "words"), [("below", "register result"), ("above", "not a drawing frame")]
)
def test_a_dilated_view_is_solved_with_what_its_side_means(relation: str, words: str) -> None:
    row = driver.classify(_measured_row(relation=relation))
    assert row["classification"] == "solved"
    assert words in row["admission"]


def test_a_drawable_same_side_resolve_makes_the_view_same() -> None:
    row = _measured_row(fell=1)
    row["same_side"] = _same_side(relation="same", difference=0.0)
    classified = driver.classify(row)
    assert classified["classification"] == "same"
    assert classified["certificate_reasons"] == ["contact counts fell: {'stage': 1}"]
    assert "new verified upper bound" in classified["admission"]


def test_a_resolve_above_the_printed_side_is_not_the_same_side() -> None:
    """A decimal witness's 36-digit frame can sit above its printed side (n = 11)."""
    row = _measured_row()
    row["same_side"] = _same_side(relation="above", difference=3.7e-33)
    classified = driver.classify(row)
    assert classified["classification"] == "solved"
    assert "above its printed side" in classified["same_side"]["reasons"][0]


def test_the_same_side_adapter_relaxes_and_records_the_module_summary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Outcome:
        def __init__(self, summary: dict[str, Any], witness: dict[str, Any] | None) -> None:
            self.payload = summary
            self.resolved = types.SimpleNamespace(witness=witness) if witness else None

        def summary(self) -> dict[str, Any]:
            return self.payload

    calls: list[tuple[str, Any]] = []

    def resolve_view(
        _witness: Any, _view: Any, *, on_conflict: str, verified_bound: Any
    ) -> Outcome:
        calls.append((on_conflict, verified_bound))
        relaxed = [{"certificate": [1, 2], "forced_gap_decimal": "-1.5e-36"}]
        found = {
            "status": "same-side",
            "relaxed": relaxed,
            "max_move": "2.0e-33",
            "side_basis": {
                "side_minus_printed_decimal": "0.000e+00",
                "fits_printed_side": True,
            },
            "register": {"below_verified_bound": False},
        }
        return Outcome(found, {"side": "1"})

    stub = types.ModuleType("stub_same_side")
    stub.resolve_view = resolve_view  # pyright: ignore[reportAttributeAccessIssue]
    stub.evand_view = lambda record: record["packing"]  # pyright: ignore[reportAttributeAccessIssue]
    monkeypatch.setattr(driver, "_same_side_module", lambda: stub)
    monkeypatch.setattr(
        driver, "verified_bound", lambda _n: {"exact_form": "7/2", "value": "3.5"}
    )
    summary, witness = driver.same_side(26, {}, {"packing": []})
    assert calls == [("relax", Fraction(7, 2))]
    assert (summary["status"], witness) == ("same", {"side": "1"})
    assert summary["result"]["relaxed"] == [
        {"certificate": 2, "forced_gap_decimal": "-1.5e-36"}
    ]
    fields = summary["fields"]
    assert (fields["relaxed_count"], fields["relaxed_largest_gap"]) == (1, 1.5e-36)
    assert (fields["fits_printed_side"], fields["below_verified_bound"]) == (True, False)


# --- the policy's decision table -----------------------------------------------------


def _same_side_row(**changes: Any) -> dict[str, Any]:
    row = _measured_row()
    row["same_side"] = _same_side(relation="same", difference=0.0, to_verified="above")
    for path, value in changes.items():
        target = row["same_side"]
        *parents, leaf = path.split("__")
        for parent in parents:
            target = target[parent]
        target[leaf] = value
    return driver.policy(driver.classify(row))["same_side"]


@pytest.mark.parametrize(
    ("changes", "expected", "report"),
    [
        ({"status": "refused"}, 1, "no view"),
        ({"decision__area": False}, 2, "refused"),
        (
            {"side__relation_to_verified": {"relation": "below", "difference": -1e-15}},
            3,
            "held",
        ),
        ({"pose_equals_witness": True}, 5, "no change"),
        ({"identity__one_to_one": False}, 6, "refused"),
        ({"identity__unnamed_turn_ids": [7]}, 6, "refused"),
        ({"shades__regressions": {"house": {"count": 1}, "stage": {"count": 0}}}, 7, "refused"),
        ({"identity__max_move": 0.6}, 9, "review"),
        ({}, 10, "admitted"),
    ],
)
def test_each_outcome_falls_in_its_row_and_is_reported_in_its_word(
    changes: dict[str, Any], expected: int, report: str
) -> None:
    entry = _same_side_row(**changes)
    assert (entry["row"], entry["report"]) == (expected, report)


def test_a_view_that_draws_the_same_picture_is_no_change_whatever_its_row() -> None:
    entry = _same_side_row(
        identity__moved={"0.001": 0},
        side__relation_to_verified={"relation": "below", "difference": -1e-15},
    )
    assert (entry["row"], entry["report"]) == (3, "no change")
    assert "register-result candidate" in entry["reason"]


def test_a_dilated_certificate_is_held_and_a_determined_merge_an_alternate() -> None:
    row = _measured_row()
    certificate = driver.policy(driver.classify(row))["certificate"]
    assert (certificate["row"], certificate["report"]) == (4, "held")
    assert "a side the record does not hold" in certificate["reason"]
    row = _measured_row()
    row["same_side"] = _same_side(relation="same", difference=0.0, to_verified="equal")
    row["generator"]["determined_merges"] = [["determined-merge", 1.0, 2.0, 1]]
    assert driver.policy(driver.classify(row))["report"] == "alternate"


def _square_at(degrees: str) -> driver.Placed:
    mp.mp.dps = 60
    turn = mp.radians(mp.mpf(degrees))
    cosine, sine = driver.fraction_of_mp(mp.cos(turn)), driver.fraction_of_mp(mp.sin(turn))
    return (Fraction(0), Fraction(0), cosine, sine)


def test_a_turn_is_named_only_by_the_recorded_angle_changes() -> None:
    source = [_square_at("10"), _square_at("20"), _square_at("0.5"), _square_at("30")]
    view = [_square_at("12"), _square_at("21"), _square_at("0"), _square_at("33")]
    record = {
        "angle_changes": [
            ["free-angle", 10.0, 11.0, 1],
            ["free-angle", 11.0, 12.0, 1],
            ["free-angle straighten", 1, 1],
        ],
        "free_merges": [[1, 20.0, 21.0]],
    }
    ids = ["a", "b", "c", "d"]
    assert driver.unnamed_turns(view, source, record, ids) == (["d"], [])
    solved = [10.0, 20.0, 0.5, 33.0]
    assert driver.unnamed_turns(view, source, record, ids, solved) == ([], ["d"])


def test_a_root_form_is_compared_exactly_with_its_stated_polynomial() -> None:
    polynomial = "s^2 - 2 = 0"
    printed = "1.41421356237309504880168872420969807857"
    form = f"root(P, {printed})"
    near = Fraction(printed)
    assert driver.parse_polynomial(polynomial) == [Fraction(1), Fraction(0), Fraction(-2)]
    tiny = Fraction(1, 10**38)
    assert driver.compare_to(near + tiny, printed, form, polynomial)["relation"] == "above"
    assert driver.compare_to(near - tiny, printed, form, polynomial)["relation"] == "below"
