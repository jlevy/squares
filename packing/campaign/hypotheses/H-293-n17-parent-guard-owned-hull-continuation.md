---
title: "H-293 \u2014 one-round parent-guard owned-hull exclusion"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-293
  kind: hypothesis
  claim: The fixed parent-aware owned-hull initialization and one no-refinement round yield
    a freshly checked exclusion of the accepted parent packing domain restricted to the closed
    owner0 guard.
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: fresh_conditional_owned_hull_exclusion
    direction: criterion_met
    threshold: Fresh independent PASS_CONDITIONAL_CLOSED with exact initial lexicographic all-finite-hull
      intersection at step -1, a checked ordinary post-step closure, or final owner0 step15
      guarded_owner_cover_empty covering every CLOSED row meeting [13/32,27/64], including rows25/26/27
      and both boundary singletons. Complete16 updates without closure is criterion-missed for
      this fixed one-round recipe; conditional feasibility remains unresolved. Partial/resource
      stops are incomplete; malformed, altered premises or failed proof replay are refused.
      No physical counterexample, global proof, mask exclusion or census admission.
  instrument: packing/devtools/produce_n17_conditional_owned_hull.py and packing/devtools/verify_n17_conditional_owned_hull.py
  instrument_ready: true
  regime: Accepted H290 full17 numeric-cap final domain and accepted exp280 same-object full
    centered PASS_STALL; U=L=1169/250, V=935106018721/200000000000, B=1, original24 closed cells
    and D4. Label1/owner0 CLOSED half-angle guard [13/32,27/64]. Accepted exp282 exact finite
    certificate and fresh replay supply exactly5 selected target points; old owner0 hull has20
    vertices. Retain all20+5 and canonical convex hull<=48, no fallback or dropped points. All
    parent rows/intervals/references/outer/residual and other groups unchanged. One16-owner
    no-refinement round, accepted parent order excluding0 then0 last; square6/owner12 stays
    coarse. Core octagon, hull48, min_width2^-22, max_live=current live count<=64; splits=0.
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: 600s production plus300s fresh replay, combined900s/TERM900/KILL910; sampled4096MiB
    RSS.
  prereqs:
  - H-290
  - H-292
  replication: false
  registered: '2026-10-07'
  notes: Producer34 target-free controls passed1.33s; independent checker38 passed3.27s plus the new deadline control passed0.16s; author final39 passed1.49s. Ruff/BasedPyright/format zero for producer, checker static checks zero. Sole-Astra
    mathematical source review clear. Exact child-shaped sorted JSON/ChildStream canonical EOF
    roundtrip, off-grid witnessed compression, all-finite touch/cross/noncross, guard boundary-live/empty,
    partial-prefix and resource/refusal controls. No actual conditional child or intersection
    evaluated.
---
# Parent-Guard Owned-Hull Continuation

This experiment uses accepted H290 and the same-object centered exp280 PASS_STALL as
explicit parent premises, together with accepted exp282’s fresh exact finite
certificate. It does not construct a fresh wall seed or transplant the five conditional
points into an unconditional parent.
The new schema retains ancestry, the closed guard, finite proof receipts,
canonical/compressed object identities and the full original numeric frame.

Owner0 starts with the canonical convex hull of all20 prior vertices and all5 exact
selected target points.
Exact origin witnesses distinguish old vertices from selected points.
All other groups and every original closed row, interval, reference, outer polygon and
residual polygon are unchanged.
The augmented hull must fit48 vertices; there is no fallback or silent truncation.

Before updates, scan all finite hull pairs in lexicographic order, including points and
segments. Any exact nonempty owned-hull intersection is a conditional contradiction,
including a shared boundary point.
Otherwise run at most one16-owner round with owner0 last and square6/owner12 unchanged.
Splitting is disabled by passing the current live count; the producer must report zero
splits, unchanged partitions and groups of at most48 vertices after every certified
update.

An ordinary checked closure has priority.
After the final owner0 update, the guard-specific terminal requires every CLOSED row
intersecting the guard to have no residual polygon: rows25,26,27, including both
singleton boundary intersections.
The fresh checker reconstructs the exact roster, references and intersections.
Empty row26 alone supplies no terminal proof.

The producer’s closure is a candidate.
A clean independent process replays the complete conditional initialization and every
step through canonical EOF and binds the actual closure witness.
Only PASS_CONDITIONAL_CLOSED meets the primary criterion.
Complete16 nonclosed updates miss this fixed one-round criterion and leave conditional
feasibility unresolved.
Partial/resource stops are incomplete; proof or custody failures are refused.

The guard excludes the known endpoint chart0/1, so no unconditional endpoint monitor is
applied to this conditional child.
Accepted parent endpoint retention and the separate exp282 endpoint control remain
premises. A checked closure excludes only the accepted parent domain restricted to this
closed guard.
It supplies no full-mask exclusion, ordinary census admission, global cover
or optimality claim.
Existing generic root admission must continue refusing this child schema and ancestry.

The frozen production600s and fresh300s phases share one900s lease with TERM900/KILL910
and sampled4GiB RSS. Parent intake permits a10MiB seed and512MiB compressed/2GiB decoded
node. The new child permits64MiB compressed/512MiB decoded; final/report output is64MiB.
No retry, refinement or resource relaxation is allowed after launch.
Fresh descriptor construction copies only the frozen producer’s child path and
canonical/compressed identities; it changes no scientific parameter.

The conditional ownership implication is sole-Astra reviewed hand mathematics.
Exact finite and sequential checks provide the stated computational assurance, not an
independent mathematical derivation or end-to-end formal theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
