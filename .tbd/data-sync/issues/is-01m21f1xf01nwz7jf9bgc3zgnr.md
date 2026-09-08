---
type: is
id: is-01m21f1xf01nwz7jf9bgc3zgnr
title: Review math loading complexity before release
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T21:33:44.799Z
updated_at: 2026-09-08T22:21:18.343Z
---
Owner is concerned that the working page relies on an overengineered or brittle font pipeline. Perform a bounded independent architecture review of build-time KaTeX rendering, geometry reservations, saved font variants, cached font readiness and platform rendering assumptions. Identify removable machinery and concrete release blockers; preserve the working page and do not start a replacement rendering framework.

## Notes

Independent Astra architecture review completed: keep the working shared runtime and optional host geometry preparation, remove the four unused shipped per-base diagnostics, and verify the exact Linux-produced artifact on macOS. The diagnostics were removed in 2474530b. Linux artifact from successful Pages run34283695063 at dab2a381 passed all29 Mac geometry cells with zero measured movement and maximum intrinsic width difference0.171875px. Client-side rendering is already supported without publication preparation; new formulas require no font regeneration. KPress PR64 documents the architecture. Integration review of4a868bb confirmed static/katex and static/js unchanged; final combined Pages checks remain on parent think-qcmi.
