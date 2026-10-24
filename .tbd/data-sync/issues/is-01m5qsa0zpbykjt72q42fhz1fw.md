---
type: is
id: is-01m5qsa0zpbykjt72q42fhz1fw
title: "Import #797: Kevin Fang's c*(k) < 4√(2k)+1 for every k ≥ 6 (squarepack-certs theorem-a at b1b3f6b)"
kind: task
status: in_progress
priority: 2
version: 6
delegate: c-import-797-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T20:23:19.286Z
updated_at: 2026-10-24T20:58:20.530Z
started_at: 2026-10-24T20:24:12.105Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/797 (TheSnakeFang, 18:52:48Z): for every k >= 6, k^2 - ceil(sqrt(32k)) - 1 unit squares fit in a square of side < k, so c*(k) < 4 sqrt(2k) + 1. Ryu's L packing (Theorem 1.3) with filled band ends, b the odd integer nearest sqrt(2k); a 5-page note. Source TheSnakeFang/squarepack-certs@b1b3f6b theorem-a/ (note PDF+TeX, lband.py exact construction, windowed_check.py, certificates k=6..40 and 101, SHA-256 for k=300 and 600 with regenerate.sh). The repository head db1ed62 (3 commits past the last read) adds note v0.2 crediting Evan Daniel's earlier bound (doi:10.5281/zenodo.23624565): read for priority and credit. Bears on the deficiency rows (Ryu's Theorems 1.2-1.4, T-163). Stage 0 owner; stage 1 triage is read-only first. Source claims are unverified.

## Notes

2026-10-24 stage 1 triage (c-triage-797-1024, read-only, main 84d4a75af).
Pin: squarepack-certs db1ed6220731fce432fa3b1ef3b994b5ab6c3663 (head; theorem-a code/certs byte-identical to b1b3f6b; note v0.2 = Zenodo 10.5281/zenodo.23624565, v0.1 = 23624412 = note at 31bdc2d). Correction: 23624565 is Fang's own v0.2, not Daniel's; Daniel's bound is evand/square-packing 4b456fe/aa12b98 (pushed 2026-10-18T15:47:56Z), held by think-f8py (stalled in_progress since 10-19), not registered.
Claim map: theorem-a -> new reported row in asymptotic-waste-bounds deficiency_upper_bounds (no T-NNN; settles no n <= 324, #471 precedent); 36 certificates -> retained + replayed, no rows (every count <= 1024 already below k in the record); optimized constructions -> prose only, not registered.
Checked: independent exact re-implementation from the note: bound holds k=6..60000 (both b at ties), Lemma 2 and B(k) hold; full geometry valid k=6..40,101; controls refused k=6..30; least slack 8019401/78023840599 at k=19705 reproduced; all comparison claims hold exactly (Ryu 1.2/1.3/1.4/1.6, T-163, Daniel counts 495210/255215/249568).
Consequence: adding the row forces deficiency_family Statement + T-163 assessment recompute ([15,41]; with Daniel [15,34]u[36,39]).
Price: cert replay 15-45 CPU-min (36 shipped); k=300/600 1-2 CPU-h, recommend skip; stage 4 review tbd-strong-max ~150-250k tokens; maintained module W7 ~100-150k tokens.
Drafts: scratchpad triage-797/ result-requests-797.yaml, import-plan-797.md, acknowledgement-797.md, intake-watch-squarepack-certs.yaml (schemas validate).

2026-10-24 coord-intake-1024 on c-triage-797-1024's report: decided by stated rules, not owner questions. (1) Theorem A gets its own reported row in deficiency_upper_bounds, credited after Daniel (his c*(k) <= 4 ceil(sqrt(2k-7)) - 1, 4b456fe, pushed 2026-10-18T15:47:56Z, came first; the axis-row fill is his; neither bound dominates per k). (2) Daniel's row (think-f8py, stalled since 19 Oct) lands in the same change. (3) T-163's assessment is recomputed as the deficiency gate requires. (4) k = 300 and 600: author's hashes only; the 36 shipped certificates replayed. (5) Theorem A's construction check promoted to a maintained module (OR-1). Lane c-import-797-1024, worktree wt-797, branch claude/intake-2026-10-24-deficiency-797. Fang's stage 4 note review follows in its own lane once the PR is open. Correction: doi 10.5281/zenodo.23624565 is Fang's note v0.2, not Daniel's bound.
