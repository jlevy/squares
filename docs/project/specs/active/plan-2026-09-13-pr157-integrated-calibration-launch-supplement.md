# PR157 Integrated Calibration Launch Supplement

Date: September 13, 2026. Status: draft for exact-head review under `think-99bz`.

The
[BC329 target-free three-profile run sheet](plan-2026-09-13-n11-bc329-three-profile-run-sheet.md)
defines the solved `n=2` calibration fixture, frozen tuple, host conditions, sequential
profiles, source-distinct reads, and retention procedure.
For an integrated PR157 run, replace that sheet’s **Execution Preconditions** block and
its PR156-only remote-identity refusal with the checks below.
Keep its other refusal conditions and literal `snapshot`, `read`, `join`, `retain`, and
`source-closure` commands.
The run sheet’s admission table records PR156 reviews.
For this supplement, reassess every required gate on one clean PR157 `EXECUTION_REV` and
record an accepted exact-head verdict before the coordinator.
Its PR156 **Remote identity** row is replaced by the PR157 identity guard below;
acceptance of an ancestor does not admit the integrated merge resolution.

This supplement does not admit a profile launch.
First commit and publish the reviewed PR156 merge on PR157, obtain independent review of
the resulting exact head and reader blob, and pass the integrated validation gates.
No full-shape calibration profile or BC329 scientific target is performed while
preparing or reviewing this supplement.

## Integrated Execution Identity

Run this block from the actual PR157 checkout before the run sheet’s **Fresh Roots and
Host Observations** block.
It replaces the PR156 checkout path, branch assertion, and `PR156_HEAD` equality check.
The local branch has a different name from GitHub’s PR157 head ref; check both names and
their shared commit.
A moving PR156 head also stops the launch until PR157 incorporates it.

```bash
set -euo pipefail

export REPOSITORY="$(git rev-parse --show-toplevel)"
export PACKING="$REPOSITORY/packing"
export UV_CACHE_DIR=/private/tmp/bc329-pr157-uv-cache
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=0
export LC_ALL=C
export TZ=UTC

test "$(git -C "$REPOSITORY" rev-parse --show-toplevel)" = "$REPOSITORY"
test "$(git -C "$REPOSITORY" branch --show-current)" = codex/pr157-reviewed-stack
if git -C "$REPOSITORY" rev-parse -q --verify MERGE_HEAD > /dev/null; then
  exit 1
fi
test -z "$(git -C "$REPOSITORY" status --porcelain=v1 --untracked-files=all)"
git -C "$REPOSITORY" diff --quiet
git -C "$REPOSITORY" diff --cached --quiet
test "$(uname -s)" = Darwin
test "$(uname -m)" = arm64
test ! -e "$PACKING/.gate-running"
command -v jq > /dev/null

UV_VERSION="$(uv --version | awk '{print $2}')"
case "$UV_VERSION" in
  ''|*[!0-9.]*) exit 1 ;;
esac
awk -v version="$UV_VERSION" 'BEGIN {
  split(version, part, ".");
  exit ! (part[1] > 0 || (part[1] == 0 && part[2] >= 12));
}'

mkdir -p "$UV_CACHE_DIR"
cd "$PACKING"
uv sync --frozen --all-extras --group dev
export PATH="$PACKING/.venv/bin:/Users/levy/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHON="$PACKING/.venv/bin/python3"
test "$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" = 3.14
test "$($PYTHON -c 'import sys; print(sys.prefix)')" = "$PACKING/.venv"

export EXECUTION_REV="$(git -C "$REPOSITORY" rev-parse HEAD)"
export READER_REV="$EXECUTION_REV"
test "$(gh pr view 157 --repo jlevy/squares --json state --jq .state)" = OPEN
test "$(gh pr view 157 --repo jlevy/squares --json baseRefName --jq .baseRefName)" = \
  codex/n11-bc329-runner-publication-stack
export PR157_REF="$(gh pr view 157 --repo jlevy/squares --json headRefName --jq .headRefName)"
test "$PR157_REF" = claude/n11-w7-weighted-atom-admission
export PR157_HEAD="$(gh pr view 157 --repo jlevy/squares --json headRefOid --jq .headRefOid)"
test "$EXECUTION_REV" = "$PR157_HEAD"
test "$EXECUTION_REV" = \
  "$(gh api "repos/jlevy/squares/git/ref/heads/$PR157_REF" --jq .object.sha)"
export PR156_HEAD="$(gh pr view 156 --repo jlevy/squares --json headRefOid --jq .headRefOid)"
git -C "$REPOSITORY" merge-base --is-ancestor "$PR156_HEAD" "$EXECUTION_REV"

export READER_PATH=packing/devtools/read_fixed_core_calibration_profile.py
export READER_BLOB="$(git -C "$REPOSITORY" rev-parse "$READER_REV:$READER_PATH")"
test "$READER_BLOB" = "$(git -C "$REPOSITORY" hash-object "$REPOSITORY/$READER_PATH")"
test "$READER_REV" = "$EXECUTION_REV"

test "$(wc -c < "$REPOSITORY/packing/cases/n02_fixed_core_packet_calibration/fixture.json" | tr -d ' ')" = 935
test "$(shasum -a 256 "$REPOSITORY/packing/cases/n02_fixed_core_packet_calibration/fixture.json" | awk '{print $1}')" = \
  1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539
test "$(git -C "$REPOSITORY" show "$EXECUTION_REV:packing/cases/n02_fixed_core_packet_calibration/fixture.json" | shasum -a 256 | awk '{print $1}')" = \
  1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539

assert_pr157_identity() {
  test "$(git -C "$REPOSITORY" branch --show-current)" = codex/pr157-reviewed-stack
  test "$(git -C "$REPOSITORY" rev-parse HEAD)" = "$EXECUTION_REV"
  if git -C "$REPOSITORY" rev-parse -q --verify MERGE_HEAD > /dev/null; then
    return 1
  fi
  test -z "$(git -C "$REPOSITORY" status --porcelain=v1 --untracked-files=all)"
  git -C "$REPOSITORY" diff --quiet
  git -C "$REPOSITORY" diff --cached --quiet
  test ! -e "$PACKING/.gate-running"
  test "$(gh pr view 157 --repo jlevy/squares --json state --jq .state)" = OPEN
  test "$(gh pr view 157 --repo jlevy/squares --json baseRefName --jq .baseRefName)" = \
    codex/n11-bc329-runner-publication-stack
  test "$(gh pr view 157 --repo jlevy/squares --json headRefName --jq .headRefName)" = \
    "$PR157_REF"
  test "$(gh pr view 157 --repo jlevy/squares --json headRefOid --jq .headRefOid)" = \
    "$EXECUTION_REV"
  test "$(gh api "repos/jlevy/squares/git/ref/heads/$PR157_REF" --jq .object.sha)" = \
    "$EXECUTION_REV"
  test "$(gh pr view 156 --repo jlevy/squares --json headRefOid --jq .headRefOid)" = \
    "$PR156_HEAD"
  git -C "$REPOSITORY" merge-base --is-ancestor "$PR156_HEAD" "$EXECUTION_REV"
  test "$READER_REV" = "$EXECUTION_REV"
  test "$READER_BLOB" = "$(git -C "$REPOSITORY" hash-object "$REPOSITORY/$READER_PATH")"
}
assert_pr157_identity
```

The independent reader review must accept `READER_BLOB` at `EXECUTION_REV` and the file
the checkout executes.
Every `read` and `join` call in the run sheet must pass
`--expect-execution-revision "$EXECUTION_REV"` and
`--expect-reader-revision "$READER_REV"`. In the same shell, insert this call
immediately before `set +e` in the run sheet’s **One Maintained Coordinator Command**
block:

```bash
assert_pr157_identity
```

A changed ref or checkout requires a new execution revision and review.

## Math and Source Closure Gates

Keep the two PR157-MATH-05 expansion controls and the packet-boundary control on the
integrated tree. They require the trillion-token weighted atom and the unweighted
half-threshold subset explosion to refuse before token or subset work.
The packet control exercises `run_raw_sweep` and `run_exact_route` with one or two
workers and both hostile atom shapes, before shared state, workers, or receipts.
Run them from `PACKING` with the checkout’s Python 3.14, then retain their passing
output with the exact execution revision.
The
[weighted-atom handoff](../../../../packing/campaign/agent-sessions/session-127-weighted-five-site-atom-admission.md)
records the resource limits and review.

```bash
"$PYTHON" -m pytest -q \
  tests/test_weighted_threshold_atoms.py::test_a_compact_trillion_token_atom_is_refused_before_any_token_work \
  tests/test_fractional_threshold.py::test_the_half_threshold_term_explosion_is_refused_before_enumeration \
  tests/test_fixed_core_packet.py::test_packet_sweeps_refuse_expansion_before_shared_state_workers_or_receipts
```

The [run-set verifier contract](plan-2026-09-13-n11-bc329-runset-verifier.md) defines
the complete import closure, fixture, and runtime declarations.
After the run sheet’s `retain` step, inspect every staged path and use its **Durable
Retention** block to check the actual index tree with
`source-closure --candidate-tree "$TREE_OID"`. The verifier must return accepted JSON
binding `EXECUTION_REV` and `TREE_OID`. Do not replace this with a comparison of
selected source files; PR157 changes paths inside the receipt-bound closure.

Before the evidence commit, require `HEAD` still to equal `EXECUTION_REV` and tracked
working files to match the index.
The evidence commit must have `EXECUTION_REV` as its sole parent and the checked staged
tree as its tree. Apply the run sheet’s postcommit
`source-closure --candidate-tree "$EVIDENCE_COMMIT"` check, retain both accepted JSON
outputs and their hashes outside `REVIEW_ROOT`, and record the exact evidence commit
OID. The required parent and tree checks are:

```bash
test "$(git -C "$REPOSITORY" rev-parse HEAD)" = "$EXECUTION_REV"
git -C "$REPOSITORY" diff --quiet
# Commit the inspected index using the run sheet's Durable Retention block.
test "$(git -C "$REPOSITORY" rev-list --parents -n 1 "$EVIDENCE_COMMIT")" = \
  "$EVIDENCE_COMMIT $EXECUTION_REV"
test "$(git -C "$REPOSITORY" rev-parse "$EVIDENCE_COMMIT^{tree}")" = "$TREE_OID"
```

An accepted calibration profile remains an operational measurement on the solved `n=2`
fixture. BC329 registration and execution require their separate admission after the
evidence commit is published and hosted checks pass.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
