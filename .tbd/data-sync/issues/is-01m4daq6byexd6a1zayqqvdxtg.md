---
type: is
id: is-01m4daq6byexd6a1zayqqvdxtg
title: Synchronize case popover collapsed state with native close
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T08:40:15.998Z
updated_at: 2026-10-08T10:55:29.986Z
started_at: 2026-10-08T08:42:25.348Z
closed_at: 2026-10-08T10:55:29.985Z
close_reason: Delivered and independently reviewed in PR435 at a0ca6346; automatic PR checks pass (31 passes, 26 intentional skips). Complete-checkpoint timing failures remain explicitly open under think-kyzi, with census/shard children think-z8cv and think-lyuh; no complete-gate pass is claimed.
resolution: null
duplicate_of: null
---
Final full CI37748134343 at a910a0e6 failed one browser contract: after Escape hides #pop-case, a frontier row still has aria-expanded=true. All 3243 other shard-C tests and every deep research/portability job passed. Diagnose native beforetoggle versus queued toggle state/focus handling, correct the source behavior without sleeps or weaker assertions, and add a deterministic regression covering closure and pending fetch invalidation. Preserve source focus semantics and rapid close/reopen behavior. Coordinator owns bead mutations, commits, source pinning, PR updates and final validation.

## Notes

Full checkpoint37748134343 at a910a0e6 completed with eleven deep/portability jobs passing, ten intentional skips, and one actual main-gate failure plus its dependent aggregate. Only fast behavioral shard C failed: test_a_frontier_row_opens_its_record_and_steps_to_the_next observes an invisible native popover with one aria-expanded=true row (3,243 other tests passed). Gate wall1371.41 s; full run1505 s. Complete failed log and compact timing/summary receipts are retained outside scratch. Claimed child think-gtyf covers a source fix and deterministic close-state regression; moderate browser worker owns the disjoint JS/tests/probe and Astra independently reviews event ordering, focus and request lifecycle. Ordinary row reopening already invalidates older requests; no second normal-row stale-fetch production defect is claimed. All earlier automatic PR checks remain passed at that head, and the corrected source head will receive fresh automatic/full validation.

Delivery update, 2026-10-08:

Native close correction is delivered at a0ca63461d33c7dc2e12f4d08c9af6008aa1ba20. A deterministic native-hide/same-task ARIA regression failed before the fix. beforetoggle(closed) now synchronously collapses rows, advances the request epoch and clears pending state; queued focus restoration respects cached reopening and outside focus. All 17 required Chromium case-record controls pass in 41.34 seconds, scoped source/probe lint and types pass, and independent Astra queued-event review has no unresolved finding. The independent event proof and red/green logs are retained outside scratch. Final automatic Packing/Pages/mergeability checks pass (31 contexts, 26 intentional skips). Attempt 2 also failed on per-test wall limits: the census-ledger control took 14.63 seconds and the ten-shard residue control 12.71 seconds, each against 12 seconds. The earlier overview-fragment failure was absent; no functional failure class was reported. Gate wall was 1771.02 seconds within 3600 seconds and attempt running elapsed was 1903 seconds. Final run counts are eleven reused passes, two failures (main gate and dependent aggregate), and ten intentional skips. Both attempts are preserved; no further unchanged-head reruns were performed. Full-checkpoint timing remains unresolved under think-kyzi.. Local broad process/copy controls remain under think-1fwk; they do not change this browser contract.
