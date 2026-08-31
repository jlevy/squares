---
type: is
id: is-01m0pnhtxskzbpvh73z96s06a5
title: "Glossary audit: check every SYNOPSIS term against how it is actually used"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-23T06:39:57.369Z
updated_at: 2026-08-23T06:39:57.369Z
---
SYNOPSIS.md now carries a Terminology section fixing the sense of ~25 terms. It was written from usage, but nothing has checked the reverse direction: that every use in the directory matches the definition.

Go term by term. For each:

1. grep every occurrence across explorations/packing/ -- reports, campaign artifacts, hypothesis registry, defect log, runbook, specs, code comments, and the bead titles/bodies.
2. Decide whether each use matches the definition, contradicts it, or is a third sense nobody noticed.
3. Fix the uses, or fix the definition where usage is right and the definition is too narrow.

Known live risks, from writing it:

- **cell / instance cell.** The rule (bare "cell" = configuration space; a sweep position is an "instance cell") was applied to SYNOPSIS.md in seven places, and NOWHERE ELSE. campaign/README.md, the hypothesis artifacts, exp-00x rounds and defects.yaml all still say "cell" for both senses -- e.g. controls.yaml's "a cell of the sweep whose answer is known in advance", H-016's "every cell of the sweep". Either fix them or scope the rule to the synopsis and say so.
- **quench.** Now defined as all three stages (cell solve, cell fixed point, angle refinement). Check that "quench" in exp-006 through exp-010, in H-002, and in the plan spec means the whole thing, and that "quench 0.1.0" vs "0.2.0" is distinguishable where it matters. D-029 is what happens when it is not.
- **basin.** Defined relative to a specific quench. Check nothing writes "basin" where it means "cell", which is the D-029 confusion in the other direction.
- **polish / exploration.** Established as "polish failure" / "exploration failure". Confirm nothing has quietly started writing "polish gap" (recorded as not-adopted).
- **gap.** Defined as best_side minus standing_best. Rounds at n=5 and n=10 quote gaps to the analytic optimum; those coincide there, but check nothing quotes a gap to a different baseline without saying so.
- **exact / polished / verified (f64).** Tier words also read as ordinary adjectives. Check no artifact says "exact" loosely where the tier is meant, or vice versa.

Deliverable: the terms reconciled, plus a judgement on whether any of this is worth a checker. A grep-based check for the cell/instance-cell rule is plausible; most of the rest is not mechanizable and should not be faked.
