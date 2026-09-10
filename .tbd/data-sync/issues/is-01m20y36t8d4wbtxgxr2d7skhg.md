---
type: is
id: is-01m20y36t8d4wbtxgxr2d7skhg
title: Document the font and math loading architecture in KPress
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T16:37:21.314Z
updated_at: 2026-09-08T18:40:08.402Z
closed_at: 2026-09-08T18:40:08.402Z
close_reason: KPress PR61 merged at 20a7d2b after the final browser, JavaScript, lint, distribution and Python3.12/3.13/3.14 CI matrix passed (run34256487179). It adds correct per-family font readiness/hydration, the canonical architecture document, and the optional-browser availability repair.
resolution: null
duplicate_of: null
---
User explicitly requests a defined code-adjacent home for the font loading and math loading architecture. Add a canonical note beside the Squares rendering tools, linked from renderer/preparation/host entry points and development.md. Explain embedded composite font sources, build-time measured per-base geometry, matching metadata/hydration, actual-glyph readiness and per-node visibility, dynamic values, initial certificate layout, heat-map/print scheduling, no-JS/failure behavior, and independent correctness versus performance probes. Link KPress public runtime documentation as upstream API owner and keep implementation details out of the reader-facing page.
