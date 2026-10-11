---
type: is
id: is-01m4mdbdkx61v53br8cp4cmght
title: "Register: a typed regularizations field on result records, T-146 the first (PR #487)"
kind: task
status: closed
priority: 1
version: 5
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T02:40:56.957Z
updated_at: 2026-10-11T04:47:04.827Z
closed_at: 2026-10-11T04:47:04.826Z
close_reason: "Merged in PR #487 (c6bf2d46f): typed regularizations on register entries, T-146 the first"
resolution: null
duplicate_of: null
---
The owner's 2026-10-11 decision (epic think-cdud, items 2 and 3): an optional per-count regularizations list in packing/frontier/results.schema.yaml with n, of, by, method, side (same|solved), changes and identity (basis source-claim|measured, with measurements); a check_results rule set (n in scope and once; of exists, is not the entry, covers n, dated no later; by among attribution.source_keys or project only without attribution; non-negative numbers; measured needs a measurement); the CREDITED map of devtools/check_half_angle_area.py replaced by a read of the register; RESULTS.md and result pages print each item; docs in epistemics.md (Results by Others), packing/frontier/README.md and result-import.md stage 3. T-146 carries 15 items: of T-125 (Ryan Xu, #432) at 70, 102, 123, 129, 146, 295; T-138 (Mishapolk's refinement) at 103 and 258; T-136 (SQUISH #481) at 153, 236, 263, 269, 292, 302, 303; by [Daniel regularized lists 2026-10-10]; side solved; identity basis source-claim with the stage 4 review's measurements. Done with T-146's stage 4 exit (think-8k76) on claude/determined-rubin-yjfy2a by a records lane started 2026-10-11.

## Notes

2026-10-11, records lane (done on claude/determined-rubin-yjfy2a, not pushed): commit
8e5922560 "register: typed regularizations, and T-146's stage 4 exit at V3/C3", then
aeb8a7219 re-pins DATA_REVISION.

- Schema: optional `regularizations` on result entries in
  packing/frontier/results.schema.yaml (n, of, by, method, side same|solved, changes
  {merged_rotation_groups_deg, straightened, re_angled}, identity {basis
  source-claim|measured, measured_in, one_to_one, moved, max_move, max_turn_deg}),
  additionalProperties false, contract still ResultsRegister/v1. `measured_in` sits
  inside `identity`, beside the measurements it sources; `re_angled` was needed for
  T-146's data (302: 26 free angles moved).
- Checker: devtools.check_results.regularizations_problems, wired in main(): n in the
  entry's scope and once; `of` registered, not the entry, holding n, dated no later
  (result_date, as superseded_by); `by` among attribution.source_keys, or `project` only
  without attribution; counts and measurements numbers >= 0 (counts whole), moved <= n,
  measured_in a repository file, a measured identity with one measurement. Tests in
  tests/test_results_register.py (positive, each refusal, gate failure, live T-146,
  schema refusals, RESULTS.md sentence).
- Consumer: check_half_angle_area.regularized_credit() reads `of` per n from the
  register entry citing the import's packet; the regularized half of CREDITED is gone
  (and the unused T-137 reader); credited() serves both.
- Views: RESULTS.md "Regularizations" section and a "Regularizations" row in the site's
  result head (overview_data.Result.regularizations), both from
  result_credit.regularization_sentence.
- Docs: epistemics.md (Parallel Projects and Their Credit bullet; frontier table row),
  packing/frontier/README.md (Adding or Reviewing a Result), result-import.md stage 3
  (sixth rule).
- T-146 carries the 15 items. `changes` come from the source's JSON angle_changes, read
  as the review read them (sums of free-angle counts; a move to 0 is a straightening):
  beyond the review's narrative, they record 14 straightened at 263 and 4 at 269 and the
  free-angle moves of the fewest views. Measurements are the review's; turn angles are
  asin of the third route's exact largest sine where nearest centres pair one to one,
  and the review's binary64 values at 123, 129 and 292.
- The atlas follow-up is think-k35c (not filed again).
