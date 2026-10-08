---
type: is
id: is-01m4d0s3h9zzz2gfjnzggj6qgt
title: Retroactively label result-intake pull requests
kind: chore
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4bxdtbvasjn91jwhz448s7b
hold: null
hold_until: null
created_at: 2026-10-08T05:46:32.872Z
updated_at: 2026-10-08T05:46:40.964Z
started_at: 2026-10-08T05:46:40.963Z
---
User requests the intake label on all historical GitHub PRs whose primary purpose is importing, recording, or validating newly reported results. Inventory open, merged, and closed PRs; preserve existing labels; exclude incidental intake and general tooling or proof development. pr422_gates owns inventory and GitHub label mutations; root verifies report and closes after complete coverage.
