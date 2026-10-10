"""Exact and adversarial controls for the literal BC303 T1 witness reader."""

# The tests exercise independent reconstruction helpers at their trust boundaries.
# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import cast

import pytest

from devtools import replay_bc303_t1_witness as replay

REPO = Path(__file__).resolve().parents[2]


def _measure_document() -> dict[str, object]:
    return replay.strict_json_bytes(REPO.joinpath(replay.MEASURE_PATH).read_bytes(), "measure")


def test_bound_replay_emits_the_closed_narrow_determination() -> None:
    record = replay.replay(REPO)
    replay.validate_record(record, REPO)
    witness = cast(dict[str, object], record["witness"])
    determination = cast(dict[str, object], record["determination"])
    memberships = cast(list[dict[str, object]], record["memberships"])

    assert len(cast(list[object], record["sources"])) == 18
    assert len(memberships) == 377
    assert [row["index"] for row in memberships if row["inside_core"]] == list(
        replay.CAPTURED_INDICES
    )
    assert witness["labels"] == [3, 4, 11, 12]
    assert witness["captured_mass"] == "800003/800000"
    assert witness["surplus"] == "3/800000"
    assert witness["named_strict_inequality_holds"] is False
    assert determination == {
        "outcome": "rejected",
        "claim": (
            "for every X in the bottom-left one-corner role-C domain with labels 0 and "
            "15 absent, S(X) > epsilon"
        ),
        "scope": "the named one-corner BC303 T1 local surplus inequality only",
        "global_routing": "not-claimed",
        "n11_lower_bound": "not-claimed",
        "minimum_surplus": "not-claimed",
    }
    assert record["source_revision"] == replay.SOURCE_REVISION
    assert (
        record["implementation_revision"]
        == subprocess.run(
            ("git", "-C", str(REPO), "rev-parse", "HEAD"), check=True, capture_output=True
        )
        .stdout.decode()
        .strip()
    )
    assert replay.encode_record(record, REPO) == replay.encode_record(deepcopy(record), REPO)


def test_retained_rows_must_match_every_bound_source_atom() -> None:
    original = replay.replay(REPO)
    changed_weights = deepcopy(original)
    rows = cast(list[dict[str, object]], changed_weights["memberships"])
    delta = Fraction(1, replay.WEIGHT_SCALE)
    for index, change in ((0, delta), (2, -delta)):
        row = rows[index]
        weight = Fraction(cast(str, row["weight"])) + change
        row["weight"] = str(weight)
        row["weight_units"] = int(replay.WEIGHT_SCALE * weight)
    with pytest.raises(replay.T1ReplayError, match="bound source atom"):
        replay.validate_record(changed_weights, REPO)
    with pytest.raises(replay.T1ReplayError, match="bound source atom"):
        replay.encode_record(changed_weights, REPO)

    negative_excluded = deepcopy(original)
    rows = cast(list[dict[str, object]], negative_excluded["memberships"])
    rows[1]["weight"] = "-1"
    rows[1]["weight_units"] = -replay.WEIGHT_SCALE
    with pytest.raises(replay.T1ReplayError, match="bound source atom"):
        replay.validate_record(negative_excluded, REPO)

    outside_excluded = deepcopy(original)
    rows = cast(list[dict[str, object]], outside_excluded["memberships"])
    rows[1]["point"] = ["10", "10"]
    _inside, slacks = replay.closed_core_membership(
        (Fraction(10), Fraction(10)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(1), Fraction(0)),
    )
    rows[1]["axis_slacks"] = [str(value) for value in slacks]
    with pytest.raises(replay.T1ReplayError, match="bound source atom"):
        replay.validate_record(outside_excluded, REPO)

    for changed_flag in (False, 1):
        altered_membership = deepcopy(original)
        rows = cast(list[dict[str, object]], altered_membership["memberships"])
        rows[0]["inside_core"] = changed_flag
        with pytest.raises(replay.T1ReplayError, match="bound source atom"):
            replay.validate_record(altered_membership, REPO)


def test_retained_implementation_revision_must_name_the_executing_reader() -> None:
    record = replay.replay(REPO)
    record["implementation_revision"] = "0" * 40
    with pytest.raises(replay.T1ReplayError, match="implementation revision differs"):
        replay.validate_record(record, REPO)
    with pytest.raises(replay.T1ReplayError, match="implementation revision differs"):
        replay.encode_record(record, REPO)


def test_cross_checkout_and_dirty_executing_reader_are_refused(tmp_path: Path) -> None:
    checkout = tmp_path / "input-checkout"
    subprocess.run(
        ("git", "clone", "--shared", "--quiet", "--no-checkout", str(REPO), str(checkout)),
        check=True,
    )
    # Keep every authenticated source and the clone-local reader package, while
    # avoiding unrelated bulk during both the current and historical checkouts.
    custody_paths = {
        *(source.path for source in replay.SOURCES),
        replay.READER_PATH,
        "packing/devtools/__init__.py",
    }
    subprocess.run(
        ("git", "-C", str(checkout), "sparse-checkout", "set", "--no-cone", "--stdin"),
        input="".join(f"/{path}\n" for path in sorted(custody_paths)),
        text=True,
        check=True,
    )
    subprocess.run(
        ("git", "-C", str(checkout), "checkout", "--quiet", "HEAD"),
        check=True,
    )

    def materialized_paths() -> set[str]:
        paths: set[str] = set()
        for directory, directories, names in checkout.walk():
            directories[:] = [
                name for name in directories if name not in {".git", "__pycache__"}
            ]
            paths.update((directory / name).relative_to(checkout).as_posix() for name in names)
        return paths

    assert materialized_paths() == custody_paths
    with pytest.raises(replay.T1ReplayError, match=r"executing T1 reader.*path"):
        replay.replay(checkout)

    reader = checkout / replay.READER_PATH
    reader.write_bytes(reader.read_bytes() + b"\n# changed executing reader\n")
    output = tmp_path / "dirty.json"
    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "devtools.replay_bc303_t1_witness",
            "--repository",
            str(checkout),
            "--output",
            str(output),
        ),
        cwd=checkout / "packing",
        check=False,
        capture_output=True,
    )
    assert result.returncode == 2
    assert result.stdout == b""
    assert "differs from implementation revision" in result.stderr.decode()
    assert not output.exists()

    subprocess.run(
        ("git", "-C", str(checkout), "reset", "--hard", "HEAD"), check=True, capture_output=True
    )
    subprocess.run(
        ("git", "-C", str(checkout), "checkout", "--quiet", replay.SOURCE_REVISION),
        check=True,
    )
    # The re-bound source revision postdates this reader, so the checkout now holds a
    # reader file; the refusal turns on its not being the executing one, not on absence.
    assert materialized_paths() == custody_paths
    assert reader.resolve() != Path(replay.__file__).resolve()
    with pytest.raises(replay.T1ReplayError, match=r"executing T1 reader.*path"):
        replay.replay(checkout)


def test_source_binding_rejects_changed_missing_and_duplicate_json_bytes() -> None:
    sources = {source.path: (REPO / source.path).read_bytes() for source in replay.SOURCES}
    replay.validate_source_bytes(sources)

    changed = dict(sources)
    changed[replay.SOURCES[0].path] += b"\n"
    with pytest.raises(replay.T1ReplayError, match="source bytes changed"):
        replay.validate_source_bytes(changed)

    missing = dict(sources)
    del missing[replay.SOURCES[-1].path]
    with pytest.raises(replay.T1ReplayError, match="source path set"):
        replay.validate_source_bytes(missing)

    with pytest.raises(replay.T1ReplayError, match="duplicate JSON object key"):
        replay.strict_json_bytes(b'{"atoms":[],"atoms":[]}\n', "measure")


def test_same_total_d4_measure_mutation_cannot_preserve_the_witness() -> None:
    document = _measure_document()
    atoms = cast(list[list[str]], document["atoms"])
    delta = Fraction(1, replay.WEIGHT_SCALE)
    for index in range(8):
        atoms[index][2] = str(Fraction(atoms[index][2]) + delta)
    for index in range(32, 40):
        atoms[index][2] = str(Fraction(atoms[index][2]) - delta)

    measure = replay._parse_measure(document)
    assert measure.total_mass == replay.TOTAL_MASS
    with pytest.raises(replay.T1ReplayError, match="atom capture or T1 allowance"):
        replay._literal_witness(measure)


def test_closed_membership_distinguishes_core_edges_vertices_and_parent_only_points() -> None:
    center = (Fraction(1, 2), Fraction(1, 2))
    ray = (Fraction(1), Fraction(0))
    edge = (replay.CORE_LOWER, Fraction(1, 2))
    vertex = (replay.CORE_UPPER, replay.CORE_UPPER)
    parent_only = (Fraction(0), Fraction(1, 2))
    just_outside = (replay.CORE_UPPER + Fraction(1, replay.WEIGHT_SCALE), Fraction(1, 2))

    assert replay.closed_core_membership(edge, center, ray)[0]
    assert replay.closed_core_membership(vertex, center, ray)[0]
    assert not replay.closed_core_membership(parent_only, center, ray)[0]
    assert 0 <= parent_only[0] <= 1
    assert 0 <= parent_only[1] <= 1
    assert not replay.closed_core_membership(just_outside, center, ray)[0]


def test_complete_labels_preserve_zero_sign_bin_wrap_and_axis_aliases() -> None:
    zero = (Fraction(0), Fraction(0))
    ray = (Fraction(1), Fraction(0))
    half = replay.HALF_CORE_SIDE
    synthetic_mark = (zero,)

    assert replay.complete_labels(zero, ray, synthetic_mark, half) == list(range(8))
    assert replay.complete_labels((half, Fraction(0)), ray, synthetic_mark, half) == [
        0,
        5,
        6,
        7,
    ]
    assert replay.complete_labels((half, half), ray, synthetic_mark, half) == [0, 7]
    assert (
        replay.complete_labels(
            (half + Fraction(1, replay.WEIGHT_SCALE), Fraction(0)),
            ray,
            synthetic_mark,
            half,
        )
        == []
    )
    literal_center = (Fraction(1, 2), Fraction(1, 2))
    assert replay.complete_labels(literal_center, ray, replay.MARKS, half) == [3, 4, 11, 12]
    assert replay.complete_labels(
        literal_center, (Fraction(0), Fraction(1)), replay.MARKS, half
    ) == [
        3,
        4,
        11,
        12,
    ]
    assert replay._axis_aliases() == [
        {"folded_index": 0, "reflected": False, "canonical_axis": ["1", "0"]},
        {"folded_index": 0, "reflected": True, "canonical_axis": ["1", "0"]},
    ]


def test_owner_identity_and_record_scope_mutations_are_refused() -> None:
    with pytest.raises(replay.T1ReplayError, match="repeats an owner identity"):
        replay.unique_owner_surplus(
            (("same-owner", replay.CAPTURED_MASS), ("same-owner", replay.CAPTURED_MASS))
        )

    record = replay.replay(REPO)
    determination = cast(dict[str, object], record["determination"])
    determination["global_routing"] = "established"
    with pytest.raises(replay.T1ReplayError, match="overstates"):
        replay.validate_record(record, REPO)


def test_cli_atomically_writes_the_same_strict_record_as_stdout(tmp_path: Path) -> None:
    output = tmp_path / "t1.json"
    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "devtools.replay_bc303_t1_witness",
            "--repository",
            str(REPO),
            "--output",
            str(output),
        ),
        cwd=REPO / "packing",
        check=False,
        capture_output=True,
    )

    assert result.returncode == 0
    assert result.stderr == b""
    assert result.stdout == output.read_bytes()
    retained = replay.strict_json_bytes(output.read_bytes(), "retained record")
    replay.validate_record(retained, REPO)


def test_cli_refusal_is_nonzero_and_does_not_publish(tmp_path: Path) -> None:
    output = tmp_path / "refused.json"
    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "devtools.replay_bc303_t1_witness",
            "--repository",
            str(tmp_path),
            "--output",
            str(output),
        ),
        cwd=REPO / "packing",
        check=False,
        capture_output=True,
    )

    assert result.returncode == 2
    assert result.stdout == b""
    refusal = json.loads(result.stderr)
    assert refusal["status"] == "refused"
    assert not output.exists()
