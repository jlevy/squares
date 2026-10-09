---
type: is
id: is-01m4g7nsqn6jdnyg1kbc1nekhm
title: "Review B on #473 non-blocking follow-ups (N1-N4)"
kind: task
status: open
priority: 3
version: 1
labels:
  - n-17
dependencies: []
parent_id: is-01m4g2z6jk4eycyrwrvqe9vrer
created_at: 2026-10-09T11:44:47.861Z
updated_at: 2026-10-09T11:44:47.861Z
---
From pullrequestreview-5469544287: N1 PR CI no longer has a passing check round trip for the two n17 propagation tools or a successful two-child generate (all moved to slow) — consider one cheap fast round trip; N2 test_regional_mode_uses_transfer_once is at 10.72 s CPU lower bound on PR suite-b, near the 12 s ceiling; N3 three documents still give the retained-JSON step cost as ~1.5 s; N4 the PR-surface retained-JSON step no longer asserts the sweep found files (held > 0) now that the whole-tree test is slow.
