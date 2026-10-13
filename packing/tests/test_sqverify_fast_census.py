"""The clean-room verifier's census, and its controls on the certificates it decides.

`devtools.sqverify_fast_census --family mixed` keeps, per retained format M or L
certificate, `sqverify-fast`'s verdict at all 201 net directions, and the default
rectangle family the same for every format T certificate at Tokoharu's threshold
10001/10000. For a certificate on which an evidence entry rests, it keeps a control
receipt: the original verified again at its least-bound direction, and two mutants
refused there (every mass scaled by 99/100, and every mass scaled so that the exact
capture at the least-bound leaf's centre is at most one part in a million below the
row's threshold). `campaign/result-import.md` asks that two mutated certificates be
refused by every checker that accepted the original, with a test holding them; this is
that test for `V-sqverify-fast`.

These tests read the retained receipts, the retained candidates and the evidence
register only; nothing here builds or runs the verifier. Each mutant's capture at the
centre is recomputed here from the receipt's exact capture and factor, so each refusal
is the verifier's correct answer rather than a budget running out, and one receipt of
each family has its exact capture recomputed from the candidate by an exact evaluator
written apart from the crate.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import (
    direction,
    metadata_net,
    mixed_exact,
    net_step,
    read_raw,
    scaled,
)
from sqpack.rectangle_density import coverage_at_point, load_candidate
from sqpack.yamlio import safe_load

FOLDER = census.CENSUS_ROOT / "census-mixed"
#: The rectangle family's census: format T, at Tokoharu's threshold.
RECTANGLES = census.CENSUS_ROOT / "census"
#: The format T receipt whose exact capture is recomputed here from the candidate.
RECOMPUTED_T = "rect_n66_L8385"
#: Tokoharu's threshold, which the rectangle family passes for every format T row.
TOKOHARU_THRESHOLD = "10001/10000"
EVIDENCE = census.PROJECT / "frontier/evidence.yaml"
RESULTS = census.PROJECT / "frontier/results.yaml"
VERIFIER = "V-sqverify-fast"
#: How far below lemma F3's cap on an expanded rectangle's density, 2^96, a certificate
#: on the reviewed route stays: eight coinciding images of its densest row at most 2^32.
#: The retained ones are near 2^19, so none is near the cap.
DENSITY_CEILING = 2**32
#: The receipt whose exact capture is recomputed here from the candidate.
RECOMPUTED = "mixed_n67_L848"
#: The retained format M certificate on a declared net (step 1/1001, 416 directions).
DECLARED = "mixed_n18_L470"
#: Lemma N0's cap on a declared net's direction count, its condition (a).
MAX_ANGLE_COUNT = 2**16
#: The `source_sha256` of builds whose crate source a soundness review accepted.
#: `census.REVIEWED_SOURCES` holds the same digests with each one's commit, review and
#: scope, which `--evidence` states; widening the route takes an edit to both.
REVIEWED_SOURCES = frozenset(
    {
        # The source the two reviews of 3 October accepted at 4ddf37d9c.
        "9985c465116631570c873ecc33af126adc6f14c7429a5ed44d922254d3c7f8a7",
        # The same `src/`, `Cargo.lock` and `build.rs`, with `Cargo.toml` changed only by
        # the gate's test profile (IR-4 of the 5 October route review); through e020eb1e2.
        "7c49cf79f2408e745d5a0759caf85768d92c502bb574b95dbc12b81a36e50300",
        # main's crate at 910b6b12c: the declared net of format M (`proof_net`, lemma N0,
        # f007d7afd) with the fixes of the 5 October declared-net review's DN-2, DN-4 to
        # DN-6 and DN-9 (910b6b12c). The soundness review of 6 October
        # (review-2026-10-06-sqverify-fast-declared-net-soundness.md) read the whole diff
        # from e020eb1e2 and accepted it for standard-net certificates, and for format M on
        # a declared net once its finding DR-1 (the control's evaluator on the standard
        # step) was fixed and the fix read, which the re-check of the same day did. So the
        # declared-net path is reviewed source too (`declared_nets`).
        "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88",
    }
)


@cache
def cases() -> dict[str, census.Case]:
    return {case.certificate: case for case in census.mixed_cases()}


@cache
def entries() -> dict[str, Any]:
    data = json.loads((FOLDER / "census.json").read_text(encoding="utf-8"))
    value: dict[str, Any] = data["cases"]
    return value


@cache
def rectangle_cases() -> dict[str, census.Case]:
    return {case.certificate: case for case in census.rectangle_cases()}


@cache
def rectangle_entries() -> dict[str, Any]:
    data = json.loads((RECTANGLES / "census.json").read_text(encoding="utf-8"))
    value: dict[str, Any] = data["cases"]
    return value


def case_of(name: str) -> census.Case:
    """A certificate's census case, of either family."""
    return rectangle_cases()[name] if name in rectangle_entries() else cases()[name]


def row_of(name: str) -> dict[str, Any]:
    """A certificate's census row, of either family."""
    return rectangle_entries()[name] if name in rectangle_entries() else entries()[name]


@cache
def controls() -> dict[str, dict[str, Any]]:
    return {
        path.name.removesuffix(".control.json"): json.loads(path.read_text(encoding="utf-8"))
        for folder in (FOLDER, RECTANGLES)
        for path in sorted(folder.glob("*/*.control.json"))
    }


@cache
def decided() -> dict[str, dict[str, Any]]:
    """Each evidence entry that `V-sqverify-fast` decides, by its id."""
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    return {
        entry["id"]: entry
        for entry in register["evidence"]
        if VERIFIER in (entry.get("verifiers") or [])
    }


@cache
def cited() -> dict[str, str]:
    """Each evidence entry that `V-sqverify-fast` decides, by the certificate it names."""
    by_path = {
        str(case.candidate.relative_to(census.PROJECT)): name
        for name, case in {**cases(), **rectangle_cases()}.items()
    }
    found: dict[str, str] = {}
    for ident, entry in decided().items():
        name = by_path.get(str(entry.get("certificate")))
        assert name is not None, f"{ident}: no census case for its certificate"
        found[ident] = name
    return found


@cache
def citing() -> dict[str, list[dict[str, Any]]]:
    """The register results that cite each evidence id."""
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    found: dict[str, list[dict[str, Any]]] = {}
    for record in register["results"]:
        for ident in record.get("evidence") or []:
            found.setdefault(ident, []).append(record)
    return found


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_every_mixed_census_case_is_verified_at_every_direction_of_its_net() -> None:
    """All 201 directions of the standard net, or every node of the net a certificate
    declares (`mixed_n18_L470`'s 416)."""
    assert entries()
    for name, entry in entries().items():
        least = entry["least_bound_leaf_exact"]
        case = cases()[name]
        total = census.net_directions(case)
        assert entry["status"] == "VERIFIED", name
        assert entry["returncode"] == 0, name
        assert entry["directions_verified"] == total, name
        assert least["clears_threshold"] is True, name
        assert Fraction(least["exact_coverage"]) >= Fraction(entry["threshold"]), name
        assert entry["candidate_sha256"] == sha256(case.candidate), name
        receipt = FOLDER / case.packet / f"{name}.jsonl.gz"
        rows = [json.loads(line) for line in gzip.decompress(receipt.read_bytes()).splitlines()]
        directions = [row for row in rows if "r" in row]
        assert sorted(int(row["r"]) for row in directions) == list(range(total)), name
        assert all(row["verdict"] == "verified" for row in directions), name
        summary = rows[-1]
        assert summary["kind"] == "sqverify-fast-summary/v1", name
        assert summary["status"] == "VERIFIED", name


def test_every_rectangle_census_case_cited_is_verified_at_every_direction() -> None:
    """The format T rows an evidence entry rests on, at all 201 directions of the
    standard net and Tokoharu's threshold."""
    for evidence_id, name in cited().items():
        if name not in rectangle_entries():
            continue
        entry = rectangle_entries()[name]
        case = rectangle_cases()[name]
        least = entry["least_bound_leaf_exact"]
        assert entry["status"] == "VERIFIED", evidence_id
        assert entry["returncode"] == 0, evidence_id
        assert entry["directions_verified"] == census.STANDARD_DIRECTIONS, evidence_id
        assert entry["threshold"] == TOKOHARU_THRESHOLD, evidence_id
        assert least["clears_threshold"] is True, evidence_id
        assert Fraction(least["exact_coverage"]) >= Fraction(entry["threshold"]), evidence_id
        assert entry["candidate_sha256"] == sha256(case.candidate), evidence_id
        receipt = RECTANGLES / case.packet / f"{name}.jsonl.gz"
        rows = [json.loads(line) for line in gzip.decompress(receipt.read_bytes()).splitlines()]
        directions = [row for row in rows if "r" in row]
        assert sorted(int(row["r"]) for row in directions) == list(
            range(census.STANDARD_DIRECTIONS)
        ), evidence_id
        assert all(row["verdict"] == "verified" for row in directions), evidence_id
        assert rows[-1]["kind"] == "sqverify-fast-summary/v1", evidence_id
        assert rows[-1]["status"] == "VERIFIED", evidence_id


def test_every_entry_the_verifier_decides_has_a_verified_case_and_a_refused_control() -> None:
    for evidence_id, name in cited().items():
        assert row_of(name)["status"] == "VERIFIED", evidence_id
        assert name in controls(), f"{evidence_id}: no control receipt for {name}"
        assert controls()[name]["status"] == "CONTROLS_REFUSED", evidence_id


def net_problems(
    raw: dict[str, Any], premises: dict[str, Any], source: census.ReviewedSource | None
) -> list[str]:
    """Where a census row's net is outside what its crate source's review accepted.

    Without a declaration, the standard net and core of the 5 October route review
    (Carrying the Route): 201 half-angles of step 83/40000 at core side 9977/10000. A
    format M file that declares its own net (`proof_net`) needs a source whose review
    read the declared-net path, and the checklist (b) of the 6 October soundness review:
    the declaration exactly `step` and `last` (with `count = last + 1` if given), metadata
    that only restates it, the premises the net the file declares, and lemma N0's (a) to
    (e) recomputed here in exact rationals, apart from the crate.
    """
    problems = ["a format L net block in a format M file"] if "net" in raw else []
    net = raw.get("proof_net")
    if net is None:
        if (premises["angle_count"], premises["D"], premises["B"]) != (
            201,
            "83/40000",
            "9977/10000",
        ):
            problems.append("not the standard net and core")
        return problems
    if source is None or not source.declared_nets:
        problems.append("a declared net, built from a source no declared-net review read")
    if (
        not isinstance(net, dict)
        or not {"step", "last"} <= set(net) <= {"step", "last", "count"}
        or type(net["last"]) is not int
        or ("count" in net and net["count"] != net["last"] + 1)
    ):
        return [*problems, "proof_net is not exactly step and an integer last"]
    step, count, core = Fraction(str(net["step"])), int(net["last"]) + 1, Fraction(raw["B"])
    top = step * (count - 1)
    metadata = raw.get("certificate") or {}
    holds = {
        "net_origin proof_net": premises.get("net_origin") == "proof_net",
        "D is the declared step": Fraction(str(premises["D"])) == step,
        "angle_count is last + 1": premises["angle_count"] == count,
        "net_last_tangent": Fraction(str(premises.get("net_last_tangent", -1))) == top,
        "B is the file's": Fraction(str(premises["B"])) == core,
        "shrink_bound is B (1 + D)": (
            Fraction(str(premises.get("shrink_bound", 2))) == core * (1 + step)
        ),
        "metadata only restates the net": (
            Fraction(str(metadata.get("D", step))) == step
            and metadata.get("angle_count", count) == count
        ),
        "(a) D > 0 and 2 <= N <= 2^16": step > 0 and 2 <= count <= MAX_ANGLE_COUNT,
        "(b) B (1 + D) < 1": core * (1 + step) < 1,
        "(c) the last tangent past tan(pi/8)": top * top + 2 * top - 1 > 0,
        "(d) the last tangent at most 1/2": top <= Fraction(1, 2),
        "(e) B (1 + D / (1 - D^2/4)) < 1": core * (1 + step / (1 - step * step / 4)) < 1,
    }
    return [*problems, *(name for name, ok in holds.items() if not ok)]


def test_every_entry_the_verifier_decides_is_within_what_its_review_accepted() -> None:
    """The per-certificate conditions of the review of 5 October (Carrying the Route),
    and for a declared net those of the soundness review of 6 October (`net_problems`).

    A certificate outside them (points or segments, another core side, net, domain or
    threshold, a declared net outside lemma N0 or on a source whose review did not read
    it, a scaling factor, densities near lemma F3's caps, a fault injected, or a crate
    source no review accepted) needs another review before an evidence entry may rest on
    its census row.
    """
    for evidence_id, name in cited().items():
        if name in rectangle_entries():
            assert format_t_problems(name) == [], evidence_id
            continue
        raw = read_raw(cases()[name].candidate)
        assert raw["points"] == [], evidence_id
        assert raw.get("scaling_factor", "1") == "1", evidence_id
        densest = max(
            Fraction(row["mass"])
            / ((Fraction(x2) - Fraction(x1)) * (Fraction(y2) - Fraction(y1)))
            for row in raw["rectangles"]
            for x1, y1, x2, y2 in [row["rectangle"]]
        )
        assert 8 * densest <= DENSITY_CEILING, evidence_id
        entry = entries()[name]
        premises = entry["premises"]
        n = int(premises["n"])
        assert (n, premises["L"]) == (entry["n"], entry["L"]), evidence_id
        assert premises["format"] == "M", evidence_id
        assert premises["centre_domain"] == "per-bin", evidence_id
        source = census.REVIEWED_SOURCES.get(entry["build"]["source_sha256"])
        assert net_problems(raw, premises, source) == [], evidence_id
        assert Fraction(premises["mass_exact"]) == n - Fraction(1, 100000), evidence_id
        assert premises["expanded_points"] == premises["expanded_segments"] == 0, evidence_id
        assert entry["threshold"] == "1", evidence_id
        assert entry["refused_directions"] == [], evidence_id
        assert entry["build"]["source_sha256"] in REVIEWED_SOURCES, evidence_id
        assert (entry["build"]["profile"], entry["build"]["rustc"].split()[1]) == (
            "release",
            "1.98.0",
        ), evidence_id
        receipt = FOLDER / entry["packet"] / f"{name}.jsonl.gz"
        summary = json.loads(gzip.decompress(receipt.read_bytes()).splitlines()[-1])
        assert summary["fault_injected_at_box"] is None, evidence_id


def format_t_problems(name: str) -> list[str]:
    """Where a format T row is outside what the review of its route accepted.

    The certificates the 6 October review of the format T route read: Tokoharu's format
    with no point or segment, the standard net and core (201 half-angles of step 83/40000
    at core side 9977/10000), Tokoharu's centre domain, a mass of n - 1/100, densities far
    below lemma F3's caps, decided at Tokoharu's threshold 10001/10000 by a build of
    reviewed source with no fault injected, and controlled by a build of reviewed source.
    """
    entry = rectangle_entries()[name]
    case = rectangle_cases()[name]
    raw = read_raw(case.candidate)
    premises = entry["premises"]
    n = int(premises["n"])
    densest = max(
        Fraction(weight) / ((Fraction(x2) - Fraction(x1)) * (Fraction(y2) - Fraction(y1)))
        for (x1, y1, x2, y2), weight in zip(raw["rectangles"], raw["weights"], strict=True)
    )
    receipt = RECTANGLES / entry["packet"] / f"{name}.jsonl.gz"
    summary = json.loads(gzip.decompress(receipt.read_bytes()).splitlines()[-1])
    control = controls().get(name) or {}
    metadata = raw.get("certificate") or {}
    holds = {
        "metadata restates the standard net": (
            Fraction(str(metadata.get("D", "83/40000"))) == Fraction(83, 40000)
            and int(metadata.get("angle_count", census.STANDARD_DIRECTIONS))
            == census.STANDARD_DIRECTIONS
        ),
        "no declared net": "proof_net" not in raw and "net" not in raw,
        "n and L are the row's": (n, premises["L"]) == (entry["n"], entry["L"]),
        "format T": premises["format"] == "T",
        "no point or segment": "points" not in raw and "segments" not in raw,
        "no expanded point or segment": (
            premises["expanded_points"] == premises["expanded_segments"] == 0
        ),
        "Tokoharu's centre domain": premises["centre_domain"] == "tokoharu",
        "the standard net and core": (premises["angle_count"], premises["D"], premises["B"])
        == (census.STANDARD_DIRECTIONS, "83/40000", "9977/10000"),
        "mass n - 1/100": Fraction(premises["mass_exact"]) == n - Fraction(1, 100),
        "densities far below lemma F3's caps": densest <= DENSITY_CEILING,
        "Tokoharu's threshold": entry["threshold"] == TOKOHARU_THRESHOLD,
        "no refused direction": entry["refused_directions"] == [],
        "row of reviewed source": entry["build"]["source_sha256"] in REVIEWED_SOURCES,
        "release build of rustc 1.98.0": (
            entry["build"]["profile"],
            entry["build"]["rustc"].split()[1],
        )
        == ("release", "1.98.0"),
        "no fault injected": summary["fault_injected_at_box"] is None,
        "controls of reviewed source": (
            (control.get("build") or {}).get("source_sha256") in REVIEWED_SOURCES
        ),
    }
    return [condition for condition, ok in holds.items() if not ok]


def test_every_entry_the_verifier_decides_rests_on_a_review_of_its_certificate() -> None:
    """The route carries only to a certificate whose mathematics a review read.

    Each replay entry names, as its `audit_record`, the review that read its
    certificate, and every result citing the entry lists that review, accepting and
    covering the result: the 5 October review of the route for T-094's two, and for
    T-097's mixed_n66_L843 the review of the same day that read it before its replay.
    """
    for evidence_id in cited():
        record = decided()[evidence_id]["proof"]["audit_record"]
        results = citing().get(evidence_id) or []
        assert results, f"{evidence_id}: no result cites it"
        for result in results:
            reviews = [
                review for review in result.get("reviews") or [] if review["path"] == record
            ]
            assert reviews, f"{evidence_id}: {result['id']} does not list {record}"
            for review in reviews:
                assert review["verdict"] == "accepted", evidence_id
                assert result["id"] in (review.get("covers") or [result["id"]]), evidence_id


@pytest.mark.parametrize("name", sorted(controls()))
def test_each_control_refuses_both_mutants_where_the_original_verifies(name: str) -> None:
    receipt = controls()[name]
    entry = row_of(name)
    case = case_of(name)
    # The threshold the row was decided at: 1 for formats M and L, which declare it, and
    # Tokoharu's 10001/10000 for format T, which the receipt records.
    threshold = Fraction(entry["threshold"])
    assert Fraction(receipt.get("threshold", "1")) == threshold
    assert receipt["kind"] in KINDS
    # Format T's controls are v1 at the tightest centre; v2 is format M's sweep (FC-1).
    assert receipt["kind"] == KINDS[0] or name not in rectangle_entries()
    assert receipt["status"] == "CONTROLS_REFUSED"
    assert (receipt["packet"], receipt["n"], receipt["L"]) == (case.packet, case.n, case.side)
    assert receipt["candidate_sha256"] == sha256(case.candidate) == entry["candidate_sha256"]
    exact = Fraction(receipt["exact_capture_independent"])
    assert receipt["captures_agree"] is True
    assert exact == Fraction(receipt["exact_capture_crate"])
    if name in rectangle_entries():
        # Format T: the tightest least-bound leaf centre of the row's 200 oblique
        # directions, by exact capture (`census.tightest_centre`), which is the centre
        # of that direction's least-bound leaf in the census receipts.
        assert receipt["selection"] == "tightest least-bound leaf centre"
        assert receipt["centres_weighed"] == census.STANDARD_DIRECTIONS - 1
        rows = gzip.decompress(
            (RECTANGLES / case.packet / f"{name}.jsonl.gz").read_bytes()
        ).splitlines()
        (row,) = (
            row
            for row in map(json.loads, rows)
            if "r" in row and int(row["r"]) == receipt["index"]
        )
        box = row["least_bound_box"]
        assert receipt["centre"] == [box["x"], box["y"]]
        assert receipt["index"] >= 1
    else:
        least = entry["least_bound_leaf_exact"]
        assert receipt["index"] == least["r"]
        assert receipt["centre"] == least["centre"]
        assert exact == Fraction(least["exact_coverage"])
    runs = {run["name"]: run for run in receipt["runs"]}
    assert set(runs) == {"original", "scaled-99-100", "near-threshold"}
    original = runs["original"]
    assert (original["returncode"], original["verdict"]) == (0, "verified")
    # v1 ran the 99/100 mutant at the least-bound direction only; v2 runs it at every
    # direction of the net (FC-1), held below by `test_each_scaled_sweep_...`.
    single = (
        ("scaled-99-100", "near-threshold")
        if receipt["kind"] == KINDS[0]
        else ("near-threshold",)
    )
    for mutant in single:
        run = runs[mutant]
        mutation = run["mutation"]
        factor = Fraction(mutation["factor"])
        assert Fraction(mutation["capture_at_centre"]) == exact * factor, mutant
        witness = mutation["capture_at_witness"]
        # The mutant's capture is below the threshold at the least-bound leaf's centre or
        # at the refusal's witness, so the claim the mutant makes is false there and a
        # refusal is the only correct answer.
        assert exact * factor < threshold or (
            witness is not None and Fraction(witness) < threshold
        ), mutant
        assert run["returncode"] == 1, mutant
        # A refusal on coverage, never audit-failed, non-finite or unresolved (CC-1).
        assert run["verdict"] == census.CANDIDATE, mutant
    if receipt["kind"] == KINDS[0]:
        # Each v1 receipt's 99/100 refusal has its own witness below the threshold, 1 for
        # format M and Tokoharu's 10001/10000 for format T, evaluated apart from the
        # crate: the rule v2 holds at every refused direction (CC-6).
        scaled = runs["scaled-99-100"]["mutation"]
        assert scaled["capture_at_witness"] is not None
        assert Fraction(scaled["capture_at_witness"]) < threshold
    else:
        # v2: every run as `--control` judged it, from the receipt's own fields.
        assert all(map(census.control_run_held, receipt["runs"]))
    assert Fraction(runs["scaled-99-100"]["mutation"]["factor"]) == census.CONTROL_SCALE
    near = runs["near-threshold"]["mutation"]
    assert exact * Fraction(near["factor"]) <= threshold * (1 - census.NEAR_THRESHOLD)


#: The control receipt kinds: v1 ran the 99/100 mutant at the least-bound direction, where
#: each receipt kept shows it refused; v2 runs it at every direction of the net (FC-1 of
#: the 6 October re-check). A v1 receipt that is CONTROLS_REFUSED meets v2's rule on the
#: one direction it ran: a refusal with an exact capture below 1 at a pose evaluated apart
#: from the crate. It is kept, not regenerated.
KINDS = ("sqverify-fast-control/v1", "sqverify-fast-control/v2")


def sweeps() -> dict[str, dict[str, Any]]:
    """Each v2 receipt's 99/100 sweep, by certificate."""
    return {
        name: next(run["sweep"] for run in receipt["runs"] if run["name"] == "scaled-99-100")
        for name, receipt in controls().items()
        if receipt["kind"] == KINDS[1]
    }


@pytest.mark.parametrize("name", sorted(sweeps()))
def test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness(
    name: str,
) -> None:
    """At every direction of the net, the 99/100 mutant is refused at one at least, and
    every direction that does not verify it is a coverage refusal at a pose in the per-bin
    domain where its capture, recomputed here from the candidate by the evaluator written
    apart from the crate, is the one the receipt keeps, below 1, with the original's at
    least 1. Where it verifies, the original captures at least 100/99, which is no
    defect."""
    sweep = sweeps()[name]
    case = cases()[name]
    assert census.sweep_held(sweep)
    assert sweep["net_directions"] == census.net_directions(case)
    raw = read_raw(case.candidate)
    for item in sweep["refused"]:
        index = int(item["r"])
        assert item["verdict"] in {census.CANDIDATE, census.AXIS_REFUSED}, index
        assert census.in_domain(raw, index, item["pose"]), index
        px, py = (Fraction(value) for value in item["pose"])
        original = mixed_exact(raw, px, py, index)
        assert census.CONTROL_SCALE * original == Fraction(item["capture"]) < 1, index
        assert original >= 1, index


def refusal(index: int, **overrides: Any) -> dict[str, Any]:
    """A made-up refusal that holds, with any field overridden."""
    return {
        "r": index,
        "verdict": census.CANDIDATE,
        "method": "interval-branch-and-bound",
        "pose": [1.0, 2.0],
        "coverage_refusal": True,
        "in_domain": True,
        "capture_below_1": True,
        "captures_agree": True,
        "original_at_least_1": True,
        **overrides,
    }


def sweep(
    refused: list[dict[str, Any]], verified: list[int], **overrides: Any
) -> dict[str, Any]:
    """A made-up sweep that holds when its refusals do, with any field overridden."""
    count = len(refused) + len(verified)
    return {
        "directions": count,
        "net_directions": count,
        "indices_complete": True,
        "returncode": 1,
        "summary_status": "REFUSED",
        "summary_refused_directions": [item["r"] for item in refused],
        "fault_injected_at_box": None,
        "premises_agree": True,
        "verified_directions": verified,
        "refused": refused,
        **overrides,
    }


def test_a_sweep_holds_only_with_a_witnessed_refusal_at_every_direction_it_refuses() -> None:
    """The acceptance rule of FC-1's fix, on made-up sweeps, one clause at a time."""
    good = [refusal(1), refusal(2)]
    assert census.sweep_held(sweep(good, [0, 3]))
    # The mutant verified everywhere: no refusal shows the verifier refuses a false claim.
    assert not census.sweep_held(sweep([], [0, 1, 2], returncode=0, summary_status="VERIFIED"))
    # Exit 1 and REFUSED, with no refusal among the rows.
    assert not census.sweep_held(sweep([], [0, 1, 2], summary_refused_directions=[1]))
    # Exit and summary disagree, each way.
    assert not census.sweep_held(sweep(good, [0], summary_status="VERIFIED"))
    assert not census.sweep_held(sweep(good, [0], returncode=0))
    # An admission refusal or a crash, not a coverage refusal.
    assert not census.sweep_held(sweep(good, [0], returncode=2))
    # Not every direction of the net ran, or an index ran twice or was skipped.
    assert not census.sweep_held(sweep(good, [0], net_directions=201))
    assert not census.sweep_held(sweep(good, [0], indices_complete=False))
    # The rows do not add up, or the summary names other refused directions.
    assert not census.sweep_held(sweep(good, [0], directions=4))
    assert not census.sweep_held(sweep(good, [0], summary_refused_directions=[1]))
    # A fault injected, or a mutant on another net or count.
    assert not census.sweep_held(sweep(good, [0], fault_injected_at_box=17))
    assert not census.sweep_held(sweep(good, [0], premises_agree=False))
    # Each clause of a refusal (CC-1, CC-2, CC-4, CC-5).
    for field in (
        "coverage_refusal",
        "in_domain",
        "capture_below_1",
        "captures_agree",
        "original_at_least_1",
    ):
        assert not census.sweep_held(sweep([refusal(1), refusal(2, **{field: False})], [0]))


@pytest.mark.parametrize(
    ("row", "coverage"),
    [
        ({"r": 3, "verdict": "counterexample-candidate"}, True),
        ({"r": 3, "verdict": "audit-failed"}, False),
        ({"r": 3, "verdict": "non-finite"}, False),
        ({"r": 3, "verdict": "unresolved"}, False),
        ({"r": 3, "verdict": "fault-injected"}, False),
        ({"r": 0, "verdict": "refused", "method": "axis-vertex-sweep"}, True),
        ({"r": 0, "verdict": "non-finite", "method": "axis-vertex-sweep"}, False),
    ],
)
def test_only_a_coverage_refusal_counts(
    monkeypatch: pytest.MonkeyPatch, row: dict[str, Any], *, coverage: bool
) -> None:
    """CC-1: a counterexample candidate whose witness the crate confirmed below the
    threshold, or the axis sweep's refusal; an audit failure, a non-finite enclosure, an
    unresolved box or an injected fault is a defect to surface, not a refusal."""
    raw = read_raw(cases()[RECOMPUTED].candidate)
    capture = Fraction(99, 100)
    monkeypatch.setattr(census, "mixed_exact", lambda *_: Fraction(1))
    pose = [5.0, 5.0]
    full = {**row}
    if row["r"]:
        full["witness"] = {
            "exact_pose": pose,
            "exact_below_threshold": True,
            "exact_coverage": str(capture),
        }
    else:
        full["argmin"] = ["5", "5"]
        full["min_certified_lower_bound"] = 0.99 - 1e-12
    record = census.refusal_record(raw, full, Fraction(99, 100), format_m=True)
    assert record["coverage_refusal"] is coverage
    assert record["capture"] == str(capture)
    assert record["capture_below_1"]
    assert record["captures_agree"]
    assert record["original_at_least_1"]
    assert record["in_domain"]
    assert census.refusal_held(record) is coverage


def test_a_refusal_outside_the_domain_or_disagreeing_with_the_crate_does_not_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CC-2 and CC-5: a pose outside lemma D's per-bin domain refutes nothing, and the
    exact capture must be the crate's."""
    raw = read_raw(cases()[RECOMPUTED].candidate)
    monkeypatch.setattr(census, "mixed_exact", lambda *_: Fraction(1))
    low, high = census.domain_bounds(raw, 3)
    row = {
        "r": 3,
        "verdict": census.CANDIDATE,
        "witness": {
            "exact_pose": [float(low) / 2, float(high)],
            "exact_below_threshold": True,
            "exact_coverage": "99/100",
        },
    }
    record = census.refusal_record(raw, row, Fraction(99, 100), format_m=True)
    assert not record["in_domain"]
    assert not census.refusal_held(record)
    row["witness"] = {**row["witness"], "exact_pose": [5.0, 5.0], "exact_coverage": "98/100"}
    record = census.refusal_record(raw, row, Fraction(99, 100), format_m=True)
    assert record["in_domain"]
    assert not record["captures_agree"]
    assert not census.refusal_held(record)


def test_the_per_bin_domain_is_lemma_ds() -> None:
    """At the axis the bin floor is 0 and the half-width 1/2; at node r it is rho(rD - D/2)
    with rho(t) = (1 + 2t - t^2) / (2 (1 + t^2)), from L - rho to rho on each axis."""
    raw = read_raw(cases()[RECOMPUTED].candidate)
    side, step = Fraction(raw["L"]), net_step(raw)
    assert census.domain_bounds(raw, 0) == (Fraction(1, 2), side - Fraction(1, 2))
    low = 5 * step - step / 2
    rho = (1 + 2 * low - low * low) / (2 * (1 + low * low))
    assert census.domain_bounds(raw, 5) == (rho, side - rho)
    assert census.in_domain(raw, 5, [str(rho), str(side - rho)])
    assert not census.in_domain(raw, 5, [str(rho - Fraction(1, 10**12)), "5"])


def test_a_sweep_reads_the_binarys_rows_and_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """scaled_sweep against a stub binary that prints fixed rows: the axis refusal is
    judged at its least vertex, a confirmed candidate at its witness, an audit failure is
    kept as a refusal that does not count, and rows and summary are reconciled."""
    raw = read_raw(cases()[RECOMPUTED].candidate)
    premises = entries()[RECOMPUTED]["premises"]
    monkeypatch.setattr(census, "mixed_exact", lambda *_: Fraction(1))
    witness = {
        "exact_pose": [5.0, 5.0],
        "exact_below_threshold": True,
        "exact_coverage": "99/100",
    }
    rows = [
        {
            "r": 0,
            "method": "axis-vertex-sweep",
            "verdict": "refused",
            "argmin": ["5", "5"],
            "min_certified_lower_bound": 0.99 - 1e-12,
        },
        {"r": 1, "verdict": "verified"},
        {"r": 2, "verdict": census.CANDIDATE, "witness": witness},
    ]
    stated = {
        key: premises.get(key)
        for key in ("D", "B", "L", "n", "net_origin", "format", "centre_domain")
    }
    summary = {
        "kind": "sqverify-fast-summary/v1",
        "status": "REFUSED",
        "refused_directions": [0, 2],
        "fault_injected_at_box": None,
        "premises": {**stated, "angle_count": 3, "input_sha256": "x"},
    }

    def stub(lines: list[dict[str, Any]]) -> Path:
        out = tmp_path / "rows.jsonl"
        out.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
        binary = tmp_path / "stub.sh"
        binary.write_text(f"#!/bin/sh\ncat {out}\nexit 1\n", encoding="utf-8")
        binary.chmod(0o755)
        return binary

    three = {**premises, "angle_count": 3}
    held = census.scaled_sweep(
        stub([*rows, summary]),
        raw,
        tmp_path / "m.json",
        1,
        factor=Fraction(99, 100),
        threads=1,
        premises=three,
    )
    assert held["indices_complete"]
    assert held["premises_agree"]
    assert [item["r"] for item in held["refused"]] == [0, 2]
    assert held["refused"][0]["pose"] == ["5", "5"]
    assert census.sweep_held(held)
    audit = [*rows[:2], {"r": 2, "verdict": "audit-failed", "witness": witness}, summary]
    failed = census.scaled_sweep(
        stub(audit),
        raw,
        tmp_path / "m.json",
        1,
        factor=Fraction(99, 100),
        threads=1,
        premises=three,
    )
    assert failed["refused"][1]["coverage_refusal"] is False
    assert not census.sweep_held(failed)
    # A row missing from the stream: the indices are not the net's.
    short = census.scaled_sweep(
        stub([rows[0], rows[2], summary]),
        raw,
        tmp_path / "m.json",
        1,
        factor=Fraction(99, 100),
        threads=1,
        premises=three,
    )
    assert not short["indices_complete"]
    assert not census.sweep_held(short)
    # A mutant whose summary states another count of squares: another certificate.
    other = {**summary, "premises": {**summary["premises"], "n": 1 + int(premises["n"])}}
    moved = census.scaled_sweep(
        stub([*rows, other]),
        raw,
        tmp_path / "m.json",
        1,
        factor=Fraction(99, 100),
        threads=1,
        premises=three,
    )
    assert not moved["premises_agree"]
    assert not census.sweep_held(moved)
    # The axis capture far above the sweep's certified bound: they do not agree (CR-5).
    loose = [{**rows[0], "min_certified_lower_bound": 0.9}, *rows[1:], summary]
    apart = census.scaled_sweep(
        stub(loose),
        raw,
        tmp_path / "m.json",
        1,
        factor=Fraction(99, 100),
        threads=1,
        premises=three,
    )
    assert apart["refused"][0]["captures_agree"] is False
    assert not census.sweep_held(apart)


def test_a_refusal_record_on_the_real_evaluator() -> None:
    """CR-4 of the re-check: refusal_record unpatched, at the receipt's least-bound
    centre of RECOMPUTED, where the original's exact capture is the receipt's."""
    receipt = controls()[RECOMPUTED]
    raw = read_raw(cases()[RECOMPUTED].candidate)
    index = int(receipt["index"])
    exact = Fraction(receipt["exact_capture_independent"])
    capture = census.CONTROL_SCALE * exact
    row = {
        "r": index,
        "verdict": census.CANDIDATE,
        "witness": {
            "exact_pose": receipt["centre"],
            "exact_below_threshold": capture < 1,
            "exact_coverage": str(capture),
        },
    }
    record = census.refusal_record(raw, row, census.CONTROL_SCALE, format_m=True)
    assert record["capture"] == str(capture)
    assert record["captures_agree"] is True
    assert record["in_domain"] is True
    assert record["original_at_least_1"] is (exact >= 1)
    assert record["capture_below_1"] is (capture < 1)


def near_run(**overrides: Any) -> dict[str, Any]:
    """A made-up near-threshold run that holds, with any field overridden."""
    mutation = {
        "factor": "9/10",
        "capture_at_centre": "999999/1000000",
        "capture_at_witness": "99/100",
        "witness_captures_agree": True,
        "centre_in_domain": True,
        "witness_in_domain": True,
        **overrides.pop("mutation", {}),
    }
    return {
        "name": "near-threshold",
        "expect": "refused",
        "returncode": 1,
        "verdict": census.CANDIDATE,
        "exact_below_threshold": True,
        "mutation": mutation,
        **overrides,
    }


def test_a_near_threshold_run_holds_only_on_a_confirmed_coverage_refusal() -> None:
    """CR-3 of the re-check: the near-threshold mutant's refusal is a counterexample
    candidate the crate confirmed below the threshold, its exact capture at the witness
    this tool's, and the claim false at a centre in the domain."""
    assert census.control_run_held(near_run())
    assert not census.control_run_held(near_run(verdict="audit-failed"))
    assert not census.control_run_held(near_run(exact_below_threshold=False))
    assert not census.control_run_held(near_run(returncode=0))
    assert not census.control_run_held(near_run(mutation={"witness_captures_agree": False}))
    outside = {"centre_in_domain": False, "witness_in_domain": False}
    assert not census.control_run_held(near_run(mutation=outside))
    above = {"capture_at_centre": "1", "capture_at_witness": "1"}
    assert not census.control_run_held(near_run(mutation=above))
    # Either place suffices.
    assert census.control_run_held(near_run(mutation={"centre_in_domain": False}))
    assert census.control_run_held(near_run(mutation={"capture_at_witness": None}))


def test_an_evidence_entry_states_a_sweep_control() -> None:
    """The v2 sentence names the refusals, the slack directions and the near factor."""
    run = {
        "sweep": {
            "directions": 201,
            "refused": [refusal(r) for r in range(187)],
            "verified_directions": list(range(14)),
        }
    }
    text = census.scaled_control_text(139, run)
    assert "refused at 187 of the 201 net directions" in text
    assert "the mutant verified at the other 14" in text
    assert "least vertex" in text
    near = {"mutation": {"factor": "453393222524583/500000000000000"}}
    assert census.near_factor(near) == "0.9068"


def test_one_control_capture_is_recomputed_from_the_candidate() -> None:
    """The centre's capture, and the 99/100 mutant's at its witness, from the candidate."""
    receipt = controls()[RECOMPUTED]
    raw = read_raw(cases()[RECOMPUTED].candidate)
    index = int(receipt["index"])
    x, y = (Fraction(value) for value in receipt["centre"])
    assert mixed_exact(raw, x, y, index) == Fraction(receipt["exact_capture_independent"])
    (scaled,) = (run for run in receipt["runs"] if run["name"] == "scaled-99-100")
    px, py = (Fraction(value) for value in scaled["witness"]["exact_pose"])
    capture = census.CONTROL_SCALE * mixed_exact(raw, px, py, index)
    assert capture == Fraction(scaled["mutation"]["capture_at_witness"]) < 1


def test_one_format_t_control_capture_is_recomputed_from_the_candidate() -> None:
    """The centre's capture, and the 99/100 mutant's at its witness, by
    `sqpack.rectangle_density`, which was written before the crate and shares no code
    with it, though the crate's authors read it (INDEPENDENCE.md)."""
    receipt = controls()[RECOMPUTED_T]
    case = rectangle_cases()[RECOMPUTED_T]
    candidate = load_candidate(case.candidate, n=case.n)
    cosine, sine = direction(int(receipt["index"]))
    x, y = (Fraction(value) for value in receipt["centre"])
    capture = coverage_at_point(candidate, x, y, cosine, sine)
    assert capture == Fraction(receipt["exact_capture_independent"])
    (scaled,) = (run for run in receipt["runs"] if run["name"] == "scaled-99-100")
    px, py = (Fraction(value) for value in scaled["witness"]["exact_pose"])
    witness = census.CONTROL_SCALE * coverage_at_point(candidate, px, py, cosine, sine)
    assert witness == Fraction(scaled["mutation"]["capture_at_witness"])
    assert witness < Fraction(TOKOHARU_THRESHOLD)


def test_each_reviewed_source_names_the_review_that_accepted_it() -> None:
    """The gate's digests are the driver's, each with a retained review, and only a review
    that read the declared-net path admits a row on a declared net."""
    assert set(census.REVIEWED_SOURCES) == REVIEWED_SOURCES
    for digest, source in census.REVIEWED_SOURCES.items():
        assert len(digest) == 64, digest
        assert (census.PROJECT.parent / source.review).is_file(), digest
    # The only source whose review read the declared-net path is main's at 910b6b12c.
    assert {
        digest for digest, source in census.REVIEWED_SOURCES.items() if source.declared_nets
    } == {"d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"}


def test_an_evidence_entry_names_the_reviewed_build_its_row_was_made_from() -> None:
    entry = entries()[RECOMPUTED]
    text = census.evidence_entry(
        cases()[RECOMPUTED], FOLDER, entry, audit_record=census.ROUTE_REVIEW, date="2026-10-05"
    )
    (record,) = safe_load(text)
    source = census.REVIEWED_SOURCES[entry["build"]["source_sha256"]]
    built = entry["build"]["source_sha256"][:8]
    assert f"these receipts' build is {built}..., the source at {source.commit}" in " ".join(
        record["replay"].split()
    )
    assert "at all 201 directions of the standard net" in " ".join(record["replay"].split())
    assert source.statement in " ".join(record["limitations"].split())


def test_an_evidence_entry_states_its_threads_and_the_review_of_the_source_that_ran() -> None:
    """The row's own thread count, and for a standard-net row built from a later reviewed
    source (main's at 910b6b12c), the review that accepted that source."""
    entry = entries()[RECOMPUTED]
    main_source = "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"
    rows = {
        "as run": entry,
        "main": {
            **entry,
            "threads": 1,
            "build": {**entry["build"], "source_sha256": main_source},
        },
    }
    texts = {
        name: safe_load(
            census.evidence_entry(
                cases()[RECOMPUTED], FOLDER, row, audit_record=census.ROUTE_REVIEW, date="x"
            )
        )[0]
        for name, row in rows.items()
    }
    limitations = {
        name: " ".join(record["limitations"].split()) for name, record in texts.items()
    }
    pinpoints = {
        name: " ".join(record["proof"]["pinpoints"].split()) for name, record in texts.items()
    }
    assert entry["threads"] == 2
    assert "CPU seconds at two threads and" in limitations["as run"]
    assert "CPU seconds at one thread and" in limitations["main"]
    assert "the crate source that ran" not in pinpoints["as run"]
    later = f"the crate source that ran, at 910b6b12c, by {census.DECLARED_NET_REVIEW}"
    assert later in pinpoints["main"]


def test_an_evidence_entry_refuses_a_row_built_from_unreviewed_source() -> None:
    """mixed_n18_L470's row was built at f007d7afd, a source not in REVIEWED_SOURCES."""
    name = DECLARED
    assert entries()[name]["build"]["source_sha256"] not in REVIEWED_SOURCES
    with pytest.raises(SystemExit, match="no review accepted"):
        census.evidence_entry(
            cases()[name], FOLDER, entries()[name], audit_record="x", date="2026-10-05"
        )


#: A stand-in digest for the declared-net row's build in the two tests below.
STAND_IN = "0" * 64


@pytest.mark.parametrize("scope", ["declared nets", "standard net only"])
def test_an_evidence_entry_on_a_declared_net_states_the_net_and_its_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, scope: str
) -> None:
    """The declared-net row as if built from a reviewed source, with a stand-in control:
    stated with its own net if that source's review read the declared-net path, and
    refused if it did not."""
    declared_nets = scope == "declared nets"
    source = census.ReviewedSource("910b6b12c", census.DECLARED_NET_REVIEW, "-", declared_nets)
    monkeypatch.setitem(census.REVIEWED_SOURCES, STAND_IN, source)
    name = DECLARED
    case = cases()[name]
    packet = tmp_path / case.packet
    packet.mkdir()
    receipt = FOLDER / case.packet / f"{name}.jsonl.gz"
    (packet / receipt.name).write_bytes(receipt.read_bytes())
    refused = {
        "verdict": "counterexample-candidate",
        "mutation": {"capture_at_centre": "0", "factor": "999/1000"},
    }
    control = {
        "status": "CONTROLS_REFUSED",
        "index": 408,
        "runs": [
            {"name": "original", "verdict": "verified"},
            {"name": "scaled-99-100", **refused},
            {"name": "near-threshold", **refused},
        ],
    }
    (packet / f"{name}.control.json").write_text(json.dumps(control), encoding="utf-8")
    entry = entries()[name]
    reviewed = {**entry, "build": {**entry["build"], "source_sha256": STAND_IN}}
    if not declared_nets:
        with pytest.raises(SystemExit, match="no review of the declared net accepted"):
            census.evidence_entry(case, tmp_path, reviewed, audit_record="x", date="2026-10-06")
        return
    text = census.evidence_entry(case, tmp_path, reviewed, audit_record="x", date="2026-10-06")
    (record,) = safe_load(text)
    replay = " ".join(record["replay"].split())
    limitations = " ".join(record["limitations"].split())
    assert "at all 416 directions of the net it declares" in replay
    assert "the source at 910b6b12c" in replay
    assert "at all 416 net directions" in limitations
    assert "of 416 half-angles of step 1/1001, with B(1 + D) = 500499/500500 < 1" in limitations
    assert "the other 415 by interval branch and bound" in limitations
    assert census.DECLARED_NET_REVIEW in " ".join(record["proof"]["pinpoints"].split())
    assert "the net its candidate declares (proof_net)" in record["proof"]["assumptions"][1]


def test_the_net_conditions_admit_the_declared_net_only_on_a_source_that_read_it() -> None:
    """`net_problems` on the retained declared-net row, as if its build were of a source
    whose review read the declared-net path, and of one whose review did not."""
    raw = read_raw(cases()[DECLARED].candidate)
    premises = entries()[DECLARED]["premises"]
    read_it = census.ReviewedSource("-", "-", "-", declared_nets=True)
    standard_only = census.ReviewedSource("-", "-", "-", declared_nets=False)
    assert net_problems(raw, premises, read_it) == []
    assert net_problems(raw, premises, standard_only) == [
        "a declared net, built from a source no declared-net review read"
    ]
    net = raw["proof_net"]
    assert net_problems({**raw, "proof_net": {**net, "step": "1/999"}}, premises, read_it) == [
        "D is the declared step",
        "net_last_tangent",
        "shrink_bound is B (1 + D)",
        "(b) B (1 + D) < 1",
        "(e) B (1 + D / (1 - D^2/4)) < 1",
    ]
    assert "(c) the last tangent past tan(pi/8)" in net_problems(
        {**raw, "proof_net": {**net, "last": 414}}, premises, read_it
    )
    assert net_problems({**raw, "proof_net": {**net, "last": "415"}}, premises, read_it) == [
        "proof_net is not exactly step and an integer last"
    ]
    assert net_problems({**raw, "net": {}}, premises, read_it) == [
        "a format L net block in a format M file"
    ]
    assert net_problems(raw, {**premises, "D": "83/40000"}, read_it) == [
        "D is the declared step",
    ]
    # One variant per remaining condition (finding FC-4 of the 6 October re-check).
    shapes = (
        {**net, "count": 415},
        {**net, "offset": "1/2002"},
        {"step": net["step"]},
    )
    for shape in shapes:
        assert net_problems({**raw, "proof_net": shape}, premises, read_it) == [
            "proof_net is not exactly step and an integer last"
        ], shape
    stretched = {**raw, "proof_net": {**net, "last": 2000}}
    assert "(d) the last tangent at most 1/2" in net_problems(stretched, premises, read_it)
    one_node = {**raw, "proof_net": {**net, "last": 0}}
    assert "(a) D > 0 and 2 <= N <= 2^16" in net_problems(one_node, premises, read_it)
    restated = {**raw, "certificate": {"D": "2/2002", "angle_count": 416}}
    assert net_problems(restated, premises, read_it) == []
    changed = {**raw, "certificate": {"D": "1/1000"}}
    assert net_problems(changed, premises, read_it) == ["metadata only restates the net"]
    for key, value, problem in (
        ("net_origin", "standard", "net_origin proof_net"),
        ("angle_count", 417, "angle_count is last + 1"),
        ("B", "9977/10000", "B is the file's"),
    ):
        assert net_problems(raw, {**premises, key: value}, read_it) == [problem], key


def test_the_exact_evaluator_reads_a_declared_net() -> None:
    """Finding DR-1 of the 6 October review: on mixed_n18_L470's net (step 1/1001) the
    control's evaluator gives the crate's exact capture at the least-bound leaf's centre,
    where the standard step scored another angle (1.2947 against 1.0703)."""
    raw = read_raw(cases()[DECLARED].candidate)
    entry = entries()[DECLARED]
    least = entry["least_bound_leaf_exact"]
    x, y = (Fraction(value) for value in least["centre"])
    assert net_step(raw) == Fraction(1, 1001) == Fraction(entry["premises"]["D"])
    assert mixed_exact(raw, x, y, int(least["r"])) == Fraction(least["exact_coverage"])


def test_the_census_reads_a_format_t_metadata_net(tmp_path: Path) -> None:
    """GN-5 of the review of jlevy/squares#485: a format T file whose metadata sets a net
    (rect_n40_L67's density on 401 directions of step 83/80000, as the release decided
    it) is read on that net, as admission reads it: its direction count, its step, the
    net its mutants keep, and the exact evaluator's angle. Before, the census counted 201
    directions, scored the standard step, dropped the net from the mutants and could not
    load the file in the evaluator."""
    original = rectangle_cases()["rect_n40_L67"].candidate
    raw = read_raw(original)
    finer = {**raw, "certificate": {**raw["certificate"], "D": "83/80000", "angle_count": 401}}
    path = tmp_path / "certified_candidate.json"
    path.write_text(json.dumps(finer), encoding="utf-8")
    case = census.Case("2026-10-10", "rect_n40_L67-401", 40, "67/10", path=path)
    assert metadata_net(finer) == (Fraction(83, 80000), 401)
    assert census.net_directions(case) == 401
    assert net_step(finer) == Fraction(83, 80000)
    assert scaled(finer, Fraction(99, 100))["certificate"] == {
        "D": "83/80000",
        "angle_count": 401,
    }
    # The standard net in metadata is still dropped from a mutant, as before.
    assert metadata_net(raw) == (Fraction(83, 40000), 201)
    assert "certificate" not in scaled(raw, Fraction(99, 100))
    assert census.net_directions(rectangle_cases()["rect_n40_L67"]) == 201
    # The release's control centre at direction 220 of the 401 net (the review's item 8).
    x, y = Fraction(3.353931795732347), Fraction(5.09801085267264)
    cosine, sine = direction(220, Fraction(83, 80000))
    expected = coverage_at_point(load_candidate(original, n=40), x, y, cosine, sine)
    assert census.exact_capture(case, finer, x, y, 220) == expected
    assert float(expected) == pytest.approx(1.0013165657619967, abs=1e-15)


def test_a_control_refuses_a_row_decided_on_another_net() -> None:
    """The census control evaluates on the file's net and refuses a row whose net differs."""
    entry = entries()[DECLARED]
    other = {**entry, "premises": {**entry["premises"], "D": "83/40000"}}
    with pytest.raises(SystemExit, match="not the file's"):
        census.control(Path("/nonexistent"), cases()[DECLARED], other)


def test_a_control_serves_format_m_and_format_t_rows_only() -> None:
    """Format L's centre domain is Tokoharu's, which format M's sweep does not compute
    (CR-7 of the FC-1 re-check), so its row is refused before the binary runs; a format T
    row takes the rectangle route, which needs the threshold its row was decided at."""
    entry = entries()[DECLARED]
    other = {**entry, "premises": {**entry["premises"], "format": "L"}}
    with pytest.raises(SystemExit, match="format M and format T rows only"):
        census.control(Path("/nonexistent"), cases()[DECLARED], other)
    rectangle = rectangle_entries()[RECOMPUTED_T]
    bare = {key: value for key, value in rectangle.items() if key != "threshold"}
    with pytest.raises(SystemExit, match="records no threshold"):
        census.control(Path("/nonexistent"), rectangle_cases()[RECOMPUTED_T], bare)
