---
type: is
id: is-01m4d2npx6prwa4weh47b2wskm
title: A7 Retain homepage fragment destinations for registered withdrawn results
kind: bug
status: closed
priority: 1
version: 4
assignee: codex
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T06:19:38.789Z
updated_at: 2026-10-08T13:09:30.794Z
started_at: 2026-10-08T06:19:59.250Z
closed_at: 2026-10-08T13:09:30.794Z
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
Independent Astra review found that the known-only homepage result-fragment guard excludes withdrawn T-117 and T-118 although their permanent URL registry tombstones are retained. Derive exact retired aliases from the registry and route those old homepage fragments, including encoded forms and actual link clicks, to the explanatory tombstones. Keep live-result query filtering and unknown-ID refusal, with no numeric-range guesses or primary content fetch.
