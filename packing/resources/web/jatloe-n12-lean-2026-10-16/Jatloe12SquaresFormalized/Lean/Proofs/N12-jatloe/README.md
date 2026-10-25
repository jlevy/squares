# Twelve-square formalization

The unconditional theorem is
`N12Compact.Final.optimality : S12.packingConstant12 = 4` in
[Final.lean](Compact/Assembly/Final.lean). It applies to twelve arbitrarily
rotated unit squares with disjoint interiors and allows boundary contact.
All 117 retained cases are assembled, and the explicit 4-by-3 grid attains 4.

Jatloe provided the full mathematical proof and partial Lean formalization.
Ben Gurevitch aided in formalization. **CTJLewis refactored and compiled the proof.**

The proof source matches upstream `main` commit
`1f60d412707aae824b76fbaf11d4e708695451fa`. Successful run `38849916588`
authenticated the 5,377 previously compiled project modules and reran the final
exact-type and axiom audit. The run reused every project object from cache;
it was not a fresh rebuild. Verification inherits the classification's native
compiler trust: 1,624 approved native-generated axioms plus three standard
axioms, with no admissions or unexpected custom axioms.

[The repository README](../../../README.md) has the current evidence links,
credits, binary-export status, and GitHub replay instructions. The publication
pins Lean 4.35.0 and Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`.
The complete inventory including dependencies/setup/audit is 9,583 modules,
within the hard 10,000 limit.

Original mathematical documents remain in `mathematics/current/` and research
notes in `mathematics/research/`. Dated handoffs and source comments describe
historical stages; their earlier "uncompiled" or pending-work statements are
superseded by the accepted run-specific evidence. The Lean proof files are
preserved unchanged, including historical comments.
