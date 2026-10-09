---
title: H-323 — Exact Shared-Centre Endpoint Control
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-323
  kind: hypothesis
  claim: The accepted rational n17 packing supplies an exact feasible endpoint for the frozen shared-centre relaxation.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: n17-shared-centre-endpoint
    direction: criterion_met
    threshold: >-
      At U=1169/250 and lambda=1, reconstruct all seventeen E_i and all136 H_ij
      from the accepted exp308 original24 catalogue and the canonical endpoint mask1900015.
      Read exp235's exact rational corners at S=4675530093604551/10^15, join source rows
      through SOURCE_ROW_LABELS to the H256 candidate cells, translate each centre by
      (U-S)/2 and rotate r3=(y,U-x). Require actual original-cell membership, unique
      transformed cells, and the exact canonical mask; inherited assignment metadata is
      not a membership verdict. Retain every closed facet, including degenerate equality
      rows. All34 rational centre coordinates must satisfy every reconstructed Ax<=b row.
      A separate fresh process must rebuild all geometry and coordinates, compare the
      complete mathematical payload and recheck all held generated input bytes after
      checking. Accept only constructed and freshly verified payloads with complete,
      successful owned-group supervision and unchanged registered inputs. Resource stops,
      unavailable sampling before or during execution, or unexpected termination are
      scientifically incomplete even if a prelaunch supervisor envelope says REFUSED;
      invalid input or
      failed membership is refused and unresolved, never a packing contradiction.
      No lambda/mask/source substitution, unregistered retry, first8 LP, numerical
      proposal, exclusion, census admission, new bound or optimality claim.
  instrument: packing/devtools/n17_shared_centre_lp.py
  instrument_ready: true
  regime: >-
    One endpoint positive control, exact Fraction arithmetic, source row-label join,
    same accepted exp308 corner_descriptor/corner_certificate/corner_replay roles.
    Original E_i=C_i intersect [1/2,U-1/2]^2; D_ij=E_j-E_i; H_ij is the convex hull of
    the union of D_ij clipped by n.delta>=7 for the eight signed normals (7,3)/(3,7).
    Accepted parsing, YAML parsing, build_cover/D4 reconstruction and physical packing
    validity are inherited bounded premises. NEW guarded arithmetic covers E/D/H,
    rows, centre transformation and primal checking; it does not reprove those premises.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: >-
    One cooperative construction120s plus fresh120s; combined outer TERM240s/KILL250s
    signal deadlines cover import/parser stalls, with final reaping/sampling/report
    possibly later. One worker; sampled4GiB current RSS per live process in the owned
    group,0.25s sleep between samples, each ps sample bounded1s. Sampling is not an exact
    cadence or allocation-time hard cap. Unavailable samples scientifically incomplete.
    Original-cell/E/D/clip/raw/H vertex ceilings
    32/36/72/73/584/88; all136 pairs and at most12580 rows. Each phase at most2,000,000
    NEW checked scalar operations/comparisons; reduced Fraction operands/results at
    most4096 bits, not CPython/GCD temporaries. Descriptor10MiB, accepted role64MiB,
    witness1MiB, each NEW packet8MiB; output ceiling or arithmetic/wall exhaustion
    incomplete. No unchanged retry or cap expansion. This is an allocation, not a
    performance forecast or full first-eight pilot allocation.
  prereqs: [H-316, H-321, H-322]
  replication: false
  registered: '2026-10-08'
  notes: >-
    Original pre-target registration retained. Exp315 refused the wrong canonical endpoint orbit before E/D/H or primal checking; fresh verification was unstarted. The scientific verdict is unresolved, stopped by a guard. Finite metadata gives r3=3730943 and unique f1=1900015; a corrected control requires a separate prospective registration. The registered r3 criterion and original manifest are unchanged.
    Astra mathematical and final source review cleared; all35 synthetic controls passed.
    Launch records actual Git provenance; Git identities do not determine verdicts.
    Existing run_registered_phases and supervise_posix own two fresh processes,
    combined wall/RSS limits and cleanup. First8 masks remain separately frozen at
    849919,850943,851839,851903,916351,980927,981887,1630207 and are not evaluated here.
---
# Exact Shared-Centre Endpoint Control

The shared-centre LP pilot needs a positive control: its relaxation must retain a known
physical packing. This round tests that requirement using the accepted exact rational
[exp-235 witness](../series/series-000-smoke-and-calibration/results/exp-235-n17-rational-upper/portable-witness.yaml).
It does not propose a new packing or a stronger bound.

The source-specific adapter and geometry contract are described in the
[LP readiness document](../../../docs/project/research/research-2026-10-07-n17-shared-centre-lp-readiness.md).
Execution uses the existing registered-phase runner inside the POSIX supervisor.
The registry’s criterion and resource regime are frozen before the real endpoint is
read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
