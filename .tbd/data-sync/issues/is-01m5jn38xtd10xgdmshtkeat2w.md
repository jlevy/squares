---
type: is
id: is-01m5jn38xtd10xgdmshtkeat2w
title: "Home page News box: discreet significance filter at top right, default S5 if enough S5 items else S4+S5"
kind: task
status: open
priority: 0
version: 2
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:31.577Z
updated_at: 2026-10-22T21:03:21.536Z
---
c-lane-home-recent-1022, branch claude/home-recently-added (also carries the 'Recently added' section). Epic think-s38d.

## Notes

2026-10-22 21:10Z (c-lane-home-recent-1022): pushed draft PR #736 (https://github.com/jlevy/squares/pull/736), head 313c19c1e (feat e77f13dc1 + merge of origin/main 59b1ec594, #729).
- Home News box: three newest News articles at its opening levels, under news.html's own significance filter in a compact form (render_changelog.news_significance_filter shared; news_filters(compact=True)), small and right-aligned above the cards.
- Opening levels decided at render time (news_highlights.default_levels): S5 alone where News holds >= 3 S5 articles, else S4+S5. Today: S5 (13 Oct, 13 Oct, 30 Sep); with T-194's S5 item it leads with 16 Oct (tested both ways).
- Box carries the newest 3 at each level (9 cards, 42,550 bytes), hidden outside the opening levels, kept hidden without scripts; news-filters.js preview mode (data-news-limit) shows the newest 3 matching and carries a changed choice to news.html as news-s on "All news" (data-news-carry).
- news.html byte-identical apart from the site.css and news-filters.js asset hashes.
- Local: news/changelog/publication tests 87 passed; homepage browser tests 8 passed (1280/390, light/dark, keyboard, no-JS); lint/type clean on changed files. Edit tier running; hosted CI pending.
