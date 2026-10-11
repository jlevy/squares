---
type: is
id: is-01m3sq5aphftxdvr0spvz9sbny
title: Verify interpreter and imported package roots before worktree validation
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
created_at: 2026-09-30T17:52:53.445Z
updated_at: 2026-09-30T17:52:53.445Z
---
During Session164 closeout in the isolated cleanup worktree, an initial renderer invoked with the root checkout venv imported root sqpack through its editable install because PYTHONPATH omitted the isolated packing/src entry. It made no root diff; the mismatch was found and corrected before retaining final validation. Add a reusable bootstrap or validation preflight that reports and verifies the selected repository, interpreter, sqpack module root and devtools root before rendering or validating. Reject mixed-worktree imports explicitly. Prefer a properly bound task environment on external scratch; retain a tested explicit-path fallback. This protects future source-bound proof runs as well as generated records. No existing mathematical receipt is invalidated by this metadata-only incident.
