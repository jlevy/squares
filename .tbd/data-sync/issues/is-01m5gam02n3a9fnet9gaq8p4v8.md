---
type: is
id: is-01m5gam02n3a9fnet9gaq8p4v8
title: "Owner decisions for #715 (and #666): counts above 1024, recipe-only rows, 335, hosting the bulk certificates"
kind: task
status: in_progress
priority: 1
version: 3
delegate: coord-intake-1021b
labels:
  - result-import
  - decision
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T22:51:56.373Z
updated_at: 2026-10-22T13:13:20.757Z
started_at: 2026-10-21T22:51:57.158Z
---
From the read-only triage of #715 (c-triage-715; full text: policy.md in the coordinator scratchpad triage-715/). No rule sets a ceiling above the n <= 324 horizon or mentions 1024, but the record holds nothing above 998, and #666's eight counts above 1024 wait on the same question.
D1. Track counts above 1024? Recommended: yes, no ceiling, rows recorded as reported (one answer covers #666).
D2. Do L-border/tiling rows with no certificate file of their own become rows? Recommended: yes, decided exactly from the recipe by a maintained checker; write the rule into the frontier README (4e4c8ce's deletion bounds wait on it too).
D3. Name a key reason to record 335 (#715's certificate is 1.84e-11 above Couzo's own 8 Oct decimal row)? Recommended: no; check the 8 Oct decimal poses exactly first; if they fail, propose a deferred-conflict correction.
D4. Host the certificates above 1024 (25-89 MB as Git stores them; OR-18)? Recommended: yes, a hosted-data manifest staged in the stage 2 PR; the owner publishes data/couzo-715-certificates-v1.
D5 (already open on #686): per-row credit beyond the horizon.
blocked_on: none

## Notes

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/residue-held.tsv).

**D2 also reaches below 1024.** The report-order walk of Couzo's history at 325 to 1024
holds 64 recipe bounds that no certificate file of their count stated when they were
published:

- `23aff0c`'s `upper_bounds.json`: 46 L-border and tiling constructions;
- Kevin Fang's `composites/table.csv` at `bef5c42` ("reproducible-only"): 17;
- `487b058`'s index: 1, at 327.

**Proposed D6.** Do index deletion bounds become rows? They are the bounds an index states
by deleting squares from the next count's certificate. There are 54 (`4e4c8ce` 39,
`23aff0c` 15); this is `think-yfoo`'s #627 C1 question.

- The runbook's claim table: "a consequence of another claim, such as monotonicity, at a
  count where the record holds no such value: its own entry only when it settles a case;
  otherwise the parent's scope covers it."
- Recommended: no rows, except where an issue claims the count, as #675 did at 992 and 995
  and #715 does at 743 and 985.

**D1.** Couzo's `5a299b4` index states 5,078 non-grid bounds above 1024: 282 certificates
and 4,796 constructions. #715 claims 1,112 of those counts. The certificate files cover
139 counts.
