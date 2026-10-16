# Person Profiles

This directory holds the records behind the site’s person profiles and the reviewed
joins from credited names to those records.
[Attribution Policy](../../attribution.md) owns the naming and credit rules the records
apply.

## Layout

| Path | What it holds | Contract and schema |
| --- | --- | --- |
| `people/<id>.md` | One record per person: a stable id, display and real names, aliases, account links, sources and an optional short biography | `packing.squares:Contributor/v1`, [`schemas/contributor.schema.yaml`](schemas/contributor.schema.yaml) |
| `occurrences.yaml` | Every reviewed span of a credited name in the register, bibliography and case records, joined to a person record or left unresolved, with PDF inspection receipts | `packing.squares:ContributorOccurrences/v1`, [`schemas/occurrences.schema.yaml`](schemas/occurrences.schema.yaml) |
| `schemas/` | The two schemas, named after the record kind each validates | — |

Each record’s filename is its id, in lowercase words joined by hyphens.
Person records live in `people/` and nothing else does, so no other file’s name can be
read as a person’s. The rest of `packing/` follows the same layout: in
`packing/campaign/`, each kind of record has its own directory and its schema sits in
`schemas/`. Each record names its schema in its `softschema` header by a relative path,
such as `../schemas/contributor.schema.yaml`, and the loaders in `sqpack.contributors`
and `sqpack.contributor_occurrences` refuse a record whose header names another one.

## Tools

Run these from `packing/`:

- `python -m devtools.contributor_census` summarizes the census: resolved, unresolved
  and non-person spans, and the PDFs still awaiting inspection.
- `python -m devtools.contributor_census --stale` lists every reviewed span whose source
  text has changed.
- After merging new credit records, `python -m devtools.contributor_census --reconcile`
  rewrites `occurrences.yaml`. It drops stale spans and adds new ones.
  A new span is joined only when its exact label is already reviewed as one person, or
  when exactly one record claims that spelling with sources.
- `python -m devtools.render_contributors` renders the profile pages under `profiles/`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
