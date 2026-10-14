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

import dataclasses
import gzip
import hashlib
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import atlas_orientation
from devtools import regularize_axis_components as axis
from devtools.atlas_orientation import orient_atlas_witness, reflect_y_axis
from devtools.regularize_axis_components import (
    ALGORITHM,
    ATLAS_CONTRACT,
    EVAND_CREDIT,
    EVAND_GENERATOR,
    RATIONAL_DIGITS,
    ROOT,
    SMALLEST_DILATION,
    SNAP_TOLERANCE,
    STAGE_GAP,
    WITNESS_SCHEMA,
    AtlasLayout,
    RegularizeError,
    atlas_record,
    atlas_totals,
    axis_square,
    centre,
    check_atlas,
    costed_once,
    decide_drawn_view,
    exact_frame,
    house_count_of,
    house_partners,
    interior_overlap_interval,
    lattice_target,
    main,
    promotion_dilations,
    regularize,
    repeated_costs,
    slide_limit,
    stage_contacts,
    stage_count_of,
)
from devtools.upper_bound_packets import MAX_SIDE_INCREASE
from sqpack.witness import exact_verify, load_witness, promote_rational, witness_document
from sqpack.yamlio import load_yaml

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
    assert index["contract"] == ATLAS_CONTRACT
    assert index["softschema"]["contract"] == ATLAS_CONTRACT
    assert index["generators"][ALGORITHM]["method"] == ALGORITHM
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
    # Each record names its generator, and a drawn view carries its regularization in the
    # register's terms: three squares slid along the row, none turned.
    assert {record["generator"] for record in index["entries"]} == {ALGORITHM}
    assert regularized["regularization"] == {
        "n": 4,
        "of_witness": "W-row",
        "by": "project",
        "method": ALGORITHM,
        "side": "same",
        "identity": {
            "basis": "measured",
            "measured_in": "packing/regularized/index.json",
            "one_to_one": True,
            "moved": 3,
            "max_move": 0.06,
            "max_turn_deg": 0.0,
        },
    }
    assert "regularization" not in unchanged
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


def drawn_by_another_generator(layout: AtlasLayout, n: int) -> dict[str, Any]:
    """Draw count `n` from another generator's view, as an admission writes one: here the
    axis tool's own view relabelled, which is exact and verifies as any view must."""
    index = json.loads(layout.index.read_text())
    entries = {record["n"]: record for record in index["entries"]}
    reference = entries[n]
    view = load_yaml(gzip.decompress(layout.view(n).read_bytes()).decode())["witness"]
    regularization = {
        **reference["regularization"],
        "method": "a fixture through devtools.regularize_evand",
    }
    view["certificate"] = {
        "kind": "regularized-view",
        "label": "regularized",
        "derived_from": reference["source"]["id"],
        "generator": EVAND_GENERATOR,
        "credit": EVAND_CREDIT,
        "regularization": regularization,
    }
    text = witness_document(view, schema=str(WITNESS_SCHEMA))
    layout.view(n).write_bytes(gzip.compress(text.encode(), mtime=0))
    entries[n] = {
        "n": n,
        "status": "regularized",
        "generator": EVAND_GENERATOR,
        "run": {"id": "fixture-run"},
        "source": reference["source"],
        "side": {
            "reported": reference["side"]["reported"],
            "view": view["side"],
            "relation": "same",
            "view_minus_reported": "0.000e+00",
            "view_minus_verified_upper_bound": None,
        },
        "view": {
            "path": reference["view"]["path"],
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
        },
        "shades": reference["shades"],
        "exact_verification": {
            "repository_verifier": True,
            "independent_checker": True,
            "passed": True,
        },
        "decision": {"row": 10, "decision": "admit", "reason": "fixture"},
        "measured": {
            "identity_by": "fixture",
            "shades_by": "fixture",
            "contacts": {
                rule: {"before": [0, 0, 0, 0, 0], "after": [0, 0, 0, 0, 0]}
                for rule in ("house", "stage")
            },
            "symmetry": 0,
            "regressions": 0,
        },
        "regularization": regularization,
        "reference": reference,
    }
    records = [entries[key] for key in sorted(entries)]
    index["entries"] = records
    index["generators"][EVAND_GENERATOR] = {
        "tool": "packing/devtools/regularize_evand.py",
        "generated_by": "fixture",
        "method": "fixture",
        "credit": EVAND_CREDIT,
    }
    index["runs"] = [
        {
            "id": "fixture-run",
            "generator": EVAND_GENERATOR,
            "finished": "2026-10-12",
            "parameters": {},
            "counts": 1,
            "cost": {"cpu_seconds": 0, "wall_seconds": 0, "workers": 1},
        }
    ]
    index["totals"] = atlas_totals(records)
    layout.index.write_text(json.dumps(index), encoding="utf-8")
    return entries[n]


def test_another_generators_view_is_checked_kept_and_decided_again(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PACK_JOBS", "1")
    layout = scratch_atlas(tmp_path)
    assert main(["--update-atlas"], layout=layout) == 0
    entry = drawn_by_another_generator(layout, 4)
    assert check_atlas(layout) == []
    # The full check re-derives this tool's record into the reference and decides the
    # other generator's view again on both exact routes.
    assert main(["--verify-atlas"], layout=layout) == 0

    # Updating this tool's layer keeps the drawn view and its run, and refreshes the
    # reference beside it.
    retained = layout.view(4).read_bytes()
    assert main(["--update-atlas"], layout=layout) == 0
    index = json.loads(layout.index.read_text())
    kept = next(record for record in index["entries"] if record["n"] == 4)
    assert kept == entry
    assert layout.view(4).read_bytes() == retained
    assert [run["id"] for run in index["runs"]] == ["fixture-run"]
    assert index["totals"]["views_by_generator"] == {EVAND_GENERATOR: 1}

    # A view that no longer says what its entry says is named, field by field.
    view = load_yaml(gzip.decompress(retained).decode())["witness"]
    view["certificate"]["credit"] = "someone else"
    text = witness_document(view, schema=str(WITNESS_SCHEMA))
    layout.view(4).write_bytes(gzip.compress(text.encode(), mtime=0))
    problems = check_atlas(layout)
    assert "n=4: the view differs from the one its verdict was recorded for" in problems
    assert any("certificate credit is 'someone else'" in problem for problem in problems)
    layout.view(4).write_bytes(retained)

    # Its witness changed: the view lapses, and this tool's record is drawn again.
    path = layout.packing / "w/n-004.yaml"
    path.write_text(path.read_text() + "# corrected\n", encoding="utf-8")
    assert main(["--update-atlas"], layout=layout) == 0
    index = json.loads(layout.index.read_text())
    assert {record["generator"] for record in index["entries"]} == {ALGORITHM}
    assert index["runs"] == []
    assert list(index["generators"]) == [ALGORITHM]
    assert check_atlas(layout) == []


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
    assert index["generators"][ALGORITHM]["parameters"]["center_dilation"] == SMALLEST_DILATION
    (record,) = index["entries"]
    assert record["status"] == "regularized"
    # A dilated frame is not the witness's side, so its regularization was solved to one.
    assert record["regularization"]["side"] == "solved"
    assert Fraction(record["exact_frame"]["center_dilation"]) == 1 + Fraction(1, 10**29)
    assert record["side"]["fits_reported_side"] is False
    assert record["exact_verification"]["passed"] is True

    # A layer built under one dilation policy is checked under that policy only.
    assert main(["--check-atlas", "--smallest-dilation"], layout=layout) == 0
    assert main(["--verify-atlas", "--smallest-dilation"], layout=layout) == 0
    (problem,) = check_atlas(layout)
    assert problem.startswith(f"index {ALGORITHM} is ")
    assert main(["--verify-atlas"], layout=layout) == 1


def test_an_oriented_atlas_view_derives_in_the_ancestor_pose_then_rechecks_the_image(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    layout = scratch_atlas(tmp_path)
    path = layout.packing / "w/n-004.yaml"
    ancestor = load_witness(path, fallback_schema=WITNESS_SCHEMA)
    ancestor["claim"].update(
        method="numerical-multiprecision",
        precision={"decimal_digits": 120, "rounding": "nearest"},
    )
    write_witness(path, ancestor)
    frame = exact_frame(ancestor)
    certificate = corner_witness(
        [[(str(x), str(y)) for x, y in piece.corners] for piece in frame.pieces],
        str(frame.side),
        kind="rational",
        name="ancestor",
    )
    parent = layout.certificates / "packet/n-004-rational.yaml.gz"
    parent.parent.mkdir()
    parent.write_bytes(gzip.compress(witness_document(certificate).encode(), mtime=0))
    entry = {"n": 4, "witness": {"path": "w/n-004.yaml"}}
    before, parent_text, _ = atlas_record(entry, layout)
    assert parent_text is not None
    assert before["exact_frame"]["matches_retained_certificate"] is True

    # The registered case is replaced by this small fixture to exercise the same
    # wrapper without paying for an unrelated full-corpus derivation.
    monkeypatch.setattr(atlas_orientation, "REFLECTED_N", 4)
    monkeypatch.setattr(atlas_orientation, "PARENT_FACTS", "tests/synthetic")
    monkeypatch.setattr(atlas_orientation, "PARENT_SOURCE_KEY", "synthetic-parent")
    ancestor["source"]["key"] = "synthetic-parent"
    write_witness(path, orient_atlas_witness(ancestor))
    after, image_text, _ = atlas_record(entry, layout)
    assert image_text is not None
    assert after["exact_frame"]["matches_retained_certificate"] is False
    assert after["exact_frame"]["ancestor_matches_retained_certificate"] is True
    assert after["exact_frame"]["geometry_transform"]["operation"] == "reflect-y-axis"
    assert after["exact_verification"]["passed"] is True
    assert after["exact_verification"]["independent_checker"] is True
    for key in ("moves", "statuses", "non_regression", "side", "shades", "changed_squares"):
        assert after[key] == before[key]
    original = load_yaml(parent_text)["witness"]
    image = load_yaml(image_text)["witness"]
    assert image["squares"] == reflect_y_axis(original)["squares"]
    assert image["side"] == original["side"]
    assert image["certificate"]["regularization"] == original["certificate"]["regularization"]
    assert image["certificate"]["geometry_transform"]["parent"]["exact_certificate"] == (
        layout.relative(parent)
    )


def edit_drawn(
    layout: AtlasLayout, n: int, change: Callable[[dict[str, Any], dict[str, Any]], None]
) -> dict[str, Any]:
    """Apply `change(entry, view)` to a drawn count's index entry and view together, the
    view re-gzipped deterministically and its digest updated: an edit the cheap check
    reads as consistent."""
    index = json.loads(layout.index.read_text())
    entry = next(record for record in index["entries"] if record["n"] == n)
    document = load_yaml(gzip.decompress(layout.view(n).read_bytes()).decode())
    change(entry, document["witness"])
    text = witness_document(document["witness"], schema=document["softschema"]["schema"])
    layout.view(n).write_bytes(gzip.compress(text.encode(), mtime=0))
    entry["view"]["sha256"] = hashlib.sha256(text.encode()).hexdigest()
    layout.index.write_text(json.dumps(index), encoding="utf-8")
    return entry


def test_the_deep_re_decision_re_measures_the_identity_and_the_count(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B3: the register publishes a drawn view's identity as measured, so the
    re-decision measures it again against the witness, and counts the squares."""
    monkeypatch.setenv("PACK_JOBS", "1")
    layout = scratch_atlas(tmp_path)
    assert main(["--update-atlas"], layout=layout) == 0
    drawn_by_another_generator(layout, 4)
    retained = (layout.index.read_text(), layout.view(4).read_bytes())

    def entry() -> dict[str, Any]:
        index = json.loads(layout.index.read_text())
        return next(record for record in index["entries"] if record["n"] == 4)

    assert decide_drawn_view(entry(), layout)[1] == []

    # "Moved 0", written into the entry and the view's certificate together: the cheap
    # check reads the two as consistent, and only measuring again refuses it.
    def unmoved(record: dict[str, Any], view: dict[str, Any]) -> None:
        for item in (record["regularization"], view["certificate"]["regularization"]):
            item["identity"].update(moved=0, max_move=1e-9, max_turn_deg=0.0)

    edit_drawn(layout, 4, unmoved)
    assert check_atlas(layout) == []
    (problem,) = decide_drawn_view(entry(), layout)[1]
    assert problem.startswith(
        "n=4: the drawn view's identity measures {'one_to_one': True, 'moved': 3"
    )
    assert main(["--verify-atlas"], layout=layout) == 1

    # A view one square short is still a valid packing on both routes.
    layout.index.write_text(retained[0], encoding="utf-8")
    layout.view(4).write_bytes(retained[1])
    edit_drawn(layout, 4, lambda _record, view: view["squares"].pop())
    assert check_atlas(layout) == []
    problems = decide_drawn_view(entry(), layout)[1]
    assert "n=4: the drawn view holds 3 squares" in problems


def case_record(layout: AtlasLayout, n: int, value: str, exact_form: str | None) -> None:
    """A case record holding only the verified upper bound the check reads."""
    assert layout.frontier is not None
    layout.frontier.mkdir(exist_ok=True)
    form = "null" if exact_form is None else f"'{exact_form}'"
    (layout.frontier / f"n-{n:03d}.md").write_text(
        f"---\npacking:\n  n: {n}\n  verified_upper_bound:\n    value: '{value}'\n"
        f"    exact_form: {form}\n---\n\n# s({n})\n",
        encoding="utf-8",
    )


def test_every_drawn_view_is_held_to_its_case_records_verified_upper_bound(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B1: the side of every drawn view, this tool's included, against `U`,
    decided exactly, closed forms included."""
    monkeypatch.setenv("PACK_JOBS", "1")
    monkeypatch.setattr(axis, "ABOVE_U", {})
    layout = scratch_atlas(tmp_path)
    assert main(["--update-atlas"], layout=layout) == 0
    layout = dataclasses.replace(layout, frontier=tmp_path / "packing/frontier")
    (layout.frontier or tmp_path).mkdir()
    # The row's view is exactly at the printed side 4.
    assert check_atlas(layout) == ["n=4: its case record states no verified upper bound U"]
    case_record(layout, 4, "4", None)
    assert check_atlas(layout) == []

    case_record(layout, 4, "5", "5")
    assert check_atlas(layout) == [
        (
            "n=4: the view is -1.000e+00 from U, below it: a new result, registered before "
            "it is drawn (row 3)"
        )
    ]
    # 1.25e-41 below a closed form a 40-digit evaluation rounds to the view's side.
    case_record(layout, 4, "4", "sqrt(16 + 1/10**40)")
    (problem,) = check_atlas(layout)
    assert problem.startswith("n=4: the view is -1.250e-41 from U, below it")

    # 4 - (3/2) sqrt(7) above: a view above U is drawn only where it is named.
    case_record(layout, 4, "3.968627", "(3/2)sqrt(7)")
    assert check_atlas(layout) == [
        "n=4: the view is 3.137e-02 above U, at a count ABOVE_U does not name"
    ]
    monkeypatch.setattr(axis, "ABOVE_U", {4: "a fixture above U"})
    assert check_atlas(layout) == []
    # The list only shrinks on purpose: a named count drawn at U is named no longer.
    case_record(layout, 4, "4", "4")
    assert check_atlas(layout) == [
        "n=4: ABOVE_U names it, but no view is drawn above U there; take it off the list"
    ]
    monkeypatch.setattr(axis, "ABOVE_U", {})

    # Another generator's entry records s_V - U, and a `bound` one is at U.
    drawn_by_another_generator(layout, 4)
    assert check_atlas(layout) == [
        "n=4: view_minus_verified_upper_bound is None, not '0.000e+00'"
    ]

    def at_u(record: dict[str, Any], _view: dict[str, Any]) -> None:
        record["side"]["view_minus_verified_upper_bound"] = "0.000e+00"

    edit_drawn(layout, 4, at_u)
    assert check_atlas(layout) == []

    def bound(record: dict[str, Any], _view: dict[str, Any]) -> None:
        record["side"]["relation"] = "bound"

    edit_drawn(layout, 4, bound)
    case_record(layout, 4, "4.5", "9/2")
    problems = check_atlas(layout)
    assert "n=4: the relation is 'bound', but the view is -5.000e-01 from U" in problems
    assert "n=4: view_minus_verified_upper_bound is '0.000e+00', not '-5.000e-01'" in problems


def test_a_views_side_relation_is_decided_against_the_witnesss_own_side(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B2: `same` is `s_V = s_W`, for this tool's views as for any other's."""
    monkeypatch.setenv("PACK_JOBS", "1")
    layout = scratch_atlas(tmp_path)
    assert main(["--update-atlas"], layout=layout) == 0
    index = json.loads(layout.index.read_text())
    (record,) = (entry for entry in index["entries"] if entry["n"] == 4)
    assert record["regularization"]["side"] == "same"
    record["regularization"]["side"] = "solved"
    layout.index.write_text(json.dumps(index), encoding="utf-8")
    assert check_atlas(layout) == [
        (
            "n=4: the regularization's side is 'solved', and the view is at the witness's "
            "own side s_W"
        )
    ]


def test_a_reclassified_copy_of_a_run_records_no_cost_of_its_own(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """#548 review B5: a run decided again on a copy of its directory keeps the source
    run's cost in its receipt; the index records that cost once. Review C, C3: the copy is
    the run its receipt marks (`reclassified_from`), whatever the order of the runs, and
    equal seconds decide nothing: a cost repeated unmarked is refused."""
    full = {"cpu_seconds": 49301.63, "wall_seconds": 13812.25, "workers": 4}
    runs = [
        {"id": "full", "cost": dict(full)},
        {
            "id": "same2",
            "cost": {"cpu_seconds": 3062.97, "wall_seconds": 3355.87, "workers": 2},
        },
        {"id": "refreshed-full", "reclassified_from": "full", "cost": dict(full)},
        {"id": "fixture", "cost": {"cpu_seconds": 0, "wall_seconds": 0, "workers": 1}},
        {"id": "fixture-2", "cost": {"cpu_seconds": 0, "wall_seconds": 0, "workers": 1}},
    ]
    once = costed_once(runs)
    assert [once[0], once[1], *once[3:]] == [runs[0], runs[1], *runs[3:]]
    assert once[2]["reclassified_from"] == "full"
    assert once[2]["cost"] == {
        "cpu_seconds": 0.0,
        "wall_seconds": 0.0,
        "workers": 4,
        "note": "reclassified from full without re-running a stage; that run's cost is "
        "recorded there",
    }
    assert costed_once(once) == once
    assert repeated_costs(runs) == []
    # The copy listed first, as when a source run is admitted after its copy: the same
    # run is the copy, and the source keeps its cost.
    assert costed_once(runs[::-1]) == once[::-1]
    assert repeated_costs(runs[::-1]) == []
    # A copy whose source the index does not list is the one record of that cost.
    (alone,) = costed_once([runs[2]])
    assert alone == {"id": "refreshed-full", "cost": full}
    # Unmarked, equal seconds are refused in either order rather than guessed at.
    unmarked = [runs[0], {"id": "refreshed-full", "cost": dict(full)}]
    assert costed_once(unmarked) == unmarked
    for order in (unmarked, unmarked[::-1]):
        (problem,) = repeated_costs(order)
        assert "neither is marked as the other's reclassified copy" in problem
    looped = [{**runs[0], "reclassified_from": "refreshed-full"}, runs[2]]
    assert "is recorded on none" in repeated_costs(looped)[0]

    monkeypatch.setenv("PACK_JOBS", "1")
    layout = scratch_atlas(tmp_path)
    assert main(["--update-atlas"], layout=layout) == 0
    drawn_by_another_generator(layout, 4)
    index = json.loads(layout.index.read_text())
    (run,) = index["runs"]
    run["cost"] = {"cpu_seconds": 2.5, "wall_seconds": 9.0, "workers": 1}
    index["runs"].append({**run, "id": "fixture-copy", "reclassified_from": "fixture-run"})
    layout.index.write_text(json.dumps(index), encoding="utf-8")
    assert "index run fixture-copy repeats run fixture-run's cost" in check_atlas(layout)
    index["runs"][-1] = {**run, "id": "fixture-copy"}
    layout.index.write_text(json.dumps(index), encoding="utf-8")
    assert (
        "index run fixture-copy repeats run fixture-run's cost and neither is marked as the "
        "other's reclassified copy: write `reclassified.from`, the run it was copied from, "
        "into the copy's receipt.json"
    ) in check_atlas(layout)
