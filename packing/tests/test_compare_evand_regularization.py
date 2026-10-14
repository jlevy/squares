"""The regularization cross-tabulation counts what its inputs hold and refuses the rest."""

from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path
from typing import Any

import mpmath as mp
import pytest

from devtools import compare_evand_regularization as compare


def _pick(n: int, level: int, **extra: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "n": n,
        "level": level,
        "variant": "conservative",
        "orientation_g": 0,
        "groups": "2 -> 2",
        "symmetry": [],
        "input": "exact batch (register witness)",
    }
    row.update(extra)
    return row


def _entry(n: int, status: str) -> dict[str, Any]:
    entry: dict[str, Any] = {"n": n, "status": status}
    if status == "refused":
        entry["refusal"] = {"kind": "promotion-overlap"}
    return entry


def _index(statuses: dict[int, str]) -> dict[str, Any]:
    entries = [_entry(n, status) for n, status in statuses.items()]
    counted: dict[str, int] = {}
    for status in statuses.values():
        counted[status] = counted.get(status, 0) + 1
    return {
        "contract": compare.INDEX_CONTRACT,
        "entries": entries,
        "totals": {
            "records": len(entries),
            "statuses": counted,
            "refusals": {"promotion-overlap": counted["refused"]}
            if "refused" in counted
            else {},
        },
    }


SMALL_BEST = [
    _pick(1, 0, symmetry=[1, 2, 3, 4, 5, 6, 7], groups="1 -> 1"),
    _pick(2, 2, groups="4 -> 2", orientation_g=3),
    _pick(3, 1, variant="fewest", groups="3 -> 2", input="store best (refreshed)"),
    _pick(4, 0),
    _pick(5, 2, symmetry=[4]),
]
SMALL_INDEX = {1: "unchanged", 2: "regularized", 3: "refused", 4: "refused", 5: "unchanged"}


def test_crosstab_counts_each_side_and_their_overlap() -> None:
    result = compare.crosstab(
        compare.read_best(SMALL_BEST), compare.read_index(_index(SMALL_INDEX))
    )
    upstream = result["upstream"]
    assert upstream["levels"] == {"0": 2, "1": 1, "2": 2, "3": 0}
    assert upstream["changed"] == 3
    assert upstream["variants"] == {"conservative": 4, "fewest": 1}
    assert upstream["fewest_counts"] == [3]
    assert (upstream["orientation_kept"], upstream["orientation_changed"]) == (4, 1)
    assert upstream["inputs"] == {
        "exact batch (register witness)": 4,
        "store best (refreshed)": 1,
    }
    assert (upstream["rotation_groups_before"], upstream["rotation_groups_after"]) == (12, 9)
    assert upstream["fewer_groups_at"] == 2
    assert upstream["symmetry_imposed_at"] == 2
    assert result["project"] == {"regularized": 1, "unchanged": 2, "refused": 2}
    assert result["status_by_upstream_level"] == {
        "regularized/2": 1,
        "unchanged/0": 1,
        "unchanged/2": 1,
        "refused/0": 1,
        "refused/1": 1,
    }
    assert result["project_changed_also_changed_upstream"] == 1
    assert result["project_changed_unchanged_upstream"] == []
    assert result["refused_changed_upstream"] == 1
    assert result["refused_unchanged_upstream"] == [4]
    assert result["unchanged_changed_upstream"] == [5]
    assert result["upstream_changes_beyond_project"] == 2


def _committed_totals() -> dict[str, Any]:
    """The committed index's own totals, which move with every merge of main's records."""
    return json.loads(compare.INDEX.read_text(encoding="utf-8"))["totals"]


def _axis_refused() -> int:
    """The axis tool's own refusals: since v2 another generator's view may be drawn where
    the axis tool refused, so the index's totals, which count what is drawn, can be fewer."""
    return sum(entry["status"] == "refused" for entry in compare.load_index().values())


def test_the_committed_index_recounts_to_its_totals() -> None:
    # load_index refuses an index whose drawn entries do not recount to its totals; what
    # is asserted here holds at any index, not the counts of one merge.
    index = compare.load_index()
    totals = _committed_totals()
    statuses = [entry["status"] for entry in index.values()]
    assert sorted(index) == list(range(1, 325))
    assert set(statuses) <= set(compare.STATUSES)
    assert totals["records"] == 324
    assert sum(totals["statuses"].values()) == 324
    assert sum(totals["refusals"].values()) == totals["statuses"]["refused"]
    # A drawn view of another generator replaces only a record the axis tool refused or
    # drew, never adds a refusal.
    assert _axis_refused() >= totals["statuses"]["refused"]


def test_an_index_that_disagrees_with_its_totals_is_refused() -> None:
    document = _index(SMALL_INDEX)
    wrong = copy.deepcopy(document)
    wrong["totals"]["statuses"]["refused"] = 3
    with pytest.raises(compare.InputRefusedError, match="recount"):
        compare.read_index(wrong)
    repeated = copy.deepcopy(document)
    repeated["entries"][1]["n"] = 1
    with pytest.raises(compare.InputRefusedError, match="more than once"):
        compare.read_index(repeated)
    foreign = copy.deepcopy(document)
    foreign["contract"] = "packing.squares:Something/v1"
    with pytest.raises(compare.InputRefusedError, match="contract"):
        compare.read_index(foreign)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"level": 4}, "level"),
        ({"groups": "2 to 2"}, "groups"),
        ({"orientation_g": 8}, "orientation_g"),
        ({"symmetry": [0]}, "symmetry"),
        ({"n": 1}, "more than once"),
    ],
)
def test_a_list_row_the_tallies_cannot_read_is_refused(
    change: dict[str, Any], message: str
) -> None:
    rows = copy.deepcopy(SMALL_BEST)
    rows[1].update(change)
    with pytest.raises(compare.InputRefusedError, match=message):
        compare.read_best(rows)


def test_inputs_over_different_counts_are_refused() -> None:
    with pytest.raises(compare.InputRefusedError, match="different counts"):
        compare.crosstab(
            compare.read_best(SMALL_BEST[:-1]), compare.read_index(_index(SMALL_INDEX))
        )


@pytest.mark.parametrize(
    ("degrees", "folded"),
    [(0, 0), (45, 45), (-45, 45), (90, 0), (135, 45), (49.5, -40.5), (-0.25, -0.25)],
)
def test_fold_maps_a_rotation_into_the_half_open_quarter(degrees: float, folded: float) -> None:
    assert compare.fold_degrees(mp.mpf(degrees)) == mp.mpf(folded)


def test_a_tilt_near_but_not_at_a_class_angle_is_refused() -> None:
    assert compare.tilt_class(mp.mpf("45") - mp.mpf("1e-20"), "here") == "45"
    assert compare.tilt_class(mp.mpf("1e-20"), "here") == "axis"
    assert compare.tilt_class(mp.mpf("0.0057"), "here") == "other"
    with pytest.raises(compare.InputRefusedError, match="neither"):
        compare.tilt_class(mp.mpf("45") - mp.mpf("1e-9"), "here")
    assert compare.record_class(["axis", "axis"]) == "axis-only"
    assert compare.record_class(["axis", "45"]) == "all-45"
    assert compare.record_class(["45", "other", "axis"]) == "other-tilt"


def test_the_refused_records_split_by_their_witness_tilts() -> None:
    result = compare.refused_tilts(compare.load_index())
    counts, records = result["counts"], result["records"]
    assert set(counts) == {"all-45", "other-tilt", "axis-only"}
    assert {kind: len(members) for kind, members in records.items()} == counts
    assert sum(counts.values()) == result["refused"] == _axis_refused()
    # Every refused record holds a tilted square.
    assert counts["axis-only"] == 0
    # n = 51's witness is exact over Q(sqrt 2), with 17 squares at 45 degrees.
    assert {5, 10, 19, 27, 51} <= set(records["all-45"])
    assert {11, 17, 18} <= set(records["other-tilt"])
    tilts = result["other_tilts_degrees"]
    assert tilts["11"] == ["40.1819"]
    assert tilts["17"] == ["36.6238", "39.805"]
    assert tilts["18"] == ["24.2952"]


def test_certificate_angles_read_each_rotation_exactly(tmp_path: Path) -> None:
    t_45 = "2588834764831844055010554526310613/6250000000000000000000000000000000"
    text = f"# a comment line\n3 5\n1/2 1/2 0\n3/2 1/2 -1/20000\n5/2 5/2 {t_45}\n"
    plain = tmp_path / "n-3.cert"
    plain.write_text(text, encoding="utf-8")
    packed = tmp_path / "n-3.cert.gz"
    packed.write_bytes(gzip.compress(text.encode("utf-8")))
    for path in (plain, packed):
        result = compare.certificate_angles(path)
        assert result["n"] == 3
        assert [row["class"] for row in result["squares"]] == ["axis", "other", "45"]
        assert result["squares"][1]["rotation_degrees"] == "-0.0057295779"
        # A rational t just above tan(22.5 degrees) is a rotation just past 45.
        assert result["squares"][2]["folded_degrees"] == "-45.0"


def test_the_command_exits_two_on_a_refused_input(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    best = tmp_path / "best.json"
    best.write_text(json.dumps([_pick(1, 9)]), encoding="utf-8")
    assert compare.main(["crosstab", "--best", str(best)]) == 2
    assert "refused: n = 1: level 9" in capsys.readouterr().err


def test_the_crosstab_defaults_to_the_vendored_lists(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """With no `--best`, the upstream side is the vendored copy at its pin.

    Only the upstream tallies are asserted: they are a function of the vendored bytes,
    which `devtools.check_vendored_evand` holds to the manifest's upstream digests, and
    they are the figures the regularization assessment's appendix states. The project
    side moves with the regularized layer and is not pinned here.
    """
    assert compare.VENDORED_BEST.is_file()
    assert compare.main(["crosstab", "--json"]) == 0
    upstream = json.loads(capsys.readouterr().out)["upstream"]
    assert upstream["levels"] == {"0": 177, "1": 30, "2": 117, "3": 0}
    assert upstream["variants"] == {"conservative": 310, "fewest": 14}
    assert (upstream["orientation_kept"], upstream["orientation_changed"]) == (276, 48)
    assert (upstream["rotation_groups_before"], upstream["rotation_groups_after"]) == (
        2400,
        1172,
    )
    assert upstream["symmetry_imposed_at"] == 101
