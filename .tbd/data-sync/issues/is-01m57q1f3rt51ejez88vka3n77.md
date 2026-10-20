---
type: is
id: is-01m57q1f3rt51ejez88vka3n77
title: Isolate editable Python environments for concurrent worktree gates
kind: bug
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
created_at: 2026-10-18T14:35:50.775Z
updated_at: 2026-10-18T14:35:50.775Z
---
A commit hook in the #665 worktree ran uv run on 18 October 2026 and rebuilt editable sqpack/kpress in the shared main packing/.venv while #676 exact-head qualification was active. Both .pth paths changed at 14:31:06–08 UTC from the intended source to fix-665-adoption-20261018. Explicit branch PYTHONPATH still resolves #676, but an environment without PYTHONPATH resolves #665. Nested controls may replace or clear PYTHONPATH; the two worktrees differ in sqpack/release.py and sqpack/cli/validate.py. The affected #676 gate was cleanly stopped at 309.30 seconds (exit 130), not counted as a pass or source failure.

Track a reusable validation/bootstrap safeguard: each worktree uses an explicit isolated UV_PROJECT_ENVIRONMENT; hooks and gate subprocesses preserve the intended interpreter and inspect editable import origins, including without PYTHONPATH. A fresh process must refuse unexpected origins before the expensive gate. No production-code fix belongs in #676. Its immediate mitigation is a new external isolated environment plus exact-head records/push reruns. Related prior closed issue think-wyc9 also records worktree import contamination.

Evidence: /Volumes/spud-ext1/agent-source/squares-intake-20261018-evidence/push-8f4f8a5ce-environment-contamination.json and original gate log/provenance in that directory.
