---
type: is
id: is-01m25zs0xky60mnw0q1fvb5bfz
title: Independently verify the revised n11 explainer and rendered artifacts
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
dependencies: []
parent_id: is-01m25zrj5np9ywft00t8j8neaz
created_at: 2026-09-10T15:42:56.946Z
updated_at: 2026-09-10T20:24:55.914Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Independently review the revised explainer for mathematical scope, reader clarity, and
rendered behavior. Reconstruct the exact headline and endpoint statements from the
retained T-025/T-026 proof records, verify that point and threshold budgets are not
conflated, and check that compactness or endpoint language does not overstate T-026.

Run the focused explainer tests, source-generation checks, PDF check, links and the
appropriate repository validation tier. Inspect the rendered article at representative
screen and print widths. Record any remaining simplifications as deliberate teaching
choices rather than completeness claims.

## Notes

Independent documentation review covers PR #148 head f7126bfc. The branch publishes the v0.4.0 explainer edition and exactly two source-derived history entries. v0.4.0 first became this explainer's edition label on September 10, 2026 at 35484ebd; v0.3.0 first became that label on September 8, 2026 at ce3b1ab5. T-018 remains the visual teaching spine; T-025 and T-026 retain their exact endpoint and weak-limit scopes; the individual-parent result is excluded because it supplies neither joint disjointness nor a new lower bound.\n\nLocal validation passes: 135 broad focused tests at 35484ebd, then 62 focused tests after the provenance qualification; Ruff, BasedPyright, generated-claim drift, prepared output, deterministic PDF/font, complete atlas, Flowmark and Practical Prose checks pass. Hosted build, prepare, Firefox, geometry, suite, sweeps, macOS and mergeability pass. Validate fails only on main's inherited expired session099 state. WebKit's 1280px saved custom-serif geometry probe reproduced one failure despite f712 changing only prose/comments; require the stacked rerun to decide it. Keep this task open until PR #148 is retargeted to the published research branch and stacked required checks pass.
