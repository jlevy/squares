"""Stage 4's negative controls for Hosono's checkers: mutations they refuse.

``campaign/result-import.md`` asks that two mutated certificates be refused by every
checker that accepted the original, with a test holding them. Tokoharu's ``verify.cpp``
(the rectangle replays of ``devtools.audit_wand125_rectangles``) and Hosono's
``mixed_rotated_verify.cpp`` (the mixed replays of
``devtools.audit_wand125_point_and_mixed``) each have one retained control: a standing
certificate and two mutations of it run on one net direction, the original accepted
again there and both mutations refused. Hosono's ``verify_portable.py``, the ``s(21)``
point replay, has two: the source's runner on each of two mutated covers, ending in the
witness replay's own refusal. These tests read the retained receipts and the retained
certificates only; nothing here compiles or runs a checker.

Each mutation is regenerated here from the retained certificate, its digest checked
against the receipt's, and a witness evaluated in exact arithmetic: every mutation
leaves a centre covered below 1 at the control's angle, or a closed unit square holding
less than the ``s(21)`` threshold, so the refusal is the checker's correct answer rather
than a budget running out.
"""

from __future__ import annotations

import hashlib
import json
import re
import shlex
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_tokoharu_density as tokoharu
from devtools import audit_wand125_point_and_mixed as mixed
from devtools import audit_wand125_rectangles as rect
from devtools.retained_data import read_retained_bytes, read_retained_text

#: The first-party readers of a mixed candidate, which the audit keeps private.
semantic_digest = mixed._semantic_digest  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
measure = mixed._n50_measure  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

RECTANGLE_N = 41
MIXED_NAME = "n37"


@cache
def rectangle_receipt() -> dict[str, Any]:
    name, _side = rect.OCTOBER_1.cases[RECTANGLE_N]
    path = rect.OCTOBER_1.directory / "receipts/controls" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


@cache
def mixed_receipt() -> dict[str, Any]:
    path = mixed.MIXED[MIXED_NAME].receipts / "control.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _centre(receipt: dict[str, Any]) -> tuple[Fraction, Fraction]:
    x, y = (Fraction(value) for value in receipt["witness"]["centre"])
    return x, y


def _runs(receipt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["name"]: item for item in receipt["runs"]}


# --------------------------------------------------------------------------- rectangles


def test_the_rectangle_control_runs_the_least_bound_direction_under_the_shipped_flags() -> None:
    receipt = rectangle_receipt()
    packet = rect.OCTOBER_1
    name, side = packet.cases[RECTANGLE_N]
    case = packet.case_directory(packet.source, name)
    rows = [
        json.loads(line)
        for line in read_retained_text(case / "verified_angles.jsonl").splitlines()
    ]
    least = min(rows, key=lambda row: (row["lower_bound"], row["r"]))
    assert receipt["kind"] == rect.CONTROL_KIND
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["packet"], receipt["source_revision"]) == (packet.date, packet.revision)
    assert (receipt["certificate"], receipt["n"], Fraction(receipt["L"])) == (
        name,
        RECTANGLE_N,
        side,
    )
    assert receipt["direction"] == least["r"]
    assert receipt["upstream_row"] == least
    checker = receipt["checker"]
    assert checker["verify_cpp_sha256"] == rect.VERIFY_SHA256
    assert checker["runner_sha256"] == rect.RUNNER_SHA256
    assert checker["compile"] == list(rect.RUNNER_COMPILE)
    runner = (rect.CHECKER / "run_verify.py").read_text()
    assert repr(checker["compile"]).replace(", ", ",") in runner
    assert checker["argv"] == ["./verify", str(least["r"]), str(least["r"])]
    assert "subprocess.run(['./verify',str(r),str(r)]" in runner


def test_the_rectangle_original_is_accepted_with_the_upstream_results() -> None:
    receipt = rectangle_receipt()
    original = _runs(receipt)["original"]
    name, _side = rect.OCTOBER_1.cases[RECTANGLE_N]
    case = rect.OCTOBER_1.case_directory(rect.OCTOBER_1.source, name)
    published = tokoharu.load_json(case / "certificate_metadata.json")["input_sha256"]
    assert original["input_sha256"] == published
    run = original["run"]
    assert run["verdict"] == "ACCEPTED"
    assert run["matches_upstream"]
    assert run["returncode"] == 0
    assert run["command"] == receipt["checker"]["argv"]
    (row,) = run["rows"]
    assert row == json.loads(run["stdout"])
    upstream = receipt["upstream_row"]
    assert row["status"] == "verified"
    assert all(row[key] == upstream[key] for key in ("r", "nodes", "leaves", "lower_bound"))
    assert Fraction(row["lower_bound"]) >= tokoharu.TARGET


@pytest.mark.parametrize("kind", rect.MUTATIONS)
def test_each_rectangle_mutation_is_refused(kind: str) -> None:
    receipt = rectangle_receipt()
    run = _runs(receipt)[kind]["run"]
    assert run["verdict"] == "REFUSED"
    assert run["returncode"] != 0
    assert run["rows"] == []
    assert run["stderr"].startswith(f"UNRESOLVED {receipt['direction']} ")
    assert run["command"] == receipt["checker"]["argv"]


def test_the_rectangle_mutations_are_regenerated_and_provably_uncovered() -> None:
    """Each mutation's input digest, and its exact coverage at the witness, recomputed."""
    receipt = rectangle_receipt()
    runs = _runs(receipt)
    name, side = rect.OCTOBER_1.cases[RECTANGLE_N]
    case = rect.OCTOBER_1.case_directory(rect.OCTOBER_1.source, name)
    candidate = tokoharu.load_json(case / "certified_candidate.json")
    _side, shrink, _total, rects = tokoharu.density(candidate)
    r = receipt["direction"]
    c, s = rect.net_rotation(r * tokoharu.GAP)
    witness = receipt["witness"]
    assert (Fraction(witness["cos"]), Fraction(witness["sin"])) == (c, s)
    assert Fraction(witness["side"]) == shrink
    low, high = side / 2, side - shrink * (c + s) / 2
    assert [Fraction(v) for v in witness["domain"]] == [low, high]
    centre = _centre(receipt)
    assert all(low <= v <= high for v in centre)
    contributions = rect.orbit_contributions(
        rect.candidate_orbits(candidate, rects), centre, c, s, shrink
    )
    covered = sum(contributions.values(), Fraction())
    assert Fraction(witness["coverage_exact"]) == covered >= 1
    top = rect.heaviest(contributions)
    assert runs["drop-top-contributor"]["mutation"]["row"] == top
    assert (
        Fraction(runs["drop-top-contributor"]["mutation"]["contribution_at_witness_exact"])
        == (contributions[top])
    )
    upstream = receipt["upstream_row"]["lower_bound"]
    assert rect.CONTROL_FACTOR * Fraction(upstream) < 1
    assert Fraction(runs["scale-weights"]["mutation"]["factor"]) == rect.CONTROL_FACTOR
    digests = {"original": runs["original"]["input_sha256"]}
    for kind in rect.MUTATIONS:
        mutated = rect.mutate_candidate(candidate, kind, top)
        digest = hashlib.sha256(rect.input_text(mutated).encode()).hexdigest()
        assert digest == runs[kind]["input_sha256"], kind
        digests[kind] = digest
        _s, _b, mass, images = tokoharu.density(mutated)
        assert Fraction(runs[kind]["mass_exact"]) == mass < RECTANGLE_N
        at_witness = rect.coverage_exact(images, centre, c, s, shrink)
        assert Fraction(runs[kind]["witness_coverage_exact"]) == at_witness < 1, kind
    assert len(set(digests.values())) == 3


# --------------------------------------------------------------------------- mixed


@cache
def mixed_candidate() -> dict[str, Any]:
    return json.loads(mixed.mixed_retained(mixed.MIXED[MIXED_NAME])["candidate.json"])


def test_the_mixed_control_runs_the_least_bound_direction_under_the_shipped_flags() -> None:
    receipt = mixed_receipt()
    certificate = mixed.MIXED[MIXED_NAME]
    shipped = mixed.shipped_results(certificate)
    oblique = {int(key): row for key, row in shipped.items() if int(key)}
    least = min(oblique, key=lambda index: (oblique[index]["lower"], index))
    assert receipt["kind"] == mixed.MIXED_CONTROL_KIND
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["certificate"], receipt["revision"], receipt["n"]) == (
        certificate.name,
        certificate.revision,
        certificate.n,
    )
    assert receipt["directory"] == certificate.directory.as_posix()
    assert receipt["index"] == least
    record = receipt["shipped_record"]
    assert (record["nodes"], record["lower"]) == (
        oblique[least]["nodes"],
        oblique[least]["lower"],
    )
    assert record["status"] == "ANGLE_VERIFIED"
    checker = receipt["checker"]
    source = (mixed.MIXED_CODE / "mixed_rotated_verify.cpp").read_bytes()
    assert checker["source_sha256"] == hashlib.sha256(source).hexdigest()
    assert checker["argv"] == ["verify", "input.txt", str(record["nodes"])]
    shipped_compile = (mixed.MIXED_CODE / "mixed_rotated_verify.py").read_text()
    assert "['c++','-O2','-std=c++17','-ffp-contract=off','-fno-fast-math'" in shipped_compile
    assert checker["compile"].endswith("c++ -O2 -std=c++17 -ffp-contract=off -fno-fast-math")
    assert receipt["tarball"]["status"] == "TARBALL_MATCHES_PIN"
    assert receipt["tarball"]["sha256"] == mixed.tarball_pin(certificate)[0]
    assert receipt["bindings"]["status"] == "BUNDLE_BOUND_TO_PACKET"
    assert receipt["preconditions"]["status"] == "DRIVER_PRECONDITIONS_HOLD"
    assert receipt["environment"]["PYTHONOPTIMIZE"] is None


def test_the_mixed_original_is_accepted_with_the_shipped_record() -> None:
    receipt = mixed_receipt()
    original = _runs(receipt)["original"]
    assert original["candidate_digest"] == mixed.MIXED[MIXED_NAME].candidate_digest
    assert original["candidate_digest"] == semantic_digest(mixed_candidate())
    run = original["run"]
    assert run["verdict"] == "ACCEPTED"
    assert (run["returncode"], run["frontier_boxes"]) == (0, 0)
    record = receipt["shipped_record"]
    assert all(
        run["output"][key] == record[key] for key in ("status", "nodes", "leaves", "lower")
    )


@pytest.mark.parametrize("kind", mixed.MIXED_MUTATIONS)
def test_each_mixed_mutation_is_refused(kind: str) -> None:
    receipt = mixed_receipt()
    run = _runs(receipt)[kind]["run"]
    assert run["verdict"] == "REFUSED"
    assert run["returncode"] == 0
    assert run["output"]["status"] == "ANGLE_UNRESOLVED"
    assert run["frontier_boxes"] > 0
    assert run["output"]["nodes"] <= receipt["shipped_record"]["nodes"]
    # The checker stops on the first box it cannot resolve at its depth floor, which is
    # where the coverage crosses gamma at the edge of the deficit the witness proves, so
    # the exact coverage there is gamma to within the checker's own slack.
    assert run["stopped_at"] == "depth floor"
    gap = Fraction(run["stop_centre_coverage_exact"]) - Fraction(receipt["gamma"])
    assert abs(gap) < Fraction(1, 10**6)


def test_the_mixed_mutations_are_regenerated_and_provably_uncovered() -> None:
    """Each mutation's candidate digest, and its exact coverage at the witness, recomputed
    with this repository's own expansion of the measure, not the source's."""
    receipt = mixed_receipt()
    runs = _runs(receipt)
    data = mixed_candidate()
    side, core, items = measure(data)
    witness = receipt["witness"]
    c, s = rect.net_rotation(Fraction(witness["t"]))
    assert (Fraction(witness["cos"]), Fraction(witness["sin"])) == (c, s)
    assert Fraction(witness["side"]) == core
    low, high = (Fraction(v) for v in witness["domain"])
    assert low == side / 2
    centre = _centre(receipt)
    assert all(low <= v <= high for v in centre)
    images = mixed.d4_images(side, items)
    orbits = {row: images[8 * row : 8 * row + 8] for row in range(len(items))}
    contributions = rect.orbit_contributions(orbits, centre, c, s, core)  # pyright: ignore[reportArgumentType]
    covered = sum(contributions.values(), Fraction())
    assert Fraction(witness["coverage_exact"]) == covered >= Fraction(receipt["gamma"])
    top = rect.heaviest(contributions)
    assert runs["drop-top-contributor"]["mutation"]["row"] == top
    assert Fraction(runs["scale-masses"]["mutation"]["factor"]) == rect.CONTROL_FACTOR
    assert rect.CONTROL_FACTOR * Fraction(receipt["shipped_record"]["lower"]) < 1
    digests = {runs["original"]["candidate_digest"]}
    inputs = {runs["original"]["input_sha256"]}
    for kind in mixed.MIXED_MUTATIONS:
        mutated = mixed.mutate_mixed(data, kind, top)
        assert semantic_digest(mutated) == runs[kind]["candidate_digest"], kind
        digests.add(runs[kind]["candidate_digest"])
        inputs.add(runs[kind]["input_sha256"])
        _side, _core, changed = measure(mutated)
        assert sum(item[4] for item in changed) == Fraction(mutated["total_mass"])
        assert Fraction(runs[kind]["total_mass"]) == Fraction(mutated["total_mass"])
        at_witness = rect.coverage_exact(
            mixed.d4_images(side, changed),  # pyright: ignore[reportArgumentType]
            centre,
            c,
            s,
            core,
        )
        assert Fraction(runs[kind]["witness_coverage_exact"]) == at_witness < 1, kind
    assert len(digests) == len(inputs) == 3


# --------------------------------------------------------------------------- s(21) points

#: The refusal each mutation must end in: the root-stage witness replay's own words.
N21_REFUSAL = {
    "drop-heaviest-point": re.compile(r"ValueError: Insufficient witness mass"),
    "move-point": re.compile(r"ValueError: Point containment not proved: (?P<index>\d+)"),
}


@cache
def n21_original() -> bytes:
    return read_retained_bytes(mixed.SOURCE / mixed.N21 / "certificates/n21-original.txt")


@cache
def n21_receipt(kind: str) -> dict[str, Any]:
    path = mixed.N21_CONTROLS / f"n21_control_{kind}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def n21_accepting_bindings() -> dict[str, str]:
    """The script digests of the run that accepted the original, by file name."""
    record = json.loads((mixed.PACKET / "receipts/n21/run-inputs.json").read_text())
    return {Path(path).name: digest for path, digest in record["bindings"].items()}


def test_the_n21_controls_directory_holds_only_its_controls() -> None:
    expected = {
        f"n21_control_{kind}{suffix}"
        for kind in mixed.N21_MUTATIONS
        for suffix in (".json", ".log", "_root.log")
    }
    assert {p.name for p in mixed.N21_CONTROLS.iterdir()} == expected


def test_the_n21_witness_is_the_one_pose_of_the_first_admissible_root() -> None:
    """Root 832 is ``[2/5, 1/2]^2 x [0, 1/16]``; its only admissible pose, centre
    ``(1/2, 1/2)`` at angle zero, is the closed square ``[0, 1]^2``."""
    x, rest = divmod(mixed.N21_WITNESS_ROOT, 200)
    y, t = divmod(rest, 8)
    box = [Fraction(x, 10), Fraction(x + 1, 10), Fraction(y, 10), Fraction(y + 1, 10)]
    assert box == [Fraction(2, 5), Fraction(1, 2), Fraction(2, 5), Fraction(1, 2)]
    assert (t, mixed.N21_WITNESS_CORNER) == (0, (0, 0))


@pytest.mark.parametrize("kind", mixed.N21_MUTATIONS)
def test_each_n21_mutation_is_regenerated_and_provably_uncovered(kind: str) -> None:
    """The mutation, recomputed from the retained cover and read back with the exact
    audit's own reader, changes only the eight rows the receipt names, keeps the measure
    D4-invariant, and leaves the closed square ``[0, 1]^2`` below the threshold."""
    receipt = n21_receipt(kind)
    original = n21_original()
    mutation = mixed.mutate_n21(original, kind)
    assert hashlib.sha256(original).hexdigest() == mixed.N21_HASHES["n21-original.txt"]
    assert receipt["mutation"]["original_sha256"] == mixed.N21_HASHES["n21-original.txt"]
    assert receipt["mutation"]["sha256"] == hashlib.sha256(mutation.data).hexdigest()
    assert receipt["mutation"]["rows"] == list(mutation.rows)
    side, before = points(original)
    _side, after = points(mutation.data)
    rows = [i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    assert rows == list(mutation.rows)
    assert len(rows) == 8
    if kind == "drop-heaviest-point":
        heaviest = max(v for *_, v in before)
        assert all(before[i][2] == heaviest and after[i][2] == 0 for i in rows)
        assert all(before[i][:2] == after[i][:2] for i in rows)
    else:
        step = Fraction(1, 1000)
        assert all(before[i][2] == after[i][2] > 0 for i in rows)
        assert all(
            abs(after[i][0] - before[i][0]) + abs(after[i][1] - before[i][1]) == step
            for i in rows
        )
        assert (Fraction(1), Fraction(7, 10)) in {before[i][:2] for i in rows}
        assert len({(x, y) for x, y, _ in after}) == len(after)
    weights = {(x, y): v for x, y, v in after}
    for (x, y), v in weights.items():
        assert all(weights[p] == v for p in ((side - x, y), (x, side - y), (y, x)))
    q = mixed.N21_THRESHOLD
    total = sum((v for *_, v in after), Fraction(0))
    assert Fraction(receipt["mutation"]["total"]) == total < 21 * q

    def corner(items: list[tuple[Fraction, Fraction, Fraction]]) -> Fraction:
        return sum((v for x, y, v in items if 0 <= x <= 1 and 0 <= y <= 1), Fraction(0))

    witness = receipt["witness"]
    assert witness["root"] == mixed.N21_WITNESS_ROOT
    assert Fraction(witness["threshold"]) == q
    assert Fraction(witness["capture_original_exact"]) == corner(before) >= q
    assert Fraction(witness["capture_mutated_exact"]) == corner(after) < q


@pytest.mark.parametrize("kind", mixed.N21_MUTATIONS)
def test_each_n21_mutation_is_refused_by_the_source_runner(kind: str) -> None:
    """``verify_portable.py``, with the accepting run's bytes and flags, ends in the
    witness replay's own refusal at root 832, every root before it having replayed."""
    receipt = n21_receipt(kind)
    assert receipt["kind"] == mixed.N21_CONTROL_KIND
    assert receipt["status"] == "CONTROL_REFUSED"
    assert (receipt["certificate"], receipt["revision"]) == ("point_n21_L5", mixed.REVISION)
    accepted = n21_accepting_bindings()
    checker = receipt["checker"]
    assert checker["verify_portable_sha256"] == accepted["verify_portable.py"]
    assert checker["assemble_portable_sha256"] == accepted["assemble_portable.py"]
    assert checker["portable_replay_sha256"] == accepted["portable_replay.py"]
    assert checker["workers"] == mixed.N21_WORKERS == 2

    log = (mixed.N21_CONTROLS / receipt["receipt"]).read_text(encoding="utf-8")
    lines = log.splitlines()
    command = shlex.split(lines[0].removeprefix("# command: "))
    assert command[1:3] == ["verify_portable.py", "--bundle"]
    assert command[4:7] == ["--workers", "2", "--out"]
    cwd = lines[1]
    assert cwd.startswith("# cwd: point_n21_L5/ staged by ")
    assert f"verify_portable.py {accepted['verify_portable.py']} " in cwd
    assert f"re-bound to cover {receipt['mutation']['sha256']}, the {kind} mutation" in cwd
    assert cwd.endswith(receipt["mutation"]["detail"])
    rebinding = receipt["rebinding"]
    index = json.loads(read_retained_bytes(mixed.SOURCE / mixed.N21 / "archive-index.json"))
    assert rebinding["pristine_manifest_sha256"] == index["manifest_sha256"]
    assert f"bundle {index['manifest_sha256']} re-bound" in cwd
    assert rebinding["files"] == 75130
    # The cover and the 37,222 records naming its digest; no Python on the replay's path.
    assert rebinding["files_rewritten"] == 37223
    assert rebinding["python_naming_a_replaced_digest"] == [
        "runs/evand_n21_n32_bridge_20260927/results/n21_L5_refit29_scoped_gate/check.py"
    ]
    footer = re.search(r"^# finished \S+; exit (\d+); ", log, re.MULTILINE)
    assert footer is not None
    assert int(footer[1]) == receipt["run"]["exit"] == 1
    assert "RuntimeError: root failed: exit 1; see root.log" in log

    run = receipt["run"]
    assert run["verdict"] == "REFUSED"
    assert run["result"] is None
    assert run["failure"] == {
        "status": "FAILED",
        "error": "RuntimeError('root failed: exit 1; see root.log')",
    }
    exits = [(e["stage"], e["shard"], e["exit_code"]) for e in run["stage_exits"]]
    assert exits == [("root", None, 1)]
    assert run["stage"] == "root"
    assert run["parents_completed"] == mixed.N21_WITNESS_ROOT
    stage_log = (mixed.N21_CONTROLS / f"n21_control_{kind}_root.log").read_text()
    assert stage_log.rstrip().splitlines()[-1] == run["refusal"]
    # Up to root 801 the progress lines are the accepting run's: every root empty.
    accepting = (mixed.PACKET / "receipts/n21/root.log").read_text().splitlines()
    assert stage_log.splitlines()[:9] == accepting[:9]
    assert accepting[8].startswith("801 {'witnesses': 0, 'empty': 801,")
    refusal = N21_REFUSAL[kind].fullmatch(run["refusal"])
    assert refusal is not None
    if "index" in refusal.groupdict():
        assert int(refusal["index"]) in receipt["mutation"]["rows"]
    assert run["raised_in"]["file"] == "replay_physical_point_witness.py"
    assert run["raised_in"]["function"] == "replay"


def points(data: bytes) -> tuple[Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    """The exact audit's reader of a point file: the side, and ``(x, y, weight)``."""
    return mixed._points(data)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
