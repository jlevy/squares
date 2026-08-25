---
type: is
id: is-01m0vyec8k6gbtc795ya5z228x
title: Reject durable-document links into local tbd injections
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-25T07:51:33.394Z
updated_at: 2026-08-25T07:51:42.597Z
closed_at: 2026-08-25T07:51:42.596Z
close_reason: Replaced ephemeral .tbd/docs links with on-demand tbd guideline names and taught the existing documentation checker to reject that generated local-state target. Focused documentation, Ruff, and fast-gate checks pass.
resolution: null
duplicate_of: null
---
CI on PR #31 found that development.md linked into generated .tbd/docs state. The links passed locally because tbd had injected those files, but failed in a clean checkout. Replace them with tbd guidelines command references and make the existing documentation checker reject .tbd/docs targets even when locally present.
