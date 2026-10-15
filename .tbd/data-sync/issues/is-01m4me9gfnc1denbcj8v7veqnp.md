---
type: is
id: is-01m4me9gfnc1denbcj8v7veqnp
title: "PDF atlas: make case numbers neutral and keep red only on the specific new values"
kind: task
status: closed
priority: 2
version: 10
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels:
  - pr-619
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
child_order_hints:
  - is-01m4zn9wfkeaagyv78fm101dyr
  - is-01m4zpbcfswycrk3vynth3h85k
  - is-01m4zr45pxh7wjwcrkf88txx2k
  - is-01m4zr9zhts3t2bmmnh2eaqwnn
hold: null
hold_until: null
created_at: 2026-10-11T02:57:22.931Z
updated_at: 2026-10-15T13:17:34.404Z
started_at: 2026-10-15T11:21:23.860Z
closed_at: 2026-10-15T13:17:34.404Z
close_reason: Delivered in PR619, merged 31eaf6333c5d5b6b3d111241768cdd3d30982588. All 43 executed PR checks and selected Deep38735581202 passed. Main Pages38739226771 published site v0.7.7, shared infographics v0.6.1 and lower-bounds paper v0.4.7; actual deployment audit job116439283652 passed 4460/4460 checks. Main full Packing remains independently in progress; no three-minute performance claim. Focused CI safety and performance work continues under think-3d1m and think-kxmq.
resolution: null
duplicate_of: null
---
Owner request 2026-10-10: get rid of the red colouring on numbers in the PDF, as was done for the web Atlas in PR #462, and rely on red only for specific values.

Current state (origin/main 6038af33c):
- The atlas posters (square-packings-100-20261008.pdf, square-packings-324-20261008.pdf) are built as SVG by packing/devtools/build_known_best_atlas.py and converted by cairo in render_composite_pdf.py. known-best-1-100.svg is also embedded in the n = 11 lower-bounds explainer (templates/n11-lower-bounds-explainer-article.md:168), so the explainer PDF carries the same red.
- The red is FIRST_PARTY_ACCENT_COLOR = "#a3123f" (packing/src/sqpack/render/style.py:46). Its comment still says "a lower bound this project proved", but it now marks any contribution dated on or after RECENT_SINCE = 2026-08-22 (build_bound_citations.py:163; flags from result_status.py RecentContributions).
- build_known_best_atlas.py:2011-2013 paints the whole case number n red when any contribution is recent (recent.any), else LABEL_MUTED_COLOR #47525f. This is the change: the case number should always be the neutral label colour.
- Keep, as the "specific values": the upper-bound value when recent.upper (:2061), the lower-bound value when recent (:2131), and the O badge when recent.optimal (:2033, :2236-2240). Only the number is accented, not the s(n) prefix (_append_function_text :2168-2201). FIGURE-PLAYBOOK.md:465-467 records that per-value rule.
- Update the words that describe the old rule: the legend at :2531-2539 ("recent result") and the alt text at :843 and :852 ("Case counts are crimson for recent results"). Fix the stale constant comment in style.py and the FIGURE-PLAYBOOK.md:129 counts (81 of 100, 297 of 324 cases).

Done when: no case number in either poster or the explainer figure is red; recent bound values and O badges still are; legend, alt text and FIGURE-PLAYBOOK describe that rule; the posters, the 1-100 composite (SVG, PNG, PDF, @2x) and the explainer PDF are regenerated and their receipt and drift checks pass; tests in test_known_best_atlas.py (:1429, :2088, :2363, :3183) are updated to pin the new rule, including a negative assertion on the case-number fill.

Related, not in scope unless the owner widens it: the web uses a different red for recency (--site-new-result, site.css:91) and always paints lower-bound values red whether recent or not (--site-bound-lower, site.css:2573, :2608, :2735, site-result.css:234). think-rt8s owns writing the one red rule down in epistemics.md; this change should agree with whatever it records. think-ju2n (closed) deliberately kept the PDF labels unchanged until this explicit request.

## Notes

Latest owner rule supersedes the initial historical O-badge-red acceptance wording: case numbers and badges remain neutral, and recency crimson appears only on specific numeric bound values. Source rules were already delivered; closure head4ddf4935 repairs stale descriptions and regenerates the complete retained poster family against existing admitted6133 data. Independent XML audit confirms424/424 case numbers #47525f and381/381 red elements numeric tspans (100:6upper55lower;324:73upper247lower), no red badge/nonnumeric content. Maintained infographic v0.6.1 cut2SVG4PNG2PDF/96owningpasses; embedded lowerbounds paper v0.4.7 actually regenerated,869250bytes,2/2page loads agree. Real redraw includes previously unexported current data/bounds/credits, recorded under childdx2k rather than claiming description-only. Final canonical push4dd has one RUF001 literal punctuation failure, planned runtime-preserving Unicode escape; other checks still running. Final hosted checkpoint/publication pending.
