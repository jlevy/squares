"""The weighted-atom source replay reproduces the retained charges, and refuses what it should.

`devtools.replay_weighted_atom_source` is the independent half of a pair. The declared token
total, budget, charge and charged-placement list come from `devtools.plateau_reader`'s own
`WeightedPoint` path; the replay rebuilds the atom as a production `ThresholdAtom` and derives
all of them again from the family's exact placement geometry. These tests hold it to the four
retained receipts, then mutate each declared figure in turn to show the comparison is load
bearing rather than decorative -- a replay that cannot fail confirms nothing.

The coordinates involved are exact rationals up to about 965 characters wide, so this is also
where the model's exactness meets real retained data.
"""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import replay_weighted_atom_source as replay
from sqpack.fractional import ceiling

PACKING = Path(ceiling.__file__).resolve().parents[3]
RESULTS = (
    PACKING
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "agenda-034"
)

#: Every retained receipt that declares the seven-token, threshold-four charge, with the
#: family it was written against and the number of placements it charges. The second and
#: third families are byte-identical, so this is four receipts over three distinct families.
PAIRS = (
    ("lane-a6-loop-reader-2.json", "lane-a6-loop-family-2.json", (2, 2, 1, 1, 1), 8),
    (
        "lane-a6-reader-saturated-symmetric.json",
        "lane-a6-saturated-symmetric-153-40.json",
        (1, 2, 2, 1, 1),
        10,
    ),
    ("lane-a6-loop-reader-1.json", "lane-a6-loop-family-1.json", (1, 2, 2, 1, 1), 10),
    (
        "lane-a6-reader-saturated-153-40.json",
        "lane-a6-saturated-family-at-n-1-exact25.json",
        (2, 2, 1, 1, 1),
        5,
    ),
)

PRIMARY = PAIRS[0]


@pytest.mark.parametrize(
    ("reader", "family", "multiplicities", "charged"),
    PAIRS,
    ids=[pair[0].removeprefix("lane-a6-").removesuffix(".json") for pair in PAIRS],
)
def test_every_retained_receipt_reproduces_exactly(
    reader: str, family: str, multiplicities: tuple[int, ...], charged: int
) -> None:
    receipt = replay.replay(RESULTS / reader, RESULTS / family)
    atom = receipt["replay"]["atom"]
    assert receipt["replay"]["disagreements"] == []
    assert receipt["replay"]["reproduced"] is True
    assert tuple(atom["multiplicities"]) == multiplicities
    assert (atom["site_count"], atom["token_count"]) == (5, 7)
    assert (atom["threshold"], atom["budget"]) == (4, 1)
    assert atom["threshold_charge"] == "3/2"
    assert atom["violation"] == "1/2"
    assert len(atom["charged_placements"]) == charged
    # The replay says what it has not decided; neither obligation may quietly read as done.
    assert receipt["ceiling_proof"]["checked"] is False
    assert receipt["scientific_target"]["run"] is False


def test_the_charge_is_above_the_budget_which_is_why_the_motif_was_retained() -> None:
    receipt = replay.replay(RESULTS / PRIMARY[0], RESULTS / PRIMARY[1])
    atom = receipt["replay"]["atom"]
    assert Fraction(atom["threshold_charge"]) > atom["budget"]


def test_both_inputs_are_digest_bound_because_nothing_retained_binds_them() -> None:
    """The receipts name a scratch path that is gone, so content is the only binding left."""

    receipt = replay.replay(RESULTS / PRIMARY[0], RESULTS / PRIMARY[1])
    for side in ("reader", "family"):
        digest = receipt["replay"][side]["sha256"]
        assert len(digest) == 64
        assert set(digest) <= set("0123456789abcdef")
    assert receipt["replay"]["reader"]["sha256"] != receipt["replay"]["family"]["sha256"]


def _mutated(tmp_path: Path, **changes: Any) -> Path:
    """The primary receipt with its declared atom fields overwritten."""

    record = json.loads((RESULTS / PRIMARY[0]).read_text(encoding="utf-8"))
    atom = record["k5_cliques"]["atom"]
    for key, value in changes.items():
        atom[key] = value
    path = tmp_path / "mutated-reader.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        pytest.param({"threshold_charge": "5/4"}, "exact threshold charge 3/2", id="charge"),
        pytest.param({"budget": 2}, "exact budget 1", id="budget"),
        pytest.param({"size": 5}, "exact token total 7", id="token-total"),
        pytest.param(
            {"charged_placements": [11, 14, 16, 21, 26, 28, 35]},
            "exact charged placements",
            id="charged-list",
        ),
    ],
)
def test_a_mutated_declaration_is_caught_rather_than_echoed(
    tmp_path: Path, changes: dict[str, Any], expected: str
) -> None:
    receipt = replay.replay(_mutated(tmp_path, **changes), RESULTS / PRIMARY[1])
    assert receipt["replay"]["reproduced"] is False
    assert any(expected in problem for problem in receipt["replay"]["disagreements"])


def test_a_mutated_threshold_is_caught_through_the_budget_it_implies(tmp_path: Path) -> None:
    """The threshold is an input to the rebuild, so the figures depending on it catch it."""

    receipt = replay.replay(_mutated(tmp_path, threshold=3), RESULTS / PRIMARY[1])
    assert receipt["replay"]["reproduced"] is False
    assert receipt["replay"]["atom"]["budget"] == 2
    assert any("exact budget 2" in problem for problem in receipt["replay"]["disagreements"])


def test_dropping_a_token_count_changes_the_charge_and_is_caught(tmp_path: Path) -> None:
    """The understated-budget mutation, on real data: a heavy site read as light."""

    record = json.loads((RESULTS / PRIMARY[0]).read_text(encoding="utf-8"))
    atom = record["k5_cliques"]["atom"]
    atom["points"][0]["multiplicity"] = 1
    path = tmp_path / "light-reader.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    receipt = replay.replay(path, RESULTS / PRIMARY[1])
    assert receipt["replay"]["reproduced"] is False
    # Six tokens still floor to a budget of one, so the budget alone would not have caught
    # it; the charge is what moves, which is why every figure is compared and not just one.
    assert receipt["replay"]["atom"]["token_count"] == 6
    assert any("token total" in problem for problem in receipt["replay"]["disagreements"])


def test_a_receipt_of_another_kind_is_refused_rather_than_read(tmp_path: Path) -> None:
    record = json.loads((RESULTS / PRIMARY[0]).read_text(encoding="utf-8"))
    record["kind"] = "plateau-reader/v2"
    path = tmp_path / "wrong-kind.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(replay.ReplayError, match="receipt kind is"):
        replay.replay(path, RESULTS / PRIMARY[1])


def test_a_family_the_receipt_was_not_written_against_is_reported() -> None:
    """The 56-placement receipt against the 37-placement family: the only binding retained."""

    receipt = replay.replay(
        RESULTS / PRIMARY[0], RESULTS / "lane-a6-saturated-family-at-n-1-exact25.json"
    )
    assert receipt["replay"]["reproduced"] is False
    assert any("was written against" in p for p in receipt["replay"]["disagreements"])


def test_a_family_whose_declared_total_does_not_match_its_placements_is_reported(
    tmp_path: Path,
) -> None:
    record = json.loads((RESULTS / PRIMARY[1]).read_text(encoding="utf-8"))
    record["total_weight"] = "12"
    path = tmp_path / "bad-total.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    receipt = replay.replay(RESULTS / PRIMARY[0], path)
    assert receipt["replay"]["reproduced"] is False
    assert any("total_weight" in problem for problem in receipt["replay"]["disagreements"])


def test_a_float_coordinate_cannot_enter_a_charge(tmp_path: Path) -> None:
    """A JSON float parses to an exact base-ten rational, never to a binary64 value."""

    record = json.loads((RESULTS / PRIMARY[0]).read_text(encoding="utf-8"))
    atom = record["k5_cliques"]["atom"]
    atom["points"] = deepcopy(atom["points"])
    atom["points"][4]["y"] = 1.9125
    path = tmp_path / "float-site.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    receipt = replay.replay(path, RESULTS / PRIMARY[1])
    # 153/80 is exactly 1.9125, so the replay still reproduces: the decimal was read as the
    # rational it spells, not rounded through a float.
    assert receipt["replay"]["reproduced"] is True


def test_the_command_line_separates_a_disagreement_from_an_unreadable_input(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert replay.main([str(RESULTS / PRIMARY[0]), str(RESULTS / PRIMARY[1])]) == 0
    assert json.loads(capsys.readouterr().out)["replay"]["reproduced"] is True

    mutated = _mutated(tmp_path, threshold_charge="5/4")
    assert replay.main([str(mutated), str(RESULTS / PRIMARY[1])]) == 1
    assert json.loads(capsys.readouterr().out)["replay"]["reproduced"] is False

    assert replay.main([str(tmp_path / "absent.json"), str(RESULTS / PRIMARY[1])]) == 2
    assert "cannot read" in json.loads(capsys.readouterr().err)["error"]
