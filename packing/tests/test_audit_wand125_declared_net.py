"""The first-party audit of wand125's mixed certificate on a declared net (jlevy/squares#366).

`devtools.audit_wand125_declared_net` recomputes `mixed_n18_L470`'s exact premises from
the retained files, lemma N0's five among them, and refuses a copy whose net, mass or
stated facts are changed. Its bundle receipt binds the source's own runs to the declared
net, and its comparison passes a replay only when every regenerated record is the
shipped one.
"""

from __future__ import annotations

import importlib
import json
import math
import os
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_wand125_declared_net as declared
from devtools.retained_data import read_retained_bytes


def test_the_audit_recomputes_to_its_receipt() -> None:
    assert declared.main(["audit", "--check"]) == 0


@pytest.mark.parametrize("key", sorted(declared.CERTIFICATES))
def test_every_certificate_recomputes_to_its_receipt(key: str) -> None:
    assert declared.main(["audit", "--certificate", key, "--check"]) == 0


def test_the_finer_net_of_6_october_holds_lemma_n0() -> None:
    """mixed_n18_L4704 (T-099): core 1999/2000 on 832 tangents of step 1/2006."""
    facts = declared.audit(key="n18-L4704")
    assert facts["status"] == "EXACT_PREMISES_HOLD"
    assert all(facts["premises"].values())
    assert facts["net"]["step"] == "1/2006"
    assert facts["net"]["count"] == "832"
    assert facts["net"]["rotated_side_upper"] == "4011993/4012000"
    assert facts["net"]["endpoint_check"] == "497/4024036"
    assert (facts["mass"], facts["rectangles"]) == ("1799999/100000", 209)
    assert facts["oblique_records"] == 831
    n19 = declared.audit(key="n19-L48229")
    assert (n19["mass"], n19["rectangles"], n19["oblique_records"]) == (
        "1899999/100000",
        313,
        415,
    )
    assert n19["net"] == declared.audit()["net"]


@pytest.mark.parametrize(
    ("key", "listed", "rows"), [("n18-L4704", 2515, 209), ("n19-L48229", 1267, 313)]
)
def test_each_bundle_of_6_october_is_bound_to_its_net(key: str, listed: int, rows: int) -> None:
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "bundle.json").read_text(encoding="utf-8"))
    facts = declared.audit(key=key)
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert record["certificate"] == stated.name
    assert (record["listed_files"], record["code_files"]) == (listed, 10)
    assert record["oblique_inputs"] == facts["oblique_records"]
    assert record["rectangle_images"] == 8 * rows
    assert record["upstream_oblique_nodes"] == facts["oblique_nodes"]


def test_the_one_retained_driver_differs_from_the_n50_copy_only_in_its_worker_cap() -> None:
    """mixed_n18_L4704's code/verify_mixed_full_proof.py is retained because one line
    differs from the mixed_n50_L740 copy: the bound on --workers, 16 where it was 3."""
    stated = declared.CERTIFICATES["n18-L4704"]
    assert stated.own_code == {"verify_mixed_full_proof.py"}
    own = stated.code_reference("verify_mixed_full_proof.py").read_text().splitlines()
    n50 = (declared.N50_DIRECTORY / "code/verify_mixed_full_proof.py").read_text().splitlines()
    assert len(own) == len(n50)
    changed = [(a, b) for a, b in zip(n50, own, strict=True) if a != b]
    assert len(changed) == 1
    before, after = changed[0]
    assert "assert 1<=a.workers<=3;" in before
    assert after == before.replace("a.workers<=3", "a.workers<=16")


@pytest.mark.parametrize("key", ["n18-L4704", "n19-L48229"])
def test_each_sample_of_the_source_checker_returned_the_shipped_records(key: str) -> None:
    stated = declared.CERTIFICATES[key]
    receipts = sorted((stated.receipts / "sample").glob("nodes-*.json"))
    assert receipts
    for path in receipts:
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["status"] == "SAMPLE_REPLAYED", path.name
        assert record["certificate"] == stated.name
        assert record["binding"]["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
        assert record["candidate_digest"] == declared.audit(key=key)["candidate_digest"]
        assert record["tarball"]["sha256"] == stated.tarball_pin()[0]
        assert [row["index"] for row in record["rows"]] == record["nodes"]
        assert all(row["matches_upstream"] for row in record["rows"]), path.name


@pytest.mark.parametrize("key", ["n18-L4704", "n19-L48229"])
def test_each_corrupted_net_fails_lemma_n0_or_the_format(key: str) -> None:
    """The three corrupted declarations `control` runs the source's net check on."""
    candidate = json.loads(
        read_retained_bytes(declared.CERTIFICATES[key].directory / "candidate.json")
    )
    for label, variant in declared.corrupted_nets(candidate).items():
        net = variant["proof_net"]
        if label == "extra-field":
            assert set(net) == {"step", "last", "offset"}
            continue
        step, count = Fraction(net["step"]), int(net["last"]) + 1
        checks = declared.premises(
            declared.net_facts(Fraction(candidate["B"]), step, count), count
        )
        failing = {name for name, held in checks.items() if not held}
        assert failing == (
            {"b_core_fits", "e_tangent_form"}
            if label == "coarser-step"
            else {"c_reaches_past_pi_over_4"}
        ), (key, label)


def test_the_audit_holds_lemma_n0_on_the_declared_net() -> None:
    facts = declared.audit()
    assert facts["status"] == "EXACT_PREMISES_HOLD"
    assert all(facts["premises"].values())
    assert facts["net"]["step"] == "1/1001"
    assert facts["net"]["count"] == "416"
    assert facts["net"]["rotated_side_upper"] == "500499/500500"
    assert facts["net"]["endpoint_check"] == "1054/1002001"
    assert facts["mass"] == "1799999/100000"
    assert facts["oblique_records"] == 415


def test_the_bundle_receipt_binds_every_oblique_input_to_the_declared_net() -> None:
    record = json.loads((declared.RECEIPTS / "bundle.json").read_text(encoding="utf-8"))
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert (record["listed_files"], record["code_files"]) == (1266, 10)
    assert record["oblique_inputs"] == 415
    assert record["rectangle_images"] == 8 * 136
    assert record["upstream_oblique_nodes"] == declared.audit()["oblique_nodes"]


def copy_directory(tmp_path: Path) -> Path:
    """The retained files as plain JSON in a scratch directory."""
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        (tmp_path / name).write_bytes(read_retained_bytes(declared.DIRECTORY / name))
    return tmp_path


def edit(directory: Path, name: str, change: Any) -> None:
    path = directory / name
    value = json.loads(path.read_text(encoding="utf-8"), parse_float=str)
    change(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def coarser_step(value: dict[str, Any]) -> None:
    # B (1 + 1/999) = 1 exactly: the core need not fit inside the unit square.
    value["proof_net"]["step"] = "1/999"


def short_net(value: dict[str, Any]) -> None:
    # t = 414/1001 < tan(pi/8): the net stops short of pi/4.
    value["proof_net"]["last"] = 414


def offset_field(value: dict[str, Any]) -> None:
    value["proof_net"]["offset"] = "1/2002"


def heavier_row(value: dict[str, Any]) -> None:
    row = value["rectangles"][0]
    row["mass"] = str(Fraction(row["mass"]) + Fraction(1, 10**9))


def stated_endpoint(value: dict[str, Any]) -> None:
    value["net"]["endpoint"] = "414/1001"


def missing_record(value: dict[str, Any]) -> None:
    del value["results"]["207"]


@pytest.mark.parametrize(
    ("name", "change", "message"),
    [
        ("candidate.json", coarser_step, "lemma N0"),
        ("candidate.json", short_net, "lemma N0"),
        ("candidate.json", offset_field, "proof_net has fields"),
        ("candidate.json", heavier_row, "total_mass"),
        ("manifest.json", stated_endpoint, "manifest net endpoint"),
        ("certificate.json", missing_record, "no record"),
    ],
)
def test_a_changed_copy_is_refused(
    tmp_path: Path, name: str, change: Any, message: str
) -> None:
    directory = copy_directory(tmp_path)
    assert declared.audit(directory)["status"] == "EXACT_PREMISES_HOLD"
    edit(directory, name, change)
    with pytest.raises(declared.AuditError, match=message):
        declared.audit(directory)


def shipped_tree(root: Path) -> dict[str, Any]:
    """A bundle tree holding what ``compare`` reads, the records being the retained
    certificate's; file times are a day before any run."""
    certificate = json.loads(read_retained_bytes(declared.DIRECTORY / "certificate.json"))
    for r in range(416):
        path = root / declared.record_name(r)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(certificate["results"][str(r)]), encoding="utf-8")
    (root / "proof/certificate.json").write_bytes(
        read_retained_bytes(declared.DIRECTORY / "certificate.json")
    )
    (root / "proof/net001/input.txt").write_text("unchanged", encoding="utf-8")
    (root / "bundle.json").write_text(
        json.dumps(
            {
                "status": "REPLAYED_PROOF_BUNDLE",
                "certificate": "ALL_ANGLES_VERIFIED_AND_REPLAYED",
            }
        ),
        encoding="utf-8",
    )
    for path in root.rglob("*"):
        os.utime(path, (1_790_000_000, 1_790_000_000))
    return certificate


def replay(shipped: Path, fresh: Path, certificate: dict[str, Any]) -> Path:
    """A copy of ``shipped`` after a complete run: every record written again, the
    certificate rewritten in another order, the progress record, the driver's binary and
    the runner's record. Returns the runner's record."""
    shutil.copytree(shipped, fresh)
    for r in range(416):
        (fresh / declared.record_name(r)).write_text(
            json.dumps(certificate["results"][str(r)]), encoding="utf-8"
        )
    reordered = {**certificate, "results": dict(reversed(certificate["results"].items()))}
    (fresh / "proof/certificate.json").write_text(json.dumps(reordered), encoding="utf-8")
    (fresh / "proof/replay-progress.json").write_text('{"done": 416, "total": 416}')
    (fresh / declared.DRIVER_BINARY).write_bytes(b"binary")
    meta = fresh.parent / "run.meta"
    meta.write_text(
        "asserts: on\nstart: 2026-10-05T17:16:28Z\nexit: 0\nend: 2026-10-05T22:00:00Z\n"
    )
    return meta


def test_a_complete_replay_matches_whatever_order_it_rewrites_the_certificate_in(
    tmp_path: Path,
) -> None:
    """Finding DN-1's second probe: the driver rewrites the certificate with its records
    in another order, which is the same certificate."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    result = declared.compare(shipped, fresh, meta)
    assert result["status"] == "FULL_REPLAY_MATCHES_SHIPPED", result["differing"]
    assert result["records_matching"] == 416
    assert result["certificate_rewritten"]


def test_a_copy_on_which_nothing_ran_does_not_match(tmp_path: Path) -> None:
    """Finding DN-1's first probe: a copy made without keeping file times, on which no
    replay ran, has every record newer than the shipped one and equal to it."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    shipped_tree(shipped)
    shutil.copytree(shipped, fresh, copy_function=shutil.copy)
    meta = tmp_path / "run.meta"
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 0\n")
    result = declared.compare(shipped, fresh, meta)
    assert result["status"] == "MISMATCH"
    assert any("progress record" in line for line in result["differing"])
    assert any("binary" in line for line in result["differing"])


def test_a_replay_with_a_changed_or_stale_record_does_not_match(tmp_path: Path) -> None:
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    changed = fresh / declared.record_name(207)
    changed.write_text(json.dumps({**certificate["results"]["207"], "nodes": 1}))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/net207/replayed.json: differs from the shipped record"
    ]
    os.utime(changed, (1_790_000_000, 1_790_000_000))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/net207/replayed.json: not written by this run"
    ]
    (fresh / "proof/net001/input.txt").write_text("changed", encoding="utf-8")
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 1\n")
    differing = declared.compare(shipped, fresh, meta)["differing"]
    assert "the run did not exit zero: 1" in differing
    assert "proof/net001/input.txt: changed by the replay" in differing


def enclosing_lines(candidate: dict[str, Any]) -> list[str]:
    """Rectangle lines in the input's layout that enclose the expanded candidate."""
    side = Fraction(candidate["L"])
    lines = []
    for row in candidate["rectangles"]:
        corners = [Fraction(value) for value in row["rectangle"]]
        area = (corners[2] - corners[0]) * (corners[3] - corners[1])
        density = Fraction(row["mass"]) / 8 / area
        for image in declared.orbit(side, corners):
            fields = []
            for exact in (*image, density):
                value = float(exact)
                fields += [
                    math.nextafter(value, -math.inf).hex(),
                    math.nextafter(value, math.inf).hex(),
                ]
            lines.append(" ".join(fields))
    return [*lines, "0"]


def test_rectangle_lines_must_enclose_every_image_of_every_row() -> None:
    candidate = json.loads(read_retained_bytes(declared.DIRECTORY / "candidate.json"))
    lines = enclosing_lines(candidate)
    declared.rectangle_block(candidate, lines)
    record = json.loads((declared.RECEIPTS / "bundle.json").read_text(encoding="utf-8"))
    assert record["rectangle_lines"] == "ENCLOSE_THE_EXPANDED_CANDIDATE"
    heavier = list(lines)
    fields = heavier[0].split()
    fields[8:10] = [(float.fromhex(fields[9]) * 2).hex(), (float.fromhex(fields[9]) * 3).hex()]
    heavier[0] = " ".join(fields)
    with pytest.raises(declared.AuditError, match="encloses none of its images"):
        declared.rectangle_block(candidate, heavier)
    with pytest.raises(declared.AuditError, match="point count"):
        declared.rectangle_block(candidate, [*lines[:-1], "1"])
    twice = [lines[0], *lines[0:7], *lines[8:]]
    with pytest.raises(declared.AuditError, match="encloses none of its images"):
        declared.rectangle_block(candidate, twice)


@pytest.mark.parametrize("core", [Fraction(1999, 2000), Fraction(999, 1000)])
def test_the_coarser_net_breaks_the_cores_fit_and_nothing_else(core: Fraction) -> None:
    net = declared.coarser_net(core)
    step, last = Fraction(net["step"]), int(net["last"])
    assert core * (1 + step) >= 1
    # The sharp extent, not only the sufficient test: a core at a bin's edge does not fit
    # strictly inside its unit square (FN-3). At D = (1 - B)/B it still would.
    assert declared.sharp_extent(core, step) >= 1
    assert declared.sharp_extent(core, (1 - core) / core) < 1
    assert declared.reaches_past_pi_over_8(last * step)
    assert not declared.reaches_past_pi_over_8((last - Fraction(1, 2)) * step)


@pytest.mark.parametrize(("key", "index"), [("n18-L4704", 797), ("n19-L48229", 37)])
def test_each_control_is_refused_for_its_own_premise(key: str, index: int) -> None:
    """The source's checker accepts the original at its least recorded bound and refuses
    two mass mutants there, each provably uncovered at an exact witness; the source's net
    check and sqverify-fast refuse each corrupted net for the premise it breaks; and
    sqverify-fast verifies the original and refuses the same two mutants."""
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "control.json").read_text(encoding="utf-8"))
    assert record["status"] == "CONTROLS_REFUSED"
    assert (record["certificate"], record["index"]) == (stated.name, index)
    assert record["checker"]["source_sha256"] == declared.CHECKER_SHA256
    original, *mutants = record["runs"]
    assert original["run"]["verdict"] == "ACCEPTED"
    assert original["run"]["output"]["lower"] == record["shipped_record"]["lower"]
    assert [run["name"] for run in mutants] == ["scale-masses", "near-threshold"]
    for run in mutants:
        assert Fraction(run["witness_coverage_exact"]) < 1, run["name"]
        assert run["run"]["verdict"] == "REFUSED", run["name"]
        assert run["run"]["output"]["status"] == "ANGLE_UNRESOLVED", run["name"]
    assert Fraction(mutants[1]["witness_coverage_exact"]) == 1 - declared.NEAR_THRESHOLD
    assert [item["name"] for item in record["nets"]] == list(declared.NET_REFUSALS)
    candidate = json.loads(read_retained_bytes(stated.directory / "candidate.json"))
    assert record["nets"][0]["proof_net"] == declared.coarser_net(Fraction(candidate["B"]))
    for item in record["nets"]:
        source_rule, admission_rule = declared.NET_REFUSALS[item["name"]]
        assert item["source"]["verdict"] == "REFUSED", item["name"]
        assert source_rule in item["source"]["message"], item["name"]
        assert item["sqverify_fast"]["verdict"] == "REFUSED", item["name"]
        assert admission_rule in item["sqverify_fast"]["stderr"], item["name"]
    fast = json.loads(
        (stated.receipts / "control-sqverify-fast.json").read_text(encoding="utf-8")
    )
    assert fast["status"] == "CONTROLS_REFUSED"
    assert fast["binary_sha256"] == record["sqverify_fast"]
    assert [(run["name"], run["held"]) for run in fast["runs"]] == [
        ("original", True),
        ("scale-masses", True),
        ("near-threshold", True),
    ]


def test_a_run_with_nothing_showing_its_assertions_were_on_does_not_match(
    tmp_path: Path,
) -> None:
    """Finding FN-1 of the 6 October review: the source's checks are asserts, so a run
    whose record and snapshot do not show them on proves nothing."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    meta.write_text("start: 2026-10-05T17:16:28Z\nexit: 0\nend: 2026-10-05T22:00:00Z\n")
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "nothing shows the driver's assertions were on during the run"
    ]
    snapshot = {
        "status": "ASSERTS_ON",
        "taken": "2026-10-05T18:00:00Z",
        "processes": [{"pid": 1}, {"pid": 2}],
    }
    (meta.parent / declared.PROCESSES).write_text(json.dumps(snapshot))
    assert declared.compare(shipped, fresh, meta)["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    # A snapshot taken outside the run, or one that does not show the assertions on,
    # shows nothing about it.
    for changed in ({"taken": "2026-10-05T23:00:00Z"}, {"status": "NOT_SHOWN"}):
        (meta.parent / declared.PROCESSES).write_text(json.dumps(snapshot | changed))
        assert declared.compare(shipped, fresh, meta)["status"] == "MISMATCH"


def test_a_certificate_the_run_did_not_rewrite_does_not_match(tmp_path: Path) -> None:
    """Finding FN-2: the shipped certificate equals the retained one, so an unrewritten
    copy must not count as the driver's output."""
    shipped, fresh = tmp_path / "shipped", tmp_path / "fresh"
    certificate = shipped_tree(shipped)
    meta = replay(shipped, fresh, certificate)
    os.utime(fresh / "proof/certificate.json", (1_790_000_000, 1_790_000_000))
    assert declared.compare(shipped, fresh, meta)["differing"] == [
        "proof/certificate.json: not rewritten by this run"
    ]


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["python3", "code/verify_mixed_full_proof.py", "proof"], "runs asserts"),
        (["python3", "-B", "-c", "import sys"], "runs asserts"),
        (["python3", "-O", "code/verify_mixed_full_proof.py"], "optimizes"),
        (["python3", "-BO", "-c", "x"], "optimizes"),
        (["python3", "-OO", "-m", "x"], "optimizes"),
        (["python3", "-m", "x", "-O"], "runs asserts"),
    ],
)
def test_an_optimizing_command_line_is_recognised(argv: list[str], expected: str) -> None:
    assert declared.optimizing(argv) is (expected == "optimizes")


def test_replay_refuses_to_run_with_assertions_off(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PYTHONOPTIMIZE", "1")
    with pytest.raises(declared.AuditError, match="assertions are off"):
        declared.replay("n18-L4704", tmp_path / "absent.tar.gz", tmp_path, 1, tmp_path)


def test_the_complete_n18_replay_matches_the_shipped_run() -> None:
    """think-drtz: the bundle's own driver replayed mixed_n18_L4704 over all 832 nodes with
    its assertions on, as the /proc snapshot taken during the run shows, and every record
    it regenerated is the shipped one."""
    full = declared.CERTIFICATES["n18-L4704"].receipts / "full"
    record = json.loads((full / "compare.json").read_text(encoding="utf-8"))
    assert record["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert (record["records_matching"], record["records"]) == (832, 832)
    assert record["progress"] == {"done": 832, "total": 832}
    assert record["certificate_rewritten"]
    assert record["differing"] == []
    run = declared.read_meta(full / "run.meta")
    assert run["exit"] == "0"
    assert declared.asserts_were_on(run, full / declared.PROCESSES)


#: The check2 certificates of 6 October 2026 at ``2fad66e``, with their row counts and
#: declared nets: they ship the source's run of its adaptation of sqverify_fast, not C++
#: records.
CHECK2 = {
    "n18-L4705": (324, "1/5002", 2073),
    "n19-L4825": (341, "1/5002", 2073),
    "n20-L4905": (327, "1/2006", 832),
    "n26-L5545": (477, "1/2006", 832),
    "n27-L56435": (439, "1/2006", 832),
    "n28-L5735": (531, "1/1001", 416),
    "n30-L58835": (402, "1/2006", 832),
    "n39-L665": (600, "1/1001", 416),
    "n41-L6775": (376, "1/1001", 416),
}
#: The source's adaptation of this repository's sqverify_fast, by its build's
#: ``source_sha256``: every check2 run names it.
ADAPTED_SOURCE = "ab6e33e164dbc5c32b40349ba55981b58e630b5eef59534196a69d259404fd7c"


def test_the_check2_certificates_are_the_ones_the_table_names() -> None:
    assert {key for key, stated in declared.CERTIFICATES.items() if stated.check2} == set(
        CHECK2
    )
    assert not declared.CERTIFICATES["n29-L581"].check2


@pytest.mark.parametrize("key", sorted(CHECK2))
def test_each_check2_certificate_holds_lemma_n0_and_its_receipt(key: str) -> None:
    rows, step, count = CHECK2[key]
    stated = declared.CERTIFICATES[key]
    facts = declared.audit(key=key)
    assert facts["format"] == "check2"
    assert facts["status"] == "EXACT_PREMISES_HOLD"
    assert all(facts["premises"].values())
    assert (facts["rectangles"], facts["net"]["step"], facts["net"]["count"]) == (
        rows,
        step,
        str(count),
    )
    assert Fraction(facts["mass"]) == stated.n - declared.GAP
    check = facts["source_check"]
    assert (check["status"], check["directions"]) == ("VERIFIED", count)
    assert check["source_sha256"] == ADAPTED_SOURCE
    assert check["control_status"] == "REFUSED"


def test_the_finest_net_has_the_premises_lemma_n0_needs() -> None:
    """mixed_n18_L4705 and mixed_n19_L4825: core 4999/5000 on 2073 tangents of step
    1/5002, finer than any net the source declared before."""
    facts = declared.audit(key="n18-L4705")["net"]
    step, core = Fraction(1, 5002), Fraction(4999, 5000)
    assert Fraction(facts["rotated_side_upper"]) == core * (1 + step) < 1
    assert Fraction(facts["endpoint"]) == Fraction(2072, 5002)
    assert Fraction(facts["endpoint_check"]) > 0
    # The last bin still holds an orientation: its floor is below tan(pi/8).
    assert not declared.reaches_past_pi_over_8(Fraction(2072 * 2 - 1, 2) * step)
    assert Fraction(facts["tangent_form"]) < 1


def copy_check2(tmp_path: Path, key: str) -> Path:
    """A check2 directory's retained files, decompressed, in a scratch directory."""
    directory = declared.CERTIFICATES[key].directory
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        name = path.relative_to(directory).as_posix().removesuffix(".gz")
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(read_retained_bytes(directory / name))
    return tmp_path


def coarser_check2_step(value: dict[str, Any]) -> None:
    # 4999/5000 (1 + 1/1001) > 1: a core at a bin's edge need not fit.
    value["proof_net"]["step"] = "1/1001"


def stated_bundle_endpoint(value: dict[str, Any]) -> None:
    value["net"]["endpoint"] = "2071/5002"


def fewer_directions(value: dict[str, Any]) -> None:
    value["directions"] = 2072


def unrefused_control(value: dict[str, Any]) -> None:
    value["tries"][0]["status"] = "VERIFIED"


@pytest.mark.parametrize(
    ("name", "change", "message"),
    [
        ("candidate.json", coarser_check2_step, "lemma N0"),
        ("candidate.json", heavier_row, "total_mass"),
        ("bundle.json", stated_bundle_endpoint, "bundle.json net endpoint"),
        ("check2/receipt.json", fewer_directions, "receipt digest"),
        ("check2/control.json", unrefused_control, "control was not refused"),
    ],
)
def test_a_changed_check2_copy_is_refused(
    tmp_path: Path, name: str, change: Any, message: str
) -> None:
    directory = copy_check2(tmp_path, "n18-L4705")
    assert declared.audit(directory, key="n18-L4705")["status"] == "EXACT_PREMISES_HOLD"
    edit(directory, name, change)
    with pytest.raises(declared.AuditError, match=message):
        declared.audit(directory, key="n18-L4705")


def test_a_check2_file_unlike_its_listed_digest_is_refused(tmp_path: Path) -> None:
    directory = copy_check2(tmp_path, "n20-L4905")
    spec = directory / "check2/src/SPEC.md"
    spec.write_text(spec.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(declared.AuditError, match=r"SPEC\.md is not the file"):
        declared.audit(directory, key="n20-L4905")


def test_both_forms_of_the_source_control_record_are_read() -> None:
    tries = {
        "refused": True,
        "tries": [{"status": "REFUSED", "exit": 1}],
    }
    assert declared.control_refused(tries)
    assert not declared.control_refused(tries | {"tries": [{"status": "VERIFIED", "exit": 0}]})
    assert not declared.control_refused(tries | {"refused": False})
    assert declared.control_refused({"status": "REFUSED", "exit": 1})
    assert not declared.control_refused({"status": "REFUSED", "exit": 0})


def receipt_v1(value: dict[str, Any]) -> None:
    """An earlier pre-publication receipt rewritten in the shape of `mixed_n30_L58925`'s
    of 10 October: a schema, the build as ``verifier``, and the control as one try."""
    control = value.pop("control")
    value["schema"] = declared.PREPUBLICATION_V1
    value["verifier"] = {"name": "sqverify-fast"} | value.pop("build")
    value["control"] = {
        "kind": "every mass times factor, 32 directions spread over the net",
        "tries": [
            {
                "factor": "197/200",
                "status": control["status"],
                "exit": control["exit"],
                "directions": 32,
                "refused": control["refused_directions"],
                "exact_below_threshold": control["exact_below_threshold"],
            }
        ],
        "refused": True,
    }


def other_factor(value: dict[str, Any]) -> None:
    value["control"]["tries"][0]["factor"] = "99/100"


def verified_try(value: dict[str, Any]) -> None:
    value["control"]["tries"][0]["status"] = "VERIFIED"


def passing_try(value: dict[str, Any]) -> None:
    value["control"]["tries"][0]["exit"] = 0


def control_not_refused(value: dict[str, Any]) -> None:
    value["control"]["refused"] = False


def second_try(value: dict[str, Any]) -> None:
    tries = value["control"]["tries"]
    tries.append(tries[0] | {"factor": "99/100"})


def no_verifier(value: dict[str, Any]) -> None:
    del value["verifier"]


def build_for_verifier(value: dict[str, Any]) -> None:
    value["build"] = value.pop("verifier")


def later_schema(value: dict[str, Any]) -> None:
    value["schema"] = "fine-net-check2-receipt/v2"


def test_both_shapes_of_the_pre_publication_receipt_are_read_alike(tmp_path: Path) -> None:
    """The earlier shape and `PREPUBLICATION_V1`, of the same run, give the same facts."""
    directory = copy_check2(tmp_path, "n18-L4705")
    earlier = declared.audit(directory, key="n18-L4705")
    assert earlier["status"] == "EXACT_PREMISES_HOLD"
    edit(directory, declared.PREPUBLICATION, receipt_v1)
    later = declared.audit(directory, key="n18-L4705")
    assert later == earlier
    assert later["prepublication_check"]["control_refused_directions"] == 29


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (other_factor, "not refused at 197/200"),
        (verified_try, "not refused at 197/200"),
        (passing_try, "not refused at 197/200"),
        (control_not_refused, "not refused at 197/200"),
        (second_try, "not one try"),
        (no_verifier, "no build in verifier"),
        (build_for_verifier, "no build in verifier"),
        (later_schema, "no reader for pre-publication schema"),
    ],
)
def test_a_v1_pre_publication_receipt_without_its_build_or_refused_control_is_refused(
    tmp_path: Path, change: Any, message: str
) -> None:
    directory = copy_check2(tmp_path, "n18-L4705")
    edit(directory, declared.PREPUBLICATION, receipt_v1)
    edit(directory, declared.PREPUBLICATION, change)
    with pytest.raises(declared.AuditError, match=message):
        declared.audit(directory, key="n18-L4705")


def no_build(value: dict[str, Any]) -> None:
    del value["build"]


def unrefused_status(value: dict[str, Any]) -> None:
    value["control"]["status"] = "VERIFIED"


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (no_build, "no build in build"),
        (unrefused_status, "pre-publication control was not refused"),
    ],
)
def test_an_earlier_pre_publication_receipt_without_its_build_or_refused_control_is_refused(
    tmp_path: Path, change: Any, message: str
) -> None:
    directory = copy_check2(tmp_path, "n18-L4705")
    edit(directory, declared.PREPUBLICATION, change)
    with pytest.raises(declared.AuditError, match=message):
        declared.audit(directory, key="n18-L4705")


@pytest.mark.parametrize("key", sorted(CHECK2))
def test_each_check2_bundle_is_bound_to_the_packet_and_its_logs_to_the_net(key: str) -> None:
    _rows, _step, count = CHECK2[key]
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "bundle.json").read_text(encoding="utf-8"))
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert (record["format"], record["certificate"]) == ("check2", stated.name)
    assert record["tarball"]["sha256"] == stated.tarball_pin()[0]
    assert record["listed_files"] == 15
    assert record["retained_files_equal"] + record["pinned_files_equal"] + 1 == 15
    log = record["run_log"]
    assert log["directions"] == count
    assert log["source_sha256"] == ADAPTED_SOURCE
    assert log["least_oblique"]["lower"] >= 1
    assert log["axis_lower"] >= 1
    control = record["control_log"]
    assert Fraction(control["factor"]) == Fraction(197, 200)
    assert control["refused"] >= 1
    assert control["exact_below_threshold"] >= 1


def test_the_n29_bundle_is_bound_like_the_earlier_proof_bundles() -> None:
    stated = declared.CERTIFICATES["n29-L581"]
    record = json.loads((stated.receipts / "bundle.json").read_text(encoding="utf-8"))
    facts = declared.audit(key="n29-L581")
    assert record["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
    assert (record["listed_files"], record["code_files"]) == (1266, 10)
    assert record["oblique_inputs"] == facts["oblique_records"] == 415
    assert record["rectangle_images"] == 8 * 505
    assert record["upstream_oblique_nodes"] == facts["oblique_nodes"]
    assert record["tarball"]["sha256"] == stated.tarball_pin()[0]


def test_each_check2_run_names_its_input_published_or_listed() -> None:
    """Finding FN-1 of the review of T-102 to T-111: eight check2 run logs name an input
    other than the published candidate.json. The audit names each, and refuses any other."""
    for key in CHECK2:
        facts = declared.audit(key=key)
        published = key not in declared.UNPUBLISHED_RUN_INPUTS
        assert facts["run_input"]["published_candidate"] is published, key
        if not published:
            assert facts["run_input"]["sha256"] == declared.UNPUBLISHED_RUN_INPUTS[key]
        assert facts["prepublication_check"]["input_is_published_candidate"]
    assert len(declared.UNPUBLISHED_RUN_INPUTS) == 8


def test_an_unlisted_or_stale_run_input_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    listed = dict(declared.UNPUBLISHED_RUN_INPUTS)
    unlisted = {key: value for key, value in listed.items() if key != "n20-L4905"}
    monkeypatch.setattr(declared, "UNPUBLISHED_RUN_INPUTS", unlisted)
    with pytest.raises(declared.AuditError, match="neither the published candidate"):
        declared.audit(key="n20-L4905")
    stale = listed | {"n18-L4705": "0" * 64}
    monkeypatch.setattr(declared, "UNPUBLISHED_RUN_INPUTS", stale)
    with pytest.raises(declared.AuditError, match="neither the published candidate"):
        declared.audit(key="n18-L4705")


def test_both_forms_of_the_control_factor_read_197_200() -> None:
    assert declared.control_factor({"tries": [{"factor": "197/200"}]}) == Fraction(197, 200)
    kind = {"kind": "every mass x 0.985, 32 directions"}
    assert declared.control_factor(kind) == Fraction(197, 200)
    assert declared.control_factor({"kind": "masses halved"}) is None


def test_a_control_witness_is_recomputed_exactly() -> None:
    """Finding FN-2: each control witness must lie in its node's per-bin domain and carry
    the capture an evaluator written apart from the crate computes on the scaled measure,
    below one."""
    exact = importlib.import_module("devtools.check_sqverify_fast").mixed_exact
    stated = declared.CERTIFICATES["n41-L6775"]
    candidate = declared.load_json(read_retained_bytes(stated.directory / "candidate.json"))
    half = Fraction(1, 2)
    scaled = {
        "L": candidate["L"],
        "B": candidate["B"],
        "proof_net": candidate["proof_net"],
        "rectangles": [
            {"rectangle": row["rectangle"], "mass": str(Fraction(row["mass"]) * half)}
            for row in candidate["rectangles"]
        ],
    }
    side = Fraction(candidate["L"])
    pose = (float(side / 2), float(side / 2))
    capture = exact(scaled, Fraction(pose[0]), Fraction(pose[1]), 7)
    assert capture < 1

    def tried(coverage: Fraction, where: tuple[float, float]) -> list[dict[str, Any]]:
        witness = {
            "exact_below_threshold": True,
            "exact_pose": list(where),
            "exact_coverage": str(coverage),
        }
        return [{"r": 7, "verdict": "counterexample-candidate", "witness": witness}]

    assert declared.control_witnesses(candidate, tried(capture, pose), half) == 1
    with pytest.raises(declared.AuditError, match="not the logged one"):
        declared.control_witnesses(candidate, tried(capture + Fraction(1, 10**12), pose), half)
    with pytest.raises(declared.AuditError, match="outside the per-bin domain"):
        declared.control_witnesses(candidate, tried(capture, (0.1, pose[1])), half)


def test_every_cpp_sample_receipt_verified_its_nodes() -> None:
    """cpp-sample: the source's C++ checker, the producer's own code but sharing none with
    sqverify_fast, verified each check2 candidate at every node it ran."""
    receipts = [
        (key, path)
        for key in sorted(CHECK2)
        for path in sorted((declared.CERTIFICATES[key].receipts / "cpp-sample").glob("*.json"))
    ]
    assert (
        "n41-L6775",
        declared.CERTIFICATES["n41-L6775"].receipts / "cpp-sample/nodes-0409-0415.json",
    ) in receipts
    for key, path in receipts:
        stated = declared.CERTIFICATES[key]
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["status"] == "SAMPLE_VERIFIED", path.name
        assert record["certificate"] == stated.name
        assert record["checker_sha256"] == declared.CHECKER_SHA256
        assert record["threshold"] == "1"
        assert record["tarball"]["sha256"] == stated.tarball_pin()[0]
        assert record["binding"]["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
        assert record["candidate_digest"] == declared.audit(key=key)["candidate_digest"]
        assert [row["index"] for row in record["rows"]] == record["nodes"]
        for row in record["rows"]:
            assert row["verified"], (path, row["index"])
            assert row["status"] == "ANGLE_VERIFIED", (path, row["index"])
            assert (row["frontier_boxes"], row["exact_witnesses"]) == (0, 0)
            assert float(row["lower"]) >= 1


@pytest.mark.parametrize("key", sorted(CHECK2))
def test_each_check2_candidate_passes_the_source_cpp_checker_at_its_sampled_nodes(
    key: str,
) -> None:
    """The source's C++ checker, which shares no code with sqverify_fast, verified each
    check2 candidate at the nodes cpp-sample ran, its least-bound node among them."""
    stated = declared.CERTIFICATES[key]
    receipts = sorted((stated.receipts / "cpp-sample").glob("nodes-*.json"))
    assert receipts, key
    bundle = json.loads((stated.receipts / "bundle.json").read_text(encoding="utf-8"))
    ran: set[int] = set()
    for path in receipts:
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["status"] == "SAMPLE_VERIFIED", path.name
        assert record["certificate"] == stated.name
        assert record["checker_sha256"] == declared.CHECKER_SHA256
        assert record["threshold"] == "1"
        assert record["tarball"]["sha256"] == stated.tarball_pin()[0]
        assert record["binding"]["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
        assert record["candidate_digest"] == declared.audit(key=key)["candidate_digest"]
        assert [row["index"] for row in record["rows"]] == record["nodes"]
        for row in record["rows"]:
            assert row["verified"], (path.name, row["index"])
            assert row["status"] == "ANGLE_VERIFIED"
            assert (row["frontier_boxes"], row["exact_witnesses"]) == (0, 0)
            assert float(row["lower"]) >= 1
        ran |= set(record["nodes"])
    assert bundle["run_log"]["least_oblique"]["r"] in ran


@pytest.mark.parametrize("key", sorted(CHECK2))
def test_each_census_row_runs_as_the_source_copy_of_the_crate_did(key: str) -> None:
    """compare-census: this repository's census row and the source's run of its copy of
    the crate both verify every node of the declared net."""
    stated = declared.CERTIFICATES[key]
    record = json.loads((stated.receipts / "compare-census.json").read_text(encoding="utf-8"))
    _rows, _step, count = CHECK2[key]
    assert record["status"] == "BOTH_VERIFY_EVERY_DIRECTION"
    assert (record["certificate"], record["directions"]) == (stated.name, count)
    census = declared.PROJECT / record["census_receipts"]
    assert declared.file_sha256(census) == record["census_receipts_sha256"]
    assert record["least_oblique"]["census"]["lower"] >= 1


def test_the_n29_sample_returned_the_shipped_records() -> None:
    stated = declared.CERTIFICATES["n29-L581"]
    receipts = sorted((stated.receipts / "sample").glob("nodes-*.json"))
    assert receipts
    for path in receipts:
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["status"] == "SAMPLE_REPLAYED", path.name
        assert record["binding"]["status"] == "BUNDLE_BOUND_TO_PACKET_AND_NET"
        assert all(row["matches_upstream"] for row in record["rows"]), path.name
        assert 364 in record["nodes"]
