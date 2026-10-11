---
type: is
id: is-01m4macq85exe9g8cpbstcggpr
title: Recover and classify the post-deploy GitHub link audit failure
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
labels:
  - website
  - ci
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
created_at: 2026-10-11T01:49:13.859Z
updated_at: 2026-10-11T01:49:13.859Z
---
PR462 merged as6038af33 and Pages deploy succeeded. Main run38101925790 failed only12 GitHub blob/main links with HTTP503;3920 of3932 checks passed, including deployed revision, site browser/assets/PDF checks. Preserve the exact failure receipt, verify external-link availability, and obtain a completed publication audit after recovery. Evaluate bounded retry/cache behavior without suppressing persistent broken links or treating incomplete checks as success. Link this recovery to think-xio5; do not close final verification until complete.
