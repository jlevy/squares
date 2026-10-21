# Person Profiles

This directory holds the records behind the site’s person profiles and the reviewed
joins from credited names to those records.
[Attribution Policy](../../attribution.md) owns the naming and credit rules the records
apply.

## Layout

| Path | What it holds | Contract and schema |
| --- | --- | --- |
| `people/<id>.md` | One record per person: a stable id, display and real names, aliases, account links, sources and an optional short biography | `packing.squares:Contributor/v1`, [`schemas/contributor.schema.yaml`](schemas/contributor.schema.yaml) |
| `occurrences.yaml` | One span per credited name the census extracts from the register, bibliography and case records, plus manual spans in fields it does not extract, such as the project-author constant; each is joined to a person record, left unresolved for identity review, or marked as not a person; then the PDF inspection receipts | `packing.squares:ContributorOccurrences/v1`, [`schemas/occurrences.schema.yaml`](schemas/occurrences.schema.yaml) |
| `schemas/` | The two schemas, named after the record kind each validates | — |

Each record’s filename is its id, in lowercase words joined by hyphens.
Person records live in `people/` and nothing else does, so no other file’s name can be
read as a person’s. The rest of `packing/` follows the same layout: in
`packing/campaign/`, each kind of record has its own directory and its schema sits in
`schemas/`. Each record names its schema in its `softschema` header by a relative path,
such as `../schemas/contributor.schema.yaml`, and the loaders in `sqpack.contributors`
and `sqpack.contributor_occurrences` refuse a record whose header names another one.

A span’s `start` and `end` count Unicode code points, as Python indexes a string, not
UTF-8 bytes or UTF-16 units.

## Tools

Run these from `packing/`:

- `uv run --frozen --all-extras --group dev python -m devtools.contributor_census`
  summarizes the census: resolved, unresolved and non-person spans, the manual spans in
  fields the census does not extract, the labels that may be a clause or an organization
  rather than a person, and the PDFs still awaiting inspection.
  When a span no longer matches its source, it exits 1 and points to `--stale`.
- `uv run --frozen --all-extras --group dev python -m devtools.contributor_census --stale`
  lists every reviewed span whose source text has changed, or whose source is gone or no
  longer parses, and exits 1 if there is any.
- After merging new credit records,
  `uv run --frozen --all-extras --group dev python -m devtools.contributor_census --reconcile`
  rewrites `occurrences.yaml` after validating the complete replacement.
  It preserves unchanged reviewed fields, including manual span boundaries, drops stale
  fields and adds the live spans of changed or new fields.
  New person spans remain unresolved for source-specific review.
  The report lists candidate profile IDs as suggestions and, as each new span’s `prior`,
  the dropped spans of its record with the same label, with their dispositions,
  identities, evidence and notes.
  It exits 3 when it dropped a resolved join, and exits 1 without writing when a manual
  field changed, since only a hand review can carry that join forward.
- `uv run --frozen --all-extras --group dev python -m devtools.contributor_census --draft PATH`
  writes every extracted span to `PATH` as an unresolved proposal, and refuses to
  overwrite `occurrences.yaml`.
- `uv run --frozen --all-extras --group dev python -m devtools.render_overview --output DIR`
  renders the site, including the profile pages under `DIR/profiles/`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
