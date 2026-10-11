---
type: is
id: is-01m3q3346jb4mfsg5c35w99eyw
title: Replay and reconcile all 12028 T-059 rows
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m3yrzkz80qd1wv5sjr0kkkv0
created_at: 2026-09-29T17:23:40.881Z
updated_at: 2026-10-02T17:01:22.247Z
---
After strict receipt admission and measured cost estimate, replay all row minima and witnesses with exact unique 0..12027 census. Preserve incomplete output honestly and do not equate this with the separate global counting proof.

## To finish (validation backlog, 2026-10-02)

T-059 (wand125's equality of all 12,028 n11 row minima, V0/C1). Blocked by think-pgrx (journal admission headroom). From packing/: `python -m devtools.check_general_pose_tree_census run resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full.jsonl 0-12027 --checker <clean checkout of wand125/square-packing-tools at 0d33ab61726c2ab03e3eb8f457dabaf22db8571f> --certificate-dir resources/web/external-square-certificates-2026-09-22/kleddamag-11 --leaf 10 --max-seconds 18000`, then the same journal with `--require-complete`; retain the summary only after exit 0 (COMPLETE_ROW_EQUALITY). Expected CPU: 9,446 CPU-seconds at the source, one uninterrupted process. Refutes: any row minimum or witness differing from Kleddamag's recorded minima, or a global minimum other than 999962528. Moves the rung: the complete census recorded as an exact-algebraic replayed-here entry derives V3/C3. Run `uv run --frozen --all-extras --group dev python -m devtools.check_results`.

## Notes

Session164 Sol read-only feasibility: existing reviewed wrapper can run0-12027 without new mathematics or producer changes, but serially in one uninterrupted isolated subprocess. No wrapper resume/sharding/merge: requested_rows is bound into identity and final output must be fresh. Timeout retains a bound PARTIAL journal(exit3), refusal exit2, complete census/equalities/exact witness attainment exit0 COMPLETE_ROW_EQUALITY. Required finite whole-process max-seconds; no per-row timeout. 64MiB inputs/journal read ceiling,2MiB source ceiling. Source-reported9446CPU-seconds is the only full-run cost evidence; 3sample row times0.5964/0.6371/0.8216s are nonrepresentative. Suggested18000s ceiling is scheduling allowance, not measured runtime. Full journal cannot fit current~480KiB mutation-snapshot headroom (mandatory fields alone exceed1.2MiB); design/test retained evidence handling first. Pinned checkout clean0d33ab61726c2ab03e3eb8f457dabaf22db8571f; cert3296630B/ref1348749B match pins. No full run started. From packing with external env: python -m devtools.check_general_pose_tree_census run resources/web/wand125-tools-2026-09-29/receipts/n11-bound-full.jsonl 0-12027 --checker /Volumes/spud-ext1/agent-scratch/wand125-tools-01a0ebfc/upstream --certificate-dir resources/web/external-square-certificates-2026-09-22/kleddamag-11 --leaf 10 --max-seconds 18000. Then validate same journal/checker/certificate-dir with --require-complete; retain complete summary only after exit0. This is row-equality replay, not a new global packing proof.

2026-09-29 upstream integration: wand125 provisional T-056/T-057 map to canonical T-058/T-059. Published Couzo/de Winter retain T-056/T-057. Historical notes and archived receipts retain their original labels; no evidence bytes or acceptance level changed.
