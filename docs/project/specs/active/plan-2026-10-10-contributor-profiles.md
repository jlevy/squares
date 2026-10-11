# Feature: Contributor Profiles and Linked Result Credits

**Date:** 2026-10-10

**Author:** Codex, for Joshua Levy

**Status:** Data-model spike complete; initial population and website implementation in
progress in [PR #490](https://github.com/jlevy/squares/pull/490).

**Workflow:** W7 pipeline improvement, entered through `tbd shortcut new-plan-spec`.

**Beads:** `think-39mp` (feature epic), `think-sxpm` (completed model spike),
`think-m7il` (population and full census), `think-9yli` (pages and name links).

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

## Attribution Policy and Follow-up

[Attribution Policy](../../../../attribution.md) is the single authority for preferred
person names, handle reconciliation, project/tool distinctions, lineage and PDF credits.
It records case-specific decisions and exceptions.
The shared design guide owns layout; this plan owns rollout and coverage.

The owner added four follow-ups: `think-t3a9` reconciles Ahmed/Queuingtheorydotcom and
supported handles, including Joshua Levy/jlevy/ojoshe; `think-vix3` audits personal Levy
credits against project branding, including PDFs; `think-8yk4` verifies the suggested
EvolvingPrograms/Lewis identity; and `think-xid4` establishes the canonical policy and
references. A handle match is not a global replacement rule, and archived source wording
remains unchanged. Complete the scoped identity update now; review historical credit
migrations by renderer and role under their own beads: `think-2v8h` for bound citations,
`think-zupq` for verifier author fields and `think-ir3i` for PDF profile links and
compact credit lines.
The Lewis audit establishes affiliation with the EvolvingPrograms organization, not a
personal alias; its person/infrastructure roles remain separate.

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

The initial implementation fixes an occurrence origin as repository-relative `path`,
stable `record_key` and `field`. Each reviewed span records the complete
`expected_text`, `start`, `end`, original `label`, `role`, `disposition`, optional
`contributor_id` and supporting evidence.
The validator reads the source field and rejects stale text, overlapping spans, labels
that differ from their spans, unknown profiles and unresolved evidence pointers.
Array items use individual field pointers.
Existing plain credit strings remain available for sorting, print and metadata.
When equal credit strings from different sources have conflicting reviewed identities,
the composed credit remains unlinked rather than selecting one source arbitrarily.

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

A shared article loader owns same-site fetches, inert parsing, relative URL rebasing,
prepared assets and a pristine cached article; each consumer receives a clone.
Controllers own request generation and visibility, invalidate pending requests when
closed or replaced, and scope injected IDs and their fragment/ARIA references.
Contributor links inside an active overlay are handled before its ordinary anchor-close
handler and preserve the original visible page opener for focus restoration.
Static case, result and profile pages include the same enhancement scripts as the
overview.

## Implementation Plan

### Phase 0: Review and Data-Model Spike

- [x] Review record families, identity evidence and the relevant website code path.
- [x] Write the phased plan and record limits of the source census.
- [x] Add schema, loader and semantic checks to the existing schema gate.
- [x] Seed Walter Stromquist, Evan Daniel and Mira: historical byline, named contributor
  with publication site, and handle-only identity without an invented biography.
- [x] Exercise invalid metadata, provenance, IDs, unsafe links and body shapes;
  independently validate using softschema.
- [x] Complete independent model review and required PR validation; record the outcomes.

This phase proves the record contract against examples.
Publishing routes and converting names belong to Phase 2. The model spike alone
introduces no dead profile links.

### Phase 1: Select Contributors and Build Profile Records

Owner: `think-m7il`; first reviewed batch and reusable tooling: `think-0dqj`.

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

Owner: `think-9yli`; page generation: `think-s3wj`; browser behavior: `think-0d3g`.
Implementation proceeds beside the initial population batch, with publication acceptance
depending on its reviewed mappings.

Implement standalone pages/index and shared popovers, then the full name-link surface
matrix. Once the occurrence and renderer APIs are fixed, delegate page/overlay work,
mechanical credit conversion and content review to disjoint lanes.
One integrator owns shared generators, route registration, build declarations and output
regeneration.

Report which occurrences became links and why any remain text.
Historical population may continue in reviewed batches, but publication never uses
guessed identities or missing destinations.
Add profile/occurrence maintenance to ordinary result intake.

### Phase 3: Reviewable Basic Website

Acceptance owner: `think-vqio`. This PR includes the model spike, the initial reviewed
population and a working website.
The first acceptance scope is the contributor directory, sourced profile pages,
popovers, and reviewed name links in main result tables, result histories, frontier
credits and case panels, figures and result lists.
Unknown identities remain visible as ordinary credit text.

| Sub-bead | Deliverable | Requested agent | Status |
| --- | --- | --- | --- |
| `think-0dqj` | Initial profiles, census tool, reviewed occurrence contract and credit links | Sol, `xhigh` | Complete |
| `think-s3wj` | Directory, standalone profiles, safe biography rendering and publication integration | Sol, `xhigh` | Complete |
| `think-0d3g` | Shared article loading, accessible contributor popovers and browser checks | Sol, `xhigh` | Complete |
| `think-vqio` | Independent technical review, integrated preview and validation receipts | Astra, `xhigh`, with coordinator integration | Review complete; publication checks on PR #490 |

The first independent implementation review requested three fixes: initialize overlays
before their controllers run on standalone pages (`think-0cxt`), preserve distinct
publication backlinks and accept every valid provenance pointer (`think-4f3u`). The
integrated build also identified two pages over their existing byte budgets
(`think-c5gl`) and missing executable-script classifications.
These are acceptance work for this PR, with regression tests, rather than deferred
archive work.

The coordinator owns plan updates, beads, commits and final validation.
Implementation agents own disjoint file sets, with one owner for generated routes and
shared page shells. The Astra review fixes the source-aware credit and overlay contracts
before edits, then reviews the frozen implementation after integration.

`think-erx9` adds the requested design-system audit to this acceptance phase.
The canonical specification is
[`paper-design.md`](../../../../packing/devtools/templates/paper-design.md), not a
second profile-specific design system.
Review case, result, contributor and legacy card popovers together: token and typography
ownership, dimensions and scrolling, close actions, keyboard/focus behavior, native
links, canonical-page content, responsive themes, prepared math and script loading.
Reconcile stale descriptions in that specification and link this plan to the shared
contract; track any implementation discrepancy as an acceptance fix.
`think-jm0i` owns typography and close-button clearance corrections; `think-iu56` owns
publication-input and required-browser coverage gaps identified by the audit.
`think-iabo` owns the duplicate result headline found in the same review; a fetched
article retains its title on the standalone page and shows one visible title in its
result popover.

- [x] Render the same biography, identity fields and public links in a standalone page
  and its popover.
- [x] Preserve credit wording and role while converting reviewed names to links.
- [x] Verify keyboard focus, Escape, modified clicks, fetch failure, request races and
  transitions from case/result popovers.
- [x] Verify routes, sitemap, build selection, stale output removal and source drift
  detection.
- [x] Open a working preview and inspect desktop/mobile and light/dark presentations.
- [x] Resolve independent review findings and update PR #490 with executed validation,
  preview instructions and remaining census coverage.

### Phase 4: Complete the Archive and Remaining Surfaces

`think-m7il` remains open until every inventoried source has an inspection receipt and
every credit occurrence has a disposition.
Batch work continues across PDF bylines, acknowledgments, referenced authors, historical
construction catalogues and contributed reports.
`think-bw3z` owns historical PDF inspection and profile batches; `think-nlob` owns web,
construction and contributed-report reconciliation.
The census distinguishes inspected, pending, unresolved and non-person records.
Profile and occurrence counts are reported separately from the count of inspected PDFs.

`think-jn87`, under `think-9yli`, tracks remaining paper, project-card, footer,
authored-prose, atlas and first-party print conversions after the basic website passes
review. Create disjoint authoring and renderer sub-beads for each batch, preserving the
same identity review and validation requirements.
The initial release does not establish complete archive coverage.

### Intake and Progress Checks

From `packing/`, with the task environment configured, run
`uv run --frozen --all-extras --group dev python -m devtools.contributor_census` for
profile counts, structured credit dispositions and PDF inspection coverage.
Add `--json` for pending source addresses and candidate profile IDs.
Candidate IDs are review suggestions only.

The first implementation batch contains 20 profiles.
Its structured census covers 974 occurrences: 738 resolved to profiles, 230 unresolved
and six non-person credits.
The manifest also reviews the generator-owned project-author credit separately, for 975
retained occurrences and 739 resolved joins in total.
All 144 tracked PDFs still require the complete credit census; a byline-only inspection
does not count as reading a paper’s acknowledgments and references.
These counts describe the initial batch and are regenerated by the census command.

For each intake batch, inspect the cited source, reserve person IDs, author sourced
profiles and review the exact source spans before adding resolved mappings.
Run the schema/semantic checks, render the affected pages and verify the new name links
before closing the batch bead.
If a source field changes, review the changed attribution before updating its expected
text; do not silence source drift by copying the new text without checking identity and
role.

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
hosted PR checks. Record executed evidence against the relevant phase; unexecuted
acceptance criteria remain unchecked.

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

### Basic Website Verification

The records tier passed all 49 selected steps in 57.50 seconds after publication
integration. Softschema repair checks accepted all 20 profiles and the occurrence
manifest without repairs or warnings.
Independent Astra checks passed 85 contributor/occurrence tests, then six targeted
review regressions covering distinct bibliography works, valid provenance pointers,
generated-page popovers and script inventory.
The source-aware census reports the initial coverage above; it does not mark the
remaining PDFs inspected.

The local preview serves the complete site at `http://127.0.0.1:8790/`, with the
directory at `/contributors/index.html` and progress at `http://127.0.0.1:7790/` while
those local servers run.
Rebuild with `python -m devtools.preview_site --output PATH --serve` from `packing/` in
the project environment; use external scratch for the output.
Manual inspection confirmed directory-to-popover navigation, the standalone profile,
Escape/focus restoration and mobile dark-mode layout.
The generated-page browser selection passed six checks with Chromium required and no
skips. It covers directory, profile, case and result entry points, native navigation
without scripts and fetch-failure fallback.
The budget and content-preservation selection passed 12 tests: T-124 is 299,837 bytes
against 300,000, and the results table is 791,833 against 800,000. All 178 cases, 67
history steps and source links remain present; browser DOM and XML math equivalence
checks passed. The design audit reconciled the canonical guide, component ownership,
standalone and overlay contracts, and the development guide.
Profile metadata and headings now use shared typography roles; close-button clearance
applies to the opening breadcrumb rather than narrowing the whole article.
Eight computed-style browser combinations cover desktop/mobile, light/dark and
standalone/popover layouts, including long source identifiers and URLs.
Publication filters include the contributor stylesheet and cited license; browser
coverage includes its sans roles and the case-table DOM preservation check.
The result popover shows one visible title after fetching, while standalone pages and
cached articles retain theirs.
Three generated-page browser checks and 28 Node checks cover that correction.
Independent Astra review accepted the reconciled design guide and final implementation
with no remaining functional or design blockers.
The complete contributor browser suite passed 26 tests; a separate eight-case run
explicitly checked the resolved theme.
Hosted integration also exercised existing page contracts: `think-u5c8` reconciles
footer navigation, script ordering, contributor output/freshness and real sparse
evidence restoration; `think-wrpf` preserves relative profile links, full credit text
and semantic MathML in the existing rendering checks.
The complete affected modules passed 357 overview/workflow tests and 138
case/result-column tests, with no skips.
Astra accepted the final integration fixes and independently passed the pruning and
sparse-restoration checks.

The local edit floor passed.
Its broad behavioral run encountered a changing file inventory during formatting; a
retry was interrupted before the README integration fix, so neither run is a passing
broad behavioral receipt.
The README check passed after adding this policy to its layout and authority map.
Final hosted receipts and publication status are recorded on
[PR #490](https://github.com/jlevy/squares/pull/490), with the tested head and base,
rather than copied into this plan as moving CI status.

The upstream layout integration (`think-ztic`) adopts Atlas as the case directory and
`results.html` as the Results index while retaining complete contributor, case and
result pages, reviewed credit links and the shared article loader.
A fetched result uses its canonical H1 as the sole visible headline and accessible
dialog name.
The page-heading follow-up (`think-4w5c`) requires contributor directory and
profile H1s to inherit the same sans-serif, all-caps title rule as other site pages;
popovers retain the shared compact heading hierarchy.
Generated computed-style checks compare the contributor pages with the standard page
role at desktop/mobile widths in both themes.

## WIP Handoff: 2026-10-10

The owner requested a work-in-progress PR and handoff before further implementation.
Continue on `codex/contributor-profiles-plan-spike` in
[PR #490](https://github.com/jlevy/squares/pull/490). Implementation commit `85e0ac66f`
merges upstream `6038af33c`; the handoff commit adds documentation only.
Do not treat the earlier green CI on `ed89bfdda` as validation of this merge.
The PR is being retained as draft, with integration acceptance open.

### Selected Next Slice: Generic Profile URLs

`think-0v2c` is open and unstarted: make `/profiles/index.html` and `/profiles/ID.html`
the canonical directory and person-page URLs.
Use “Profiles” wording so cited paper authors are included without implying that every
person directly contributed to the project.
All 20 current records already have navigable pages under `/contributors/`; the
requested URL migration has **not** been implemented.
Update generated links, route registration, sitemap, publication inventory, popover
loading, tests and design documentation together.
Keep registered forwarders for existing `/contributors/` links.
Preserve reviewed identity joins, displayed credit wording, source roles and shared
article-loader accessibility and fallback behavior.

### Acceptance and Remaining Work

- `think-4w5c` is complete: standalone headings inherit the shared sans-serif, uppercase
  H1 style; popovers use the shared compact hierarchy.
- `think-ztic` remains in progress for merged-site acceptance.
  On `85e0ac66f`, 446 renderer tests, 61 browser integration tests, 16 heading/design
  checks, 29 Node tests, 106 published-site tests and 263 validation/URL tests passed in
  their respective selections.
  The rebuilt full preview and publication checks passed; the route registry reports 946
  rows and no failures.
  Astra accepted the implementation and final publication-checker changes.
- The local `packing-validate --push --inner-jobs 4` gate **failed**: reachable
  behavioral tests exceeded their 900-second ceiling, after partial pytest output had
  already shown an `F` without a final failure traceback.
  Total gate wall was 1018.93 seconds, with 65 of 66 steps completed.
  Diagnose the failing selection and rerun; this is not established as a timing-only
  failure. Do not raise the ceiling to hide it.
- Earlier required Packing, Pages and deferred CI passed on `ed89bfdda` only.
  Inspect the PR checks for the pushed handoff head before claiming acceptance.
- `think-39mp` remains the epic; `think-m7il` owns population and census, `think-9yli`
  publication. The census still has 230 unresolved occurrences and 144 PDFs awaiting
  complete credit inspection.
  Continue PDF and web batches through `think-bw3z` and `think-nlob` after the selected
  URL/acceptance slice; remaining renderers are `think-jn87`.
- Attribution policy is [attribution.md](../../../../attribution.md).
  Ahmed and Levy aliases are sourced.
  Lewis is affiliated with EvolvingPrograms; do not infer that the organization is a
  proven personal alias.
  Bound citations, verifier credits and compact PDF links remain tracked by
  `think-2v8h`, `think-zupq` and `think-ir3i`.

### Resume Setup

Run `tbd prime` and `tbd sync`, reread the selected beads, then claim the next slice
before editing.
Bead state lives on `tbd-sync`; this plan records its handoff snapshot in
the PR itself. Use Sol agents for mechanical implementation and Astra for technical
review, with separate file ownership.

On this Mac, source
`/Volumes/spud-ext1/agent-scratch/contributor-profiles-01a126ff/env.sh` before
build/test commands.
It sets the external scratch directories, pinned environment and browser location.
Verify the volume is mounted and writable; do not fall back to internal disk for bulk
output. Run Python through `uv run --frozen --all-extras --group dev` from `packing/`
with Python 3.14.7, never the system interpreter.
The failed gate log is in that scratch directory at `tmp/upstream-push-gate.log`;
scratch logs are local diagnostic aids, not portable PR evidence.
The outcome above is the durable receipt.
Do not format or mutate the tree while broad pytest collection runs.

The existing local preview at `http://127.0.0.1:8790/` serves the merged site, including
`/contributors/index.html`; the bead board is at `http://127.0.0.1:7790/` while its
server runs. Neither local server is a production deployment.

## Open Decisions and Limits

- Additional organization-wide code review requires named repositories beyond this
  checkout and its declared dependency.
- Keep occurrence-manifest fields and source accessors consistent with census output.
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
