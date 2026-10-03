# BC329 Target-Free Three-Profile Run Sheet

Date: September 13, 2026. Owner: `think-vy5i`. Admission owners: `think-gscz`,
`think-5dql`, `think-n4gh`, and `think-pp3j`.

This sheet measures the fixed-core runner on a solved $n=2$ fixture before BC329 is
allowed to run. Each profile exercises the same four route shapes and retains 14,404
direction rows. The fixture is deliberately easy, so its time and memory measurements
describe operating overhead.
They do not predict the cost of BC329.

The profile schema is `fixed-core-packet-calibration/v1`. It cannot state a scientific
acceptance or a new lower bound.
Following this sheet does not allocate an experiment, register BC329, open the BC329
source, or invoke `devtools.fixed_core_packet`.

## Admission State

Do not execute the coordinator until every row below says **accepted** at one common,
clean PR 156 head.

| Gate | Required evidence | Current state |
| --- | --- | --- |
| Calibration producer | CAL-1 through CAL-7 accepted on the integrated source | Accepted through implementation head `fcb538c29b846fb5e7c33bd962772ada9c21aedd`; exact PR-head integration review pending |
| Observed worker topology | Configured and observed workers, task lifetimes, child identities, and supervisor binding reconstruct from retained bytes | [First review](../../reviews/review-2026-09-13-n11-bc329-topology-coordinator-initial.md) refused temporal binding; `fc3e314d` repairs that boundary, but cross-route and phase-time checks remain open |
| Three-profile coordinator | Three sequential fresh profiles, exact command records, strict readback, and atomic summary publication | [Rereview](../../reviews/review-2026-09-13-n11-bc329-coordinator-rereview.md) at `fc3e314d` refused inverted route chronology, disjoint phase time, and a second `result.json` read. Repair `dbbf8495` closed those targeted controls, but its [exact-head review](../../reviews/review-2026-09-13-n11-bc329-coordinator-final.md) found infinite deadline identity and finite phase-sum overflow. The [follow-up exact-head review](../../reviews/review-2026-09-13-n11-bc329-coordinator-arithmetic-final.md) accepts both arithmetic repairs at `775c71d5`; later integrated-head and positive-run evidence remain |
| Source-distinct reader | Separate implementation; independently bound revision, geometry, arithmetic, rows, resources, and topology | [Rereview](../../reviews/review-2026-09-13-n11-bc329-reader-rereview.md) of `7e4d2487` accepted F1–F5 and refused F6/F7. The [exact-commit review](../../reviews/review-2026-09-13-n11-bc329-reader-f6f7-overflow.md) of the first repair refused F6b finite phase overflow. The [final exact-head review](../../reviews/review-2026-09-13-n11-bc329-reader-f6f7-final.md) accepted F6/F7 at `a5701e73` after 23 independent full-binder controls. Later integrated-head/source closure remains under `think-n4gh` |
| Run-set verifier | Source-distinct proof join, coordinator-root inventory and retention, and full source closure | Initial [exact-head review](../../reviews/review-2026-09-13-n11-bc329-runset-verifier.md) refused six controls. Repair `0874e912` closed those controls, but its [rereview](../../reviews/review-2026-09-13-n11-bc329-runset-verifier-rereview.md) refused a valid 22-file coordinator root and a status check/copy race. The [final R3 exact-head review](../../reviews/review-2026-09-13-n11-bc329-runset-verifier-r3-final.md) accepts the repair at verifier blobs from `2ea77405`; actual positive-run bytes, evidence-commit OID, and later integrated-head admission remain |
| This run sheet | Literal commands, frozen values, refusal rules, and retention path accepted on the execution head | [Independent operational review](../../reviews/review-2026-09-13-n11-bc329-three-profile-run-sheet.md) refused the earlier snapshot. The [integrated-head review](../../reviews/review-2026-09-13-n11-bc329-integrated-run-sheet.md) refused missing verifier wiring at `fbd915fc`. A [wiring rereview](../../reviews/review-2026-09-13-n11-bc329-run-sheet-identity-refusal.md) accepted the five verifier commands but refused evidence-commit parent identity; the revised sheet remains a draft pending final exact-head rereview |
| Remote identity | Clean local `HEAD` equals the live PR 156 head | Pending the reviewed integration push |
| Profiles and BC329 | No positive profile and no BC329 target has run | Satisfied |

An acceptance of one ancestor does not admit an unreviewed merge resolution.
Record the exact execution revision and each review verdict before changing this table
to accepted.

## Frozen Values

All three profiles use one tuple:

| Setting | Frozen value |
| --- | ---: |
| Requested workers | $4$ |
| Effective raw workers | $4$ |
| Effective normalized-exact workers | $4$ |
| Effective reflected-interval workers | $1$ |
| Effective dilation workers | $1$ |
| Internal calibration allowance | $5400$ seconds |
| External supervisor allowance | $7200$ seconds |
| Termination grace | $2$ seconds |
| Expected direction rows per profile | $14{,}404$ |

The tuple is `4 / 5400 / 7200 / 2`. A different worker count or allowance requires a new
reviewed sheet. These values do not set the later BC329 allowance.

The fixture is exactly 935 bytes with SHA-256
`1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539` at
`packing/cases/n02_fixed_core_packet_calibration/fixture.json`.

## Execution Preconditions

Use the PR 156 worktree on an otherwise idle Apple silicon macOS host.
The runtime must be the checkout’s Python 3.14 environment.
`uv` must be at least 0.12. Run `uv sync` once before the series; do not clear its cache
between profiles. This controls the Python environment and makes no cold
operating-system-cache claim.
Run the Bash blocks below in order in one shell, so each exported revision and path
remains bound to the same run set.

```bash
set -euo pipefail

export REPOSITORY=/private/tmp/squares-n11-bc329-stack
export PACKING="$REPOSITORY/packing"
export UV_CACHE_DIR=/private/tmp/bc329-pr156-uv-cache
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONOPTIMIZE=0
export LC_ALL=C
export TZ=UTC

test "$(git -C "$REPOSITORY" branch --show-current)" = \
  codex/n11-bc329-runner-publication-stack
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
export PR156_HEAD="$(gh pr view 156 --repo jlevy/squares --json headRefOid --jq .headRefOid)"
test "$EXECUTION_REV" = "$PR156_HEAD"
test -z "$(git -C "$REPOSITORY" status --porcelain=v1 --untracked-files=all)"
git -C "$REPOSITORY" diff --quiet
git -C "$REPOSITORY" diff --cached --quiet

test "$(wc -c < "$REPOSITORY/packing/cases/n02_fixed_core_packet_calibration/fixture.json" | tr -d ' ')" = 935
test "$(shasum -a 256 "$REPOSITORY/packing/cases/n02_fixed_core_packet_calibration/fixture.json" | awk '{print $1}')" = \
  1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539
test "$(git -C "$REPOSITORY" show "$EXECUTION_REV:packing/cases/n02_fixed_core_packet_calibration/fixture.json" | shasum -a 256 | awk '{print $1}')" = \
  1aface38ab79526397b7b9f24325df844e2eb9717d3e29a094fcdefe8822f539
```

The admission records must name `EXECUTION_REV`. The reader executes from the same clean
checkout, so its revision argument must equal that exact head.
The independent reader review must bind the reader file’s bytes at that head; a separate
module does not imply a different Git revision.
It must also bind the file from which the reader is actually executing, so an external
copy cannot claim the checkout’s revision.

## Fresh Roots and Host Observations

The coordinator requires a fresh, nonexistent run root and creates `profile-1`,
`profile-2`, and `profile-3` itself.
The sibling review root holds the coordinator’s top-level console record, the pre-series
host snapshot, and the maintained verifier’s inventory, reader records, and admission.
Its retention whitelist is exactly 19 files: five host/coordinator records, the
inventory and admission, and four reader records per profile.
Keep verifier console output in a separate audit root; no other file belongs in
`REVIEW_ROOT`. Nothing written after the coordinator returns may be placed inside the
run root or any profile directory.

```bash
export RUN_SET_ID="$(date -u +%Y%m%dT%H%M%SZ)-${EXECUTION_REV:0:12}-$$"
export RUN_ROOT="/private/tmp/bc329-fixed-core-calibration-$RUN_SET_ID"
export REVIEW_ROOT="/private/tmp/bc329-fixed-core-calibration-review-$RUN_SET_ID"
export AUDIT_ROOT="/private/tmp/bc329-fixed-core-calibration-audit-$RUN_SET_ID"
test ! -e "$RUN_ROOT"
test ! -e "$REVIEW_ROOT"
test ! -e "$AUDIT_ROOT"
mkdir "$REVIEW_ROOT"
mkdir "$AUDIT_ROOT"

ps -axo pid=,ppid=,pgid=,%cpu=,rss=,etime=,comm= \
  > "$REVIEW_ROOT/pre-series-processes.txt"
uptime > "$REVIEW_ROOT/pre-series-uptime.txt"

export CACHE_1="run 1: shared UV cache $UV_CACHE_DIR retained; no cold-cache claim"
export CACHE_2="run 2: shared UV cache $UV_CACHE_DIR retained; no cold-cache claim"
export CACHE_3="run 3: shared UV cache $UV_CACHE_DIR retained; no cold-cache claim"
export LOAD_1="run 1: pre-series argument-free process snapshot at $REVIEW_ROOT/pre-series-processes.txt; no quiet-host lease claimed"
export LOAD_2="run 2: same pre-series snapshot; sequential execution; no quiet-host lease claimed"
export LOAD_3="run 3: same pre-series snapshot; sequential execution; no quiet-host lease claimed"
```

These strings are invocation-bound operator observations.
They are not per-run host measurements and do not prove exclusive use of the machine.

## One Maintained Coordinator Command

Do not create `RUN_ROOT` first.
The command creates it, runs the three profiles in order, executes both maintained
immediate readers after each profile, and stops at the first refusal.
It records each internal command’s exact argument vector, status, stdout, stderr, and
the calibration command’s monotonic time through process return.
It then atomically publishes and rereads one duplicate-key-safe summary.

```bash
set +e
"$PYTHON" -m devtools.run_fixed_core_calibration_profiles run \
  --repository "$REPOSITORY" \
  --expect-implementation-revision "$EXECUTION_REV" \
  --run-root "$RUN_ROOT" \
  --workers 4 \
  --calibration-seconds 5400 \
  --external-seconds 7200 \
  --grace-seconds 2 \
  --cache-observation "$CACHE_1" \
  --cache-observation "$CACHE_2" \
  --cache-observation "$CACHE_3" \
  --background-load "$LOAD_1" \
  --background-load "$LOAD_2" \
  --background-load "$LOAD_3" \
  > "$REVIEW_ROOT/coordinator.stdout.log" \
  2> "$REVIEW_ROOT/coordinator.stderr.log"
COORDINATOR_STATUS=$?
set -e
printf '%s\n' "$COORDINATOR_STATUS" > "$REVIEW_ROOT/coordinator.status"
test "$COORDINATOR_STATUS" -eq 0
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset snapshot \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  > "$AUDIT_ROOT/snapshot.stdout.json" \
  2> "$AUDIT_ROOT/snapshot.stderr.log"
jq -e '.status == "accepted" and .inventory_sha256 != null' \
  "$AUDIT_ROOT/snapshot.stdout.json" > /dev/null
```

After this command returns, treat the entire `RUN_ROOT` as immutable.
A successful coordinator has exactly 22 top-level files: one summary, three run records,
and 18 calibration/readback logs.
The snapshot records every run-root directory and file type, byte count, and digest at
the first post-return observation.
A retry uses a new run-set identity.
Keep a refused or partial root for diagnosis.

## Source-Distinct Readback

The source-distinct reader is a separate maintained module.
It does not import the producer’s fixture factory, constants, normalization, receipt
validator, direction reconstruction, membership replay, or dilation helper.
It independently checks the closed calibration schema, source and reader revisions,
exact fixture geometry, normalization and dilation arithmetic, every retained row and
digest, worker topology, resource summaries, invocation identity, and supervisor
binding.

After `think-n4gh` is independently accepted, use the verifier to launch each reader in
order. It checks the snapshot before and after each child, writes that reader’s exact
argv, status, streams, and proof into `REVIEW_ROOT`, and refuses a changed run root.
Each status test stops the shell before the next reader on refusal.

```bash
export READER_REV="$EXECUTION_REV"

set +e
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset read \
  --repository "$REPOSITORY" \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --expect-reader-revision "$READER_REV" \
  --run-order 1 \
  > "$AUDIT_ROOT/read-1.stdout.log" \
  2> "$AUDIT_ROOT/read-1.stderr.log"
READER_1_STATUS=$?
set -e
test "$READER_1_STATUS" -eq 0

set +e
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset read \
  --repository "$REPOSITORY" \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --expect-reader-revision "$READER_REV" \
  --run-order 2 \
  > "$AUDIT_ROOT/read-2.stdout.log" \
  2> "$AUDIT_ROOT/read-2.stderr.log"
READER_2_STATUS=$?
set -e
test "$READER_2_STATUS" -eq 0

set +e
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset read \
  --repository "$REPOSITORY" \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --expect-reader-revision "$READER_REV" \
  --run-order 3 \
  > "$AUDIT_ROOT/read-3.stdout.log" \
  2> "$AUDIT_ROOT/read-3.stderr.log"
READER_3_STATUS=$?
set -e
test "$READER_3_STATUS" -eq 0

"$PYTHON" -m devtools.verify_fixed_core_calibration_runset join \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --expect-reader-revision "$READER_REV" \
  > "$AUDIT_ROOT/join.stdout.json" \
  2> "$AUDIT_ROOT/join.stderr.log"
jq -e '.status == "accepted" and (.runs | length) == 3' \
  "$AUDIT_ROOT/join.stdout.json" > /dev/null
```

The revision equality follows the reader CLI’s checkout binding.
It does not waive the independent review: the reviewer must accept the reader file’s
exact bytes at `EXECUTION_REV` before this sheet becomes eligible.

Require `run-root-inventory.json`, each profile’s `.command.json`, `.stdout.json`,
`.stderr.log`, and `.status`, and `run-set-reader-admission.json` in `REVIEW_ROOT`. The
join checks all three reader proofs against their coordinator runs, including exact
argv, revisions, typed invocation identity, and receipt byte counts and digests.
The [maintained verifier contract](plan-2026-09-13-n11-bc329-runset-verifier.md)
specifies the exact reader-command/proof join (R2), run-root byte/type inventory and
archive comparison (R3), and full source-closure check (R4). Its first implementation
landed at `878e18d0`, but the
[independent exact-head review](../../reviews/review-2026-09-13-n11-bc329-runset-verifier.md)
refused all three obligations: six mutations expose shared-invalid identity types, an
extra run record, a stale staged-tree argument, inconsistent copied proof bytes, a
changed coordinator status, and an oversized-JSON refusal-path failure.
The
[verifier rereview](../../reviews/review-2026-09-13-n11-bc329-runset-verifier-rereview.md)
at `0874e912` confirms that all six original controls now refuse, but it finds two new
R3 blockers: the coordinator’s required command logs are rejected, and a changed nonzero
status can pass between the first status read and the retained digest snapshot.
The
[follow-up R3 review](../../reviews/review-2026-09-13-n11-bc329-runset-verifier-r3-final.md)
accepts both repairs at its exact source blobs.
The literal commands and retention block below remain an unadmitted draft until all
implementation gates are accepted on one integrated execution head and the postcommit
source-closure check is exercised.

## Refusal Conditions

Abort before the coordinator if any of these holds:

- one implementation or sheet review does not accept the exact integrated head;
- local `HEAD`, the live PR 156 head, or the named execution revision differ;
- the checkout is dirty, `uv` is older than 0.12, the runtime is outside the checkout’s
  Python 3.14 environment, or the fixture bytes differ;
- the tuple is not exactly `4 / 5400 / 7200 / 2`;
- `RUN_ROOT`, `REVIEW_ROOT`, or `AUDIT_ROOT` already exists;
- another profile, validation gate, package build, or scientific target is running; or
- the operator sees material competing host load.

Stop and retain the current root if the coordinator exits nonzero, any run is incomplete
or refused, a command record or summary is absent, process-group reaping is unproved,
the receipt reports an RSS observer error or fewer than two positive error-free samples,
or an immediate readback fails.

Refuse operational admission if any profile lacks one of its 14,404 direction rows;
contains a wrong or duplicate label; reports a raw charge other than 2, a normalized
exact or dilation charge other than 1, an interval enclosure other than $[8,8]$, a
dense/slab disagreement, a stall, or exhausted interval budget; changes the candidate,
dilation, topology, RSS, source, invocation, or receipt binding; or fails the
source-distinct reader.
Also refuse if the reader command or revision differs from the accepted record, if an
immutable run artifact changes after coordinator return, or if the retention destination
already exists. A nonzero `snapshot`, `read`, `join`, `retain`, or `source-closure`
status, or a failed accepted-JSON check, stops admission and preserves the external
roots for diagnosis.

A refusal is operational evidence.
It is not a BC329 result.

## Durable Retention

After all three source-distinct reads pass, retain the evidence in Git at

```text
packing/campaign/series/series-000-smoke-and-calibration/results/agenda-035/bc329-fixed-core-calibration-${EXECUTION_REV:0:12}/
```

The directory contains the three-profile summary, coordinator console records, host
observations, all 19 whitelisted review records, and a compressed archive of the
unchanged `RUN_ROOT`, plus a SHA-256 file and archive contents list.
The raw archive is part of the evidence commit so the retained proof does not depend on
an expiring CI artifact.
`retain` requires a fresh, nonexistent evidence root; it copies the exact review set,
compares each archived member with the coordinator-return inventory, and rereads the
archive digest. Leave the external run, review, and audit roots in place on any refusal.

```bash
export EVIDENCE_RELATIVE="packing/campaign/series/series-000-smoke-and-calibration/results/agenda-035/bc329-fixed-core-calibration-${EXECUTION_REV:0:12}"
export EVIDENCE_ROOT="$REPOSITORY/$EVIDENCE_RELATIVE"
test ! -e "$EVIDENCE_ROOT"
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset retain \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --evidence-root "$EVIDENCE_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  > "$AUDIT_ROOT/retain.stdout.json" \
  2> "$AUDIT_ROOT/retain.stderr.log"
jq -e --arg revision "$EXECUTION_REV" \
  '.status == "accepted" and .execution_revision == $revision' \
  "$AUDIT_ROOT/retain.stdout.json" > /dev/null
(
  cd "$EVIDENCE_ROOT"
  shasum -a 256 -c run-root.tar.gz.sha256
  tar -tzf run-root.tar.gz | diff -u run-root-contents.txt -
)
```

Stage the evidence directory and any intended status documents.
Inspect the staged paths before running this block.
The candidate is the actual index tree, not a named ancestor or a hand-picked three-file
diff.
The verifier reconstructs the complete receipt import closure, fixture, and runtime
declarations at `EXECUTION_REV`; it compares modes, blobs, hashes, and working bytes
with that staged tree.

```bash
git -C "$REPOSITORY" add -- "$EVIDENCE_RELATIVE"
git -C "$REPOSITORY" diff --cached --name-status
if git -C "$REPOSITORY" diff --cached --quiet; then
  exit 1
fi
export TREE_OID="$(git -C "$REPOSITORY" write-tree)"
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset source-closure \
  --repository "$REPOSITORY" \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --candidate-tree "$TREE_OID" \
  > "$AUDIT_ROOT/source-closure-staged.stdout.json" \
  2> "$AUDIT_ROOT/source-closure-staged.stderr.log"
jq -e --arg revision "$EXECUTION_REV" --arg tree "$TREE_OID" \
  '.schema == "fixed-core-calibration-source-closure-check/v2" and
   .status == "accepted" and .execution_revision == $revision and
   .candidate_tree == $tree' \
  "$AUDIT_ROOT/source-closure-staged.stdout.json" > /dev/null
```

Commit that inspected index tree.
Then pass the exact new `HEAD` commit OID to the same verifier.
Before committing, require `HEAD` to remain `EXECUTION_REV` and tracked working files to
match the index. After committing, require the evidence commit to have exactly that
execution commit as its sole parent.
Its tree must still equal `TREE_OID`; the postcommit verifier also requires the index to
match that commit tree.
Keep both accepted JSON outputs outside `REVIEW_ROOT`, and record their hashes and the
actual evidence commit OID in the admission disposition.

```bash
test "$(git -C "$REPOSITORY" rev-parse HEAD)" = "$EXECUTION_REV"
git -C "$REPOSITORY" diff --quiet
git -C "$REPOSITORY" commit -m "Retain target-free BC329 fixed-core calibration run set"
export EVIDENCE_COMMIT="$(git -C "$REPOSITORY" rev-parse HEAD)"
test "$(git -C "$REPOSITORY" rev-list --parents -n 1 "$EVIDENCE_COMMIT")" = \
  "$EVIDENCE_COMMIT $EXECUTION_REV"
test "$(git -C "$REPOSITORY" rev-parse "$EVIDENCE_COMMIT^{tree}")" = "$TREE_OID"
"$PYTHON" -m devtools.verify_fixed_core_calibration_runset source-closure \
  --repository "$REPOSITORY" \
  --run-root "$RUN_ROOT" \
  --review-root "$REVIEW_ROOT" \
  --expect-execution-revision "$EXECUTION_REV" \
  --candidate-tree "$EVIDENCE_COMMIT" \
  > "$AUDIT_ROOT/source-closure-committed.stdout.json" \
  2> "$AUDIT_ROOT/source-closure-committed.stderr.log"
jq -e --arg revision "$EXECUTION_REV" --arg tree "$TREE_OID" \
  '.schema == "fixed-core-calibration-source-closure-check/v2" and
   .status == "accepted" and .execution_revision == $revision and
   .candidate_tree == $tree' \
  "$AUDIT_ROOT/source-closure-committed.stdout.json" > /dev/null
shasum -a 256 "$AUDIT_ROOT/source-closure-staged.stdout.json" \
  "$AUDIT_ROOT/source-closure-committed.stdout.json" \
  > "$AUDIT_ROOT/source-closure-outputs.sha256"
printf '%s\n' "$EVIDENCE_COMMIT" > "$AUDIT_ROOT/evidence-commit.txt"
```

The evidence commit advances PR 156 beyond `EXECUTION_REV`; it may add evidence and
status documents but must preserve every receipt-bound source path.
Keep the external originals until the evidence commit is pushed, hosted CI passes, and
`think-1mma` records admission.

Only then may `think-17qa` register one BC329 scientific target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
