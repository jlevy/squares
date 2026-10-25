---
type: is
id: is-01m5sv63jp99w0b7fbc8z9kdns
title: "Exact-side register slice 2: stated polynomials (older-notation houses, catalogue polynomials, reported roots)"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-10-25-exact-side-register.md
labels:
  - project
dependencies: []
parent_id: is-01m5sv3xcxr02a4019fz9bbmn9
created_at: 2026-10-25T15:34:36.886Z
updated_at: 2026-10-25T15:34:36.886Z
---
Slice 2 of the exact-side register (spec docs/project/specs/active/plan-2026-10-25-exact-side-register.md; epic think-gbr2; tracker #811). Add the exact sides the record states but slice 1 does not read:

- the sixteen houses written in older notations, which `exact_sides.read_form` leaves unread: fifteen quadratic closed forms in the verified lane (n = 5, 10, 18, 19, 26, 27, 38, 40, 52, 65, 66, 67, 82, 85, 89, such as `2 + (1/2)sqrt(2)`) and n = 11's `root(P_trump11, ...)`, read through SymPy's minimal polynomial or the case package's own polynomial;
- the catalogue polynomials in the reported lane, as configurations of the catalogue's packings: 11, 17, 28, 37, 39, 41, 69, 87, 128, 205, 235, 300 (degree 5 to 83), each isolated within one unit of its printed side's last place;
- T-120 to T-123's reported roots at 102, 106, 152 and 177 (#419), as configurations at V0/C0;
- superseded algebraic certificates the register stands behind, such as T-174's at 302.

Price: about 2 agent-hours. Measured on 25 October 2026: all twelve catalogue polynomials decide (SymPy irreducible over Z, Descartes isolated at the printed decimal +- one unit) in 1.5 s together, degree 83 at n = 235 taking 0.53 s. Done when `--check` names no house in an older notation and the register lists each stated polynomial with its basis.
