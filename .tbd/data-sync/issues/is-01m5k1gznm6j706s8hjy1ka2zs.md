---
type: is
id: is-01m5k1gznm6j706s8hjy1ka2zs
title: Use a Topics dropdown and consistent significance segments on News
kind: feature
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:10:43.763Z
updated_at: 2026-10-23T00:43:27.584Z
started_at: 2026-10-23T00:10:49.927Z
closed_at: 2026-10-23T00:43:27.583Z
close_reason: Topics-only dropdown complete; retained desktop/mobile News contracts passed96.53s/67.26s, shared significance segments preserved, color/keyboard/history/bookmark/no-script/reduced-motion behavior verified, scoped checks clean.
resolution: null
duplicate_of: null
---
Implement only the News Topics/Tags filter as a colored dropdown multiselect, adapting the read-only Metabrowser chip-menu reference. Preserve news-topics/news-s URLs, history and hash restoration, S4/S5 default significance, and all-news access without scripts. Topics uses a compact All/one/+N summary, checked choices stay open, semantic topic colors, arrows/Home/End/Escape, outside dismissal and focus restoration. News significance remains inline segmented buttons, styled consistently with homepage Grid/Triangle; no significance dropdown. The later Results Archive significance-segments request is tracked separately by think-p39d. Reuse shared tokens, original menu chevron endpoints and reversed motion, light/dark styling and mobile fit. Parent owns builds/commit; plan updates coordinated with landings. Plan: docs/project/specs/active/plan-2026-10-22-site-navigation.md.

## Notes

Completed Topics-only dropdown while preserving inline News S3-S5 significance segments with S4/S5 defaults and all topics selected. Generic overview/filter-menu.js owns the compact All/None/one/+N summary, ordinary pressed-button focus, arrows/Home/End, Escape/outside/Tab dismissal, focus restoration and viewport fit. Checked choices stay open. news-filters.js keeps selection, news-topics/news-s URLs, unrelated query state, history and hash revelation authoritative. Topic fills and marks reuse shared design tokens; selected text/check ink retains measured contrast. Panel and chevron share navigation's original down/up endpoints, negative180-degree expansion, timing and explicit0ms reduced-motion override. No dependencies or new filter semantics for News. The later Archive S1-S5 request is separately completed under think-p39d. Script declaration/classification/input integration and current paper-design policies are complete; plan maintained by landings.

Focused receipts from packing with task environment: python -m pytest 'tests/test_site_homepage.py::test_news_facets_history_bookmarks_and_shared_meters[1280]' -q -x --tb=short:1passed96.53s; same[390]:1passed67.26s after final reduced-motion fix. Existing contract verifies Grid/Triangle-equivalent significance styling, light/dark topic colors/check contrast, keyboard/open-state/summary/viewport fit, URLs/history/bookmarks/tallies/counts/tooltips and no-JavaScript complete-news access. Compatibility/direct News semantic checks16passed19.24s. Scoped Ruff and Biome clean; overview and probes tsc passed; scoped Python source/test BasedPyright0errors0warnings. Earlier failures were fixed: label-changing/CSS-cased test expectations, selected topic hover contrast4.22:1, and KPress tiny reduced-motion duration on discrete menu closing. No sleeps or weakened visibility assertions added. Parent owns source commits, full current-head rebuild, live review and CI under think-kmpp.
