---
title: H-327 — most distance-2 residue orbits yield candidate infeasible sub-patterns of arity at most ten
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-327
  kind: hypothesis
  claim: >-
    At least 60 of the 95 distance-2 residue orbits of the exp-259 partition yield a
    sub-pattern of at most ten of their seventeen cells that the retained float
    selector fails to place at U = 1169/250, with best penetration at least 5e-3 under
    each of three seeds. These are candidates for sub-pattern exclusion, whose
    infeasibility must be certified before drawing mathematical arity conclusions.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      For each of the 95 orbits, the candidate subset returned by the survey's deletion
      search, its arity and best penetration under each seed, and the deletion path;
      numerical placements and failures distinguished from exact feasibility or
      exclusion certificates. Record any later exact exclusion and its subset size
      separately from the numerical screening result.
    direction: >-
      Confirm the screening claim when at least 60 orbits yield candidates of arity at
      most ten with penetration at least 5e-3 under every seed. Fewer than 60 refutes
      only this screening claim for the specified search. Failed numerical search
      establishes no infeasibility or lower bound on minimum infeasible arity. A
      certified infeasible k-cell subset gives an upper bound of k on that minimum;
      neither a deletion path nor one placed subset proves that every smaller subset
      is feasible.
    threshold: 60 of 95 candidate subsets; arity at most 10; penetration at least 5e-3; three seeds.
  instrument: >-
    devtools.survey_n17_residue --distance 2 --sample 0 with its minimal-sub-pattern
    stage, run from a clean worktree on the exp-259 partition, with a receipt per orbit;
    the endpoint's own state as the positive control, which must place. Exact
    infeasibility validation is a subsequent exclusion-verifier obligation, outside
    this float screening run.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; the 95 distance-2 orbits of the exp-259 partition;
    float search only, three seeds; no exact certificate is produced.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: About 95 orbits at 205 s per shard of the survey, 5 to 15 CPU-hours with three seeds.
  prereqs: [H-276]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route F. Correction of 9 October following review C7: the original
    registration treated float deletion outputs as lower bounds on certificate arity.
    They are candidate subsets only. The stall classification of 5 October placed one
    14-cell subset of m1964767 and returned arity-15 deletion candidates for the two
    diagnosed states; this neither proves those candidates infeasible nor rules out
    smaller infeasible subsets elsewhere. Even a certified inclusion-minimal
    infeasible subset need not have minimum cardinality among all infeasible subsets.
    The frozen 95-orbit exp-259 population is retained for this screening registration;
    a run on a later partition must report its changed population and denominator.
---
# H-327: Does the Hard Tail Decompose?

**Mechanism.** A state is excluded by containment when any of its sub-patterns is
rigorously infeasible.
The float deletion search supplies candidate subsets for an exact exclusion engine;
smaller candidates may cost less to certify.
A placed fourteen-cell subset certifies neither the feasibility of other fourteen-cell
subsets nor the absence of smaller infeasible ones.

**Falsifier.** Fewer than 60 of the 95 orbits yield candidates of arity at most ten
under the registered numerical criteria.

**Expected information.** A numerical candidate roster for sub-pattern exclusion and its
measured search cost.
Exact exclusions of small candidates would justify routing those states to sub-pattern
methods.

**Limits.** The float run establishes no mathematical arity bound.
A certified infeasible subset of size $k$ gives an upper bound on minimum infeasible
arity; a lower bound requires feasibility of every smaller subset.
The penetration threshold is the selector’s own scale and does not predict closure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
