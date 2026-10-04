"""The regularizer on fixtures small enough to be checked by hand.

Synthetic witnesses, each built so the exact answer is known before the tool runs: a row
with slack that compacts into the wall and each other, a block one part in ten to the
thirteenth off its lattice that snaps onto it, and a square whose slide would run into a
tilted neighbour and so must stop short and be refused. Two more hold the neighbour
non-regression rule: a slide that costs a tilted neighbour its stage contact, and one
that costs an aligned neighbour its exact house contact while the stage's coarser gap
still counts it; each must be undone. The command is held to its boundary (it never
writes under `witnesses/` or `atlas/`), and the atlas layer's three modes are run on a
scratch tree of three records: one regularized, one unchanged and one refused.
"""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.regularize_axis_components import (
    ALGORITHM,
    RATIONAL_DIGITS,
    ROOT,
    SMALLEST_DILATION,
    SNAP_TOLERANCE,
    STAGE_GAP,
    WITNESS_SCHEMA,
    AtlasLayout,
    RegularizeError,
    axis_square,
    centre,
    check_atlas,
    house_count_of,
    house_partners,
    interior_overlap_interval,
    lattice_target,
    main,
    promotion_dilations,
    regularize,
    slide_limit,
    stage_contacts,
    stage_count_of,
)
from devtools.upper_bound_packets import MAX_SIDE_INCREASE
from sqpack.witness import exact_verify, load_witness, promote_rational, witness_document

HALF = Fraction(1, 2)


def decimal_witness(
    squares: list[tuple[str, str, str]], side: str, *, name: str = "fixture"
) -> dict[str, Any]:
    """A decimal centre-angle Witness/v2 record, the kind every Couzo witness is."""
    return {
        "id": f"W-{name}",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "radians",
        },
        "squares": [
            {"id": index, "center": [x, y], "angle": angle}
            for index, (x, y, angle) in enumerate(squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "numerically-checked",
            "method": "numerical-f64",
            "precision": {"binary_bits": 53, "rounding": "nearest-even"},
            "tolerance": "1e-9",
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic"},
    }


def corner_witness(
    squares: list[list[tuple[str, str]]], side: str, *, kind: str, name: str
) -> dict[str, Any]:
    """A corner-form Witness/v2 record: rational as the exact grids are, or decimal as the
    one digitized record is."""
    exact = kind == "rational"
    return {
        "id": f"W-{name}",
        "n": len(squares),
        "side": side,
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": kind},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": index, "corners": [list(point) for point in corners]}
            for index, corners in enumerate(squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "verified" if exact else "numerically-checked",
            "method": "exact-algebraic" if exact else "numerical-multiprecision",
            **(
                {}
                if exact
                else {
                    "precision": {"decimal_digits": 120, "rounding": "nearest"},
                    "tolerance": "2e-6",
                }
            ),
            "limitations": "synthetic fixture",
        },
        "source": {"path": "tests/synthetic"},
        **(
            {"certificate": {"kind": "exact-rational-sat", "replay": "synthetic"}}
            if exact
            else {}
        ),
    }


def write_witness(path: Path, witness: dict[str, Any]) -> Path:
    path.write_text(witness_document(witness, schema=str(WITNESS_SCHEMA)), encoding="utf-8")
    return path


def view_centres(view: dict[str, Any]) -> list[tuple[Fraction, Fraction]]:
    return [
        centre([(Fraction(x), Fraction(y)) for x, y in s["corners"]]) for s in view["squares"]
    ]


# A square pinned in a container's top-right corner, so the exact frame's side is exactly
# the declared one and the right-wall lattice sits at side - 1/2, not a hair below it.
PIN_3 = ("2.5", "2.5", "0")
PIN_4 = ("3.5", "3.5", "0")
# A square pinned in the top-left corner, so the exact frame's left wall stays at zero:
# the promotion translates a pose to its bounding box, and without it a row seated a
# little off the left wall would be carried onto it before any slide.
LEFT_3 = ("0.5", "2.5", "0")
LEFT_4 = ("0.5", "3.5", "0")


def test_a_row_with_slack_compacts_into_the_wall_and_each_other() -> None:
    """Three squares drift 0.03, 0.06 and 0.09 right of their slots; all three come home."""
    witness = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), ("2.59", "0.5", "0"), PIN_4], "4"
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    assert view_centres(view)[:3] == [
        (HALF, HALF),
        (Fraction(3, 2), HALF),
        (Fraction(5, 2), HALF),
    ]
    assert view["side"] == "4"
    assert report["exact_verification"]["repository_verifier"]["valid"] is True
    # Before: only the bottom wall counts for each (0.03 is three gaps).  After: the
    # first touches the left wall, the bottom and its neighbour; the last has a hole on
    # its right, half a side short of the far wall's lattice.
    assert report["contacts"]["stage"]["histogram_before"][1] == 3
    assert [s["stage"][1] for s in report["squares"][:3]] == [3, 3, 2]
    # The house rule agrees here: every contact the stage counts is exact.
    assert [s["house"][1] for s in report["squares"][:3]] == [3, 3, 2]
    assert report["contacts"]["house"]["became_lighter"] == 0
    assert report["squares"][2]["light_faces"] == {"right": "hole", "top": "hole"}
    assert report["regularization"]["moves"]["compactions"] == 3
    assert report["regularization"]["moves"]["converged"] is True
    assert report["regularization"]["exact_contacts_after"] == 2
    assert view["certificate"]["kind"] == "regularized-view"
    assert view["certificate"]["label"] == "regularized"
    assert "regularized" in view["claim"]["limitations"]


def test_a_block_off_its_lattice_by_a_hair_snaps_onto_it_exactly() -> None:
    """A 2-by-2 block a few 1e-13 short of its lattice lands on it, by snaps only.

    Two exact squares in opposite corners of a side-5 container fix the exact frame:
    the promotion translates a pose to its bounding box and takes the side from it, so
    without them the block's own hair-width residual would become the frame's origin.
    The residuals leave 2e-13 between neighbours, room for the 1e-15 tilts: two squares
    whose centres are exactly a side apart cannot both be tilted.
    """
    witness = decimal_witness(
        [
            ("2.4999999999997", "2.4999999999996", "1e-15"),
            ("3.4999999999999", "2.4999999999996", "-2e-15"),
            ("2.4999999999997", "3.4999999999998", "0"),
            ("3.4999999999999", "3.4999999999998", "3e-16"),
            ("0.5", "0.5", "0"),
            ("4.5", "4.5", "0"),
        ],
        "5",
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    assert view_centres(view)[:4] == [
        (Fraction(5, 2), Fraction(5, 2)),
        (Fraction(7, 2), Fraction(5, 2)),
        (Fraction(5, 2), Fraction(7, 2)),
        (Fraction(7, 2), Fraction(7, 2)),
    ]
    assert view["side"] == "5"
    moves = report["regularization"]["moves"]
    assert moves["compactions"] == 0
    assert moves["snaps"] >= 8
    assert moves["converged"] is True
    assert Fraction(moves["largest_move"]) <= SNAP_TOLERANCE
    assert report["regularization"]["statuses"] == {"exact-axis": 6}
    # The block's shades do not change: a snap changes the representation, not the
    # drawing.  Each block square has its two neighbours and no wall.
    assert [s["stage"] for s in report["squares"][:4]] == [[2, 2]] * 4
    # Four exact face contacts inside the block; the verifier also reports a zero gap for
    # the block's two diagonal corner touches and for its outer corner, which now meets
    # the pinned square's corner exactly.
    assert report["regularization"]["exact_contacts_after"] == 7
    assert report["exact_verification"]["repository_verifier"]["touching_pairs"] == 7


def test_a_slide_into_a_tilted_square_stops_short_and_is_refused() -> None:
    """The tilted diamond's lower corner dips 0.01 into the lane the square would sweep."""
    # The diamond at 45 degrees has its lowest corner at (1.01, 0.99): at height 1 it
    # spans x in [1, 1.02], touching the seated square's right edge without entering it,
    # so the square at 1.53 may slide only 0.01 before its top-left corner meets it.
    diamond_y = str(Fraction("0.99") + Fraction("0.70710678118654752440084436210484904"))
    witness = decimal_witness(
        [
            ("0.5", "0.5", "0"),
            ("1.53", "0.5", "0"),
            ("1.01", diamond_y, "0.78539816339744830962"),
            PIN_3,
        ],
        "3",
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    moved = report["squares"][1]
    assert moved["moves"] == []
    (refused,) = moved["rejected_moves"]
    assert refused["blockers"] == ["square:3"]
    assert refused["reached_target"] is False
    assert Fraction(refused["distance"]) < Fraction("0.0100001")
    assert Fraction(refused["distance"]) > Fraction("0.0099999")
    assert refused["stage_contacts"] == [1, 1]
    assert refused["house_contacts"] == [1, 1]
    assert moved["light_faces"] == {
        "left": "tilted-neighbour",
        "right": "hole",
        "top": "tilted-neighbour",
    }
    assert view_centres(view)[1] == (Fraction("1.53"), HALF)
    assert report["exact_verification"]["repository_verifier"]["valid"] is True


def test_a_slide_that_costs_a_tilted_neighbour_its_stage_contact_is_undone() -> None:
    """Square 1 sits 0.02 off the left wall; square 2, tilted 0.002 radians, is 1.003 to its
    right, a stage contact. Sliding 1 onto the wall gains it the wall and costs it 2, which
    its own counts allow, but leaves 2 with 1.023 between centres: past the stage's gap.
    The rule holds square 1's slides and runs again, and nothing is lighter than before.
    """
    witness = decimal_witness(
        [("0.52", "0.5", "0"), ("1.523", "0.502", "0.002"), LEFT_3, PIN_3], "3"
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    rounds = report["regularization"]["rounds"]
    assert rounds[0] == {"regressions": {"house": 0, "stage": 1}, "newly_held": {"1": "slides"}}
    assert rounds[1] == {"regressions": {"house": 0, "stage": 0}, "newly_held": {}}
    assert report["regularization"]["non_regression"]["held"] == {"1": "slides"}
    assert report["residual_regressions"] == []
    assert report["contacts"]["stage"]["became_lighter"] == 0
    assert report["squares"][0]["held"] == "slides"
    assert report["squares"][1]["status"] == "near-axis-untouched"
    assert [s["stage"] for s in report["squares"][:2]] == [[2, 2], [2, 2]]
    assert view_centres(view)[0] == (Fraction("0.52"), HALF)
    assert report["exact_verification"]["repository_verifier"]["valid"] is True


def test_a_slide_that_costs_a_neighbour_its_exact_house_contact_is_undone() -> None:
    """Squares 1 and 2 share a side exactly, 0.005 off the left wall's lattice; a tilted
    square 3 sits 1.008 to the right of 2, a stage contact. Square 1 slides onto the wall,
    trading its house contact with 2 for the wall. Square 2 cannot follow: closing the
    gap would carry it 1.013 from square 3 and cost it that stage contact. The stage's
    0.01 gap still counts 1 and 2 as touching, so only the house rule sees square 2 lose
    a side, and that alone undoes square 1's slide.
    """
    witness = decimal_witness(
        [
            ("0.505", "0.5", "0"),
            ("1.505", "0.5", "0"),
            ("2.513", "0.502", "0.002"),
            LEFT_4,
            PIN_4,
        ],
        "4",
    )
    report, view = regularize(witness, source_path="tests/synthetic")

    rounds = report["regularization"]["rounds"]
    assert rounds[0] == {"regressions": {"house": 1, "stage": 0}, "newly_held": {"1": "slides"}}
    assert rounds[-1]["regressions"] == {"house": 0, "stage": 0}
    assert report["contacts"]["house"]["became_lighter"] == 0
    assert report["contacts"]["stage"]["became_lighter"] == 0
    assert [s["house"] for s in report["squares"][:2]] == [[2, 2], [2, 2]]
    # The report is the last round's: square 1 held, square 2 already touching it.
    assert report["squares"][0]["held"] == "slides"
    assert report["squares"][1]["moves"] == []
    assert view_centres(view)[:2] == [(Fraction("0.505"), HALF), (Fraction("1.505"), HALF)]


def test_single_square_counts_match_the_whole_packing_counts() -> None:
    """The counts that judge one slide are the counts the whole packing is shaded with."""
    poses = [
        (0.5, 0.5, 0.0),
        (1.5, 0.5, 0.0),
        (2.5 + 1e-7, 0.5, 0.0),
        (0.5, 1.5 + 3e-6, 0.0),
        (1.52, 1.5, 0.002),
        (3.5, 3.5, 0.0),
    ]
    ids = [str(index) for index in range(1, len(poses) + 1)]
    whole = [len(found) for found in house_partners(poses, 4.0, ids)]
    assert [house_count_of(index, poses, 4.0, ids) for index in range(len(poses))] == whole
    # Square 2 meets square 3 a tenth of a micron off: inside the house rule's 2e-6.
    # Square 4 sits 3e-6 above square 1: outside it, so only the wall counts.
    assert whole == [3, 3, 2, 1, 0, 2]
    staged = stage_contacts(poses, 4.0)
    assert [stage_count_of(index, poses, 4.0) for index in range(len(poses))] == staged


def test_exact_slide_limits_on_rational_corners() -> None:
    """The collision time is exact: a touching neighbour is a zero-gap stop, not an overlap."""
    moving = axis_square((Fraction(3, 2) + Fraction(3, 100), HALF))
    neighbour = axis_square((HALF, HALF))
    far = axis_square((HALF, Fraction(5, 2)))
    limit, blockers = slide_limit(
        moving, (-1, 0), Fraction(3, 100), [("1", neighbour), ("far", far)], Fraction(3)
    )
    assert limit == Fraction(3, 100)
    assert [(b.kind, b.name) for b in blockers] == [("target", ""), ("square", "1")]
    # Touching from below along the whole slide is not an overlap at any distance.
    below = axis_square((Fraction(3, 2), Fraction(-1, 2)))
    assert interior_overlap_interval(moving, (-1, 0), below) is None
    # The wall stops a slide that asks for more room than there is.
    limit, blockers = slide_limit(neighbour, (-1, 0), Fraction(1), [], Fraction(3))
    assert limit == 0
    assert [(b.kind, b.name) for b in blockers] == [("wall", "x=0")]


def test_lattice_targets_seat_from_the_nearer_wall() -> None:
    side = Fraction("10.607174680178947")
    assert lattice_target(Fraction("0.5298"), side) == HALF
    assert lattice_target(Fraction("8.1061"), side) == side - HALF - 2
    assert lattice_target(Fraction("6.722"), side) == Fraction(13, 2)
    assert lattice_target(Fraction(1), Fraction(3)) == HALF


def test_the_stage_rule_counts_as_the_workbench_does() -> None:
    poses = [(0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (0.5, 1.5, 0.0), (1.5, 1.5, 1e-9)]
    assert stage_contacts(poses, 2.0) == [4, 4, 4, 4]
    slack = [(0.5, 0.5, 0.0), (1.5 + 2 * STAGE_GAP, 0.5, 0.0), (1.0, 1.5, 0.8)]
    assert stage_contacts(slack, 2.0) == [2, 1, 0]


def test_the_command_writes_a_verifiable_view_only_where_it_is_told(tmp_path: Path) -> None:
    witness = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), PIN_3], "3", name="cli"
    )
    source = write_witness(tmp_path / "cli.yaml", witness)
    output = tmp_path / "out"

    assert main([str(source), "--output-dir", str(output)]) == 0
    report = json.loads((output / "cli-regularized.json").read_text())
    assert report["exact_verification"]["passed"] is True
    assert report["exact_verification"]["independent_checker"]["verification_passed"] is True
    view = load_witness(output / "cli-regularized.yaml")
    result, verdict = exact_verify(view)
    assert verdict.valid is True
    assert result["coordinate_provenance"] == "verified"
    assert view["certificate"]["derived_from"] == "W-cli"
    # The view names its schema by a path relative to itself, not by this machine's.
    assert (
        not (output / "cli-regularized.yaml").read_text().split("schema: ")[1].startswith("/")
    )

    assert main([str(source), "--output-dir", str(ROOT / "witnesses" / "nowhere")]) == 2
    assert main([str(source), "--output-dir", str(ROOT / "atlas")]) == 2
    assert not (ROOT / "witnesses" / "nowhere").exists()


def scratch_atlas(tmp_path: Path) -> AtlasLayout:
    """Three records: a decimal row with slack, an exact grid with a vacancy, and a
    digitized corner witness that has no exact frame."""
    packing = tmp_path / "packing"
    (packing / "w").mkdir(parents=True)
    (packing / "certificates").mkdir()
    row = decimal_witness(
        [("0.53", "0.5", "0"), ("1.56", "0.5", "0"), ("2.59", "0.5", "0"), PIN_4],
        "4",
        name="row",
    )
    unit = [("0", "0"), ("1", "0"), ("1", "1"), ("0", "1")]
    grid = corner_witness(
        [
            unit,
            [(str(int(x) + 1), y) for x, y in unit],
            [(x, str(int(y) + 1)) for x, y in unit],
        ],
        "2",
        kind="rational",
        name="grid",
    )
    digitized = corner_witness(
        [
            [("0", "0"), ("1", "0.000001"), ("0.999999", "1.000001"), ("0", "1")],
            [("1.1", "0"), ("2.1", "0"), ("2.1", "1"), ("1.1", "1")],
        ],
        "2.1",
        kind="decimal",
        name="digitized",
    )
    entries = []
    for n, witness in ((2, digitized), (3, grid), (4, row)):
        write_witness(packing / "w" / f"n-{n:03d}.yaml", witness)
        entries.append({"n": n, "witness": {"path": f"w/n-{n:03d}.yaml"}})
    manifest = packing / "manifest.json"
    manifest.write_text(json.dumps({"atlas": {"entries": entries}}), encoding="utf-8")
    return AtlasLayout(
        packing, tmp_path, manifest, packing / "regularized", packing / "certificates"
    )


def test_the_atlas_layer_updates_checks_and_verifies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The pool follows the gate's cap, as `sqpack.workers` does for every pooled tool, so
    # one worker here keeps the scratch layer in this process.
    monkeypatch.setenv("PACK_JOBS", "1")
    layout = scratch_atlas(tmp_path)

    assert main(["--update-atlas"], layout=layout) == 0
    index = json.loads(layout.index.read_text())
    assert index["algorithm"] == ALGORITHM
    assert index["label"] == "regularized"
    statuses = {record["n"]: record["status"] for record in index["entries"]}
    assert statuses == {2: "refused", 3: "unchanged", 4: "regularized"}
    refused, unchanged, regularized = index["entries"]
    assert refused["refusal"]["kind"] == "promotion-unsupported"
    # The grid's two squares beside the vacancy are light, and stay so: it is a hole.
    assert unchanged["shades"]["house"]["light_after"] == 2
    # The row compacts, but no square reaches four sides: shading counts squares, and a
    # row on a wall is still light; the moves are what the record shows.
    assert regularized["shades"]["house"]["light_before"] == 4
    assert regularized["shades"]["house"]["light_after"] == 4
    assert regularized["moves"]["compactions"] == 3
    assert regularized["exact_verification"]["passed"] is True
    assert regularized["view"]["path"] == "packing/regularized/n-004-regularized.yaml.gz"
    assert sorted(path.name for path in layout.directory.iterdir()) == [
        "index.json",
        "n-004-regularized.yaml.gz",
    ]
    view = gzip.decompress(layout.view(4).read_bytes()).decode("utf-8")
    assert "W-row-regularized" in view
    assert index["totals"]["statuses"] == {"refused": 1, "regularized": 1, "unchanged": 1}

    # The drawings of the views live beside them and answer to their renderer's check.
    (layout.directory / "rendering").mkdir()
    (layout.directory / "rendering" / "n-004.svg").write_text("<svg/>", encoding="utf-8")
    assert check_atlas(layout) == []
    assert main(["--check-atlas"], layout=layout) == 0
    assert main(["--verify-atlas"], layout=layout) == 0

    retained = layout.view(4).read_bytes()
    layout.view(4).write_bytes(
        gzip.compress(view.replace("W-row", "W-other").encode(), mtime=0)
    )
    assert check_atlas(layout) == [
        "n=4: the view differs from the one its verdict was recorded for"
    ]
    assert main(["--verify-atlas", "--n", "4"], layout=layout) == 1
    layout.view(4).write_bytes(retained)

    grid = layout.packing / "w/n-003.yaml"
    grid.write_text(grid.read_text() + "# touched\n", encoding="utf-8")
    (layout.directory / "stray.txt").write_text("", encoding="utf-8")
    assert check_atlas(layout) == [
        "n=3: the witness changed since its view was derived (stale)",
        "unexpected file packing/regularized/stray.txt",
    ]
    assert main(["--check-atlas"], layout=layout) == 1


# Two squares meeting a hair too closely: their 31-digit centres put them 1e-30 into each
# other, the way a decimal witness rounds an exact contact. A pinned corner square fixes
# the frame. Dilation 1 is not a packing; the smallest dilation that is spreads the
# centres by 1e-29 about the container's centre.
OVERLAP = [("0.5", "0.5", "0"), ("1.499999999999999999999999999999", "0.5", "0"), PIN_3]


def test_the_smallest_verifying_dilation_is_promote_rationals_own() -> None:
    """The prototype walks `promote_rational`'s ladder and stops where it would.

    Without the flag the layer's rule holds: dilation 1 or refusal. With it, the frame is
    the first packing on the ladder, its side grows past the printed one by the spread,
    and the compaction snaps the opened contact shut again.
    """
    witness = decimal_witness(OVERLAP, "3", name="overlap")
    ladder = promotion_dilations(RATIONAL_DIGITS)
    assert ladder[0] == 1
    assert len(ladder) == 16
    assert ladder[1:] == sorted(ladder[1:])
    assert ladder[-1] == 1 + Fraction(1, 1000)

    with pytest.raises(RegularizeError) as refused:
        regularize(witness, source_path="tests/synthetic")
    assert refused.value.kind == "promotion-overlap"
    assert "at dilation 1 is not a packing" in str(refused.value)

    report, view = regularize(witness, source_path="tests/synthetic", smallest_dilation=True)
    promotion, _certificate = promote_rational(
        witness,
        rational_digits=RATIONAL_DIGITS,
        max_side_increase=MAX_SIDE_INCREASE,
        source_path="tests/synthetic",
        replay_path="tests/synthetic",
    )
    dilation = report["exact_frame"]["center_dilation"]
    assert dilation == promotion["center_dilation"]
    assert Fraction(dilation) == 1 + Fraction(1, 10**29)
    # The whole packing spread: the side is the printed one plus twice the spread.
    assert Fraction(view["side"]) == 3 + Fraction(2, 10**29)
    assert report["exact_frame"]["fits_reported_side"] is False
    assert report["exact_verification"]["repository_verifier"]["valid"] is True
    # The 9e-30 the dilation opened between the pair is a snap, and it closes exactly.
    assert view_centres(view)[:2] == [(HALF, HALF), (Fraction(3, 2), HALF)]
    assert report["contacts"]["house"]["became_lighter"] == 0


def test_the_atlas_records_a_dilation_only_when_the_prototype_is_asked_for(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PACK_JOBS", "1")
    packing = tmp_path / "packing"
    (packing / "w").mkdir(parents=True)
    (packing / "certificates").mkdir()
    write_witness(packing / "w/n-003.yaml", decimal_witness(OVERLAP, "3", name="overlap"))
    manifest = packing / "manifest.json"
    entries = [{"n": 3, "witness": {"path": "w/n-003.yaml"}}]
    manifest.write_text(json.dumps({"atlas": {"entries": entries}}), encoding="utf-8")
    layout = AtlasLayout(
        packing, tmp_path, manifest, packing / "regularized", packing / "certificates"
    )

    assert main(["--update-atlas"], layout=layout) == 0
    (record,) = json.loads(layout.index.read_text())["entries"]
    assert record["status"] == "refused"
    assert record["refusal"]["kind"] == "promotion-overlap"

    assert main(["--update-atlas", "--smallest-dilation"], layout=layout) == 0
    index = json.loads(layout.index.read_text())
    assert index["parameters"]["center_dilation"] == SMALLEST_DILATION
    (record,) = index["entries"]
    assert record["status"] == "regularized"
    assert Fraction(record["exact_frame"]["center_dilation"]) == 1 + Fraction(1, 10**29)
    assert record["side"]["fits_reported_side"] is False
    assert record["exact_verification"]["passed"] is True

    # A layer built under one dilation policy is checked under that policy only.
    assert main(["--check-atlas", "--smallest-dilation"], layout=layout) == 0
    assert main(["--verify-atlas", "--smallest-dilation"], layout=layout) == 0
    (problem,) = check_atlas(layout)
    assert problem.startswith("index parameters is ")
    assert main(["--verify-atlas"], layout=layout) == 1
