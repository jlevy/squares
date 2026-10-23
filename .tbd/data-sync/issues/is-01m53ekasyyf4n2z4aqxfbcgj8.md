---
type: is
id: is-01m53ekasyyf4n2z4aqxfbcgj8
title: "Algebraic house writer: adopt T-174 at 70, 153 and 207 (and T-193's 16 on the stack) once adopt_houses writes an algebraic side (#660 A1)"
kind: task
status: in_progress
priority: 2
version: 8
delegate: c-houses-1023
labels:
  - regularization
  - validation
  - result-import
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T22:51:21.278Z
updated_at: 2026-10-23T18:47:55.164Z
started_at: 2026-10-21T17:42:18.505Z
---
The writer gap the house rule names, and its one code-gap staging (packing/campaign/result-import.md, "The House Rule"): `adopt_houses` writes rational houses only and refuses an algebraic one (`plan`, `rational`). PR #660 stages T-174's algebraic houses at 70, 153 and 207 under this bead as `no writer`. After #658 lands with a T-193 reader, T-193's 16 algebraic houses join them (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302). Opened by #660's addressing pass for its review A1.

## Validation
- Claim: each staged count's algebraic side, the one root of its minimal polynomial in an isolating interval, ordered exactly below its case by `exact_sides`, and confirmed (V3/C3 with an accepted review).
- Run: the code slice first. `adopt_houses` must write an exact form for a root of p in an interval, which `select_houses.parse_case` and `regularize_evand.verified_bound` read back. `upper_bound_houses` must take an algebraic source: PR #574's algebraic facts are already Witness/v2, and T-193's minimal-polynomial forms need deriving. The prose and coverage writers and `--check` need it too. Then the adoption's commands, as on think-3mry, for these counts.
- Cost: 0.6 CPU-h of runs for the three counts on main (3.8 CPU-h for 19 on the stack), at 0.2 CPU-h a count, after the code slice. At an algebraic house the runs are expected to settle the count: no rational view is same or bound at an irrational side, and no number-field view is decided on two routes yet.
- Budget status: gated on a code slice (this bead's), within the 40 CPU-h item cap.
- Possible subset under the cap: not needed.
- Depends on: the writer slice; #658 for the T-193 counts; OR-18's storage reading for T-193's forms (n = 204 is 11.54 MB raw and 3.53 MB stored), and the hosted-witness reader if OR-18 hosts one.
- Done when: the staged algebraic counts are adopted and off `PENDING_ADOPTION`, each regularized or settled in its adoption's pull request.
- Machine note: as for think-3mry.

## Notes

2026-10-21 coord-intake-1021b: ownership transferred to the 21 October intake coordinator (no update since the previous owner's last note; the 19 October machine-transfer handoff #684 and the owner's instruction of 21 October to resume the intake). Triage of the 21 October sweep follows.

2026-10-21 c-triage-sweep-1021b (read-only triage of the 21 October sweep): #658 merged on 19 October and main now stages T-193's 16 algebraic houses under this bead (select_houses.PENDING_ADOPTION, NO_WRITER) beside T-174's 70, 153 and 207; open PR #706 takes 204 off (T-223 is below T-193 there), leaving 18 counts. Nothing outside this bead blocks the writer slice. At eight counts (88, 126, 175, 199, 232, 266, 292, 301) adopt_houses.plan also refuses the house until think-8ido corrects T-193's regularization item (select_houses.CORRECTIONS_OWED); that gate is in code, not a sweep wait. Price: the writer slice (adopt_houses exact algebraic form and witness, upper_bound_houses algebraic source, the prose and coverage writers, --check), then about 0.2 CPU-h a count: 2.0 CPU-h for the ten counts free now (70, 153, 207, 102, 123, 258, 259, 267, 295, 302), 1.6 CPU-h for the eight after think-8ido, all under the 40 CPU-h item cap.
blocked_on: none

2026-10-23 c-houses-1023 (branch claude/intake-2026-10-23-algebraic-houses, draft PR #756 https://github.com/jlevy/squares/pull/756, head bf603b446, main 7335d0098 merged; labels S2, intake):
- Writer: `exact_sides.form`/`read_form` write and read an algebraic side as root(<minimal polynomial in s>, <low>, <high>) at 40 places, in both lanes; rational houses byte-identical. Number-field houses come from derived facts and receipts (`algebraic_witness_reports derive-forms`; `upper_bound_houses.FIELD_COUNTS`).
- Adopted: T-174 at 70, 153 and 207; T-193 at 102, 123, 258, 259, 295 and 302. Each is off PENDING_ADOPTION. Custody passed: 70 houses, 197 inputs, 42 mutations refused.
- Still staged here: 267, priced at about 6 CPU-h for its three field jobs plus about 2 CPU-h per atlas rebuild and not run (coordinator's decision), and 88, 126, 175, 199, 232, 266, 292 and 301, waiting on think-8ido and the owner's Q2.
- Regularized: grid-slack at 0.5, 1 and 5 degrees (no frame on a number-field witness) and Evan Daniel's driver, twice; the 258/259/302 rerun used --timeout 2400. At 102, 123, 153, 207, 258, 259 and 302 every view is a rational side 1.06e-19 to 1.79e-19 above U, and none is drawn. Per the owner's Q13 answer (think-r8cn), each count draws its exact house, as SETTLED decided-no-better with owed = think-mbdw. 70 and 295 read regular as published. Evidence is under packing/cases/regularized_drawings/think-ot5c-2026-10-23/. Compute about 1.5 CPU-h in all.
- Release: DATA_REVISION re-pinned. A no-public-change record for the four papers, from renders at fb0889e2 against main 7335d0098, twice each, with 69 files byte-identical.
- Blocker: the nine atlas/regularized/n-*.svg URLs the builder no longer declares fail `site_urls --check --history-ref origin/main`, in the records tier and test_site_urls. Every disposition is site code, so the decision went to think-yezl (decision, under think-ezt8) for the site lane.
- Not done: stamp_landed (#736 not merging), and the second exact route for number-field views (think-mbdw).

2026-10-23 c-houses-1023, update: PR #756 head 578cb8ed3, with main 7cd0a94bf merged (#752, #751, #748, #746 and #747 merged along the way; DATA_REVISION re-pinned after each). Hosted CI found follow-ons, and each is fixed:
- the reader tables did not know the written root form (`render_research_tables.ROOT_FORM`);
- the sweeps checkout lacked T-193's packet;
- the chunk census, taxonomy and evidence profile, SCREEN_FINDINGS, the rigidity blocks, the composite figure and PR 574's frozen algebraic claims were stale;
- the integrity-ceremony ratchet flagged a digest comparison;
- about 20 tests pinned 70 or the earlier houses.
At 5bcd728e5 every hosted job passes except validate, overview, suite-c and pages-required, and those fail only on the nine atlas/regularized/n-*.svg addresses (think-yezl, the site lane's decision). The papers' no-change record has been re-measured five times, last against cc91ee1b8, with 69 files byte-identical each time.
