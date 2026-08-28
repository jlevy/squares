# Enumerated Contact-Scaffold Atlas

This collection stores the complete abstract size-five slice of the draft
contact-assembly grammar within one fixed scope: one semantic angle class, no wall
colors, and a signed `u`- or `v`-normal color on every present edge.
It contains 11,013 orbits over all 21 connected unlabeled five-vertex graph topologies.

The collection is deliberately geometry-free.
An entry says which abstract vertices have a signed `u`- or `v`-normal contact relation.
It says nothing about square positions, tangential offsets, wall seating, non-edge
separation, container fit, local realizability, or packing feasibility.

The [size-five topology overview](rendering/contact-scaffolds-size5-overview.svg) shows
the 21 abstract graphs and their orbit counts.

The cards are incidence diagrams laid out for reading.
Their positions are not square coordinates.

## Stable Identities

[`contact-scaffolds-size5.json`](contact-scaffolds-size5.json) stores each topology once
and gives its orbit representatives as fixed-width base-four strings.
A stable identity has the form `T5-NN/<digits>`:

| Digit | Contact color |
| --- | --- |
| `0` | `u` normal, negative sign |
| `1` | `u` normal, positive sign |
| `2` | `v` normal, negative sign |
| `3` | `v` normal, positive sign |

Digits follow the topology’s lexicographically ordered edge list.
The code is the minimal representative under the topology automorphism group and the
eight container symmetries.
For example, `T5-01/0000` is the first retained orbit and `T5-21/0123230121` is the
last.

Compression does not remove records.
The 21 topology records contain exactly 11,013 unique codes, and the public iterator
decodes them into 11,013 `ContactScaffold` objects.
Independent Burnside counts and a separate all-orbit reconstruction agree with every
per-topology count.

## Inspect One Record

From `explorations/packing`, query a retained identity without re-enumerating or writing
files:

```bash
uv run --frozen python -m devtools.build_contact_scaffold_atlas --show T5-01/0000
```

The JSON response contains an `abstract_scaffold` with five vertices, signed contact
edges, and empty wall-color lists.
Its claim status and semantics explicitly exclude geometry, realization, feasibility,
and a packing verdict.
Unknown topologies, malformed identities, invalid digits, and valid-looking codes that
are not retained orbit representatives fail instead of being silently canonicalized.

Python consumers can call `scaffold_by_identity(atlas, identity)` for direct lookup or
`iter_atlas_scaffolds(atlas)` for ordered traversal.
Both validate the retained atlas before returning a scaffold.

## Rebuild and Validate

Regenerate or byte-check the complete artifact and its house overview:

```bash
uv run --frozen python -m devtools.build_contact_scaffold_atlas --update
uv run --frozen python -m devtools.build_contact_scaffold_atlas --check
uv run --frozen pytest -q tests/test_contact_scaffold_atlas.py \
  tests/test_contact_isomorph_free_burnside.py
```

The schema prohibits geometry channels.
Cross-field controls enforce topology order, edge widths, representative order and
uniqueness, per-topology counts, and the 11,013 total.
The size-five local-LP stage remains unrun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
