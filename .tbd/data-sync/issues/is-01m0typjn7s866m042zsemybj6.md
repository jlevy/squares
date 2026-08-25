---
type: is
id: is-01m0typjn7s866m042zsemybj6
title: Make the square-packing frontier transparent, complete, and reusable
kind: epic
status: open
priority: 1
version: 27
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - framework
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0tyqg1a378tyc20by1hwxxq
  - is-01m0tyqgf98qcvjycr6101bs6r
  - is-01m0tyqgsx5exc4x29nekgkn0a
  - is-01m0tyqh36cegypksg5f4rbdj2
  - is-01m0tyqhc5tesckqkhvs406tjj
  - is-01m0tyqhned2mpbrv6a2fdtfrx
  - is-01m0tyqhyhcvcvh5e9j8p2ps0y
  - is-01m0tyqj7srczg0jvc4za541dw
  - is-01m0tyy5k7e4ags20c1fxqth7f
  - is-01m0tz23d5r6xb901bn764en9w
  - is-01m0tz2wgbnct1d681tejb3ccw
  - is-01m0tz8tx11drbgs8hb2092nkt
  - is-01m0tz8txqbfr7v3z93tffjaq0
  - is-01m0tz96g5svy9h1j9ntejmze9
  - is-01m0v06qf4hksmdqc2rga0vr4x
  - is-01m0v06yyh15pkz846vsgxj1wc
  - is-01m0vd6xfaz5p8ccnq6xrnr5x5
  - is-01m0vhjwpg55jj6jt0g96qpr87
created_at: 2026-08-24T22:36:47.654Z
updated_at: 2026-08-25T07:22:33.388Z
---
Cross-cutting redesign of the square-packing frontier, assurance model, validation toolkit, and contributor workflow. Reusable framework implementation uses W7 pipeline-improvement rather than W4 process review or the general-improvement fallback: it balances mathematical soundness, reader and agent clarity, operational discipline, and research efficiency. Make current status effortless to inspect; distinguish published mathematical status, local numerical checks, and exact formal certification; keep public-source coverage explicit and current; and provide general entry points for importing, viewing, checking, and promoting witnesses. Add no metadata, gate, table, hash, or work item without a named failure or reader need. Acceptance: one obvious path answers what is known for each n and why; verified always means exact formal assurance; numerical claims state their actual method and limits; historical unknowns are preserved rather than invented; source and tooling gaps are visible; and the workflow catches consequential errors without ritual or tracker spam.

## Notes

2026-08-25 implementation checkpoint: SquarePackingCase/v2 and Experiment/v2 migrations, typed evidence and source coverage, generated frontier status, Witness/v1 inspect/check/verify/promote tools, exact rational promotion, strict YAML loading, number-field preconditions, n=29 and UnitSquare reviews, document map/common-doc checks, workflow entry contracts, and terminology cleanup are built. No reader-facing source hashes were added; retained source-supplied hashes are archival data only. The generic outward-rounded interval-existence promotion path remains open under think-75ll. Final ordinary validation is being rerun after repairing unrelated open-child/closed-parent bead inconsistencies surfaced by tbd sync.
