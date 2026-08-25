---
type: is
id: is-01m0vxe4ntpat4xcagtf04c37z
title: "[epic] TUTORIAL pedagogical review: notation, LP exposition, and references"
kind: epic
status: open
priority: 1
version: 9
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
created_at: 2026-08-25T07:33:57.050Z
updated_at: 2026-08-25T07:42:32.673Z
---
Reader-driven review of `explorations/packing/TUTORIAL.md`, raised while reading it as
the intended newcomer audience. The tutorial is factually close to
[`SYNOPSIS.md`](SYNOPSIS.md) and every relative link resolves, but it is harder to
follow than it needs to be. The questions, in the order they were raised, plus the
accuracy drifts found while checking them:

| Bead | Question |
| --- | --- |
| think-8hdt | **Notation.** No symbol table. `s` versus `s(n)`, per-square versus whole-vector quantities, `θ` versus `a`, `φ`, `a*`, `β`, `s*`, `oᵢₖ,ₓ`—introduced in passing, several never defined, three letters carrying two meanings each |
| think-ejgd | **The linear program.** T-2 is the central structural result and is never written as a program. Needs the explicit form and a short on-ramp: what an LP is, why being one is good news, why the linear part is easy—§4's corner mechanism is stated in terms of an undefined "optimal basis" |
| think-ap15 | **The quench map.** The three-stage description is too vague to follow. What type of solve, what determines the current cell, what "move the angles" means, and repeat until when and why. It is one algorithm with knobs, not a family, and the tutorial does not say so |
| think-i22v | **Precision.** What precision to operate at, how the regimes relate to hardware `f64`, and how much the work depends on hardware speed versus exact or arbitrary-precision arithmetic. The `1e-11` floor is a solver tolerance, not machine epsilon, and the tutorial invites the wrong reading |
| think-i3wv | **References and prerequisites.** The core concepts a reader needs up front, with somewhere to look—linear programming, algebraic number fields, numeric methods—plus what actually implements the exact arithmetic here, and with which algorithms and libraries |
| think-g5o3 | **How many roots?** Every example extrapolates from Trump, which has a single `α` of degree 8. Do we know how many are needed in general—yes or no, and why |
| think-czye | **Accuracy drift.** Five claims that no longer match the record, including a step count, a superseded absolute, and a missing frontier lane |

Scope boundary: the tutorial owns the conceptual on-ramp only.
`SYNOPSIS.md` stays authoritative for every result, status, count, and verdict; this
epic must not move status prose into the tutorial.

Each bead records findings first and proposes the edit second, so the wording change can
be decided separately from the finding.
Nothing in `TUTORIAL.md` has been edited yet.
