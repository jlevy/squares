---
title: X-032 — Route S fixed-support threshold-certificate compression
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-032
  title: Route S Fixed-Support Threshold-Certificate Compression
  date: '2026-09-15'
  author: Codex coordinator with delegated source-first audits
  campaign: packing.squares
  brief: >-
    Freeze one no-target compression family on T-025's exact atom-support universe,
    define its positive D4-orbit complexity and at-most-23 acceptance threshold, and
    separate T-026's support-and-rescaling provenance role from any future compression
    result.
  sources:
  - packing/cases/n11_threshold_certificate/certificate.json
  - packing/cases/n11_threshold_certificate/replay.py
  - packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md
  - packing/cases/n11_threshold_certificate/t-026-dilation-limit-proof.md
  - packing/campaign/explorations/X-024-two-lines-at-eleven.md
  - packing/campaign/hypotheses/H-156-threshold-certificate-past-3-82.md
  - docs/project/reviews/review-2026-09-14-small-n-significant-progress-mathematical-audit.md
  - docs/project/reviews/review-2026-09-14-n11-post-w5-route-selection.md
  - packing/campaign/agent-sessions/session-134-n11-route-s-admission.md
  proposes: [H-163]
---
# X-032: Route S Fixed-Support Threshold-Certificate Compression

**Status: preregistered admission, with no scientific target.** This report fixes the
objects, metric, and verdict boundary for BC-343 before any compression candidate is
produced.
It registers H-163 but does not allocate `exp-161`, run an optimizer, change an
atom, replay candidate coverage, or make a compression claim.
T-025 and T-026 retain their existing results and assurance levels.

## Frozen Control

The control is the exact T-025 endpoint certificate
[`certificate.json`](../../cases/n11_threshold_certificate/certificate.json), SHA-256
`3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`. It fixes all of the
following:

- container side `L = 191/50`, core side `B = 9977/10000`, 181 net directions, and D4
  symmetry;
- 584 positive point atoms in 79 D4 orbits;
- 320 positive two-of-three threshold atoms in 40 D4 orbits; and
- the theorem’s exact budget rule, total budget `685457679/62500000 = 10.967322864`, and
  complete closed-core domain.

The 119 orbit representatives expand to 904 atoms.
This count, rather than the JSON byte size or the number of distinct rational weights,
is the control value for H-163. T-025’s existing exact event-cell and interval
branch-and-bound routes remain the coverage decisions.
The admission tooling may authenticate and inventory the source, but this branch runs
neither route on a changed certificate.

## One Fixed-Support Family

Let `U025` be T-025’s ordered universe of 79 point-atom orbits and 40 threshold-atom
orbits. A member of the Route S family assigns one nonnegative rational weight to each
orbit in `U025`; every D4 image receives the same weight.
Weight zero makes an orbit inactive.
Every other field is fixed by T-025:

- point coordinates and threshold point triples;
- threshold value two and budget coefficient one;
- atom type, orbit membership, and canonical expansion order;
- `L`, `B`, the angle limit, direction net, D4 action, and closed-domain semantics.

The family permits sparse reweighting of an exact support *universe*. It does not permit
moving or coalescing sites, changing threshold triples, adding atoms, changing the net
or shrink, or substituting a different certificate language.
Those changes could be valuable, but they would test a different hypothesis.

A deterministic decompressor must take a canonical list of orbit representatives and
their rational weights, expand every D4 image in the frozen order, and emit a candidate
in the existing T-025 certificate format.
The admission analyzer must reject an unknown, duplicated, incomplete, or incorrectly
expanded orbit before any coverage decision.
The decompressed T-025 control must reproduce the frozen source bytes or a
field-for-field canonical equivalent with the same authenticated digest recorded in its
receipt.

## Preregistered Complexity and Verdict

For a family member `C`, define

```text
N+(C) = number of U025 orbit representatives assigned strictly positive weight.
```

The control has `N+(T-025) = 119`. The fixed compression threshold is `N+(C) <= 23`:
five copies of 23 account for only 115 of the 119 original orbit representatives.
Expanded atom count, distinct positive weights, denominator size, manifest bytes, and
independent coordinate parameters are useful diagnostics, but none may replace `N+`
after a target has run.

A future H-163 target confirms the claim only if all of these statements hold:

1. The candidate is produced from `U025` by the admitted deterministic decompressor and
   has `N+ <= 23`.
2. Exact arithmetic gives nonnegative rational weights, orbit-constant D4 expansion, and
   total budget strictly below eleven under T-025’s unchanged budget rule.
3. The existing exact event-cell sweep and method-distinct interval branch-and-bound
   both accept the complete T-025 closed-core domain and agree on the least charge,
   which is at least one.
4. A source-distinct replay authenticates the manifest, reconstructed certificate, and
   result without trusting an optimizer’s summary.
5. The manifest gives a short generating account of the retained orbit pattern; merely
   serializing the same complexity differently does not satisfy the proof-simplification
   objective.

An exact infeasibility certificate proving that no family member with `N+ <= 23` can
meet the frozen budget and coverage constraints refutes H-163. A bounded search that
finds no candidate is unresolved and may justify parking this family operationally; it
does not prove that no sparse reweighting or no simple proof exists.
A malformed source, failed mutation control, route disagreement, incomplete coverage, or
timeout is an invalid or unresolved instrument outcome, never a scientific negative.

## T-026 Is a Provenance Sentinel

T-026 rescales T-025’s atom weights uniformly and changes the shrink and direction net
to prove a dilation-limit lower bound.
Its 720- and 1440-step certificates therefore do not form the H-163 control, target, or
complexity baseline.
They remain a sentinel for two provenance facts: their atom coordinates, threshold
triples, and orbit structure come from T-025, and their weights differ by the documented
common factor before the dilation argument.

The admission analyzer may verify those identities without running T-026 coverage or
dilation replay. A mismatch shows that the Route S support inventory is not faithful to
the retained proof.
Agreement supplies no evidence that a compressed candidate covers the
T-025 domain or retains T-026’s stronger bound.

## Target-Blind Controls

Admission requires controls whose outcomes do not depend on a compression candidate:

- decompress the full 119-orbit T-025 manifest and recover the frozen source identity,
  inventory, budget, and D4 closure;
- accept a synthetic 23-positive-orbit manifest at the complexity boundary and reject a
  24-positive-orbit manifest before coverage is considered;
- reject duplicate, missing, off-support, wrong-type, wrong-threshold, non-D4, negative,
  and nonrational mutations; and
- verify only the documented support identity and uniform-rescaling relationship for the
  T-026 sentinels.

These controls admit a producer and checker.
They are not candidate certificates and cannot resolve H-163.

## Scope

Route S seeks a simpler proof of the already established endpoint result
`s(11) >= 191/50`; it does not seek a higher side in this family.
Success would not replace T-026’s stronger lower bound.
It would supply a substantially smaller exact certificate and a reusable way to describe
mixed point-and-threshold proofs.

The fixed-support restriction isolates sparsity from geometric redesign.
Failure within it leaves coordinate templates, new atom supports, different threshold
languages, and other proofs open.
No conclusion about any of those routes follows from this admission or from a later
bounded unsuccessful search.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
