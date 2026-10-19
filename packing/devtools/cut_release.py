#!/usr/bin/env python3
"""Prepare one component's patch or minor edition and its release-impact decision.

Site cuts regenerate claim documents and leave infographic and paper editions alone.
Infographic cuts redraw both posters and every PDF/PNG export at one shared version.
Paper cuts change only that paper's history and regenerate its HTML, Markdown and PDF.
Ordinary cuts run shared release/date contracts and the owning component's quick tests.
`--include-deep-tests` also runs slow and exhaustive tests in that component's files.
Neither selection replaces the full checkpoint required for final review.
Every cut records the complete delivered change in `release.RELEASE_IMPACTS`; the scope
explains the patch or minor choice. Internal work and changelog bookkeeping need no cut.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.6.0 \
        --component site --impact minor --scope "Add a substantial capability." --dry-run
    uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.5.1 \
        --component infographics --impact patch --scope "Refresh the displayed results."

`--date` is the planned first-publication day, written `October 13, 2026`; it defaults
 to today in UTC and is corrected if deployment lands on another day. The command
commits and publishes nothing. Keep the selected edition fixed through review, then
confirm deployment with `check_published_site`. A GitHub release is needed only for
assets whose public download addresses use it, such as the films.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shlex
import subprocess
import sys
import textwrap
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from strif import atomic_output_file

from devtools import release_pin
from sqpack import release
from sqpack.cli.validate import QUICK_TESTS

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
REVISION_LINE = re.compile(r'^PUBLICATION_REVISION = "([0-9a-f]{7,40})"$', re.MULTILINE)
IMPACTS_OPEN = "RELEASE_IMPACTS: tuple[ReleaseImpactDecision, ...] = ("
SCOPE_WIDTH = 76
COMMON_TESTS = (
    "tests/test_release.py",
    "tests/test_release_components.py",
    "tests/test_artifact_dates.py",
)
#: Generation ownership also determines the tests a cut runs (think-8iml). Scientific
#: assertions stay in their existing lanes; a cut's quick checks are iteration feedback.
COMPONENT_TESTS = {
    "site": ("tests/test_verify_claim.py", "tests/test_verify_threshold_claim.py"),
    "infographics": ("tests/test_known_best_composites.py",),
    "paper:n11-lower-bounds-explainer": (
        "tests/test_n11_lower_bounds_explainer.py",
        "tests/test_render_n11_lower_bounds_explainer_pdf.py",
        "tests/test_verify_claim.py",
        "tests/test_verify_threshold_claim.py",
    ),
    "paper:n11-optimality-review": ("tests/test_render_n11_optimality_review.py",),
    "paper:n11-threshold-bound-review": ("tests/test_render_n11_threshold_bound_review.py",),
    "paper:square-packing-methods-survey": ("tests/test_render_packing_methods.py",),
}
PAPER_MODULES = {
    "paper:n11-lower-bounds-explainer": "devtools.render_n11_lower_bounds_explainer",
    "paper:n11-optimality-review": "devtools.render_n11_optimality_review",
    "paper:n11-threshold-bound-review": "devtools.render_n11_threshold_bound_review",
    "paper:square-packing-methods-survey": "devtools.render_packing_methods",
}


def parsed(version: str) -> tuple[int, int, int]:
    """The semantic core shared by all public component histories."""
    return release.parsed_version(version)


def _current(source: str, history_name: str) -> str:
    """Read the selected history's head without executing source or trusting imports."""
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign) or not any(
            isinstance(target, ast.Name) and target.id == history_name
            for target in node.targets
        ):
            continue
        if isinstance(node.value, ast.Tuple) and node.value.elts:
            entry = node.value.elts[0]
            if isinstance(entry, ast.Call):
                for keyword in entry.keywords:
                    if keyword.arg == "version" and isinstance(keyword.value, ast.Constant):
                        value = keyword.value.value
                        if isinstance(value, str):
                            parsed(value)
                            return value
    raise ValueError(f"release.py has no literal head edition in {history_name}")


def _scope_literal(scope: str) -> str:
    pieces = textwrap.wrap(scope, SCOPE_WIDTH, break_long_words=False, break_on_hyphens=False)
    quoted = [
        json.dumps(piece + (" " if index < len(pieces) - 1 else ""), ensure_ascii=False)
        for index, piece in enumerate(pieces)
    ]
    if len(quoted) == 1 and len(quoted[0]) <= SCOPE_WIDTH - 8:
        return quoted[0]
    return "(\n" + "".join(f"            {piece}\n" for piece in quoted) + "        )"


def with_edition(
    source: str,
    *,
    version: str,
    first_published: str,
    scope: str,
    revision: str,
    component: str = "site",
    impact: release.ReleaseImpact = "patch",
) -> str:
    """Add one owning history entry and impact decision; leave other editions intact."""
    release.component_history(component)
    history_name = release.COMPONENT_HISTORY_NAMES[component]
    history_open = f"{history_name} = (\n"
    current = _current(source, history_name)
    if parsed(version) <= parsed(current):
        raise ValueError(f"{version} is not after the current edition, {current}")
    expected = release.successor_version(current, impact)
    if version != expected:
        raise ValueError(
            f"{component} {impact} impact requires successor {expected}, not {version}"
        )
    datetime.strptime(first_published, "%B %d, %Y")  # noqa: DTZ007
    if scope.strip() != scope or not scope.endswith(".") or "\n" in scope or scope == ".":
        raise ValueError("the scope is one trimmed sentence ending in a full stop")
    if re.fullmatch(r"[0-9a-f]{7,40}", revision) is None:
        raise ValueError(f"{revision!r} is not a commit")
    if (
        source.count(history_open) != 1
        or source.count(IMPACTS_OPEN) != 1
        or len(REVISION_LINE.findall(source)) != 1
    ):
        raise ValueError("release.py is not laid out as cut_release expects")
    literal = _scope_literal(scope)
    entry = (
        "    PublicationHistoryEntry(\n"
        f'        version="{version}",\n'
        f'        first_published="{first_published}",\n'
        f"        result_scope={literal},\n"
        "    ),\n"
    )
    decision = (
        "    ReleaseImpactDecision(\n"
        f'        component="{component}",\n'
        f'        previous_version="{current}",\n'
        f'        version="{version}",\n'
        f'        impact="{impact}",\n'
        f"        reason={literal},\n"
        "    ),\n"
    )
    bumped = source.replace(history_open, history_open + entry)
    if IMPACTS_OPEN + ")" in bumped:
        bumped = bumped.replace(IMPACTS_OPEN + ")", IMPACTS_OPEN + "\n" + decision + ")")
    else:
        bumped = bumped.replace(IMPACTS_OPEN + "\n", IMPACTS_OPEN + "\n" + decision)
    if component == "site":
        return REVISION_LINE.sub(f'PUBLICATION_REVISION = "{revision}"', bumped)
    return bumped


def _git(*arguments: str) -> str:
    done = subprocess.run(
        ("git", "-C", str(REPO), *arguments), capture_output=True, text=True, check=True
    )
    return done.stdout.strip()


def steps(
    version: str, component: str = "site", *, include_deep_tests: bool = False
) -> list[tuple[str, tuple[str, ...]]]:
    """Component-owned generation and checks; deeper tests require an explicit choice."""
    release.component_history(component)
    plan: list[tuple[str, tuple[str, ...]]]
    if component == "infographics":
        plan = [
            (
                "redraw both infographics and all their exports",
                ("devtools.build_known_best_atlas", "--update-composites"),
            ),
            (
                f"hold the complete infographic family to {version}",
                ("devtools.build_known_best_atlas", "--check-composites"),
            ),
        ]
    elif component == "site":
        plan = [("regenerate the claim documents", ("devtools.render_verifiable_claim",))]
    else:
        module = PAPER_MODULES[component]
        if component == "paper:n11-lower-bounds-explainer":
            plan = [
                ("regenerate this paper's HTML and Markdown", (module,)),
                ("regenerate this paper's PDF", (module + "_pdf", "--update")),
            ]
        else:
            plan = [("regenerate this paper's HTML, Markdown and PDF", (module, "--pdf"))]
    tests = [*COMMON_TESTS, *COMPONENT_TESTS[component]]
    if component in PAPER_MODULES:
        tests.append("tests/test_paper_structure.py")
    marker = () if include_deep_tests else ("-m", QUICK_TESTS)
    plan.append(
        ("run the tests that hold this component's edition", ("pytest", "-q", *tests, *marker))
    )
    return plan


def remaining(version: str, component: str = "site") -> str:
    history_name = release.COMPONENT_HISTORY_NAMES[component]
    artifacts = {
        "site": "the regenerated claim documents and the site's changed public outputs",
        "infographics": "both infographic SVGs, every PNG export and both PDFs together",
    }.get(component, "this paper's HTML, Markdown and PDF together")
    return textwrap.dedent(
        f"""\
        Left to do, none of it done here:
          1. Review the impact decision and diff, then commit release.py and {artifacts}.
             Keep {version} fixed through review. Other components keep their own editions.
          2. Obtain the full checkpoint for final review on matching source and base.
             Component checks, including --include-deep-tests, do not supply omitted checks.
          3. Merge, wait for the "Certificate page" workflow on main, then from packing/:
               python -m devtools.check_published_site --commit <merge commit>
             The {component} version {version} is complete when that passes.
          4. If the deployment's UTC date differs, correct {history_name}'s new date
             and record the deployment evidence beside its history.
        No tag or GitHub release is created here. A release is cut only to host generated
        assets needing a download address. Films stay on render_overview.FILM_RELEASE
        until re-cut; packages/workbench/README.md carries their publication runbook."""
    )


def prepared(
    version: str,
    first_published: str,
    scope: str,
    *,
    component: str = "site",
    impact: release.ReleaseImpact = "patch",
) -> tuple[str, str]:
    """Prepare the complete edit, refusing dirty input or a stale data pin before writes."""
    revision = _git("rev-parse", "--short=8", "HEAD")
    bumped = with_edition(
        release_pin.RELEASE.read_text(encoding="utf-8"),
        version=version,
        first_published=first_published,
        scope=scope,
        revision=revision,
        component=component,
        impact=impact,
    )
    dirty = _git("status", "--porcelain")
    if dirty:
        raise ValueError(f"the working tree is not clean:\n{dirty}")
    if release_pin.check(REPO, release_pin.RELEASE) != 0:
        raise ValueError("the pinned data revision is stale; re-pin and commit first")
    return revision, bumped


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="the new edition, as vMAJOR.MINOR.PATCH")
    parser.add_argument(
        "--component", choices=tuple(release.COMPONENT_HISTORY_NAMES), default="site"
    )
    parser.add_argument("--impact", choices=("patch", "minor"), required=True)
    parser.add_argument(
        "--scope", required=True, help="one sentence explaining the delivered change"
    )
    parser.add_argument("--date", help="the planned first-publication day: October 13, 2026")
    parser.add_argument("--dry-run", action="store_true", help="print the plan; change nothing")
    parser.add_argument(
        "--include-deep-tests",
        action="store_true",
        help=(
            "include the selected component's slow and exhaustive tests; "
            "full checkpoint stays separate"
        ),
    )
    arguments = parser.parse_args(argv)
    today = datetime.now(UTC)
    first_published = arguments.date or f"{today:%B} {today.day}, {today.year}"
    try:
        revision, bumped = prepared(
            arguments.version,
            first_published,
            arguments.scope,
            component=arguments.component,
            impact=arguments.impact,
        )
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    plan = steps(
        arguments.version, arguments.component, include_deep_tests=arguments.include_deep_tests
    )
    print(
        f"{arguments.component}: {release.component_version(arguments.component)} -> "
        f"{arguments.version}, first published {first_published}; {arguments.impact} impact"
    )
    print(
        f"  1. add the owning history entry and release-impact decision (revision {revision})"
    )
    for number, (what, command) in enumerate(plan, start=2):
        print(f"  {number}. {what}: python -m {shlex.join(command)}")
    if arguments.dry_run:
        print("dry run: nothing was changed")
        print(remaining(arguments.version, arguments.component))
        return 0
    with atomic_output_file(release_pin.RELEASE) as temporary:
        temporary.write_text(bumped, encoding="utf-8")
    for what, command in plan:
        print(f"+ {what}", flush=True)
        done = subprocess.run((sys.executable, "-m", *command), cwd=PACKING, check=False)
        if done.returncode != 0:
            print(
                f"FAIL: could not {what}. release.py is edited and completed outputs are "
                "in the tree; repair the failure and run the remaining commands above. "
                "Do not publish an incomplete family or choose another version during review.",
                file=sys.stderr,
            )
            return done.returncode
    print(remaining(arguments.version, arguments.component))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
