---
type: is
id: is-01m4czyzvb518ndgqv1bvjnp5t
title: "PR #395 E6: verify paper publication against real sparse producer outputs"
kind: bug
status: closed
priority: 1
version: 4
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T05:32:17.130Z
updated_at: 2026-10-08T13:09:30.755Z
started_at: 2026-10-08T05:32:34.724Z
closed_at: 2026-10-08T13:09:30.755Z
close_reason: |
  Completed the covered PR395 source implementation and review scope at 9700cef526a3bcb22d35504c498e23006b910635 against e74a82190302a576e312a9daf2780626971454a2. All174 changed paths accounted; all30 A–E findings addressed by four pinned formal technical reviews and five public disposition replies. Packing37776513680, Pages37776513669 and full37776676917 terminal SUCCESS:105/105 unique selections, all11 mandatory jobs/all10 scientific jobs/all3 exhaustive shards; unchanged strict12-second and browser budgets pass;5305 publication checks, all5 producers/all3 PDFs and20 rendered+20 static contexts pass. No live-deployment or owner Search Console claim: merge confirmation remains required and actual served-site verification follows merge.
  reviews B: https://github.com/jlevy/squares/pull/395#pullrequestreview-5457000213
  reviews C: https://github.com/jlevy/squares/pull/395#pullrequestreview-5457000502
  reviews D: https://github.com/jlevy/squares/pull/395#pullrequestreview-5457000871
  reviews E: https://github.com/jlevy/squares/pull/395#pullrequestreview-5457001109
  dispositions A: https://github.com/jlevy/squares/pull/395#issuecomment-6060495212
  dispositions B: https://github.com/jlevy/squares/pull/395#issuecomment-6060495552
  dispositions C: https://github.com/jlevy/squares/pull/395#issuecomment-6060495995
  dispositions D: https://github.com/jlevy/squares/pull/395#issuecomment-6060496417
  dispositions E: https://github.com/jlevy/squares/pull/395#issuecomment-6060496706
  CI: https://github.com/jlevy/squares/actions/runs/37776676917
resolution: null
duplicate_of: null
---
Hosted optimality job publication fixtures cross-build threshold from a sparse checkout missing its PROOF.md, and shared prepared-math plus paper CSS are rejected as multiple asset roots. Repair real producer/fixture boundaries without skipping checks, and test supported shared-asset external/inline round trips strictly. Run 37732462251 optimality job 113164599987.
