---
title: Project Changelog and Recent PR Backfill
description: A YAML-backed project history rendered for GitHub and at the bottom of About
author: Codex, for the repository owner
---
# Feature: Project Changelog and Recent PR Backfill

**Date:** 2026-10-13

**Author:** Codex, for the repository owner

**Status:** Implemented in PR #590; final validation and publication pending.

**Tracking:** `think-j7nb` (planning), `think-jpto` (implementation epic)

**Workflow:** W7 pipeline-improvement planning

## Overview

Add a project-wide changelog that explains what each meaningful merged PR or stack
contributed. Store the entries in YAML under a Soft Schema contract, with Markdown for
reader-facing descriptions.
Generate a readable GitHub document and embed the same history at the bottom of the
website’s existing About page.

Backfill the latest 36 PRs merged into main, using their descriptions, reviews and the
current project record.
Each entry should usually be a sentence to a few lines.
Larger efforts, such as regularization, can have a short introduction and several nested
bullets.
Describe delivered work at a useful intermediate level: a new record admitted, a
proof imported, a pipeline repaired, or a regularization capability added.

## Goals

- Cover record admissions, research imports, pipeline improvements, regularization,
  website changes and substantive documentation work.
- Give each selected PR a traceable place in an entry or a documented editorial
  disposition; group actual stacks without repeating the same achievement.
- Reuse the evidence and prose already available, editing them for readers who have not
  followed the PR discussions.
- Maintain one authoritative YAML record and consistent GitHub and website views.
- Make About an index of launched papers, PDFs, results and site features, with direct
  links and known versions.

## Non-Goals

Another results register, per-commit or per-bead reporting, a new website page, and
automatic publication of machine-written summaries are outside this feature.

## Background

There is no project-wide changelog.
`PUBLICATION_HISTORY` in [`release.py`](../../../../packing/src/sqpack/release.py)
covers publication editions, which should remain distinct from this PR-level project
history.

The website’s About page is already generated as `about.html`. Its manuscript is
[`about-article.md`](../../../../packing/devtools/templates/about-article.md), whose
last content section is Documentation.
`about_page()` in
[`render_overview.py`](../../../../packing/devtools/render_overview.py) expands that
manuscript and sends it through kpress.
This is the insertion point; no new navigation item or site assembler is needed.

The existing PR template already separates results, dispositions, changes by purpose,
validation and limits.
The frontier register, intake requests, retained source packets, reviews and session
close records provide the evidence needed to edit those summaries.

## Design

### Editorial unit and depth

Use a dated entry with a short title, a Markdown summary, PR links and optional Markdown
bullets. Describe the contribution and why it matters.
For significant efforts, use bullets for independently useful pieces, such as policy,
reproducible tooling and verified admissions.
Do not turn every implementation file, fix commit or validation command into an entry.

Keep historical claims at their merge-time evidential status.
A reported proof import can be noteworthy without being a proof replay.
Admission, replay, adoption and an acknowledgement are different events.
Later corrections get a linked entry; the changelog does not derive old claims from
today’s result rungs.

For a formal stack, record only the layers delivered to main.
Freeze an entry’s PR membership and date once published.
Later deliveries from the same stack get another entry sharing `stack_id`, rather than
moving or enlarging an old announcement.
Related PRs sharing one public contribution can use `grouping: related`; this does not
assert formal-stack membership.
Follow-ups can also reference an earlier entry.

### About as a launch index

About must answer what has launched across papers, infographic PDFs, result records and
site features. Give each relevant entry direct, labeled links to those public artifacts,
with its component editions when known.
A reader should be able to go from the short announcement to the paper, downloadable PDF
or result page without opening GitHub.
Keep PR and supporting-record links as provenance, rather than using them as a
substitute for the launched artifact.

Store public destinations in optional `artifacts` items with `kind`, `label` and
`target`. Kinds distinguish papers, PDFs, results, pages and graphics.
Targets are canonical HTTPS addresses checked against the site URL registry.
Labels identify a current view when an old edition has no retained public address; never
label a moving latest-download URL as an archived edition.

Optional `publication` records a verification-evidence URL and, when evidenced, its
first-live UTC `date`. For an entry announcing several artifacts, this is the evidenced
UTC date when the complete announced set became public; omit it if that date is unknown.
Keep it separate from the entry’s merge date.
A merged or prepared change is not automatically a launched component.
Authoring/backfill checks public destinations and retains deployment or
publication-history evidence before presenting an artifact as launched.
Unknown historical first-live dates stay absent.

Render the changelog at the bottom of About with readable contribution titles, concise
summaries, optional subpieces, artifact links and component versions.
Distinguish a confirmed launch from project-only or prepared work in the wording.
The complete history should make it easy to find both the public deliverable and the
meaningful pipeline work behind it, without exposing the maintenance audit table.

### Authoritative record and contract

Use `packing/site-changelog.yaml`, with a sibling `site-changelog.schema.yaml`. The
payload is pure YAML; Markdown prose lives in block scalars.
The root `softschema` metadata names `packing.squares:SiteChangelog/v1`, its relative
schema path and its maturity.
Omit `envelope` for this root-level payload; do not write `envelope: null`.

The [draft schema](plan-2026-10-13-site-changelog.schema.yaml) and
[copyable examples](plan-2026-10-13-site-changelog.examples.yaml) accompany this plan.
They demonstrate the record shape, not a completed production backfill.

| Field | Meaning |
| --- | --- |
| `repository` | The canonical GitHub repository URL used to generate PR links |
| `entries[].id` | Stable entry identifier and permalink fragment |
| `date` | UTC merge date; for a grouped delivery, the latest merge date of the included PRs |
| `title` | Short plain-text contribution title |
| `pull_requests` | Nonempty, unique PR numbers represented by this entry |
| `summary` | Markdown description, normally one sentence to a few lines |
| `details` | Optional Markdown, usually a short nested bullet list for a substantial effort |
| `stack_id` | Optional verified formal-stack identity; repeated across later deliveries |
| `grouping` | Explicit `related` grouping for several PRs sharing a contribution without a formal-stack claim |
| `categories` | Optional structured labels: records, pipeline, regularization, site or documentation |
| `result_ids` | Optional record identities for linking, without duplicating their current state |
| `artifacts` | Optional labeled links to launched papers, PDFs, results, pages or graphics |
| `publication` | Optional publication evidence and known first-live date, separate from merge date |
| `releases` | Optional component/version references to authoritative release histories |
| `references` | Optional `{label, target}` references; HTTPS URLs or repository-relative paths |

The planning examples use `permissive` maturity and explicitly allow extension fields.
Before publication, settle the consumed fields and close the production contract under
`enforced`. `permissive` alone does not reopen a closed schema.
The current `validate_schemas` corpus requires `enforced`, so production integration
must use the settled contract rather than silently weakening that corpus.

Validate types and required fields structurally.
Check calendar dates, unique entry IDs, PR membership across entries, main-branch
delivery and stack membership at the appropriate semantic boundary.
A JSON Schema date format is only an annotation.
Never fetch GitHub during ordinary rendering: merge metadata and editorial decisions are
acquired during authoring and backfill, then committed as local inputs.
Retain the actual API `base_ref` for stacked PRs.
If it names a predecessor branch, `delivery_to_main` records the merge commit and its
repository commit URL after the importer verifies that same commit on local main’s
first-parent history.

### Shared rendering and placement

Add `devtools.render_changelog` with one validated entry model and a deterministic
Markdown renderer. It generates root `CHANGELOG.md`, including stable anchors and
absolute PR links, and provides `--check` for freshness.
The YAML remains authoritative; the generated Markdown is a reader view, not another
manually maintained source.

Add `{{CHANGELOG}}` after `{{DOCUMENTATION_BLOCK}}` in the About manuscript, before its
footer. Reuse the same entry renderer through `about_page()`, with the existing site
section typography. Show newest dates first, group entries under date headings and keep
metadata out of the reader’s way.
The initial history should remain fully available without a new page or navigation item;
add an `about.html#changelog` permalink.
Entry links use `#changelog-entry-<id>` in both reader views; date headings use a
separate `changelog-date-` namespace so neither can borrow another About heading.

Use the existing repository-link helper to resolve structured references and Markdown
links for each destination.
GitHub links resolve from the repository root; website links use the project’s canonical
published and repository addresses.
Preserve math through the existing kpress path.
Escape title and metadata text; accept paragraphs, links, emphasis, inline code, math
and lists in prose, and refuse raw HTML or unsafe link schemes.
About currently renders trusted Markdown, so this policy must be explicit.

Map the YAML as a registry and `CHANGELOG.md` as a generated view, and link the readable
view from README’s Repository Guide.
Account for `CHANGELOG.md` in the documentation filename rules.
Generated Markdown formatting must agree with Flowmark so the commit hook cannot make
`--check` drift.

### Component versions and release policy

Keep version authority in `packing/src/sqpack/release.py`, with distinct release units:

| Component | Shared artifacts | Policy |
| --- | --- | --- |
| `site` | Website and workbench public edition | Retain `PUBLICATION_HISTORY`; prepare `v0.6.0` as a minor release for the new changelog capability |
| `infographics` | Both 1–100 and 1–324 infographic SVGs, PDFs and PNG exports | Add one `INFOGRAPHIC_HISTORY` and version; either graphic changing advances the same version on the complete pair |
| `paper:<slug>` | One paper’s HTML, Markdown and PDF | Retain each paper’s independent history; another component changing does not advance it |

Before this implementation, the infographic family inherited the site version, while the
papers already had independent histories.
The family now versions independently of site cuts.
Import the already printed `v0.5.0` as its baseline using verified publication evidence;
do not infer a first-live date from a PDF filename or redraw date.
Keep existing public download addresses.
Their `20261008` suffix is a stable naming convention, not the semantic version.
Preserve the derivation receipts independently of release identity.

Choose bumps from the delivered reader-facing change:

- **Patch:** a correction, ordinary data/content refresh, or small styling,
  accessibility, usability or export fix within the existing scope.
- **Minor:** a substantial new capability, coverage expansion, visualization redesign,
  or substantial new paper exposition or methods.
  Reset patch to zero.

When a release contains both, minor wins.
Select one bump per component for the complete batch, not per fix commit.
Internal tests, source housekeeping and changelog-only bookkeeping do not independently
trigger a release. Neither a result’s significance score nor a stronger evidence rung
determines the version bump.

A reader-visible revision to either infographic must advance the shared family version
and rebuild both graphics and their PDF/PNG exports at that version.
This replaces the current ability to deliberately redraw changed graphics under the same
semantic version. A byte-identical rebuild is not a new edition; an untouched poster may
retain its published edition while the source record advances between deliberate
redraws.

Reuse `build_known_best_atlas.update_composites()` and `CompositeIdentity.stamp`, the
existing complete-family export checks and `cut_release` lifecycle.
Add an infographic cut mode or companion entry point; a site-only cut no longer owns
infographic numbering.
Hold the selected edition fixed during review, verify every advertised family output,
and publish the complete pair together.
Refuse mixed versions or a missing export.

Each explainer or review paper continues to version separately.
Its HTML, Markdown and PDF must agree on its edition.
A shared template change advances every affected paper whose public output changes,
rather than bumping unaffected papers.
Retain existing paper draft labels and publication/revision dates; do not borrow the
site’s edition or retrospectively renumber old papers.

Add optional `releases` to changelog entries, containing `{component, version}`. These
are references to editions in the corresponding retained history, not a second store of
current versions. Use cores such as `v0.5.1`, without data-hash suffixes or `Draft`
labels. This is illustrative syntax, not a version assigned to a historical PR:

```yaml
releases:
  - component: infographics
    version: v0.6.0
  - component: paper:n11-lower-bounds-explainer
    version: v0.4.6
```

Validate historical references against their matching history entries, not today’s
current constants. Do not fabricate version references during backfill when no edition
was actually cut. Keep entry merge dates distinct from `first_published` and paper
revision dates. A merged cut can be described as prepared; publication is confirmed by
the existing deployment audit.

The release preparation/closeout workflow must record an impact decision for each
externally changed component and require its patch or minor successor.
Cross-check the changelog references, authoritative histories, visible artifact stamps
and export receipts.
Validate component ownership and rendered changes; do not infer a bump from PR size,
every repository edit, or the presence of a new provenance digest alone.

### Backfill boundary and sources

Freeze the initial main-branch window at 36 merged PRs, from #479 on 2026-10-10 to #588
on 2026-10-13. Newest first:

```text
588, 509, 497, 581, 560, 579, 576, 507, 558, 556, 553, 555,
518, 551, 516, 547, 546, 531, 512, 519, 520, 513, 508, 502,
496, 499, 487, 462, 492, 477, 491, 474, 478, 482, 480, 479
```

Review the complete diff and merged state when a description is stale.
Use PR summaries and their linked records as a starting point, then fill gaps, combine
repeated prose and adapt the wording.
Keep a separate backfill review mapping every selected PR to an entry or a short
omission reason; do not put that audit table into About.
Changelog-only synchronization and purely administrative changes may have no independent
noteworthy entry, with the reason retained in that review.

The examples establish the intended level of detail:

- #588: a second reported n = 17 proof imported with retained sources and comparisons,
  at V0/C1; no claim of a local Lean rebuild.
- #497 and #509: regularization groundwork, with bullets for policy, comparison tooling
  and vendored provenance.
  They belong to formal stack 498, whose remaining layers are still open.
  #581 is a separate verification-gap review.
  Do not announce regularized bounds or admissions, and do not reuse open #549’s
  proposed T-154 identity: current T-154 belongs to #588.
- #553: admission and adoption of newly replayed upper-bound certificates, referencing
  T-151 and T-152. A later reply-bookkeeping PR does not re-admit those results.
- #462: the unified website overview, atlas and results navigation.
- #496: bounded publication audits and selective local push checks, without an
  unsupported general speedup claim.

### Ongoing authoring

Make changelog upkeep part of PR closeout.
A reusable first-party import/draft command reads merged PR metadata and current local
records, produces candidate YAML and a coverage audit, and leaves the wording for
editorial review. Require actual merge metadata and main-branch delivery for committed
public entries.
A subsequent changelog-update PR or documentation batch can publish those
entries; do not invent a merge date before the source PR merges or make the website
build depend on GitHub.
Changelog-only synchronization PRs receive an audit disposition rather than creating an
endless sequence of entries about changelog updates.

Document this closeout step beside the existing PR workflow.
Allow manual additions and corrections through the same schema and renderer; no
scheduled job or unreviewed prose publication is needed for the initial feature.

## Implementation Plan

One implementation phase, with four coordinated deliverables:

- [x] Settle the schema, validated loader, shared renderer, draft/import command and
  freshness check. Keep schema-bound validation in the ordinary fast surface.
- [x] Backfill and editorially review the 36-PR window, with explicit coverage and
  verified stack grouping.
  Reuse available work and retain merge-time claim limits.
- [x] Add component release-impact policy, shared infographic versioning and consistency
  checks, preserving independent paper histories.
- [x] Integrate GitHub and About views, reference rewriting, discovery, build inputs,
  publication scope and maintenance instructions.

The initial implementation includes 20 entries covering 23 PRs, 13 editorial omissions
and all 36 retained main-branch deliveries.
The subsequent main integration adds one grouped regularization delivery and one related
n17 report-and-policy launch, giving 22 entries, 47 retained PR deliveries and the same
13 editorial omissions.
The production record stores delivery, formal-stack and coverage metadata beside the
entries; the reader views omit that audit metadata.
The [backfill review](../../reviews/review-2026-10-13-site-changelog-backfill.md)
records every disposition and publication evidence.

The owner’s editorial refinement excludes routine internal documentation, planning and
bookkeeping from the public history.
Retain external-facing documentation, results, important tooling improvements and
substantive research or admission policy changes.
The coverage audit remains complete without forcing every audited PR into a public
entry.

The closed production contract is `packing/site-changelog.schema.yaml`.
`devtools.render_changelog --check --baseline-ref origin/main` checks generated Markdown
and independently freezes prior entries from the local main reference.
`devtools.import_changelog` acquires merged metadata during authoring and verifies local
main ancestry before writing candidates.
Neither normal rendering nor validation fetches GitHub.
The companion planning schema and examples remain the original design samples.

`devtools.check_release_impact` selects candidates from producer declarations and their
Python helper imports.
Each candidate needs its owning patch/minor successor or a fresh review naming the exact
changed paths, examined outputs and no-change reason.
The site cut prepares `v0.6.0`. After the regularization launch, the shared infographic
family prepares `v0.6.0`; only the n11 lower-bound explainer prepares `v0.4.6`, a patch
for its added n17 proof-report explanation.
The other three papers keep their editions.
These selected editions require their complete exports and deployment before being
announced as published; the launch entries cite the already verified main deployments.
Export-family staging and rollback make an interrupted infographic cut retryable without
selecting another version.

The additional legend-removal request is tracked as `think-8lsv`: remove the redundant
bottom S/V/C strip while retaining the Results page’s complete ladder documentation.

## Testing Strategy

Use a small set of meaningful behavioral and negative checks:

- Schema and semantics accept the examples and refuse missing prose, malformed dates,
  duplicate IDs, duplicate PR membership, unmerged layers and invalid stack grouping.
- One fixture covers a standalone admission, a multi-piece stack delivery and a later
  delivery from the same stack, with frozen old membership and dates.
- GitHub and About show the same entries, PR links and order.
  Structured repository references resolve correctly in each destination; raw HTML and
  unsafe schemes fail.
- Renderer `--check` detects an edited generated body.
  Markdown bullets and math survive both render paths and formatting.
- Launch tests distinguish merged/prepared work from verified publication, preserve
  unknown first-live dates, and check direct public artifact links.
- The changelog is the last About content section, has stable anchors and readable
  desktop/mobile layout, and remains discoverable from GitHub.
- Component tests cover patch and minor successors, both infographic versions advancing
  together, a missing/mixed export refusal, independent paper editions, and no invented
  backfill versions.
- A YAML-only edit triggers the overview publication path.
  Add declared inputs to `RENDER_INPUTS`, `pages_scope`, Pages push filters and their
  existing contract tests.
- Register the enforced production dataset with `validate_schemas` and its existing
  validator-equivalence coverage.
  Add a fast renderer freshness check.

Run the change-reachable push tier and hosted fast/browser checks, then obtain the full
checkpoint before merging the implementation.
Keep PR-level publication evidence separate from a mathematical proof replay.

## Rollout Plan

Review this plan and its copyable examples, then implement the single phase.
Validate backfill coverage and compare both generated reader views against the same
YAML. Publish through the existing About artifact and verify the deployed changelog with
the normal publication audit.
Begin routine updates with the documented closeout process.

## Open Questions

The proposed initial cutoff is 36 merged main-branch PRs.
Extend it if the owner wants more historical context; the schema and backfill command
must support that without changing the rendering design.
No unresolved question blocks the draft implementation plan.

## References

- [PR template](../../../../.github/PULL_REQUEST_TEMPLATE.md)
- [Website layout plan](plan-2026-10-08-site-layout-and-navigation.md)
- [Website development loop](plan-2026-10-10-website-development-loop.md)
- [Development and validation](../../../../development.md)
- [Regularization policy](../../policies/regularization-policy.md)
- [Result register](../../../../packing/frontier/results.yaml)
- [About manuscript](../../../../packing/devtools/templates/about-article.md)
- [Soft Schema](https://github.com/jlevy/softschema)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
