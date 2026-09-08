# Retained Known-Best Packing Sources

This directory records upstream provenance for the `n = 1..100` known-best witness
corpus. [`sources.json`](sources.json) distinguishes retained upstream assets from
metadata-only source records.

## Kingbird Retention Policy

No express license or permission covering redistribution of the Kingbird catalogue SVGs
was located during the 2026-08-26 review.
The repository therefore retains no raw Kingbird SVG in this source inventory.
It retains attributed source metadata, normalized numerical center and angle facts in
the Witness/v2 corpus, and deterministic house renderings derived from those facts.
The retained Witness/v2 coordinate fields are the deterministic regeneration input.

This is a conservative repository-retention policy, not a legal conclusion.
The source metadata is not itself a geometry or feasibility claim.
Each witness carries its own finite-precision feasibility receipt and explicitly
disclaims exactness and optimality.
Live adapter audits are ephemeral and must not write source geometry; retaining raw
Kingbird assets requires an applicable license or express permission.

The metadata attributes the SVG and high-precision updates to David Ellsworth and the
original catalogue compilation to Erich Friedman, following the
[Kingbird catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html).

## The Range `n = 101..324`

Decision of 2026-09-07, under
[the atlas expansion plan](../../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md),
decision `D2`: the policy above applies unchanged to the 123 catalogue cases in
`n = 101..324` whose geometry the prospective audit located but did not retain.
Each is acquired once, ephemerally, by the atlas builder's `--fetch` path; the SVG is
parsed to numerical centre-and-angle facts, and only those facts, the attribution, and
the source metadata are retained, with `raw_asset_retained: false`.
The source-availability map records the state as
`derived-facts-acquisition-approved-2026-09-07`; its 2026-08-26 audit remains the
provenance record for which source served which `n`.
The
[survey of sources beyond 100](../../../../docs/project/research/research-2026-09-07-square-packing-sources-beyond-100.md)
found no source with express reuse terms that carries this range, so there is no
licensed alternative to prefer.
Express permission from the catalogue's author would allow raw retention and is an
owner action, not a prerequisite here.

## Retained UnitSquare Renderings

The `unitsquare/` files are retained public evidence renderings for the newer `n = 68`
and `n = 69` records.
Those renderings identify governed source receipts in metadata but expose only rounded
polygon coordinates, so the normalized witnesses preserve that limitation.
Their retained bytes are checked against the SVG digests independently declared in the
UnitSquare Release 1 `results.json`; the source inventory names those values
`upstream_declared_sha256`. Git and deterministic full-content replay remain the
integrity boundary for co-committed outputs.
Do not reformat these archival source bytes or replace them with the repository’s house
renderings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
