"""Name the successful pull-request run that already validated this exact tree, or nothing.

A push to `main` runs the complete post-merge surface, and on 2026-09-15 that was 53
minutes of the `validate` job alone, 830 s of it (at `--jobs 1`) the same `fast` steps
the pull request had just run. `development.md` measured how often those are the same
bytes: 53 of 55 merges to `main` carried a tree byte-identical to the pull-request head
that was merged. Equal tree ids mean equal bytes for every tracked file, the verifying
code and the workflow included, so a fast step that passed on that tree is not
re-evidenced by passing on it again.

The rule is a proof about the tree, not trust in a label:

* every pull-request run of `packing-validation.yml` uploads an artifact named
  `pull-request-tree-<tree id>`, where the id is `git rev-parse HEAD^{tree}` of the
  commit that run checked out -- GitHub's test merge, which is what its jobs validated;
* after a push, this looks up artifacts by the pushed commit's tree id and accepts a run
  only if it is a completed, successful `pull_request` run of this workflow in this
  repository, from a branch of this repository rather than a fork. Success is the run's
  conclusion, so every job in it passed, not just the one that uploaded the artifact;
* anything else -- no artifact, an expired one, a failed or cancelled run, an API error --
  names no run, and the complete surface runs as before. Every failure of this tool
  fails toward repeating work, never toward skipping it.

What the named run licenses is narrow, and `sqpack.cli.validate` applies it: only `fast`
steps are left out, and not the ones that read beyond the tree
(`Step.reads_beyond_tree`). Every deferred step still runs after the merge, so `OR-13`
is unchanged: the fast checks ran in CI on these bytes before the merge, and the slow
ones run on them after it.

Usage, from the post-merge `validate` job:

    uv run --frozen --all-extras --group dev python -m devtools.verified_merge_tree \\
        --sha "$GITHUB_SHA" --repository "$GITHUB_REPOSITORY" --github-output "$GITHUB_OUTPUT"
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
ARTIFACT_PREFIX: Final = "pull-request-tree-"
WORKFLOW_PATH: Final = ".github/workflows/packing-validation.yml"

type Api = Callable[[str], Any]


@dataclass(frozen=True)
class Verdict:
    """The run that validated the tree, if any, and why each candidate was or was not it."""

    tree: str
    run_id: int | None
    reasons: tuple[str, ...]


def artifact_name(tree: str) -> str:
    return f"{ARTIFACT_PREFIX}{tree}"


def tree_of(sha: str) -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "--verify", "--quiet", f"{sha}^{{tree}}"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    tree = completed.stdout.strip()
    if completed.returncode != 0 or not tree:
        raise ValueError(f"{sha!r} does not name a commit with a tree in this checkout")
    return tree


def refusal(run: Mapping[str, Any], *, repository: str) -> str | None:
    """Why this run does not prove its tree passed, or `None` when it does."""
    head = run.get("head_repository") or {}
    base = run.get("repository") or {}
    checks = (
        (run.get("event") == "pull_request", f"event is {run.get('event')!r}"),
        (run.get("path") == WORKFLOW_PATH, f"workflow is {run.get('path')!r}"),
        (run.get("status") == "completed", f"status is {run.get('status')!r}"),
        (run.get("conclusion") == "success", f"conclusion is {run.get('conclusion')!r}"),
        (base.get("full_name") == repository, f"repository is {base.get('full_name')!r}"),
        (
            head.get("full_name") == repository,
            f"head repository is {head.get('full_name')!r}, a fork's run is not accepted",
        ),
    )
    failed = [reason for passed, reason in checks if not passed]
    return "; ".join(failed) if failed else None


def verify(tree: str, *, repository: str, api: Api) -> Verdict:
    """Search the artifacts named for `tree` and return the newest run that proves it."""
    reasons: list[str] = []
    try:
        listing = api(
            f"repos/{repository}/actions/artifacts?name={artifact_name(tree)}&per_page=100"
        )
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return Verdict(tree, None, (f"artifact lookup failed: {error}",))
    artifacts = [
        artifact
        for artifact in listing.get("artifacts", [])
        if artifact.get("name") == artifact_name(tree)
    ]
    if not artifacts:
        return Verdict(tree, None, (f"no artifact named {artifact_name(tree)}",))
    ordered = sorted(
        artifacts, key=lambda artifact: int(artifact["workflow_run"]["id"]), reverse=True
    )
    for artifact in ordered:
        run_id = int(artifact["workflow_run"]["id"])
        if artifact.get("expired"):
            reasons.append(f"run {run_id}: its artifact has expired")
            continue
        try:
            run = api(f"repos/{repository}/actions/runs/{run_id}")
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            reasons.append(f"run {run_id}: lookup failed: {error}")
            continue
        refused = refusal(run, repository=repository)
        if refused is None:
            reasons.append(f"run {run_id}: a successful pull-request run of this tree")
            return Verdict(tree, run_id, tuple(reasons))
        reasons.append(f"run {run_id}: {refused}")
    return Verdict(tree, None, tuple(reasons))


def _gh_api(path: str) -> Any:
    completed = subprocess.run(
        ("gh", "api", path), capture_output=True, text=True, check=False, timeout=60
    )
    if completed.returncode != 0:
        raise OSError(
            completed.stderr.strip() or f"gh api {path} exited {completed.returncode}"
        )
    return json.loads(completed.stdout)


def main(argv: Sequence[str] | None = None, *, api: Api = _gh_api) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.verified_merge_tree",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.add_argument("--sha", required=True)
    _ = parser.add_argument("--repository", required=True, help="OWNER/NAME")
    _ = parser.add_argument(
        "--github-output",
        type=Path,
        default=None,
        help="append `run=<id>` here when a run is named, and `run=` when none is",
    )
    arguments = parser.parse_args(argv)
    try:
        tree = tree_of(str(arguments.sha))
    except ValueError as error:
        print(f"no verified pull-request run: {error}")
        verdict = None
    else:
        verdict = verify(tree, repository=str(arguments.repository), api=api)
        print(f"tree {tree} of {arguments.sha}:")
        for reason in verdict.reasons:
            print(f"  {reason}")
        if verdict.run_id is None:
            print("no verified pull-request run: the complete surface runs")
        else:
            print(f"verified by pull-request run {verdict.run_id}")
    if arguments.github_output is not None:
        named = "" if verdict is None or verdict.run_id is None else str(verdict.run_id)
        with Path(arguments.github_output).open("a", encoding="utf-8") as stream:
            _ = stream.write(f"run={named}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
