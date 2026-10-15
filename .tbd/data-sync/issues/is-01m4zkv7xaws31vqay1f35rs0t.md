---
type: is
id: is-01m4zkv7xaws31vqay1f35rs0t
title: Classify the slow-test opt-in in the CLI budget contract
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4y1bk4xqtpbjc6ppar1abj7
hold: null
hold_until: null
created_at: 2026-10-15T11:06:05.609Z
updated_at: 2026-10-15T11:07:10.147Z
started_at: 2026-10-15T11:07:10.146Z
---
Canonical e9cd pre-push caught one failure: test_gate_budgets.test_every_boolean_flag_is_classified_as_a_tier_or_not. New --include-reachable-slow is a push-selection option, not a new validation tier; explicitly classify it in the existing flag-audit contract and retain the check that unknown booleans fail. Run the focused budget contract and all affected option tests, preserve the failed canonical receipt and reuse its passing selected tests without repeating unchanged scientific work. No budget or assertion weakening.
