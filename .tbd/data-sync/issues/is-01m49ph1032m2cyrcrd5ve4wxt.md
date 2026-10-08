---
type: is
id: is-01m49ph1032m2cyrcrd5ve4wxt
title: "A1: site_urls registry derived from builder declarations, site-urls.yaml and docs/project/site-urls.md with --check"
kind: task
status: closed
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-10-06-site-urls-seo-performance.md
delegate: codex-pr395-site-review
labels:
  - pages
dependencies:
  - type: blocks
    target: is-01m49ph1mprzwjqxe2r959cvbz
  - type: blocks
    target: is-01m49ph2b8x80wccsyns6728zn
  - type: blocks
    target: is-01m49ph30g3ssvdg6jj3rrttbx
  - type: blocks
    target: is-01m49ph3nezcsjef7cq236g2vh
  - type: blocks
    target: is-01m49ph4bew4jd47e14xrehgy2
  - type: blocks
    target: is-01m49ph51jh1cry2pt12e3gkaa
parent_id: is-01m49ph0abvy6j16zcq4jse39y
hold: null
hold_until: null
created_at: 2026-10-06T22:49:39.075Z
updated_at: 2026-10-08T13:09:30.508Z
started_at: 2026-10-06T22:54:02.736Z
closed_at: 2026-10-08T13:09:30.507Z
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
Lane A. New packing/devtools/site_urls.py; rows: path, kind, canonical, generator, first_published, status; hashed assets one pattern row; permanence rules for cases/{n}.html and result/t-{nnn}.html; replaces over-claiming SITE_PAGES docstring. Spec: Principle 2.
