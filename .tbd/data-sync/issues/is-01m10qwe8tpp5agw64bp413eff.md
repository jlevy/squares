---
type: is
id: is-01m10qwe8tpp5agw64bp413eff
title: "W7: build and price the CG-010 target-free full cell"
kind: feature
status: closed
priority: 0
version: 6
spec_path: explorations/packing/campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
labels:
  - packing
  - focus-correctness
dependencies: []
created_at: 2026-08-27T04:33:06.328Z
updated_at: 2026-08-30T10:37:10.575Z
closed_at: 2026-08-27T07:41:28.137Z
close_reason: "CG-010 structural criterion completed: source-free n=3 full-cell label, total wall and pair-axis inventories, joint 48-image canonical orbit, derived candidate/work price, typed cap, eight mutation controls, enforced schema, independent W2 repairs and three final ACCEPT verdicts. LP solves remain zero; numerical realization, target geometry, H-044/H-045, and n=11 execution remain outside this bead."
resolution: null
duplicate_of: null
---
Own the constructive-enumeration successor to completed BC-019. Define and exercise one target-free full fixed-angle cell with declared walls, one frozen separating axis per non-edge, canonical ties, typed caps, and explicit pricing for angle assignments, wall seatings, non-edge axes, and symmetry orbits. This is reusable W7 instrumentation only: do not consult atlas geometry, run n=11, claim H-044/H-045, or infer geometry or feasibility from the 11,013 abstract scaffolds.

## Notes

2026-08-30 session-045: BC-019 closed. The contact-assembly contract is at contact-assembly-v2-draft and now carries the clause it never had -- per-record certificates or typed limitations. Over n<=30: 17 records have every component expressible as a rigid-lattice primitive and carry the complexity tuple; 13 carry a typed limitation naming exactly which components fail, with the shape, size, tilt and wall seating X-008 measured. The missing grammar move is named rather than guessed: a primitive for axis-aligned polyominoes that are not a bar, rectangle or corner L. BC-024 is what makes that safe -- every unexpressed component in the corpus is untilted. Two things declined rather than computed: internal_slide_dof is zero throughout by the rigid-lattice primitive's own semantics, not by evaluating D = 2m - rank(A_normal) - 2, which prices a contact scaffold and the detector finds none here; and the contact normal axis and sign are absent from the census, so they are listed as unfillable rather than reconstructed from lattice deltas, which would be an assumption about the fit presented as a measurement. The contract names the record and its replay so the two cannot drift into disagreeing silently. No H-044 verdict. Evidence: atlas/known-best/contact-assembly-grammar.yaml, devtools/certify_assembly_coverage.py, campaign/series/series-000-smoke-and-calibration/results/bc-019-assembly-coverage.json, tests/test_assembly_coverage.py. Next action: none for this commitment; remaining contract work needs the minimal-partition solver.
