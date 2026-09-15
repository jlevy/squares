---
type: is
id: is-01m2gxxqtm13wn0rk7a4aj0dtr
title: "PR 160 defects: dead repair option, aborting probe, mislabelled best-of-k"
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-14T21:42:13.072Z
updated_at: 2026-09-15T02:59:27.491Z
closed_at: 2026-09-15T02:59:27.490Z
close_reason: "All items fixed on PR #160 by lane C: D07 ec0a0604, D09 78c338be, D08 fbc74c0e, D39 158af9d5, D38 and D37 acae83c6, D40 5d5760cd."
resolution: null
duplicate_of: null
---
Defects on PR #160 found by the 2026-09-14 audit. All fail safe or mislabel, and none ranks an invalid state:

- **The Search panel's repair option can never run.** `src/api/search-api.ts:81` sets repair tolerance 1e-8, and `search/pack-runner.ts:307-309` throws above 1e-9 when the plan is validated (verified). `search-api.test.ts` only uses `repair: false`.
- **A malformed or non-finite probe result aborts the run** instead of counting a refusal: `trial_from_probe` raises (`trial_records.py:396-418`).
- **Best-of-k is labelled "first k seeds" but uses the first k admitted trials** (`benchmark.py:282-291`), and the tolerance rates divide by admitted trials without saying so (`:265-269`). `sweep()` can report best-of-k over fewer than k trials (`:431-435`).
- **Three validity rules and no parity fixture**: probe SAT plus Python at 1e-5 deepest pair, TypeScript `assessPackingSnapshot` / `resolvePacking` at 1e-9, and the gap bar's summed 1e-4. A state the benchmark admits can be invalid in Pack or Search. This belongs to think-nals, noted here so the audit reads whole.
- **The Search panel shows only status counts**: no validity counts, work or block distribution, and `summarizeSearch` is unused (against the plan's gate D).

## Notes

2026-09-14, PR #160 review lane C: every item is fixed on #160. Validity rules unified into one contract with a shared fixture: D07 (ec0a0604) and D09 (78c338be). Benchmark admission refuses below-record, non-converged repairs and unresolvable success bands: D08 (fbc74c0e), which is the reopened work behind closed think-1fpa's contradicted done-when. Dead repair option: D39 (158af9d5). Aborting probe: D38, and mislabelled best-of-k and rates: D37 (acae83c6). Status counts only: D40 (5d5760cd).
