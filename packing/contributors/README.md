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

- `uv run --frozen --all-extras --group dev python -m devtools.contributor_census`
  summarizes the census: resolved, unresolved and non-person spans, and the PDFs still
  awaiting inspection.
- `uv run --frozen --all-extras --group dev python -m devtools.contributor_census --stale`
  lists every reviewed span whose source text has changed.
- After merging new credit records,
  `uv run --frozen --all-extras --group dev python -m devtools.contributor_census --reconcile`
  rewrites `occurrences.yaml` after validating the complete replacement.
  It preserves unchanged reviewed fields, including manual span boundaries, drops stale
  fields and adds the live spans of changed or new fields.
  New person spans remain unresolved for source-specific review.
  The report lists candidate profile IDs as suggestions and retains the dropped spans’
  prior dispositions and notes for that review.
- `uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR`
  renders the site, including the profile pages under `DIR/profiles/`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
