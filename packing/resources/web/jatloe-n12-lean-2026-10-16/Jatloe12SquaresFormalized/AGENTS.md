# Formalization rules

Read README.md before working on this project. Preserve the original packing
definitions, strict interior disjointness, legal boundary contact, and public
theorem statements. Do not add admissions, custom axioms, unsafe proof oracles,
new native proof sites, or weaker hypotheses to make verification pass.

The original numerical classification uses native_decide and retains compiler
trust. Geometric arguments, checker soundness and assembly remain ordinary Lean
proofs. Distinguish written source, component verification, and a completed
final theorem/type/axiom audit. Do not claim global optimality verified before
the final profile passes.

Use the project scripts for serial module replay. The remote runner may use
multiple Lean threads within a module. Keep local defaults conservative and
machine-specific logs/caches under ignored .verification/ and .lake/ directories.
Preserve Jatloe's, Ben Gurevitch's and CTJLewis's credits.
