---
type: is
id: is-01m4e37ersbgmvw7ana72wd5an
title: "PR #395 rollout: validate lazy result popover record links on the deployed site"
kind: bug
status: open
priority: 1
version: 1
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
created_at: 2026-10-08T15:48:34.711Z
updated_at: 2026-10-08T15:48:34.711Z
---
Actual merged deployment913781538 failed2/3750 checks: the homepage and all-results record-link checker assumes inline site-records markup, while production rows use data-row-pop-src fragments with static fallback links. Correct the checker to verify each expected row binds its own served fragment and canonical fallback, and every rendered record link remains present; retain fail-closed negative coverage for missing/mismatched rows, fragment destinations and record links. Deploy and validate through a separately reviewed follow-up PR.
