"""Authenticate enforced quick-shard execution and report its explicit omissions.

The canonical suites exclude the existing frontend-owned files, slow and exhaustive
cases. Optional omissions are the exact 47 observed in full run 38565361504, artifact
11897004148; none is counted as executed. A changed or required module cannot reuse
an omission. This tool compares fresh collection with the actual JUnit receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from devtools import run_negative_controls, suite_files
from sqpack.cli import validate
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REQUIRED_MODULES = frozenset(
    "packing/tests/" + name
    for name in (
        "test_atlas_orientation.py",
        "test_bound_citations.py",
        "test_check_published_site.py",
        "test_overview.py",
        "test_overview_sections.py",
        "test_regularized_drawings.py",
        "test_replay_bc303_t1_witness.py",
        "test_results_register.py",
        "test_site_forwarders.py",
        "test_verifier_registry.py",
        "test_enforced_quick_workflow.py",
    )
)
# Observed omissions, not passing evidence. New omissions must fail for review.
KNOWN_OMISSIONS = frozenset(
    [
        "test_poster::test_ffmpeg_returns_the_frame_asked_for",
        (
            "tests.test_gate_budgets::test_the_live_pending_tiers_pass_until_their_da"
            "tes_and_are_named_after_them"
        ),
        "tests.test_n17_bb_native::test_a_summary_equals_the_python_tinylp_path",
        "tests.test_n17_bb_native::test_certificate_and_taylor_modes_use_the_python_fallbacks",
        (
            "tests.test_n17_bb_native::test_differential_replay_is_bitwise_for_all_fo"
            "ur_call_types"
        ),
        "tests.test_n17_bb_native::test_f7_control_is_not_certified",
        "tests.test_n17_bb_native::test_highs_is_a_distinct_numerical_baseline",
        "tests.test_n17_bb_native_edges::test_empty_rows_admit_supported_box_limits[1]",
        "tests.test_n17_bb_native_edges::test_empty_rows_admit_supported_box_limits[7]",
        (
            "tests.test_n17_bb_native_edges::test_inverted_bounds_report_infeasible_w"
            "ithout_panicking"
        ),
        "tests.test_n17_bb_native_edges::test_pair_core_rejects_unsupported_merging",
        "tests.test_n17_bb_native_edges::test_session_call_order_is_enforced",
        (
            "tests.test_n17_bb_native_edges::test_session_rejects_invalid_dimensions["
            "arguments0-expected 1..7 boxes]"
        ),
        (
            "tests.test_n17_bb_native_edges::test_session_rejects_invalid_dimensions["
            "arguments1-expected 1..7 boxes]"
        ),
        (
            "tests.test_n17_bb_native_edges::test_session_rejects_invalid_dimensions["
            "arguments2-<=64 rows]"
        ),
        (
            "tests.test_n17_bb_native_edges::test_session_rejects_invalid_dimensions["
            "arguments3-invalid row columns]"
        ),
        (
            "tests.test_n17_bb_native_edges::test_session_rejects_invalid_dimensions["
            "arguments4-matching row dimensions]"
        ),
        "tests.test_n17_bb_native_edges::test_tiny_lp_preserves_negative_zero",
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[dark-1280-n11-optimality-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[dark-1280-n11-threshold-bound-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[dark-390-n11-optimality-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[dark-390-n11-threshold-bound-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[light-1280-n11-optimality-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[light-1280-n11-threshold-bound-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[light-390-n11-optimality-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_front_has_early_font_dis"
            "covery_and_stable_first_paint[light-390-n11-threshold-bound-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_math_is_visible_without_"
            "javascript[n11-optimality-review]"
        ),
        (
            "tests.test_paper_publication::test_linked_paper_math_is_visible_without_"
            "javascript[n11-threshold-bound-review]"
        ),
        (
            "tests.test_paper_terms::test_every_term_is_defined_once_before_its_first"
            "_use[n11-lower-bounds-explainer]"
        ),
        (
            "tests.test_pdf_math_browser::test_final_math_guard_distinguishes_hidden_"
            "alternatives_and_render_errors"
        ),
        "tests.test_pdf_math_browser::test_production_pdf_accepts_typeset_math",
        (
            "tests.test_pdf_math_browser::test_production_pdf_preserves_readable_nati"
            "ve_mathml_fallback[error]"
        ),
        (
            "tests.test_pdf_math_browser::test_production_pdf_preserves_readable_nati"
            "ve_mathml_fallback[timeout]"
        ),
        (
            "tests.test_pdf_math_browser::test_production_pdf_refuses_raw_tex_after_f"
            "ont_failure[error]"
        ),
        (
            "tests.test_pdf_math_browser::test_production_pdf_refuses_raw_tex_after_f"
            "ont_failure[timeout]"
        ),
        "tests.test_pdf_math_browser::test_the_complete_atlas_and_caption_fit_one_letter_page",
        "tests.test_process_memory::test_darwin_current_memory_agrees_with_external_ps",
        (
            "tests.test_render_n11_optimality_review::test_a_print_can_ask_for_every_"
            "formula_at_once"
        ),
        (
            "tests.test_render_n11_optimality_review::test_diagram_labels_keep_public"
            "ation_sizes_through_viewbox_scale"
        ),
        (
            "tests.test_render_n11_optimality_review::test_formulas_are_drawn_as_thei"
            "r_text_is_on_macos_and_linearly_elsewhere"
        ),
        (
            "tests.test_render_n11_optimality_review::test_pdf_refuses_a_math_host_wi"
            "thout_rendered_katex"
        ),
        "tests.test_render_n11_optimality_review::test_radical_svg_has_print_geometry",
        (
            "tests.test_render_packing_methods::test_printed_paper_has_its_own_title_"
            "dates_and_absolute_links"
        ),
        "tests.test_render_packing_methods::test_unrendered_math_never_publishes_a_pdf",
        (
            "tests.test_windows_supervision::test_native_venv_worker_and_grandchild_a"
            "re_owned_and_reaped[memory]"
        ),
        (
            "tests.test_windows_supervision::test_native_venv_worker_and_grandchild_a"
            "re_owned_and_reaped[normal]"
        ),
        (
            "tests.test_windows_supervision::test_native_venv_worker_and_grandchild_a"
            "re_owned_and_reaped[timeout]"
        ),
    ]
)

NEGATIVE_CONTROL_NAMES = frozenset(
    [
        "defect log - open defect with no bead",
        "defect log - soundness defect with no direction",
        "defect log - narrative link pointing nowhere",
        "defect log - recurrence naming a defect that does not exist",
        "defect log - fixed status contradicting an unresolved fix",
        "defect log - count disagreeing with the list",
        "frontier - non-verified evidence promoted into the verified lane",
        "frontier - attributed evidence dropping its source",
        "frontier - novelty claimed without a dated source review",
        "full-cell - generated control rejects a geometry channel",
    ]
)


class CoverageError(ValueError):
    """The source identity or actual execution does not cover the declared scope."""


def git(*arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def changed_modules(baseline: str) -> set[str]:
    return {
        path
        for path in git(
            "diff",
            "--name-only",
            baseline,
            "HEAD",
            "--",
            "packing/tests",
            "packages/workbench/tests",
        ).splitlines()
        if path.endswith(".py")
        and Path(path).name.startswith("test_")
        and (REPO / path).is_file()
    }


def modules_for_shard(modules: set[str], suite: str) -> list[str]:
    costs = suite_files.load_costs()
    excluded = {
        "packing/" + name
        for name in (validate.BROWSER_FLOOR_LIVENESS_TESTS, *validate.SITE_LAYOUT_TESTS)
    }
    return sorted(
        path
        for path in modules - excluded
        if suite_files.shard_of(path, costs) == "abcd".index(suite) + 1
    )


def node_key(node: str) -> str:
    path, *parts = node.split("::")
    module = path.removesuffix(".py").removeprefix("../").replace("/", ".")
    return ".".join((module, *parts[:-1])) + "::" + parts[-1]


def collect_nodes(modules: Sequence[str]) -> set[str]:
    if not modules:
        return set()
    paths = [os.path.relpath(REPO / path, ROOT) for path in modules]
    environment = dict(os.environ)
    environment.pop("PACKING_VALIDATION_ARTIFACT_DIR", None)
    result = subprocess.run(
        (
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
            "-m",
            validate.QUICK_TESTS,
            *paths,
        ),
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise CoverageError(f"required-case collection failed: {result.stdout}{result.stderr}")
    nodes = {
        node_key(line)
        for line in result.stdout.splitlines()
        if any(line.startswith(path + "::") for path in paths)
    }
    for path in paths:
        prefix = path.removesuffix(".py").removeprefix("../").replace("/", ".")
        if not any(node.startswith((prefix + "::", prefix + ".")) for node in nodes):
            raise CoverageError(f"required module collected no quick cases: {path}")
    return nodes


def junit_nodes(documents: Sequence[str]) -> dict[str, str]:
    nodes: dict[str, str] = {}
    for document in documents:
        for case in ET.fromstring(document).iter("testcase"):
            key = case.attrib["classname"] + "::" + case.attrib["name"]
            if key in nodes:
                raise CoverageError(f"repeated executed case: {key}")
            nodes[key] = (
                "skipped"
                if case.find("skipped") is not None
                else "failed"
                if case.find("failure") is not None or case.find("error") is not None
                else "passed"
            )
    if not nodes:
        raise CoverageError("the shard has no actual JUnit cases")
    return nodes


def execution_problems(
    expected: set[str], observed: Mapping[str, str], protected_modules: set[str]
) -> list[str]:
    problems = [
        f"required case absent or not passed: {node}"
        for node in sorted(expected)
        if observed.get(node) != "passed"
    ]
    prefixes = {
        path.removeprefix("packing/").removesuffix(".py").replace("/", ".")
        for path in protected_modules
    }
    for node, status in observed.items():
        if status == "failed":
            problems.append(f"failed case: {node}")
        elif status == "skipped":
            protected = any(
                node.startswith((prefix + "::", prefix + ".")) for prefix in prefixes
            )
            if protected or node not in KNOWN_OMISSIONS:
                problems.append(f"unreviewed or changed-module omission: {node}")
    return problems


def verify_shard(artifacts: Path, suite: str, sha: str, baseline: str) -> dict[str, Any]:
    if (
        git("rev-parse", "HEAD") != sha
        or (artifacts / "source-sha.txt").read_text().strip() != sha
    ):
        raise CoverageError("source SHA differs from the workflow's actual checkout")
    runs = [json.loads(path.read_text()) for path in artifacts.glob("run-*.json")]
    if len(runs) != 1 or runs[0]["commit"] != sha or runs[0]["git_status"]:
        raise CoverageError(
            "validation receipt is absent, mixed, or names a dirty/different tree"
        )
    if runs[0]["selected_steps"] != [f"fast behavioral tests, shard {suite.upper()}"]:
        raise CoverageError("validation did not select exactly the canonical shard")
    baseline = git("rev-parse", "--verify", "--end-of-options", baseline + "^{commit}")
    protected = set(REQUIRED_MODULES) | changed_modules(baseline)
    modules = modules_for_shard(protected, suite)
    expected = collect_nodes(modules)
    observed = junit_nodes([path.read_text() for path in artifacts.glob("*.junit.xml")])
    problems = execution_problems(expected, observed, protected)
    if problems:
        raise CoverageError("\n".join(problems))
    return {
        "source_sha": sha,
        "source_tree": git("rev-parse", "HEAD^{tree}"),
        "scope_baseline": git("rev-parse", baseline),
        "suite": suite,
        "status": "success",
        "required_modules": modules,
        "required_nodeids": sorted(expected),
        "passed_cases": sum(status == "passed" for status in observed.values()),
        "omitted_cases": sorted(
            node for node, status in observed.items() if status == "skipped"
        ),
        "frontend_exclusions": [
            validate.BROWSER_FLOOR_LIVENESS_TESTS,
            *validate.SITE_LAYOUT_TESTS,
        ],
        "scope": "four canonical quick suites; frontend and deferred tiers are separate",
    }


def aggregate_problems(receipts: Sequence[Mapping[str, Any]], sha: str) -> list[str]:
    suites = [row.get("suite") for row in receipts]
    if len(receipts) != 5 or set(suites) != {*"abcd", "negative-controls"}:
        return ["requires four quick-shard receipts and the affected negative-control receipt"]
    problems = [
        f"suite {row.get('suite')}: unsuccessful or different source"
        for row in receipts
        if row.get("status") != "success"
        or row.get("source_sha") != sha
        or not isinstance(row.get("passed_cases"), int)
        or row["passed_cases"] < 1
    ]

    control = next(row for row in receipts if row.get("suite") == "negative-controls")
    if (
        control.get("passed_cases") != 10
        or set(control.get("selected_controls", [])) != NEGATIVE_CONTROL_NAMES
    ):
        problems.append("the control receipt must prove the exact ten schema mutations")
    return problems


def select_negative_controls(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    controls = [row for row in document["controls"] if row["name"] in NEGATIVE_CONTROL_NAMES]
    if len(controls) != 10 or {row["name"] for row in controls} != NEGATIVE_CONTROL_NAMES:
        raise CoverageError(
            "registry must contain each of the ten affected schema controls once"
        )
    return controls


def negative_control_problems(events: Sequence[Mapping[str, Any]]) -> list[str]:
    started = [event for event in events if event.get("event") == "run_started"]
    finished = [event for event in events if event.get("event") == "control_finished"]
    ended = [event for event in events if event.get("event") == "run_finished"]
    if (
        len(started) != 1
        or set(started[0].get("selected_controls", [])) != NEGATIVE_CONTROL_NAMES
    ):
        return ["negative-control journal does not declare the exact ten controls"]
    if len(finished) != 10 or {row.get("name") for row in finished} != NEGATIVE_CONTROL_NAMES:
        return ["not every selected negative control completed exactly once"]
    if any(row.get("status") != "passed" for row in finished):
        return ["a selected negative control failed or was interrupted"]
    if len(ended) != 1 or ended[0].get("status") != "passed" or ended[0].get("completed") != 10:
        return ["negative-control run did not finish successfully with ten controls"]
    return []


def verify_negative_controls(artifacts: Path, sha: str) -> dict[str, Any]:
    if (
        git("rev-parse", "HEAD") != sha
        or (artifacts / "source-sha.txt").read_text().strip() != sha
    ):
        raise CoverageError("negative controls must run at the actual workflow source SHA")
    controls = select_negative_controls(
        safe_load((ROOT / "devtools/controls.yaml").read_text())
    )
    selected = artifacts / "selected-controls.json"
    selected.write_text(json.dumps({"controls": controls}, indent=2) + "\n")
    journal = artifacts / "negative-controls.jsonl"
    status = run_negative_controls.main([str(selected), "-j", "2", "--timings", str(journal)])
    if status:
        raise CoverageError("the affected negative controls did not all fire")
    events = [json.loads(line) for line in journal.read_text().splitlines()]
    problems = negative_control_problems(events)
    if problems:
        raise CoverageError("\n".join(problems))
    return {
        "source_sha": sha,
        "source_tree": git("rev-parse", "HEAD^{tree}"),
        "suite": "negative-controls",
        "status": "success",
        "passed_cases": 10,
        "selected_controls": sorted(NEGATIVE_CONTROL_NAMES),
        "scope": "ten affected schema mutations only; other controls remain separate",
    }


def require_aggregate(receipts: Sequence[Mapping[str, Any]], sha: str) -> None:
    problems = aggregate_problems(receipts, sha)
    if problems:
        raise CoverageError("\n".join(problems))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--suite", choices=list("abcd"))
    parser.add_argument("--baseline-ref", default="origin/main")
    modes.add_argument("--aggregate", action="store_true")
    modes.add_argument("--negative-controls", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.aggregate:
            receipts = [
                json.loads(path.read_text()) for path in args.artifacts.glob("*/execution.json")
            ]
            require_aggregate(receipts, args.source_sha)
            print(f"four quick suites and ten schema controls succeeded at {args.source_sha}")
        elif args.negative_controls:
            receipt = verify_negative_controls(args.artifacts, args.source_sha)
            (args.artifacts / "execution.json").write_text(json.dumps(receipt, indent=2) + "\n")
            print("the ten selected schema mutations fired at the actual workflow source SHA")
        else:
            if args.suite is None:
                parser.error("--suite is required without --aggregate")
            baseline = args.baseline_ref or "origin/main"
            if set(baseline) == {"0"}:
                baseline = "origin/main"
            receipt = verify_shard(args.artifacts, args.suite, args.source_sha, baseline)
            (args.artifacts / "execution.json").write_text(json.dumps(receipt, indent=2) + "\n")
            print(
                f"suite {args.suite}: {receipt['passed_cases']} passed, "
                f"{len(receipt['omitted_cases'])} omitted; changed cases all executed"
            )
    except (CoverageError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
