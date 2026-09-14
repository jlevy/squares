---
type: is
id: is-01m2gxxqtm13wn0rk7a4aj0dtr
title: "PR 160 defects: dead repair option, aborting probe, mislabelled best-of-k"
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:13.072Z
updated_at: 2026-09-14T21:42:39.327Z
---
Defects on PR #160 found by the 2026-09-14 audit. All fail safe or mislabel, and none ranks an invalid state:

- **The Search panel's repair option can never run.** `src/api/search-api.ts:81` sets repair tolerance 1e-8, and `search/pack-runner.ts:307-309` throws above 1e-9 when the plan is validated (verified). `search-api.test.ts` only uses `repair: false`.
- **A malformed or non-finite probe result aborts the run** instead of counting a refusal: `trial_from_probe` raises (`trial_records.py:396-418`).
- **Best-of-k is labelled "first k seeds" but uses the first k admitted trials** (`benchmark.py:282-291`), and the tolerance rates divide by admitted trials without saying so (`:265-269`). `sweep()` can report best-of-k over fewer than k trials (`:431-435`).
- **Three validity rules and no parity fixture**: probe SAT plus Python at 1e-5 deepest pair, TypeScript `assessPackingSnapshot` / `resolvePacking` at 1e-9, and the gap bar's summed 1e-4. A state the benchmark admits can be invalid in Pack or Search. This belongs to think-nals, noted here so the audit reads whole.
- **The Search panel shows only status counts**: no validity counts, work or block distribution, and `summarizeSearch` is unused (against the plan's gate D).
