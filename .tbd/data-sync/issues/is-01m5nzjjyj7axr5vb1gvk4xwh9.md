---
type: is
id: is-01m5nzjjyj7axr5vb1gvk4xwh9
title: "PR #756 follow-up review B with a correctness review of merge commit 474409acf"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-rev-756b-1024
labels: []
dependencies: []
parent_id: is-01m5ndgfnpr93ktyy1ayc60vtb
hold: null
hold_until: null
created_at: 2026-10-24T03:34:22.415Z
updated_at: 2026-10-24T04:19:09.373Z
started_at: 2026-10-24T03:34:32.874Z
---

## Notes

2026-10-24 c-rev-756b-1024 (follow-up review, letter B, round 2, of PR #756 at head 87f95620c84d27f19c0cb4e21d1ccd606b319624, merge base 14b14f2d192bc99aedf8bd13fb2311c2f6b565c1; follows review A at 7bc4cae11 and its dispositions):
- Review B posted as a PR comment: https://github.com/jlevy/squares/pull/756#issuecomment-6379772274 (marker `<!-- tbd:review v=1 id=B kind=follow-up pr=756 round=2 head=87f95620c84d27f19c0cb4e21d1ccd606b319624 base=14b14f2d192bc99aedf8bd13fb2311c2f6b565c1 -->`).
- Verdict: approve with one Medium finding (B1); nothing in the merges blocks merge.
- Correctness review of merge 474409acf (main 0bbb0a2c4): correct. ADOPTED, LATER_PASSES, OVERTAKEN, ALGEBRAIC_ADOPTED, results.yaml, source-coverage.yaml, occurrences.yaml, the custody receipt and eight generated JSON files all equal their three-way expectation; T-231 at 204 intact. Regenerated in a scratch checkout of the merge and compared, with no difference: a fresh custody (70 houses, 201 inputs, 44 mutations), the escape screen at the ten moved counts (byte-identical, totals = SCREEN_FINDINGS), and contributor_census --reconcile (YAML-equal). Generator checks (RESULTS, research tables, family and contact-shade censuses, bound citations, composite figure, regularized drawings, flip regularization) and house checks (select, adopt, default_drawings --check and --check-state, upper_bound_houses check --n 204 295) pass; records tier passes but for the bead tree and lint (skipped) and render_changelog against today's origin/main (passes against 0bbb0a2c4). Second merge 87f95620c (main 14b14f2d1): no conflicts, no record change.
- Dispositions: A1-A4, A6, A8-A12, A14 hold; A7's deferral holds (think-tng3 open); A13 declined but a bead was opened; A5 holds at the six T-193 counts but not at 153 and 207 (B1).
- Findings: B1 Medium (153 and 207 case records call T-174's certificate refinement "its source's regularization", then say "the drawing is not regularized", under the card label "Regularization"); B2 Low (root_side docstring stale after A14's closed form); B3 Low (PR body results table: custody 197/42 and 1388 rows stale; now 201/44 and 1389). Suggestion B4 (gate step name omits the owed state).
- Question 3 (303): nothing needed in #756; SETTLED[303] is main's, byte-identical at head. Whichever of #756/#757 lands second needs a merge checked like 474409acf (33 shared files).
- Tests at 87f95620c (2 workers, nice 2): the generator and house checks pass; refused-tilts exits 0 with 259 held; build_witness passes on all nine algebraic houses and 204 under A9's exact equality; reviewer probes for A2, A4, A6, A8, A14 hold; pytest -n 2 over ten files: 419 passed, 1 failed (browser test test_an_atlas_cell_opens_the_same_record timed out under load; passed alone).
