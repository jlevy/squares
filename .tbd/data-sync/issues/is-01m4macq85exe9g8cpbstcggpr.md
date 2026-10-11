---
type: is
id: is-01m4macq85exe9g8cpbstcggpr
title: Recover and classify the post-deploy GitHub link audit failure
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
  - ci
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-11T01:49:13.859Z
updated_at: 2026-10-11T02:46:02.525Z
started_at: 2026-10-11T02:25:14.529Z
closed_at: 2026-10-11T02:46:02.524Z
close_reason: "Complete replacement audit passed 3932/3932 checks, 993 unique requests, zero retries, audit wall511.65s with enforced1800s limit. Checker183705ffb audited deployed6038af33, unchanged render/data expectations and exact Workbench revision. Both hosted attempts (12/25 GitHub503 failures) remain preserved as failures. PR462 merged/deployed; final layouts/browser/assets/PDF checks and prior exact-tree hosted gates passed. Receipt: durable website-cleanups/audit/published6038-complete-receipt.txt. Cleanup PR496 CI is separately pending."
resolution: null
duplicate_of: null
---
PR462 merged as6038af33 and Pages deploy succeeded. Main run38101925790 failed only12 GitHub blob/main links with HTTP503;3920 of3932 checks passed, including deployed revision, site browser/assets/PDF checks. Preserve the exact failure receipt, verify external-link availability, and obtain a completed publication audit after recovery. Evaluate bounded retry/cache behavior without suppressing persistent broken links or treating incomplete checks as success. Link this recovery to think-xio5; do not close final verification until complete.
