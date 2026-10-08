---
type: is
id: is-01m4de1sqb9njw6m6j9n0e3tp2
title: Recover PR435 workflow triggers from stale GitHub merge reference
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T09:38:29.226Z
updated_at: 2026-10-08T10:55:29.994Z
started_at: 2026-10-08T09:40:34.259Z
closed_at: 2026-10-08T10:55:29.994Z
close_reason: Delivered and independently reviewed in PR435 at a0ca6346; automatic PR checks pass (31 passes, 26 intentional skips). Complete-checkpoint timing failures remain explicitly open under think-kyzi, with census/shard children think-z8cv and think-lyuh; no complete-gate pass is claimed.
resolution: null
duplicate_of: null
---
After native stack444 was linked, PR435 head advanced to a0ca63461 while refs/pull/435/merge remained c0ee1f82 with parents d948311d8 and old a910a0e6. Automatic Packing/Pages/Deferred checks were absent after both synchronize and a close/reopen refresh; push mergeability and exact-head full dispatch work. This matches the symptom reported in github/gh-stack issue319, without establishing the service cause. Recover the current merge reference through reversible stack metadata repair, preserve both branch heads and requested base, and require final PR-triggered plus full validation. Retain diagnostics outside disposable scratch.

## Notes

Delivery update, 2026-10-08:

Reversible metadata repair recovered PR435's current merge reference without changing the requested base d948311d8335d48245da02dd5509ed76813c2e9b or final head a0ca63461d33c7dc2e12f4d08c9af6008aa1ba20. Stack 444 was dissolved for recovery, then formal stack 447 linked PR403 → PR435 with the original branches. Current merge ref b431231478970196d44a0c649766701de6846387 has exactly those two parents. Recovered initial PR runs were canceled by ordinary concurrency supersession when stack membership was restored; replacement Packing37758273623 and Pages37758273635 pass. Final watch reports 31 passes, 26 intentional skips, no failures/pending; mergeability37756690133 passes. Attempt 2 also failed on per-test wall limits: the census-ledger control took 14.63 seconds and the ten-shard residue control 12.71 seconds, each against 12 seconds. The earlier overview-fragment failure was absent; no functional failure class was reported. Gate wall was 1771.02 seconds within 3600 seconds and attempt running elapsed was 1903 seconds. Final run counts are eleven reused passes, two failures (main gate and dependent aggregate), and ten intentional skips. Both attempts are preserved; no further unchanged-head reruns were performed. Full-checkpoint timing remains unresolved under think-kyzi.. Compact current-reference/membership/repair and canceled-run evidence is retained outside scratch. The stale-reference symptom matches upstream gh-stack issue319; exact service cause is not established. No merge or branch deletion was performed.
