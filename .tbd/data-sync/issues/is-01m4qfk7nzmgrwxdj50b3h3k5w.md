---
type: is
id: is-01m4qfk7nzmgrwxdj50b3h3k5w
title: Label every issue; intake label in the runbook and sweep
kind: task
status: closed
priority: 2
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T07:17:53.470Z
updated_at: 2026-10-12T23:39:01.383Z
started_at: 2026-10-12T07:18:01.788Z
closed_at: 2026-10-12T23:39:01.382Z
close_reason: "Delivered in PR #546 (merged 2026-10-12): 68 labels on 65 issues, and check_requests --github plus the intake sweep list an intake entry lacking the label (266093429, cf24e494f, 28f412bf4)."
resolution: null
duplicate_of: null
---

## Notes

## Labels, 2026-10-12

Owner's ask (2026-10-12): every issue tagged, `intake` on reports of new items.
Inventory: 68 issues on jlevy/squares (pull requests excluded), 53 in
packing/campaign/result-requests.yaml, 15 not (#500, #501, #503 to #506, #521 to #529).
Before: 57 issues had no label; #308, #358, #367, #375, #400, #411, #413, #419, #445
and #472 had `n-17`; #405 had `n-17` and `tracker`. No issue had `intake`. Every
existing label was set by jlevy.

Classes:

- Intake reports, 64: the 45 register `result-report` entries; #295 and #308
  (`defect-report`, but they offer counterexamples, replacement results or a refutation
  the record took in); #358 (`other`, certificates for two n17 classes offered for
  admission); #367 (`other`, the B2 branching method offered for the repository); and
  the 15 unregistered issues, each of which offers results (#523 is also a compute
  request).
- Trackers, 2: #317 (owner's n = 11 umbrella), #405 (n17 tracker).
- Notice, 1: #411 (repositories moved).
- Bug, 1: #445 (verifier memory, fixed by PR452).

Added: `intake` to 64 issues, `n-17` to #494, #495 and #523, and `tracker` to #317. That
is 68 labels on 65 issues. Every label was added after re-reading the issue's live labels.
None was removed. #405, #411 and #445 were left as they were. After the edits, a fresh
listing shows all 68 issues labelled and every planned label present.

Doubtful: #358 and #367 are `other` in the register, but each offers an item for the
record. #367 in particular is a method report. #411's `n-17` is arguable, since the
notice covers ten repositories, two of them n17, but the owner set it. No label looks
wrong.

Change table (scratch copy:
/tmp/claude-0/-home-user-squares/387dc0a2-0a91-51c6-bf71-f69e33945398/scratchpad/labels/changes.md):

| issue | register kind | labels before | added | reason |
| ---: | --- | --- | --- | --- |
| #170 | result-report | none | intake | register kind result-report |
| #227 | result-report | none | intake | register kind result-report |
| #238 | result-report | none | intake | register kind result-report |
| #247 | result-report | none | intake | register kind result-report |
| #256 | result-report | none | intake | register kind result-report |
| #279 | result-report | none | intake | register kind result-report |
| #280 | result-report | none | intake | register kind result-report |
| #281 | result-report | none | intake | register kind result-report |
| #282 | result-report | none | intake | register kind result-report |
| #294 | result-report | none | intake | register kind result-report |
| #295 | defect-report | none | intake | defect report offering counterexamples and replacement results (T-083..T-086) |
| #296 | result-report | none | intake | register kind result-report |
| #308 | defect-report | n-17 | intake | defect report offering a refutation of DS7 Theorem 9's argument |
| #309 | result-report | none | intake | register kind result-report |
| #316 | result-report | none | intake | register kind result-report |
| #317 | correction | none | tracker | owner's umbrella for the n = 11 proof |
| #358 | other | n-17 | intake | certificates for two n17 classes offered for admission |
| #363 | result-report | none | intake | register kind result-report |
| #366 | result-report | none | intake | register kind result-report |
| #367 | other | n-17 | intake | the B2 branching method offered for the repository |
| #368 | result-report | none | intake | register kind result-report |
| #375 | result-report | n-17 | intake | register kind result-report |
| #399 | result-report | none | intake | register kind result-report |
| #400 | result-report | n-17 | intake | register kind result-report |
| #401 | result-report | none | intake | register kind result-report |
| #413 | result-report | n-17 | intake | register kind result-report |
| #414 | result-report | none | intake | register kind result-report |
| #419 | result-report | n-17 | intake | register kind result-report |
| #420 | result-report | none | intake | register kind result-report |
| #422 | result-report | none | intake | register kind result-report |
| #425 | result-report | none | intake | register kind result-report |
| #428 | result-report | none | intake | register kind result-report |
| #432 | result-report | none | intake | register kind result-report |
| #438 | result-report | none | intake | register kind result-report |
| #446 | result-report | none | intake | register kind result-report |
| #451 | result-report | none | intake | register kind result-report |
| #465 | result-report | none | intake | register kind result-report |
| #470 | result-report | none | intake | register kind result-report |
| #471 | result-report | none | intake | register kind result-report |
| #472 | result-report | n-17 | intake | register kind result-report |
| #476 | result-report | none | intake | register kind result-report |
| #481 | result-report | none | intake | register kind result-report |
| #483 | result-report | none | intake | register kind result-report |
| #484 | result-report | none | intake | register kind result-report |
| #485 | result-report | none | intake | register kind result-report |
| #486 | result-report | none | intake | register kind result-report |
| #488 | result-report | none | intake | register kind result-report |
| #489 | result-report | none | intake | register kind result-report |
| #494 | result-report | none | intake,n-17 | register kind result-report |
| #495 | result-report | none | intake,n-17 | register kind result-report |
| #500 | unregistered | none | intake | not in the register; body offers results |
| #501 | unregistered | none | intake | not in the register; body offers results |
| #503 | unregistered | none | intake | not in the register; body offers results |
| #504 | unregistered | none | intake | not in the register; body offers results |
| #505 | unregistered | none | intake | not in the register; body offers results |
| #506 | unregistered | none | intake | not in the register; body offers results |
| #521 | unregistered | none | intake | not in the register; body offers results |
| #522 | unregistered | none | intake | not in the register; body offers results |
| #523 | unregistered | none | intake,n-17 | not in the register; body offers results |
| #524 | unregistered | none | intake | not in the register; body offers results |
| #525 | unregistered | none | intake | not in the register; body offers results |
| #526 | unregistered | none | intake | not in the register; body offers results |
| #527 | unregistered | none | intake | not in the register; body offers results |
| #528 | unregistered | none | intake | not in the register; body offers results |
| #529 | unregistered | none | intake | not in the register; body offers results |

## Runbook and sweep, 2026-10-12

Commit 2660934297f32a1b7f5b0de82e862462173afc3d, pushed as
`claude/wizardly-meitner-wqn4x3-labels` (no PR):

- `devtools.check_requests.compare_github`, shared by `--github` and the intake sweep,
  lists each issue the record holds as `kind: result-report`, open or closed, whose
  live labels lack `intake`. The difference reads "#N is a result report without the
  `intake` label". The sweep lists it as needing action, and its next step is the
  command `gh issue edit N --add-label intake`. For a new issue, the step now also
  says that a result report gets the label.
- `campaign/result-import.md`: a stage 0 bullet ("A report gets the `intake` label"),
  a sentence in the Prompt's step 3, and the Intake Sources and `--github` rows. Stage
  7 and After the Merge are untouched for the parallel comment lane. None of the pushed
  sibling branches (adoption, imports, results-overview) touches these files.
- Tests: `test_the_github_comparison_lists_every_result_report_without_the_intake_label`
  (recorded fetch) and
  `test_a_report_without_the_intake_label_needs_action_and_names_the_command`.

Validation:

- Touched tests: 84 passed. Ruff check and format are clean. BasedPyright on the
  touched files: 0 errors, 0 warnings, 0 notes.
- `packing-validate --edit`: 63 of 65 steps passed. Browser floor failed because this
  worktree had no `node_modules`; after `npm ci`, `--only "browser floor"` passed (2
  steps). The type floor timed out at its 900 s ceiling twice, at a load average of
  about 15 on 4 cpus, with sibling worktrees running their own gates; CI reads 64 to
  112 s. Run directly with no ceiling, the same command over the whole project gives
  0 errors, 0 warnings, 0 notes in 1430 s.
- `packing-validate --records`: 49 steps passed, 232.7 s.
- Live `make intake`: the Kingbird capture succeeded, and the sweep lists no result
  report without the `intake` label. It exits 1 on 22 other items: 15 issues not in the
  record (#500 to #529), 5 owner replies of 12 October not yet recorded, and 2 watched
  repositories (evand, wand125).

## Merge and PR, 2026-10-12

Merged origin/main (#531, 7847cf3d5) into the branch as 8a5e72e65 (merge commit, no
rebase), pushed with a normal push. PR: https://github.com/jlevy/squares/pull/546 (not
merged). Conflicts, each resolved by keeping both rules: `compare_github`'s docstring
(one-line summary, a label paragraph, #531's edited-comment paragraph); the Intake
Sources row; the sweep's module docstring; `test_check_requests.py` (both tests kept;
#531's test gives its issue the `intake` label; the label test adds an edited comment on
the unlabelled #7). The `--github` row now also says "created or edited". The sweep's
label test adds an edited-comment step.

Validation at 8a5e72e65: touched tests 85 passed; Ruff clean; BasedPyright on the four
touched files 0/0/0; `check_requests` exit 0; `--records` exit 0 (49 of 107, 158.7 s);
`--fast` exit 1 at load 13 to 18 on 4 CPUs (8 ceiling timeouts, browser floor without
node_modules, workbench Animate view timing, D-168 time budget); a rerun after `npm ci`
passed the browser floor and the regressions, and the Animate view failed again on
timing (#538). Hosted: all 15 checks that ran passed (run 38229096917). Live `--github`:
29 differences, no report without `intake`.
