---
type: is
id: is-01m4yezgymfksx798467evpv4h
title: Verify the zero-pending live budget state instead of skipping required coverage
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T00:21:48.627Z
updated_at: 2026-10-15T00:28:10.538Z
started_at: 2026-10-15T00:21:57.932Z
---
At exact source 6756bda8d, enforced shard D runs 4101 passing tests in243.11s under335s ceiling, then check_enforced_quick rejects required tests.test_gate_budgets::test_the_live_pending_tiers_pass_until_their_dates_and_are_named_after_them because it skips when no tier has pending_measurement. Module changed in this PR so omissions are correctly refused. Preserve exact node, all pending-date and real-bead assertions, and strengthen zero-pending branch to validate actual live unrecorded-tier state without fake pending data or vacuous success. Retain original failed job116174451148 log. No ceiling raise, allowlist bypass, marker change or weakened coverage checker.

## Notes

Narrow fix is ready but uncommitted, only test_gate_budgets.py. Exact protected node changed from1skip0.46s to1pass0.43s. It now checks nonempty declared PR-tier roster, verifies live unrecorded_problems and rejects bead-store lookup when nothing is pending. Every pending/date/real-bead assertion remains. Existing refusal controls6pass; full module93pass1.05s with0skips; Ruff/types0findings. Original strictD tests4101pass243.11s remained valid; failure was subsequent required-case accounting. Root batches this with distinct strictC overrun fixes rather than launching another cohort for one small correction.
