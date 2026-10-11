---
type: is
id: is-01m3tf45sa2rs9stvkrt3cqwgr
title: Match n11 paper presentation exactly to the previous explainer
kind: task
status: closed
priority: 1
version: 10
delegate: sol
labels: []
dependencies:
  - type: blocks
    target: is-01m3tfk55tdjnvapbh1330qw7e
  - type: blocks
    target: is-01m3tfk7z8s0pr9jv0kksvzh6y
  - type: blocks
    target: is-01m3tfkatddsz86ee870exr3e0
  - type: blocks
    target: is-01m3tfkczqspdb8hp17z6252h9
parent_id: is-01m3tf1nb0x65ybpkdj2d9y7gs
created_at: 2026-10-01T00:51:41.465Z
updated_at: 2026-10-01T01:53:02.320Z
closed_at: 2026-10-01T01:53:02.320Z
close_reason: "Completed in draft PR261 at 9e97024f5: original-proof attribution and component links; Sol common-doc/citation and exact shared publication styling reviews; Astra-max adversarial reconciliation (no blocker/high/medium, two low qualifications resolved, 11 simplification candidates); source-bound illustration plan with implementation deferred to four separate beads. 231 focused local tests and PDF inspection passed; hosted integration fixes tracked separately by think-dhsh. Parent think-75cp remains open for user feedback; no merge or publication."
resolution: null
duplicate_of: null
---
User requires identical look and feel to prior explainer: format chips (HTML/PDF/Markdown), title metadata formatting, typography, spacing, colors and shared style conventions. Delegate separate implementation agent to compare original shell/article/CSS and new paper, reuse components where practical, and perform side-by-side visual checks. Preserve original-proof provenance as first prose and preserve math. Keep corrections on draft branch; no publication until feedback integrated.

## Notes

Shared CSS/fonts/metadata/chips/print style and measured SVG sizing complete; 231 focused tests pass, physical PDF role sizes confirmed by independent Sol. First hosted frontend job caught missing nullable-parent guard in new typography probe under isolated strict TS program (earlier tsconfig check did not cover that group). Guard added; actual typecheck-probe-groups program and targeted browser test pass. Final CI rerun pending alongside think-dhsh sparse-citation fix.
