---
type: is
id: is-01m5jd4zpw87v2a5ne04b6ppn6
title: Use serif prose and subtle body spacing in News cards
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: domain-finterm-news-serif
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:14:39.067Z
updated_at: 2026-10-22T18:31:00.399Z
started_at: 2026-10-22T18:14:47.866Z
---
Apply the user-requested News card typography: factual and mathematical body prose uses existing serif tokens; titles, dates, controls, references and artifact metadata stay sans. Add a small amount of vertical spacing around body prose. Own only the News card CSS in packing/devtools/templates/site.css and the relevant design-system guidance. Reuse existing tokens; preserve source identities and other workers' changes. Run focused existing style/frontend checks. No commit or push; coordinator integrates.

## Notes

Implementation ready for coordinator integration; no commit or push. Coordinator extended ownership to render_news wrappers and affected existing tests.

News summaries/details use ordinary KPress prose/math roles (serif by default, retaining reader font preferences); titles/dates/topics/significance remain sans. Publication records have their own sans-text wrapper. Added 0.25rem body padding above/below, preserving existing paragraph rhythm and card behavior. Updated the News section of paper-design.md and existing browser probe/assertions. Shared CSS/design-doc popover edits by the other worker preserved.

Checks: final affected rendering suite tests/test_changelog.py tests/test_news_highlights.py tests/test_changelog_publication.py: 74 passed in 44.11s. Desktop/mobile News behavior/typography/spacing and whole-homepage math-face walk: 3 passed in 68.54s. Existing test_site_math_preferences.py: 9 passed in prior final-production-source run (the same run exposed 4 stale all-sans publication expectations, subsequently corrected and rerun green). Scoped Biome, Ruff check/format, tsc probes, and git diff --check passed. Mobile screenshot visually reviewed at scratch tmp/news-serif-think-46td/news-card-390.png.

Files: packing/devtools/render_changelog.py; packing/devtools/templates/site.css (News rules only); packing/devtools/templates/paper-design.md (News guidance only); packing/tests/probes/site_homepage/news.js; packing/tests/test_site_homepage.py; packing/tests/test_news_highlights.py (wrapper assertion); packing/tests/test_changelog_publication.py (wrapper and math-role assertions).
