---
type: is
id: is-01m135mtdeshe5ptxevhkwgczs
title: Reconcile the figure record's derived facts back into the frontier
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T03:12:05.550Z
updated_at: 2026-08-28T03:12:18.683Z
---
atlas/known-best/composite-figure.json now computes facts the corpus does not hold, and marks each with provenance "derived". Today that is 84 algebraic degrees and 10 perfect-square rigidity determinations. The record is the review surface; the corpus is still the gap.

Close the loop: write the derived values into the frontier records with an explicit derived provenance (per think-18mu's vocabulary), then flip those entries in the figure record from "derived" to "frontier". When that is done, running the figure-record generator with --review should report degree_derived_here as 0, and any future non-zero value is a new gap rather than a standing one.

Depends on think-18mu for the vocabulary and think-kj6n for the degrees. Do not let the figure quietly become the system of record: it exists to make the gap visible, not to substitute for filling it.
