---
type: is
id: is-01m4zsr7m7gexqq4fsexm5jx9x
title: "F1: remove automatic fast-check reuse based on unauthenticated artifact names"
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T12:49:18.470Z
updated_at: 2026-10-15T13:17:49.495Z
started_at: 2026-10-15T12:49:26.605Z
---
Independent review found the same live source-authentication gap in baseline fc2ceae79: verified_merge_tree.py accepts a self-named tree artifact with successful native run/job names, without authenticating the executed PR merge source. Deferred work stays cold, but allowlisted fast checks can be skipped on main. Remove the automatic reuse path and its dead producer/verifier plumbing rather than introducing a provenance framework. Preserve every fast/scientific check, budgets and normal PR selection. Update the shared guide and meaningful workflow/selection controls. More main fast work may run, but no new proof API overhead or trusting self-declared artifact names. The retired deferred candidate and review evidence are preserved separately.

## Notes

Implemented in PR620: https://github.com/jlevy/squares/pull/620. Current head 82b816496edc1a75be73374e3a9c81a5e8ccd525, base 31eaf6333c5d5b6b3d111241768cdd3d30982588. Producer, lookup, automatic narrowing and dead verifier removed; scientific STEPS and workflow run commands unchanged. Two controls failed before removal, including 86 suppressed checks; final integrated controls passed 14/14 in 1.35s. Site-only v0.7.8 cut passed 111 tests with 15 deliberate deselections in 8.67s; component-impact errors are empty. Infographics v0.6.1 and paper editions remain unchanged. Independent committed-head senior and security reviews are running. One explicit full Packing dispatch38741455333 is selected; no redundant Deep dispatch. Main repeat cost remains unmeasured, so no three-minute claim. Broad local builds are held at 75MiB external scratch; no internal fallback.
