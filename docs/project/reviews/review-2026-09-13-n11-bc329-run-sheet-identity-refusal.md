# PR 156 Run-Sheet Exact-Diff Rereview

**Verdict: REFUSE this run-sheet revision for execution admission.** The five
maintained-verifier commands are wired with the correct flags, output checks, and
22-file/19-file boundaries.
One commit-identity gap remains: after the long profile run, the sheet can commit
evidence on a different parent while its staged and postcommit checks still accept.
No positive profile or BC329 target was run.

## Exact Boundary

- Scope: read-only review of the uncommitted diff to
  `docs/project/specs/archive/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md` in
  `/private/tmp/squares-n11-bc329-stack`, plus the maintained verifier and relevant CLI
  contracts. The report itself is outside the repository.
  No repository file, index, commit, bead, or remote was changed by this review.
- Local base HEAD: `fbd915fc3b2fcdbb26d032dd67f43dffc3bec18d`. Reviewed run-sheet
  working-file Git blob: `8a838bfa5f0214d101d11d5d780aeb583f23cbd1`. Maintained verifier
  blob: `cd17583c410043367b1a85707617a68df095f74e`.
- The working tree was already dirty: the run sheet and document map were modified, and
  two review documents were untracked.
  This is a prospective rereview of the draft bytes, not a claim that the current
  checkout satisfies the run sheet’s clean-head execution gate.

## Accepted Wiring

- Concatenated Bash fences pass `bash -n`; `git diff --check` reports no whitespace
  error. The coordinator’s literal `4 / 5400 / 7200 / 2` flags match its parser.
  The verifier’s `_parser` accepts the exact `snapshot`, `read`, `join`, `retain`, and
  `source-closure` flags used by the sheet
  (`packing/devtools/verify_fixed_core_calibration_runset.py:1140-1156`).
- The successful coordinator writes exactly 22 top-level run-root files: one summary,
  three run records, and 18 stdout/stderr logs.
  The verifier’s `COORDINATOR_TOP_LEVEL_FILES` matches this set
  (`verify_fixed_core_calibration_runset.py:36-47`). Its `REVIEW_NAMES` has exactly 19
  files: five host/coordinator records, inventory and admission, and four reader records
  per profile (`:102-116`). The sheet’s separate audit root keeps verifier console
  output out of this exact review whitelist.
- The coordinator status test precedes `snapshot` (`run sheet:191-203`). Each `read`
  exit is tested before the next child; `join` follows all three (`:230-283`). The
  verifier captures reader argv/status/streams, checks the live root against the
  snapshot on both sides of each child, and joins typed proof identities and receipt
  byte/digest bindings (`verify_fixed_core_calibration_runset.py:533-603, 645-761`). A
  zero exit from `read` is not by itself a joined proof; the final `join` supplies that
  check.
- `retain` receives a nonexistent evidence root, copies the 19 review files, rereads the
  archive digest, and checks archive members against the coordinator-return inventory
  (`run sheet:363-381`; verifier `:820-939`). The sheet’s extra hash and contents check
  matches its emitted filenames.
- Both `source-closure` calls pass the required repository, roots, execution revision,
  and candidate. Its JSON prints the resolved tree OID in `candidate_tree`, so comparing
  both outputs with `TREE_OID` is correct (`run sheet:399-442`; verifier
  `:1041-1135, 1159-1200`). The verifier reconstructs the receipt source closure,
  fixture, and three runtime declarations, then compares execution, candidate, and
  working bytes.

## Blocking Finding: Evidence Commit Parent Is Not Bound to Execution Revision

The preflight binds `HEAD` and the live PR head to `EXECUTION_REV` only before the
coordinator (`run sheet:106-111`). After the run, the staged check passes `TREE_OID` and
validates source closure and index-tree equality (`:391-411`). The postcommit block
requires only `EVIDENCE_COMMIT != EXECUTION_REV`, its tree equals `TREE_OID`, and the
verifier accepts that commit as current `HEAD` with the same index tree (`:422-438`).
Neither the sheet nor `verify_source_closure`
(`verify_fixed_core_calibration_runset.py:1053-1070`) checks the evidence commit’s
parent.
Thus an intervening HEAD movement can leave the reviewed source closure unchanged
while making the evidence commit advance a different branch state.
The claimed exact PR 156 execution-to-evidence identity is then unproved.

A target-free isolated Git reproduction used an execution commit, an intervening
document-only commit that preserved source bytes, and an evidence commit.
The sheet’s existing postcommit conditions all passed (`candidate != execution`,
candidate tree = staged tree, index tree = candidate tree, candidate = current `HEAD`).
The proposed exact-parent condition refused because
`git rev-list --parents -n 1 "$candidate"` was not `"$candidate $execution"`. This tests
the Git identity gap without invoking the verifier or a profile.
The verifier source has no parent/ancestry branch to close that gap; a valid retained
run set with unchanged receipt closure would reach the same identity checks.

Minimum repair, placed after staged closure acceptance and immediately before
`git commit`, then after computing `EVIDENCE_COMMIT`:

```bash
test "$(git -C "$REPOSITORY" rev-parse HEAD)" = "$EXECUTION_REV"
git -C "$REPOSITORY" diff --quiet
# Inspect the already printed staged name/status set; commit exactly that index.
git -C "$REPOSITORY" commit -m "Retain target-free BC329 fixed-core calibration run set"
export EVIDENCE_COMMIT="$(git -C "$REPOSITORY" rev-parse HEAD)"
test "$(git -C "$REPOSITORY" rev-list --parents -n 1 "$EVIDENCE_COMMIT")" = \
  "$EVIDENCE_COMMIT $EXECUTION_REV"
```

The precommit equality catches an earlier HEAD movement.
The postcommit single-parent equality catches a movement between that check and
`git commit` and rules out a merge commit with an extra parent.
Keep the existing tree equality and postcommit `source-closure` checks; they bind the
committed bytes and index, while the added assertions bind its history to the execution
commit. The existing clean preflight and staged-path inspection remain necessary for the
intended index contents.

This verdict concerns the sheet’s current uncommitted bytes only.
The admission table correctly leaves integrated-head review, remote identity, and
positive-run evidence pending.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
