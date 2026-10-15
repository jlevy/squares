---
type: is
id: is-01m4me9gfnc1denbcj8v7veqnp
title: "PDF atlas: make case numbers neutral and keep red only on the specific new values"
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
child_order_hints:
  - is-01m4zn9wfkeaagyv78fm101dyr
  - is-01m4zpbcfswycrk3vynth3h85k
hold: null
hold_until: null
created_at: 2026-10-11T02:57:22.931Z
updated_at: 2026-10-15T11:49:51.726Z
started_at: 2026-10-15T11:21:23.860Z
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

Closure audit at main f97 confirms implemented case labels always use LABEL_MUTED_COLOR, and existing tests assert gray labels with independent numeric-only upper/lower accents and neutral O badges. The remaining defect is stale accessibility prose and figure guidance saying labels/badges turn crimson. Correcting SUMMARY_PROSE, style comment, figure-playbook and atlas README in codex/tutorial-closure; root owns these paths, separate from agent tutorial/News closure edits. Keep open until source review, appropriate component release/export regeneration and matching receipt/deployment verification; no unverified claim that regenerated artifacts have passed.
