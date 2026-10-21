# Feature: Contributor Profiles and Linked Result Credits

**Date:** 2026-10-10

**Author:** Codex, for Joshua Levy

**Status:** Data-model spike, initial population, website and `/profiles/` URLs
implemented; continued from [PR #490](https://github.com/jlevy/squares/pull/490) in
[PR #578](https://github.com/jlevy/squares/pull/578), under final integration and review
on 2026-10-21. The current integration bead is `think-zpfo`; coverage expansion and
final validation are still in progress.
Dated validation receipts below apply only to the revisions they name.

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
The website publishes complete standalone profiles at `/profiles/<id>.html`. Directory
rows, project bylines and narrative links navigate directly; designated case/result
credit links may retain the existing contextual overlay enhancement.

Convert credited names into profile links wherever the website presents them, including
main results tables, result histories, case pages, paper credits and project cards.
Preserve the printed name in the evidence record, with its credit order, role and source
relationship; visible linked labels follow the attribution policy.
Linking a person must not turn an acknowledgment into authorship.

## Current Integration: 2026-10-21

Continue through `think-zpfo` and [PR #578](https://github.com/jlevy/squares/pull/578).
The active checkout is `/Volumes/spud-ext2/worktrees/squares-profiles-final-20261021`;
source `/Volumes/spud-ext2/agent-scratch/about-profiles-20261020/integration-env.sh`
before build or test commands.
Latest upstream integration includes origin/main `970e89de8` and its T-196 adoption at
227 and 260. Merge `e9149e2a2` preserves release `v0.8.15` beneath the proposed profile
release `v0.9.0`; `3ae236a16` pins that data revision.
The two changed finder occurrences now reference Joost de Winter.
Canonical result and source-coverage views reconcile, with no stale attribution spans.
Earlier dated receipts below are historical, including their counts, environments and
preview ports.

The frozen identity batch contains 75 profiles.
The structured census reports 1,435 resolved spans, 78 non-person spans and seven
unresolved spans; ten manual origins are reported separately.
The primary-authorship model yields 213 distinct registered results and 701 non-primary
person/result credits.
Results retain all authored registered results.
The requested Records subset (`think-lekx`) covers current contributions across every
result kind, including optimality proofs and formalizations.
Bound records require strict improvements; matching an existing bound alone does not
qualify. Family-specific currentness is implemented in `profile_records.py` and must not
be inferred from bound standing for non-bound results.
The classifier passed ten focused tests.
The directory and profile renderers show 114 current authored Records, with unresolved
priority or scope identified separately.
Astra reviewed the model and renderer boundaries without a blocker.
Formalization uses the existing result kind in the ontology, schema and filters;
`proves_kind` preserves the distinction from the original result.
Family-currentness work remains under `think-e953` and `think-kqi1`. The seven remaining
spans have explicit identity or collective-credit exceptions under `think-0v9j`; no new
mathematical result is registered in this PR. All 146 inventoried PDFs still await
complete credit inspection; this presentation slice does not close `think-m7il`.

Home and About lead to the directory, which shows full names, distinct results by
significance, separate credits, resources and public accounts.
Additional handles stay on individual profiles, keeping directory names compact.
Profile resources share homepage cards, with the source address directly beneath the
author byline. Recorded GitHub issue and pull-request references retain their source or
registration role. The
[presentation contract](../../../../packing/devtools/templates/paper-design.md#person-profiles)
and [attribution policy](../../../../attribution.md) own these rules.

| Bead | Acceptance scope |
| --- | --- |
| `think-xwad` | Shared distinct-result/significance and credit tally |
| `think-7oq3` | Visible account usernames and filtered additional handles |
| `think-r9xr` | Shared profile/homepage resource cards and source-link order |
| `think-wa1u` | Recorded GitHub issue and PR references with typed icons |
| `think-rvi5` | Shared account glyphs |
| `think-qks9` | Primary content uses normal foreground |
| `think-ml63` | Full names in About narrative |
| `think-sj8n` | Derived Years active in directory and profiles |
| `think-1ofm` | Directory people, distinct results, credits and unique resource totals |
| `think-uyag` | Evidenced years and source links in existing biographies |
| `think-vdsd` | Lower-level-only breadcrumbs, nearer navigation and clear of titles |
| `think-f3cl` | Paper release decisions for visible profile-credit changes |
| `think-d0zr` | Wide table, separate Results/Credits, blank zero cells, first-line icons |
| `think-etb6` | Shared nav GitHub mark and harmonious icon sizing |
| `think-gjxb` | Original-work activity years, excluding later citations |
| `think-94ky` | Primary results versus per-result credits, both by significance |
| `think-sb9n` | Evidenced author joins and historical authored sources |
| `think-uwd6` | Bidirectional profile coverage, significant results and PDF credits |
| `think-8wj0` | Generated PDF proof/formalization figure credits and person profiles |
| `think-2ccx` | Nine construction-finder profiles printed in PDF figure credits |
| `think-nd1y` | Significant-result identities and missing-authored-work review |
| `think-eigy` | Remaining clear person labels across all significance levels |
| `think-0ltn` | Dated historical contribution evidence not represented by existing records |
| `think-noql` | SoftSchema references, derived-data rules and agent maintenance guide |
| `think-cq58` | Reconcile this plan, phases, acceptance and current receipts |
| `think-mthi` | Accounts-only column and visible website/repository Resources |
| `think-njfb` | Parenthesized single-level tallies and muted significance detail |
| `think-lekx` | All authored Results and current Records across every result kind |
| `think-x43w` | Frits Göbel display name and Lewis account evidence |
| `think-q4t4` | Formalization contributor roles, resource membership and own-support years |
| `think-65yl` | Seven reviewed credit joins for the upstream Daniel n343 source |
| `think-4m6m` | Bounded worker evidence, measured test costs and integrated validation fixes |
| `think-98c5` | Linked-name result assertions and exact terminology anchors |
| `think-5q5y` | Canonical names and SVG navigation geometry regressions |

The reviewed preview is <http://127.0.0.1:8790/profiles/index.html>, served from
`/Volumes/spud-ext2/agent-scratch/about-profiles-20261020/site-merged-3ae236a16`. It
includes all 75 profiles, separate Results, Records and Credits, credit significance
breakdowns, Accounts and Resources columns, and muted parenthetical tallies.
The complete merged build includes all four PDFs.
All 7,298 publication checks pass; the PDFs contain 7, 8, 8 and 25 valid profile
annotations. The profile audit covers 692 pages with zero label mismatches or broken
profile destinations.
The directory reserves 16rem for full names and lets resource addresses wrap at normal
boundaries, with a fallback for long segments.
The URL registry has 1,144 rows with zero failures.
The latest merge passes all 52 record-validation and 68 edit checks, plus 54
identity/tally/coverage and 20 classifier/T-196 tests.
All 69 selected post-merge push-gate steps pass in 952.59 seconds; hosted acceptance
remains pending.
The sourced integration environment includes the project interpreter and
tools on PATH.

Local focused checks passed: 88 profile, naming, resource, tally and GitHub-reference
tests in 91.16 seconds; 62 release/component/impact tests in 17.93 seconds; and 19
result-rollup tests in 10.35 seconds.
Those checks predate the activity-year and primary-authorship corrections; the revised
models passed 29 focused tests, including the reviewed historical year sets for all 45
previous profiles and disjoint result/credit invariants.
New PDF-profile records passed 92 contributor tests; full integration acceptance remains
pending. Astra reviewed the biography sources, build inputs, release decisions, identity
joins, activity years and revised attribution model with no blocker.
The additional Records classification and renderer have passed independent Astra review.
The integrated push gate exposed an unused test binding and two missing document-map
entries; both are corrected.
The full type rerun passed in 229.2 seconds.
The complete integrated gate passed all 68 non-behavioral checks; its behavioral run
finished with 17,266 passing tests, 76 failures, 62 skips and one expected failure in
1,193.64 seconds. The focused rerun covered all 76 original failure selectors (77 cases
after the PDF-custody test gained a second source): 76 passed in 166.02 seconds, and the
remaining quoted-attribute test parser was corrected and passed in 8.05 seconds.
The three navigation/table modules passed all 53 tests in 72.97 seconds; the browser
floor passed in 31.32 seconds.
Astra reviewed the final changes without findings.
Hosted checks exposed generated explainer revision dates, quote-sensitive footer and
credit assertions, and a reproducible mobile result-title font shift.
The URL registry now agrees with the October 21 explainer revision; parsed HTML
assertions preserve exact content and links.
Under `think-i2l2`, result IDs occupy their own line on narrow screens, and heading math
retains its authored case and normal tracking.
T-037 measured 0.002 mobile layout shift in repeated light/dark runs, compared with
0.103 before the fix.
Eighteen focused tests preserve all 224 titles and cover font arrival across five
widths. These measurements apply to the tested cases, not every possible title.
The rebuilt preview passes all 16 peer-page scenarios; the rollup and footer regressions
pass 30 tests in 45.61 seconds.
The final browser floor passes in 29.46 seconds.
Hosted checks on the final pushed revision remain required before readiness.
Corrections preserve attribution, page budgets and geometry checks; they also fix nested
case-page profile URLs by rebasing links before optional quote compaction.
The served-page audit now resolves every profile destination from its containing page,
including unquoted HTML attributes.
The seven new test modules passed 121 tests in 27.50 seconds; their measured costs are
retained without changing existing weights or the unknown-cost threshold.
The snapshot budget includes the retained El Moumni volume and preserves its pending
full-inspection status.
A measured 252 MiB bound replaces the insufficient 229 MiB bound; no source evidence is
excluded to meet it.
The PDF link regression passed after Markdown formatting; the repaired PDF was rebuilt
and its seven profile annotations verified before preview promotion.
The full push gate and final hosted checks are recorded in PR #578 and `think-zpfo`;
these focused receipts do not stand in for that acceptance.

Visible oversight credit labels and links require proposed paper successors: explainer
`v0.4.14` and methods survey `v0.2.4`. The site remains the proposed `v0.9.0` batch.
Confirm all proposed edition dates at first deployment.
The next reviewer should review PR #578, starting with the final checks and diff;
merging and deployment remain separate from this handoff.

## Remaining Integration Phases

| Phase | Work and acceptance | Owner beads | State |
| --- | --- | --- | --- |
| Attribution correction | Disjoint primary results and non-primary credits, significance tallies, original-work activity years; all-profile regression and independent review | `think-94ky`, `think-gjxb`, `think-sb9n` | Model and renderer implemented; final rebuild/checks pending |
| Coverage completion | Every existing profile’s evidenced work reconciled; significant-result authors and PDF credits audited; missing joins, profiles and result records explicitly distinguished | `think-uwd6`, `think-m7il` | In progress; no complete-archive claim |
| Contract and plan reconciliation | Document canonical references, semantic checks and update procedure; reconcile current requirements and historical receipts | `think-noql`, `think-cq58` | In progress |
| Website acceptance | Rebuild all affected pages, verify table/card/link destinations and responsive presentation, run integrated gates | `think-zpfo`, presentation beads above | Pending corrected model and coverage fixes |
| Review handoff | Commit, integrate latest main/PR head, push PR #578, wait for hosted checks and publish final receipts | `think-zpfo` | Pending; do not merge or deploy |

The implementation phases below describe the original delivery sequence.
Dated review and handoff sections preserve their historical evidence; this section and
Current Integration define the next work.
The canonical model maintenance guide is
[Person Profiles](../../../../packing/contributors/README.md).

### Explicit Follow-ups Outside This PR

The owner confirmed that this PR completes profile links and stabilizes the website; new
historical result registrations are separate intake work.

| Bead | Remaining work |
| --- | --- |
| `think-m7il` | Full archive population and all 146 PDF full-credit inspections |
| `think-0v9j` | Seven unresolved spans: collective Levy credits, BuddenPing, a seed-data clause and hmbelvedere |
| `think-jtp4` | Historical original-claim intake for Gensane/Ryckelynck, Stromquist and Arslanov |
| `think-mdb2` | Profile projection of existing non-T/source-claim ledgers, including beyond-horizon records and historical Schadt work |
| `think-o3j2` | MacIver reported lower-bound intake with missing-certificate limitations |
| `think-0ltn` | Dated historical contributions lacking a canonical date-bearing record |
| `think-wwav` | Accessible profile anchors in generated atlas SVG/PDF credit paragraphs |
| `think-j13b` | Previously tracked mobile performance diagnosis |

Generated atlas credit text currently has no profile anchors: reviewed figure identity
joins establish evidence, not SVG or PDF link annotations.
The publication footnote and normal HTML name links are separate supported surfaces.
See the [coverage review](../../reviews/review-2026-10-21-profile-coverage.md) and
[PDF credit audit](../../../../packing/contributors/reviews/2026-10-21-pdf-credit-coverage.md)
for source evidence and dispositions.

## Goals and Scope

- One record per evidenced person, with optional real name, aliases, Twitter/X, GitHub,
  Substack, personal website and publication website.
- Include historical and current credit occurrences, starting with key contributors
  visible on the site and credited on retained PDFs, then reconcile the full archive.
- Source identity matches, biography facts and account ownership; omit unknown values.
- Keep directory and narrative navigation ordinary links that work without JavaScript.
  Preserve contextual enhancements only on designated case/result credit surfaces.
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
Mira, Guzhou0806 and Julian-JJ may remain handle-only profiles.
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

Home and About share a brief invitation and the standard **All Profiles** action,
without name previews.
The directory is a surname-sorted table of full real/public names, a shared separate
Results and Credits columns, public account icons with visible usernames or domains, and
cited-resource counts linking to each profile’s Resources section.
Results count distinct registered IDs with reviewed primary authorship.
Credits count distinct results explicitly crediting the person in a non-primary role,
once per person and result.
Both use the reported result’s significance.
Source packets containing several authors’ work require the reviewed result-specific
credit roles; packet authorship alone does not establish primary authorship of every
result.
The same tally renderer serves project cards and profile pages, retaining project
scope and displaying one occupied significance level as “3 results (at S4).” The typed
`site_resources` projection derives resource relationships from the existing curated
homepage inventories and explicit bylines; person records store no second list.
Credits and Resources remain separate counts.
Directory and individual profiles retain About navigation ancestry.
Profiles show additional selected **Handles** excluding repeated names and current
account usernames, account handles or URLs with platform icons, and Related News derived
from existing explicitly linked announcements.
Scoped authored prose links exact unique full names while preserving reviewed credit
joins and archived wording.
The [attribution policy](../../../../attribution.md#website-and-pdf-presentation) owns
those matching boundaries; the
[design guide](../../../../packing/devtools/templates/paper-design.md#person-profiles)
owns the shared presentation and audit contract.

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

Store `packing/contributors/people/<id>.md` with `schemas/contributor.schema.yaml`,
contract `packing.squares:Contributor/v1`, envelope `contributor`, status `enforced`.
The directory follows the layout of `packing/campaign/`. Person records are alone in
`people/`, so no other file’s name reads as a person’s. Both schemas are in `schemas/`,
each named for the kind it validates.
The occurrence manifest `occurrences.yaml` and a `README.md` sit at the top.
Each record declares its schema by relative path.
Use the existing hermetic JSON Schema validator; the installed softschema CLI provides
an independent compatibility and repair check.
New consumer fields require reviewed contract changes rather than an unvalidated
extension hidden from CI.

| Field | Meaning |
| --- | --- |
| `id` | Lowercase slug matching the filename, fixed once published: the person’s evidenced real name (`manasseh-ahmed`, `hiroaki-hosono`), otherwise the handle they publish under (`guzhou0806`) |
| `display_name` | Preferred public name: the evidenced real name where there is one, otherwise the handle; compact credits use the surname (`Ahmed`, `Hosono`) |
| `real_name` | Optional publicly evidenced name |
| `surname` | Optional evidenced family name for link labels and list ordering; requires provenance, with no word-position inference |
| `aliases` | Evidenced spellings, initials and handles; not globally unique IDs |
| `display_aliases` | Optional unique selection of evidenced aliases to show; empty by default, with provenance retained on the original aliases |
| `links` | Typed public URLs and optional handles; publication/personal sites are distinct |
| `sources` | Local IDs, repository-relative archive paths and/or primary URLs, with locators |
| `provenance` | Payload field pointers and supporting source IDs |
| `bio_sources` | Source IDs supporting the optional body paragraph |

Inline person links and directory ordering use the registry-wide naming resolver
described in
[Attribution Policy](../../../../attribution.md#one-identity-several-public-labels) and
[Person Profiles](../../../../packing/devtools/templates/paper-design.md#person-profiles).
Profile headings retain full public names; reviewed source spans retain their original
wording as evidence.
Neither surname labels nor sorting create identity joins.

Keep biography only in the Markdown body, followed by the required documentation footer,
without a heading or duplicate YAML biography field.
Consumers render it as content and never extract structured facts from it.
Phase 2 renders only inline Markdown within that paragraph, disables or escapes raw
HTML, and applies the same HTTP(S)-only URL policy to biography links as to structured
links. Test that policy in standalone pages and any retained contextual overlays.
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

Render each resolved occurrence with the shared surname-or-handle label as an anchor to
`profiles/<id>.html`, rebased to the containing page.
Designated case/result credit surfaces may enhance these links with popovers; directory
rows, project bylines and authored prose navigate directly.
Retain its original reviewed label in the occurrence record.
Profile pages link back to credited results and papers through the reviewed manifest,
preserving roles.

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

### Routes and navigation

Publish a complete static page at `profiles/<id>.html`, with canonical metadata,
lower-level breadcrumb, sitemap entry and a directory linking every published profile.
Home and About contain a short invitation and **All Profiles** button, without names.
Directory rows, account links and resource bylines use ordinary navigation.
Retired published contributor URLs retain the existing URL-history redirects.

The shared profile article remains usable by designated case/result credit overlays; it
is not a second biography renderer.
Those optional consumers retain the shared article loader’s same-site fetch, cached
pristine article, URL rebasing, scoped IDs, stale-request guards, normal-navigation
fallback and focus restoration.
Do not add an overlay to the directory or narrative links.

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

Implement standalone pages/index and the full name-link surface matrix, retaining
contextual overlays only on the designated existing credit surfaces.
Once the occurrence and renderer APIs are fixed, delegate page/overlay work, mechanical
credit conversion and content review to disjoint lanes.
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
- [x] Preserve original credit wording in the evidence record and retain roles while
  converting reviewed names to policy-compliant linked labels.
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

## Takeover: 2026-10-13

At the owner’s request, Claude Code continued this work on
`claude/admiring-goodall-q8xeuh` in
[PR #578](https://github.com/jlevy/squares/pull/578), which carries every commit of #490
and supersedes it. That branch merges `main` (327 commits) and resolves its eight
conflicts. `contributor_census --stale` and `--reconcile` now repair the occurrence
manifest after a merge: there, 41 reviewed spans had gone stale and 194 were new.
The branch adds Marc Leonard Overbeck’s record, `marc-leonard-overbeck`, the former
`kleddamag`, which has his real name and links to GitHub `Kleddamag` and X `@kleddamag`.
It also adds sourced records for John Bidwell, David Ellsworth, Thierry Gensane and
Philippe Ryckelynck, so there are 24 records.
No archived source names Muhammad Maaz.
The `/profiles/` slice below is merged, and the WIP handoff that follows is kept as
history.

Later the same day, each owner request became a bead under `think-39mp`:

| Bead | Slice | State |
| --- | --- | --- |
| `think-nyk1` | `contributor_census --stale` and `--reconcile` | done |
| `think-k9mc` | Overbeck’s record, `marc-leonard-overbeck` | done |
| `think-1y3x` | Records for Bidwell, Ellsworth, Gensane and Ryckelynck | done |
| `think-8we0` | wand125 credited as Hiroaki Hosono record-wide; record `hiroaki-hosono`, keeping GitHub `wand125` and X `@wand_125` | done |
| `think-5bao` | Merge `main`, including the n = 17 stack (#560, #571, #577), keeping both renames and joining the stack’s `Overbeck` labels | in progress while `main` moves |
| `think-2wtr` | The `people/`, `schemas/` and README layout above | done with this branch |
| `think-vqk8` | Record `manasseh-ahmed`, the former `queuingtheorydotcom`, with the owner-confirmed spelling Manasseh corrected in first-party text | done with this branch |
| `think-kf4u` | Records `oscar-fitzharding` and `david-r-maciver`, whom #588’s import of the n = 17 Lean proof credits, with their four spans joined | done with this branch |
| `think-g2ga` | ry-xu credited as Ryan Xu record-wide; record `ryan-xu`, keeping GitHub `ry-xu` and X `@small_LM` | done with this branch |

The renamed records keep forwarders at their previewed addresses
(`contributors/kleddamag.html`, `contributors/queuingtheorydotcom.html` and
`contributors/wand125.html`). With Oscar Fitzharding, David R. MacIver and Ryan Xu there
are 27 records. Population continues under `think-m7il`: 221 structured spans are
unresolved, among them Chaoweeraprasit, Ostashev, Wang, Li and Maaz.

### Regularization Integration

The first regularization merge brought `main` at `aeef99ef0` into PR #578, including the
regularized-bounds result T-155. The five conflicts retain both the upstream exact
certificate and the profile branch’s preferred personal credits, both independent
renderer regressions, and regenerated result and citation views.
The census joins two new Daniel spans without unresolved or stale additions, and the URL
registry has 1,020 rows with no failures.
Recorded derivation provenance and direct quotations retain their original labels;
published person credits come from the reviewed case and profile records.
The n=29 explanation distinguishes its historical Schadt ceiling from the current exact
regularized certificate.
Merge acceptance remains tracked by `think-5bao`, with final validation receipts on the
PR.

### News and Later Upstream Results

The 14 October integration brings `origin/main` at `37e6757ed` into PR #578, including
the news history and the later result registrations.
`think-5bao` tracks merge validation; `think-dpvm` tracks news attribution.
News prose links reviewed people to their standalone profiles and uses the preferred
name from each person record, normally the real name.
The first mention in each entry uses the full preferred name.
Retained delivery titles, quotations, source identifiers and URLs keep their original
text, as required by [the attribution policy](../../../../attribution.md).
People without reviewed profiles remain named without speculative links.

Both the profiles overview and news use ordinary navigation to individual profile pages.
Contextual credit popovers remain available on result and case pages.
The merged census adds thirteen reviewed joins and eleven unresolved spans, removes four
superseded spans, and has no stale joins.
The URL registry contains 1,026 rows with no failures.
The census now covers 27 profiles and 1,165 structured spans: 929 resolved, six
non-person and 230 unresolved.
All 146 tracked PDFs still need full inspection receipts.
Remaining population work stays in Phase 4; validation receipts are recorded on PR #578.

### Integration: 2026-10-15

This integration brings `origin/main` at `4c9af6902` into PR #578: 306 upstream commits
and 34 source conflicts, tracked by `think-5bao`. It retains the new News entries and
editorial revisions, the basic and advanced tutorials, Explanations navigation, and the
profile branch’s reviewed credit links.
News first mentions use reviewed preferred names and link directly to their profiles.
The Profiles directory and News keep ordinary profile navigation; contextual credit
popovers remain available on case and result pages.
Retained delivery metadata, source identifiers and quotations keep their original text.

The reconciled census covers 27 profiles and 1,349 structured spans: 1,032 resolved, six
non-person and 311 unresolved, with no stale joins.
All 146 tracked PDFs still await full inspection receipts.
The regenerated URL registry contains 1,056 rows with no failures.
Earlier census and route totals remain historical receipts for their own cuts.

Upstream site history through `v0.7.9` is retained, including its `v0.7.0` News and
Explanations launch.
The contributor feature takes the next minor site edition, `v0.8.0`; the infographics
retain upstream `v0.6.1`. The independent paper credit corrections remain
optimality-review `v0.1.8` and threshold-review `v0.1.1`, planned for 15 October
publication. Both sides’ paper no-public-change findings are retained for verification
against the merged outputs.
The upstream data revision is retained during the merge; its final pin is a separate
commit after the merged data is committed.

The integration retains upstream’s quick-push validation policy and complete selected
test coverage, with deep checks reserved for explicit checkpoints.
During validation, five more upstream commits landed through `6e73ef1c2` (#623), adding
News math typesetting and reader-page corrections at site `v0.7.10`. The follow-up
integration retains those changes alongside direct profile links and the proposed site
`v0.8.0` release. Initial hosted CI reported three failures, addressed by the follow-up
below. The follow-up normalizes 152 closed-form `proved_by` lists from `wand125` to
`Hosono` and aligns `apply_closed_form.py` with that credit, without changing numeric
bounds. The occurrence manifest was reconciled to the updated source labels.
Release-impact scopes were refreshed against `origin/main`; the source-based check
passes without changing paper versions.
The local case-page size correction is implemented without new dependencies: numeric
entities use equivalent UTF-8, and optional class-value quotes are omitted only on KaTeX
HTML atoms, preserving MathML and SVG. The 17-square page is 498,343 bytes against its
500,000-byte ceiling, and 11 targeted checks passed.
A fresh production render confirms that size.
All 31 active hosted checks passed at `0d8daf55c`, including the frontend suite.

The latest local push run passed 66 of 67 prerequisite checks, then its reachable
behavioral selection hit the 900-second subprocess limit.
The stale changelog-derived prerequisite was corrected and its targeted recheck passed.
Partial behavioral output also contained failures before the timeout; this is not
established as a timing-only failure or a passing push gate.
The completed hosted run establishes validation of that integration; publication
acceptance remains open.

### Further upstream integration

The next integration brings 94 commits through `3685616df` into the profiles branch,
including reports T-188 through T-192, site editions `v0.7.11` and `v0.7.12`, News
topics and counts, and isolated browser-forwarder checks.
Twelve conflicted files required reconciliation.
The site feature remains `v0.8.0`.

The census now covers 27 profiles and 1,376 structured spans: 1,052 resolved, six
non-person and 318 unresolved.
All 146 PDFs still await full inspection receipts.
News retains the earlier 39 profile links and adds six reviewed links across two new
articles. First linked mentions use preferred display names; subsequent mentions use
surnames. The URL registry contains 1,061 rows with no failures.

Curated credits in the new Greff report use Hosono consistently with the shared
attribution policy. Repository identifiers, source keys and archived text remain
unchanged. Validation results and the final head are recorded on PR #578 and
`think-5bao`; earlier green heads do not validate this integration.

The built design review covers the directory, Ahmed and Levy profiles, and News at
1280px and 390px in light and dark themes.
All 16 contexts pass the retained overflow, clipping, word-split and font checks.
Profile H1s use the shared upright, uppercase Source Sans 3 styling.
Direct directory navigation, browser Back and profile breadcrumbs also pass, including
mobile navigation without JavaScript.
The design-guide table now states direct directory navigation consistently with its
profile section.

The first hosted run found one result-page size regression: T-174 was 303,135 bytes
against a 300,000-byte ceiling.
Omitting optional quotes from safe HTML class attributes reduces it to 299,477 bytes,
preserving parsed content, links, MathML, SVG and article extraction anchors.
Case pages retain their narrower KaTeX-only compaction.

The following integration brings 40 commits through `e2e018f32` into `fb3f3e351`, with
six conflicted files.
Published site editions `v0.7.13` and `v0.7.14` remain in the history; the proposed
profiles feature stays `v0.8.0`, and paper editions remain independent.
The homepage and News archive share the same canonical announcement articles and topic
chips. Renderers preserve authored names and wording; first linked mentions follow the
preferred display names in the attribution policy.
News and the profile directory use ordinary profile navigation, while marked credits in
case and result records keep their contextual popovers.

The census is unchanged at 27 profiles and 1,376 spans: 1,052 resolved, six non-person
and 318 unresolved, with 146 PDFs pending inspection and no stale occurrences.
The current URL registry check passes with 1,061 rows and no failures.
The direct release-impact check against `e2e018f32` passes with exact no-change scopes
of 24 inputs for the explainer and 52 for the methods survey.
The fresh preview at `http://127.0.0.1:8791/` was opened in the owner’s default browser.
Twelve desktop/mobile and light/dark layout contexts and twelve direct-navigation checks
pass, including navigation without JavaScript; the three homepage articles match their
News counterparts. All 31 standard hosted checks pass on `77fe330dd`. Local broad
validation passed all 68 prerequisites but timed out in its behavioral selection; its
diagnostic retry recorded worker-startup and browser-load timing failures.
The complete hosted checkpoint and local diagnostic dispositions are recorded in
[PR #578](https://github.com/jlevy/squares/pull/578) and `think-5bao`; those live
receipts carry the final status.
The draft remains unmerged, and archive population remains open.

### Senior Review and Upstream Integration: 2026-10-18

The next integration incorporates 383 commits from main through `7d3504551`, including
the two policy-only commits that followed the reviewed code snapshot `d167d4b86`. Work
runs in an external-drive worktree, separate from both the active main checkout and the
original profile checkout.
Fourteen files conflicted: source records, generated indexes, the document map and
release declarations.
Resolutions preserve upstream result status, evidence and publication history through
site v0.7.27, posters v0.6.3 and methods survey v0.2.3. The profiles edition remains
v0.8.0.

Two independent Astra reviews examined the identity model, attribution boundaries,
rendering and publication interfaces, navigation, accessibility and design-system
consistency. They found the following defects:

- Reconciliation authorized a new source occurrence from a matching label or alias.
  New and changed spans now remain unresolved; candidate identities appear in the report
  for source-specific review.
  Unchanged reviewed source fields retain their decisions.
  `think-um9i` tracks this correction.
- Reconciliation could add an extractor’s whole-field span over a reviewed substring.
  It now preserves reviewed field coverage and validates the proposed complete manifest
  before atomic replacement.
  Failed validation leaves the prior file intact.
- A delayed profile response could replace a newer ordinary native popover, or navigate
  away after the reader opened that newer panel.
  Native openings now cancel pending article requests; success and failure responses
  have regression coverage under `think-uivz`.
- The profile-build command in the component README was invalid.
  The documented command now uses `devtools.render_overview` through the locked project
  environment.

The design review also requested readable role labels and a person-specific accessible
name for profile dialogs.
Those changes preserve credit provenance and use the existing article heading.
The earlier suggestion of a failed-stylesheet loading hang was not reproduced for 404,
500, aborted or wrong-MIME responses in the supported Chromium; disabled and preload
stylesheets are not emitted by the site.

The source-context audit checked all 729 existing automatically joined spans: 728
retained their supported identities and one stale Couzo span was removed after the
upstream case changed.
Primary sources were reviewed in documentary groups; this was not an independent reread
of every archived file or a new verification of result lineage.
The record now retains source-specific audit notes instead of matching-label
justifications. Of 60 new spans, 22 received explicit reviewed joins.
Three proposed Levy joins remain unresolved because their sources credit the project
collectively.

The resulting census has 27 profiles and 1,433 structured spans: 1,073 resolved, 354
unresolved and six non-person.
All 146 PDFs still await full-credit inspection.
The proposed site and two paper edition dates are provisional for first deployment; this
draft has not been deployed.
Published editions keep their original dates.

Focused validation passed 10 occurrence tests, 10 profile-rendering tests and 35
Chromium profile tests.
The browser floor passed its lint and type checks and 341 Node tests; schemas validated
351 Markdown records and 973 YAML datasets.

The fresh built-site review passed 50 screenshot contexts and 25 navigation checks at
1280px and 390px, in light and dark themes, including long credit lists and mobile
navigation without JavaScript.
This is Chromium coverage; physical devices, screen readers, zoom and print were not
tested.

The broader pre-push run passed all 68 prerequisites, then exposed a worker snapshot
capacity failure and an oversized T-174 page.
That run was interrupted after retaining its failures.
A desktop browser timing check also exceeded its limits; a separate navigation trace
does not establish the cause of the failed navigation.

`think-iyao` tracks the measured snapshot allowance: profile evidence newly requires
Göbel’s 4,982,398-byte archived paper.
The reviewed main snapshot occupies 222,575,174 bytes, and the integrated snapshot
approximately 229 MB. The selected repair retains that evidence and changes the bounded
allowance from 216 to 224 MiB, with private-worker custody and oversized-input refusal
tests. It does not remove evidence to fit the old limit.
`think-jhst` tracks T-174’s 300 KB limit: compact optional attribute quotes only within
published result articles, preserving parsed content, links and foreign XML. Final test
outcomes and the browser timing disposition belong in the PR receipts.

The standard hosted run at `2c071e59d` found two failures: n = 29’s adoption-history
replay and the preview watcher callback’s type check.
Under `think-isve`, the adoption writer now reproduces the retained record’s historical
wording from its prior state.
Six focused tests pass, including the replay contracts for all 53 adopted records.
No case records, evidence or identity joins changed, so no data repin is needed.
The callback type fix also passes focused BasedPyright.
Both repairs are queued for final hosted CI; that run remains required for acceptance.

The final hosted release-impact check correctly found that the n = 29 writer repair was
missing from both reviewed no-change scopes.
Under `think-97m2`, those scopes now include `adopt_houses.py`: 25 inputs for the
explainer and 53 for the methods survey.
The writer repair reproduces historical wording already retained in the case record, so
this added input is source-reviewed without claiming a new render or PDF comparison.

The next merge incorporates main `e952755bc` (PR #679), retaining published site edition
`v0.7.28` and making the profiles edition `v0.8.0` its minor successor.
It preserves all 27 profiles, the 25/53 reviewed no-change scopes and both revision
pins; the incoming Rust changes touch no data paths.
The merged URL reference validates with 1,068 rows, and 95 focused release/URL tests
pass. The explicit `--base e952755bc` release-impact check passes; the normal
`--baseline-ref e952755bc` check must run after the merge commit updates the merge base.

Review and validation receipts for this integration are recorded on PR #578 and
`think-5bao`. The historical PDF census and profiles without sufficient identity
evidence remain Phase 4 work under `think-m7il`.

## Integration After PR #671 and PR #407: 2026-10-19

The Sol continuation under `think-wrh8` integrates actual main
`e0319ffd1c96986e0260083db7d3f3411f3bb4ef`, after PR #671 and PR #407 landed.
The earlier qualification against `6833d05` retains its own source and test receipts.
All 217 result IDs, rungs and significance scores, 641 evidence IDs, every case’s bound
values and exact forms, and the current houses, rigidity records and default views are
retained. The eighteen new lower-bound rows remain V0/C0 except T-216 at V3/C3; n108’s
adopted lower bound remains `531/50`.

The selected site edition remains proposed `v0.8.0`, following actual `v0.7.30`. The
explainer inherits `v0.4.8` and its October 13 article revision; the methods survey
keeps `v0.2.3`, and the posters keep `v0.6.3`. Fresh release dispositions compare the
final 30/52 input scopes with actual main: five regenerated claim-link inputs enter the
explainer scope, and the unchanged n108 case leaves the methods scope.
The paper manuscripts, producers, methods figure inputs and explainer’s n11 citation
entry were compared exactly; no baseline paper render or PDF comparison was performed.

Review F’s F1 is fixed in `9812f19afba96325547ec02644cab03d138c4b67`: the cached
original article is detached after stylesheet discovery, before clone consumers receive
it. Its ownership regression failed before the fix and passes with all 29 tests in the
Node article-loader suite.
No heap or latency improvement was measured.
The final merged-source gates and independent follow-up review remain required; earlier
hosted success at `b76a24fd` does not qualify this integration.

The conservative census has 27 profiles and 1,437 structured spans: 1,072 resolved, 359
unresolved and six non-person.
All 146 PDFs still await full-credit inspection.
The new source’s literal n108 `wand125` credit stays unresolved rather than inheriting
the earlier lower bound’s reviewed identity join.
News wording remains prepared on PR #578; record the actual merge and delivery dates
after those events. This integration has not been deployed.

## Integration and Review: 2026-10-20

A Claude continuation integrated main twice, `4851d8193` and then `e7de85ff6` (#701,
T-223). Main had cut site editions `v0.8.0` to `v0.8.8` in the meantime, so the profile
edition is cut as `v0.9.0`, a minor successor of `v0.8.8`. The optimality review
`v0.1.8` and the threshold review `v0.1.1` keep their proposed editions.
The explainer (`v0.4.12`) and the methods survey (`v0.2.3`) keep main’s editions, with
no-public-change decisions that compare their candidate scopes with main.
Every proposed date still needs confirmation at the first deployment.

The fine-net source `[wand125 fine-net lower bounds 2026-10-16]` now credits Hosono.
Its retained packet says that all 18 of its commits are authored by Hiroaki Hosono, and
its repository is the wand125 account’s own, so it joins `hiroaki-hosono` on the same
evidence as every other wand125 source.
This supersedes the 19 October decision to keep its credit on the handle.
Results T-200 to T-217 now print `Hosono after Tokoharu and
Levy`. The same pass migrated `squarepacker` to Ryu and `ctjlewis` to Lewis under the
handle rule that `attribution.md` restores from main’s `epistemics.md`.

Three independent reviews, of the data model, the site and the content, were each
followed by fixes with regression tests:

- Reconcile refuses to drop a changed manual origin, reports each dropped join as
  `prior` on the span that replaces it, and exits 3 when a resolved join was dropped.
- Profiles now link the results they credit.
  Levy’s profile has 136 result links, Hosono’s 73 and Evan Daniel’s 80; before the fix
  they had 0, 0 and 3.
- Bios no longer call an open case optimal or a packing new.

The census has 27 profiles and 1,496 structured spans: 1,101 resolved, 389 unresolved
and 6 non-person. All 146 PDFs still await full-credit inspection.
The private-worker snapshot allowance is now 229 MiB, measured on the integrated tree.

## WIP Handoff: 2026-10-10 (historical)

This section records the state at the 10 October handoff.
Its counts, paths and open items are superseded by the sections above.

The owner requested a work-in-progress PR and handoff before further implementation.
Continue on `codex/contributor-profiles-plan-spike` in
[PR #490](https://github.com/jlevy/squares/pull/490). Implementation commit `85e0ac66f`
merges upstream `6038af33c`; the handoff commit adds documentation only.
Do not treat the earlier green CI on `ed89bfdda` as validation of this merge.
The PR is being retained as draft, with integration acceptance open.

### Generic Profile URLs (think-0v2c)

The URL migration is implemented.
`/profiles/index.html` (canonical `profiles/`) and `/profiles/ID.html` are the directory
and person-page URLs for every record.
Visible text says “Profiles”: the directory’s title, heading, intro and list label, the
colophon link, each profile’s breadcrumb and the popover’s accessible name.
Cited paper authors are therefore included without implying that every person directly
contributed to the project.
Generated credit links, the popover’s **Open profile** default, record links from reader
documents, `SITE_PAGES`, the URL register and its sitemap use `profiles/`. The directory
and the 20 profiles the reviewed preview served keep a registered forwarder at the
earlier `/contributors/` address (`render_overview.LEGACY_PROFILES`); `kleddamag`
forwards to `marc-leonard-overbeck`, and a profile added since has no forwarder.
Each of those 21 rows in `packing/site-urls.yaml` carries a 2026-10-13 amendment
recording the move. Internal names are unchanged: the `packing/contributors/` records,
the `Contributor/v1` contract, module names, `data-contributor*` attributes, CSS classes
and the occurrence manifest.
Reviewed identity joins, credit wording, source roles and the article loader’s
accessibility and no-script fallback are unchanged.

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

### Historical Setup (Superseded)

The following setup and gate receipt belonged to the October 10 handoff.
Do not use these paths or commands as the current continuation entry point.

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

The existing local preview at `http://127.0.0.1:8791/` serves the merged site, including
`/profiles/index.html`; the bead board is at `http://127.0.0.1:7790/` while its server
runs. Neither local server is a production deployment.

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
- [Site URL design](../done/plan-2026-10-06-site-urls-seo-performance.md)
- [Result-kind model](../done/plan-2026-10-01-result-kinds.md)
- [Resource archive](../../../../packing/resources/README.md)
- [Bibliography](../../../../packing/resources/bibliography.yaml)
- [Existing credit audit](../../../../packing/atlas/known-best/credit-attributions.json)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
