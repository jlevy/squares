# Known-Best Packing Atlas, `n = 1..100`

This atlas retains one complete geometry record for every frontier case from `n = 1`
through `n = 100` and renders every record with the repository’s deterministic house
renderer. The machine-readable discovery layer is [`manifest.json`](manifest.json).

[![The complete known-best atlas from n equals one through one hundred.](known-best-1-100.svg)](known-best-1-100.svg)

The composite is a native 10-by-10 SVG, not a screenshot montage.
Its 5,050 square polygons come from the same normalized witnesses as the individual
figures under [`rendering/`](rendering/). [`known-best-1-100.png`](known-best-1-100.png)
is the GitHub-facing raster preview; it carries the SHA-256 of its source SVG so the
atlas check rejects a stale preview.

The pipeline has four separate layers:

1. exact canonical grids, attributed Kingbird-derived numerical facts, or retained
   UnitSquare SVG renderings;
2. normalized [`Witness/v1`](../../witnesses/witness.schema.yaml) geometry;
3. numerical or exact feasibility receipts at the assurance the source supports; and
4. deterministic SVGs under [`rendering/`](rendering/).

Chunk decompositions do not belong in the source witness.
They live in separate, regenerable annotation artifacts with their detector version,
deterministic objective, tolerances, and limitations.
The current annotations are explicitly calibration-only because the 1–100 corpus was
inspected during their design.
This prevents a taxonomy invented from the corpus from being counted as independent
confirmation on the same corpus.

[`chunk-components.json`](chunk-components.json) is the exploratory layer that tests the
assembly intuition without crossing that boundary.
At the registered `1e-6`-radian angle and `1e-3` contact tolerances, 1,780 of 1,860
squares in the 36 non-grid records belong to a multi-square same-angle contact
component.
Twenty-five of those 36 records use no more than six such components and three
singletons. This is strong evidence for a broad **contact-assembly** description.
It is not yet evidence that every component is one of the enumerator’s narrower bar, L,
or rectangle skeletons.

The 36 non-grid records contain 169 multi-square components: 55 contact chains and 114
cyclic patches. Contact-normal equalities alone leave 859 internal slide degrees before
overlap intervals or wall contacts are applied, and 792 squares are wall-seated at the
registered contact tolerance.
A connected contact assembly is therefore not automatically a rigid chunk; the next
grammar must retain and price those slides.

The retained maximal-lattice detector establishes that stricter decomposition directly
for only 21 of 100 records.
Its other 79 results are recorded as `not-established`, not as failures: a maximal
polyomino may split into two allowed chunks.

[`chunk-partitions.json`](chunk-partitions.json) performs that split with a bounded,
deterministic exact-cover search over contiguous bars, filled rectangles, and corner Ls.
It certifies all 64 grid-derived records and 3 of 36 non-grid records inside the
six-chunk/two-free budget.
Two non-grid cases are conclusively outside that budget, 23 have no partition in this
candidate universe, and eight are search-capped and therefore indeterminate after the
declared 10,000-state limit.
The broad contact result and the narrow partition result therefore point in the same
direction: same-angle assembly is common, but rigid integer-lattice chunks are too
narrow as the only grammar for the interesting records.

The partition atlas evaluates every allowed exact free-square count, prefers an
in-budget certificate when one exists, then minimizes free squares before chunk count.
If an earlier free-count slice is capped, a later in-budget certificate still proves
existence, but the retained selection marks its free-square and chunk minimality as
indeterminate. A later out-of-budget certificate leaves both budget membership and
`F`/`C` minimality indeterminate; likewise, any later capped slice leaves an earlier
out-of-budget certificate indeterminate.
The atlas reports exact and near bands separately and types state-cap and
candidate-universe limitations.
It is calibration evidence only and emits no H-044 verdict.
The contrast is useful rather than embarrassing.
It says the corpus supports the chunk intuition while the current grammar and detector
do not yet support the proposed coverage claim.

[`chunk-evidence-profile.json`](chunk-evidence-profile.json) condenses the full non-grid
census into 36 source-stratified rows.
Its [`house-rendered overview`](evidence/non-grid-chunk-evidence-profile.svg) shows
contact coverage, component count, free squares, largest component, internal slide
degrees, the narrow partition disposition, and the broad-budget flag for every case.
Ten cases are fully covered, 27 cover at least 90 percent, 33 cover at least 75 percent,
and 35 cover at least half; `n = 5` is the lone zero-contact outlier.
Orange row outlines identify the only registered-to-regularized changes (`n = 68`, `69`,
and `71`) instead of hiding tolerance sensitivity in an aggregate.

[`contact-assembly-grammar.yaml`](contact-assembly-grammar.yaml) records the proposed
revision as a versioned, schema-checked draft.
It keeps rigid lattice chunks as a strict subgrammar and adds contact scaffolds whose
tangential slides remain LP variables.
Its complexity tuple charges free squares, assemblies, internal slide degrees, angle
classes, mandatory contacts, and largest assembly size.
No scalar budget is frozen yet.

[`contact-enumeration-pricing.json`](contact-enumeration-pricing.json) prices the first
target-free implementation without reading atlas geometry.
Exact connected labeled counts grow from 15,104 at size 4 to 9,684,224 at size 5. The
exhaustive size-4 control reduces to 124 canonical labels and local LP solves; 26 pass
the local equations, which accept one fitted-angle class only and still omit walls,
non-edge separation, and container fit.
Mixed angle classes fail before an LP solve.
The isomorph-free size-5 path reduces 1,533,696 topology colorings to 11,013 exact
orbits. Those abstract representatives are retained without geometry or local LP
outcomes; the earlier 9,296,855,040-image raw path remains only a differential oracle.

[`contact-full-cell-control.json`](contact-full-cell-control.json) is a separate
literal, source-free structural control for CG-010. Its three-square axis-aligned L has
eight available non-edge axis-and-order branches; the retained fixture selects one raw
cell, checks all 48 D4-by-relabeling images, emits one canonical label, and performs
zero LP solves. The artifact validates representation, canonicalization, typed caps, and
work accounting only.
It contains no centres, side, geometry, container-fit result, packing feasibility claim,
or optimality claim.

[`contact-overlays.json`](contact-overlays.json) indexes five deterministic visual
strata from the registered descriptive census: `n = 11`, `28`, `40`, `68`, and `89`.
Every SVG under [`contact-overlays/`](contact-overlays/) uses the same house renderer as
the base atlas. Dashed orange lines join square centres or a centre to a seated wall;
they show tolerance-qualified graph incidence, not exact physical contact loci or
rigidity. The numerical overlay feature is deliberately distinct from the renderer’s
certified exact-contact feature, and the gallery remains calibration-only.

## Coverage Policy

Exact integer records use a canonical row-major subset of the corresponding grid.
Noninteger catalogue records use attributed Kingbird-derived numerical center and angle
facts retained in Witness/v1; the upstream SVGs are not retained in this source
inventory because the review located no express redistribution terms.
This is a conservative retention policy, not a legal conclusion.
The newer public UnitSquare renderings supersede the older Kingbird geometry at `n = 68`
and `n = 69`; their six-decimal polygon coordinates are explicitly recorded as
rendering-derived numerical evidence, not as the unavailable interval boxes named in
their metadata.

Every witness limits its claim to feasibility of the retained construction.
The phrase “known best” comes from the frontier register and never turns a numerical
witness into an optimality proof.

## Rebuild

From `explorations/packing`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --check
uv run --frozen --all-extras --group dev python -m devtools.census_known_best_chunks --check
uv run --frozen python -m devtools.render_known_best_contact_overlays --check
uv run --frozen python -m devtools.profile_known_best_chunks --check
uv run --frozen python -m devtools.price_contact_enumeration --check
```

Source acquisition is an explicit network operation and is not part of CI:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --fetch
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
```

The first command acquires only missing UnitSquare assets unless `--refresh` is
requested; Kingbird live audits are ephemeral and write no geometry.
The second rebuilds witnesses, individual house renderings, the SVG and PNG composite,
the manifest, and frontier witness links from retained inputs.
PNG regeneration uses macOS `sips` when available and ImageMagick otherwise; check mode
reads the embedded source-SVG receipt without invoking either renderer.
Git remains the integrity boundary for co-committed outputs.
Upstream asset integrity uses only hashes declared independently by a source; the PNG’s
local source-SVG receipt tracks derivation and is not source evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
