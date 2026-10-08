---
title: A Static, Crawlable Site with a Registered URL Scheme
description: Review of the published site's URL system, link structure, search-engine readiness and page-load behaviour, and the plan that makes every page complete static HTML at a registered, permanent address
author: Claude (agent), for the repository owner
---
# Feature: A Static, Crawlable Site with a Registered URL Scheme

**Date:** 2026-10-06

**Author:** Claude (agent), for the repository owner

**Status:** Implemented; validation and rollout are tracked in PR #395

**Workflow:** W7 pipeline improvement (the published site is the surface)

**Reviewed baseline:** `7569e5ae` (main after PR #390)

**Beads:** see [Implementation Plan](#implementation-plan); the epic and its children
are linked to this spec
(`tbd list --spec plan-2026-10-06-site-urls-seo-performance.md`).

## Implementation Checkpoint (2026-10-07)

PR #395 implements the plan following senior review A and independent senior,
performance, security and correctness passes.
All five implementation lanes are complete.
Canonical pages serve all 324 cases and 116 live results; two previously removed result
addresses serve explained, non-indexed tombstones.
The registry retains old paths and query/fragment aliases, and checks semantic result
identity against the historical baseline.

The upstream integration reused the provisional `T-116` token for a different result.
Its explicit pre-registry amendment preserves the former publication date and binding;
the current article directs prior n = 39 readers to `T-110`. This is an explained token
reuse, with both results still available, rather than an unchanged semantic permalink.
The generator rejects unamended identity collisions and failed history checks before
writing either generated file.
Six unpublished bootstrap dates were corrected to the earliest explicit registrations
reconstructed from main history: `T-080`–`T-082` to 2026-10-02, and `T-113`–`T-115` to
2026-10-06. The nine canonical HTML, Markdown and PDF editions of the three papers also
retain their first publication dates from trusted release history: the lower-bound
explainer on 2026-09-05, the optimality review on 2026-09-30, and the threshold review
on 2026-10-05. These dates remain separate from original-proof and revision dates.
Established registrations remain immutable; a proposed PR cannot serve as its own
historical authority.

Generic content and the three papers use prepared visual mathematics with retained
reader font choices.
Generic pages record the checked build-time KaTeX version; the glyph guard verifies that
version and each formula’s own single semantic MathML subtree without requiring a
browser typesetting program.
Primary content reads without JavaScript.
Shared immutable assets, local dimensioned drawings, static synopsis chapters and
separate workbench JSON keep the completed pages within documented path-specific budgets
and the strict 2 MB ceiling.

All five producers build, including three PDFs and the workbench.
The rebuilt site has 484 HTML files within their budgets.
Three-run browser measurements pass over twelve scenarios at both viewports and themes,
with a separate no-JavaScript check: maximum median CLS 0.075, LCP 1,404 ms, longest
task 228 ms and blocking time 178 ms.
These are local unthrottled measurements, not field Core Web Vitals.
Live case/result popover checks and the workbench’s positive and negative policy checks
also pass.

Local site checks and the assembled-site check pass.
The broader Mac run was interrupted under storage pressure; isolated checks reproduce
three unchanged scientific output comparisons, and two unchanged profiler tests require
Linux `/proc`. Validation uses the existing hosted 104-step checkpoint on Linux
alongside pull-request CI. Exact-head CI, independent review dispositions and their
final evidence are recorded in [PR #395](https://github.com/jlevy/squares/pull/395).
Deployment and the owner’s Search Console account setup follow merge.

Hosted verification exposed missing producer dependencies and browser tests that still
expected the earlier client-built pages.
The producer jobs now stage their shared card and own their crawler outputs.
Required Chromium checks exercise cached drawings, complete static case pages, filter
navigation and registered retired-result fragments.
Fetched case popovers declare the font context their prepared prose inherits.
Disposable mutation snapshots omit measured historical outputs while retaining
scientific inputs and linked evidence under the unchanged 192 MiB limit; the read-only
auditor refuses candidates that mandatory copy routes would restore.
The final hosted run and independent dispositions remain recorded on PR #395.

## Overview

The site at `https://jlevy.github.io/squares/` is starting to get traffic, and people
link to individual case records such as
[`cases/11.html`](https://jlevy.github.io/squares/cases/11.html).
Those case records have the worst problems on the site.
A reader with scripts, and Google’s renderer, never stays on `cases/11.html`: a script
in its head sends them to `cases/?n=11`, which fetches the same file again and redraws
it in the site’s design.
The page shifts while that happens, and Google sees a page that calls itself canonical
and then redirects to a URL whose canonical is `cases/`.

The review below covers the whole site: which URLs it publishes and how they are made,
how pages link to each other, what each page tells a search engine, how much each page
weighs, and what moves after first paint.
It found that the site is careful about some things already, such as forwarders for
moved pages, shared content-hashed assets for its own pages, and a deployed-site check.
But it has no sitemap, no 404 page and no registry of its addresses.
Five pages are larger than the 2 MB that Google reads, and several pages build their
main content in the browser.

This plan settles the design the owner asked for in conversation:

1. **Every page is complete static HTML.** What a reader sees, and what Google indexes,
   is in the bytes the server sends.
   JavaScript enhances a page that already reads correctly; it never redirects between
   content pages, never fetches primary content, and never moves laid-out content after
   first paint.
2. **Every entity has one permanent address**, listed in a generated URL registry that
   the build and the deployed-site check both enforce.
   An address in the registry stays served for as long as the site exists, either as a
   page or as a forwarder.
3. **`cases/N.html` is the canonical, search-friendly page for case N**, complete in the
   site’s design, with no redirect.
4. **Each page has a byte and layout-shift budget** that CI enforces.
   Nothing published approaches the 2 MB Google reads.

## Goals

- Every published HTML page renders its full content without JavaScript, in the site’s
  design, at its canonical URL.
- `cases/N.html` for every case is a complete page: navigation, one `h1`, `<main>`, the
  record, the drawing at reserved dimensions, server-rendered math, a specific title and
  description, breadcrumb structured data, and a self-referencing canonical.
- One generated, checked-in URL registry lists every published path with its kind,
  canonical form, generator and status.
  The build fails if it writes a file the registry does not list, if a listed live path
  is missing, or if a path that `main` once listed disappears without a forwarder or
  tombstone.
- The site publishes `sitemap.xml` (generated from the registry), `404.html`, favicon
  files at stable paths, and a Search Console verification token produced by the build.
- Every published HTML file is under a hard 2,000,000-byte limit, and each page family
  has a smaller budget.
- No page shifts after load.
  CI measures cumulative layout shift (CLS) on representative pages at desktop and
  mobile widths, and fails above the budget.
- Each page’s head carries a topical title, a specific description, and structured data
  where it fits: `ScholarlyArticle` and Google Scholar `citation_*` tags for the papers,
  `BreadcrumbList` for records, papers and documents, and one `Dataset` for the frontier
  register.
- The URL scheme, the static-page contract and the JavaScript policy are written in
  `development.md` and enforced by tests, so the next contributor follows them without
  reading this plan.

## Non-Goals

- Changing the site’s visual design.
  Pages keep the kpress design system; the work moves rendering from the browser to the
  build.
- Moving the site to a custom domain.
  That is an owner decision listed under [Open Questions](#open-questions); this plan
  keeps `SITE_URL` the only definition of the address, so a later move is a one-constant
  change plus a forwarding plan.
- The root user site at `https://jlevy.github.io/`. Its repository
  (`jlevy/jlevy.github.io`) does not exist publicly; creating it, and the `robots.txt`,
  favicon and site name it would carry, is an owner action listed under
  [Rollout Plan](#rollout-plan).
- Rewriting the workbench.
  It is an application; it keeps its scripts, but its data moves out of its HTML.
- Withdrawing the self-contained offline copy of a paper.
  It remains available as a build output (`site_assets.inline_assets`); the published
  page links shared assets.

## Background

### What Was Reviewed, and How

Three parallel audits ran on 2026-10-06 against `7569e5ae`. The live site was not
reachable from the review session (its egress policy blocks `jlevy.github.io`), so each
audit ran on a local build made with the same renderers `pages.yml` runs:
`render_overview --output site` (verified identical to HEAD with `--check`), the three
paper renderers with `--site`, and the workbench’s `build_site`. Facts about live server
behaviour (headers, the served 404, the root `robots.txt`) are marked as to be verified
on the live site after deployment.

### Published URL Families Today

All paths are relative to `SITE_URL` (`packing/devtools/render_overview.py:112`).

| Family | Count | Generator | Today |
| --- | ---: | --- | --- |
| `/` and the section pages (`all-results.html`, `frontier.html`, `papers.html`, `visualize.html`) | 5 | `render_overview.PAGES` | Static; overview 2.7 MB |
| Reader documents (`tutorial.html`, `readme.html`, `epistemics.html`, `synopsis.html`, `conventions.html`, `development.html`) | 6 | `site_documents` | Static; synopsis 1.6 MB |
| `cases/` | 1 | `render_case_pages.cases_page` | The record page: reads `?n=N`, fetches `N.html`, redraws it |
| `cases/{n}.html` | 324 | `render_case_pages.case_records` | Plain record with no site design; scripted readers are redirected to `cases/?n=N` |
| `result/t-{nnn}.html` | 111 | `render_overview.result_fragments` | Headless HTML fragments (no `<head>`, title or canonical); links written from the site root, so 7,879 of 7,880 links 404 when the file is read at its own URL |
| `papers/{slug}.html`, `.md`, `.pdf` | 3 × 3 | three paper jobs in `pages.yml` | Static; 2.1–3.3 MB each, about 1 MB of inline base64 fonts and 0.4–0.6 MB of inline KaTeX |
| `workbench/` | 1 | `workbench_tools.build_site` | Application; 5.0 MB, of which 3.3 MB is inline JSON |
| Forwarders (`MOVED_PAGES`) | 7 | `render_overview.forwarder_pages` | Correct: script plus `<noscript>` refresh plus canonical to the target |
| Moved-file copies (`MOVED_FILES`) | 4 | `publish` job | Byte copies of paper `.md`/`.pdf` at old paths |
| Root atlas files (`known-best-*`, posters), `social-card.png` | 10 | explainer job; `social_card` | `known-best-1-100.png` is linked nowhere |
| `assets/{css,fonts,js}/{name}.{hash}.{ext}` | 45 | `site_assets` | Content-hashed; used by the site’s own pages, not by the papers or the workbench |

Addresses with meaning beyond the path: `all-results.html#t-nnn`, `frontier.html#n-N`,
`cases/?n=N`, `cases/N.html?raw`, `?view=embed`, table filter queries, and the
overview’s old fragments, which `overview/forward.js` sends on (with a catch-all that
sends any unknown fragment to the lower-bounds explainer).

### Findings

**URL system.**

- **No registry.** `SITE_PAGES` (`render_overview.py:281`) says it is every page the
  site serves, but it omits 324 records, 111 result files, the forwarders, the paper
  files and every asset.
  The only table of paths, in
  [plan-2026-09-29-github-pages-overview.md](plan-2026-09-29-github-pages-overview.md#url-layout),
  is stale (no Part II paper, no assets, no queries).
- **Stability is a policy, not a check.** `development.md` says “an address the site has
  served keeps working”, and `MOVED_PAGES`/`MOVED_FILES` implement it for hand-moved
  pages. `check_published_site` checks only the current build’s own declarations and
  samples three case records.
  A result that is withdrawn, or a case file that is renamed, deletes its page with
  every check green (`write_site` prunes it, `render_overview.py:1319-1324`).
- **Register IDs have been renumbered on branches** (T-102..T-111 were provisional hours
  before merge). Nothing on `main` has been renumbered so far (all 93 first-parent
  commits since 2026-09-29 were checked), but only `conventions.md:88` stops it.
- **Case-sensitivity and padding.** IDs read `T-018`, URLs say `t-018`; cases are
  `n-011.md` in the record and `11.html` on the site.
  Neither alternative form is served.
- **Links that leave the site for what the site serves.** 3,615 links point at
  `packing/frontier/n-NNN.md` on GitHub where `cases/N.html` exists
  (`overview_data.py:428-431`; `cases/11.html` links its own GitHub file 32 times).
  `all-results.html` links `epistemics.md` on GitHub three times beside three links to
  `epistemics.html`.
- **`cases.html` forwards to `cases/index.html`**, while the canonical spelling is
  `cases/`.

**Search engines.**

- **Case records send conflicting signals.** See the Overview.
  The original reason for the redirect, avoiding 324 copies of 1.8 MB of inline assets,
  disappeared when the site moved to shared assets (`render_case_pages.py:21-27`).
- **Five pages exceed Google’s 2 MB HTML limit.** Since February 2026 Googlebot indexes
  only the first 2 MB of uncompressed HTML. The lower-bounds explainer (3.29 MB) puts
  its `h1` at byte 1,317,061, behind inline fonts, and loses about half its text,
  including the proof.
  The overview (2.73 MB) loses its popover summaries, “PDFs and Videos”, “Other
  Projects”, its only links to the reader documents, and every script.
  Parts II and III (2.30 and 2.08 MB) lose only their trailing scripts.
  The workbench (5.0 MB) loses its data.
- **No sitemap, `robots.txt` or `404.html`.** A `robots.txt` counts only at the host
  root, `https://jlevy.github.io/robots.txt`, which belongs to the (absent) user site.
  The sitemap must therefore be submitted in Search Console under a URL-prefix property
  for `https://jlevy.github.io/squares/`, verified by a token the build writes, because
  every deploy replaces the whole site.
- **111 result files are crawlable and headless**, with broken relative links.
- **No `h1`** on the overview (its title is an `h2`) or on the case records (whose
  headings start at `h3`). The overview’s title is “The Squares Project”, with no topic
  words. Case titles are “n = N · Case Records”.
  Paper titles run 68–89 characters.
  Case descriptions differ only in *n*.
- **No structured data anywhere.**
- **The favicon is a `data:` URI.** Google shows one favicon per host, read from the
  host’s home page, so it never appears in Search.
  It needs a file at a stable path, declared on the root user site.
- **Math ships as TeX source** typeset in the browser on the site’s own pages, so
  snippets and headings can index as `\(s(11)\)`. The explainer already pre-renders its
  math.
- **Forwarders are built right**: script, `<noscript>` refresh and canonical agree.

**Page weight.** Measured on the local build; gzip figures are what Pages transfers.

| Page | HTML bytes | gzip | What fills it |
| --- | ---: | ---: | --- |
| `workbench/index.html` | 4,996,863 | — | 3.34 MB inline JSON data, 1.08 MB CSS, 0.92 MB fonts |
| `papers/n11-lower-bounds-explainer.html` | 3,285,532 | ≈1.07 MB | 1.30 MB CSS with 37 base64 fonts, 0.58 MB KaTeX and other scripts |
| `index.html` | 2,727,614 | 281 KB | 1.24 MB of atlas SVG in `<template>`s; 111 rows and popover summaries repeated from `all-results.html` |
| `papers/n11-threshold-bound-review.html` | 2,296,070 | ≈1.0 MB | same inline fonts and KaTeX |
| `papers/n11-optimality-review.html` | 2,078,063 | ≈1.0 MB | same |
| `frontier.html` | 1,678,531 |  | 0.98 MB of inline SVG |
| `synopsis.html` | 1,624,199 |  | 127 KB of model JSON; 552 K characters of text |
| `all-results.html` | 1,379,239 |  | 234 KB of MathML; 380 K characters |
| `result/t-007.html` (largest of 111) | 520 K |  | about 1,600 links each |

The test that bounds the overview’s size (`PAGE_CEILINGS`,
`packing/tests/test_overview.py:5480`) is a ratchet: it has been raised with each batch
of results and stands at 2,800,000. The overview has 25.9 K DOM elements, the explainer
24.7 K, the synopsis 29.5 K.

**Layout stability and load time.** See
[Layout Stability and Script Inventory](#layout-stability-and-script-inventory).

### Hosting Constraints That Bound the Design

GitHub Pages serves static files with no custom headers and no server redirects, and
caches everything for 600 seconds (`Cache-Control: max-age=600`; content-hashed assets
cannot be marked immutable).
Every deploy replaces the whole artifact.
A project site’s `404.html` is served for missing paths under `/squares/`, at the
requested URL, so its links must be root-absolute.
Pages answers `/squares/frontier` with `frontier.html`; canonicals resolve that
duplicate. The site limit is 1 GB and the soft bandwidth limit 100 GB a month; with
papers at about 1 MB gzipped each, that ceiling is within reach of a popular week, which
is one more reason to move their fonts into cached shared files.

## Design

### Principle 1: Every Page Is Complete Static HTML

A page is complete when, with JavaScript disabled, it shows all of its content in the
site’s design at its final layout.
The build renders everything a reader reads: text, tables, drawings, math (as KaTeX HTML
plus MathML, as the explainer does), navigation and footers.

JavaScript on content pages is limited to three classes, and each script declares its
class in its header comment:

| Class | Allowed | Examples |
| --- | --- | --- |
| **Head bootstrap** | Synchronous, tiny, runs before first paint, sets root attributes only | Theme and font-preference attributes on `<html>` |
| **Input response** | Runs only in response to a reader’s input; may open overlays, sort or filter in place, switch tabs | Table sort and filter, popovers, theme toggle, atlas size switch |
| **Non-layout enhancement** | Runs after load; may not change the geometry of anything laid out | Copy buttons, scroll-spy highlighting in the TOC rail |

Forbidden on content pages: redirects (except on registered forwarders), fetching
content that the page needs to be complete, inserting or replacing laid-out content
after first paint, and typesetting math on the client when the build can typeset it.
Overlays opened on input may fetch the target page and show an extract of it, because
the link they decorate leads to that complete page.

The workbench is an application and is exempt from the content-page rules, but not from
the byte budget: its data becomes separate cacheable files.

### Principle 2: One Permanent Address per Entity, in a Registry

**The canonical forms.** These do not change; the registry lists them and the build
enforces them.

| Entity | Canonical URL | Notes |
| --- | --- | --- |
| Home | `/squares/` | never `index.html` in links |
| Section page | `/squares/{name}.html` | `all-results`, `frontier`, `papers`, `visualize` |
| Reader document | `/squares/{name}.html` | lowercase stem of the root document |
| Case | `/squares/cases/{n}.html` | decimal, no zero padding; the case page itself |
| Case index | `/squares/cases/` | a static list of every case, linking each `N.html` |
| Result | `/squares/result/t-{nnn}.html` | lowercase, three digits; a complete page |
| Paper | `/squares/papers/{slug}.html`, `.md`, `.pdf` | slug `n{N}-{subject}-{kind}` |
| Workbench | `/squares/workbench/` |  |
| Row anchor | `all-results.html#t-{nnn}`, `frontier.html#n-{N}` | stable fragment ids |

**Alternative and legacy forms**, each forwarded rather than duplicated:

- `cases/?n=N` (the current record page) forwards to `cases/N.html`, keeping the
  fragment. It is the only query-addressed form, and it is retired.
- `cases.html#n-N` already forwards; it now goes straight to `cases/N.html`.
- The seven `MOVED_PAGES` forwarders and four `MOVED_FILES` copies stay.
- `404.html` resolves common mis-spellings before showing “not found”: an uppercase
  result ID (`result/T-018.html`), a zero-padded or prefixed case (`cases/011.html`,
  `cases/n-11.html`), and a result page that does not exist to its row anchor.
  It is the only page where client-side redirection is allowed for unregistered paths,
  because Pages gives no other mechanism.
- The overview’s fragment forwarder keeps its explicit list, but its catch-all no longer
  sends every unknown fragment to the explainer; it sends only a frozen list of the
  explainer-era ids, emitted from the explainer’s build.
  Two explainer anchors that docs once cited and that no longer exist (`#proof`,
  `#beyond-point-atoms-the-current-bound`) get kept anchors in the explainer.
- Registered forwarders keep their script redirect beside the `<noscript>` refresh,
  because only the script carries query and fragment state across; they are the one
  exception to the no-redirect rule, and the registry names each one.
  HTTP scripts use the canonical directory URL; file navigation and no-script refreshes
  use its physical `index.html`, so offline readers reach the page rather than a
  directory listing.

**The registry.** A new module, `packing/devtools/site_urls.py`, derives every published
path from the builders’ own declarations (`render_overview.PAGES`, `PAPERS`,
`MOVED_PAGES`, `MOVED_FILES`, `COMPOSITE_ASSETS`, `SOCIAL_CARD`, the case set, the
register, the workbench) and writes `packing/site-urls.yaml`, checked in and
drift-checked like the other generated registers.
Each row records the path, its kind (`page`, `record`, `result`, `paper-file`,
`forwarder`, `copy`, `asset-file`, `site-file`), its canonical URL, the generator
(`module:function`), the date it was first published, and its status (`live`,
`forwarded` with a target, or `withdrawn` with a tombstone).
Hashed assets are one pattern row, not 45 rows.
Two families are permanent by rule: `cases/{n}.html` for every *n* the register has
covered (the range only grows), and `result/t-{nnn}.html` for every ID that has ever
been on `main`. Each result’s stable identity includes its kind, scope, establishment
date, attribution, source lineage, evidence IDs and artifact paths.
Historical checks compare these semantic fields; dates alone do not identify a result.
A correction records the previous binding in a dated, explained amendment.
Same-date ID swaps fail; ordinary wording and review-rating corrections remain possible.
A rendered Markdown page, `docs/project/site-urls.md`, shows the same table for readers
and is linked from `development.md`.

Three checks hold the registry to the site:

1. **Required PR history and drift:** the registry must derive from current builder
   declarations and preserve every historical public path and result identity against
   `origin/main`. This runs in fast, records and edit validation; a push check alone is
   not the enforcement surface.
2. **Closed world:** every selected producer checks all of its declared files, metadata,
   asset namespaces and budgets.
   Partial builds name their producers explicitly and reject omitted outputs or empty
   namespaces. Final assembly and `preview_site` require every registration.
   Missing or unexpected files fail; removed records retain an explained tombstone and,
   where known, a registered replacement.
3. **Deployed** (`check_published_site`): every non-asset row is fetched, all cases and
   results included, and registered forwarders and byte copies are checked.

`sitemap.xml` is written from the registry: every `live` row of kind `page`, `record`,
`result` and paper HTML, with `<lastmod>` taken from record dates (a paper’s revision
date, a result’s registration or amendment date, a case’s last result), never from the
clock or Git, so the double render stays byte-identical (OR-18).

### Principle 3: `cases/N.html` Is the Case Page

`render_case_pages.case_records` renders each record as a full site page: the shared
stylesheets and navigation, a breadcrumb (Home › Cases › n = 11), one `h1` naming the
problem for that *n* (“11 Unit Squares in a Square”), `<main>` holding the record, the
drawing with explicit `width`, `height` and `viewBox`, server-rendered math, and links
to the neighbouring cases.
`case-forward.js` is deleted.
`cases/` becomes a static index of all cases, rendered at build time, with a small head
script that forwards legacy `?n=N` and `#n-N` aliases to `N.html`. Both `cases/#n-N` and
`cases/index.html#n-N` remain supported, as does `cases.html#n-N`. A valid numeric query
takes precedence over the case fragment; other query state, meaningful record fragments
and embedding state survive.
Invalid counts leave the static index readable.
`case-page.js` performs only this registered alias forwarding; it does not render
records. Popovers that preview a case keep fetching `N.html` and extracting its
`article`.

Titles and descriptions are written from the record:

- Title: `11 Unit Squares in a Square: Bounds and Best Packing (n = 11)`, under 60
  characters where *n* allows.
- Description: the bracket on *s(n)*, who holds each bound, and whether the case is
  solved.
- Structured data: `BreadcrumbList`.

Every “n = N” link on the site points at `cases/N.html`; the record keeps one “On
GitHub” link to its source file.

### Result Pages

`result/t-nnn.html` becomes a complete page: head, navigation, an `h1` naming the claim
(`T-060: s(11) = …, the optimality of the Trump packing`), `<main>`, and links written
relative to `result/`. The popovers on the overview and the results table fetch the page
and extract its `article`, rebasing links as `case-popover.js` already does.
The overview no longer carries the 111 popover summaries inline.

### Head and Structured Data

`render_overview.head_tags` stays the single writer of head metadata and gains optional
structured data and robots directives through `PageMeta`.

- Overview title: “The Squares Project: Packing Unit Squares in a Square”; its title
  heading becomes the page’s `h1`.
- Papers: drop the site suffix from `<title>` for articles, keeping titles near 60
  characters; add `ScholarlyArticle` JSON-LD (headline, authors, dates, `isPartOf` the n
  = 11 series, the PDF) and the Google Scholar tags (`citation_title`,
  `citation_author`, `citation_publication_date`, `citation_pdf_url`,
  `citation_abstract_html_url`). Parts II and III gain `article:published_time`.
- `BreadcrumbList` on case, result, paper and document pages.
- One `Dataset` on `frontier.html` for the frontier register, licensed CC BY 4.0, with
  its distribution on GitHub.
- No `WebSite` block under `/squares/`; Google reads that only from the host’s home
  page.
- `<meta name="robots" content="max-image-preview:large">` on every page.
- Reader-document descriptions lengthened to state what each document is for.
- `google-site-verification` on `index.html` only, from a constant the owner sets.
- Favicon files (`favicon.svg`, `favicon-48.png`, `apple-touch-icon.png`) published at
  stable unhashed paths and linked from every page; the inline `data:` icon goes.
- `SITE_URL` stays the one definition of the address; the copy in
  `render_n11_lower_bounds_explainer_pdf.py:178` imports it.

### Page Weight and Budgets

- **Papers link the shared assets.** The three paper renderers link the
  `site_assets.shared()` bundle (fonts, kpress CSS, KaTeX) as the site’s own pages do
  (`render_overview.page_assets`), instead of inlining it.
  Expected: about 1.3 MB less per paper, the `h1` near the top of the file, about
  0.1–0.2 MB gzipped per paper after the first, cached across pages.
  The self-contained copy remains a build output for offline use.
- **The overview carries only what it shows.** Recent results render server-side (the
  rows `RECENT_DEFAULTS` selects), with “See all results” linking `all-results.html`.
  Broad filters live on that complete table; the overview explains its recent subset and
  passes supported query state to the full-table link.
  The atlas tiles leave the HTML: each tile is an SVG file under `atlas/` referenced by
  `<img width height>`, which keeps them in Google Images and in the browser cache; a
  tile that must follow the site’s theme ink uses a shared SVG sprite with `<use>`
  instead.
- **Frontier and synopsis**: drawings use standalone SVG files.
  The synopsis becomes a static chapter index and complete static chapter pages, with
  every old heading ID retained on the index beside an ordinary chapter link.
  Primary content no longer needs browser page-model JSON. A legacy fragment reaches its
  heading and chapter link; reading the chapter takes one additional navigation.
- **Workbench**: its 3.3 MB of data becomes separate hashed JSON files.
- **Budgets**, enforced by `check_published_site --local` on the assembled site:

| Family | Hard limit | Budget |
| --- | ---: | ---: |
| Any published HTML | 2,000,000 | — |
| Overview, section pages, documents |  | 600 KB |
| Papers |  | 800 KB |
| Case and result pages |  | 300 KB |
| Workbench HTML (excluding its data files) |  | 600 KB |

The `PAGE_CEILINGS` ratchet in `test_overview.py` is replaced by these budgets.
A page over budget fails the build; raising a budget is a reviewed edit to one table in
`site_urls.py`, with a reason.

### Layout Stability and Script Inventory

The retained measurement protocol and executable script inventory are described in
[development.md → Browser Load and Readability Protocol](../../../../development.md#browser-load-and-readability-protocol).
The build observes navigation before first paint, tests desktop/mobile and light/dark,
and checks complete visible primary content in a separate no-JavaScript context.
CI enforces CLS, LCP and task limits; it rejects unknown startup programs and includes
negative fixtures for early shifts, hidden headings/prose/math, missing assets and
undeclared scripts. Direct atlas query URLs are measured as navigation scenarios.

Prepared visual math uses the pinned renderer’s actual metrics for each reader font
choice. Existing semantics remain in the HTML, once per formula.
The lower paper’s four prepared choices are retained; generic pages share their visual
structure and select metric differences before paint.
Images reserve their intrinsic proportions; mobile atlas wrapping is determined in CSS
before its interaction program runs.

Each family retains its byte budget, and every HTML page retains the 2,000,000-byte hard
ceiling. The generated [budget exceptions](../../site-urls.md#html-byte-budgets) name
individual complete records or papers and their measured reason.
Exceptions do not admit a new family-wide limit.

### Where Things Are Documented

- `development.md` gets one section, **The Published Site**, that states the three
  principles, links the generated URL table and the budgets, and says how to add a page,
  a page family or a forwarder.
  The existing paragraphs about forwarders move into it.
- `packing/devtools/templates/paper-design.md` (shared assets) is updated for the
  papers’ move to linked assets.
- The stale URL Layout table in `plan-2026-09-29-github-pages-overview.md` is replaced
  by a link to the generated table.

## Implementation Plan

One branch and one pull request, built by parallel lanes in separate worktrees with
disjoint write sets, merged by the coordinator.
Each bead below names its lane.

### Phase 1: Contract, Static Pages, Metadata and Budgets

**Lane A — URL registry and crawl files** (`site_urls.py`, `site-urls.yaml`,
`check_published_site.py`, `write_site` hooks, `development.md`):

- [x] A1: `site_urls.py` registry derived from builder declarations, `site-urls.yaml`
  and `docs/project/site-urls.md` written with `--check` drift detection
- [x] A2: closed-world and append-only checks against `origin/main`; tombstone rendering
  for withdrawn rows
- [x] A3: `sitemap.xml` from the registry with record-derived `lastmod`
- [x] A4: `404.html` with root-absolute assets and the alias table
- [x] A5: per-page byte budgets and the 2,000,000-byte hard limit in
  `check_published_site --local`; retire `PAGE_CEILINGS`
- [x] A6: `check_published_site` (deployed mode) fetches registry rows instead of hand
  lists and samples
- [x] A7: `development.md` “The Published Site” section; replace the stale URL Layout
  table

**Lane B — Static case and result pages** (`render_case_pages.py`, `case-record.html`,
`cases-article.md`, `overview/case-*.js`, `overview/row-popover.js`, result rendering in
`render_overview.py`/`overview_sections.py`, `overview_data.py`):

- [x] B1: `cases/N.html` rendered as a complete site page (nav, breadcrumb, `h1`,
  `<main>`, reserved drawing size, server-rendered math, neighbour links); delete
  `case-forward.js`
- [x] B2: `cases/` as a static index; legacy `?n=N` and `cases.html#n-N` forward to
  `N.html`; retire record rendering in `case-page.js`
- [x] B3: case titles and descriptions from the record; `BreadcrumbList`
- [x] B4: `result/t-nnn.html` as complete pages with rebased links; popovers extract
  from them; overview drops inline popover summaries
- [x] B5: every “n = N” link points at `cases/N.html`; `epistemics.html` instead of the
  GitHub copy on `all-results.html`; `cases.html` forwards to `cases/`

**Lane C — Head metadata and structured data** (`head_tags`, `PageMeta`, `page_title`,
`site_documents.py` descriptions, paper front matter, favicon files):

- [x] C1: `h1` and topical title on the overview
- [x] C2: `ScholarlyArticle` JSON-LD and `citation_*` tags for the papers; article
  titles without the site suffix; published dates for Parts II and III
- [x] C3: `BreadcrumbList` for papers and documents; `Dataset` on `frontier.html`;
  `max-image-preview:large`
- [x] C4: favicon files at stable paths; verification-token constant
- [x] C5: lengthen reader-document descriptions; `SITE_URL` single definition

**Lane D — Page weight** (paper renderers and shells, `site_assets.py`,
`overview_sections.py` atlas and recent rows, frontier and synopsis drawings, workbench
data):

- [x] D1: papers link the shared asset bundle; offline copy remains a build output;
  print and PDF checks follow
- [x] D2: overview renders only the recent rows and links the full table
- [x] D3: atlas tiles, frontier drawings and the synopsis model JSON move to files
- [x] D4: workbench data in separate hashed files

**Lane E — Layout stability** (scope set by the performance audit):

- [x] E1: CLS, LCP and long-task guard in CI over representative pages at 1280 and 390
  widths, with probes in files per the browser-code rule
- [x] E2: fix each measured shift source (server-render math, reserve drawing and media
  sizes, font metric overrides, theme before paint)
- [x] E3: script inventory: every content-page script declares its class; delete or
  replace the forbidden ones

Lanes A–E run in parallel.
Lane B’s pages and Lane D’s weight changes both feed Lane A’s budgets, so A5’s budget
values are set last, from the merged build.

## Testing Strategy

- Unit tests for the registry (derivation, drift, append-only against a fixture of an
  older registry), the sitemap (byte-identical across two renders, only canonical pages,
  `lastmod` from records), the 404 alias table, and the head writer (structured data
  validates as JSON; every page has exactly one `h1`).
- The existing `render_overview --check` double render covers the new files.
- `check_published_site --local` on the assembled tree in the `publish` job enforces the
  closed world, the budgets and the head contract on every page, including all 324 case
  pages, 116 live result pages and two withdrawn-result tombstones (no sampling).
- A no-JavaScript render test: Chromium with JavaScript disabled loads each page family
  and asserts that the main content, `h1` and drawings are present and laid out.
- The layout-stability guard (E1) runs on every pull request that touches a page.
- `packing-validate --push` before every push; `packing-validate --fast` is what the
  pull request runs.

## Rollout Plan

1. Merge the pull request; the Pages workflow deploys and `verify-deployment` runs the
   registry-driven checks against the live site.
2. Owner actions, outside this repository:
   - Create a Search Console URL-prefix property for `https://jlevy.github.io/squares/`,
     put its verification token in the constant C4 adds, and submit `sitemap.xml` after
     the next deploy.
   - Decide the root user site: either create `jlevy/jlevy.github.io` with a
     `robots.txt` (`Allow: /`, `Sitemap: https://jlevy.github.io/squares/sitemap.xml`),
     a home page that links the project, the favicon and the site name, or leave the
     host root empty and rely on Search Console alone.
   - Run URL Inspection on `cases/11.html`, the three papers and `/squares/`, and watch
     the Pages report for “Page with redirect” and “Duplicate, Google chose different
     canonical” over the following weeks.
3. Live checks to record in the pull request after deploy: `http://` to `https://`
   redirect, the served `404.html` for a missing path, `Cache-Control` and gzip on a
   paper, the extensionless `/squares/frontier` behaviour, and the root `robots.txt`.

## Open Questions

- **Custom domain.** Stay at `jlevy.github.io/squares/` permanently, or move to a
  project domain before backlinks accumulate?
  A domain gives the project its own favicon, site name, `robots.txt`, a Domain property
  in Search Console and a CDN; the cost is a migration that relies on GitHub’s automatic
  301s. Two couplings to know: setting a custom domain on the `jlevy.github.io` user
  site moves `/squares/` with it, and renaming this repository changes the Pages path.
  This plan keeps either choice a one-constant change.
- **The root user site.** Does the owner want one (see Rollout Plan)?
- **Atlas tiles as `<img>` or sprite.** `<img>` tiles are indexable and cached but draw
  in fixed colours; a sprite keeps theme ink.
  The plan uses `<img>` unless the owner prefers the theme ink.

## References

- Audit reports (session scratchpad, summarized above): URL system and link graph; SEO
  and crawlability; performance and layout stability
- [plan-2026-09-29-github-pages-overview.md](plan-2026-09-29-github-pages-overview.md) —
  the overview, navigation and forwarders this plan builds on
- [development.md](../../../../development.md) — the published-site paragraphs this plan
  consolidates
- Bead `think-jl8e` — the missing link preview on X, traced to page size
- Google:
  [Googlebot file limits](https://developers.google.com/search/docs/crawling-indexing/googlebot),
  [redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects),
  [JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics),
  [favicons](https://developers.google.com/search/docs/appearance/favicon-in-search),
  [site names](https://developers.google.com/search/docs/appearance/site-names),
  [robots.txt](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt),
  [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google Scholar inclusion guidelines](https://scholar.google.com/intl/en/scholar/inclusion.html)
- GitHub Pages:
  [limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits),
  [custom 404](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site),
  [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
