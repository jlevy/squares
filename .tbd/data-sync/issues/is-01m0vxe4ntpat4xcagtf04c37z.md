---
type: is
id: is-01m0vxe4ntpat4xcagtf04c37z
title: "[epic] TUTORIAL pedagogical review: notation, LP exposition, and references"
kind: epic
status: closed
priority: 1
version: 14
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
child_order_hints:
  - is-01m0vxh18tn84y586tps6sskf8
  - is-01m0vxhwqe5yfntb1697t5rk15
  - is-01m0vxjmmmmrfc9xr67ckahra5
  - is-01m0vxmhjdsq7rdy94g9pxx3nx
  - is-01m0vxns5mzy4axt8mdrhaachj
  - is-01m0vxv0f1v7nqpeq5a2kfwjwq
  - is-01m0vxwz54jtrrk1xvg7z3fc46
  - is-01m0vz75fav40ygkba88fajt0p
  - is-01m0w07k24sv5nc6hzacmc6tjt
created_at: 2026-08-25T07:33:57.050Z
updated_at: 2026-08-25T08:29:53.249Z
closed_at: 2026-08-25T08:29:53.249Z
close_reason: All eight child beads implemented in TUTORIAL.md (82c68dc). Findings are recorded in docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md, which stays as the durable record of what was found and why. think-4b9m remains open outside this epic for the SYNOPSIS and conventions gate-step-count drift.
resolution: null
duplicate_of: null
---
Reader-driven review of `explorations/packing/TUTORIAL.md`, raised while reading it as
the intended newcomer audience.
Findings are written up in
[review-2026-08-25-tutorial-pedagogy-and-accuracy.md](explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md),
which every bead here carries as its spec link.

| Bead | Finding | Question |
| --- | --- | --- |
| think-czye | TR-1…TR-7 | **Accuracy drift.** A gate step count now wrong in three documents, a superseded absolute, a miscredited baseline column, a dropped "interiors", a missing frontier lane, and two judgement calls |
| think-8hdt | TR-8 | **Notation.** No symbol table. `s` versus `s(n)`, per-square versus whole-vector, `θ` versus `a`, `φ`, `a*`, `β`, `s*`, `oᵢₖ,ₓ` — introduced in passing, several never defined, three marks carrying two meanings each |
| think-ejgd | TR-9 | **The linear program.** T-2 is never written as a program. Needs the explicit form and a short on-ramp — §4's corner mechanism rests on an undefined "optimal basis" |
| think-ap15 | TR-10 | **The quench map.** Too vague to follow. What type of solve, what determines the cell, what "move the angles" means, and repeat until when and why. One algorithm with knobs, not a family |
| think-i22v | TR-11 | **Precision.** What precision to operate at, how the regimes relate to hardware `f64`, and how much depends on hardware speed versus exact or arbitrary-precision arithmetic. The `1e-11` floor is a solver tolerance, not machine epsilon |
| think-g5o3 | TR-12 | **How many roots?** Every example extrapolates from Trump's single `α` of degree 8. Do we know how many are needed in general — yes or no, and why |
| think-i3wv | TR-13 | **References and prerequisites.** The concepts a reader needs up front with somewhere to look, plus what actually implements the exact arithmetic here |
| think-sofa | TR-14 | **The vocabulary card.** Fourteen rows chosen by no stated rule; `proposer`, `refiner`, `rigidity`, `descriptor`, and the polish/exploration failure pair are all used in the body and absent |

Scope boundary: the tutorial owns the conceptual on-ramp only.
`SYNOPSIS.md` stays authoritative for every result, status, count, and verdict, and no
bead here moves status prose into the tutorial.

Each bead records findings first and proposes the edit second, so the wording change can
be decided separately from the finding.
`TUTORIAL.md` is unchanged.

Out of scope and tracked separately: think-4b9m, the half of TR-1 where `SYNOPSIS.md`
and `conventions.md` say thirty-one gate steps against the thirty-two now registered in
`validate.py`.
