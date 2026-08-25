---
title: X-001 — the standing review and the search-philosophy capture
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-001
  title: The standing review and the search-philosophy capture
  date: '2026-08-23'
  author: Claude (agent), captured from the PR #4 branch
  campaign: packing.squares
  brief: >-
    Audit the toolkit documents, supply the experiment method they lacked, and capture
    the strategy layer - where search effort should point, and why pointing should beat
    scaling.
  sources:
  - docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md
  - docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md
  - docs/project/research/research-2026-08-22-infrastructure-for-packing-exploration.md
  - docs/project/research/research-2026-08-22-lean-for-packing-proofs-and-validation.md
  - docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
  proposes: [H-001, H-002, H-003, H-004, H-005, H-006, H-007, H-008, H-009, H-010, H-011, H-012, H-013, H-014, H-015, H-021, H-022, H-023, H-024]
---
# X-001 — the idea source this campaign’s registry was mined from

This campaign did not generate its own hypotheses first.
Two documents, written independently on the PR #4 branch, contain a fifteen-entry
hypothesis register and a strategy layer, and they are the exploration report this
registry is codified from.

They live under `docs/project/` rather than in this directory because they were written
as standalone research and review documents before the campaign existed.
This artifact is the pointer that makes the trail navigable and the reference check
meaningful; it does not restate them.

## What they are

**[The standing review](../../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)**
— ten findings (R-1…R-10) on what the toolkit documents were missing, a fifteen-entry
hypothesis register with kill criteria and budget tiers, a run protocol, and a series
plan S0–S6. Its main theoretical contribution is R-2: **for fixed angles, minimising `s`
is a linear program**, numerically checked by an independent implementation — a
1,056-constraint LP at Trump’s angles reproduced `s(11)` to solver precision and every
centre to `9e-16`.

**[A Search Philosophy for Square Packing](../../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)**
— the strategy layer.
Its registered premise is that record packings are unusually constrained and may have
low hit probability under named baseline proposers; H-012 must measure that conditional
claim before it is treated as a fact.
The response is cartography: **the map is the deliverable and records are corollaries.**

**Amended 2026-08-23.** Optima need not be isolated points.
The exact `n = 3` sliding family proves that a map keyed by terminal coordinates can
count its own quantizer; `n = 5` supplies an unresolved warning but not a rank or
connectivity proof. See [D-034](../../defects.md); terminal-component identity is a
precondition on the deliverable, not a detail of its implementation.

## What has been codified

| Registry entry | Source |
| --- | --- |
| [H-001](../hypotheses/H-001-angle-class-reduction.md) angle-class reduction | review H-1, merged with this campaign’s narrower two-tilt claim |
| [H-002](../hypotheses/H-002-lp-in-cell-polish.md) LP-in-cell polish | review H-2 — the register’s own top priority |
| [H-011](../hypotheses/H-011-small-n-census.md) small-`n` census | review H-11, from the strategy capture |
| [H-012](../hypotheses/H-012-record-basins-are-rare.md) rarity premise | review H-12, from the strategy capture |
| [H-003](../hypotheses/H-003-basin-frequency-and-contacts.md) through [H-010](../hypotheses/H-010-stromquist-triple.md) | review H-3 through H-10 |
| [H-013](../hypotheses/H-013-delta-continuation.md) through [H-015](../hypotheses/H-015-map-elites-illumination.md) | review H-13 through H-15 |
| [H-021](../hypotheses/H-021-endpoint-identifiability.md), open questions [H-022](../hypotheses/H-022-trump-local-geometry.md) and [H-023](../hypotheses/H-023-n5-terminal-connectivity.md), and [H-024](../hypotheses/H-024-record-angle-class-count.md) | readiness review: measurement-system and local-geometry gaps exposed while preparing the overnight agenda; H-024 splits the corpus-law half from H-001’s algorithmic comparison |

All fifteen review ids are now artifacts.
The registry versions are canonical where their criteria sharpen or correct the
historical prose.

## What this campaign contributed back

Three claims of its own, renumbered into the free range above the review’s block:
[H-016](../hypotheses/H-016-stock-annealer-reaches-standing-best.md) (the null,
refuted), [H-017](../hypotheses/H-017-budget-scaling.md) (budget scaling, demoted once
H-012 supplied a better instrument), and [H-018](../hypotheses/H-018-basin-entry.md)
(basin entry, one of the few strategy-bearing items runnable today).

And one correction that runs the other way: the review’s calibration ladder uses `n = 5`
and `n = 10`, which this campaign adopted as its positive control — and the
search-philosophy report then pointed out that **both are 45° mechanisms**, so passing
them proves the machinery and says nothing about finding an oblique record.
That correction is recorded in
[series-000](../series/series-000-smoke-and-calibration/README.md), whose controls are
now explicitly labelled machinery-validation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
