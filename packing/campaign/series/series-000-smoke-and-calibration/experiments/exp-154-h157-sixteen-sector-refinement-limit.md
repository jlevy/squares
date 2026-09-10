---
title: "exp-154 — sixteen owner sectors and the angular refinement limit"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-154
  series: series-000
  title: Sixteen owner sectors and the angular refinement limit
  date: '2026-09-10'
  hypotheses:
  - H-157
  tier: exploratory
  subject:
    label: Exact survivor weight of the transported mass-eleven ceiling family under refined
      owner-sector patches at q = 96/25
    engine: A bin-count parametrisation of devtools.owner_footprints in a scratch copy, with
      devtools.transport_ceiling_family and devtools.screen_corner_dual_salvage.screen_footprint
      imported verbatim; the tracked module was not edited
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64; project Python 3.14; one process
    engine_commit: 67ccd16bb23ac2ba03b3430e757839b5b18528f4
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Eight-bin equivalence against the tracked devtools.owner_footprints -- the membership
      predicate over 1444 signed rays by 8 sectors, sector_endpoint_rays, endpoint_footprint
      polygons vertex for vertex, and class ids with their reflection pairing, all at zero
      disagreements -- plus reproduction of lane X1's recorded eight-bin readings (survivor weight
      33/4 to exactly 10, four classes at exactly 10, mean deletion 55/32, nearest survivor at SAT
      gap 0.014978). Exact Sutherland-Hodgman clipping independently checks all twelve
      parent/child survivor sets and the 270 singleton rays selected as neutral by SAT;
      it does not independently census all remaining rays or validate the distance calculation.
    candidate: Sixteen closed angular bins per mark, thirty-two classes per corner; then the
      singleton-ray refinement limit, one class per retained signed ray at 1444 classes per mark,
      of which every coarser angular partition is a coarsening; then a pose probe deleting against
      each of the eight members of the mark clique.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Opus 5 measurement lane, coordinated by Claude Fable
    entry_point: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-screen16.py.txt
    command: cd packing && uv run --frozen --all-extras --group dev python3 $SCRATCH/screen16.py,
      then the same invocation on verify_eight.py, verify_geometry.py, limit.py, crosscheck2.py
      and consolidate.py. $SCRATCH is the directory holding the retained
      results/agenda-034/lane-x4-*.py.txt scripts restored to their original .py names; each
      script pins paths in SCRATCH and REPO constants, which a replay must repoint
      before running, and the scripts import nbins.py from it alongside devtools.
    budget: Registered at under an hour. Six retained scripts, no unattended runner, no retry.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-survivors-16.json
    commit: 67ccd16bb23ac2ba03b3430e757839b5b18528f4
    dirty: false
  results:
  - shape: determination
    role: outcome
    question: Does every refined sixteen-sector subclass of the four neutral eight-sector classes
      have exact survivor weight strictly below 10?
    outcome: criterion_missed
    checked_by: Six of the eight refined subclasses read exactly 10 and two improve to19/2,
      satisfying the registered upper bound79/8 more strongly. Over the full thirty-two-class sixteen-bin split the maximum
      survivor weight is exactly 10, attained at six classes. Both readings agree under SAT and
      under exact convex clipping, 12 of 12, and the whole table is symmetric under the diagonal
      reflection J -> 15 - J with m1 <-> m2, which the screen was not told to satisfy.
  - shape: determination
    role: mechanism
    question: Does the refined patch reach further toward the nearest surviving core, as the
      registered mechanism predicted?
    outcome: invalid
    checked_by: Independent source review found that the delivered distance helper assumed
      disjoint polygons but applied the formula to two intersecting cases. The six neutral
      children retain the stated positive distance to fixed targets; m1:J9/16 and m2:J6/16
      intersect their original target cores55/50 and have actual fixed-target distance zero.
      The unchanged all-children identity is false and does not decide the compound0.015
      reach criterion. Patch nesting and the1.6165x to1.6175x area increase still reproduce;
      the count-based primary rejection is unaffected.
  - shape: determination
    role: mechanism
    question: Can angular refinement eliminate every neutral class on the retained ray
      universe under its intersection-patch construction?
    outcome: criterion_missed
    checked_by: At the singleton-ray limit, 135 classes per mark read exactly 10 and they form a
      contiguous interval in retained-ray order. Any bin containing one of those retained rays
      has intersection-patch survivor weight exactly10. Deleting against whole owner cores59/60
      leaves10. An arbitrary guaranteed subpatch gives only at least10 unless it also contains a
      common mark; a positive-area subpatch of core59 omitting both marks leaves43/4. These
      deductions concern the fixed patch-only residual domain and require new admissibility under
      stronger restrictions. They are exploratory mechanisms, not another registered target.
  verdict:
    decision: rejected
    primary_criterion: The exact survivor weight of the transported mass-eleven ceiling family,
      maximised over the refined subclasses of the four neutral eight-sector classes, against the
      registered threshold of strictly below 10.
    reason: Six refined subclasses still read exactly 10, so the case split as posed is not closed
      by refinement and H-157 is refuted on its own registered direction.
  effort:
    timebox: under an hour, as registered
    wall_seconds: 356.1
    stopped_by: criterion
---
# Exp154: Sixteen Sectors Improve Two Subclasses and Leave Six Neutral

**Independent source review, September 10, 2026.** The survivor table and primary
rejection reproduce.
This revision corrects the aggregate field from minimum to the preregistered maximum,
withdraws two invalid distance calculations and narrows the angular/pose deductions.
It does not rerun or change the original target criterion.

**H-157 is refuted on its own registered direction.** It predicted exact survivor weight
at most `79/8 = 9.875` for every refined subclass of the four neutral eight-sector
classes. Six of the eight read **exactly 10**, and two improve to `19/2`, satisfying the
registered upper bound `79/8` more strongly.
The refutation clause says one neutral class defeats the split, and six survive.

| refined subclass | parent | survivor weight | deletion |
| --- | --- | --- | --- |
| `bottom-left:m1:J6/16` | `m1:j3` | **10** | 1 |
| `bottom-left:m1:J7/16` | `m1:j3` | **10** | 1 |
| `bottom-left:m1:J8/16` | `m1:j4` | **10** | 1 |
| `bottom-left:m1:J9/16` | `m1:j4` | `19/2` | `3/2` |
| `bottom-left:m2:J6/16` | `m2:j3` | `19/2` | `3/2` |
| `bottom-left:m2:J7/16` | `m2:j3` | **10** | 1 |
| `bottom-left:m2:J8/16` | `m2:j4` | **10** | 1 |
| `bottom-left:m2:J9/16` | `m2:j4` | **10** | 1 |

All exact. The two that break delete four extra weight-`1/8` placements each, indices
`[7, 16, 29, 55]` for `m1:J9` and `[2, 22, 25, 50]` for `m2:J6`.

**The patch enlargement is verified.** The guaranteed wedge widens from `pi/4` to
`3pi/8`, the refined patch does contain its parent vertex for vertex and is strictly
larger — 1.6165x to 1.6175x the area — and it does lie inside the anchored quarter-core
`Q_phi(m)` for every one of the 87 to 94 retained signed rays in its closed bin.
For the six neutral children, the squared distance to the selected target core remains

```
d^2 = 75308842465387162009/335694834731568400000000      d = 0.014977891
```

The two improved children instead intersect their selected targets, core55 for
`m1:J9/16` and core50 for `m2:J6/16`, so those fixed-target distances are zero.
The original distance helper assumed disjointness without checking it.
A mark being a vertex does not prevent the patch from approaching another core.
The claimed all-children identity is withdrawn; distance to the nearest *remaining*
survivor must also be distinguished from distance to a target that has been deleted.

**The retained finite universe has a further obstruction.** At one class per retained
signed ray, 135 classes per mark read exactly ten.
Any coarsening retaining such a ray has an intersection patch with survivor weight ten.
The whole-core pose probes leave ten at two mark-clique members.
The local T1 and T2 statements are given with their fixed-domain premises in
[X-026 §5.1](../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md).
T2 gives only a lower bound of ten for an arbitrary guaranteed subpatch; equality
requires a common mark in that patch.
Neither statement applies automatically after stronger residual restrictions.
They do not establish that the conditional strategy fails, because a conditional proof
needs one closed owner selection per packing rather than every class closed.
X-026 escape 1 is narrowed rather than closed on that reading.

**Costs.** Five measured steps totalling 356.1 s: the eight-bin control and sixteen-bin
screen 4.1 s, the exact containment and reach audit 1.6 s, the singleton-ray limit with
the pose probe 93.8 s, the independent clipping cross-check 91.2 s, and consolidation
with the bin-theorem check 165.4 s. A sixth step, the eight-bin equivalence control
against the tracked module, is recorded only as under 5 s and is not in the total.

**Scope.** The lane measured deletions, not atoms, so the conditional threshold line
(`H-155`) is untouched.
Nothing tracked was edited by the lane; the bin-count parametrisation lives in a
retained scratch copy and promoting it into `packing/devtools/owner_footprints.py` is
carried separately under `OR-1`.

Everything measured, both cross-checks, the false start that had to be discarded, and
the ten scripts are retained beside
[lane X4](../results/agenda-034/lane-x4-sixteen-sectors-and-the-refinement-limit.md).
<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
