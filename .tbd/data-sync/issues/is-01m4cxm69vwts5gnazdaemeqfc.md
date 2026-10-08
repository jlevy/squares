---
type: is
id: is-01m4cxm69vwts5gnazdaemeqfc
title: Preserve offline case alias navigation through the real static page
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-site-urls-seo-performance.md
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m49ph0abvy6j16zcq4jse39y
hold: null
hold_until: null
created_at: 2026-10-08T04:51:26.138Z
updated_at: 2026-10-08T13:09:30.657Z
started_at: 2026-10-08T04:52:44.246Z
closed_at: 2026-10-08T13:09:30.657Z
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
PR #395 old cases.html forwarder sends file:// readers to cases/ directory listing after the move to canonical directory URLs. Preserve registered HTTP canonical identity cases/, provide an actual cases/index.html fallback for offline and no-script readers, verify actual case content rather than directory arrival, and preserve supported query/fragment selectors without weakening invalid-selector handling.
