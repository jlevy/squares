---
title: Compact Homepage, Consistent Case Layouts, and Scroll-Aware Navigation
description: Website remediation plan with visible atlas and results previews, dedicated detail pages, clean case and popover math, and shared Headroom navigation
author: Codex, for the repository owner
---
# Feature: Compact Homepage, Consistent Case Layouts, and Scroll-Aware Navigation

**Date:** 2026-10-08

**Author:** Codex, for the repository owner

**Status:** Implemented in draft PR #462; hosted verification in progress

**Tracking:** `think-2u4x` (epic), `think-s54c` (planning)

**Workflow:** W9 remediation

## Overview

Make the Square Packing website easier to scan and navigate.
The homepage starts with a short problem introduction and a **The Squares Project** card
linking to `about.html`. The atlas preview comes next, followed by **Recent Major
Results**, then **Papers**, **PDFs**, **Video**, **Squares Project Documentation**, and
**More Resources**. Papers and documentation reuse the dedicated pages’ cards; PDF
downloads and the inline video remain separate sections.
The Atlas has **Show More** and **Explore** buttons; the results preview links to the
complete Results page.
All buttons use uppercase labels through shared design rules.
Card titles use Chicago Manual of Style Title Case, preserving mathematical notation,
acronyms, and proper names; descriptions remain in sentence case.
The full project section moves to the About page, with **About** in the top navigation
immediately to the left of **GitHub**. Case records and popovers share readable layouts
and math. A shared header hides while scrolling down and returns immediately when
scrolling up, on desktop and mobile.

The owner confirmed the header direction, visible atlas and results previews, the
homepage order, paper-card grouping, and the About page and navigation position.
This spec lists the fixes and their acceptance criteria.

## Goals

- A substantially shorter homepage with a clear overview, brief section introductions,
  and visible atlas and results previews.
- Prominent buttons from those previews to dedicated pages containing the complete atlas
  and results table.
- The atlas directly after the problem introduction, followed by **Recent Major
  Results**, then **Papers**, **PDFs**, **Video**, **Squares Project Documentation**,
  and **More Resources**.
- A dedicated About page for the full **The Squares Project** section, a compact project
  card beneath the homepage intro text, and **About** immediately before **GitHub** in
  the top navigation.
- Consistent case-page and popover layouts, with readable mathematics, starting with the
  reported rendering problem for $n = 291$.
- Navigation that remains easy to reach while scrolling on desktop and mobile.
- Centered single-card groups, uppercase button labels, and compact popover headings
  without duplicate result titles.

## Non-Goals

Scientific bounds, attribution, evidence classifications, and verification records keep
their existing meaning.
This is a presentation and navigation change.
The workbench’s packing behavior and the papers’ mathematical content are outside this
repair wave; shared button typography applies to their controls too.

## Background

The current implementation already renders a static subset of recent results, with full
filtering on `all-results.html`. Each result has a canonical `result/t-NNN.html` page.
The homepage atlas contains all 324 tiles, with lazy external drawings; 100 tiles are
initially visible. There is no dedicated visual Atlas page.
`frontier.html` is the survey table, and `cases/N.html` is a complete case record whose
article also supplies the case popover.

The homepage’s long introductions and full atlas make the initial overview too large for
the owner’s intended layout.
The owner also reports ugly or broken mathematics in the $n = 291$ case popover.
Its exact visual failure and cause still need reproduction; this plan does not treat a
source inspection as a confirmed diagnosis.

Source inspection identifies useful fixtures: the verified interval includes a long
rational upper bound in one inline formula, and the record’s general-bound prose uses
plain ASCII mathematics.
The interval has no local overflow rule outside the prose container.
Check those paths first and retain $n = 291$ in the browser fixtures.

This wave builds on the [overview plan](plan-2026-09-29-github-pages-overview.md) and
preserves the static pages, canonical addresses, and published-link guarantees of the
[URL and rendering plan](plan-2026-10-06-site-urls-seo-performance.md).

## Design

### Homepage and dedicated pages

Use only H1 and H2 headings on the homepage.
Main section headings share the introduction’s sans, uppercase title styling; the legend
retains its compact label role.
Give main section headings a modest extra 0.5rem of space above them.

Keep the homepage in this order:

1. Show the single native hero packing for 53 squares above the introduction.
   Center it at a compact width and retain its case popover.
   Use the caption: “Best known packing for 53 identical squares.
   Colors indicate angle.
   Darker colors mean more common shared faces.”
   Restore the two explanatory introductory paragraphs: first describe the long-standing
   geometry question and define $s(n)$, then explain upper and lower bounds with the
   owner’s $s(29) \le 5.934$ and reported $s(29) \ge 5.81$ examples.
   The hero graphic opens its case popover, with its case record as the no-script
   destination. The popover offers separate Case Record, Frontier row and Atlas tile
   actions. The full Frontier Survey lives below the graphics on the Atlas page, with a
   distinct target for each table row and graphical tile.
   An Atlas tile link fully expands the grid before scrolling to and highlighting the
   requested tile, including cases beyond the initial hundred.
   Follow it with a centered **The Squares Project** card linking to `about.html`.
2. Embed the existing SVG atlas graphic, initially filtered to fewer rows, with **Show
   More**, **Download PDF**, and **Explore the Atlas** buttons.
   Download the complete 1–324 PDF, with a shared down-arrow-over-baseline icon.
   Place the download action immediately before Explore.
   In-place expand/collapse controls use the shared double-down/double-up chevrons
   respectively, synchronized with state.
   Omit explanatory selection/tile prose.
3. **Recent Major Results** immediately below the atlas: up to twelve S4-or-higher
   results and a prominent **View all results** button.
   Omit the count and scope sentence.
   Omit an introductory sentence that only explains the links.
   Center the legend card at a medium width, with a centered small-caps **LEGEND**
   heading. Make the whole card link to `all-results.html#verification-ladders`.
   Significance, Verification and Confirmation each occupy their own line, with icons
   and chips in one column and labels aligned to their right.
   Remove the “What each rung means” text from the homepage card.
4. **Papers** mirrors all reading cards on the Papers page, using shared content and
   destinations. **PDFs** holds the poster downloads, followed by **Video** with its
   native click-to-play player.
   **Squares Project Documentation** mirrors About’s introductory text and documentation
   cards through shared rendering.
5. **More Resources** as an H1 above the related-project cards.
   Remove the link-summary block and redundant catalogue introduction.
   Keep **Squares Project Documentation** on both the homepage and About, and retain the
   old related-project anchor for existing links.

Move paper cards out of the introduction or atlas area into **Papers**. Keep every paper
reachable through that group and use concise card copy.
Keep PDF cards on the homepage and Papers page.
Keep the video on the homepage and Visualize page, in a separate group from PDFs.
Remove media from the dedicated Atlas page.
Remove the shorter-film/release/receipt paragraph from the homepage; media card eyebrows
are simply **PDF** and **Video**. Center every card group that contains one card,
including the project card beneath the introduction.

Move the full **The Squares Project** section’s project narrative, approach,
attribution, and contextual links to `about.html`. Its homepage card has a brief
description and opens that page.
Keeping the card within the intro area leaves Atlas as the second section.
Add **About** to the shared top navigation immediately before **GitHub**, on desktop and
mobile. Break the About narrative into short paragraphs, including before “Now several
others”. Use only H1 section headings on About, all with the same title styling as The
Squares Project. Add the H1 **Contribute Your Results!** above the reporting invitation.
Keep **Squares Project Documentation** on both the homepage and About.
Remove **Reading and Research** from About.
Papers retains its paper, tutorial, and PDF cards; omit redundant Frontier Survey and
Workbench cards from both pages.
Use the shared header for the About page and retain the source material’s meaning and
links. Preserve the existing homepage `#the-squares-project` destination on the project
card or forward it to the About page.

Use a compact row subset of the original SVG atlas and up to twelve recent results
initially. Recent results must be S4 or higher, dated within the last 180 days, and not
superseded. Keep the complete results page’s filters unchanged.
The register currently contains six qualifying entries; the twelve-row limit allows the
preview to grow as results qualify.
Each headline links to its canonical result page.
The atlas preview preserves the original SVG drawings, colors, and case destinations in
six Triangle rows, cases 1 to 36. Web labels show only the case number and an applicable
recent-result star; the PDF retains its additional labels.
Both pages use the shared Atlas layout and animation engine.
Prepare the remaining drawings during initialization so Show More starts immediately.
The first click reveals 100 cases; the second reveals all 324. Keep Triangle at each
stage. At full coverage Show Less restores 36, using the same shared animation.
Explore remains a direct link to the dedicated Atlas page.
Without JavaScript, retain the visible SVG preview and Explore link.

Publish the complete interactive atlas at `atlas.html`, reusing its existing drawings,
view controls, and case-record behavior.
Triangle is the default; Grid is explicitly selectable with `?atlas=grid`, and existing
`?atlas=triangle` links remain valid.
Collapsed coverage is approximately 100 cases: Grid ends on a complete rectangular row
for its current width and size; Triangle ends on a complete square-number group.
Recompute the count on width, size, and view changes.
Web Atlas tiles show only their case number and any recent-result star; bounds and
evidence marks remain in the popover.
PDF labels retain their full metadata.
The homepage uses the same **Show More** and **Show Less** controls as the Atlas page.

Expanded coverage is strictly all 324 cases, including a short final Grid row when
necessary (`think-b2o9`). Keep the complete results table and filters at
`all-results.html`. Use the Atlas as the case directory, with the Frontier survey below
its graphics. Forward old case-directory addresses to the Atlas, preserving individual
case records. The shared navigation exposes the Atlas page while retaining access to
Frontier.

Register `atlas.html` and `about.html` in `packing/site-urls.yaml` and the builders’
page, asset, crawl, preview, and Pages-scope declarations.
Preserve the existing homepage atlas fragments and query view state when forwarding to
the full atlas. Keep the recent-results anchor useful for its preview and preserve
existing result and case addresses.

Related-project material remains accessible through the compact resource area.
The open `think-lt7k` task belongs to the earlier overview epic; its homepage-card
expectations must be reconciled with this layout during implementation, with its source
coverage retained.

### Case pages and popovers

Use one set of content-width, spacing, heading, drawing, bounds-summary, and math rules
for the standalone case record and its article inside a popover.
Adapt the available width to the container.
Case-property icons and significance/verification/confirmation chips use one shared
styled tooltip system, with meaningful descriptions, theme-aware surfaces, standard
transitions, keyboard focus, and reduced-motion behavior (`think-tg0p`). The same
treatment applies to icons in fetched popovers and tables.

Shared screen scrollbars are thin, with transparent tracks and theme-aware thumbs,
including popovers and horizontal diagrams (`think-7y0v`). Stack the centered case
packing diagram above the number line at every width.
Give the sticky destination-button footer equal padding above and below its buttons.

Center the compact **Case Record** label above a prominent typeset $n = N$ count.
Place case icons first, followed by any recent-result star and notes, then status tags.
Remove **All cases** from the case steps.
The sticky footer offers separate Case Record, Frontier row, and Atlas diagram links,
each with the same right arrow.

Popovers must fit the viewport, provide usable scrolling and a reachable close control,
and preserve focus and the link to the complete case page.
Balance the drawing with the title, bounds and summary so its current height limit does
not force the useful overview below an oversized figure.

Reproduce $n = 291$ through both the direct case page and the atlas or Frontier popover.
Check prepared math, its inherited font context, and long bound expressions before
choosing a fix. Keep exact expressions available; reflow or locally scroll long formulas
without clipping glyphs or creating page-wide horizontal overflow.

Use compact sans heading scales for case, result and document popovers.
Once a result article loads, keep its complete main heading and remove the small
duplicate preview title.
Keep a useful title during loading or failure and preserve accessible dialog names and
unique heading IDs.

### Shared Headroom header

Use the owner’s confirmed behavior:

- Visible at the top of the page.
- Hide while scrolling down once clear of the top region.
- Reappear on the first meaningful upward scroll, without requiring a return to the top.
- Stay visible while navigation has focus or the theme menu is open.
- Preserve a usable header without JavaScript; disable animated travel for reduced
  motion.

Apply the same behavior to ordinary pages, standalone case and result pages, synopsis
chapters, the three paper shells, and Visualize.
Keep the Workbench header visible when its document does not scroll.
Include secondary tabs in the header geometry and account for mobile wrapping, resizing,
anchor offsets, and touch overscroll.
An open theme menu must remain attached to its control.

Implement the behavior once in a checked browser source file and shared wiring.
The existing KPress header, static-content shell, paper shells, and Workbench shell all
need coverage; their markup is not currently identical.

### Components and interfaces

| Surface | Main source |
| --- | --- |
| Homepage sections and previews | `packing/devtools/templates/overview-article.md`, `packing/devtools/overview_sections.py` |
| Page generation and shared wiring | `packing/devtools/render_overview.py`, `packing/devtools/site_assets.py` |
| Case article and overlays | `packing/devtools/render_case_pages.py`, `packing/devtools/overview/case-popover.js`, `packing/devtools/overview/popover.js` |
| Prepared mathematics and its fonts | `packing/devtools/site_math.py`, `packing/devtools/overview/math.js` |
| Shared styling and navigation | `packing/devtools/templates/site.css`, `packing/devtools/templates/site-nav.css`, `packing/devtools/templates/site-nav.html` |
| Shared button and popover typography | `packing/devtools/templates/paper-type.css`, `packing/devtools/templates/paper-design.md` |
| Workbench shell | `packages/workbench/tools/workbench_tools/build_site.py` |
| Published addresses and deployment scope | `packing/site-urls.yaml`, `packing/devtools/pages_scope.py`, `.github/workflows/pages.yml` |

Atlas and About are the two proposed public route additions.
Reuse current case, result, and table interfaces, the existing design tokens, and the
prepared-math pipeline.

## Implementation Plan

One repair phase, with independently scoped issues.
Each issue adds its own focused regression coverage; the final browser review checks
their combined behavior.

| Issue | Bead | Priority | Scope and acceptance |
| --- | --- | --- | --- |
| L1: Repair the $n = 291$ case math | `think-18kd` | P1 | Reproduce on the direct page and case popover, identify the failure, then render all formulas without parse errors, missing glyphs, clipping, or raw markup. Retain a regression that exercises the actual failure. |
| L2: Normalize case and popover layouts | `think-0ahf` | P1 | Consistent headings, spacing, drawings, bounds and math across both containers. No viewport-wide overflow; long content scrolls inside the popover and its close control remains reachable. |
| L3: Tighten the homepage and preserve both previews | `think-5c8r` | P1 | Order: intro with centered project card, Atlas preview, Recent Major Results, Papers, PDFs, Video and Squares Project Documentation, resources. Filtered initial SVG rows and up to twelve S4+ recent results; no count/scope sentence; linked legend card; prominent destination buttons. |
| L4: Publish the complete dedicated Atlas page | `think-a9au` | P1 | All 324 cases and existing view controls work at `atlas.html`; case links/popovers work; navigation and the URL registry include it; legacy atlas links and view state still reach the full atlas. |
| L5: Add shared Headroom navigation | `think-byu7` | P1 | Hide down, show immediately up on desktop and mobile; visible at top and during focus/menu use; all four shell families covered; no layout jump or obscured anchor target. |
| L6: Verify the combined website layouts and interactions | `think-xio5` | P2 | Browser checks cover section order, paper-card grouping, previews and buttons, the About page and project card, About immediately before GitHub in the nav, the dedicated Atlas and Results pages, $n = 291$ math, popover scrolling/focus, and header direction. Retain reviewed before/after screenshots across representative shells, widths and themes. |
| L7: Publish The Squares Project About page | `think-h21i` | P1 | Move the full project section to `about.html`; retain its narrative, attribution and links; add About immediately before GitHub in the shared top nav; the homepage project card opens About; register and crawl the new route. |
| L8: Expand the homepage Atlas in place | `think-hyd6` | P1 | Show More alongside Explore; retain native SVG drawings in initial Triangle rows 1–6 (36 cases), immediately animate to 100 then 324 with two Show More clicks, and Show Less back to 36 using the shared engine; retain destinations and keyboard state. |
| L9: Standardize uppercase button labels | `think-rfy8` | P1 | One shared design rule across site, popovers, Atlas, papers and Workbench; preserve mathematical case and card prose. |
| L10: Remove duplicate result titles and tighten popover headings | `think-1rg7` | P1 | One visible main title after article loading, meaningful fallback, unique accessible heading IDs, compact shared sans hierarchy. |
| L11: Align the navigation gear | `think-675d` | P1 | Gear follows GitHub in the shared track and aligns with navigation text across desktop and mobile shells. |
| L12: Separate and place media cards | `think-erq7` | P1 | PDF cards on homepage and Papers; click-to-play inline video on homepage and full player on Visualize. Separate groups; no autoplay or initial video download on homepage; no media cards on Atlas. |
| L14: Hero popover and expanded Atlas case navigation | `think-h3ms` | P1 | A single centered native hero packing for 53 uses the requested best-known caption and opens its case popover; separate record/Frontier/Atlas actions follow current case. Atlas targets fully expand before revealing the matching tile, including n=291/324. |
| L17: Case popover hierarchy and Atlas directory | `think-g28m` | P1 | Centered Case Record eyebrow and larger mathematical count; icons, star/notes, then tags; shared right-arrow destination buttons; remove All cases and forward directory URLs to Atlas. |
| L18: Web Atlas labels and shared controls | `think-ngcg` | P2 | Web graphic shows only case number and applicable star, PDF detail preserved; homepage Show More/Show Less controls match Atlas through 36 → 100 → 324. |
| L19: Subtle shared scrollbars | `think-7y0v` | P2 | Thin theme-aware thumbs and transparent tracks across shared screen surfaces. |
| L20: Shared evidence tooltips | `think-tg0p` | P2 | Meaningful styled hover/focus tooltips for case-property icons and S/V/C levels, including fetched popovers; standard motion and reduced-motion support. |
| L21: Readable introduction | `think-8xzs` | P2 | Restore both owner-provided explanatory paragraphs with prepared math and upper/lower-bound examples. |
| L22: About H1 headings | `think-6m9n` | P2 | About uses H1 section headings throughout, preserving anchors and body content. |
| L23: Atlas PDF download action | `think-axt8` | P2 | Download PDF immediately before Explore the Atlas; shared download icon and uppercase action styling; complete 1–324 PDF. |
| L24: Six-row homepage Atlas preview | `think-hl8r` | P2 | Initially show cases 1–36 in six complete Triangle rows; Show More to 100 then 324, Show Less to 36. |
| L25: Matching reading and documentation sections | `think-sq1i` | P2 | Homepage Papers mirrors all reading cards, PDFs stays separate, and Squares Project Documentation matches About. About H1s share The Squares Project title style. |
| L26: Integrate the new methods paper | `think-mbp9` | P2 | Preserve current-main methods reading, use its canonical Title Case card, and apply shared Headroom/tooltip shell behavior. |
| L15: Consolidate Frontier Survey under Atlas | `think-od15` | P1 | Full survey after graphical Atlas; distinct row/tile fragments, legacy Frontier forwarding and unified top navigation. |
| L16: Complete responsive Atlas preview rows | `think-b2o9` | P1 | Around 100 collapsed cases, ending on complete rectangular Grid rows or complete square-number Triangle groups at every width and size; recompute on view, size, and resize; expanded coverage remains strictly all 324. |
| L13: Honor SVG Atlas themes | `think-pvod` | P1 | Initial, expanded and cached SVGs use shared live light/dark theme tokens for backgrounds, labels, outlines and badges; preserve native packing colors and geometry. |

Start with L1’s reproduction so its regression identifies a real failure.
L2 and L5 can be developed independently.
L3 integrates with L4 and L7 so the preview buttons and project card have working
destinations. L6 depends on the website implementation issues.
Give parallel writers disjoint files; keep shared templates, route registration, and
integration with one owner.

Implementation lanes use Sol agents for homepage content and previews, case math and
layouts, and shared navigation.
The coordinator owns route registration, shared asset wiring, the local server,
integration checks, and commits.
An Astra agent reviews the combined change before completion.

## Testing Strategy

Extend the existing case, math, overview, atlas, URL, and shared-header browser
contracts, including `test_case_pages.py`, `test_site_case_records.py`,
`test_site_math.py`, `test_site_math_preferences.py`, `test_overview.py`,
`test_site_atlas_views.py`, `test_site_urls.py`, and `test_site_wide_blocks.py`. Keep
probes in JavaScript files and use browser conditions and animation frames to
synchronize scroll checks.

Check at least 390 px mobile and 1280 px desktop, plus a narrower 320 px overflow pass.
Cover light and dark themes, reduced motion, and static content without JavaScript.
Exercise direct and fetched case articles for $n = 5, 11, 17, 291, 324$, repeated
popover opening, keyboard close/focus restoration, and long formulas.
The case page and popover must retain the same claims, evidence links, and semantic
math.

Header checks include top, down, immediate up, focus, an open theme menu, resize, anchor
navigation, a paper page, a generated case/result page, and the Workbench.
Homepage checks assert the section order, all paper cards grouped under **Papers**, the
project card’s About target, actual preview limits, and both primary buttons.
About checks assert the retained project content and links, and **About** immediately
before **GitHub** in the shared top navigation.
Atlas checks assert complete case coverage, old-link forwarding, reversible homepage
stages 36 → 100 → 324 → 36, immediate animation without click-time requests, repeated
expansion/collapse, reduced motion, and native SVG colors and labels.
Measure the homepage against the existing 1.3-megabyte page ceiling.
Check uppercase computed button styles, the legend card’s destination and keyboard
activation, hero popover actions, expanded Atlas targets for n=53/291/324, centered solo
cards, and the loaded T-115 result popover’s single title and accessible name.
Reuse `preview_site.py` for the visual review and the existing site-page measurement
tools for established rendering budgets.

Follow [development.md’s validation tiers](../../../../development.md#validation-tiers):
focused checks and `--edit` during implementation, the reachable `--push` surface before
pushing, PR frontend and fast checks, and the full checkpoint at final review.
Fast regressions belong in the existing CI surface.

## Rollout Plan

Build and review the local static site with desktop and mobile screenshots before
publishing the website changes.
Update the URL registry and generated route view with the Atlas and About additions,
verify old addresses, and use the existing Pages deployment workflow.
Close the epic when all implementation issues and the combined browser review pass.
Planning completion leaves the implementation issues open.

## Remaining Verification

- Finish hosted checks on the final PR revision.
- Run the full pre-merge checkpoint tracked by `think-xio5` before merging.
  The reviewed homepage starts with cases 1 to 36 in six Triangle rows.

## References

- [Original overview plan](plan-2026-09-29-github-pages-overview.md)
- [Static pages and published URLs](plan-2026-10-06-site-urls-seo-performance.md)
- [Site URL registry](../../../../packing/site-urls.yaml)
- [Case 291 source record](../../../../packing/frontier/n-291.md)
- [Homepage template](../../../../packing/devtools/templates/overview-article.md)
- [Case page renderer](../../../../packing/devtools/render_case_pages.py)
- [Shared navigation](../../../../packing/devtools/templates/site-nav.html)
- [Validation and development](../../../../development.md#validation-tiers)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
