---
title: H-051 — a blinded n = 68 public-parent surgery pilot matches the released child
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-051
  kind: hypothesis
  claim: >-
    Starting only from the hash-verified public n = 68 parent, a proposer isolated from
    all child-bearing data and limited to the frozen delete/reinsert, connected-block
    shear, contiguous-strip move, and local-reoptimization grammar emits an independently
    valid packing whose certified side upper bound is no greater than the released
    child's reported side, within a tier-S budget of at most 1e9 dynamic pair tests.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:5', 'search:7', 'search:8', 'search:20']
  criterion:
    shape: determination
    metric: >-
      independently valid proposer output with certified side upper bound compared with
      the released n = 68 child's reported side after the proposal is frozen
    direction: >-
      accepted only if at least one output matches or beats the released child's reported
      side; rejected if the full counted budget completes with no such output; unresolved
      if provenance, blinding, precision, validity, or work-accounting guards fail
    threshold: released n = 68 child side
  instrument: >-
    Agenda-012 BC-113 separates an agenda-reading coordinator/validator from a fresh
    proposer with no inherited task history and no prior receipt of X-011, agenda-012,
    this hypothesis, or any child-bearing source. The coordinator builds the validator,
    sanitized launch card, and isolated allowlisted parent snapshot. Inside that
    network-disabled snapshot, the fresh proposer version-stamps its implementation and
    freezes the exact schedule under the registered move grammar before emitting target
    output. The child blind lifts only after proposer output is immutable; inability to
    attest the separation stops the run before measurement.
  instrument_ready: false
  regime: >-
    n = 68 only, under exactly one BC-109 serialization model. Without inspecting the
    child or the released gain, BC-109 selects and hashes the first compatible,
    independently valid parent model in the fixed order `declared:<stable-id>`
    lexicographically, `nearest-6`, then `truncate-6`; no child-bearing fact may change
    that arm. After proposer output is immutable, the selected parent's precision and the
    corresponding child model must pass the gain-relative surgery-grade contract or the
    result is unresolved by precision refusal; never fall through to another model. All
    quantities use a wall-aligned Cartesian frame normalized so each small square has
    side 1 and the container has side L. Published-to-rigid Euclidean displacement,
    compatible-pose corner ambiguity width, container-side interval width, and every
    signed wall/pair-separation interval width must each be at most one quarter of the
    released 7.68618004216131e-5 gain. A point-valued or rounded reported side must lie
    inside the retained side interval; a source-declared upper or lower bound instead
    requires the full interval to preserve that one-sided direction.
  instance: {axis: n, point: 68}
  priority: 1
  cost_estimate: >-
    tier S, capped at 1e9 dynamic pair tests and one 180-minute agent block; the counted
    proposal schedule is frozen by the fresh proposer before it receives any
    child-bearing data
  prereqs:
  - exactly one compatible and valid parent model frozen without child or gain inspection
  - fresh proposer, sanitized launch card, and isolated allowlisted snapshot with network disabled
  replication: false
  registered: '2026-09-01'
  notes: >-
    This is one calibration cell, not a verdict on H-030's two-of-six claim and not an
    independent-discovery claim. A valid miss rejects H-051 under this grammar and budget;
    it does not reject public-parent surgery under a different preregistered grammar.
    BC-113 records the proposed decision with `needs_review: true`. H-051 remains
    registered because the ledger excludes review-pending rounds from derived status.
    After agenda-013 BC-120 independently replays and explicitly passes the result,
    BC-121 applies the frozen disposition by clearing `needs_review` without changing the
    decision.
---
# H-051 — Blinded `n = 68` Surgery Calibration

The released improvement is large enough to separate a real response from the rounded
source floor once BC-109 freezes a child-independent parent arm and a sealed
corresponding child result.
The information barrier is part of the instrument.
The agenda-reading coordinator may validate and compare, but may not propose; the fresh
proposer receives neither these documents nor child-bearing data.
Role separation, a sanitized launch card, and the isolated input allowlist are all
mandatory.

## Measurement contract

BC-109 first resolves SVG transforms into global coordinates and identifies the square
container rectangle `(x0, y0, W, H)`. For candidate mathematical side `L`, it maps a
global SVG point `(X,Y)` to `(L * (X - x0) / W, L * (y0 + H - Y) / H)`. Thus the
mathematical frame has lower-left origin, wall-aligned axes, container `[0,L]` by
`[0,L]`, and unit squares constrained to side exactly 1; the released gain and every
threshold are in these unit-square-length coordinates, not pixels or viewBox units.
Vertex correspondence follows the source polygon order after testing the four cyclic
shifts and both windings; an unresolved tie is a typed ambiguity, not a smaller error.

Each serialization model maps a published decimal vertex to a closed rectangle in global
SVG coordinates and retains the published decimal itself as its nominal point.
A rigid unit-square pose is compatible only when the inverse image of every one of its
matched mathematical corners lies in the corresponding source rectangle; an empty
compatible-pose set is a precision refusal.
For square `i` and corner `k`, let `C[i,k]` contain that mathematical corner over all
compatible poses and sides.
The corner-ambiguity statistic is the maximum, over `i,k`, of
`sup(norm2(p - q) for p,q in C[i,k])`. The published-to-rigid displacement is the
maximum distance, over compatible poses, from a mathematical corner to the affine image
of its nominal published decimal at the same `L`. A unique projection can therefore have
zero ambiguity but still fail on displacement.

For a candidate side `L` and square corners `P[i]`, the signed wall clearance is
`min(p.x, p.y, L - p.x, L - p.y for p in P[i])`. For unit axis `a`, define
`axis_gap(a,A,B) = max(min(a dot B) - max(a dot A), min(a dot A) - max(a dot B))`. The
signed pair separation is the maximum `axis_gap` over the edge-normal axes of both
squares. It is positive for separation, zero for contact, and negative for overlap.
BC-109 encloses each wall and pair quantity over the compatible pose and side boxes; the
reported width statistic is the largest of those interval widths.

A point-valued or rounded source side must belong to the retained side interval.
If the source explicitly declares an upper bound, the interval’s upper endpoint must be
no greater than that bound; for a declared lower bound, its lower endpoint must be no
smaller. Small width without this relation is not surgery-grade.

H-051 has one arm and one pair-test budget.
Without inspecting the child or the released gain, BC-109 selects the first compatible,
independently valid parent model in this fixed order: source-declared models by
lexicographic stable id, then `nearest-6`, then `truncate-6`. It hashes that parent-only
selection receipt and never changes it.
After proposer output is immutable, the validator applies the gain-relative precision
threshold to the selected parent and evaluates the corresponding child model under the
same full contract. A parent or child precision failure records a refusal, and a later
model cannot rescue the registered result.
BC-113 retains the resulting criterion decision with `needs_review: true`; the ledger
shows the round under Needs review and does not use it to derive this hypothesis’s
status. BC-120 independently replays and challenges it; only an explicit pass authorizes
BC-121 to clear `needs_review` on the unchanged decision.
A caveat, discrepancy or inability to reproduce leaves H-051 registered and the disputed
measurement visible.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
