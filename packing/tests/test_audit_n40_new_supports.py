"""The finite steps of Guzhou0806's s(40) > 3359/500 (#485) hold, and refuse controls.

`devtools.audit_n40_new_supports` reads the retained new density and wand125's original
pool, decides the density's orbit facts and the claim's finite steps in exact rationals,
regenerates both kernel inputs, compares every value with both release receipts and
prices the continuous-pose replay. These tests read retained files only and run no
binary: the axis stage is the packet's receipt, judged as ``check-axis`` judges it.
"""

from __future__ import annotations

import dataclasses
import functools
import json
import shutil
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_continuous_pose as t145
from devtools import audit_n40_new_supports as audit
from devtools.audit_clipped_corner_transfer import text
from devtools.audit_n40_new_supports import CLAIM, RELEASE


@functools.cache
def raw() -> bytes:
    return audit.load_candidate()


@functools.cache
def pool() -> bytes:
    return audit.load_pool()


@functools.cache
def density() -> audit.Density:
    return audit.site_density(raw())


@functools.cache
def facts() -> audit.Facts:
    return audit.facts(density(), CLAIM, RELEASE)


@functools.cache
def support() -> audit.SupportFacts:
    return audit.support_facts(raw(), pool())


@functools.cache
def report() -> dict[str, Any]:
    return audit.check_report()


def least() -> Fraction:
    return audit.least_bound(audit.read_slabs(audit.RECEIPTS["ci"]))[0]


def test_the_inputs_are_the_ones_the_receipts_decided() -> None:
    pose = audit.pose_input(density(), CLAIM, RELEASE)
    assert audit.sha256(pose) == audit.POSE_SHA256
    lines = pose.splitlines()
    assert lines[1] == b"0x1.fea0cf4cbf248p-1 0x1.fea0cf4cbf249p-1"
    assert lines[2] == b"5480"
    assert len(lines) == 5483
    axis = audit.axis_input(audit.axis_rows(density()), CLAIM)
    assert audit.sha256(axis) == audit.AXIS_SHA256
    assert axis.splitlines()[0] == b"6700000000 997318636 1000000000 1000000000 4999 5000 5480"


def test_the_orbits_are_what_the_release_says() -> None:
    s = audit.support_facts(raw(), pool())
    assert s.kinds == {"inherited": 522, "generated": 163}
    assert s.sites == s.positive == s.in_k == s.orbits == 685
    assert s.inherited_exact == 522
    assert s.inherited_distinct
    assert s.generated_outside_pool == 163
    assert s.inherited_positive_before == 427
    assert s.mass == Fraction(3999, 100)
    assert density().terms == 5480


def test_every_finite_check_holds_and_the_receipt_is_this_run() -> None:
    value = report()
    failed = [check["name"] for check in value["checks"] if not check["held"]]
    assert failed == []
    assert value["status"] == "FINITE_STEPS_HOLD"
    retained = (audit.RECEIPT_DIR / "finite-audit.json").read_text(encoding="utf-8")
    assert retained == json.dumps(value, indent=1, sort_keys=True) + "\n"


def test_the_scalars_are_the_releases() -> None:
    assert CLAIM.n * CLAIM.tau - CLAIM.mass == Fraction(1, 500)
    assert CLAIM.L / CLAIM.B == CLAIM.X == Fraction(3359, 500)
    assert Fraction(217911, 99764500) == CLAIM.X - audit.EARLIER
    assert CLAIM.B - CLAIM.A * audit.extent(CLAIM.eps) == audit.NEAR_AXIS_MARGIN
    assert least() == Fraction(9005397816695287, 2**53)
    assert len(CLAIM.slabs()) == 43


def test_the_axis_minimum_is_evaluated_again_at_its_minimiser() -> None:
    f = facts()
    assert f.minimiser == (3490012394, 6201340682)
    assert f.minimum == f.minimiser_capture == 1001486431423867090847280653
    assert f.minimiser_capture_g * 10**27 >= f.minimum
    assert f.nodes == (3293, 3293)
    assert f.evaluation_bound == 627444222088298915573283512797161984 < 2**125


def test_every_control_is_refused() -> None:
    controls = {str(item["control"]): item for item in report()["controls"]}
    assert sorted(controls) == ["D1", "D2", "D3", "G", "G2", "G3", "G4"]
    assert all(item["refused"] for item in controls.values())


def test_a_reweighting_that_keeps_the_orbit_facts_is_refused_by_the_input_digests() -> None:
    """D3 keeps every orbit fact and the mass, so only the binding of the density to
    the inputs both kernels decided can refuse it."""
    d3 = next(item for item in report()["controls"] if item["control"] == "D3")
    failed = set(d3["failed"])
    assert {"pose input: the receipts' input", "axis input: the receipts' input"} <= failed
    assert not any(
        name.startswith("density: ") and name != "density: the release's candidate"
        for name in failed
    )


def test_the_finite_checks_are_t145s_not_copies() -> None:
    for name in (
        "Facts",
        "facts",
        "input_checks",
        "chain_checks",
        "receipt_checks",
        "identity_checks",
        "finite_controls",
        "FiniteControl",
        "manifest",
        "pose_input",
        "crate_premises",
    ):
        assert getattr(audit, name) is getattr(t145, name), name


def _copy_receipt(tmp_path: Path) -> Path:
    folder = tmp_path / "results"
    shutil.copytree(audit.RECEIPTS["ci"], folder)
    return folder


def _failures(checks: Sequence[audit.Check]) -> list[str]:
    return [c.name for c in checks if not c.held]


def _receipt_failures(folder: Path) -> list[str]:
    checks = audit.receipt_checks(
        "ci",
        folder,
        CLAIM,
        facts(),
        release=RELEASE,
        admission=audit.release_admission(support(), facts()),
    )
    return _failures(checks)


def test_a_slab_row_with_output_on_stderr_is_refused(tmp_path: Path) -> None:
    folder = _copy_receipt(tmp_path)
    rows = [json.loads(line) for line in (folder / "slabs.jsonl").read_text().splitlines()]
    rows[11]["stderr_sha256"] = audit.sha256(b"warning\n")
    (folder / "slabs.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows))
    failed = _receipt_failures(folder)
    assert "ci receipt: every slab verified as the contract runs it" in failed


def test_a_threshold_past_the_kernels_input_bounds_is_refused() -> None:
    wide = dataclasses.replace(CLAIM, tau=Fraction(10**8 - 1, 10**8))
    failed = [c.name for c in audit.chain_checks(wide, facts(), least(), RELEASE) if not c.held]
    assert "slabs: the kernel's threshold is at least tau" in failed


def test_a_minimiser_off_the_grid_is_not_a_vertex(tmp_path: Path) -> None:
    folder = tmp_path / "release-ci/results"
    folder.mkdir(parents=True)
    axis = json.loads((audit.RECEIPTS["ci"] / "axis.json").read_text())
    stdout = json.loads(axis["stdout"])
    stdout["minimizer_x_integer"] = str(int(stdout["minimizer_x_integer"]) + 1)
    axis["stdout"] = json.dumps(stdout)
    (folder / "axis.json").write_text(json.dumps(axis))
    moved = audit.facts(density(), CLAIM, dataclasses.replace(RELEASE, packet=tmp_path))
    assert not moved.minimiser_is_vertex
    failed = {c.name for c in audit.input_checks(moved, CLAIM, RELEASE) if not c.held}
    assert "axis: the minimiser is a vertex of the quadrant" in failed


def test_an_inherited_index_outside_the_pool_fails_a_check_rather_than_raising() -> None:
    data = json.loads(raw())
    inherited = [i for i, s in enumerate(data["sites"]) if s["kind"] == "inherited"]
    data["sites"][inherited[0]]["source_index"] = 10**6
    data["sites"][inherited[1]]["source_index"] = -1
    mutant = json.dumps(data).encode()
    s = audit.support_facts(mutant, pool())
    assert s.inherited_exact == 520
    assert s.inherited_positive_before <= 427
    failed = {c.name for c in audit.support_checks(s, audit.site_density(mutant)) if not c.held}
    assert "density: each inherited box is its pool row exactly, no row twice" in failed


def test_an_inherited_box_off_its_pool_row_is_refused() -> None:
    data = json.loads(raw())
    index = next(i for i, s in enumerate(data["sites"]) if s["kind"] == "inherited")
    data["sites"][index]["source_index"] += 1
    mutant = json.dumps(data).encode()
    checks = audit.support_checks(
        audit.support_facts(mutant, pool()), audit.site_density(mutant)
    )
    failed = {check.name for check in checks if not check.held}
    assert "density: each inherited box is its pool row exactly, no row twice" in failed


def test_a_changed_receipt_value_is_refused(tmp_path: Path) -> None:
    folder = _copy_receipt(tmp_path)
    receipt = json.loads((folder / "verification.json").read_text())
    receipt["admission"]["inherited_representatives"] = 523
    (folder / "verification.json").write_text(json.dumps(receipt))
    assert _receipt_failures(folder) == ["ci receipt: admission block"]


#: What the axis stage's judgement checks, the crate's two among them.
AXIS_STAGE_CHECKS = [
    "axis build: the retained source, the release's flags",
    "axis build: with the CI run's compiler, the CI run's binary",
    "axis run: the derived input, every output field both receipts'",
    "axis control H-above: tau = 62593/62500 gives AXIS_TEST_REFUSED",
    "axis control H-below: tau = 500743/500000 gives AXIS_COVERAGE_PROVED",
    "crate: reviewed source for a declared net, the binary embeds it",
    audit.CRATE_DECISION,
]


def test_the_axis_stage_receipt_is_this_run() -> None:
    value = audit.axis_report(audit.RECEIPT_DIR)
    assert [c["name"] for c in value["checks"]] == AXIS_STAGE_CHECKS
    assert all(c["held"] for c in value["checks"])
    retained = (audit.RECEIPT_DIR / "axis-check.json").read_text(encoding="utf-8")
    assert retained == json.dumps(value, indent=1, sort_keys=True) + "\n"


def test_an_axis_stage_without_the_crate_is_refused_unless_asked(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Without the crate's decision the stage fails, and when told not to require it, its
    judgement holds under its own status, never the full stage's (review B5)."""
    record = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())
    del record["crate"]
    (tmp_path / "axis-stage.json").write_text(json.dumps(record))
    value = audit.axis_report(tmp_path)
    assert [c["name"] for c in value["checks"] if not c["held"]] == [audit.CRATE_DECISION]
    assert value["status"] == "AXIS_STAGE_FAILED"
    partial = audit.axis_report(tmp_path, require_crate=False)
    assert [c["name"] for c in partial["checks"]] == AXIS_STAGE_CHECKS[:5]
    assert partial["status"] == audit.KERNEL_ONLY == "AXIS_KERNEL_HOLDS_WITHOUT_CRATE"
    assert audit.main(["check-axis", "--receipts", str(tmp_path), "--without-crate"]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == audit.KERNEL_ONLY


def test_a_control_that_printed_no_json_fails_rather_than_raising(tmp_path: Path) -> None:
    record = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())
    record["runs"]["H-above"]["stdout"] = "terminate called after throwing\n"
    record["crate"]["stdout"] = "thread 'main' panicked\n"
    (tmp_path / "axis-stage.json").write_text(json.dumps(record))
    failed = {c["name"] for c in audit.axis_report(tmp_path)["checks"] if not c["held"]}
    assert failed == {
        "axis control H-above: tau = 62593/62500 gives AXIS_TEST_REFUSED",
        "crate: reviewed source for a declared net, the binary embeds it",
        audit.CRATE_DECISION,
    }


def test_the_axis_stage_receipt_holds_and_a_changed_one_does_not(tmp_path: Path) -> None:
    value = audit.axis_report(audit.RECEIPT_DIR)
    assert [c["name"] for c in value["checks"] if not c["held"]] == []
    assert value["status"] == "AXIS_STAGE_HOLDS"
    record = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())
    output = json.loads(record["runs"]["axis"]["stdout"])
    output["minimum_numerator"] = str(int(output["minimum_numerator"]) - 1)
    record["runs"]["axis"]["stdout"] = json.dumps(output)
    record["runs"]["H-above"]["exit_code"] = 0
    (tmp_path / "axis-stage.json").write_text(json.dumps(record))
    failed = {c["name"] for c in audit.axis_report(tmp_path)["checks"] if not c["held"]}
    assert failed == {
        "axis run: the derived input, every output field both receipts'",
        "axis control H-above: tau = 62593/62500 gives AXIS_TEST_REFUSED",
    }


def test_the_price_is_the_receipts_scaled_by_t145s_replay() -> None:
    assert audit.lpt_makespan([3.0, 3.0, 2.0, 2.0, 2.0], 2) == 7.0
    assert audit.lpt_makespan([5.0, 1.0], 4) == 5.0
    price = report()["price"]
    assert price["receipt_slab_seconds"] == {"local": 2655.3, "ci": 5229.5}
    assert 0.5 < price["predicted_slab_cpu_hours_here"] < 1.0
    walls = price["predicted_wall_seconds_here"]
    assert walls["4"] < walls["2"] < walls["1"] < 3600


# --------------------------------------------------------------------------- the crate
# Review B1: the crate's second decision is bound to this density by the input it read,
# not by its count and mass alone.


def test_the_crate_input_is_the_one_the_facts_derive_and_the_record_names() -> None:
    derived = audit.sha256(audit.crate_axis_input(density()))
    assert derived == facts().crate_sha256["axis-A"]
    crate = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())["crate"]
    assert crate["input_sha256"] == derived


#: Changes to the crate's record or to the premises it printed, each of which must fail
#: the crate's decision: the review's reproduction first, then each field alone.
CRATE_CHANGES: list[list[tuple[str, str, object]]] = [
    [
        ("record", "input_sha256", "0" * 64),
        ("premises", "input_sha256", "1" * 64),
        ("premises", "L", "1/1"),
        ("premises", "n", 1),
        ("premises", "expanded_rectangles", 1),
    ],
    [("record", "input_sha256", "0" * 64)],
    [("premises", "input_sha256", "1" * 64)],
    [("premises", "L", "1/1")],
    [("premises", "n", 1)],
    [("premises", "expanded_rectangles", 1)],
    [("premises", "D", "83/80000")],
    [("premises", "angle_count", 401)],
    [("premises", "net_origin", "default")],
]


@pytest.mark.parametrize(
    "changes",
    CRATE_CHANGES,
    ids=["review-B1", *(f"{c[0][0]}.{c[0][1]}" for c in CRATE_CHANGES[1:])],
)
def test_a_crate_decision_on_another_input_is_refused(
    tmp_path: Path, changes: list[tuple[str, str, object]]
) -> None:
    record = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())
    crate = record["crate"]
    lines = crate["stdout"].splitlines()
    at = next(i for i, line in enumerate(lines) if '"kind"' in line)
    for where, key, value in changes:
        if where == "record":
            crate[key] = value
        else:
            lines[at] = _set(lines[at], ("premises", key), value)
    crate["stdout"] = "\n".join(lines) + "\n"
    (tmp_path / "axis-stage.json").write_text(json.dumps(record))
    judged = audit.axis_report(tmp_path)
    assert [c["name"] for c in judged["checks"] if not c["held"]] == [audit.CRATE_DECISION]
    assert judged["status"] == "AXIS_STAGE_FAILED"


# Review C1 and C3: the crate's decision on another density whose counts, expansion and
# mass are this one's, its two digests agreeing with each other.


def _d3_candidate() -> bytes:
    """Control D3's candidate, built as `density_controls` builds it: a hundredth of site
    0's weight moved to site 1."""
    data = json.loads(raw())
    step = Fraction(data["sites"][0]["weight"]) / 100
    for index, sign in ((0, -1), (1, 1)):
        data["sites"][index]["weight"] = text(
            Fraction(data["sites"][index]["weight"]) + sign * step
        )
    return json.dumps(data).encode()


def _crate_record_on(digest: str) -> dict[str, Any]:
    """The retained axis stage with the crate's input named ``digest`` in both places that
    state it, the record and the crate's own premises, and nothing else changed."""
    record = json.loads((audit.RECEIPT_DIR / "axis-stage.json").read_text())
    crate = record["crate"]
    crate["input_sha256"] = digest
    lines = crate["stdout"].splitlines()
    at = next(i for i, line in enumerate(lines) if '"kind"' in line)
    lines[at] = _set(lines[at], ("premises", "input_sha256"), digest)
    crate["stdout"] = "\n".join(lines) + "\n"
    return record


def _crate_failures(folder: Path, record: dict[str, Any]) -> tuple[list[str], str]:
    (folder / "axis-stage.json").write_text(json.dumps(record))
    judged = audit.axis_report(folder)
    return [c["name"] for c in judged["checks"] if not c["held"]], judged["status"]


def test_d3s_density_has_this_densitys_counts_expansion_and_mass() -> None:
    other = audit.site_density(_d3_candidate())
    assert other.sha256 != audit.CANDIDATE_SHA256 == density().sha256
    assert len(other.rows) == len(density().rows) == 685
    assert len(other.merged) == len(density().merged) == 5424
    assert sum(w for _, w in other.rows) == sum(w for _, w in density().rows) == CLAIM.mass
    assert audit.crate_axis_input(other) != audit.crate_axis_input(density())


def test_a_crate_decision_on_d3s_density_is_refused_by_the_derived_input(
    tmp_path: Path,
) -> None:
    """Review C1: only the comparison with the input derived here from the retained
    density can refuse a decision on D3's, whose digests agree with each other."""
    derived = audit.sha256(audit.crate_axis_input(density()))
    assert _crate_failures(tmp_path, _crate_record_on(derived)) == ([], "AXIS_STAGE_HOLDS")
    other = audit.sha256(audit.crate_axis_input(audit.site_density(_d3_candidate())))
    assert _crate_failures(tmp_path, _crate_record_on(other)) == (
        [audit.CRATE_DECISION],
        "AXIS_STAGE_FAILED",
    )


def test_a_crate_decision_on_another_candidate_on_disk_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review C3: with D3's candidate read as the retained one and the crate's decision on
    the input derived from it, every digest agrees, so only the candidate's own digest,
    which must be the release's, can refuse it."""
    candidate = _d3_candidate()
    other = audit.sha256(audit.crate_axis_input(audit.site_density(candidate)))
    monkeypatch.setattr(audit, "load_candidate", lambda: candidate)
    assert _crate_failures(tmp_path, _crate_record_on(other)) == (
        [audit.CRATE_DECISION],
        "AXIS_STAGE_FAILED",
    )


# --------------------------------------------------------------------------- the kernels
# Review B2, B3 and B6: the shared kernel files and the shared pose binary, each read from
# both packets' records and each refused when one side differs.


def _copy_kernel_records(tmp_path: Path) -> tuple[audit.Release, audit.Release]:
    """What `kernel_checks` reads of both packets, copied, as both releases at the copies."""
    copies: list[audit.Release] = []
    for name, release in (("ours", RELEASE), ("t145", t145.RELEASE)):
        packet = tmp_path / name
        parts = [
            "acquisition/upstream-subtree.sha256",
            "release-ci/results/verification.json",
            *(f"source/{path}" for path in audit.SHARED_WITH_T145),
        ]
        if name == "t145":
            parts.append("receipts/builds.json")
        for part in parts:
            (packet / part).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(release.packet / part, packet / part)
        copies.append(dataclasses.replace(release, packet=packet))
    return copies[0], copies[1]


def _drop_oracle_from_both_manifests(root: Path) -> None:
    for name in ("ours", "t145"):
        path = root / name / "acquisition/upstream-subtree.sha256"
        kept = [line for line in path.read_text().splitlines() if "tests/oracle.py" not in line]
        path.write_text("".join(f"{line}\n" for line in kept))


def _append_a_byte(path: Path) -> None:
    path.write_bytes(path.read_bytes() + b"\n")


def _append_a_byte_to_both(root: Path, path: str) -> None:
    """Both packets' retained copies of ``path`` changed alike, both manifests not: only
    the hash of the retained bytes against the manifest can see it (review C2)."""
    for name in ("ours", "t145"):
        _append_a_byte(root / name / "source" / path)


KERNELS = "kernels: byte for byte T-145's, which its review read"
POSE_BINARY = "kernels: the CI run's pose binary is T-145's, which its replay rebuilt"
KERNEL_CHANGES: list[tuple[str, Callable[[Path], None], str]] = [
    ("a shared file in neither manifest", _drop_oracle_from_both_manifests, KERNELS),
    (
        "our retained kernel not the manifest's",
        lambda root: _append_a_byte(root / "ours/source/verifier/continuous_pose.cpp"),
        KERNELS,
    ),
    (
        "T-145's retained file not ours",
        lambda root: _append_a_byte(root / "t145/source/tests/oracle.py"),
        KERNELS,
    ),
    (
        "both retained kernels changed alike, neither manifest",
        lambda root: _append_a_byte_to_both(root, "verifier/continuous_pose.cpp"),
        KERNELS,
    ),
    (
        "our CI receipt's pose binary",
        lambda root: _edit(
            root / "ours/release-ci/results/verification.json", ("binaries", "pose"), "0" * 64
        ),
        POSE_BINARY,
    ),
    (
        "T-145's CI receipt's pose binary",
        lambda root: _edit(
            root / "t145/release-ci/results/verification.json", ("binaries", "pose"), "0" * 64
        ),
        POSE_BINARY,
    ),
    (
        "T-145's replay built another binary",
        lambda root: _edit(
            root / "t145/receipts/builds.json", ("builds", "pose", "binary_sha256"), "0" * 64
        ),
        POSE_BINARY,
    ),
    (
        "T-145's replay built on another compiler",
        lambda root: _edit(root / "t145/receipts/builds.json", ("compiler",), "g++ 15.2.0"),
        POSE_BINARY,
    ),
]


def test_the_kernel_checks_hold_on_copies_of_both_packets(tmp_path: Path) -> None:
    ours, theirs = _copy_kernel_records(tmp_path)
    assert _failures(audit.kernel_checks(ours, theirs)) == []
    assert [c.name for c in audit.kernel_checks()] == [KERNELS, POSE_BINARY]


@pytest.mark.parametrize(
    ("change", "check"),
    [(change, check) for _, change, check in KERNEL_CHANGES],
    ids=[name for name, _, _ in KERNEL_CHANGES],
)
def test_a_kernel_or_binary_that_differs_on_one_side_is_refused(
    tmp_path: Path, change: Callable[[Path], None], check: str
) -> None:
    ours, theirs = _copy_kernel_records(tmp_path)
    change(tmp_path)
    assert _failures(audit.kernel_checks(ours, theirs)) == [check]


def test_the_pose_binary_literals_are_compared(tmp_path: Path) -> None:
    ours, theirs = _copy_kernel_records(tmp_path)
    other = dataclasses.replace(theirs, ci_binaries={**theirs.ci_binaries, "pose": "0" * 64})
    assert _failures(audit.kernel_checks(ours, other)) == [POSE_BINARY]


# --------------------------------------------------------------------------- mutants
# Review B4: a mutant of each value the finite checks compare, each refused by the check
# named for it, so that each is shown to bite and none can hold on absence.


def _set(value: Any, keys: Sequence[str | int], new: object) -> Any:
    """``value`` with the field at ``keys`` replaced. A string met on the way, such as a
    record's ``stdout``, is read as the JSON it holds and written back."""
    if not keys:
        return new
    if isinstance(value, str):
        return json.dumps(_set(json.loads(value), keys, new))
    value[keys[0]] = _set(value[keys[0]], keys[1:], new)
    return value


def _edit(path: Path, keys: Sequence[str | int], new: object) -> None:
    """One field of a JSON record replaced; in JSON Lines the first key is the row."""
    if path.suffix == ".jsonl":
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        path.write_text("".join(json.dumps(row) + "\n" for row in _set(rows, keys, new)))
    else:
        path.write_text(json.dumps(_set(json.loads(path.read_text()), keys, new)))


def _restate_digests(folder: Path) -> None:
    """The receipt's digests of its slab and axis records restated for the records as
    they now are, so that only the check of the changed field can see the change."""
    path = folder / "verification.json"
    receipt = json.loads(path.read_text())
    receipt["slabs_sha256"] = audit.sha256((folder / "slabs.jsonl").read_bytes())
    receipt["axis_sha256"] = audit.sha256((folder / "axis.json").read_bytes())
    path.write_text(json.dumps(receipt))


SLAB_ROWS = "ci receipt: every slab verified as the contract runs it"
AXIS_RUN = "ci receipt: the axis run"
#: One field of each block of the CI receipt, of one slab row and of the axis record,
#: with the one check that must refuse it.
RECEIPT_FIELDS: list[tuple[str, tuple[str | int, ...], object, str]] = [
    ("verification.json", ("parameters", "threshold"), "4999/5001", "ci receipt: parameters"),
    ("verification.json", ("scalar", "counting_margin"), "1/499", "ci receipt: scalar block"),
    (
        "verification.json",
        ("admission", "pose_input_sha256"),
        "0" * 64,
        "ci receipt: admission block",
    ),
    (
        "verification.json",
        ("coverage", "leaves"),
        1,
        "ci receipt: coverage block is the slabs' totals",
    ),
    (
        "verification.json",
        ("axis", "margin"),
        "0",
        "ci receipt: axis block is the axis output's",
    ),
    (
        "verification.json",
        ("slabs_sha256",),
        "0" * 64,
        "ci receipt: slab and axis records by digest",
    ),
    (
        "verification.json",
        ("source_sha256", "verifier/continuous_pose.cpp"),
        "0" * 64,
        "ci receipt: the source it ran is the retained tree",
    ),
    ("verification.json", ("status",), "REPLAYED", "ci receipt: status and flags"),
    ("verification.json", ("workers",), 2, "ci receipt: status and flags"),
    (
        "verification.json",
        ("stages", 6, "exit_code"),
        99,
        "ci receipt: the fourteen stages exited as expected",
    ),
    ("verification.json", ("binaries", "axis"), "0" * 64, AXIS_RUN),
    ("verification.json", ("binaries", "pose"), "0" * 64, SLAB_ROWS),
    ("slabs.jsonl", (7, "index"), 8, SLAB_ROWS),
    ("slabs.jsonl", (7, "arguments", 5), "29999999", SLAB_ROWS),
    ("slabs.jsonl", (7, "exit_code"), 3, SLAB_ROWS),
    ("slabs.jsonl", (7, "timed_out"), True, SLAB_ROWS),
    ("slabs.jsonl", (7, "input_sha256"), "0" * 64, SLAB_ROWS),
    ("slabs.jsonl", (7, "source_sha256"), "0" * 64, SLAB_ROWS),
    ("slabs.jsonl", (7, "binary_sha256"), "0" * 64, SLAB_ROWS),
    ("slabs.jsonl", (7, "stdout", "status"), "unresolved", SLAB_ROWS),
    ("slabs.jsonl", (7, "stdout", "pl"), 2, SLAB_ROWS),
    ("axis.json", ("exit_code",), 2, AXIS_RUN),
    ("axis.json", ("input_sha256",), "0" * 64, AXIS_RUN),
    ("axis.json", ("source_sha256",), "0" * 64, AXIS_RUN),
    ("axis.json", ("stdout", "direct_sum_matches"), False, AXIS_RUN),
    ("axis.json", ("stdout", "evaluation_abs_bound"), "1", AXIS_RUN),
]


@pytest.mark.parametrize(
    ("record", "keys", "value", "check"),
    RECEIPT_FIELDS,
    ids=[f"{r}:{'.'.join(map(str, k))}" for r, k, _, _ in RECEIPT_FIELDS],
)
def test_a_changed_receipt_field_is_refused_by_its_check(
    tmp_path: Path, record: str, keys: tuple[str | int, ...], value: object, check: str
) -> None:
    folder = _copy_receipt(tmp_path)
    _edit(folder / record, keys, value)
    if record != "verification.json":
        _restate_digests(folder)
    assert _receipt_failures(folder) == [check]


def _copy_receipts(tmp_path: Path) -> audit.Release:
    """What `identity_checks` reads of the packet, copied, as the release at the copy."""
    for part in ("source/results", "release-ci/results"):
        shutil.copytree(RELEASE.packet / part, tmp_path / part)
    for part in ("source/SHA256SUMS", "release-ci/SHA256SUMS"):
        shutil.copyfile(RELEASE.packet / part, tmp_path / part)
    return dataclasses.replace(RELEASE, packet=tmp_path)


LOCAL_RUN = "local receipt: the producer's run, not CI"
CI_RUN = f"ci receipt: run {RELEASE.ci_run} on the pin, the binaries g++ 13.3.0 rebuilds"
SUMS = "release-ci SHA256SUMS: the tree's but for the four results lines"
SAME_SLABS = "receipts: every slab identical apart from timing and the binary"
#: One field of either receipt that tells them apart or must agree between them, with
#: the checks that must refuse it. A change to the CI receipt also leaves its digest out
#: of the release's ``SHA256SUMS``.
IDENTITY_FIELDS: list[tuple[str, tuple[str | int, ...], object, list[str]]] = [
    ("source/results/verification.json", ("source_commit",), audit.PIN, [LOCAL_RUN]),
    ("source/results/verification.json", ("compiler",), audit.CI_COMPILER, [LOCAL_RUN]),
    ("release-ci/results/verification.json", ("source_commit",), "0" * 40, [CI_RUN, SUMS]),
    ("release-ci/results/verification.json", ("binaries", "pose"), "0" * 64, [CI_RUN, SUMS]),
    ("source/results/slabs.jsonl", (7, "stdout", "nodes"), 1, [SAME_SLABS]),
    ("source/results/slabs.jsonl", (7, "arguments", 5), "29999999", [SAME_SLABS]),
    (
        "source/results/axis.json",
        ("stdout", "x_nodes"),
        "3292",
        ["receipts: the axis outputs identical"],
    ),
]


def test_the_identity_checks_hold_on_a_copy_and_refuse_a_changed_sums_line(
    tmp_path: Path,
) -> None:
    release = _copy_receipts(tmp_path)
    assert _failures(audit.identity_checks(release)) == []
    sums = tmp_path / "release-ci/SHA256SUMS"
    lines = sums.read_text().splitlines()
    at = next(i for i, line in enumerate(lines) if line.endswith("results/slabs.jsonl"))
    lines[at] = "0" * 64 + lines[at][64:]
    sums.write_text("".join(f"{line}\n" for line in lines))
    assert _failures(audit.identity_checks(release)) == [SUMS]


@pytest.mark.parametrize(
    ("record", "keys", "value", "checks"),
    IDENTITY_FIELDS,
    ids=[f"{r}:{'.'.join(map(str, k))}" for r, k, _, _ in IDENTITY_FIELDS],
)
def test_a_changed_receipt_field_is_refused_by_the_identity_checks(
    tmp_path: Path, record: str, keys: tuple[str | int, ...], value: object, checks: list[str]
) -> None:
    release = _copy_receipts(tmp_path)
    _edit(tmp_path / record, keys, value)
    assert _failures(audit.identity_checks(release)) == checks


CANDIDATE = "density: the release's candidate"
#: A density changed past what the release states of it: a box past ``L``, a header
#: value, and a weight of zero.
DENSITY_FIELDS: list[tuple[tuple[str | int, ...], object, list[str]]] = [
    (
        ("sites", 522, "box", 2),
        "68/10",
        [CANDIDATE, "density: every box is a proper rectangle in K"],
    ),
    (("threshold",), "4999/5001", [CANDIDATE, "density: its header is the claim's"]),
    (
        ("sites", 0, "weight"),
        "0",
        [
            CANDIDATE,
            "density: 685 positive orbits, 522 inherited and 163 generated",
            "density: the weights sum to M",
        ],
    ),
]


@pytest.mark.parametrize(
    ("keys", "value", "checks"),
    DENSITY_FIELDS,
    ids=[".".join(map(str, k)) for k, _, _ in DENSITY_FIELDS],
)
def test_a_density_outside_the_releases_statement_is_refused(
    keys: tuple[str | int, ...], value: object, checks: list[str]
) -> None:
    mutant = json.dumps(_set(json.loads(raw()), keys, value)).encode()
    s = audit.support_facts(mutant, pool())
    assert _failures(audit.support_checks(s, audit.site_density(mutant))) == checks


def test_a_changed_pool_or_statement_is_refused() -> None:
    """The three checks `check_report` makes beside the shared ones: the pool's digest,
    PROOF.md's near-axis margin and the retained ``parameters.json``."""
    assert audit.pool_check(pool()).held
    data = json.loads(pool())
    data["weights"][0] = "1"
    assert not audit.pool_check(json.dumps(data).encode()).held
    parameters = json.loads(audit.PARAMETERS.read_text())
    assert _failures(audit.statement_checks(parameters)) == []
    assert _failures(audit.statement_checks({**parameters, "threshold": "4999/5001"})) == [
        "retained parameters.json is the claim"
    ]
    moved = dataclasses.replace(CLAIM, A=Fraction(249329658, 250000000))
    assert _failures(audit.statement_checks(parameters, moved)) == [
        "near-axis: B - A W(eps) is PROOF.md's margin",
        "retained parameters.json is the claim",
    ]


#: A wrong value of each fact the input checks read, with the one check that must
#: refuse it: these checks judge the inputs regenerated here, so a mutant of the density
#: cannot reach them, and a wrong fact is how a broken builder would show.
FACT_FIELDS: list[tuple[str, object, str]] = [
    ("terms", 5479, "density: D4 expansion"),
    ("distinct", 5423, "density: D4 expansion"),
    ("invariant", False, "density: D4-invariant"),
    ("integral", Fraction(40), "density: integral of g is M"),
    ("pose_sha256", "0" * 64, "pose input: the receipts' input"),
    ("pose_is_expansion", False, "pose input: its terms are the D4 expansion"),
    ("enclosures", (27401, 27402), "pose input: every number brackets its rational"),
    ("axis_sha256", "0" * 64, "axis input: the receipts' input"),
    ("axis_is_expansion", False, "axis input: its terms are the D4 expansion"),
    ("axis_dropped", 1, "axis input: 5480 rows, none dropped"),
    ("axis_dominated", False, "axis input: dominated by g"),
    ("axis_quarter_invariant", False, "axis input: quarter-turn invariant"),
    ("dominated_mass", CLAIM.mass, "axis input: the dominated mass is below M"),
    ("evaluation_bound", 2**125, "axis input: the int128 guards"),
    ("nodes", (3293, 3294), "axis input: the grid of breakpoints"),
    ("minimiser_is_vertex", False, "axis: the minimiser is a vertex of the quadrant"),
    ("minimiser_capture", 0, "axis: the capture at the minimiser, evaluated here"),
    ("minimiser_capture_g", Fraction(0), "axis: g captures at least as much there"),
]


@pytest.mark.parametrize(
    ("field", "value", "check"), FACT_FIELDS, ids=[f for f, _, _ in FACT_FIELDS]
)
def test_a_wrong_fact_is_refused_by_its_input_check(
    field: str, value: object, check: str
) -> None:
    wrong = dataclasses.replace(facts(), **{field: value})
    assert _failures(audit.input_checks(wrong, CLAIM, RELEASE)) == [check]


#: The scalar chain's checks that no finite control reaches: the claimed bound, the
#: domain, the near-axis order, and the receipts' least leaf bound and axis minimum.
CHAIN_CHANGES: list[tuple[str, dict[str, Fraction], Fraction, int, list[str]]] = [
    (
        "X not L over B",
        {"X": Fraction(3360, 500)},
        Fraction(0),
        0,
        ["claim: X = L / B", "claim: X raises the earlier bound"],
    ),
    (
        "B past L over sqrt 2",
        {"B": Fraction(48, 10)},
        Fraction(0),
        0,
        ["claim: X = L / B", "domain: E > 0 at every angle"],
    ),
    (
        "A past B",
        {"A": Fraction(1)},
        Fraction(0),
        0,
        ["near-axis: W increases on [0, eps] and A <= B", "near-axis: A W(eps) <= B"],
    ),
    (
        "least leaf bound below the threshold",
        {},
        Fraction(-1, 10**9),
        0,
        ["slabs: the receipts' least leaf bound is at least the threshold"],
    ),
    (
        "axis minimum below tau",
        {},
        Fraction(0),
        -(2 * 10**24),
        ["axis: the receipts' minimum is at least tau"],
    ),
]


@pytest.mark.parametrize(
    ("changes", "shift", "drop", "checks"),
    [(c, s, d, k) for _, c, s, d, k in CHAIN_CHANGES],
    ids=[name for name, _, _, _, _ in CHAIN_CHANGES],
)
def test_a_changed_scalar_is_refused_by_the_chain(
    changes: dict[str, Fraction], shift: Fraction, drop: int, checks: list[str]
) -> None:
    claim = dataclasses.replace(CLAIM, **changes)
    f = dataclasses.replace(facts(), minimum=facts().minimum + drop)
    assert _failures(audit.chain_checks(claim, f, least() + shift, RELEASE)) == checks
