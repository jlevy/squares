"""wand125's rectangle-density certificates: pins, input binding, and the bounds they carry."""

from __future__ import annotations

import dataclasses
import json
import re
import shutil
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import apply_wand125_rectangles as apply
from devtools import audit_tokoharu_density as tokoharu
from devtools.audit_wand125_rectangles import (
    CASES,
    CASES_2026_09_28,
    CASES_2026_10_01,
    CASES_2026_10_02,
    OCTOBER_1,
    OCTOBER_2,
    PACKETS,
    REPO,
    SEPTEMBER_27,
    SEPTEMBER_28,
    audit_case,
    materialize,
    monotone_bounds,
    read_tree_manifest,
    source_provenance,
    standing,
)
from devtools.check_case_prose import bound_claims, check_bound_claim, parse_front_matter
from devtools.migrate_math import markdown_math
from devtools.retained_data import (
    candidates,
    check_packet,
    compressed_path,
    read_retained_bytes,
    read_retained_text,
)
from sqpack.yamlio import safe_load

FRONTIER = Path(__file__).resolve().parents[1] / "frontier"
#: The two smallest interval inputs, so regeneration stays well inside the test ceiling.
SMALL = (21, 32)
#: The standing certificates 39d8ecc left byte-identical to ad43d29's.
UNCHANGED = (18, 19, 20, 26, 27, 30, 32, 40, 45, 61, 75, 78)
#: The standing certificates 1a25a5e left byte-identical to 39d8ecc's, by the packet
#: that retains each: four are unchanged since ad43d29.
UNCHANGED_2026_10_01 = {
    "2026-09-27": (18, 32, 45, 61),
    "2026-09-28": (21, 37, 51, 52, 57, 58, 60, 67, 71, 72, 73, 91),
}
#: The counts jlevy/squares#281 asks to register. The revision's standing table changed
#: at three more, n = 59, 77 and 78, which the issue leaves to exact values.
ISSUE_281 = (
    *(19, 20, 26, 27, 28, 29, 30, 31, 38, 39, 40, 41, 42, 43, 44, 53, 54, 55, 56),
    *(66, 68, 69, 70, 74, 75, 76, 86, 87, 88, 89, 90, 93, 94, 95),
)
#: One of the smallest interval inputs among the certificates new at 1a25a5e.
SMALL_2026_10_01 = 20
#: The standing certificates b00fc70 raised; no count is new. The import registers the
#: three at n = 20, 42 and 70; the other four are below bounds held separately.
RAISED_2026_10_02 = (20, 42, 59, 70, 77, 91, 93)


def _payload(n: int, frontier: Path = FRONTIER) -> dict:
    text = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---\n", 2)[1])["packing"]


def _value(field: dict) -> Fraction:
    return Fraction(Decimal(str(field["value"])))


@pytest.mark.parametrize(
    ("date", "upstream", "retained", "referenced"),
    [
        ("2026-09-27", 1367, 184, None),
        ("2026-09-28", 2295, 153, 55),
        ("2026-10-01", 2897, 149, 71),
        ("2026-10-02", 3167, 29, 191),
    ],
)
def test_retained_subset_matches_the_pinned_tree(
    date: str, upstream: int, retained: int, referenced: int | None
) -> None:
    packet = PACKETS[date]
    provenance = source_provenance(packet, packet.source)
    assert provenance["kind"] == "verified-retained-subset"
    assert provenance["upstream_files"] == upstream
    assert provenance["files_verified"] == retained
    assert provenance.get("files_referenced") == referenced


def test_the_later_pin_only_adds_files_except_its_readme() -> None:
    earlier = read_tree_manifest(SEPTEMBER_27.tree_manifest)
    later = read_tree_manifest(SEPTEMBER_28.tree_manifest)
    assert {path for path, digest in earlier.items() if later.get(path) != digest} == {
        Path("README.md")
    }


def test_the_october_pin_only_adds_files_except_three_readmes() -> None:
    earlier = read_tree_manifest(SEPTEMBER_28.tree_manifest)
    later = read_tree_manifest(OCTOBER_1.tree_manifest)
    assert {path for path, digest in earlier.items() if later.get(path) != digest} == {
        Path("README.md"),
        Path("point_n21_L5/README.md"),
        Path("point_n21_L5/lean/README.md"),
    }
    assert len(later) - len(earlier) == 602


def test_the_october_2_pin_changes_no_rectangle_file() -> None:
    """b00fc70 adds directories, withdraws one mixed certificate and re-hashes others."""
    earlier = read_tree_manifest(OCTOBER_1.tree_manifest)
    later = read_tree_manifest(OCTOBER_2.tree_manifest)
    changed = {path for path, digest in earlier.items() if later.get(path, digest) != digest}
    removed = {path for path in earlier if path not in later}
    assert len(later) - len(earlier) == 286 - len(removed)
    assert {path.parts[1] for path in removed} == {"mixed_n50_L7318"}
    assert len(changed) == 29
    assert Path("README.md") in changed
    assert not [path for path in changed if path.parts[1:2] and path.parts[1][:5] == "rect_"]
    new = [path for path in later if path not in earlier and path.parts[0] == "certificates"]
    added = {path.parts[1] for path in new if path.parts[1][:5] == "rect_"}
    raised = {CASES_2026_10_02[n][0] for n in RAISED_2026_10_02}
    assert added == raised | {"rect_n93_L973"}


def test_the_october_2_pin_reads_unchanged_certificates_from_three_packets() -> None:
    changed = {n for n, case in CASES_2026_10_02.items() if CASES_2026_10_01[n] != case}
    assert changed == set(RAISED_2026_10_02)
    assert set(CASES_2026_10_02) == set(CASES_2026_10_01)
    for n, (name, side) in CASES_2026_10_02.items():
        assert side >= CASES_2026_10_01[n][1]
        holder = OCTOBER_2.holder(Path("certificates") / name / "verified_angles.jsonl")
        expected = (
            OCTOBER_2
            if n in changed
            else OCTOBER_1.holder(Path("certificates") / name / "verified_angles.jsonl")
        )
        assert holder is expected
    provenance = source_provenance(OCTOBER_2, OCTOBER_2.source)
    assert provenance["referenced_path"] == str(OCTOBER_1.source.relative_to(REPO))
    assert provenance["files_referenced_by_packet"] == {
        str(SEPTEMBER_27.source.relative_to(REPO)): 4 * 4 + 7,
        str(SEPTEMBER_28.source.relative_to(REPO)): 4 * 11,
        str(OCTOBER_1.source.relative_to(REPO)): 4 * 31,
    }


def test_no_rectangle_directory_at_the_october_pin_carries_an_archive() -> None:
    """Issue 281 says each directory holds a tarball; each holds the same seven files."""
    tree = read_tree_manifest(OCTOBER_1.tree_manifest)
    for name, _side in CASES_2026_10_01.values():
        assert {path.name for path in tree if path.parts[:2] == ("certificates", name)} == {
            "certificate_input.txt",
            "certificate_metadata.json",
            "certified_candidate.json",
            "run_verify.py",
            "verification_summary.json",
            "verified_angles.jsonl",
            "verify.cpp",
        }
    assert not [
        path
        for path in tree
        if path.parts[0] == "certificates"
        and path.parts[1].startswith("rect_")
        and path.suffix in {".tar", ".tgz", ".gz", ".xz", ".zip"}
    ]


def test_unchanged_certificates_are_read_from_the_earlier_packet() -> None:
    same = {n for n, case in CASES_2026_09_28.items() if CASES.get(n) == case}
    assert same == set(UNCHANGED)
    for n, (name, side) in CASES_2026_09_28.items():
        assert n not in CASES or side >= CASES[n][1]
        here = SEPTEMBER_28.source / "certificates" / name
        assert here.is_dir() == (n not in same)
        expected = SEPTEMBER_27.source if n in same else SEPTEMBER_28.source
        assert SEPTEMBER_28.case_directory(SEPTEMBER_28.source, name) == (
            expected / "certificates" / name
        )


def test_the_october_pin_reads_unchanged_certificates_from_both_earlier_packets() -> None:
    same = {n for n, case in CASES_2026_10_01.items() if CASES_2026_09_28.get(n) == case}
    assert same == {n for counts in UNCHANGED_2026_10_01.values() for n in counts}
    changed = set(CASES_2026_10_01) - same
    assert changed == {*ISSUE_281, 59, 77, 78}
    assert len(ISSUE_281) == 34
    assert set(CASES_2026_10_01) - set(CASES_2026_09_28) == {87, 90, 93}
    held = {n: date for date, counts in UNCHANGED_2026_10_01.items() for n in counts}
    for n, (name, side) in CASES_2026_10_01.items():
        assert n not in CASES_2026_09_28 or side >= CASES_2026_09_28[n][1]
        assert (OCTOBER_1.source / "certificates" / name).is_dir() == (n in changed)
        expected = PACKETS[held[n]] if n in same else OCTOBER_1
        assert OCTOBER_1.holder(Path("certificates") / name / "verified_angles.jsonl") is (
            expected
        )
        assert OCTOBER_1.case_directory(OCTOBER_1.source, name) == (
            expected.source / "certificates" / name
        )


def test_the_october_manifest_says_which_packet_holds_each_referenced_file() -> None:
    provenance = source_provenance(OCTOBER_1, OCTOBER_1.source)
    assert provenance["referenced_path"] == str(SEPTEMBER_28.source.relative_to(REPO))
    # Four files per unchanged certificate; the licence, the requirements and the five
    # files of docs/ are unchanged since ad43d29.
    assert provenance["files_referenced_by_packet"] == {
        str(SEPTEMBER_27.source.relative_to(REPO)): 4 * 4 + 7,
        str(SEPTEMBER_28.source.relative_to(REPO)): 4 * 12,
    }
    entry = json.loads(OCTOBER_1.manifest.read_text())["sources"][0]
    assert entry["referenced_files_by_packet"] == provenance["files_referenced_by_packet"]
    assert entry["claims"] == [
        f"s({n}) >= {side}" for n, (_name, side) in sorted(CASES_2026_10_01.items())
    ]
    # A packet with a single base says nothing more than its ``referenced_path``.
    assert "files_referenced_by_packet" not in source_provenance(
        SEPTEMBER_28, SEPTEMBER_28.source
    )


def test_a_retained_file_that_differs_from_the_pinned_tree_is_refused(tmp_path: Path) -> None:
    """The October subset rebuilt elsewhere, with one per-angle row changed."""
    scratch = dataclasses.replace(OCTOBER_1, root=tmp_path)
    shutil.copytree(OCTOBER_1.directory, scratch.directory)
    assert source_provenance(scratch, scratch.source)["files_verified"] == 149
    name, _side = CASES_2026_10_01[SMALL_2026_10_01]
    rows = scratch.source / "certificates" / name / "verified_angles.jsonl"
    rows.write_text(rows.read_text().replace('"verified"', '"failed"', 1))
    with pytest.raises(ValueError, match="SHA-256 mismatch against the pinned tree"):
        source_provenance(scratch, scratch.source)


def test_a_certificate_new_at_the_october_pin_binds_to_its_published_input(
    tmp_path: Path,
) -> None:
    n = SMALL_2026_10_01
    name, side = CASES_2026_10_01[n]
    case = OCTOBER_1.source / "certificates" / name
    binding = materialize(case, tmp_path / name)
    tree = read_tree_manifest(OCTOBER_1.tree_manifest)
    assert (
        binding["input_sha256"] == tree[Path("certificates") / name / "certificate_input.txt"]
    )
    report = tokoharu.preflight(tmp_path / name, n, side)
    assert report["status"] == "PASS"
    assert Fraction(report["mass_exact"]) == n - Fraction(1, 100)
    with pytest.raises(ValueError, match="side mismatch"):
        tokoharu.preflight(tmp_path / name, n, CASES_2026_09_28[n][1])


@pytest.mark.parametrize("date", tuple(PACKETS))
@pytest.mark.parametrize("n", SMALL)
def test_regenerated_input_is_the_published_input(date: str, n: int, tmp_path: Path) -> None:
    packet = PACKETS[date]
    name, side = packet.cases[n]
    case = packet.case_directory(packet.source, name)
    binding = materialize(case, tmp_path / name)
    assert (
        binding["input_sha256"]
        == tokoharu.load_json(case / "certificate_metadata.json")["input_sha256"]
    )
    report = tokoharu.preflight(tmp_path / name, n, side)
    assert report["status"] == "PASS"
    assert Fraction(report["mass_exact"]) == n - Fraction(1, 1000 if n in {21, 27} else 100)


def test_a_changed_weight_breaks_the_input_binding(tmp_path: Path) -> None:
    name, _side = CASES[32]
    case = tmp_path / "case"
    shutil.copytree(SEPTEMBER_27.source / "certificates" / name, case)
    path = case / "certified_candidate.json"
    data = json.loads(read_retained_bytes(path))
    compressed_path(path).unlink()
    index = next(i for i, weight in enumerate(data["weights"]) if Fraction(weight) > 0)
    data["weights"][index] = str(Fraction(data["weights"][index]) * 2)
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="published SHA-256"):
        materialize(case, tmp_path / "scratch")


def test_a_side_other_than_the_pinned_one_is_refused(tmp_path: Path) -> None:
    name, side = CASES[21]
    materialize(SEPTEMBER_27.source / "certificates" / name, tmp_path / name)
    with pytest.raises(ValueError, match="side mismatch"):
        tokoharu.preflight(tmp_path / name, 21, side + Fraction(1, 200))


def test_a_candidate_naming_another_count_is_refused(tmp_path: Path) -> None:
    name, _side = CASES_2026_09_28[21]
    case = tmp_path / "certificates" / name
    shutil.copytree(SEPTEMBER_28.source / "certificates" / name, case)
    path = case / "certified_candidate.json"
    data = json.loads(read_retained_bytes(path))
    compressed_path(path).unlink()
    path.write_text(json.dumps(data | {"n": 22}))
    with pytest.raises(ValueError, match="does not declare n = 21"):
        audit_case(
            SEPTEMBER_28, tmp_path, 21, tmp_path / "out", run_replay=False, workers=1, timeout=1
        )


def test_the_standing_certificate_is_the_highest_and_unambiguous(tmp_path: Path) -> None:
    for name, n, side in (("rect_n5_L2", 5, "2.0"), ("rect_n5_L21", 5, "2.1")):
        (tmp_path / "certificates" / name).mkdir(parents=True)
        (tmp_path / "certificates" / name / "certified_candidate.json").write_text(
            f'{{"n": {n}, "L": {side}}}'
        )
    assert standing(tmp_path) == {5: ("rect_n5_L21", Fraction(21, 10))}
    (tmp_path / "certificates" / "rect_n5_L210").mkdir()
    (tmp_path / "certificates" / "rect_n5_L210" / "certified_candidate.json").write_text(
        '{"n": 5, "L": 2.10}'
    )
    with pytest.raises(ValueError, match="share the standing side"):
        standing(tmp_path)


def test_monotone_transfers_follow_the_mass() -> None:
    earlier = monotone_bounds({n: side for n, (_name, side) in CASES.items()})
    assert earlier[77] == (Fraction(89, 10), 76)
    assert all(earlier[n][1] == n for n in CASES if n != 77)
    later = monotone_bounds({n: side for n, (_name, side) in CASES_2026_09_28.items()})
    assert all(later[n][1] == n for n in CASES_2026_09_28 if n != 77)
    inherited = {n: later[n][1] for n in later if later[n][1] != n}
    assert inherited == {
        **dict.fromkeys(range(22, 26), 21),
        **dict.fromkeys(range(33, 37), 32),
        **dict.fromkeys(range(46, 51), 45),
        **dict.fromkeys(range(62, 66), 61),
        77: 76,
        **dict.fromkeys(range(79, 86), 78),
        87: 86,
        90: 89,
        92: 91,
        93: 91,
    }
    assert monotone_bounds({27: Fraction(28, 5)}, upto=29)[29] == (Fraction(28, 5), 27)
    # At 1a25a5e the n31 certificate passes the unchanged direct one at n32, and every
    # other count with a certificate, n77 included, is its own strongest source.
    newest = monotone_bounds({n: side for n, (_name, side) in CASES_2026_10_01.items()})
    assert newest[32] == (Fraction(2381, 400), 31)
    assert {n: newest[n][1] for n in newest if newest[n][1] != n} == {
        **dict.fromkeys(range(22, 26), 21),
        **dict.fromkeys(range(32, 37), 31),
        **dict.fromkeys(range(46, 51), 45),
        **dict.fromkeys(range(62, 66), 61),
        **dict.fromkeys(range(79, 86), 78),
        92: 91,
    }


@pytest.mark.parametrize("date", tuple(PACKETS))
def test_preflight_receipt_covers_every_standing_certificate(date: str) -> None:
    packet = PACKETS[date]
    record = json.loads(read_retained_text(packet.directory / "receipts/preflight/audit.json"))
    assert record["status"] == "PASS"
    assert record["source_revision"] == packet.revision
    assert record["provenance"]["kind"] == "verified-retained-subset"
    assert {
        case["n"]: (case["certificate"], Fraction(case["L"])) for case in record["cases"]
    } == (dict(packet.cases))
    for case in record["cases"]:
        assert Fraction(case["mass_exact"]) < case["n"]
        directory = packet.case_directory(packet.source, case["certificate"])
        metadata = tokoharu.load_json(directory / "certificate_metadata.json")
        assert case["input_sha256"] == metadata["input_sha256"]


@pytest.mark.parametrize("date", tuple(PACKETS))
def test_every_compressed_file_matches_its_table_row(date: str) -> None:
    assert check_packet(PACKETS[date].directory) == []
    assert candidates(PACKETS[date].directory) == []


@pytest.mark.parametrize(
    "date",
    [
        date
        for date, packet in PACKETS.items()
        if (packet.directory / "receipts/replay").is_dir()
    ],
)
def test_replay_receipt_records_complete_accepting_runs(date: str) -> None:
    packet = PACKETS[date]
    replays = packet.directory / "receipts/replay"
    record = json.loads(read_retained_text(replays / "audit.json"))
    preflight = {
        case["n"]: case["input_sha256"]
        for case in json.loads(
            read_retained_text(packet.directory / "receipts/preflight/audit.json")
        )["cases"]
    }
    assert record["cases"]
    for case in record["cases"]:
        summary = case["replay"]["summary"]
        assert case["status"] == "PASS"
        assert summary["status"] == "VERIFIED"
        assert summary["angle_cases"] == 201
        assert summary["input_sha256"] == case["input_sha256"] == preflight[case["n"]]
        assert (
            summary["verifier_source_sha256"]
            == tokoharu.load_json(replays / case["certificate"] / "verification_summary.json")[
                "verifier_source_sha256"
            ]
        )
        rows = (replays / case["certificate"] / "verified_angles.jsonl").read_text()
        assert sorted(json.loads(line)["r"] for line in rows.splitlines()) == list(range(201))


def test_frontier_records_carry_exactly_the_certified_bounds() -> None:
    """Reported lane: every standing certificate; verified lane: only replayed ones."""
    _assert_records_carry_the_certified_bounds(apply.registered(), FRONTIER)


def _assert_records_carry_the_certified_bounds(
    registration: apply.Registration, frontier: Path
) -> None:
    cases = registration.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    proofs = apply.replays(registration)
    verified = (
        monotone_bounds({n: side for n, (side, _) in proofs.items()}, upto=max(cases))
        if proofs
        else {}
    )
    for n, (side, source) in reported.items():
        payload = _payload(n, frontier)
        field = payload["reported_lower_bound"]
        if not set(field["evidence"]) & apply.OURS:
            # Another source's report holds here, at least as strong.
            assert n in registration.superseded_priors or _value(field) >= side
        else:
            holder = apply.owner(cases[source][0])
            assert Fraction(field["exact_form"]) == side
            assert field["source_key"] == holder.source_key
            assert field["evidence"] == [
                holder.report if source == n else holder.monotone_report
            ]
        lower = payload["verified_lower_bound"]
        if set(lower["evidence"]) & apply.OURS:
            proof, origin = verified[n]
            assert Fraction(lower["exact_form"]) == proof
            assert lower["evidence"] == [proofs[origin][1].replay]
        else:
            assert n not in verified or _value(lower) >= verified[n][0]


def test_records_are_what_the_apply_tool_writes() -> None:
    registration = apply.registered()
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in FRONTIER.glob("n-*.md")
    }
    for plan in apply.plans(registration):
        assert apply.apply_case(plan, registration) == texts[plan.n], plan.n
    evidence = (FRONTIER / "evidence.yaml").read_text(encoding="utf-8")
    assert apply.update_evidence(evidence, registration, texts) == evidence


def test_an_older_registration_is_refused_once_a_newer_one_holds(tmp_path: Path) -> None:
    newest = apply.REGISTRATIONS[-1]
    (tmp_path / "n-001.md").write_text(f"---\n  evidence:\n  - {newest.report}\n---\n")
    assert apply.registered(tmp_path) is newest
    with pytest.raises(ValueError, match="older"):
        apply.plans(apply.REGISTRATIONS[0], tmp_path)


def _register(registration: apply.Registration, frontier: Path) -> list[int]:
    written = []
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in frontier.glob("n-*.md")
    }
    for plan in apply.plans(registration, frontier):
        rendered = apply.apply_case(plan, registration, frontier)
        if rendered != texts[plan.n]:
            written.append(plan.n)
            texts[plan.n] = rendered
            (frontier / f"n-{plan.n:03d}.md").write_text(rendered, encoding="utf-8")
    evidence = frontier / "evidence.yaml"
    evidence.write_text(
        apply.update_evidence(evidence.read_text(encoding="utf-8"), registration, texts),
        encoding="utf-8",
    )
    return written


def test_registering_the_newest_packet_is_idempotent_and_never_lowers(tmp_path: Path) -> None:
    """A dry run of the newest registration on a copy of the records.

    Before the real registration it moves the raised and new counts; after it, it is a
    no-op. Either way a second pass writes nothing, and no lower bound falls.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.REGISTRATIONS[-1]
    counts = range(min(newest.packet.cases), max(newest.packet.cases) + 1)
    before = {n: _payload(n, frontier) for n in counts}
    written = _register(newest, frontier)
    for n in counts:
        payload = _payload(n, frontier)
        for field in ("reported_lower_bound", "verified_lower_bound"):
            assert _value(payload[field]) >= _value(before[n][field]), (n, field)
    for n in written:
        body = (frontier / f"n-{n:03d}.md").read_text(encoding="utf-8").split("---\n", 2)[2]
        assert newest.intake in body
    assert _register(newest, frontier) == []
    assert apply.registered(frontier) is newest
    _assert_records_carry_the_certified_bounds(newest, frontier)
    # The report entry covers every certificate this packet is the first to retain, and
    # every case that cites it; the monotone entry exists only if a case cites it.
    entries = {
        entry["id"]: entry
        for entry in safe_load((frontier / "evidence.yaml").read_text(encoding="utf-8"))[
            "evidence"
        ]
    }
    owned = {
        n for n, (name, _side) in newest.packet.cases.items() if apply.owner(name) is newest
    }
    citing = {identifier: _citing(frontier, identifier) for identifier in newest.entries}
    assert set(entries[newest.report]["scope"]["n_values"]) == owned | citing[newest.report]
    assert citing[newest.report] <= owned
    assert entries[newest.report]["source_key"] == newest.source_key
    if citing[newest.monotone_report]:
        assert (
            set(entries[newest.monotone_report]["scope"]["n_values"])
            == (citing[newest.monotone_report])
        )
    else:
        assert newest.monotone_report not in entries


def _citing(frontier: Path, identifier: str) -> set[int]:
    return {
        int(path.stem.removeprefix("n-"))
        for path in frontier.glob("n-*.md")
        if f"- {identifier}\n" in path.read_text(encoding="utf-8").split("---\n", 2)[1]
    }


def test_the_newest_plan_never_lowers_a_bound(tmp_path: Path) -> None:
    """``--plan`` on a copy of the records: every write it announces is a rise or a tie."""
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.REGISTRATIONS[-1]
    reported = monotone_bounds({n: side for n, (_name, side) in newest.packet.cases.items()})
    selected = {plan.n: plan for plan in apply.plans(newest, frontier)}
    for n, plan in selected.items():
        payload = _payload(n, frontier)
        if plan.reported is not None:
            assert plan.reported.side == reported[n][0]
            assert plan.reported.side >= _value(payload["reported_lower_bound"]), n
        if plan.verified is not None:
            assert plan.verified.side >= _value(payload["verified_lower_bound"]), n
    rows = {
        int(cells[1]): cells[5].strip()
        for line in apply.decision_table(newest, frontier).splitlines()[2:]
        if (cells := line.split("|"))
    }
    assert set(rows) == set(reported)
    for n, decision in rows.items():
        writes = n in selected and selected[n].reported is not None
        assert decision.startswith("write reported") == writes, n
        if n in newest.superseded_priors:
            assert decision.startswith("superseded prior"), n


def _hold(frontier: Path, n: int, value: Fraction) -> None:
    """Give case ``n`` a reported lower bound held by another source's evidence."""
    path = frontier / f"n-{n:03d}.md"
    _, front, body = path.read_text(encoding="utf-8").split("---\n", 2)
    block = (
        "  reported_lower_bound:\n"
        f"    value: '{float(value)}'\n"
        f"    exact_form: '{value}'\n"
        "    evidence:\n"
        "    - E-another-source\n"
    )
    front, count = re.subn(
        r"^  reported_lower_bound:\n(?:^    .*\n)*", block, front, count=1, flags=re.MULTILINE
    )
    assert count == 1
    path.write_text(f"---\n{front}---\n{body}", encoding="utf-8")


#: Bounds registered separately from the rectangle certificates of the packet dated by
#: the key, each stronger than what that packet's certificates give at the count:
#: wand125's exact covers at n59 and n77, Evan Daniel's at n60, n61 and n78, and
#: wand125's mixed rectangle-measure certificates at n37, n65, n66, n90 and n92.
STRONGER_REPORTS = {
    "2026-10-01": {
        37: Fraction(161, 25),
        59: Fraction(8),
        60: Fraction(8),
        61: Fraction(8),
        65: Fraction(167, 20),
        66: Fraction(421, 50),
        77: Fraction(9),
        78: Fraction(9),
        90: Fraction(48, 5),
        92: Fraction(969, 100),
    },
    # The same, with wand125's n76 mixed certificate, and the mixed certificates of the
    # packet's own revision at n91 and n92, which carries to n93.
    "2026-10-02": {
        37: Fraction(161, 25),
        59: Fraction(8),
        60: Fraction(8),
        61: Fraction(8),
        65: Fraction(167, 20),
        66: Fraction(421, 50),
        76: Fraction(447, 50),
        77: Fraction(9),
        78: Fraction(9),
        90: Fraction(48, 5),
        91: Fraction(97, 10),
        92: Fraction(39, 4),
        93: Fraction(39, 4),
    },
}


def test_a_stronger_report_from_another_source_keeps_its_field(tmp_path: Path) -> None:
    """The newest registration leaves alone every count another source reports higher.

    Each certificate the packet is the first to retain is tried against a report just
    above it, and the packet's named stronger reports against their own values. Neither
    needs a superseded prior: the comparison with the record decides.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.REGISTRATIONS[-1]
    cases = newest.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    named = STRONGER_REPORTS.get(newest.date, {})
    held = {
        n: side + Fraction(1, 1000)
        for n, (side, source) in reported.items()
        if apply.owner(cases[source][0]) is newest
    } | named
    for n, value in named.items():
        assert value > reported[n][0], n
        assert n not in newest.superseded_priors, n
    for n, value in held.items():
        _hold(frontier, n, value)
    assert not [plan.n for plan in apply.plans(newest, frontier) if plan.reported is not None]
    for n, value in held.items():
        assert _value(_payload(n, frontier)["reported_lower_bound"]) == value
    _register(newest, frontier)
    for n, value in held.items():
        assert _value(_payload(n, frontier)["reported_lower_bound"]) == value, n


@pytest.mark.parametrize("registration", apply.REGISTRATIONS, ids=lambda item: item.date)
def test_a_superseded_prior_hides_no_bound_the_record_lacks(
    registration: apply.Registration,
) -> None:
    """A prior skips its count in both lanes, so both must already hold at least as much.

    Where a stronger bound is only reported, the count is left out of the priors: the
    comparison with the record keeps the reported field, and a replayed rectangle
    certificate can still raise the verified one.
    """
    cases = registration.packet.cases
    reported = monotone_bounds({n: side for n, (_name, side) in cases.items()})
    for n in registration.superseded_priors:
        assert n in cases
        payload = _payload(n)
        for field in ("reported_lower_bound", "verified_lower_bound"):
            assert _value(payload[field]) >= reported[n][0], (n, field)
            assert not set(payload[field]["evidence"]) & apply.OURS, (n, field)


def test_every_packet_has_one_registration_with_its_own_entries() -> None:
    assert [item.date for item in apply.REGISTRATIONS] == list(PACKETS)
    identifiers = [identifier for item in apply.REGISTRATIONS for identifier in item.ids]
    assert len(identifiers) == len(set(identifiers)) == 3 * len(PACKETS)
    assert len({item.source_key for item in apply.REGISTRATIONS}) == len(PACKETS)
    october = apply.BY_DATE["2026-10-01"]
    assert october.packet is OCTOBER_1
    assert october.source_key == "[wand125 rectangle bounds 2026-10-01]"
    assert (october.report, october.monotone_report, october.replay) == (
        "E-wand125-rectangle-2026-10-01-report",
        "E-wand125-rectangle-2026-10-01-monotone-report",
        "E-wand125-rectangle-2026-10-01-source-replay",
    )
    for item in apply.REGISTRATIONS:
        if not item.entries:
            continue
        assert set(item.entries) == {item.report, item.monotone_report}
        for identifier, template in item.entries.items():
            filled = template.replace("{scope}", "{n_values: [1]}").replace(
                "{certificate}", "resources/web/x"
            )
            (entry,) = safe_load("evidence:\n" + filled)["evidence"]
            assert entry["id"] == identifier
            assert entry["source_key"] == item.source_key
            assert entry["source_reviewed"] == item.date
            assert entry["assurance"] == "reported"
            assert item.packet.revision[:7] in entry["limitations"]


def test_the_october_report_entry_says_what_the_packet_holds() -> None:
    """Every figure the entry's prose states, against the table and the receipt."""
    october = apply.BY_DATE["2026-10-01"]
    text = " ".join(october.entries[october.report].split())
    changed = {n for n, case in CASES_2026_10_01.items() if CASES_2026_09_28.get(n) != case}
    same = sorted(set(CASES_2026_10_01) - changed)
    assert f"lists 34 of the {len(changed)}" in text
    first, last = min(changed), max(changed)
    assert (
        f"from {CASES_2026_10_01[first][1]} at n{first} to "
        f"{CASES_2026_10_01[last][1]} at n{last}" in text
    )
    listed = ", ".join(str(n) for n in same[:-1]) + f" and {same[-1]}"
    assert f"The sixteen standing certificates the revision left unchanged, at n{listed}," in (
        text
    )
    record = json.loads(
        read_retained_text(OCTOBER_1.directory / "receipts/preflight/audit.json")
    )
    masses = {case["n"]: Fraction(case["mass_exact"]) for case in record["cases"]}
    assert all(masses[n] == n - Fraction(1, 100) for n in changed)
    assert masses[31] == Fraction(3099, 100) < 32
    assert "The n31 certificate, of mass 3099/100, also gives s(32) >= 2381/400" in text
    factors = []
    for n in changed:
        name, _side = CASES_2026_10_01[n]
        candidate = tokoharu.load_json(
            OCTOBER_1.source / "certificates" / name / "certified_candidate.json"
        )
        factors.append(Fraction(candidate["scaling_experiment"]["factor_exact"]))
    assert Fraction("1.00004") < min(factors)
    assert max(factors) < Fraction("1.04329")
    assert "between 1.00004 and 1.04329" in text


def test_the_october_2_report_entry_says_what_the_packet_holds() -> None:
    """Every figure the entry's prose states, against the table and the receipt."""
    october = apply.BY_DATE["2026-10-02"]
    assert october.packet is OCTOBER_2
    text = " ".join(october.entries[october.report].split())
    sides = (
        ", ".join(f"{CASES_2026_10_02[n][1]} at n{n}" for n in RAISED_2026_10_02[:-1])
        + f" and {CASES_2026_10_02[93][1]} at n93"
    )
    assert f"The seven sides are {sides};" in text
    assert "The 46 standing certificates the revision left unchanged" in text
    record = json.loads(
        read_retained_text(OCTOBER_2.directory / "receipts/preflight/audit.json")
    )
    masses = {case["n"]: Fraction(case["mass_exact"]) for case in record["cases"]}
    assert all(masses[n] == n - Fraction(1, 100) for n in RAISED_2026_10_02)
    factors = [
        Fraction(
            tokoharu.load_json(
                OCTOBER_2.source
                / "certificates"
                / CASES_2026_10_02[n][0]
                / "certified_candidate.json"
            )["scaling_experiment"]["factor_exact"]
        )
        for n in RAISED_2026_10_02
    ]
    assert Fraction("1.00009") < min(factors)
    assert max(factors) < Fraction("1.03993")
    assert "between 1.00009 and 1.03993" in text
    monotone = monotone_bounds({n: side for n, (_name, side) in CASES_2026_10_02.items()})
    earlier = monotone_bounds({n: side for n, (_name, side) in CASES_2026_10_01.items()})
    moved = {n for n in monotone if monotone[n] != earlier[n] and monotone[n][1] != n}
    assert moved == {92}
    assert monotone[92] == (Fraction(3859, 400), 91)


def _paragraphs(path: Path) -> tuple[str, list[str]]:
    _, front, body = path.read_text(encoding="utf-8").split("---\n", 2)
    title, _, rest = body.partition("\n\n")
    return f"---\n{front}---\n{title}", rest.split("\n\n")


def _write_paragraphs(path: Path, head: str, parts: list[str]) -> None:
    path.write_text(f"{head}\n\n" + "\n\n".join(parts), encoding="utf-8")


def _foreign(registration: apply.Registration, n: int) -> str:
    """Another source's intake paragraph of the registration's own date, as the exact-cover
    intakes of 1 October are at n = 59, 60, 61, 77 and 78."""
    return (
        f"{registration.intake} Another source\u2019s\n[exact-cover source](../x/README.md) "
        f"reports $s({n}) = 9$,\nchecked there by its own checker."
    )


def _direct_plan(frontier: Path) -> apply.Plan:
    """The newest registration's plan at the least count it certifies directly.

    A later source's bound can hold every such count, as wand125's check2 certificate of
    6 October does at n = 20, the last one the registration still wrote. So the tool
    writes the registration's own report back into the copy there first, and the
    placement rules are tried on the paragraph the tool writes.
    """
    newest = apply.registered(frontier)
    n = min(
        n
        for n, (name, _side) in newest.packet.cases.items()
        if apply.owner(name) is newest
        and n not in newest.superseded_priors
        and any(newest.wrote(part) for part in _paragraphs(frontier / f"n-{n:03d}.md")[1])
    )
    path = frontier / f"n-{n:03d}.md"
    bound = apply.Bound(newest.packet.cases[n][1], n, newest)
    path.write_text(
        apply.apply_case(apply.Plan(n, bound, None), newest, frontier), encoding="utf-8"
    )
    (plan,) = [plan for plan in apply.plans(newest, frontier) if plan.n == n]
    assert plan.reported == bound
    path.write_text(apply.apply_case(plan, newest, frontier), encoding="utf-8")
    assert apply.apply_case(plan, newest, frontier) == path.read_text(encoding="utf-8")
    return plan


def test_an_intake_is_written_beside_another_sources_paragraph_of_its_date(
    tmp_path: Path,
) -> None:
    """think-e26n: the paragraph is the registration's by source and packet, not by date.

    Writing the 2026-10-01 paragraphs once replaced the exact-cover intakes of the same
    day. Here the registration's own paragraph is gone and another source's of the same
    date stands first under the title: the registration writes its paragraph above it
    and leaves it, and every other paragraph, byte for byte.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.registered(frontier)
    plan = _direct_plan(frontier)
    path = frontier / f"n-{plan.n:03d}.md"
    head, parts = _paragraphs(path)
    (own,) = [part for part in parts if newest.wrote(part)]
    others = [part for part in parts if not newest.wrote(part)]
    foreign = _foreign(newest, plan.n)
    assert foreign.startswith(newest.intake)
    assert not any(item.wrote(foreign) for item in apply.REGISTRATIONS)
    _write_paragraphs(path, head, [foreign, *others])
    rendered = apply.apply_case(plan, newest, frontier)
    path.write_text(rendered, encoding="utf-8")
    after_head, after = _paragraphs(path)
    assert after_head == head
    assert after[1:] == [foreign, *others]
    assert newest.wrote(after[0])
    assert " ".join(after[0].split()) == " ".join(own.split())
    assert apply.apply_case(plan, newest, frontier) == rendered


def test_an_intake_is_rewritten_in_place_below_a_foreign_one(tmp_path: Path) -> None:
    """A same-date paragraph of another source above the registration's own stays above it.

    The tool used to take the first paragraph of its date for its own: it would have
    overwritten this one and left its own paragraph twice.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.registered(frontier)
    plan = _direct_plan(frontier)
    path = frontier / f"n-{plan.n:03d}.md"
    head, parts = _paragraphs(path)
    _write_paragraphs(path, head, [_foreign(newest, plan.n), *parts])
    before = path.read_text(encoding="utf-8")
    assert apply.apply_case(plan, newest, frontier) == before


def test_an_intake_beside_a_stronger_report_quotes_only_what_a_field_holds(
    tmp_path: Path,
) -> None:
    """think-e26n's figures: a side no field holds is a direct certificate, not ``s(n) >=``.

    At n = 59, 60, 77 and 78 another source's report held the reported field above the
    certificate and a replayed smaller-count certificate the verified one, and the tool
    wrote ``s(n) >= side``, which `check_case_prose` refuses, in a code span
    `check_math_markup` refuses. The same arrangement here, at every count where a replay
    gives a verified bound below the certificate's own side.
    """
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.REGISTRATIONS[-1]
    cases = newest.packet.cases
    proofs = apply.replays(newest)
    verified = monotone_bounds({n: side for n, (side, _) in proofs.items()}, upto=max(cases))
    counts = [
        n
        for n, (_name, side) in cases.items()
        if n in verified and verified[n][0] < side and n not in newest.superseded_priors
    ]
    assert counts
    for n in counts:
        _hold(frontier, n, cases[n][1] + Fraction(1, 1000))
        path = frontier / f"n-{n:03d}.md"
        _, front, body = path.read_text(encoding="utf-8").split("---\n", 2)
        front, count = re.subn(
            r"^  verified_lower_bound:\n(?:^    .*\n)*",
            "  verified_lower_bound:\n    value: '1'\n    exact_form: '1'\n"
            "    evidence:\n    - E-another-source\n",
            front,
            count=1,
            flags=re.MULTILINE,
        )
        assert count == 1
        path.write_text(f"---\n{front}---\n{body}", encoding="utf-8")
    planned = {plan.n: plan for plan in apply.plans(newest, frontier)}
    for n in counts:
        plan = planned[n]
        assert plan.reported is None
        assert plan.verified is not None
        path = frontier / f"n-{n:03d}.md"
        path.write_text(apply.apply_case(plan, newest, frontier), encoding="utf-8")
        _, parts = _paragraphs(path)
        (own,) = [part for part in parts if newest.wrote(part)]
        side = cases[n][1]
        assert f"a direct ${side} = " in " ".join(own.split()), n
        assert f"s({n}) >= {side}" not in own, n
        assert markdown_math(own) == own, n
        document = safe_load(path.read_text(encoding="utf-8").split("---\n", 2)[1])
        front_matter = parse_front_matter(document)
        claims = bound_claims(own, n)
        assert [check_bound_claim(claim, front_matter) for claim in claims] == [None] * len(
            claims
        ), n


def test_an_earlier_dated_paragraph_of_another_source_is_never_retired(tmp_path: Path) -> None:
    """Only the registrations' own earlier paragraphs have their claims put in the past."""
    frontier = tmp_path / "frontier"
    shutil.copytree(FRONTIER, frontier)
    newest = apply.registered(frontier)
    plan = _direct_plan(frontier)
    path = frontier / f"n-{plan.n:03d}.md"
    earlier = apply.REGISTRATIONS[apply.REGISTRATIONS.index(newest) - 1]
    foreign = (
        f"{earlier.intake} Another source reports `s({plan.n}) >= 1/1 = 1`, with total "
        "mass `1/2 = 0.5 < 1`, by its own checker."
    )
    assert not any(item.wrote(foreign) for item in apply.REGISTRATIONS)
    head, parts = _paragraphs(path)
    _write_paragraphs(path, head, [*parts[:1], foreign, *parts[1:]])
    before = path.read_text(encoding="utf-8")
    assert apply.apply_case(plan, newest, frontier) == before


def test_importer_preserves_retained_complete_coverage_outside_current_case_citations() -> None:
    evidence = (FRONTIER / "evidence.yaml").read_text(encoding="utf-8")
    texts = {
        int(path.stem.removeprefix("n-")): path.read_text(encoding="utf-8")
        for path in FRONTIER.glob("n-*.md")
    }
    identifier = "E-wand125-rectangle-source-replay"
    registration = next(row for row in apply.REGISTRATIONS if row.replay == identifier)
    assert f"- {identifier}\n" not in texts[32].split("---\n", 2)[1]
    assert 32 in monotone_bounds(apply.replayed(registration), upto=32)
    rewritten = apply.update_evidence(evidence, apply.registered(), texts)
    entry = next(
        row for row in apply.safe_load(rewritten)["evidence"] if row["id"] == identifier
    )
    assert 32 in entry["scope"]["n_values"]
    assert rewritten == evidence
