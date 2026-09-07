---
type: is
id: is-01m1yqn8kfc49b2a94gw79b2fr
title: Correct print-layout measurement for mixed text and math lines
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1ypqw8hjkd27mp8qzz43md6
created_at: 2026-09-07T20:06:24.110Z
updated_at: 2026-09-07T20:06:24.110Z
---
Local review of PR112 reproduces two false marker-alignment failures on both original and revised paper. firstLineBox groups rectangles only within 1px of the topmost run, dropping the actual line box when math and prose ascent differ. Use a first-line overlap group; preserve next-line exclusion and rejection of displaced markers. No paper CSS or font changes.
