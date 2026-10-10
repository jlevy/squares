# Feature: Contributor Profiles and Linked Result Credits

**Date:** 2026-10-10

**Author:** Codex, for Joshua Levy

**Status:** Draft design with a bounded data-model spike; population and publication
remain implementation work.

**Workflow:** W7 pipeline improvement, entered through `tbd shortcut new-plan-spec`.

**Beads:** `think-sxpm` (this plan and spike), `think-m7il` (profile population),
`think-9yli` (pages and name links).

## Overview

Give every person cited or credited in the square-packing result archive a stable
contributor record and a linkable profile.
Include historical contributors, current contributors, paper authors, and people
acknowledged for methods or prior work.
Each record has structured identity and public links in softschema YAML frontmatter.
Its optional Markdown body is one biographical paragraph of at most five sentences.
The website presents the same content as a popover and a complete standalone page.

Convert credited names into profile links wherever the website presents them, including
main results tables, result histories, case pages, paper credits and project cards.
Preserve the printed name, credit order, role and source relationship.
Linking a person must not turn an acknowledgment into authorship.

## Goals and Scope

- One record per evidenced person, with optional real name, aliases, Twitter/X, GitHub,
  Substack, personal website and publication website.
- Include historical and current credit occurrences, starting with key contributors
  visible on the site and credited on retained PDFs, then reconcile the full archive.
- Source identity matches, biography facts and account ownership; omit unknown values.
- Make ordinary links work without JavaScript and enhance them with accessible popovers.
- Use sub-agents for extraction, profile authoring and mechanical updates, with disjoint
  assignments and independent identity review.

The owner expects a few hundred profiles.
This is a planning estimate, not a measured person count.
Private contact information, inferred identities, portraits, social feeds and
contributor rankings are outside this feature.
Scientific claims and archived source bytes retain their existing authority.

## Review Before Implementation

The review covers this repository’s record organization, credit producers, schema
consumers, site generators, routes, overlays and validation.
The declared external code dependency is `vendor/kpress`; the local workspace includes
`packages/workbench`. This is not an audit of every algorithm or every repository owned
by the GitHub account.
Additional organization/repository scope needs named repositories.

Three review lanes examined archive credits, site integration and schema design.
The first two requested GPT-6.1 Sol at `xhigh`; the schema review requested GPT-6 Astra
at `xhigh`.

### Archive coverage

Inventory from the checkout based on `af17208c0`; rows and files overlap and must not be
summed into a person count.

| Source family | Inventory | Credit information |
| --- | ---: | --- |
| `packing/frontier/results.yaml` | 131 result rows | Attribution source keys, `builds_on.credit`, corrections and history |
| `packing/frontier/evidence.yaml` | 471 evidence rows | Source identities, performers, provenance and acknowledgments |
| `packing/frontier/n-*.md` | 324 case records | `found_by`, `improved_by`, `proved_by`, priority claims and resources |
| `packing/resources/bibliography.yaml` | 94 source rows; 32 name mappings | Authors, credit strings and lineage; surnames are presentation labels |
| `packing/atlas/known-best/credit-attributions.json` | 96 aliases; 20 lower-bound contributor rows; 18 optimality contributor rows; 30 optimality people entries | Curated identity, role, date and source evidence; entries overlap and include organizations |
| Tracked `packing/resources/` files | 144 PDFs; 131 raw Markdown extractions | Bylines, acknowledgments, references, figure and construction credits |
| Web archive packets | 100 immediate packet README files | Licenses, citation metadata, attribution notices and upstream accounts |
| Witness records | 423 YAML leaves, excluding schemas | Discoverer and construction provenance |
| `packing/resources/web/known-best-packings/sources.json` | 148 source rows | Construction credit and source lineage beyond headline results |

Other required census inputs are the asymptotic and strategy catalogues, unavailable
source records, rigidity/methods/simulation literature tables, and the four `PAPERS`
renderers’ author and oversight configuration.
Include `packing/resources/private-correspondence/`, contributed reports under
`packing/resources/papers/n11-complete-research-bundle-2026-09-07/`, and flat web
catalogues such as `kingbird-squares-in-squares-compared*.md`, dated captures and
alternative-packing pages.
Correspondence can identify an attribution to investigate; published identity and
biography claims still require public evidence, without publishing private contact
details. Generated copies are reconciled with sources, not counted as new people.

Counts came from Git-tracked file enumeration, JSON parsing and top-level YAML row
patterns. This is a coverage inventory, not a completed reading of every PDF page.
Phase 1 must inspect PDF bylines, acknowledgments and referenced authors, using original
pages where extraction is absent or ambiguous.
Unread material retains a pending status; absent extracted text does not establish
absent credit.

Existing aliases require identity review.
The audit preserves uncertain E./G. Bajmóczy initials and distinguishes `ctjlewis` from
the EvolvingPrograms organization.
Mira, Kleddamag, Guzhou0806 and Julian-JJ may remain handle-only profiles.
Project, organization and AI-system credits stay explicit non-person occurrences.
Do not turn a project label into a human without evidence.

### Code and consumer map

| Boundary | Existing implementation | Required integration |
| --- | --- | --- |
| Owned records | `sqpack.yamlio`; `devtools.validate_schemas` | Duplicate-key-refusing loader, corpus discovery, semantic checks |
| Credit composition | `devtools.result_credit`; `overview_data` | Preserve plain strings for sorting/print; add structured occurrence IDs |
| Identity evidence | `atlas_credit_attributions`; bibliography and credit audit | Reuse reviewed evidence, replace text joins with explicit person IDs |
| Standalone content | `render_overview.static_content_page`, `kpress_page`; `render_case_pages` | Prepared contributor article inside the existing page shell |
| Overlays | `overview/case-popover.js`; `row-popover.js` | Shared fetch/parse/rebase/assets boundary; case navigation stays separate |
| URLs and discovery | `site_urls`; `site_documents`; `result_overview.check_links` | Canonical URLs, document aliases, served paths and sitemap |
| Builds and removal | `render_overview.inputs`, `render_site`, `write_site`; `preview_site`; `pages_scope`; Pages workflow | All producers, check mode, stale-file pruning and path selection |
| Print and atlas surfaces | `build_bound_citations`; atlas/workbench/video/PDF producers | Retain text/width contracts, link through the relevant renderer |

The site overlays use checked JavaScript under `tsconfig.overview.json`, not workbench
TypeScript. Workbench navigation concerns packing/animation.
No full-text website search index was found; a searchable directory is separate from the
required profile index and sitemap.

## Design

### Records and provenance

Store `packing/contributors/<id>.md` with `contributor.schema.yaml`, contract
`packing.squares:Contributor/v1`, envelope `contributor`, status `enforced`. Use the
existing hermetic JSON Schema validator; the installed softschema CLI provides an
independent compatibility and repair check.
New consumer fields require reviewed contract changes rather than an unvalidated
extension hidden from CI.

| Field | Meaning |
| --- | --- |
| `id` | Immutable lowercase slug matching the filename |
| `display_name` | Preferred public name or handle |
| `real_name` | Optional publicly evidenced name |
| `aliases` | Evidenced spellings, initials and handles; not globally unique IDs |
| `links` | Typed public URLs and optional handles; publication/personal sites are distinct |
| `sources` | Local IDs, repository-relative archive paths and/or primary URLs, with locators |
| `provenance` | Payload field pointers and supporting source IDs |
| `bio_sources` | Source IDs supporting the optional body paragraph |

Keep biography only in the Markdown body, followed by the required documentation footer,
without a heading or duplicate YAML biography field.
Consumers render it as content and never extract structured facts from it.
Phase 2 renders only inline Markdown within that paragraph, disables or escapes raw
HTML, and applies the same HTTP(S)-only URL policy to biography links as to structured
links. Test that policy in both standalone pages and injected popovers.
The loader exposes it separately and strips only the exact footer.
Validate the single-paragraph shape; review the five-sentence maximum editorially
because initials and abbreviations defeat naive punctuation counting.

Sources and field pointers must resolve.
Claimed names, aliases and links need evidence; archive paths stay within the
repository. Links accept HTTP(S), with platform/handle consistency checked where
applicable. Omit unknown information.
A historical paper’s institutional byline does not support a claim about current
employment.

### Identity and credit occurrence joins

Profiles answer who a person is; source/result records answer what they contributed.
Do not duplicate the result ledger in profiles.

Phase 1 builds a reusable census tool and retained occurrence manifest.
Each occurrence names its repository path, source/record key, field or PDF page/section,
original label, role and disposition: resolved profile ID, unresolved identity or
non-person credit. Split grouped authors into individual people while preserving
punctuation/order. Inspect abbreviated `et al.` lists; that text is not a person.

Aliases propose matches; reviewed occurrence-to-ID assignments authorize links.
A surname unique in three seed records is not globally unique.
Never select the first alias match, merge similar cross-platform handles automatically
or infer a real name.
Unresolved occurrences retain plain text and an actionable disposition.
When profiles merge, preserve retired URLs through the existing URL-history mechanism
and migrate occurrence IDs together.

### Convert names to links

Render each resolved occurrence’s original label as an anchor to
`contributors/<id>.html`, rebased to the containing page and marked for popover
enhancement. Profile pages link back to credited results and papers through the reviewed
manifest, preserving roles.

| Name-bearing surface | Conversion point |
| --- | --- |
| Recent/all-results tables, including `after …` | `overview_sections.credit_cell`; retain plain sorting values |
| Result page/popover header and history chain | `result_overview.head`, `step` |
| Frontier upper/lower credit lines | `render_frontier_page.credit` |
| Case Found/Improved/Proved by, figures and result lists | `render_case_pages`, `visual_summary`, `results_block` |
| Paper source/author and human-oversight credits | `paper_front._credit_lines`, HTML and Markdown editions |
| Project-card authors and global footer | `overview_sections.other_project_cards`; `render_overview` footer |
| Authored prose, figures, atlas/workbench and PDFs | Deliberate source/generator pass with surface-specific links |

Correction credits sometimes sit inside result anchors, and project cards are anchors or
buttons. Use sibling person links or the existing footed-card pattern; never nest
interactive elements.
Do not replace names globally in HTML. Third-party PDFs retain their bytes; link their
authors through archive metadata and HTML. Regenerated first-party PDFs can use profile
hyperlinks while preserving credit text and layout.

### One page, two ways to read it

Publish a complete static page at `contributors/<id>.html`, with canonical metadata,
breadcrumb, sitemap entry and an index linking every published profile.
Popovers fetch that same page and extract `article.site-contributor`; no second
biography renderer.
Reuse request caching, stale-request guards, rebasing, asset loading,
failure fallback and focus restoration from case/result overlays.

Preserve modified clicks, keyboard access and no-JavaScript navigation.
A person link inside a case/result overlay replaces the active overlay while retaining a
valid return-focus target.
Escape closes the active overlay; failed fetches navigate normally.
Avoid host-ID collisions from injected headings/fragments.
Existing prepared-math asset paths assume one directory below the site root, which the
proposed route satisfies.

## Implementation Plan

### Phase 0: Review and Data-Model Spike — This PR

- [x] Review record families, identity evidence and the relevant website code path.
- [x] Write the phased plan and record limits of the source census.
- [x] Add schema, loader and semantic checks to the existing schema gate.
- [x] Seed Walter Stromquist, Evan Daniel and Mira: historical byline, named contributor
  with publication site, and handle-only identity without an invented biography.
- [x] Exercise invalid metadata, provenance, IDs, unsafe links and body shapes;
  independently validate using softschema.
- [ ] Complete independent review and PR validation; record the outcomes.

This phase proves the record contract against examples.
Publishing routes and converting names belong to Phase 2, so the spike introduces no
dead profile links.

### Phase 1: Select Contributors and Build Profile Records

Owner: `think-m7il`.

Build the reusable census tool before bulk authoring.
Begin with main-site credits, case contributors and PDF bylines; include acknowledgment
and reference authors from all inventoried families.
Key contributors are the first batch, not a filter excluding historical or less
prominent contributors.

The coordinator freezes the source inventory, reserves IDs and assigns disjoint batches.
Run authoring lanes for historical papers/PDFs, modern result repositories/handles and
construction/catalogue history.
Each owns only assigned profiles and proposed occurrence mappings.
An independent pass checks identities, public accounts and biography claims before the
coordinator integrates mappings.
Collision decisions stay with the coordinator.

Every batch reports sources inspected, resolved/unresolved/non-person occurrences and
new profiles. Completion requires a disposition for every occurrence and an inspection
receipt for every PDF, not a guessed count.
Validate profiles through softschema repair and the project checker before acceptance.

### Phase 2: Publish Pages and Link Every Resolved Name

Owner: `think-9yli`; starts after the first reviewed population batch.

Implement standalone pages/index and shared popovers, then the full name-link surface
matrix. Once the occurrence and renderer APIs are fixed, delegate page/overlay work,
mechanical credit conversion and content review to disjoint lanes.
One integrator owns shared generators, route registration, build declarations and output
regeneration.

Report which occurrences became links and why any remain text.
Historical population may continue in reviewed batches, but publication never uses
guessed identities or missing destinations.
Add profile/occurrence maintenance to ordinary result intake.

## Testing and Rollout

Add profiles to `validate_schemas.corpus_paths`, extending both the existing schema gate
and validator-equivalence coverage.
Test filename/ID mismatch, duplicate IDs, missing sources, dangling pointers, path
traversal, unsafe links, optional names/bios, body/footer handling and refusal to choose
among ambiguous labels.
Existing credit output must remain unchanged in the spike.

Publication tests cover initial static HTML, page/popover parity, canonical URLs,
sitemap, rebased links, stale-page removal, build selection and nested elements.
Browser checks cover each name-link surface, Escape/focus, modified click, fetch
failure, stale responses and overlay transitions on mobile/desktop and light/dark
themes. Use existing page budgets and the case/result/URL test patterns.

Run records/edit and change-reachable push checks, then the required checkpoint and
hosted PR checks.
Distinguish executed spike evidence from future UI acceptance criteria;
this PR does not establish browser behavior that Phase 2 has not implemented.

### Spike verification

The focused contributor, snapshot-copy and contributor-schema equivalence checks passed
92 tests, with 1,194 unrelated cases deselected.
Ruff and targeted BasedPyright reported no findings.
The installed softschema 0.8.0 repair check accepted all three seeds without repairs or
warnings.

Independent review found two issues, both corrected before publication: name lookup now
returns candidate tuples instead of resolving an identity, and negative-control
snapshots rescue the exact archive files declared by contributor sources.
A miniature worker-copy test verifies that cited evidence survives, unrelated archive
bytes stay excluded, and Git-tree inventory agrees with the live copy policy.

The initial records gate passed 48 of 49 checks; its missing document-map entry was
corrected, and the documentation check then passed for 1,994 durable documents.
The unchanged full schema-mutation test selection was interrupted after ten minutes
without observed failures; it is not counted as a passing run.
Final PR and checkpoint results are recorded on the pull request.

## Open Decisions and Limits

- Additional organization-wide code review requires named repositories beyond this
  checkout and its declared dependency.
- Fix occurrence-manifest fields against the census tool’s output before parallel edits.
- The distinct-person count and unresolved PDF identities are Phase 1 outputs.
- Preserve Unicode public spellings and original credit labels even when profile display
  names differ; the complete bibliography of each retained paper is included in the
  inventory, with explicit non-person and unresolved dispositions.

## References

- [Validation loops](../../../../development.md#validation-loops)
- [Site URL design](plan-2026-10-06-site-urls-seo-performance.md)
- [Result-kind model](plan-2026-10-01-result-kinds.md)
- [Resource archive](../../../../packing/resources/README.md)
- [Bibliography](../../../../packing/resources/bibliography.yaml)
- [Existing credit audit](../../../../packing/atlas/known-best/credit-attributions.json)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
