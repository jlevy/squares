---
type: is
id: is-01m5ndgfnpr93ktyy1ayc60vtb
title: "PR #756 (merge): senior review, address, gate"
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-rev-756-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5nrt62q564tpf7pwvr3wkv5
  - is-01m5nzjjyj7axr5vb1gvk4xwh9
hold: null
hold_until: null
created_at: 2026-10-23T22:18:39.157Z
updated_at: 2026-10-24T03:34:22.415Z
started_at: 2026-10-24T01:05:25.282Z
---

## Notes

2026-10-24 c-rev-756-1024 (senior review, letter A, round 1, of PR #756 at head 7bc4cae1199270d13b11a6a415087650bd6aafcc, merge base 64b316b6cc8f):
- Review A posted as a PR comment: https://github.com/jlevy/squares/pull/756#issuecomment-6378226088 (marker `<!-- tbd:review v=1 id=A kind=senior pr=756 round=1 head=7bc4cae1199270d13b11a6a415087650bd6aafcc base=64b316b6cc8fa31177824e20733853708b996fb5 -->`).
- Verdict: changes requested before merge, for A1 only. The reviewed diff is sound: exact on every deciding path but A2's latent one; all nine adoptions verified (smallest eligible side, root form equals witness side exactly, `packing-witness verify` passes on all nine); Q13 applied as stated; #761's design followed; tests are real updates; no visual/template/CSS/browser-script change.
- Findings: A1 High (conflicts with main 0bbb0a2c4 in 14 files after #753 and #754 merged; merge, regenerate, re-run the house checks and records tier, follow-up review). Medium: A2 (check_standing decides equality with an algebraic house from a 1e-60 enclosure), A3 (think-mbdw's scope and done-when do not cover the owed regularization; its Q13 alternative is already met), A4 (decided-no-better misstates the seven counts in the owner's terms), A5 (case records call T-193's exact solve a regularization), A6 (compare_evand_regularization refused-tilts exits 2 on the committed index; test changed to expect it), A7 (the regularized-address question lost its owner when think-yezl closed). Low: A8-A12. Suggestions: A13, A14.
- Dedicated review recommended: correctness, on A1's merge commit. Security and performance not warranted.
- Tests (7bc4cae11, 2 workers, nice 2): the six house checks pass; pytest 527 + 149 + 3 passed; packing-witness verify 9/9.
