---
type: is
id: is-01m4xka82212wb80mrdrrbnnfa
title: Let homepage and Atlas atlas viewport use the full screen width
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-14T16:18:19.821Z
updated_at: 2026-10-14T21:16:29.285Z
started_at: 2026-10-14T16:20:30.059Z
closed_at: 2026-10-14T21:16:29.278Z
close_reason: Delivered in PR604 merge16ea3bd0606c4fae2c343bf11de969301ca0f724. Final-head Packing38634417915/Pages38634417893 passed; deployment38636016372 live audit job116103959611 passed4243of4243checks at that exact revision. Independent reviewsA-H and dispositions are published. Final News has26articles, shared canonicaltopics/compactchoosers, defaultS4/S5, consistentcards/meters, T154/T153/T060highlights; Explanations hasTutorial/Papers/PDFs/Visuals and Film|Workbench; tutorial definitions/anchors preserved, Atlas uncapped withpan. Separate CI and literalcodeglyph follow-ups remain inPR599, without blocking this delivered slice.
resolution: null
duplicate_of: null
---
User reports main Atlas viewport on homepage and atlas.html capped narrower than wide screens. Remove the artificial width cap for this viewport; preserve a small edge gutter, existing horizontal scrolling, all atlas views/sizes and Regularized/Original switching. Implement in a separate reviewable delivery from PR599 CI repair, apply site version/changelog policy and verify wide and narrow viewport behavior.

## Notes

Combined News + Atlas implementation is ready in codex/atlas-full-width at /Users/levy/.codex/worktrees/site-changelog-plan/squares, based on main 37e6757ed4c51a1d93f2f999814c2a5efbe2a223. Source writes stopped; coordinator owns commits, PR, independent review, hosted gates and merge. This agent performed no code commit, push or GitHub mutation.

News is the second navigation destination; news.html has the shared caps/sans H1, sans operational content and per-day hairline native details cards. Three-line previews expand inline on hover/focus; pointer/touch presses and body interaction pin them; native keyboard/touch/no-JS disclosure toggling and ordinary body links remain usable. Homepage selects exactly two individual entries in retained date/ID order and follows them with the shared All news arrow action. About has only a short News link and hidden legacy bookmark forwarding, without the feed. Builder, served pages, CHANGELOG aliases, crawl registry and publication audit own the new News destination. All 22 frozen entries/5 days remain intact; preserve incoming main additions.

Atlas uses available page width minus existing gutter instead of its 140rem/2240px cap. Existing scrolling and drawing/layout/size/scale controls remain. Retained responsive geometry probe/regression covers both pages, 390/1920/3200, scripts/no scripts, Grid/Triangle, phone panning and restored-cap control; obsolete screenshot width override removed.

The feature supersedes unpublished site v0.6.2 with v0.7.0 minor. Infographics remain v0.6.0; papers remain explainer v0.4.6, threshold v0.1.0, optimality v0.1.7 and methods v0.2.2. Exact comparison proves the five required claim documents change only source-link revision 93822bfe to 37e6757e. Exact paper dispositions attribute navigation/chrome changes to site, without asserting unchanged paper HTML. Navigation is hidden by site-nav.css in print. October 14 first-publication metadata is planned and requires deployment confirmation; no launch evidence was invented.

Checks passed: scoped Ruff lint/format; explicit-interpreter BasedPyright 0 errors/0 warnings/0 notes; strict changed-JS tsc; Biome; Flowmark; diff whitespace; release-impact errors=[]; URL registry 978 rows/0 failures; frozen/GitHub changelog and claim freshness. In-memory home/News/About render checks, with math preparation disabled, passed final section order, 22 entries/5 days, two-entry preview, non-navigating summaries, launch links and compact About.

Late read-only math check caught duplicate KPress presentation/semantic text. Final two-file fix uses public NewsPreviewText with hidden-subtree stack, annotation/annotation-xml suppression and correct void/self-closing handling. Retained direct regression now passes exact semantic formula once plus nested suppression; final two-file Ruff lint/format and BasedPyright report zero findings. Unsafe raw-script/javascript-link refusal remains.

No local pytest/browser/site/PDF build because external scratch is full. Hosted interaction/geometry regressions use existing fixtures: News behavior only 1280/390, touch/no-JS only390; Atlas responsive cases remain. No CI architecture/timing gate changes. Actual merged PR/date/deployment evidence are still needed for closeout entry news-and-wide-atlas, release site v0.7.0.
