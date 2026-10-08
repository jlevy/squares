---
type: is
id: is-01m4daq6byexd6a1zayqqvdxtg
title: Synchronize case popover collapsed state with native close
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T08:40:15.998Z
updated_at: 2026-10-08T08:49:43.143Z
started_at: 2026-10-08T08:42:25.348Z
---
Final full CI37748134343 at a910a0e6 failed one browser contract: after Escape hides #pop-case, a frontier row still has aria-expanded=true. All 3243 other shard-C tests and every deep research/portability job passed. Diagnose native beforetoggle versus queued toggle state/focus handling, correct the source behavior without sleeps or weaker assertions, and add a deterministic regression covering closure and pending fetch invalidation. Preserve source focus semantics and rapid close/reopen behavior. Coordinator owns bead mutations, commits, source pinning, PR updates and final validation.

## Notes

Full checkpoint37748134343 at a910a0e6 completed with eleven deep/portability jobs passing, ten intentional skips, and one actual main-gate failure plus its dependent aggregate. Only fast behavioral shard C failed: test_a_frontier_row_opens_its_record_and_steps_to_the_next observes an invisible native popover with one aria-expanded=true row (3,243 other tests passed). Gate wall1371.41 s; full run1505 s. Complete failed log and compact timing/summary receipts are retained outside scratch. Claimed child think-gtyf covers a source fix and deterministic close-state regression; moderate browser worker owns the disjoint JS/tests/probe and Astra independently reviews event ordering, focus and request lifecycle. Ordinary row reopening already invalidates older requests; no second normal-row stale-fetch production defect is claimed. All earlier automatic PR checks remain passed at that head, and the corrected source head will receive fresh automatic/full validation.
