---
type: is
id: is-01m4zh3apr6q86jmjggvd08bhr
title: Keep site release checks within component-owned validation
kind: bug
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-619
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4zhskq7z8atpw93q5qyafmj
  - is-01m4zp3krgs81t3yssprxyks8e
hold: null
hold_until: null
created_at: 2026-10-15T10:18:04.887Z
updated_at: 2026-10-15T13:17:34.438Z
started_at: 2026-10-15T10:20:56.536Z
closed_at: 2026-10-15T13:17:34.438Z
close_reason: Delivered in PR619, merged 31eaf6333c5d5b6b3d111241768cdd3d30982588. All 43 executed PR checks and selected Deep38735581202 passed. Main Pages38739226771 published site v0.7.7, shared infographics v0.6.1 and lower-bounds paper v0.4.7; actual deployment audit job116439283652 passed 4460/4460 checks. Main full Packing remains independently in progress; no three-minute performance claim. Focused CI safety and performance work continues under think-3d1m and think-kxmq.
resolution: null
duplicate_of: null
---
A site release cut currently schedules the same cross-component pytest list as infographic/paper cuts, including whole-atlas composites and exhaustive proof sweeps. A manual invocation during PR617 integration entered unchanged exhaustive_exact cases; it was interrupted and a focused release/date/claim selection retained. Make cut_release validation component-aware and use the shared quick-tier predicate for ordinary cut iteration, with deeper evidence selected explicitly at the owning checkpoint. Preserve every scientific assertion and full checkpoint obligation; prove selection identities and component ownership without duplicating expensive runs.

## Notes

Release verification uses component-owned modules and QUICK_TESTS by default; explicit --include-deep-tests covers owning deeper tests. Q1 independent threshold controls fixed in 934c, child rohx closed, 48 controls passed. Full matching source/base checkpoint obligation remains. PR618 (https://github.com/jlevy/squares/pull/618), head 3fe125696590cedc3ed3601dbbe098028948fd65, base f97bc0b199e2493b0d84ba51f512e2b406b73021. Three independent final-head reviews cover all 17 paths with no open findings. Site v0.7.6 is prepared. Broad e9cd pre-push had 67 prerequisite passes and 11,387 normal passes, 50 skips and one xfail, but one budget flag-contract failure; corrected by 3fe and the old run remains failed. Final incremental canonical gate passed nine checks in 430.55s, including 5,214 normal passes (36 skipped) and two pool cases. Separate quick pool complement passed nine cases in 40s. Maintained site cut passed 111 cases, 15 deselected; release-impact errors are empty. Hosted Packing 38726302496, Pages 38726302526 and one selected Deep checkpoint 38726327460 are running. Merge/publication remain pending; no three-minute claim or PR599 strict-gate waiver. Persistent evidence: primary .codex/regularization-closeout-evidence-2026-10-13/.
