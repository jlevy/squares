---
title: H-094 — reweighting and support changes beyond the fixed-atom obstruction
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-094
  kind: open_question
  claim: >-
    Which changes to relative atom weights and D4 site orbits overcome the retained
    fixed-weight coverage obstruction and permit a stronger n = 11 certificate?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    Nonnegative rational atomic measures; the target side, net, witness geometry,
    site set and row-generation rule must be fixed for each proposed test.
  instance: {axis: n, point: 11}
  registered: '2026-09-06'
---
# H-094 — Change Weights and Sites

The
[contributed strategy, A3–A4](../../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md)
proposes support seeding followed by unrestricted pricing.
The
[fixed-weight obstruction](../series/series-000-smoke-and-calibration/experiments/exp-111-h-091-core-shrink.md)
leaves changed relative weights and sites open.
H-070’s rejected inset/release comparison covers its particular seed rule.

The first proposed discriminator is a finite rational covering LP on retained D4 site
orbits and exact bad-pose rows, transported to a selected target with their geometry
checked.
An exact dual floor of eleven rules out a mass-below-eleven certificate on those
sites at that target.
A smaller finite-row objective requires global separation before it can support a bound.

If that screen justifies new sites, use active witness boundaries or intersections to
propose orbit additions or splits, then compare the released search with an unrelated
seed. Refining support at several scales remains the same atomic proof language.
Moving sites without changing incidence cannot improve the fixed incidence LP.

Register each measurable successor with its rows or row-generation rule frozen before
its comparison. Retain a fixed-site obstruction at its stated scope; reopen that family
only when its sites, target or witness geometry changes.
Stop a seed variant that fails its declared matched comparison, without concluding that
every support prior fails.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
