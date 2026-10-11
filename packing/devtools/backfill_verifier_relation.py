#!/usr/bin/env python3
"""Name the verification programs behind every evidence entry, and audit its relation.

Every evidence entry in `frontier/evidence.yaml` whose method runs code, or that names a
replay, lists in `verifiers` the programs of `frontier/verifiers.yaml` that verified its
claim: for a source's report the checker the source says it ran, for a replay or an
audit every program the replay runs. Its existing `relationship_to_generator` says how
that code stands to the code the result's producer used (epistemics.md, Confirmation):
`same-implementation` or `generator` for the producer's own code re-run,
`shared-components` for separately written code reusing named parts of it,
`independent-implementation` for code sharing none of it.

This tool does three things, each re-runnable and idempotent:

1. **Fills `verifiers`** in every entry that lacks the field and runs code, from its
   replay command, the packet its record names and the checker digests, writing one line
   after the entry's `replay_status` and leaving every other byte as it was. An entry
   that already carries `verifiers` is never rewritten, so a person's decision stands.
2. **Audits** every entry's `relationship_to_generator` and `performed_by` against what
   its replay runs: an `independent-implementation` whose replay re-runs the producer's
   checker, or a value the record's own limitations contradict.
3. **Fixes the clear cases** in `FIXES`, each with the evidence for it, and only while
   the entry still holds the value the fix replaces. Everything else the audit finds is
   printed for a human decision and left alone.

Other lanes add evidence entries concurrently, so the owner re-runs this after a merge
rather than resolving the fields by hand. The classification is a table read in order,
first match wins: `DECISIONS` (entries a person had to read), `REPLAY_RULES` (what an
entry's replay command runs), `SOURCE_RULES` and `NAMED_PROGRAMS` (the checker a source's
own record names). An entry none of them matches is printed and left alone.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.backfill_verifier_relation
    uv run --frozen --all-extras --group dev python -m \
        devtools.backfill_verifier_relation --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from devtools.verifier_registry import (
    INDEPENDENT,
    NOT_APPLICABLE,
    RANK,
    SAME,
    SHARED,
    load,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "frontier" / "evidence.yaml"

#: Methods whose verification is a program run, as performed or as the source reports it.
CODE_METHODS = frozenset(
    {
        "numerical-f64",
        "numerical-multiprecision",
        "interval-certified",
        "exact-algebraic",
        "proof-assistant-checked",
    }
)
CONFIRMING = frozenset({"audited-here", "replayed-here", "independently-external"})
#: The `performed_by` each `origin` implies: who ran it.
PERFORMERS = {
    "replayed-here": {"repository"},
    "audited-here": {"repository"},
    "independently-external": {"independent-external"},
    "external": {"source-author", "independent-external"},
}

Entry = Mapping[str, Any]
PRODUCER = SAME


@dataclass(frozen=True)
class Classification:
    """The programs behind one entry, the relation they read as, and the rule that said so.
    `relation` is the expectation the audit holds the recorded value to, or none where
    nothing ran here to compare."""

    verifiers: tuple[str, ...]
    relation: str | None
    rule: str


def runs(verifiers: Sequence[str], relation: str | None, rule: str = "") -> Classification:
    return Classification(tuple(verifiers), relation, rule)


@dataclass(frozen=True)
class Fix:
    """A clear correction of `relationship_to_generator`, with its evidence."""

    old: str
    new: str
    evidence: str
    shared: tuple[str, ...] = ()


#: The shared parts named where a second decision reuses the producer's code.
FRACTIONAL_SHARED = ("the certificate loader and object", "the closed-form Conditions 1 to 4")
THRESHOLD_SHARED = (
    "the certificate loader",
    "the closed-form conditions",
    "the weight scale",
    "the direction net",
)
N11_SHARED = (
    (
        "this repository's exact arithmetic and construction primitives (clipping, "
        "closed-cover and collision kernels), which the published source bundles"
    ),
)
_INTERVAL_EVIDENCE = (
    "its limitations say the interval route shares {} with the exact route, the code that "
    "produced and first decided the certificate, and no part of how the last condition is "
    "decided"
)
_OWN_TOOL = (
    "this project's own result; the replay re-runs {} on the record that module wrote, so the "
    "producing code checks its own output"
)

#: Clear corrections, applied only while the entry still says `old`.
FIXES: dict[str, Fix] = {
    "E-wand125-point-source-replay": Fix(
        INDEPENDENT,
        SAME,
        (
            "the replay runs wand125's own src/check_with_sqpack.py, whose docstring says the "
            "source verifies its certificates with this repository's verifier, unmodified: the "
            "producer's verification route itself"
        ),
    ),
    "E-wand125-n052-derived-lower": Fix(
        INDEPENDENT,
        SAME,
        "the same replay as E-wand125-point-source-replay, on one certificate",
    ),
    "E-wand125-n068-derived-lower": Fix(
        INDEPENDENT,
        SAME,
        "the same replay as E-wand125-point-source-replay, on one certificate",
    ),
    "E-n045-wand125-point-cover-source-replay": Fix(
        INDEPENDENT,
        SAME,
        (
            "the replay is the source's verify.sh, which builds and runs zmx2, the checker "
            "the source verified the cover with; its limitations call it the same "
            "implementation as E-n045-evand-mixed-cover-zmx2-replay"
        ),
    ),
    "E-n061-wand125-point-cover-zmx2-replay": Fix(
        INDEPENDENT,
        SAME,
        (
            "the replay builds and runs zmx2 6b7f0f79, the digest the source's own verify.sh "
            "pins and verifies the cover with; its review says so, as wand125's own verify.sh "
            "already uses it. The pattern of E-n045-wand125-point-cover-source-replay"
        ),
    ),
    "E-n045-wand125-point-cover-report": Fix(
        INDEPENDENT,
        SAME,
        (
            "the source reports the cover decided by Evan Daniel's unmodified zmx2, the "
            "checker it verifies its covers with, as its replay here "
            "(E-n045-wand125-point-cover-source-replay) shows"
        ),
    ),
    "E-n011-global-optimality-independent": Fix(
        INDEPENDENT,
        SHARED,
        (
            "its limitations say the geometric replay shares disclosed local arithmetic and "
            "construction primitives with the source and is not a fully disjoint implementation"
        ),
        N11_SHARED,
    ),
    "E-fractional-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format("the certificate object and the closed-form conditions"),
        FRACTIONAL_SHARED,
    ),
    "E-n011-fractional-net1440-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format("the certificate object and the closed-form conditions"),
        FRACTIONAL_SHARED,
    ),
    "E-n011-corner-class-96-25-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format("the certificate object and the closed-form conditions"),
        FRACTIONAL_SHARED,
    ),
    "E-n011-threshold-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format(
            "the loader, the closed-form conditions, the weight scale and the net"
        ),
        THRESHOLD_SHARED,
    ),
    "E-n011-threshold-net1440-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format(
            "the loader, the closed-form conditions, the weight scale and the net"
        ),
        THRESHOLD_SHARED,
    ),
    "E-n011-threshold-net2880-interval-decision": Fix(
        INDEPENDENT,
        SHARED,
        _INTERVAL_EVIDENCE.format(
            "the loader, the closed-form conditions, the weight scale and the net"
        ),
        THRESHOLD_SHARED,
    ),
    "E-n005-second-order-rigidity": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("devtools.assess_n5_rigidity")
    ),
    "E-n005-fixed-side-local-rigidity": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("devtools.assess_n5_rigidity")
    ),
    "E-n040-first-order-flexibility": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("devtools.assess_n40_rigidity")
    ),
    "E-n011-trump-local-rigidity": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("cases.trump11.tangent_cones")
    ),
    "E-translation-escape-not-rigid": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("devtools.screen_translation_escape")
    ),
    "E-side2-center-lower": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("cases.small_n.optimal_moduli")
    ),
    "E-n011-repaired-lower": Fix(
        INDEPENDENT, SAME, _OWN_TOOL.format("cases.stromquist.repaired_cover")
    ),
}

#: Entries whose programs needed a person to read the record, with the reason.
DECISIONS: dict[str, tuple[Classification, str]] = {
    "E-n061-wand125-point-cover-evand-replay-report": (
        runs(("V-evand-zeromargin-py", "V-evand-zmcheck", "V-evand-zmx2"), None, "decision"),
        (
            "Daniel ran his own zeromargin.py and zmcheck on wand125's cover, and zmx2, the "
            "checker wand125 tuned the cover against, which he calls a reproduction. The "
            "record says independent-implementation; whether two programs by zmx2's author are "
            "independent of zmx2 is the owner's call."
        ),
    ),
    "E-n011-corner-class-96-25-interval-decision": (
        runs(("V-sqpack-fractional-interval",), SHARED, "decision"),
        (
            "Its replay command is the exact decision's: the interval route is the second "
            "decision inside one decide_certificate --corner-clip invocation."
        ),
    ),
    "E-k2m3-evand-valid7-qx2-replay": (
        runs(("V-evand-qx2-zm-py",), SAME, "decision"),
        (
            "Its replay stages the source's own qx2_zm.py at the hashes run V3 names and runs "
            "it here; plan_valid7_replay only copies, shards and compares leaves, and decides "
            "nothing. The record says same-implementation."
        ),
    ),
    "E-n012-levy-15680000-3949423-generator": (
        runs(("V-evand-angle-net-verify",), None, "decision"),
        (
            "This project re-weighted Daniel's points and decided the result with Daniel's "
            "own angle-net verify (main.rs 226ef3f1), built by s12_angle_net_rescale; the "
            "record names the producer's run."
        ),
    ),
    "E-n012-levy-15680000-3949423-source-replay": (
        runs(("V-evand-angle-net-verify",), SAME, "decision"),
        (
            "It rebuilds the retained s12/verify crate at main.rs 226ef3f1 with overflow "
            "checks and runs it on the certificate: the producer's verifier re-run."
        ),
    ),
    "E-n012-levy-15680000-3949423-audit": (
        runs(("V-audit-s12-reweighted",), NOT_APPLICABLE, "decision"),
        (
            "devtools.audit_s12_reweighted checks the certificate's premises in integers "
            "and Fraction and leaves coverage to the verifier: a premise check, neither a "
            "replay of the decision nor an implementation of it."
        ),
    ),
    "E-n032-evand-zmx2-full-sym-report": (
        runs(("V-evand-zmx2",), SAME, "decision"),
        (
            "It reports one zmx2 --sym-atoms run; its record names zeromargin.py and zmcheck "
            "only to say what zmx2's point test derives from and which pair avoids zmx2."
        ),
    ),
    "E-wand125-tools-ceiling-certificates": (
        runs(("V-rectangle-ceiling",), None, "decision"),
        (
            "The repository's ceiling certificates, written and decided by its own "
            "certify_rectangle_ceiling; the source's l_cap.py computes floats and checks "
            "nothing, so no checker of the source's exists to share code with. The record "
            "reads the check as independent of the source; its review names what was read."
        ),
    ),
    "E-franciscouzo-2026-09-27-report": (
        runs((), None, "decision"),
        "The source prints binary64 poses and states no method, tolerance or checker.",
    ),
    "E-casson-2026-09-23-report": (
        runs((), None, "decision"),
        (
            "The source names Ellsworth's check_packing.py and its own 50-digit checker; the "
            "packet retains neither."
        ),
    ),
    "E-n017-certified-endpoint": (
        runs(
            ("V-n17-endpoint-checkers", "V-audit-n17-endpoint-receipt"), INDEPENDENT, "decision"
        ),
        (
            "This project's own endpoint. The root and endpoint checkers decide it; the "
            "replayed audit imports neither and reconstructs every interval record, which "
            "the record reads as independent of the endpoint producer."
        ),
    ),
}


def _text(entry: Entry, *fields: str) -> str:
    parts: list[str] = []
    for name in fields:
        value = entry.get(name)
        if isinstance(value, Mapping):
            parts.extend(str(item) for item in value.values())
        elif value is not None:
            parts.append(str(value))
    return " ".join(" ".join(parts).split())


Test = Callable[[Entry], bool]
Rule = tuple[str, Test, Classification]


def _in_replay(pattern: str) -> Test:
    compiled = re.compile(pattern)
    return lambda entry: bool(compiled.search(_text(entry, "replay")))


def _and(*tests: Test) -> Test:
    return lambda entry: all(test(entry) for test in tests)


def _source(pattern: str) -> Test:
    compiled = re.compile(pattern)
    return lambda entry: bool(compiled.search(str(entry.get("source_key") or "")))


def _id(pattern: str) -> Test:
    compiled = re.compile(pattern)
    return lambda entry: bool(compiled.search(str(entry.get("id") or "")))


#: What an entry's replay runs, matched on its command. Where one command names several
#: programs, the more specific signature comes first.
REPLAY_RULES: tuple[Rule, ...] = (
    # External checkers re-run on their retained bytes: the producer's code.
    (
        "Tokoharu's verify.cpp under the wand125 rectangle preflight",
        _in_replay(r"audit_wand125_rectangles"),
        runs(("V-tokoharu-verify-cpp", "V-audit-wand125-rectangles"), PRODUCER),
    ),
    (
        "Tokoharu's verify.cpp under the density preflight",
        _in_replay(r"audit_tokoharu_density"),
        runs(("V-tokoharu-verify-cpp", "V-audit-tokoharu-density"), PRODUCER),
    ),
    (
        "wand125's mixed_rotated_verify.cpp through the bundle driver",
        _in_replay(r"audit_wand125_point_and_mixed mixed-replay"),
        runs(
            ("V-wand125-mixed-rotated-verify-cpp", "V-audit-wand125-point-and-mixed"), PRODUCER
        ),
    ),
    (
        "wand125's verify_mixed_full_proof.py, which compiles its mixed_rotated_verify.cpp",
        _in_replay(r"verify_mixed_full_proof\.py proof"),
        runs(
            (
                "V-wand125-verify-mixed-full-proof-py",
                "V-wand125-mixed-rotated-verify-cpp",
                "V-audit-wand125-point-and-mixed",
            ),
            PRODUCER,
        ),
    ),
    (
        "wand125's verify_portable.py for the point-only cover bundle",
        _in_replay(r"verify_portable\.py"),
        runs(("V-wand125-verify-portable-py", "V-audit-wand125-point-and-mixed"), PRODUCER),
    ),
    (
        "Daniel's s12 verify and squarepacker's indep_check.cpp",
        _in_replay(r"indep_check"),
        runs(("V-evand-angle-net-verify", "V-squarepacker-indep-check-cpp"), PRODUCER),
    ),
    (
        "wand125's general pose tree under the row census",
        _in_replay(r"check_general_pose_tree_census"),
        runs(("V-wand125-tools", "V-check-general-pose-tree-census"), PRODUCER),
    ),
    (
        "wand125's unified_linear_verify.cpp through the bundle driver",
        _in_replay(r"audit_wand125_linear"),
        runs(("V-wand125-unified-linear-verify-cpp", "V-audit-wand125-linear"), PRODUCER),
    ),
    (
        "the source's verify.sh, which runs zmx2",
        _in_replay(r"sh verify\.sh WORK"),
        runs(("V-evand-zmx2", "V-audit-wand125-point-and-mixed"), PRODUCER),
    ),
    (
        "zmx2 through the replay driver, audited",
        _in_replay(r"replay_evand_zmx2"),
        runs(("V-evand-zmx2", "V-replay-evand-zmx2", "V-audit-evand-mixed-covers"), PRODUCER),
    ),
    (
        "zmx2 from the overlaid packets, audited",
        _in_replay(r"zmx2 cert|certificates/s\d+/verify\.sh"),
        runs(("V-evand-zmx2", "V-audit-evand-mixed-covers"), PRODUCER),
    ),
    (
        "zeromargin.py through zm_d4_sweep.py, compared",
        _in_replay(r"zm_d4_sweep"),
        runs(("V-evand-zeromargin-py", "V-compare-evand-s32-sweep"), PRODUCER),
    ),
    (
        "the angle-net verify and xcheck.py",
        _in_replay(r"xcheck\.py"),
        runs(("V-evand-angle-net-verify", "V-evand-xcheck-py"), PRODUCER),
    ),
    (
        "the source's Lean development, built here",
        _in_replay(r"lake build"),
        runs(("V-evand-lean",), PRODUCER),
    ),
    (
        "wand125's check_with_sqpack.py and this repository's verifier",
        _in_replay(r"check_with_sqpack"),
        runs(("V-wand125-check-with-sqpack", "V-sqpack-fractional-exact"), PRODUCER),
    ),
    (
        "Wang and Li's verify.py, and Kleddamag's launcher adapted to their certificate",
        _in_replay(r"verify_wang_li|PASS_FRESH_TWO_IMPLEMENTATION"),
        runs(("V-wang-li-n11-verify", "V-kleddamag-n11-verify"), PRODUCER),
    ),
    (
        "Kleddamag's n = 11 verify.py",
        _in_replay(r"N11_SOURCE_TREE"),
        runs(("V-kleddamag-n11-verify",), PRODUCER),
    ),
    (
        "Guzhou0806's paired launcher: its verify.cpp beside Kleddamag's BigInt checker",
        _in_replay(r"replay\.js\b"),
        runs(
            ("V-guzhou-n17-verify-cpp", "V-kleddamag-n17-verify", "V-audit-guzhou-r068"),
            PRODUCER,
        ),
    ),
    (
        "Guzhou0806's R052 verify.py",
        _in_replay(r"R052/verify\.py"),
        runs(("V-guzhou-r052-verify-py",), PRODUCER),
    ),
    (
        "Guzhou0806's R012 verify.py",
        _in_replay(r"R012/verify\.py"),
        runs(("V-guzhou-r012-verify-py",), PRODUCER),
    ),
    (
        "Kleddamag's n = 17 verify.py",
        _in_replay(r"kleddamag-17-squares-certified-bound|on verify\.py --jobs"),
        runs(("V-kleddamag-n17-verify",), PRODUCER),
    ),
    (
        "Massaccesi's verifier",
        _in_replay(r"massaccesi-verify"),
        runs(("V-massaccesi-n17-verify-py",), PRODUCER),
    ),
    (
        "Burns's verifier",
        _in_replay(r"burns-verify"),
        runs(("V-burns-n17-verify-py",), PRODUCER),
    ),
    (
        "Mira's point checker",
        _in_replay(r"replay_mira_python"),
        runs(("V-mira-17squares-point-checker",), PRODUCER),
    ),
    (
        "Fort's point checker",
        _in_replay(r"replay_fort_python"),
        runs(("V-stanislavfort-17squares-point-checker",), PRODUCER),
    ),
    (
        "anabologyco's checker",
        _id(r"anabologyco"),
        runs(("V-anabologyco-n17-checker",), None),
    ),
    # First-party programs deciding another's certificate, sharing none of its code.
    (
        "the first-party R012 decision, which imports nothing from the source",
        _in_replay(r"replay_guzhou_r012_first_party"),
        runs(("V-sqpack-fractional-interval",), INDEPENDENT),
    ),
    (
        "Mira's 4.613 certificate by this repository's interval branch and bound",
        _and(_in_replay(r"replay_mira_4613_first_party"), _in_replay(r"--interval")),
        runs(("V-sqpack-fractional-interval",), INDEPENDENT),
    ),
    (
        "Mira's 4.613 certificate by this repository's exact sweep",
        _in_replay(r"replay_mira_4613_first_party"),
        runs(("V-sqpack-fractional-exact",), INDEPENDENT),
    ),
    (
        "the native parent-core interval coverage",
        _in_replay(
            r"verify_kleddamag_n11_native|verify_n11_parent_core_native|verify_evand_angle_net_native"
        ),
        runs(("V-sqpack-parent-core-native",), INDEPENDENT),
    ),
    (
        "the promotion's exact test and the independent Fraction checker",
        _in_replay(r"(?:upper_bound_packets|catalogue_upper_bounds) check --replay"),
        runs(("V-upper-bound-promotion", "V-check-rational-witness-independent"), INDEPENDENT),
    ),
    (
        "the decimal interval decision of a printed pose",
        _in_replay(r"upper_bound_intervals"),
        runs(("V-upper-bound-intervals",), INDEPENDENT),
    ),
    (
        "the independent rational checker",
        _in_replay(r"check_rational_witness_independent"),
        runs(("V-check-rational-witness-independent",), INDEPENDENT),
    ),
    (
        "a published construction decided by sqpack.verify",
        _in_replay(r"\.verify_exact\b|packing-witness"),
        runs(("V-sqpack-verify",), INDEPENDENT),
    ),
    (
        "Kingbird's figure read and checked",
        _in_replay(r"verify_svg"),
        runs(("V-kingbird29-verify-svg",), INDEPENDENT),
    ),
    (
        "Bentz's published construction by the cell certifier",
        _in_replay(r"bentz(?:46|13)\.verify_cover"),
        runs(("V-sqpack-cover",), INDEPENDENT),
    ),
    (
        "the green17 interval audit, sharing only the point data",
        _in_replay(r"green17\.interval_audit"),
        runs(("V-green17-interval-audit",), INDEPENDENT),
    ),
    (
        "Burns's atoms rebuilt and decided by this repository's exact sweep",
        _in_replay(r"--burns-control"),
        runs(("V-sqpack-fractional-exact",), INDEPENDENT),
    ),
    (
        "the clean-room n = 12 verifier",
        _in_replay(r"replay_independent\.py"),
        runs(("V-n12-independent-verifier",), INDEPENDENT),
    ),
    (
        "the n = 17 instrument's two accumulation paths",
        _in_replay(r"n17_weighted_certificate_successor"),
        runs(("V-n17-weighted-instrument",), INDEPENDENT),
    ),
    (
        "the independent five-dot union",
        _in_replay(r"independent_union"),
        runs(("V-five-dot-independent-union",), INDEPENDENT),
    ),
    (
        "the source-distinct local-theorem checker",
        _in_replay(r"review_trump_local_theorem"),
        runs(("V-review-trump-local-theorem",), INDEPENDENT),
    ),
    (
        "the n = 11 component checkers, sharing this repository's kernels with the source",
        _in_replay(r"check_n11_final_composition"),
        runs(("V-n11-optimality-checkers", "V-check-n11-final-composition"), SHARED),
    ),
    # Second decisions of this project's own certificates that reuse its loader.
    (
        "the interval decision of a weighted certificate",
        _in_replay(r"decide_certificate --quick|test_fractional_interval"),
        runs(("V-sqpack-fractional-interval",), SHARED),
    ),
    (
        "the interval decision of a threshold certificate",
        _in_replay(r"(?:n11_threshold_certificate|decide_threshold_certificate) --quick"),
        runs(("V-sqpack-threshold-interval",), SHARED),
    ),
    # This project's own results, replayed by the code that produced them.
    (
        "the dilation corollary",
        _in_replay(r"dilation_corollary"),
        runs(("V-dilation-corollary",), PRODUCER),
    ),
    (
        "a threshold certificate by its exact sweep",
        _in_replay(r"n11_threshold_certificate|decide_threshold_certificate"),
        runs(("V-sqpack-threshold-exact",), PRODUCER),
    ),
    (
        "a weighted certificate by its exact sweep",
        _in_replay(r"_fractional_certificate|decide_certificate"),
        runs(("V-sqpack-fractional-exact",), PRODUCER),
    ),
    (
        "the elementary bounds",
        _in_replay(r"check_basic_bounds"),
        runs(("V-check-basic-bounds",), PRODUCER),
    ),
    (
        "the small-n optimal moduli",
        _in_replay(r"optimal_moduli"),
        runs(("V-optimal-moduli",), PRODUCER),
    ),
    (
        "this project's own cover, by the cell certifier",
        _in_replay(r"green17\.verify_cover|stromquist\.repaired_cover"),
        runs(("V-sqpack-cover",), PRODUCER),
    ),
    (
        "the translation-escape screen",
        _in_replay(r"screen_translation_escape"),
        runs(("V-screen-translation-escape",), PRODUCER),
    ),
    (
        "the n = 5 rigidity assessment",
        _in_replay(r"assess_n5_rigidity"),
        runs(("V-assess-n5-rigidity",), PRODUCER),
    ),
    (
        "the n = 40 rigidity assessment",
        _in_replay(r"assess_n40_rigidity"),
        runs(("V-assess-n40-rigidity",), PRODUCER),
    ),
    (
        "the frontier rigidity assessment",
        _in_replay(r"assess_frontier_rigidity"),
        runs(("V-assess-frontier-rigidity",), None),
    ),
    (
        "Trump's tangent cones",
        _in_replay(r"tangent_cones"),
        runs(("V-trump11-tangent-cones",), PRODUCER),
    ),
    (
        "Trump's isolation radius",
        _in_replay(r"trump11\.isolation_radius"),
        runs(("V-trump11-isolation-radius",), PRODUCER),
    ),
    (
        "the rung-0 tree reader",
        _in_replay(r"fixed_angle_tree_check"),
        runs(("V-trump11-fixed-angle-tree-check",), None),
    ),
    (
        "the owner-footprint cover replay",
        _in_replay(r"replay_owner_footprint_cover"),
        runs(("V-replay-owner-footprint-cover",), PRODUCER),
    ),
    (
        "the wall-owner footprints",
        _in_replay(r"wall_owner_footprints"),
        runs(("V-wall-owner-footprints",), PRODUCER),
    ),
    (
        "the wall-owner containment",
        _in_replay(r"wall_owner_containment"),
        runs(("V-wall-owner-containment",), PRODUCER),
    ),
)

#: For an entry that records a source's own run, or a derivation from one: the checker
#: its source is known to verify with, by source key.
SOURCE_RULES: tuple[Rule, ...] = (
    (
        "the independent Valid7 checker, by a third party",
        _source(r"^\[wand125 valid7"),
        runs(("V-wand125-valid7-checker", "V-audit-valid7-independent"), INDEPENDENT),
    ),
    (
        "Tokoharu's verify.cpp, which wand125's rectangle certificates ship unchanged",
        _source(r"^\[(?:wand125 rectangle bounds|Tokoharu density)"),
        runs(("V-tokoharu-verify-cpp",), PRODUCER),
    ),
    (
        "wand125's point certificates, checked by its adapter and this repository's verifier",
        _source(r"^\[wand125 point bounds 2026\]"),
        runs(("V-wand125-check-with-sqpack", "V-sqpack-fractional-exact"), PRODUCER),
    ),
    (
        "Daniel's s12 verify and the source's indep_check.cpp",
        _source(r"^\[squarepacker s12"),
        runs(("V-evand-angle-net-verify", "V-squarepacker-indep-check-cpp"), PRODUCER),
    ),
    ("wand125's tools", _source(r"^\[wand125 tools"), runs(("V-wand125-tools",), None)),
    (
        "Wang and Li's verify.py and Kleddamag's sweep",
        _source(r"^\[Wang Li n11"),
        runs(("V-wang-li-n11-verify", "V-kleddamag-n11-verify"), PRODUCER),
    ),
    (
        "Kleddamag's n = 11 verify.py",
        _source(r"^\[Kleddamag n11"),
        runs(("V-kleddamag-n11-verify",), PRODUCER),
    ),
    (
        "Kleddamag's n = 17 verify.py",
        _source(r"^\[Kleddamag n17"),
        runs(("V-kleddamag-n17-verify",), PRODUCER),
    ),
    (
        "Guzhou0806's R052 verify.py",
        _source(r"^\[Guzhou0806 n17 R052\]"),
        runs(("V-guzhou-r052-verify-py",), PRODUCER),
    ),
    (
        "Guzhou0806's paired launcher",
        _source(r"^\[Guzhou0806 n17 R06"),
        runs(("V-guzhou-n17-verify-cpp", "V-kleddamag-n17-verify"), PRODUCER),
    ),
    (
        "the publisher's n = 11 optimality driver",
        _source(r"^\[Ahmed"),
        runs(("V-queuingtheory-n11-verify",), PRODUCER),
    ),
    (
        "Schadt's check.py",
        _and(_source(r"^\[Schadt n=29"), lambda entry: entry.get("assurance") == "reported"),
        runs(("V-schadt-n29-check-py",), PRODUCER),
    ),
)

#: The external programs a source's own record names, matched in its limitations and its
#: review note. Each name is specific to one registry entry.
NAMED_PROGRAMS: tuple[tuple[str, str], ...] = (
    (r"a75140df", "V-tokoharu-verify-cpp"),
    (r"mixed_rotated_verify\.cpp", "V-wand125-mixed-rotated-verify-cpp"),
    (r"verify_mixed_full_proof", "V-wand125-verify-mixed-full-proof-py"),
    (r"unified_linear_verify", "V-wand125-unified-linear-verify-cpp"),
    (r"verify_portable", "V-wand125-verify-portable-py"),
    (r"\bzm_mixed\b", "V-evand-zm-mixed-py"),
    (r"\bzmx2\b", "V-evand-zmx2"),
    (r"zeromargin\.py", "V-evand-zeromargin-py"),
    (r"\bzmcheck\b", "V-evand-zmcheck"),
    (r"qx2_zm", "V-evand-qx2-zm-py"),
    (r"Rust verifier", "V-evand-angle-net-verify"),
    (r"exact Py\w* re-?check|xcheck", "V-evand-xcheck-py"),
    (r"Lean proves|Bentz\.lean", "V-evand-lean"),
)


def named_programs(entry: Entry) -> tuple[str, ...]:
    """The external programs a source's record names, in `NAMED_PROGRAMS` order."""
    # Another entry's id names that entry's programs, not this one's.
    text = re.sub(r"\bE-[a-z0-9-]+", "", _text(entry, "limitations", "external_review"))
    return tuple(verifier for pattern, verifier in NAMED_PROGRAMS if re.search(pattern, text))


def runs_code(entry: Entry) -> bool:
    """Whether the schema asks the entry for `verifiers`: its method runs code, as
    performed or as reported, or it names a replay."""
    method = entry.get("method") or entry.get("reported_method")
    return method in CODE_METHODS or bool(entry.get("replay"))


def classify(entry: Entry) -> Classification | None:  # noqa: PLR0911 -- one return per tier of the table
    """The programs behind one entry and the relation they read as, or nothing where a
    person has to decide."""
    eid = str(entry.get("id"))
    if eid in DECISIONS:
        return DECISIONS[eid][0]
    if entry.get("replay"):
        for name, test, result in REPLAY_RULES:
            if test(entry):
                return runs(result.verifiers, result.relation, f"replay: {name}")
        return None
    for name, test, result in SOURCE_RULES:
        if test(entry):
            return runs(result.verifiers, result.relation, f"source: {name}")
    if not runs_code(entry):
        return runs((), None, "no program: a proof or a source that states no method")
    named = named_programs(entry)
    if named and entry.get("performed_by") == "source-author":
        return runs(named, PRODUCER, "source: the programs its record names")
    if entry.get("replay_status") == "public-certificate-missing":
        return runs((), None, "no program held: the source publishes no checker")
    return None


def compatible(expected: str | None, entry: Entry) -> bool:
    """Whether a recorded relation agrees with what the entry's programs read as. Nothing
    expected, or nothing run here, agrees with any value."""
    recorded = entry.get("relationship_to_generator")
    if expected is None:
        return True
    if recorded == NOT_APPLICABLE and not entry.get("replay"):
        return True
    if recorded == NOT_APPLICABLE and expected == NOT_APPLICABLE:
        return True
    if recorded in RANK and expected in RANK:
        return RANK[recorded] == RANK[expected]
    return False


@dataclass
class Outcome:
    written: list[tuple[str, Classification]] = field(default_factory=list)
    kept: list[str] = field(default_factory=list)
    unclassified: list[str] = field(default_factory=list)
    differs: list[tuple[str, Classification]] = field(default_factory=list)
    fixed: list[tuple[str, Fix]] = field(default_factory=list)
    questions: list[tuple[str, str]] = field(default_factory=list)
    performers: list[tuple[str, str]] = field(default_factory=list)


def _blocks(lines: Sequence[str]) -> dict[str, tuple[int, int]]:
    starts = [
        (match.group(1), index)
        for index, line in enumerate(lines)
        if (match := re.match(r"^  - id: (E-[a-z0-9-]+)\s*$", line))
    ]
    return {
        eid: (start, starts[position + 1][1] if position + 1 < len(starts) else len(lines))
        for position, (eid, start) in enumerate(starts)
    }


def _one_line(lines: Sequence[str], start: int, end: int, prefix: str) -> int | None:
    found = [index for index in range(start, end) if lines[index].startswith(prefix)]
    return found[0] if len(found) == 1 else None


def backfill(text: str, entries: Sequence[Entry]) -> tuple[str, Outcome]:
    """Fill `verifiers`, apply the clear fixes and audit every entry; return the new text
    and what happened to each entry."""
    outcome = Outcome()
    lines = text.split("\n")
    blocks = _blocks(lines)
    edits: dict[int, tuple[int, list[str]]] = {}
    for entry in entries:
        eid = str(entry["id"])
        start, end = blocks[eid]
        recorded = entry.get("relationship_to_generator")
        fix = FIXES.get(eid)
        if fix is not None and recorded == fix.old:
            anchor = _one_line(lines, start, end, "    relationship_to_generator:")
            if anchor is not None:
                replacement = [f"    relationship_to_generator: {fix.new}"]
                if fix.shared:
                    quoted = ", ".join(
                        json.dumps(part, ensure_ascii=False) for part in fix.shared
                    )
                    replacement.append(f"    shared_components: [{quoted}]")
                edits[anchor] = (1, replacement)
                outcome.fixed.append((eid, fix))
                recorded = fix.new
        expected_performers = PERFORMERS.get(str(entry.get("origin")))
        if expected_performers and entry.get("performed_by") not in expected_performers:
            outcome.performers.append(
                (
                    eid,
                    f"origin {entry.get('origin')}, performed_by {entry.get('performed_by')}",
                )
            )
        result = classify(entry)
        if result is None:
            if runs_code(entry) and "verifiers" not in entry:
                outcome.unclassified.append(eid)
            continue
        if result.relation is not None and not compatible(
            result.relation, {**entry, "relationship_to_generator": recorded}
        ):
            outcome.questions.append(
                (
                    eid,
                    (
                        f"its replay or record runs {', '.join(result.verifiers)} "
                        f"({result.rule}), which reads as {result.relation}; "
                        f"the record says {recorded}"
                    ),
                )
            )
        if "verifiers" in entry:
            outcome.kept.append(eid)
            if set(entry.get("verifiers") or ()) != set(result.verifiers):
                outcome.differs.append((eid, result))
            continue
        if not runs_code(entry) and not result.verifiers:
            continue
        anchor = _one_line(lines, start, end, "    replay_status:")
        if anchor is None:
            outcome.unclassified.append(eid)
            continue
        edits[anchor] = (0, [lines[anchor], f"    verifiers: [{', '.join(result.verifiers)}]"])
        outcome.written.append((eid, result))
    for index in sorted(edits, reverse=True):
        _, replacement = edits[index]
        lines[index : index + 1] = replacement
    return "\n".join(lines), outcome


def report(outcome: Outcome, entries: Sequence[Entry], updated: str) -> list[str]:
    """What the run did, then the register's counts and the questions it leaves open."""
    final = safe_load(updated)["evidence"]
    out = [
        (
            f"{len(entries)} evidence entries: wrote verifiers into {len(outcome.written)}, "
            f"{len(outcome.kept)} already named theirs, fixed {len(outcome.fixed)} relations; "
            f"{len(outcome.unclassified)} could not be classified"
        )
    ]
    relations = Counter(str(entry.get("relationship_to_generator")) for entry in final)
    out.append(
        "relationship_to_generator: "
        + ", ".join(f"{k} {v}" for k, v in sorted(relations.items()))
    )
    named = [entry for entry in final if "verifiers" in entry]
    out.append(
        f"verifiers named on {len(named)} entries, empty on "
        f"{sum(1 for entry in named if not entry['verifiers'])}; "
        f"{len(final) - len(named)} run no code and carry none"
    )
    usage = Counter(v for entry in final for v in entry.get("verifiers") or [])
    registry = load()
    out.append("entries per verifier:")
    out.extend(
        f"  {verifier_id} ({registry[verifier_id].provenance}, {registry[verifier_id].role}): "
        f"{usage.get(verifier_id, 0)}"
        for verifier_id in registry
    )
    out.extend(
        f"  {v}: {n} (NOT IN THE REGISTRY)"
        for v, n in sorted(usage.items())
        if v not in registry
    )
    if outcome.fixed:
        out.append("fixed, each a clear case:")
        out.extend(
            f"  {eid}: {fix.old} -> {fix.new}; {fix.evidence}" for eid, fix in outcome.fixed
        )
    if outcome.questions:
        out.append("relations that look wrong, left for a human decision:")
        out.extend(f"  {eid}: {why}" for eid, why in outcome.questions)
    if outcome.performers:
        out.append("performed_by values that disagree with the origin:")
        out.extend(f"  {eid}: {why}" for eid, why in outcome.performers)
    else:
        out.append("performed_by: every value agrees with its entry's origin")
    if outcome.differs:
        out.append("recorded verifiers that differ from this table (kept as recorded):")
        out.extend(
            f"  {eid}: the table says {list(result.verifiers)}"
            for eid, result in outcome.differs
        )
    decided = [eid for eid in DECISIONS if any(entry["id"] == eid for entry in final)]
    if decided:
        out.append("programs named by a recorded decision rather than a signature:")
        out.extend(f"  {eid}: {DECISIONS[eid][1]}" for eid in decided)
    if outcome.unclassified:
        out.append("could not classify, a human decision is needed:")
        out.extend(f"  {eid}" for eid in outcome.unclassified)
    return out


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=EVIDENCE)
    parser.add_argument(
        "--dry-run", action="store_true", help="classify and report, write nothing"
    )
    options = parser.parse_args(argv)
    text = options.evidence.read_text(encoding="utf-8")
    entries = safe_load(text)["evidence"]
    updated, outcome = backfill(text, entries)
    if not options.dry_run and updated != text:
        options.evidence.write_text(updated, encoding="utf-8")
    print("\n".join(report(outcome, entries, updated)))
    return 1 if outcome.unclassified else 0


if __name__ == "__main__":
    raise SystemExit(main())
