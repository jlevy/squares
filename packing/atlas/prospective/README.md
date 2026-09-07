# Prospective Packing Atlas, `n = 101..324`

This directory is a provenance record.
It answers what geometry a source has published for each `n` in the audited range, and
under what reuse terms.
Where this repository keeps that geometry is answered by
[`known-best/`](../known-best/README.md), which covers the whole range.

![Audited source coverage from n equals 101 through 324.](source-coverage-101-324.svg)

## The Source-Availability Map

[`source-availability-101-324.json`](source-availability-101-324.json) is the complete
machine-readable selection and provenance map for all 224 cases, on an access audit
dated 2026-08-26. The SVG above is a generated view of that record.
Neither artifact contains contact, rigidity, chunk, or packing-grammar annotations, and
neither makes an optimality claim.

Within the audited range, every one of the 224 cases has selected geometry, and none is
recorded as having none.
That is scoped evidence rather than a claim that the search covered every site,
publication, or unpublished construction: source selection is recorded as *provisionally
complete* against the retained catalogue and UnitSquare evidence.
Extending the range beyond `n = 324`, or surveying other authorities, is new research
work that starts with its own audit.

## The License-Safe Seed Is Retired

[`manifest.json`](manifest.json) indexed a license-safe seed of 101 normalized witnesses
and house renderings — the 97 exact grids and the four UnitSquare cases — and excluded
the 123 Kingbird-selected cases pending licence review.
On **2026-09-07** it was replaced by a retirement record.
The 101 witnesses under `witnesses/prospective/` and the 101 renderings under
`rendering/` were removed, and the record points at
[`known-best/manifest.json`](../known-best/manifest.json), which retains one normalized
`Witness/v2` construction and one house rendering for every `n` in this range under the
same retention policy the seed was built to respect.
Nothing the seed indexed was lost.
The same cases are held once instead of twice, in the collection that also carries their
frontier records.

The retirement record keeps `annotation_status: prohibited-uncomputed`, so a reader who
finds it cannot take a retired seed for an annotation source.
It reports zero retained witnesses and zero retained renderings, which is what a
consumer counting this collection’s geometry should now read.

Two things did not move with the seed.
The four retained UnitSquare SVGs stay under
[`resources/web/prospective-packings/`](../../resources/web/prospective-packings/README.md),
where the known-best builder reads and fetches them: the same upstream bytes under the
same digest declaration, and moving them would move geometry its successor depends on.
The map stays too, because a seed being superseded says nothing about which sources
exist.

## The Audit as It Stood on 2026-08-26

The counts below are the audit’s own finding on the date it was taken, kept here as the
record of what the collection then asserted.

| Status | Cases | Meaning |
| --- | ---: | --- |
| Exact grid retained | 97 | The catalogue’s stated no-tilt grid rule is generated locally with exact coordinates. |
| Licensed SVG retained | 4 | UnitSquare geometry for `n = 103`, `105`, `110`, and `131` is retained under the licence identified in its dataset metadata. |
| Public SVG located; derived facts pending acquisition | 123 | Kingbird geometry was fetched and parsed during the access audit. The inspected catalogue page states no express reuse terms, so its SVG files are not retained. |
| No selected geometry located | 0 | No case in this audited range fell into this category. |

The third row is what decision `D2` of
[the expansion plan](../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md)
resolved, by applying the `n ≤ 100` retention precedent: each SVG is fetched once and
ephemerally, parsed to numerical centre-and-angle facts, and retained as `Witness/v2`
with its attribution and `raw_asset_retained: false`. No Kingbird SVG above `n = 100` is
retained in this repository, then or now.

## Rebuild

From `packing`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.map_prospective_sources --check
uv run --frozen --all-extras --group dev python -m devtools.build_prospective_atlas --check
```

Omit `--check` from the first command to regenerate the availability JSON and its SVG
view. The second checks the retirement rather than a build: that the record validates,
its pointer resolves, the map it names is present, and no seed witness or rendering has
come back.
Its `--update` refuses and names `devtools.build_known_best_atlas`, which owns
the geometry for this range now.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
