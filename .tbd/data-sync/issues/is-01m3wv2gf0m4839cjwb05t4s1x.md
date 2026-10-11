---
type: is
id: is-01m3wv2gf0m4839cjwb05t4s1x
title: "Atlas expander: 'Show More' and 'Show Less' with double-chevron icons"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T22:58:58.651Z
updated_at: 2026-10-02T00:02:33.248Z
closed_at: 2026-10-02T00:02:33.246Z
close_reason: "Merged in jlevy/squares#286 (commit 7a9b6f0bf): the expander reads Show More / Show Less with double chevrons."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: change 'Show all 324' to 'Show More' and the other direction to 'Show Less', with an appropriate down arrow for Show More and an up arrow for Show Less: a properly styled icon such as a double-v and double-caret chevron, in the iconographic style of the current design. The icons come from the site's one icon set (the arrow icons the cards use; test_every_arrow_icon_comes_from_the_one_set), drawn as inline SVG in currentColor at the label's size, not text characters. The button keeps an accessible name that says what it does (aria-expanded; the count stays available to assistive text). Same control wherever the site has a show-all expander. With the atlas triangle work (think-kbo4).
