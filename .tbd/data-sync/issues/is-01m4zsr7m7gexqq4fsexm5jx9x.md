---
type: is
id: is-01m4zsr7m7gexqq4fsexm5jx9x
title: "F1: remove automatic fast-check reuse based on unauthenticated artifact names"
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4zvpghgeyb11h0bba3v59r6
hold: null
hold_until: null
created_at: 2026-10-15T12:49:18.470Z
updated_at: 2026-10-15T15:10:01.434Z
started_at: 2026-10-15T12:49:26.605Z
---
Independent review found the same live source-authentication gap in baseline fc2ceae79: verified_merge_tree.py accepts a self-named tree artifact with successful native run/job names, without authenticating the executed PR merge source. Deferred work stays cold, but allowlisted fast checks can be skipped on main. Remove the automatic reuse path and its dead producer/verifier plumbing rather than introducing a provenance framework. Preserve every fast/scientific check, budgets and normal PR selection. Update the shared guide and meaningful workflow/selection controls. More main fast work may run, but no new proof API overhead or trusting self-declared artifact names. The retired deferred candidate and review evidence are preserved separately.

## Notes

PR620 now contains final grouped head cf9003e0da0d6c33963a9804de4c41efdf8b3ddf on base 31eaf6333c5d5b6b3d111241768cdd3d30982588. The F1 runtime removal is unchanged from the independently reviewed first head: no artifact-name proof can suppress selected checks. Final integrated F1 controls passed 14/14 in 1.35s; site-only v0.7.8 cut passed 111 tests with 15 deliberate deselections in 8.67s. The first ordinary run failed two documentation integration checks and one browser resize-readiness comparison; those failures are preserved under think-ju0q and think-nnti. A genuine unlanded timeout receipt correction is now narrowly extracted under think-cdt9, with deterministic red/green evidence and no unrelated legacy snapshot code. Final independent senior, security and performance reviews are running over all 20 paths. Replacement full Packing38744311408 is explicitly selected at this head; superseded trial38741455333 was canceled after known failures. No redundant Deep run is selected. Component-impact errors are empty; poster and paper editions remain unchanged. Added main work remains unmeasured and the three-minute target stays open.

2026-10-15 14:20 UTC: Final independent senior, security and performance reviews cleared all 20 current-head paths. Ordinary Packing and Pages passed (31 successful checks). Full 38744311408 failed seven CALL ceilings after 2301.62 s integration, with all functional assertions and dedicated workers passing. Repairs tracked as 2equ and n5ry; integration cost under e2z4. No merge until the corrected head is reviewed and passes its required checkpoint.

2026-10-15 final-head follow-up: Final repair head15548357a31e16acd029934025a8a615f9f1e208 is pushed on exact main31eaf633. New independent full-source senior K5535320248 and security L5535320451 cover28/28 paths with no actionable findings. Ordinary Packing38756777827, Pages38756777889 and ONE selected full Packing38756833833 now run on this head; no redundant Deep. The full topology has twelve mandatory Linux owners plus aggregate, with macOS separately inspected. Local prepush passed67 prerequisite Steps; its conservative effective2CPU/jobs2/inner1 wholequick used one pytest worker and reached only~23% after800.4s, so root deliberately interrupted it (parent130/child-15). This is incomplete evidence, not passing full local validation. Source stayed frozen; final hosted coverage/skip parity is mandatory before merge. Runtime/guard and source-based paper dispositions are fully reviewed; no waived assertion/deadline.
