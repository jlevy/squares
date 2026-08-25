---
type: is
id: is-01m0wcefxrhq89zsxp2q51w2p2
title: Do not let a later check mask an earlier gate failure
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T11:56:17.207Z
updated_at: 2026-08-25T11:57:21.859Z
closed_at: 2026-08-25T11:57:21.858Z
close_reason: "Completed: treated the visible ledger failure as binding, regenerated the view, and reran the full focused checkpoint under set -euo pipefail; every command passed and terminal exit is zero."
resolution: null
duplicate_of: null
---
The phase-5 checkpoint command ran several checks sequentially without shell fail-fast behavior. packing-ledger check correctly failed on expected generated-view staleness, but a later successful git diff check made the aggregate exec exit zero. The coordinator read the inner failure and did not accept the gate. Record D-299 and rerun the decisive checks after rendering, using fail-fast or separate invocations.
