---
title: Compact Homepage, Consistent Case Layouts, and Scroll-Aware Navigation
description: Website remediation plan with visible atlas and results previews, dedicated detail pages, clean case and popover math, and shared Headroom navigation
author: Codex, for the repository owner
---
# Feature: Compact Homepage, Consistent Case Layouts, and Scroll-Aware Navigation

**Date:** 2026-10-08

**Author:** Codex, for the repository owner

**Status:** Draft; issues identified and tracked, implementation pending

**Tracking:** `think-2u4x` (epic), `think-s54c` (planning)

**Workflow:** W9 remediation

## Overview

Make the Square Packing website easier to scan and navigate.
The homepage gives a short introduction, visible previews of the atlas and recent
results, and prominent buttons to the complete Atlas and Results pages.
Case records and popovers share readable layouts and math.
A shared header hides while scrolling down and returns immediately when scrolling up, on
desktop and mobile. The PDF copy fix uses the owner’s supplied definition of the square
packing problem.

The owner confirmed both the header direction and the requirement to keep the atlas and
results previews visible.
This spec lists the fixes and their acceptance criteria.

## Goals

- A substantially shorter homepage with a clear overview, brief section introductions,
  and visible atlas and results previews.
- Prominent buttons from those previews to dedicated pages containing the complete atlas
  and results table.
- Consistent case-page and popover layouts, with readable mathematics, starting with the
  reported rendering problem for $n = 291$.
- Navigation that remains easy to reach while scrolling on desktop and mobile.
- A clear problem definition in the requested PDF, using the owner’s exact wording.

## Non-Goals

Scientific bounds, attribution, evidence classifications, and verification records keep
their existing meaning.
This is a presentation and navigation change.
The workbench’s packing controls and the papers’ mathematical content are outside this
repair wave.

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

Keep the homepage in this order:

1. A compact problem and project introduction, with the main destinations easy to find.
2. A visible atlas preview, one short introductory sentence, and a prominent **Explore
   the atlas** button.
3. A visible recent-results preview, one short introductory sentence, and a prominent
   **View all results** button.
4. Compact links or disclosures for papers, visualization, project documentation,
   related projects, and contribution information.

Use at most eight representative atlas tiles and six recent results as the initial
preview limits. These are proposed design defaults.
The result selection and ordering come from the existing register logic; each headline
links to its canonical result page.
Preview limits bound the initial content rather than just hiding the full atlas or table
in the homepage DOM. Both primary buttons remain visible without expanding anything.

Publish the complete interactive atlas at `atlas.html`, reusing its existing drawings,
view controls, and case-record behavior.
Keep the complete results table and filters at `all-results.html`. Retain the Frontier
survey and case index as distinct destinations.
The shared navigation exposes the Atlas page while retaining access to Frontier.

Register the new page in `packing/site-urls.yaml` and the builders’ page, asset, crawl,
preview, and Pages-scope declarations.
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
Popovers must fit the viewport, provide usable scrolling and a reachable close control,
and preserve focus and the link to the complete case page.
Balance the drawing with the title, bounds and summary so its current height limit does
not force the useful overview below an oversized figure.

Reproduce $n = 291$ through both the direct case page and the atlas or Frontier popover.
Check prepared math, its inherited font context, and long bound expressions before
choosing a fix. Keep exact expressions available; reflow or locally scroll long formulas
without clipping glyphs or creating page-wide horizontal overflow.

### PDF problem definition

Use this exact sentence in the requested PDF:

> The square packing problem asks for the side $s(n)$ of the smallest square that can
> hold $n$ unit squares, where the squares are free to rotate but cannot overlap.

The target PDF is pending owner clarification.
Identify its authoritative source, replace the current definition, and rebuild with its
existing renderer. Verify the sentence and its inline math in the rendered PDF. Keep the
paper’s claims and other mathematical content unchanged.

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
| Workbench shell | `packages/workbench/tools/workbench_tools/build_site.py` |
| Published addresses and deployment scope | `packing/site-urls.yaml`, `packing/devtools/pages_scope.py`, `.github/workflows/pages.yml` |

The new Atlas address is the only proposed public route addition.
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
| L3: Tighten the homepage and preserve both previews | `think-5c8r` | P1 | Brief introductions; at most eight atlas tiles and six results initially; both previews visibly present; prominent buttons to Atlas and Results; papers and resources still reachable. |
| L4: Publish the complete dedicated Atlas page | `think-a9au` | P1 | All 324 cases and existing view controls work at `atlas.html`; case links/popovers work; navigation and the URL registry include it; legacy atlas links and view state still reach the full atlas. |
| L5: Add shared Headroom navigation | `think-byu7` | P1 | Hide down, show immediately up on desktop and mobile; visible at top and during focus/menu use; all four shell families covered; no layout jump or obscured anchor target. |
| L6: Verify the combined website layouts and interactions | `think-xio5` | P2 | Browser checks cover previews and their buttons, the dedicated pages, $n = 291$ math, popover scrolling/focus, and header direction across representative shells, widths and themes. Retain reviewed before/after screenshots with the implementation evidence. |
| L7: Clarify the PDF problem definition | `think-9tcy` | P2 | Identify the requested PDF, update its source with the exact sentence above, rebuild it, and verify readable inline math and unclipped text. The target requires owner clarification before editing. |

Start with L1’s reproduction so its regression identifies a real failure.
L2 and L5 can be developed independently.
L3 and L4 integrate together so preview buttons always have a working destination.
L6 depends on the five implementation issues.
L7 has its own PDF rendering check and can proceed once its target is identified.
Give parallel writers disjoint files; keep shared templates, route registration, and
integration with one owner.

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
Homepage checks assert actual preview limits and both primary buttons; Atlas checks
assert complete case coverage and old-link forwarding.
Reuse `preview_site.py` for the visual review and the existing site-page measurement
tools for established rendering budgets.

Follow [development.md’s validation tiers](../../../../development.md#validation-tiers):
focused checks and `--edit` during implementation, the reachable `--push` surface before
pushing, PR frontend and fast checks, and the full checkpoint at final review.
Fast regressions belong in the existing CI surface.

## Rollout Plan

Build and review the local static site with desktop and mobile screenshots before
publishing the website changes.
Update the URL registry and generated route view with the Atlas addition, verify old
addresses, and use the existing Pages deployment workflow.
Close the epic when all implementation issues and the combined browser review pass.
Planning completion leaves the implementation issues open.

## Open Questions

- The precise $n = 291$ failure and smallest effective fix require reproduction.
- Choose the representative preview tiles and final compact copy during visual review;
  the visible previews, prominent destination buttons, and header direction are decided.
- Identify the PDF that should receive the supplied problem definition; its wording is
  decided.

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
