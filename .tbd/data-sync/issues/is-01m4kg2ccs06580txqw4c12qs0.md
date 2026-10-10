---
type: is
id: is-01m4kg2ccs06580txqw4c12qs0
title: Scope pre-push prerequisites to changed inputs
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-10T18:09:12.086Z
updated_at: 2026-10-10T18:12:46.510Z
started_at: 2026-10-10T18:12:46.496Z
---
Reuse the existing select_for_paths contract to scope local --push prerequisite checks, then separate policy/tooling inputs from the overly broad _CORE attribution after auditing actual dependencies. No implementation is authorized in the current slice.

Read-only evidence: --push currently selects all 65 fast/non-broad prerequisites before adding reachable behavioral tests, and bypasses prerequisite path scoping even when --since is supplied. The existing pure scoper selects 9/65 prerequisites for test_site_math_preferences.py alone, 59/65 for the eight process/test/doc paths, and 58/65 for gate_budgets.py alone. These are selection counts, not wall-time savings. The policy module reaches scientific checks through packing/src/sqpack/*; do not replace that conservative rule with a blanket omission.

Acceptance contract: compute both prerequisite and behavioral selection from the same complete changed-path set, including working-tree changes and old/new rename/delete paths. Preserve empty/unclaimed-path whole-tier fallback and all unattributed checks. Retain named negative controls for unknown files, missing attribution, scientific verifier/source/certificate edits, shared core changes, all declared Workbench render inputs, JavaScript/CSS/probe/toolchain edits, and a mixed website-plus-scientific change. Ensure no empty or silently reduced verdict. Policy/tooling changes must still run budget declaration/enforcement and validation-CLI contracts. Keep complete required PR CI and full/strict release checkpoints intact.

Implement in a bounded follow-up with focused selection tests and one ordinary push receipt. Distinguish selector overhead, subprocess/check runtime, and host contention; do not claim overall acceleration from fewer selected steps or add a generic benchmark framework. Parent process tracker remains open.
