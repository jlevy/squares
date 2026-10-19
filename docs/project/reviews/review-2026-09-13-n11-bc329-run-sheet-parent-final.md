# PR 156 Run-Sheet Parent-Identity Final Rereview

**Verdict: ACCEPT the current run-sheet working blob for this exact-diff
operational-wiring review.** The new precommit and postcommit assertions close the
evidence-commit parent gap identified in the prior rereview.
This is acceptance of the draft command procedure, not permission to execute profiles
from the currently dirty checkout or a claim that the outstanding independent gates have
passed. No positive profile or BC329 target was run.

## Exact Boundary

- Reviewed file:
  `docs/project/specs/archive/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md` in
  `/private/tmp/squares-n11-bc329-stack`, uncommitted Git blob
  `e6f448896b28ed4f7163aa70a9439a9621d8e466`, SHA-256
  `5bbbf8753ab2edcb683a7592a1a22db910f0932443dacfdd8e064cfca982127b`.
- Base local HEAD: `fbd915fc3b2fcdbb26d032dd67f43dffc3bec18d`. Maintained verifier blob:
  `cd17583c410043367b1a85707617a68df095f74e`; coordinator blob:
  `2e98fd58e81b266b21c64bfa0109b5a2b056e801`.
- Scope: the current run-sheet diff and its literal command contract.
  This rereview did not edit the repository, index, commits, or remote.
  The checkout remains dirty, so the sheet’s own clean-head execution precondition is
  not satisfied here.

## Checks

- The concatenated Bash fences pass `bash -n`, and `git diff --check` finds no
  whitespace error. The coordinator still uses the frozen `4 / 5400 / 7200 / 2` tuple.
  All five verifier subcommand names, required flags, and tested JSON fields match its
  parser and printed objects (`verify_fixed_core_calibration_runset.py:1140-1200`).
- `snapshot` follows the zero coordinator status; each `read` status is checked before
  the next reader; `join` follows all three accepted reads.
  Verifier stdout/stderr stays in `AUDIT_ROOT`, outside the exact 19-file `REVIEW_ROOT`
  whitelist. The verifier’s top-level run-root set is exactly 22 files, and its retention
  whitelist is exactly 19 review files
  (`verify_fixed_core_calibration_runset.py:36-47, 102-116`).
- `retain` is called with a nonexistent evidence root and enforces the inventory/archive
  comparison. Staged `source-closure` uses `git write-tree`; the committed call uses the
  actual evidence commit.
  The postcommit JSON assertion correctly compares the verifier’s resolved
  `candidate_tree` with the saved `TREE_OID`.
- The new precommit `HEAD == EXECUTION_REV` assertion and `git diff --quiet` check
  appear immediately before `git commit` (`run sheet:424-425`). After that commit,
  `git rev-list --parents -n 1 "$EVIDENCE_COMMIT"` must equal exactly
  `"$EVIDENCE_COMMIT $EXECUTION_REV"` (`:428-429`). This binds a single parent,
  rejecting both a moved head and a merge commit.
  The existing tree equality and postcommit source-closure checks remain in place
  (`:429-443`), binding the committed tree and index to the inspected candidate.
- A target-free isolated Git control accepted a direct evidence child; it rejected an
  intervening document-only parent both before and after commit, rejected an additional
  merge parent, and rejected an unstaged tracked edit.
  These controls exercised the literal Git assertions without a calibration run.
  No full verifier invocation was possible or needed without positive run-set bytes.

## Remaining Admission Gates

The sheet’s gate table still requires integrated-head acceptance of the producer,
coordinator, reader, and verifier at one clean execution revision; independent
acceptance of the reader at that exact revision; this sheet’s accepted revision
committed and reviewed; and equality between local `HEAD` and the live PR 156 head
before execution. Positive three-profile evidence, staged and postcommit source-closure
outputs, the actual evidence-commit OID, hosted CI, and the later admission disposition
do not exist yet. BC329 remains unregistered and unrun.
Any future edit to this sheet requires another exact-blob review before its admission
row can be marked accepted.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
