---
type: is
id: is-01m0w0cmcy87c00bdbdyvt1xm3
title: "PR #31 review 2: use the assurance enum token in the tutorial card"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0w0c7yd4nabyntb3137stwm
created_at: 2026-08-25T08:25:33.341Z
updated_at: 2026-08-25T08:27:12.812Z
closed_at: 2026-08-25T08:27:12.811Z
close_reason: "Fixed PR #31 finding 2: the vocabulary card now prints the exact `numerically-checked` assurance token used by the schema."
resolution: null
duplicate_of: null
---
PR #31 comment finding 2. TUTORIAL.md:679 writes `numerically checked` between two exact enum values even though Witness/v1 uses `numerically-checked`. Fix the vocabulary card to display the actual token.
