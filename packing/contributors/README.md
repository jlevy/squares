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
Manual occurrences can reference structured JSON figure credits as well as YAML and
generator constants: `record_key: "$"` selects the document root, and `field` remains an
exact pointer. These joins preserve figure credit identity; they do not create primary
result authorship or invent new result IDs.

## Canonical Records and References

Person identity, source authorship and registered results are separate records.
A profile is not a second result ledger, and a resource owner is not automatically the
author of every result that cites the resource.

| Relationship | Stored reference | Validation |
| --- | --- | --- |
| Profile → evidence | `sources[].id` identifies a source inside that person record; `archive_path` is repository-relative and `url` is public | The contributor loader checks source IDs, repository boundaries and allowed URLs |
| Identity field → evidence | `provenance[].field` is a JSON Pointer relative to `contributor`; `sources` names that profile’s evidence IDs | The pointer and each supporting ID must resolve; supported identity fields require provenance |
| Bio → evidence | `bio_sources` names the profile’s source IDs | Required when a biography exists; the body is reader-facing prose, never parsed for structured data |
| Occurrence → original field | `origin.path`, `origin.record_key`, `origin.field` locate a structured field; `expected_text` preserves its complete value | The occurrence loader verifies the live field, exact label span and non-overlap |
| Occurrence → person | A resolved occurrence stores `contributor_id` and `evidence` source IDs from that profile | Unknown profiles or missing evidence fail; unresolved and non-person rows carry a note and no person ID |
| Result → source | The result register’s `attribution.source_keys` and `builds_on.source_keys` reference bibliography keys | Existing register/bibliography checks validate those references; their attribution roles remain distinct |
| Resource → profiles | The shared `site_resources` projection derives explicit curated bylines and profile IDs | Resource relationships support navigation, not inferred authorship; profiles store no duplicate resource list |

The profile contract is an enforced `frontmatter-md` artifact with envelope
`contributor`. The occurrence manifest is an enforced pure-YAML artifact without an
envelope; its payload consists of `occurrences` and `inspections`. Both schemas reject
unknown fields.
Contract identity and the declared schema path are checked by the project
loaders as well as JSON Schema validation.

JSON Schema establishes field shapes and allowed values.
The semantic loaders establish cross-record integrity: identity provenance, source
paths, source text, span bounds, evidence references and URL safety.
Passing one layer does not replace the other.
The schema gate runs both through the project’s registered record checks.

See [Walter Stromquist](people/walter-stromquist.md) for a complete evidenced profile,
and [the occurrence manifest](occurrences.yaml) for the corresponding reviewed joins.
The bibliography’s printed authors and dates remain in
[`resources/bibliography.yaml`](../resources/bibliography.yaml), under its own contract.
Do not extract a year from a biography, archive path, repository name or capture date.

## Derived Presentation

[`site_tallies.py`](../devtools/site_tallies.py) computes the shared summaries.
[`profile_records.py`](../devtools/profile_records.py) derives current record IDs from
the register and case evidence, including unresolved priority and family scope.
A theorem-wide family scope counts as current only where its `record_scope.assessment`
says so, and the gate holds that assessment to the family’s maintained comparison
([`deficiency_family.py`](../cases/asymptotic/deficiency_family.py)); without one it is
unassessed. Its `load_record_index()` result is shared by a render; intersect with
primary-authored IDs through `current_record_ids()`. Use `record_input_paths()` in build
dependencies. `python -m devtools.profile_records --json` reports the complete index for
review. A result with an unassessed facet can still count once through another current
facet; only unassessed IDs without any current facet can increase the tally.
Do not add stored `result_count`, `record_count`, `credit_count` or activity-range
fields to person records: these would duplicate data and drift after intake.

- **Results:** distinct registered result IDs with reviewed primary authorship.
  A bibliography `source-author` join in a primary attribution source establishes an
  author, subject to that source’s reviewed prerequisite roles.
  A packet containing work by several people does not give them all authorship of every
  result.
- **Records:** the current subset of primary Results across all result kinds.
  Family-specific currentness and unresolved priority come from the shared record
  classifier, not profile fields or profile-specific supersession rules.
  Tied entries that carry one identical attribution are each current
  ([Several Reports at One Count](../campaign/result-import.md#several-reports-at-one-count)).
  Count each result once even when it retains several cases or kinds of contribution.
- **Credits:** distinct results explicitly crediting the person in a non-primary role.
  Repeated mentions count once; someone primary on a result cannot also receive a
  non-primary credit for it.
  Merely citing a source does not manufacture a personal credit.
  The directory total counts person/result pairs.
- **Significance:** Results, their Records subset and Credits use the reported result’s
  significance. An S5 result by A crediting B and C produces one S5 Result for A and one
  S5 Credit each for B and C.
- **Years active:** original authored publication years and explicit discovery/proof
  dates. Later reuse, citations and imports do not extend the range.
  Undated work stays unknown.
  A case improvement cannot borrow the original finder’s year.
- **Project cards:** primary Results require exact project/source relationships and
  reviewed source authorship, subject to source-specific prerequisite exclusions.
  A resource with no resolved byline profile IDs can retain Results through reviewed
  non-person or unresolved bibliography author spans.
  Received Credits still require identified people and scoped source relationships.
  Acknowledgments and later citations do not establish primary authorship.
  An author’s unrelated work and credits given by the project do not enter the tally.
- **Resources:** the same deduplicated curated inventory drives homepage cards, profile
  cards and directory counts.
  These are resource relationships, separate from Results and Credits.

A publication can support activity years and appear as a resource without a registered
result. If it contains an unregistered substantive result, review and register that
result through the normal intake process; never fabricate a result merely to fill a
profile count. The
[attribution policy](../../attribution.md#results-records-credits-and-activity-years) is
authoritative for these semantics, and the
[design contract](../devtools/templates/paper-design.md#person-profiles) defines
display.

## Updating the Records

1. Inspect the primary source and check for an existing person ID. Aliases suggest
   candidates; they do not authorize an identity merge.
2. Add or update the person’s evidenced identity fields, typed links and provenance.
   Keep the stable published ID. Unknown names, accounts and bios remain absent.
3. Add a missing authored source to the bibliography only with its actual author and
   publication evidence.
   Keep the human archive index and bibliography consistent.
4. Review exact occurrence spans and roles against those sources.
   Preserve original text; resolve each identity with supporting IDs from its person
   record. Never make a broad surname replacement or treat a source packet’s byline as
   every result’s author.
5. Run structural and semantic checks, then the census stale check.
   After an upstream merge, inspect reconciliation’s dropped joins before resolving new
   proposals.
6. Audit profile/result coverage and inspect PDF credits explicitly.
   A linked paper is not evidence that every author, acknowledgment and reference in its
   PDF was reviewed; record inspection scope honestly in `inspections`.
7. Rebuild the site and inspect the profile, directory, result links and resource cards.
   Run the applicable validation tier before committing, and update the plan/beads with
   remaining unresolved identities or unregistered work.

Run the pinned project SoftSchema CLI on self-describing artifacts, for example from
`packing/`:

```bash
uv run --frozen --all-extras --group dev softschema validate contributors/people/walter-stromquist.md
uv run --frozen --all-extras --group dev softschema validate contributors/occurrences.yaml
uv run --frozen --all-extras --group dev softschema repair --check contributors/people/walter-stromquist.md
```

The project’s contributor loaders and schema gate must also pass; CLI shape validation
alone cannot establish cross-file identity or attribution correctness.

## Tools

Run these from `packing/`:

- `uv run --frozen --all-extras --group dev python -m devtools.profile_coverage --minimum-significance 4 --json`
  reports existing-profile join gaps, unprofiled credit labels, authored sources needing
  registration review and pending PDF inspection, prioritized by S5/S4 relationships.
  Candidate identities are suggestions, never resolved joins.
  A source absent from a primary T-record is a review candidate, not proof that it lacks
  records elsewhere.

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
