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
import math
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
#: How far below its count a format T certificate's mass lies on the reviewed route:
#: n - 1/100, which the 6 October review of the route read for T-068's certificates, and
#: n - 1/1000, which the 26 October review of T-046's certificates read for rect_n27_L56
#: (review-2026-10-26-wand125-rectangle-certificates-t046.md, section 3). The theorem
#: needs only M < n, which admission recomputes; a mass at another distance from n waits
#: for a review that names it.
FORMAT_T_MASS_GAPS = frozenset({Fraction(1, 100), Fraction(1, 1000)})
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


#: The entries that decide a lemma with the crate's exact axis sweep and rest on no
#: census row, since the census rows are bounds: the near-axis lemmas of T-145 (on
#: wand125's rect_n40_L67, which only shares a census row's file) and T-157 (on
#: Guzhou0806's new-supports density, which has none). Their receipts are their packets'
#: (`test_audit_n40_new_supports`). A third lemma entry fails here until it is named.
LEMMA_ENTRIES = frozenset(
    {"E-n040-guzhou-continuous-pose-crate-axis", "E-n040-guzhou-new-supports-crate-axis"}
)


def test_only_the_named_lemma_entries_rest_on_no_census_row() -> None:
    lemmas = {ident for ident, entry in decided().items() if entry["claim"] != "lower-bound"}
    assert lemmas == LEMMA_ENTRIES


@cache
def cited() -> dict[str, str]:
    """Each evidence entry that `V-sqverify-fast` decides a bound for, by the census
    certificate it names; the lemma entries (`LEMMA_ENTRIES`) rest on no census row."""
    # The current record uses repository-relative paths; older evidence entries
    # retain their packing-relative spelling. Both must identify the same census case.
    by_path = {
        str(case.candidate.relative_to(root)): name
        for name, case in {**cases(), **rectangle_cases()}.items()
        for root in (census.PROJECT.parent, census.PROJECT)
    }
    found: dict[str, str] = {}
    for ident, entry in decided().items():
        if ident in LEMMA_ENTRIES:
            continue
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


def failed_controls() -> dict[Path, dict[str, Any]]:
    """Each control receipt kept after it failed closed, `CERT.control-failed-vN.json`,
    outside the receipts `controls()` reads."""
    return {
        path: json.loads(path.read_text(encoding="utf-8"))
        for folder in (FOLDER, RECTANGLES)
        for path in sorted(folder.glob("*/*.control-failed-v*.json"))
    }


def test_each_failed_control_receipt_is_kept_as_it_failed_and_decides_nothing() -> None:
    """A receipt kept after its control failed closed (n96's v1 of 3 October, n26's v2 of
    23 October) says `CONTROL_FAILED`, names its own certificate and packet and the
    candidate its census row read, and has the kind of a control receipt. Where no
    passing receipt was written beside it, no evidence entry the verifier decides rests on
    its certificate (A6 of PR #745's review A)."""
    failed = failed_controls()
    assert {path.name for path in failed} >= {
        "mixed_n96_L997.control-failed-v1.json",
        "mixed_n26_L5555.control-failed-v2.json",
    }
    for path, receipt in failed.items():
        name = path.name.split(".control-failed-v", 1)[0]
        assert receipt["kind"] in KINDS, path.name
        assert receipt["status"] == "CONTROL_FAILED", path.name
        assert receipt["certificate"] == name, path.name
        assert receipt["packet"] == path.parent.name, path.name
        assert receipt["candidate_sha256"] == row_of(name)["candidate_sha256"], path.name
        if name not in controls():
            assert name not in cited().values(), path.name


def test_the_census_view_reads_a_passing_control_beside_a_kept_failed_one() -> None:
    """The generated view reads n26's passing control of 4 November, not the failed one of
    23 October kept beside it, and marks a certificate with none `-`. Since that rerun no
    retained certificate has only a failed receipt; the view's `(kept)` mark for one is
    held by `test_the_mixed_report_tells_a_failed_control_from_none`."""
    view = (FOLDER / "README.md").read_text(encoding="utf-8")
    rows = {
        line.split("|")[1].strip().strip("`"): line
        for line in view.splitlines()
        if line.startswith("| `")
    }
    assert (
        (FOLDER / "wand125-fine-net-lower-bounds-446-release-2026-10-08")
        .joinpath("mixed_n26_L5555.control-failed-v2.json")
        .is_file()
    )
    assert rows["mixed_n26_L5555"].rstrip(" |").endswith("CONTROLS_REFUSED")
    assert rows["mixed_n37_L644"].rstrip(" |").endswith("-")


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
    at core side 9977/10000), Tokoharu's centre domain, a mass of n - 1/100 (or n - 1/1000,
    `FORMAT_T_MASS_GAPS`), densities far below lemma F3's caps, decided at Tokoharu's
    threshold 10001/10000 by a build of reviewed source with no fault injected, and
    controlled by a build of reviewed source.
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
        "mass n - 1/100 or n - 1/1000": (
            n - Fraction(premises["mass_exact"]) in FORMAT_T_MASS_GAPS
        ),
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
    for evidence_id in decided():
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


#: A sweep re-derives an exact capture at each direction it refused, so its cost grows
#: with the net: on 23 October, 415.68 s locally for mixed_n31_L59775's 2,073 refusals
#: against 14.90 s for mixed_n108_L1062's 201, beside a 12 s per-test ceiling. A sweep on
#: a declared net finer than the standard one runs whole in the deep surface, and the
#: pull request reads its refusals at every FINE_NET_STRIDE-th direction: 0, 296, ...,
#: 2072 on a 2,073-direction net, the directions of the eight-direction pricing sample,
#: and at the receipt's least-bound direction (`index`), where the original's capture is
#: nearest 1 and none of those eight falls (A5 of PR #745's review A).
FINE_NET_STRIDE = 296


def sweep_cases() -> list[Any]:
    """Each sweep: whole on the standard net; whole in the deep surface and sampled in
    the pull request on a finer declared net."""
    params: list[Any] = []
    for name, sweep in sorted(sweeps().items()):
        if sweep["net_directions"] > census.STANDARD_DIRECTIONS:
            params.append(pytest.param(name, "whole", marks=pytest.mark.slow, id=name))
            params.append(pytest.param(name, "sampled", id=f"{name}-sampled"))
        else:
            params.append(pytest.param(name, "whole", id=name))
    return params


@pytest.mark.parametrize(("name", "reading"), sweep_cases())
def test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness(
    name: str, reading: str
) -> None:
    """At every direction of the net, the 99/100 mutant is refused at one at least, and
    every direction that does not verify it is a coverage refusal at a pose in the per-bin
    domain where its capture, recomputed here from the candidate by the evaluator written
    apart from the crate, is the one the receipt keeps, below 1, with the original's at
    least 1. Where it verifies, the original captures at least 100/99, which is no
    defect. Sampled, the recomputation reads the refusals at every FINE_NET_STRIDE-th
    direction and at the receipt's least-bound direction."""
    sweep = sweeps()[name]
    case = cases()[name]
    assert census.sweep_held(sweep)
    assert sweep["net_directions"] == census.net_directions(case)
    raw = read_raw(case.candidate)
    least = int(controls()[name]["index"])
    refused = [
        item
        for item in sweep["refused"]
        if reading == "whole"
        or int(item["r"]) % FINE_NET_STRIDE == 0
        or int(item["r"]) == least
    ]
    assert refused, name
    if reading == "sampled":
        # The least-bound direction is where a re-derivation matters most, so the sample
        # must read a refusal there, as each fine-net sweep kept has one (on the standard
        # net the mutant can verify there: mixed_n96_L997's index 139).
        assert least in {int(item["r"]) for item in refused}, name
    for item in refused:
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


#: A made-up enclosure for a made-up axis row whose certified bound is its lower end and
#: whose mutant captures 99/100, standing in for the one `column_enclosure` recomputes from
#: a candidate where the row's vertex is not on that candidate's grid.
AROUND_99_100 = (0.99 - 1e-12, 0.99 + 1e-12)


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
    monkeypatch.setattr(census, "column_enclosure", lambda *_: AROUND_99_100)
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
    monkeypatch.setattr(census, "column_enclosure", lambda *_: AROUND_99_100)
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
    # The axis capture far above the sweep's certified bound, which is not the lower end
    # of the enclosure recomputed at its vertex: they do not agree (CR-5, F-1).
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


#: The retained fine-net certificate with a census row, a control receipt and its
#: candidate, whose axis refusal held under the constant allowance this rule replaced.
AXIS_RETAINED = "mixed_n37_L64975"
#: The constant allowance above the axis sweep's certified bound that the rule used
#: before F-1 of the 14 October review was fixed.
OLD_AXIS_ALLOWANCE = Fraction(1, 10**9)
#: The 14 October review's retained run of its sweep emulation at s(39)'s least axis
#: vertex for the 99/100 mutant (T-176): the crate's bound, the enclosure the sweep held
#: there and the exact capture. The control of 2 November found the same bound and capture.
REVIEW_N39 = (
    census.WEB
    / "wand125-fine-net-n37-n39-n44-2026-10-13/review/outputs"
    / "sweep_emulation-n39-scaled-99-100.json"
)
#: T-262's mixed_n94_L9965 (#890), whose whole-net control of 3 November failed closed at
#: the axis alone: the crate's bound, the enclosure the crate held at its least vertex (the
#: lower end its reported bound, the upper end from a build instrumented to report it,
#: review A of #892), which `column_enclosure` reproduces from the candidate, and the 99/100
#: mutant's exact capture there, to 40 digits.
N94_AXIS = (
    0.9930860126842824,
    (0.9930860126842824, 0.9930860149308234),
    Fraction("0.9930860138075014719938610497981535618057"),
)


def axis_row(pose: list[str], bound: float) -> dict[str, Any]:
    """The axis vertex sweep's row for a refused mutant."""
    return {
        "r": 0,
        "method": "axis-vertex-sweep",
        "verdict": census.AXIS_REFUSED,
        "argmin": pose,
        "min_certified_lower_bound": bound,
    }


def axis_item(name: str) -> dict[str, Any]:
    """The axis refusal a v2 control receipt keeps for its 99/100 mutant."""
    return next(item for item in sweeps()[name]["refused"] if item["r"] == 0)


@pytest.mark.parametrize("case", ["n39", "n94"])
def test_an_axis_refusal_is_judged_by_the_sweeps_enclosure_not_a_constant(
    monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    """F-1 of the 14 October review: at s(39) (T-176) and s(94) (T-262) the 99/100
    mutant's exact capture at the axis sweep's least vertex sits more than 1e-9 above the
    sweep's certified bound, at the middle of the enclosure the sweep held there. The
    refusal is sound and the capture is the one the sweep enclosed, so the axis refusal
    counts; the constant allowance of 1e-9 failed both whole-net controls closed."""
    if case == "n39":
        review = json.loads(REVIEW_N39.read_text(encoding="utf-8"))
        bound = review["crate_bound"]
        low, high = review["enclosure_at_vertex"]
        capture = Fraction(review["exact_capture_rational"])
        assert review["lower_end_equals_crate_bound"] is True
    else:
        bound, (low, high), capture = N94_AXIS
    assert capture - Fraction(bound) > OLD_AXIS_ALLOWANCE
    raw = read_raw(cases()[RECOMPUTED].candidate)
    monkeypatch.setattr(census, "mixed_exact", lambda *_: capture / census.CONTROL_SCALE)
    monkeypatch.setattr(census, "column_enclosure", lambda *_: (low, high))
    row = axis_row(["5", "5"], bound)
    record = census.refusal_record(raw, row, census.CONTROL_SCALE, format_m=True)
    assert record["capture"] == str(capture)
    assert record["captures_agree"] is True
    assert census.refusal_held(record)


def test_an_axis_capture_outside_the_sweeps_enclosure_does_not_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The rule is no looser than the sweep's arithmetic. On mixed_n37_L64975's candidate,
    whose enclosure at the 99/100 mutant's least axis vertex is 1.4e-10 wide, a capture
    5e-10 above the certified bound, which the constant 1e-9 admitted, lies outside the
    enclosure and does not count; nor does one past either end, nor a bound that is not
    the recomputed lower end, nor a vertex off the event grid. The receipt's own capture,
    at the middle, counts, and the enclosure is closed."""
    raw = read_raw(cases()[AXIS_RETAINED].candidate)
    item = axis_item(AXIS_RETAINED)
    bound = item["crate_lower_bound"]
    row = axis_row(item["pose"], bound)

    def judged(capture: Fraction, axis: dict[str, Any]) -> dict[str, Any]:
        monkeypatch.setattr(census, "mixed_exact", lambda *_: capture / census.CONTROL_SCALE)
        return census.refusal_record(raw, axis, census.CONTROL_SCALE, format_m=True)

    held = judged(Fraction(item["capture"]), row)
    assert held["captures_agree"] is True
    assert census.refusal_held(held)
    inside_old = Fraction(bound) + Fraction(5, 10**10)
    assert inside_old - Fraction(bound) <= OLD_AXIS_ALLOWANCE
    assert judged(inside_old, row)["captures_agree"] is False
    low, high = held["sweep_enclosure"]
    assert low == bound
    assert Fraction(high) - Fraction(low) < Fraction(15, 10**11)
    tiny = Fraction(1, 10**30)
    assert judged(Fraction(high), row)["captures_agree"] is True
    for capture in (inside_old, Fraction(high) + tiny, Fraction(bound) - tiny):
        record = judged(capture, row)
        assert record["captures_agree"] is False, float(capture)
        assert not census.refusal_held(record), float(capture)
    below = axis_row(item["pose"], math.nextafter(bound, -math.inf))
    assert judged(Fraction(item["capture"]), below)["captures_agree"] is False
    x, y = item["pose"]
    for pose in ([x, str(Fraction(y) + tiny)], [str(Fraction(x) + tiny), y]):
        record = judged(Fraction(item["capture"]), axis_row(pose, bound))
        assert record["sweep_enclosure"] is None, pose
        assert record["captures_agree"] is False, pose


def test_the_axis_rule_at_its_edges() -> None:
    """`axis_captures_agree` on its own: the enclosure is closed at both ends; the bound
    must be its lower end to the bit, so one ulp above or below fails; and a bound that is
    None, NaN or no number at all, a capture that is None, or no enclosure fails closed,
    returning False rather than raising."""
    low, high = 0.25, 0.75
    for capture in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        assert census.axis_captures_agree(low, capture, (low, high)), capture
    assert census.axis_captures_agree(repr(low), Fraction(1, 2), (low, high))
    for bound in (math.nextafter(low, math.inf), math.nextafter(low, -math.inf)):
        assert not census.axis_captures_agree(bound, Fraction(1, 2), (low, high)), bound
    for bound in (None, math.nan, "nan", "", "not a bound"):
        assert not census.axis_captures_agree(bound, Fraction(1, 2), (low, high)), bound
    # Shapes a JSON receipt could hold that no bound has: a list or a mapping, and a bool,
    # which float() would read as 0.0 or 1.0, the very ends of these enclosures.
    odd: list[Any] = [[low], {"bound": low}]
    for bound in odd:
        assert not census.axis_captures_agree(bound, Fraction(1, 2), (low, high)), bound
    assert census.axis_captures_agree(0.0, Fraction(1, 2), (0.0, 1.0))
    assert census.axis_captures_agree(1.0, Fraction(3, 2), (1.0, 2.0))
    flags: list[Any] = [False, True]
    assert not census.axis_captures_agree(flags[0], Fraction(1, 2), (0.0, 1.0))
    assert not census.axis_captures_agree(flags[1], Fraction(3, 2), (1.0, 2.0))
    assert not census.axis_captures_agree(low, None, (low, high))
    assert not census.axis_captures_agree(low, Fraction(1, 2), None)


def axis_receipts() -> list[Any]:
    """Each retained v2 control receipt, kept or failed, with a refusal at the axis."""
    params: list[Any] = []
    for path in sorted(FOLDER.glob("*/*.control*.json")):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if receipt.get("kind") != KINDS[1]:
            continue
        sweep = next(run["sweep"] for run in receipt["runs"] if "sweep" in run)
        item = next((item for item in sweep["refused"] if item["r"] == 0), None)
        if item is not None:
            params.append(pytest.param(path, item, id=path.name))
    return params


@pytest.mark.parametrize(("path", "item"), axis_receipts())
def test_each_retained_axis_refusal_is_the_crates_enclosure(
    path: Path, item: dict[str, Any]
) -> None:
    """At every retained v2 receipt's axis refusal, the walk on the candidate reproduces
    the crate's reported bound to the bit and holds the receipt's exact capture, so the
    rule counts it, including the receipts kept after the constant failed them closed
    (n26's of 23 October, n39's of 2 November and n94's of 3 November): thirteen
    measures from six packets on 4 November, n39's and n94's each in two receipts, the
    kept one and the one this rule passed, beside the instrumented crate's upper ends in
    `test_sqverify_fast_axis`."""
    case = cases()[path.name.split(".control", 1)[0]]
    raw = read_raw(case.candidate)
    x, y = (Fraction(value) for value in item["pose"])
    upper = census.domain_bounds(raw, 0)[1]
    enclosure = census.column_enclosure(raw, census.CONTROL_SCALE, x, y, upper)
    assert enclosure is not None
    assert enclosure[0] == item["crate_lower_bound"]
    capture = Fraction(item["capture"])
    assert Fraction(enclosure[0]) <= capture <= Fraction(enclosure[1])
    assert census.axis_captures_agree(item["crate_lower_bound"], capture, enclosure)
    if item.get("sweep_enclosure") is not None:
        assert list(enclosure) == item["sweep_enclosure"]
    if case.certificate == "mixed_n94_L9965":
        assert enclosure == N94_AXIS[1]


def test_an_axis_refusal_is_judged_on_the_recomputed_enclosure() -> None:
    """refusal_record unpatched at mixed_n37_L64975's 99/100 axis refusal: the enclosure
    recomputed from the candidate has the crate's bound as its lower end and holds the
    exact capture the receipt keeps, so the refusal counts, as `--control` judged it."""
    raw = read_raw(cases()[AXIS_RETAINED].candidate)
    item = axis_item(AXIS_RETAINED)
    row = axis_row(item["pose"], item["crate_lower_bound"])
    record = census.refusal_record(raw, row, census.CONTROL_SCALE, format_m=True)
    assert record["capture"] == item["capture"]
    assert record["sweep_enclosure"][0] == item["crate_lower_bound"]
    assert record["captures_agree"] is True
    assert census.refusal_held(record)


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
    assert "CPU seconds (wait4) at two threads and" in limitations["as run"]
    assert "CPU seconds (wait4) at one thread and" in limitations["main"]
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


def test_the_16_october_fine_net_packet_is_read_from_its_retained_release_members() -> None:
    packet = "wand125-fine-net-lower-bounds-2026-10-16"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert len(found) == 18
    root = census.WEB / packet / "release/certificates"
    for name, case in found.items():
        assert case.candidate == root / name / "candidate.json.gz"
        assert census.net_directions(case) == (2073 if case.n <= 51 else 201)


def test_the_n31_fine_net_packet_is_read_from_its_retained_release_members() -> None:
    """The 11 October n31 packet keeps its asset's members as the 16 October one does, and
    is classified as sharing the producer's crate, as that packet is."""
    packet = "wand125-fine-net-n31-2026-10-11"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert list(found) == ["mixed_n31_L59775"]
    case = found["mixed_n31_L59775"]
    root = census.WEB / packet / "release/certificates"
    assert case.candidate == root / "mixed_n31_L59775" / "candidate.json.gz"
    assert (case.n, case.side) == (31, "2391/400")
    assert census.net_directions(case) == 2073
    assert packet in census.SHARED_CRATE_PACKETS
    assert packet not in census.INDEPENDENT_MIXED_PACKETS


def test_the_446_release_packet_is_read_from_its_retained_release_members() -> None:
    """The release members of #446's four T-233 certificates are read like the n31
    packet's, and the packet shares the producer's crate."""
    packet = "wand125-fine-net-lower-bounds-446-release-2026-10-08"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    expected = {
        "mixed_n19_L48275": (19, "1931/400"),
        "mixed_n20_L49125": (20, "393/80"),
        "mixed_n26_L5555": (26, "1111/200"),
        "mixed_n27_L5655": (27, "1131/200"),
    }
    assert {name: (case.n, case.side) for name, case in found.items()} == expected
    root = census.WEB / packet / "release/certificates"
    for name, case in found.items():
        assert case.candidate == root / name / "candidate.json.gz"
        assert census.net_directions(case) == 2073
    assert packet in census.SHARED_CRATE_PACKETS
    assert packet not in census.INDEPENDENT_MIXED_PACKETS


def test_the_13_october_packet_is_read_from_its_retained_n37_and_n39_members() -> None:
    """T-178's mixed_n37_L64975 and T-176's mixed_n39_L66625 are read from the 13 October
    packet's release members, as the n31 packet's is. That packet's n44 member is not
    retained, so it holds two cases, and it shares the producer's crate."""
    packet = "wand125-fine-net-n37-n39-n44-2026-10-13"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert sorted(found) == ["mixed_n37_L64975", "mixed_n39_L66625"]
    root = census.WEB / packet / "release/certificates"
    for name, n, side in (
        ("mixed_n37_L64975", 37, "2599/400"),
        ("mixed_n39_L66625", 39, "533/80"),
    ):
        case = found[name]
        assert case.candidate == root / name / "candidate.json.gz"
        assert (case.n, case.side) == (n, side)
        assert census.net_directions(case) == 2073
    assert packet in census.SHARED_CRATE_PACKETS
    assert packet not in census.INDEPENDENT_MIXED_PACKETS


def test_the_10_october_n29_packet_is_read_from_its_retained_members() -> None:
    """T-132's mixed_n29_L582 is read from the 10 October n29 packet's release members,
    which `fine_net_followup retain` copied from the pinned asset, and the packet shares
    the producer's crate, as the other fine-net release packets do."""
    packet = "wand125-fine-net-n29-2026-10-10"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert list(found) == ["mixed_n29_L582"]
    case = found["mixed_n29_L582"]
    root = census.WEB / packet / "release/certificates"
    assert case.candidate == root / "mixed_n29_L582" / "candidate.json.gz"
    assert (case.n, case.side) == (29, "291/50")
    assert census.net_directions(case) == 2073
    assert packet in census.SHARED_CRATE_PACKETS
    assert packet not in census.INDEPENDENT_MIXED_PACKETS


def test_the_10_october_n28_n30_packet_is_read_from_its_retained_members() -> None:
    """T-142's mixed_n28_L57425 and T-143's mixed_n30_L58925 are read from the 10 October
    n28 and n30 packet's release members, which `fine_net_followup retain` copied from
    the pinned assets on 4 November, and the packet shares the producer's crate, as the
    other fine-net release packets do. Neither has a census row yet: no review reads
    them (think-4ul6)."""
    packet = "wand125-fine-net-n28-n30-2026-10-10"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert sorted(found) == ["mixed_n28_L57425", "mixed_n30_L58925"]
    root = census.WEB / packet / "release/certificates"
    for name, n, side in (
        ("mixed_n28_L57425", 28, "2297/400"),
        ("mixed_n30_L58925", 30, "2357/400"),
    ):
        case = found[name]
        assert case.candidate == root / name / "candidate.json.gz"
        assert (case.n, case.side) == (n, side)
        assert census.net_directions(case) == 2073
    assert packet in census.SHARED_CRATE_PACKETS
    assert packet not in census.INDEPENDENT_MIXED_PACKETS


def test_the_890_dilation_is_read_at_its_upstream_path_and_reproduces_the_producer() -> None:
    """#890's certificate is not Hosono's and sits at its own upstream path, which
    `MIXED_FILES` names under the format M convention's census name. Its producer decided
    it with this repository's own sqverify-fast, so a row of it is a reproduction with the
    producer's code, classified apart from the shared-crate and independent packets."""
    packet = "ozden-s94-lower-bound-2026-11-03"
    found = {name: case for name, case in cases().items() if case.packet == packet}
    assert list(found) == ["mixed_n94_L9965"]
    case = found["mixed_n94_L9965"]
    assert case.candidate == census.WEB / packet / "source/certificate/n94_L9965.json.gz"
    assert (case.n, case.side) == (94, "1993/200")
    assert census.net_directions(case) == 600
    assert packet in census.SAME_CRATE_PACKETS
    assert packet not in census.SHARED_CRATE_PACKETS | census.INDEPENDENT_MIXED_PACKETS
    fields, _ = census.mixed_relationship(case)
    assert fields == ["    relationship_to_generator: same-implementation"]


def test_the_890_replay_entry_is_what_the_census_prints() -> None:
    """E-ozden-890-n94-9965-sqverify-fast-replay is `--evidence`'s entry for
    mixed_n94_L9965, field for field (F1 of #898's review): Özden's dilation as the
    theorem's subject, the issue's digests as the candidate's custody, the second checker
    retained and not run, the replay's agreement with the source's receipts, the controls
    of 4 November with the axis enclosure they were judged by, the failed receipt kept,
    the replay's coverage, and the candidate named as its report names it. None of the
    Hosono packets' wording survives, nor a clean-room claim beside a same-implementation
    replay; Hosono's own packets keep theirs."""
    name = "mixed_n94_L9965"
    text = census.evidence_entry(
        cases()[name],
        FOLDER,
        entries()[name],
        audit_record="docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md",
        date="2026-11-03",
        control_date="2026-11-04",
    )
    (generated,) = safe_load(text)
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    (committed,) = (item for item in register["evidence"] if item["id"] == generated["id"])
    assert generated == committed
    flat = " ".join(text.split())
    for wording in ("Hiroaki Hosono's mixed_n94_L9965", "mixed-fetch", "tarball", "clean-room"):
        assert wording not in flat, wording
    assert "applied to Doğa Özden's mixed_n94_L9965" in flat
    assert census.packet_provenance(cases()["mixed_n37_L64975"]) is census.HOSONO_PROVENANCE
    assert "{certificate}" in census.HOSONO_PROVENANCE.subject


#: T-233's four certificates, each with its replay entry's id and the day its controls ran
#: (n26's were written again under the enclosure rule; the other three on the capture's).
T233_REPLAYS = {
    "mixed_n19_L48275": ("E-wand125-fine-net-446-n19-48275-sqverify-fast-replay", "2026-10-23"),
    "mixed_n20_L49125": ("E-wand125-fine-net-446-n20-49125-sqverify-fast-replay", "2026-10-23"),
    "mixed_n26_L5555": ("E-wand125-fine-net-446-n26-5555-sqverify-fast-replay", "2026-11-04"),
    "mixed_n27_L5655": (
        "E-wand125-fine-net-n27-5655-followup-sqverify-fast-replay",
        "2026-10-23",
    ),
}


@pytest.mark.parametrize("name", sorted(T233_REPLAYS))
def test_each_t233_replay_entry_is_what_the_census_prints(name: str) -> None:
    """T-233's four replay entries are `--evidence`'s, field for field, with the stage 4
    review of 23 October as their audit record. #446's report of n = 19, 20 and 26 names
    their directory, so each certificate gets its own entry, scoped to its count and naming
    its candidate (`replay_identity`); n = 27's follow-up report names its candidate. Only
    n26's states a failed control kept beside its passing one."""
    ident, controlled = T233_REPLAYS[name]
    case = cases()[name]
    text = census.evidence_entry(
        case,
        FOLDER,
        entries()[name],
        audit_record="docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md",
        date="2026-10-23",
        control_date=controlled,
    )
    (generated,) = safe_load(text)
    assert generated["id"] == ident
    assert generated["scope"] == {"n_values": [case.n]}
    assert generated["certificate"] == str(case.candidate.relative_to(census.PROJECT.parent))
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    (committed,) = (item for item in register["evidence"] if item["id"] == ident)
    assert generated == committed
    kept = f"{name}.control-failed-v2.json" in " ".join(text.split())
    assert kept is (name in census.CONTROL_HISTORY)
    assert (FOLDER / case.packet / f"{name}.control-failed-v2.json").is_file() is kept


def test_a_report_over_several_certificates_names_each_by_its_directory() -> None:
    """`reports_candidate` takes a reported entry that names the candidate, in either
    spelling, or a directory holding it with the count in its scope, and nothing else."""
    relative = "resources/web/p/release/certificates/mixed_n26_L5555/candidate.json.gz"
    directory = "packing/resources/web/p/release/certificates/"
    shared = {"certificate": directory, "scope": {"n_values": [19, 20, 26]}}
    assert census.reports_candidate(shared, relative, 26)
    assert not census.reports_candidate(shared, relative, 27)
    assert not census.reports_candidate(
        {**shared, "certificate": directory.removesuffix("/")}, relative, 26
    )
    assert not census.reports_candidate(
        {**shared, "certificate": "packing/resources/web/q/"}, relative, 26
    )
    for named in (relative, f"packing/{relative}"):
        assert census.reports_candidate({"certificate": named}, relative, 26)
    assert not census.reports_candidate({"certificate": None}, relative, 26)


def test_a_directory_report_without_a_run_of_counts_in_its_id_is_refused() -> None:
    """`replay_identity` names each certificate of a directory report by replacing its
    id's run of counts; an id with no such run (one count, or none) is refused rather
    than given an entry that would collide with another certificate's (#903 review F7)."""
    case = cases()["mixed_n26_L5555"]
    relative = str(case.candidate.relative_to(census.PROJECT))
    directory = "packing/" + relative.rsplit("mixed_n26_L5555/", 1)[0]
    shared = {"certificate": directory, "scope": {"n_values": [19, 20, 26]}}
    ident, scope, certificate = census.replay_identity(
        {**shared, "id": "E-x-446-n19-n20-n26-report"}, case, relative
    )
    assert (ident, scope) == ("E-x-446-n26-5555-sqverify-fast-replay", "26")
    assert certificate == f"packing/{relative}"
    for ident in ("E-x-446-n26-report", "E-x-446-report"):
        with pytest.raises(SystemExit, match="names no run of counts"):
            census.replay_identity({**shared, "id": ident}, case, relative)


def test_the_t132_replay_entry_is_what_the_census_prints() -> None:
    """T-132's replay entry is `--evidence`'s, field for field, with the stage 4 review of
    4 November as its audit record. Its follow-up report names the candidate retained in
    the n29 packet, so the entry takes the report's id, scope and path, and it states no
    failed control: the control of 4 November passed under #892's enclosure rule on its
    first run, and the entry names the enclosure its axis refusal lies in."""
    name = "mixed_n29_L582"
    case = cases()[name]
    text = census.evidence_entry(
        case,
        FOLDER,
        entries()[name],
        audit_record="docs/project/reviews/review-2026-11-04-wand125-fine-net-n29.md",
        date="2026-11-04",
    )
    (generated,) = safe_load(text)
    ident = "E-wand125-fine-net-n29-582-followup-sqverify-fast-replay"
    assert generated["id"] == ident
    assert generated["scope"] == {"n_values": [29]}
    assert generated["certificate"] == str(case.candidate.relative_to(census.PROJECT.parent))
    register = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    (committed,) = (item for item in register["evidence"] if item["id"] == ident)
    assert generated == committed
    assert name not in census.CONTROL_HISTORY
    assert not (FOLDER / case.packet / f"{name}.control-failed-v2.json").exists()
    assert controls()[name]["status"] == "CONTROLS_REFUSED"
    assert "[0.9908643538541804, 0.9908643548997059]" in " ".join(text.split())
