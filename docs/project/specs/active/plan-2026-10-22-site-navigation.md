---
title: Site Navigation and Page Hierarchy
description: Current route inventory and the Overview, News, Results, Learn, and About hierarchy with stable addresses and consistent breadcrumbs
author: Codex, for the repository owner
---
# Feature: Site Navigation and Page Hierarchy

**Date:** 2026-10-22

**Author:** Codex, for the repository owner

**Status:** Implementation in progress in draft PR #737. The landing-page and
standalone-shell slice is complete; integrated validation, reader checks, and
publication remain in progress.

**Tracking:** `think-7kbb` (coordination); `think-je3b` (landing pages and Resources);
`think-izo6` (substantive collection pages); `think-39yu` (semantic test migration)

**Workflow:** `tbd shortcut implement-beads`, following the reviewed navigation plan

## Overview

Use the confirmed top-level order **Overview**, **News**, **Results**, **Learn**, and
**About**. Overview and the site name link home; News links directly to its page.
Results, Learn, and About have dropdowns.
Results groups Visual Atlas, Frontier Survey, All Results, Verification, and Report a
Result. Learn groups Tutorials, Papers, Videos, Workbench, Posters, and Resources.
About groups The Squares Project, Contributor Profiles, and Project Documentation.

Use a small dropdown for each group, a consistent parent for each nested page, and short
homepage previews with buttons into the hierarchy.
Keep all existing public page addresses.
The confirmed label **Learn** replaces **Explanations** in navigation.
Learn is a menu container without a landing page; `papers.html` is the complete Papers
catalogue, alongside separate Tutorials, Posters, Videos, Workbench, and Resources
pages.

## Goals

- Let readers choose by purpose: find a bound, understand a proof, try a packing, follow
  new work, or contribute.
- Put the result register and the case-oriented Atlas and Frontier Survey under one
  Results parent, while explaining the difference between results and cases.
- Make every content page reachable through a collection or landing page, with the
  active top-level parent and a predictable trail on nested pages.
- Give the homepage selected content and direct actions without reproducing entire
  directories, paper catalogues, or resource lists.
- Preserve published paths, fragments, queries, downloads, record identities, and
  ordinary links that work without opening a popover.

## Non-Goals

This plan does not change scientific claims, verification levels, attribution, result
ranking, workbench behavior, hosting, or domain configuration.
The implementation retains the static build and introduces neither a site framework nor
a global search service.
Page-weight work already tracked as `think-v1qe` remains a separate implementation
concern; reorganizing navigation does not by itself reduce table bytes.

## Background

The source baseline is `59b1ec594` on 2026-10-22. The inventory comes from
[the URL register](../../../../packing/site-urls.yaml), the shared
[navigation partial](../../../../packing/devtools/templates/site-nav.html),
[page producers](../../../../packing/devtools/render_overview.py),
[document and chapter producers](../../../../packing/devtools/site_documents.py), and
[profile producers](../../../../packing/devtools/render_contributors.py).
The retained `site-squaremath-domain` build from the domain work was also read for
headings, current navigation, and visible breadcrumbs on the main pages, workbench, and
sample records. This is an inspection of source and an existing rendered artifact, not a
new build or a production crawl.
The current tree below records that baseline.
The homepage retains a short Profiles statement and View All Profiles button; About uses
an inline Contributor Profiles link in its project narrative.

All reader-facing addresses in this proposal use `https://squaremath.org/`. Paths in the
trees are relative to that root.
The separate [domain plan](plan-2026-10-22-squaremath-domain.md) owns publication at
that host.

### Audience journeys

| Reader’s task | First destination | Next step |
| --- | --- | --- |
| Find the best known packing or bounds for a particular n | Results → Visual Atlas | One case record, its sources, and relevant results |
| Check a new theorem, certificate, or improvement | Results → All Results | One result record, its affected cases, evidence, and authors |
| Learn the problem and its methods | Learn → Tutorials | Advanced tutorial, paper, or interactive workbench |
| Read a particular proof | Learn → Papers | The paper’s HTML, PDF, and source; linked result records |
| See or manipulate packings | Learn → Videos or Workbench | Atlas and individual cases when evidence is needed |
| Follow recent work | News | Announcement, then the linked result, paper, or profile |
| Identify a contributor or submit a result | About → Contributor Profiles; Results → Report a Result | Person’s credited work or the existing submission route |
| Reproduce or extend the project | About → Documentation | Synopsis, conventions, development guide, and repository |

The result register is organized by contribution; the Atlas and Frontier Survey are
organized by number of squares.
Neither collection contains the other.
Their common Results parent makes both discoverable without turning each result or case
into a menu entry.

## Current Site Inventory

The URL register contains **1,149 registrations**, of which **666 are content HTML
pages**. Asset patterns count as register entries, not as enumerations of every emitted
asset.
The [complete route disposition index](plan-2026-10-22-site-navigation-routes.csv)
lists all 1,149 baseline entries with their current kind, canonical address, proposed
parent, and disposition.
Its `inventory_status` column separates those `existing` rows from eight `added` rows:
the seven substantive pages listed in the current route disposition and the retained
Downloads compatibility forwarder.
Those routes are excluded from all baseline counts below.
Counts describe this baseline; implementation must reconcile later registrations before
changing navigation.

| Registered kind or family | Count | Meaning for navigation |
| --- | ---: | --- |
| General content pages | 15 | Main pages, tutorials, documentation, film, and workbench |
| Synopsis chapters | 18 | Generated chapter pages, reached from the Synopsis index |
| Profile directory and profiles | 76 | One directory and 75 individual people |
| Case records | 324 | One full page per n, from 1 through 324 |
| Result records | 229 | One full page per registered result |
| Paper HTML pages | 4 | Three n = 11 papers and the packing-methods paper |
| **Content HTML subtotal** | **666** | Collections and their content, not 666 menu items |
| Forwarders | 30 | Compatibility pages, including old contributor addresses |
| Other paper files | 8 | Four PDF and four Markdown editions |
| Byte copies | 6 | Published compatibility copies of papers or posters |
| Asset registrations | 437 | Drawings, posters, icons, and four hashed-asset patterns |
| Site files | 2 | `404.html` and `sitemap.xml` |
| **All registrations** | **1,149** | Content, compatibility, assets, and site infrastructure |

### Current navigation and content tree

`[page]` means a content HTML page; `[section]` means a fragment within a page;
`[family]` means individually published pages; `[external]` leaves the site.
The tree shows how readers reach content, so a shared preview can appear in more than
one place. It does not imply that duplicate previews are separate pages.

```text
Site name → / [page; home]
├── Overview → / [page; same destination as site name]
│   ├── The Square Packing Problem [section #the-problem; hero n = 53]
│   ├── Atlas preview [section #the-atlas-of-square-packings]
│   │   └── Atlas page, case records, and complete poster PDF
│   ├── News preview [section #news] → news.html
│   ├── Recent Major Results [section #recent-results] → results.html
│   ├── Profiles preview [section #profiles] → profiles/
│   ├── Report Your Results [section #report-your-results]
│   ├── Papers cards [section #papers] → tutorials and papers.html
│   ├── Visuals [section #visuals]
│   │   ├── Poster PDF and inline film
│   │   └── All PDFs → papers.html#pdfs; View Visualizations → visualize.html
│   ├── Squares Project Documentation [section #squares-project-documentation]
│   │   └── README, Epistemics, Synopsis, Conventions, Development
│   └── More Resources [section #more-resources; external project/source cards]
├── News → news.html [page]
│   └── News/changelog entries, filters, and dated entry anchors [sections]
├── Atlas → atlas.html [page]
│   ├── Graphical Atlas [section #the-atlas-of-square-packings; 324 tiles]
│   ├── Frontier Survey [section #the-frontier-survey; explanation]
│   ├── Best Known Results [section #best-known-results; 324 table rows]
│   └── cases/1.html … cases/324.html [family; 324 full case records]
├── Results → results.html [page]
│   ├── Added in the Last Seven Days [section]
│   ├── Earlier Publications [section #earlier-results-by-week-published]
│   ├── Verification Ladders [section #verification-ladders]
│   ├── Evidence and Exactness [section]
│   ├── Result Types and Credits [section #results-and-credits]
│   ├── Status and Supersession [section]
│   ├── Browse Results [section #all-results; filtered/sorted table]
│   └── result/t-001.html … result/t-229.html [family; 229 full records]
├── Explanations → papers.html [page]
│   ├── Tutorial [section #tutorial]
│   │   ├── tutorial.html [page; first-principles tutorial]
│   │   └── tutorial-advanced.html [page; advanced tutorial]
│   ├── Papers [section #papers]
│   │   ├── papers/n11-lower-bounds-explainer.html [page; Part I]
│   │   ├── papers/n11-threshold-bound-review.html [page; Part II]
│   │   ├── papers/n11-optimality-review.html [page; Part III]
│   │   └── papers/square-packing-methods-survey.html [page]
│   ├── PDFs [section #pdfs; poster download cards]
│   └── Visuals [section #visuals; full inline film and local navigation]
│       ├── Film local link → papers.html#visuals
│       ├── Workbench local link → workbench/ [page]
│       │   └── Animate / Pack / Search; Animation studio [application states]
│       └── visualize.html [page; standalone film with the same local links]
├── About → about.html [page]
│   ├── The Squares Project [section #the-squares-project]
│   ├── Profiles [section #profiles; same preview as home]
│   │   └── profiles/ [page; directory]
│   │       └── profiles/<person>.html [family; 75 profiles]
│   │           └── Records, Results, Credited Work, Other Reviewed Records,
│   │               Related News, public accounts, and resources [profile sections]
│   ├── Report Your Results [section #report-your-results]
│   └── Squares Project Documentation [section #squares-project-documentation]
│       ├── readme.html [page; project guide]
│       ├── epistemics.html [page; verification and significance policy]
│       ├── synopsis.html [page; chapter index]
│       │   └── synopsis/<chapter>.html [family; 18 chapters]
│       ├── conventions.html [page]
│       └── development.html [page]
└── GitHub [external utility link]
    └── Repository-only research records, archive, defects, and developer sources
Color theme [utility control; System / Light / Dark]
```

The global bar currently has six content links plus GitHub: Overview, News, Atlas,
Results, Explanations, and About.
The Film/Workbench links are a local navigation row, not global tabs.
Workbench modes, Atlas layout and size choices, table filters, news filters, popovers,
and theme choices are controls or states within pages.
They do not add pages to the route count.

The five documentation pages and all Synopsis chapters currently mark **GitHub** as
current even though the reader is still on the site.
Profiles mark About as current and visibly show `About → Profiles` ancestry.
Case and result pages declare structured breadcrumbs in their metadata, but the
inspected sample pages have no equivalent visible breadcrumb navigation.
At that baseline, About itself had no breadcrumb.

### Compatibility, fragments, downloads, and external material

The inventory baseline’s 30 forwarders comprise 21 `contributors/` addresses, four Atlas
aliases (`frontier.html`, `status.html`, `cases.html`, `cases/index.html`), one Results
alias (`all-results.html`), three paper aliases, and `defects.html`, which leads to the
repository’s defect log.
Preserve incoming queries and fragments when changing their destinations.
At that baseline `frontier.html` forwarded to `atlas.html`; the implemented hierarchy
restores it as the substantive survey page and forwards historical Atlas survey links
there.

The six copies are the two `known-best-*.pdf` aliases, the old `t-018-explainer`
Markdown and PDF, and the old `n11-optimality/t-060-explainer` Markdown and PDF. The
four paper families each publish HTML, Markdown, and PDF editions.
These download links belong with their papers; they are not additional menu entries.

Of the 437 asset registrations, 420 are Atlas drawings: 324 house drawings, 95
regularized drawings, and the Trump eleven-square overview drawing.
The other 17 registrations cover poster images and exports, icons, the social card, and
four hashed-asset/data patterns.
Films are external release assets, reached from the film page.
Crawler and deployment artifacts do not belong in the content hierarchy.

Preserve homepage aliases such as `#the-atlas`, `#learn-more`, `#pdfs`, `#video`,
`#pdfs-and-videos`, and `#other-square-packing-projects`; the About contribution and
news aliases; result-row and news-entry anchors; Atlas tile and survey-row anchors; and
Synopsis’s old section landings.
The route CSV inventories registered paths, not every anchor, query combination, or
external resource. Implementation must check those against the generated pages and their
existing compatibility tests.

The literature archive, evidence inventory, research experiments, sessions, hypotheses,
raw frontier Markdown, and defect log are repository material linked from the site.
They do not each have a separately published site page.
Synopsis chapters summarize and link these collections.
An external project card is a citation or resource link, not a local subpage.

## Design

### Proposed hierarchy

Overview and News are direct links.
Results, Learn, and About are menu containers: each label and chevron form one button
that opens its dropdown.
The first menu item leads to substantive content, rather than a category preview page.
Learn has no separate landing page or URL. Keep one dropdown level; collection pages
handle individual cases, people, papers, and chapters.

```text
Site name → / [Home; selected previews and actions]
├── Overview → / [direct link; same homepage]
├── News → news.html [direct link; announcements and changelog]
├── Results [menu container]
│   ├── Visual Atlas → atlas.html [menu; page; first Results item]
│   │   └── cases/N.html [324 case pages]
│   ├── Frontier Survey → frontier.html [menu; page; 324-row bounds table]
│   ├── All Results → results.html [menu; complete sortable and filterable register]
│   │   └── result/t-NNN.html [229 record pages]
│   ├── Verification → verification.html [menu; result ratings and evidence guide]
│   │   └── Project Epistemics → epistemics.html [page; full policy, reached by button]
│   └── Report a Result → report.html [menu; contribution instructions]
├── Learn [menu container; no category page]
│   ├── Tutorials → tutorials.html [menu; complete tutorial catalogue]
│   │   ├── tutorial.html
│   │   └── tutorial-advanced.html
│   ├── Papers → papers.html [menu; complete paper catalogue]
│   │   └── Four paper HTML pages, each with its PDF and Markdown editions
│   ├── Videos → visualize.html [menu; page]
│   ├── Workbench → workbench/ [menu; page]
│   ├── Posters → posters.html [menu; packing poster PDFs]
│   └── Resources → resources.html [menu; complete directory]
└── About [menu container]
    ├── The Squares Project → about.html [menu; project page]
    ├── Contributor Profiles → profiles/ [menu; directory]
    │   └── 75 profile pages
    └── Project Documentation → documentation.html [menu; full documentation directory]
        ├── readme.html
        ├── synopsis.html → 18 chapter pages
        ├── conventions.html
        └── development.html
GitHub and color theme [utilities]
```

Results has five dropdown entries, Learn six, and About three.
The menus omit individual records and the 18 Synopsis chapters.
Each menu destination has substantive content.
Only Overview carries summary previews.
Actual menu destinations use their menu label for browser and preview titles, page
headings, and current breadcrumb items, from the shared `navigation_title` lookup.
The homepage is the explicit heading exception: its menu/browser label remains Overview,
but its H1 remains **The Square Packing Problem**. Verification, Contributor Profiles,
Project Documentation, and Workbench use their exact menu labels.
Preserve scientific source-document titles and legacy anchors; the rendered reader page
supplies its canonical navigation heading.
The next homepage section is **Visual Atlas**; the result-preview section is titled
**Results**, retaining `#recent-results` and one **View All Results** action.
Preserve its existing `#the-atlas-of-square-packings` and `#the-atlas` anchors without
adding a duplicate problem subtitle.
Project Epistemics remains cross-linked from Project Documentation, tutorials, and
result explanations; its canonical parent is Verification under Results.

### Landing pages and content ownership

**Results.** Results is a menu container with no landing page.
`results.html` is **All Results**, the one complete sortable, filterable result
register. The menu, H1, browser title, breadcrumb, and result-record parent use that
exact label. Visual Atlas, Frontier Survey, and Verification share one action row after
the table, with no collection actions above it.
Keep every registered result once, with claims, cases, credits, ratings, status, and
canonical result-record links.
Preserve existing filters and result-row addresses.
The homepage retains its bounded recent preview and one **View All Results** action.
The complete Learn section follows Results immediately; all other homepage sections
retain their relative order.
`recent-results.html` becomes a compatibility forwarder to All Results; there is no
second complete result-table page.
Old recent section fragments map to `results.html#all-results`, while `#t-NNN` rows and
queries keep their canonical targets and filter state.

**Verification**, at `verification.html`, contains the complete rating, evidence,
credit, and status guide, including its visual rating guide and exactness examples.
All Results links to it after the table.
Verification links by one action to **Project Epistemics**, at `epistemics.html`, the
separate detailed policy document.
Legacy verification/evidence/credit/status fragments forward to the matching
Verification anchors with queries preserved and useful no-script links.
Do not copy Atlas graphics or the 324-case bounds table onto All Results.

**Visual Atlas and Frontier Survey.** Give each its own substantive Results page.
`atlas.html` opens with all 324 packings visible; the homepage keeps its shorter
preview. The Atlas has no Packings / About the Bounds / Best Known Bounds local
navigation. `frontier.html` is headed **Frontier Survey** and contains the complete
324-row bounds table with a concise key to its definitions and columns.
Preserve the reported/verified distinction, exact verification requirements, gap and
decimal semantics, row records, sorting, and filters.
Detailed audits and case histories belong in the records opened from the table.

Historical Atlas survey headings, table fragments, and `#n-N` rows forward to the survey
with their queries and fragments preserved; `#atlas-n-N` continues to select an Atlas
tile. Both pages and the menu use the same canonical title for each destination.

**Learn.** Use the menu as a container for complete content pages, with Tutorials first.
`papers.html` contains the four research papers and their series narrative;
`tutorials.html` contains both complete tutorial cards and reading guidance;
`posters.html` contains the two Atlas packing poster PDFs and their source links.
The Tutorials page ends with a **Read Papers** action to `papers.html`. There is no
generic Downloads catalogue or paper-editions table; each paper keeps its own PDF and
Markdown editions on its detail page.
Videos, Workbench, and Resources retain their substantive pages.
No Learn page or visible single-button subsection duplicates these destinations.
Legacy `papers.html#tutorial`, `#pdfs`, `#visuals`, and `#resources` links forward to
the corresponding page, preserving queries.
Without JavaScript, inline compatibility links at those fragments reach the same
destinations. `#papers` and `#explanations` remain on the Papers catalogue.
Keep `downloads.html` as a compatibility forwarder to Posters, preserving queries and
fragments. The old `#pdfs` target remains on Posters; `#paper-editions` continues to the
Papers catalogue, with a useful no-script link.
Keep every published PDF artifact.

**About.** Keep the project narrative at `about.html`, titled The Squares Project, with
its full-name attributions and a contextual Contributor Profiles link.
Keep `#profiles` on that inline link, without a separate Profiles heading, summary, or
View All button; the homepage retains its Profiles preview.
The complete documentation catalogue lives at `documentation.html`; the complete
contribution instructions and submission link live at `report.html`. Legacy About
documentation and contribution fragments forward to those pages, with inline no-script
compatibility links.
About may cross-link Resources under Learn; profile Resources fields continue to link a
person’s own sources.

**Resources.** Add `resources.html` as the complete directory under Learn, using the
existing external-resource data and card renderer.
Move the full collection from the homepage to this page.
Overview keeps a short summary and a View All Resources button; its old
`#more-resources` and `#other-square-packing-projects` landings remain useful summary
links. The directory has the breadcrumb Learn → Resources, with no competing full
directory on About.

**News.** Keep dated announcements and the full changelog together.
The result register is separate from News; News entries can cover papers, downloads, and
site changes as well as mathematical results.
Topics/Tags uses the shared dropdown multiselect.
Significance remains the inline segmented S-buttons, using the same component as the
Atlas Grid/Triangle controls; the default selection remains S4/S5. Preserve
`news-topics` and `news-s` query state, history and fragments, plus complete no-script
news access. All Results uses its separately requested S1–S5 multiselect segments under
think-p39d; Verification and Confirmation retain their floor selects.

### Homepage composition

Retain the problem introduction and hero, then a compact Atlas preview.
Follow with selected recent news, a bounded recent-results preview, selected learning
cards, and short About/contribution links.
Keep the user’s chosen visual presentation while reducing the amount of complete
catalogue content on the page.

| Current homepage content | Proposed homepage treatment | Complete destination |
| --- | --- | --- |
| Problem and n = 53 hero | Retain concise introduction and case link | Tutorial; case 53 |
| Atlas preview and controls | Retain a bounded preview, existing expand behavior, and View Visual Atlas action | Visual Atlas; Best Known Bounds; complete PDF |
| News cards | Selected recent entries and View All News button | `news.html` |
| Results (`#recent-results`) | Bounded selected rows with one View All Results action | `results.html#all-results` |
| Profiles section | Short statement and View All Profiles button; no names or table | `profiles/` |
| Report a Result | One invitation and Report a Result button | `report.html` |
| All tutorial/paper cards | Selected starting points with View All Tutorials and View All Papers actions | `tutorials.html`, `papers.html` |
| Poster and inline film | One media preview with View Videos, Workbench, and Posters actions | `visualize.html`, `workbench/`, `posters.html` |
| About the Squares Project | One direct About the Squares Project action, retaining the documentation-section anchor | `about.html` |
| Full external resource cards | Short summary and View All Resources button | `resources.html` |

Use shared records and existing card renderers for previews; do not maintain a second
copy of the full content.
Preserve old homepage anchors with visible summary landings and destination links.
Do not depend on JavaScript redirects to make those old links useful.
A preview count or selection rule is presentation data, never a new assertion about
result significance or contributor status.

### Route disposition and page parents

All 666 content pages keep their addresses.
Six new substantive pages are registered: `resources.html`, `tutorials.html`, and
`posters.html` under Learn, `documentation.html` under About, and `report.html` and
`verification.html` under Results.
The added `recent-results.html` address is retained as a compatibility forwarder to All
Results. The superseded `downloads.html` is retained as a compatibility forwarder.
The route CSV marks them as `added`, separately from the 1,149 baseline registrations.
The CSV expands the generated families and technical registrations; this table specifies
the reader-facing parent for every named page or family.

| Path or page family | Proposed label or role | Parent and disposition |
| --- | --- | --- |
| `/` (`index.html`) | Overview / Home | Overview and site-name destination; selected previews |
| `recent-results.html` | Compatibility forwarder | All Results; preserve queries and row fragments; map old section fragments to `#all-results` |
| `results.html` | All Results | Results; complete table remains at `#all-results` with query filters |
| `result/t-NNN.html` (229) | Result identifier and title | Results → All Results; retain record contents and evidence links |
| `atlas.html` | Visual Atlas | Results; all 324 packings visible by default |
| `frontier.html` | Frontier Survey | Results; concise bounds key and complete table |
| `atlas.html#the-frontier-survey`, `#the-survey`, `#best-known-results`, `#frontier-table`, `#n-N` | Historical survey links | Forward to the corresponding Frontier Survey fragment with query preserved |
| `cases/N.html` (324) | Case n | Results → Visual Atlas; reached from either Atlas or bounds table |
| `verification.html` | Verification | Results; full ratings, evidence, credit and status guide extracted from the archive |
| `epistemics.html` | Project Epistemics | Results → Verification; separate detailed policy reached by its action |
| `papers.html` | Papers | Learn; complete paper catalogue with retained address and legacy fragments |
| `tutorials.html` | Tutorials | Learn; complete tutorial catalogue |
| `posters.html` | Posters | Learn; the two packing poster PDFs and their source links |
| `downloads.html` | Compatibility forwarder | Forward to Posters; retain queries and poster fragments; paper-editions reaches Papers |
| `tutorial.html` | Tutorial | Learn; retain first-principles text |
| `tutorial-advanced.html` | Advanced Tutorial | Learn; retain advanced text and links |
| `papers/n11-lower-bounds-explainer.html` | Part I: New Lower Bounds | Learn; keep full title on the paper |
| `papers/n11-threshold-bound-review.html` | Part II: Certified Lower Bound Review | Learn; keep full title on the paper |
| `papers/n11-optimality-review.html` | Part III: Optimality Review | Learn; keep full title on the paper |
| `papers/square-packing-methods-survey.html` | How Record Square Packings Are Found | Learn; retain paper and editions |
| `visualize.html` | Videos | Learn; full player and release links |
| `workbench/` (`workbench/index.html`) | Workbench | Learn; retain application states and shareable URLs |
| `resources.html` | Resources | Learn; complete resource directory |
| `news.html` | News | Top-level page; preserve `#changelog` and entry anchors |
| `about.html` | The Squares Project | About; project narrative with preserved compatibility fragments |
| `documentation.html` | Project Documentation | About; complete reader and developer document catalogue |
| `report.html` | Report a Result | Results; complete contribution instructions |
| `profiles/` (`profiles/index.html`) | Contributor Profiles | About; full directory |
| `profiles/<person>.html` (75) | Person’s evidenced name | About → Contributor Profiles; retain all reviewed identity and credit content |
| `readme.html` | Project Guide | About; keep README content and source link |
| `synopsis.html` | Research Synopsis | About; full chapter index |
| `synopsis/<chapter>.html` (18) | Chapter title | About → Research Synopsis; keep previous/next links |
| `conventions.html` | Conventions | About; documentation entry |
| `development.html` | Development | About; documentation entry |

The 18 Synopsis chapters are: **The Program at a Glance**, **The Problem**, **The
Program So Far**, **The Cell Decomposition**, **n = 11 End to End**, **The Corner and
the Method It Forced**, **The Lay of the Land by n**, **Theoretical Results**, **What Is
Built**, **The Hypothesis Registry**, **Experiments Conducted**, **Sessions Conducted**,
**The Defect Record**, **Where This Stands**, **Workflow Entry Contracts**, **Handoff
Record**, **Terminology**, and **References**. Their exact paths appear in the CSV. They
remain chapters, rather than competing with their parent in a dropdown.

### Breadcrumbs and active navigation

Pages with collection ancestry show a breadcrumb above their heading, consistently
across kpress articles, static records, profiles, and the workbench shell.
Standalone Overview and News show no visible breadcrumb and emit no structured
`BreadcrumbList`. Their global navigation still marks the current page.
Nested pages retain their collection ancestry and plain final item.
Results, Learn, and About are menu containers with no category landing URL, so their
content pages show the container as plain ancestor text before the current page title.
The final breadcrumb item is always plain text, never a link.

| Page | Visible trail, ending with the current page |
| --- | --- |
| Overview | None |
| News | None |
| Results register | Results → All Results |
| The Squares Project | About → The Squares Project |
| Visual Atlas | Results → Visual Atlas |
| Case 11 | Results → Visual Atlas → n = 11 |
| Result T-060 | Results → All Results → T-060 |
| Verification | Results → Verification |
| Project Epistemics | Results → Verification → Project Epistemics |
| Papers, Tutorials, Posters, Tutorial, Advanced Tutorial, or a paper | Learn → Current title |
| Videos, Workbench, or Resources | Learn → Videos / Workbench / Resources, as appropriate |
| Profile directory | About → Contributor Profiles |
| Person profile | About → Contributor Profiles → Person’s name |
| Report a Result | Results → Report a Result |
| Project Documentation, Project Guide, Conventions, or Development | About → Current title |
| Research Synopsis | About → Research Synopsis |
| Synopsis chapter | About → Research Synopsis → Chapter title |

Keep Overview available through the site name without repeating it in every nested
trail. Generate visible ancestry and structured `BreadcrumbList` data from the same
parent definitions; if the structured form includes Home, its remaining ancestors must
match the visible trail.
The final item is text with `aria-current="page"`. Ancestors with a substantive
destination are links; Results, Learn, and About are plain container text with no
invented category URL. A Visual Atlas table section does not create a second breadcrumb
trail for the same case.
A result opened from a profile still belongs to Results → All Results.
Browser Back and contextual related links handle the path the reader actually took.

Mark the active top-level group by its descendant relationship.
Use `aria-current="page"` for the current page label, and an appropriate ancestor
indication such as `aria-current="true"` with a visible style for a group whose child is
open.
A fragment link may identify the selected location after explicit navigation; avoid
marking both Visual Atlas and its bounds section as the current page.
Use the same rules after a hard reload, a direct deep link, and browser Back.

Videos and Workbench are separate destinations in the Learn menu, with Videos linking
directly to `visualize.html`. Remove the Film/Workbench switcher and its persistent
local navigation row; neither content page needs a second category chooser.
Workbench’s Animate, Pack, and Search controls retain their separate application
semantics. Popovers retain a clear full-page action; their navigation must not create a
second global header inside the overlay.

### Dropdown and small-screen behavior

Use semantic navigation lists and disclosure buttons.
Overview and News keep ordinary link behavior.
Each grouped label and its chevron are one button exposing `aria-expanded` and
`aria-controls`; pressing either part opens the same list.
Its first link leads to substantive content.
All controls work with a keyboard or touchscreen.
Do not require hover, and do not assign application-menu roles to ordinary site links.
Keep the original chevron states: closed points down and open points up.
Only reverse the transition’s direction: expansion rotates by -180 degrees instead of
+180 degrees, and collapse reverses it.
Reduced motion preserves the same endpoint states without animation.

Tab reaches links and buttons in document order.
Enter or Space toggles a disclosure; Escape closes it and returns focus to its
disclosure button. Closing a menu must not leave focus in hidden content.
Outside activation closes it without blocking the activated link or stealing focus.
Opening one disclosure closes the other, and focus indicators remain visible.
Hover can supplement these interactions, never replace them.

On narrow screens, show a labelled Menu button that reveals the same groups as a
vertical list with inline disclosures.
It must fit without horizontal scrolling, work with enlarged text, and keep touch
targets separated.
Do not add flyout submenus or require the reader to dismiss a modal to
follow a link. Without JavaScript, expose the navigation links or provide a native
disclosure fallback; neither primary navigation nor the content pages may become
unreachable.

An open disclosure or keyboard focus within the header keeps the scroll-aware header
visible. Account for the header when scrolling to fragments so a section heading or
focused control is not hidden.
Coordinate dismissal with the existing theme popover and case/result/profile overlays.
Keep the site navigation usable in both themes and with reduced motion, and preserve the
current print behavior.

### Shared design-system component

The dropdowns must match the site’s existing design system.
Define one navigation disclosure component in
[Design System](../../../../packing/devtools/templates/paper-design.md) before
implementing its shared styles.
Document the typography, label casing, spacing, surface and text colors, border
treatment, disclosure-icon size and alignment, focus indicator, active-parent state, and
open/closed states. Reuse the existing KPress, `paper-type.css`, and navigation tokens;
add a shared token only for a role the current system does not express.

Collection links use **View All … →**: View All Profiles, View All Resources, View All
News, View All Papers, View All Tutorials, and View All Posters.
The homepage’s Atlas action is **View Visual Atlas →**, matching the first Results menu
destination. The homepage’s result preview has one **View All Results →** action to the
complete register. Tutorials ends with **Read Papers →**, using the same action style.
Render the existing shared right-arrow component after the label; keep the decorative
icon out of the accessible name.
Use the existing action-link component, with consistent size, padding, alignment, icon
spacing, and focus treatment.
Buttons and action links share `--paper-button-letter-spacing`, resolving to
`var(--kpress-caps-spacing, 0.021em)`. Apply it through the common casing component to
ordinary buttons, `site-action` and `site-popover-action` links, and retained tab links;
news filter buttons reuse the same token.
Mathematics inside labels keeps normal tracking.
Collection navigation styled as a button remains an actual anchor with its destination
in `href`. Individual detail links name the case, result, person, or paper; contribution
actions retain purpose-specific wording such as Report a Result.
Document this vocabulary and its examples in the same Design System entry.

Navigation and general site descriptions use the shared sans face: menus, breadcrumbs,
page headers, local navigation, collection-section headings, compact navigation
metadata, collection introductions, contributor-directory guidance, contribution
prompts, and reading suggestions.
Mark these with the shared `site-navigation-heading` and `site-navigation-copy` roles
where native navigation elements do not express the role.
Choose the role by the paragraph’s purpose, not whether it contains a mathematical term
or link.
Text explaining where to read, browse, download, or contribute is site guidance.
Substantive mathematical exposition and News article bodies retain the serif face,
including the homepage’s opening explanation of the square packing problem and its upper
and lower bounds. Do not apply a blanket paragraph override.
Remove GitHub icons from the site footer; retained footer links keep their text.

The reading measure is 35em of the shared prose font base, or 630px at an 18px base.
Card groups use that same outer width across catalogues and profile resources, with a
shared frame rule and a responsive column count capped to the actual number of cards.
Large cards use an 18rem minimum and fit two columns from 37rem; two Tutorials cards
therefore fill the reading measure without an empty third slot.
Wide tables, Atlas drawings, paper figures, and the Workbench application remain
visual/data surfaces rather than alternate prose measures.
Headings resolve the same calculated reading width instead of interpreting em against
their own font size.
Displayed breadcrumbs align their left edge with the header logo text through shared
responsive header geometry; this latest rule supersedes their earlier alignment to the
prose column. Column padding sits outside that text measure.

News article prose remains serif; publication, artifact, and supporting-record metadata
remains muted sans. Metadata group labels occupy their own lines, and each artifact,
publication-evidence, PR, or reference link occupies a separate line.
Display the first publication date without parenthesizing the evidence link, and omit
terminal periods and middle-dot separators around metadata links.

Use the same component and tokens in every page producer and the workbench shell.
Do not introduce per-page dropdown markup or styling.
The design-system entry must also specify keyboard and touch behavior, narrow-screen
expansion, no-script fallback, light/dark themes, reduced motion, and scroll-aware
header interaction. Link the shared stylesheet and behavior implementation back to that
entry, and include representative paper, record, profile, and workbench pages in visual
review.

### Profile, popover, and footer consistency follow-ups

These follow-ups belong to the navigation and consistency implementation under
`think-7kbb`. The table records the requested behavior; the linked beads carry current
implementation and validation status.
Document their shared components and states in the existing
[Design System](../../../../packing/devtools/templates/paper-design.md).

| Bead | Requirement and acceptance |
| --- | --- |
| `think-2abe` | Put Accounts second, immediately after Name, in the profile directory. Preserve the relative Records → Results → Credits order and existing sorting and responsive behavior. |
| `think-7kbb` | Active coordination parent: reconcile all current requests, child/spec links, integration evidence, and final publication. |
| `think-5yys` | In progress: apply the shared 35em reading measure and prose-aligned card groups, cap columns to actual cards, use sans navigation chrome, remove footer GitHub icons, and preserve corrected chevron endpoints/motion. |
| `think-j4jk` | Remove repeated Recent Results introductions, contents links and per-day filter navigation; this first cleanup is superseded by the single-table view under `think-vasz`. |
| `think-0xj7` | Use each menu destination’s canonical label for its H1, browser metadata and current breadcrumb; rename Project Documentation and Contributor Profiles consistently; put Report a Result last under Results, outside About; preserve the explicit homepage Problem/Visual Atlas/Results preview labels and no-trail Overview/News rule. |
| `think-vasz` | Completed predecessor: the arrival-ordered Recent Results table; superseded by the canonical All Results consolidation under `think-6ts0`. |
| `think-oala` | Completed predecessor: disclosure for older Recent Results rows; the duplicate page is retired under `think-6ts0`. |
| `think-6rnk` | Closed: migrate Verification guide assertions to its dedicated page without restoring duplicated archive prose. |
| `think-z3lz` | In progress: current-head CI integration repairs and final artifact validation. |
| `think-7r1w` | Extract archive explanation into Verification and keep Project Epistemics as the separate detailed policy reached by its action; preserve legacy fragments. |
| `think-7xta` | Replace Downloads with canonical Posters, containing only packing poster PDFs; retain old Downloads and paper-edition compatibility routes without deleting artifacts. |
| `think-p3xu` | Use shared sans semantic roles for general site descriptions, contributor and collection introductions, contribution prompts, and reading guidance; preserve serif mathematical exposition. |
| `think-9lhb` | Only News Topics/Tags becomes a dropdown multiselect; retain shared inline significance S-buttons, S4/S5 defaults, and existing URL/history/no-script behavior. |
| `think-kmpp` | In progress: complete preview rebuild, integrated browser and registry/link checks, current-head CI, and publication readiness. |
| `think-ximb` | Audit every page family for the shared 35em prose measure and card-edge alignment; retain only deliberate wide data/visual surfaces. |
| `think-1k0j` | Align every displayed breadcrumb below the header logo text using shared responsive geometry, superseding prose-column alignment. |
| `think-dows` | Remove the obsolete secondary-film paragraph from Videos, preserving the primary video and other content. |
| `think-3qn4` | Put Visual Atlas first in Results; final collection/menu consolidation is tracked by `think-6ts0`. |
| `think-mdrd` | Separate Frontier Survey into its own substantive page, show all 324 Atlas packings by default, retain incoming survey links, and keep canonical survey labels. |
| `think-6ts0` | Consolidate complete result collections into All Results at `results.html`; keep the bounded homepage preview and retain Recent Results as a compatibility route. |
| `think-dq6a` | Put Tutorials first in Learn and add the shared Read Papers action at the bottom of Tutorials. |
| `think-aefa` | Set the numeric total in each profile-table tally in bold, never italic; keep its result, record, or credit label in regular weight. Preserve muted significance parentheticals and blank zero cells through the shared tally component. |
| `think-mpxs` | Give shared profile, result, and case popovers roughly 60% more width on wide screens where space permits. Base the shared responsive rule on `--kpress-measure`, panel padding, and viewport gutters. Audit the current 36rem general and 46rem framed-page ceilings rather than multiplying every variant. Cap prose measure while preserving room for case visualizations, narrow-screen fit, focus, controls, scrolling, and freedom from horizontal overflow. |
| `think-klec` | Use diagonal outward arrows for the shared expand action. Prefer Lucide `maximize-2` if available in the existing pinned icon set; otherwise use a coherent shared equivalent. Preserve shared icon sizing, the accessible Open full page label, and identical header/footer destinations wherever an overlay opens a full page. |
| `think-vvy9` | Remove the Profiles footer link. Put “Formatted and typeset with Flowmark and KPress” on its own line and the displayed version on the bottom line. Apply the same layout across shared footer variants, retaining project/repository attribution and the existing version provenance. |

### Components and interfaces

Use one declared hierarchy for top-level groups, menu entries, page-family parents, and
breadcrumb labels. Route membership must be explicit for overlapping collections such as
Epistemics and profile-linked results.
Reuse the URL register for existing addresses and the page producers for record
membership; do not turn the dated CSV into a second live route registry.

Register and render the new Resources page through the existing page and URL producers.
The implementation touches the shared `site-nav.html` and `site-nav.css`, navigation
rendering in `render_overview.py`, its overview/article templates, `site_documents.py`,
`render_case_pages.py`, `render_contributors.py`, result and paper rendering, and the
workbench’s shared navigation integration.
Browser behavior belongs in repository JavaScript or TypeScript files under the existing
browser floor. No new package is needed merely to render links and disclosure controls.

There is no external API change.
Existing canonical paths, record identities, filter parameters, workbench state links,
and asset URLs retain their meanings.
Internal navigation helpers will need a page identity and parent lookup rather than only
the current flat `data-page` key.
Visible breadcrumbs and metadata must use that lookup.

## Implementation Plan

### Phase 1: Agree the hierarchy and route contract

- [ ] Use the confirmed order Overview, News, Results, Learn, About; review the dropdown
  contents and homepage ownership.
- [ ] Reconcile the inventory with the then-current URL register and retain a
  disposition for every content page, alias, and named fragment family.
- [x] Define the shared parent map and page-family rules.
  Keep the current paths and the initial Atlas/Frontier section arrangement.
- [ ] Review a small desktop/mobile navigation prototype, including a case, a profile,
  and the workbench, before applying it to every producer.

### Phase 2: Implement navigation and landing pages

- [x] Update the shared Design System document with the navigation disclosure component,
  its tokens, states, and accessibility/interaction contract; use that component
  consistently across pages and the workbench.
- [x] Add shared dropdowns, active-parent rules, and ancestry breadcrumbs across all
  page producers and the workbench.
- [x] Reorganize Results and Learn with the specified entry points; add the full
  Resources directory at `resources.html` under Learn; include the About project page
  with Overview and News as standalone pages without breadcrumb trails.
- [x] Reduce homepage catalogues to previews and direct actions while preserving old
  anchors and ordinary links.
- [ ] Audit collection buttons across Overview and all landing pages for the shared View
  All … wording, right-arrow component, spacing, and focus styling; retain distinct
  detail-link and contribution-action labels.
- [ ] Complete the five tracked profile, popover, and footer follow-ups above and
  document their tally, width, expand-action, and footer conventions in the Design
  System.
- [ ] Keep the full record pages, download editions, compatibility forwarders, and
  query/fragment behavior intact.

### Completed shared navigation and popover slice

The `think-pfsk` slice defines the five navigation groups and one parent lookup in
`packing/devtools/site_navigation.py`. Visible and structured breadcrumbs use the same
lookup. The shared disclosure controller preserves ordinary links and no-script access,
adds the mobile Menu, and keeps an open or focused header visible.
The Design System records its typography, states, focus treatment, and collection-action
convention. Breadcrumbs sit 1rem below navigation and leave 2.5rem before the title;
paper format chips occupy that gap.
They are hidden in print and overlays.

The `think-mpxs` and `think-klec` fixes use the standard reading measure plus padding
for prose panels, preserve the wider case stage and viewport gutters, and share the same
diagonal expand glyph and full-page destination in both icon modes.
Profile headings reserve space for both controls, and standalone profiles use the shared
trail gap without an extra vertical offset.

Focused checks passed on 2026-10-22: nine navigation/component tests, 34 existing
navigation assertions, header baseline/type/control checks, two breadcrumb/title
geometry checks, and the real long-profile control check at 320 pixels.
The final semantic breadcrumb-selector regression passed independently: one test, 24.17
seconds. Ruff, helper types, browser formatting, and the overview JavaScript type check
passed. Phase 3 retains responsibility for the complete build, validation, and reader
journeys.

### Completed landing and standalone-shell slice

The `think-je3b` slice reorganized Results with the register table immediately after its
introduction and local links; added Atlas section links; kept complete tutorial, paper,
and download catalogues on their own pages under Learn; and moved the ranked shared
resource directory to `resources.html`. Overview now uses selected learning cards and
visible summaries at its retained collection fragments.
The four standalone paper shells and Workbench use the shared breadcrumbs and navigation
program, with both declared as render inputs.
The Papers catalogue retains `papers.html#explanations`. The `think-izo6` follow-up
separates Tutorials, Downloads, Documentation, and Report a Result into substantive
pages, without a Learn category page or visible stub sections.

Focused checks passed on 2026-10-22: six section-helper tests, 21 landing/resource
tests, 11 Workbench navigation/input tests, and four standalone-paper tests.
These cover the existing resource ranking and linked bylines, shared card text and
dates, collection links, retained fragments, parent breadcrumbs, navigation scripts, and
freshness inputs.
The follow-up collection split passed 30 focused content checks and its
canonical-route regression.
All six changed page producers rendered through the published-math pipeline; the URL
register checked at 1,154 entries with no failures.
These checks cover the full tutorial, paper, poster, document, and contribution content
on the new pages, plus preserved profile credits and legacy destination links.

The `think-qxq2` follow-up makes Results a container and moves the complete daily
arrivals and weekly publication lists to `recent-results.html`. All Results keeps the
table, filters, row addresses, rating guide, and explanatory anchors; the Visual Atlas
keeps its existing page and section addresses with its new title.
Overview links both result collections.
Eight focused checks passed, including the page split, retained row links and filters,
four migrated paper/video expectations, and the archive runway at its unchanged byte
ceiling. The generated URL register now has 1,155 entries with no failures.

The integrated build, full validation surface, and reader checks remain in Phase 3.

### Phase 3: Verify reader journeys and publish

- [ ] Check every route family against the parent map, and verify all dropdown and
  breadcrumb targets in a built artifact.
- [ ] Exercise the journeys, keyboard/touch behavior, responsive layouts, deep links,
  browser history, and no-script fallbacks described below.
- [ ] Run the repository’s applicable validation tiers, review the implementation PR,
  and check the deployed pages at `squaremath.org` after publication.
- [x] Separate Frontier Survey from the Atlas at the owner’s request; keep both as
  substantive Results destinations and preserve historical incoming links.

Implementation began after PR #733 merged and the owner authorized the reviewed
hierarchy. The coordination bead remains open through integrated validation and reader
checks; the completed landing slice is tracked separately above.

## Testing Strategy

Check the CSV’s existing rows against all baseline URL-register entries and audit added
substantive pages and compatibility routes separately.
Verify counts and named-page coverage, check relative documentation links, run the
document-map renderer/check, and format the new Markdown with the project’s pinned
Flowmark. A complete site build verifies the implemented hierarchy.

For implementation, extend existing navigation, document, profile, record, and workbench
checks rather than copying template markup into new tests.
Prove that each content page has exactly one top-level parent, each nested page has a
resolvable acyclic ancestry, and no asset or forwarder appears in a content menu.
Reconcile the complete generated route set, including newly added records, rather than
hard-coding 666 as a permanent site limit.

Browser acceptance covers desktop and narrow mobile layouts in both themes, keyboard
navigation, touch activation, increased text size, reduced motion, and disabled
JavaScript. Check every dropdown item at least once.
Include representative direct loads of a paper, advanced tutorial, profile, result, case
11, a late Atlas case such as 291, a Synopsis chapter, the Resources directory, and the
workbench. Verify menu focus and dismissal, sticky header interaction, current-parent
indication, visible/structured breadcrumb agreement, and a plain current-page label on
every nested page, including the About children; Overview and News have no trail.
Confirm the shared 35em reading measure and the absence of a Film/Workbench switcher.
Expand a News entry and check that metadata links each occupy their own line, with serif
article prose and muted sans metadata.

For the profile/popover follow-ups, check Accounts immediately after Name while Records,
Results, and Credits retain their relative order.
Compare nonzero and zero tallies, including significance parentheticals.
Exercise each shared popover at wide and narrow widths and after scrolling; verify its
text-width cap, viewport gutters, focus, and controls.
Check that both outward-arrow actions have the Open full page accessible name and the
same destination.
Compare shared footer variants: no Profiles link, the formatting credit
on its own line, and the provenance-backed displayed version on the bottom line.

Retain regression coverage for `frontier.html` and case aliases, old contributor
addresses, old paper downloads, legacy homepage and About fragments, result filters,
result-row links, news-entry links, synopsis section landings, and Atlas tile/table
anchors. Confirm the complete Atlas opens all 324 cases and the homepage preview stays
bounded; optional collapse and tile links still reach the correct target.
A compatibility pass must also work without JavaScript where that behavior is currently
supported.

Follow [the validation tiers](../../../../development.md#validation-tiers): edit checks
while changing code, reachable push checks before publishing a branch, the normal PR
fast surface, and the full checkpoint at implementation close.
Measure any changed page weight and browser cost against the existing published-page
budgets.
A menu change must not introduce a new rendering or navigation fetch dependency.

## Rollout Plan

Land this plan separately from the current presentation and domain work.
Implement only after its review choices are settled.
Publish the shared hierarchy and matching landing-page links together, with the site
build’s existing URL and link checks.

Keep the route register and compatibility outputs intact throughout.
Check the live Home, Results, Atlas bounds anchor, Learn, a profile, a result, and
Workbench after publication.
A revert of the navigation implementation restores the preceding layout without changing
scientific records or invalidating published URLs.

## Open Questions

- **Homepage selection?** Recommend retaining the Atlas preview and recent news/results,
  with a smaller selection of learning content.
  The homepage people section retains its short statement and View All Profiles button.
  About links the directory contextually in the project narrative.
  Choose learning cards during visual review rather than inventing a new ranking policy
  in this plan.
- **Frontier as its own page?** Recommend the direct Results menu anchor and Atlas local
  navigation first. Revisit only with evidence that the combined page remains difficult
  to use or exceeds its measured rendering limits.

## References

- [Complete route disposition index](plan-2026-10-22-site-navigation-routes.csv)
- [Published URL catalogue](../../site-urls.md) and
  [URL registration implementation](../../../../packing/devtools/site_urls.py)
- [Current layout plan](plan-2026-10-08-site-layout-and-navigation.md)
- [Contributor profiles plan](plan-2026-10-10-contributor-profiles.md)
- [News and changelog plan](plan-2026-10-13-site-changelog.md)
- [Domain plan](plan-2026-10-22-squaremath-domain.md) and
  [deployment guide](../../guides/site-deployment.md)
- [Workbench page template](../../../../packages/workbench/assets/template.html)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
