---
type: is
id: is-01m4ey3ts2b11ntjfy8xt3stk0
title: Keep complete catalogue equations within the PDF page
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-resume-01a11d93
labels: []
dependencies: []
parent_id: is-01m4eszf0kjvjadgn77f0hy2pc
hold: null
hold_until: null
created_at: 2026-10-08T23:38:27.489Z
updated_at: 2026-10-08T23:38:36.001Z
started_at: 2026-10-08T23:38:36.000Z
---
Hosted catalogue artifact at 760dd953 renders a complete 411-page PDF, but readonly spot QA shows historical H83 equations clipped beyond the right physical page edge (page126). The 112-TeX-character/four-term chunk heuristic permits wide numeric terms. Preserve every coefficient and algebraic identity, split expanded displays more conservatively, use complete coefficient tables for wide individual terms, and exercise actual print-width refusal/positive controls in CI. No identity/proof/data-pin change.
