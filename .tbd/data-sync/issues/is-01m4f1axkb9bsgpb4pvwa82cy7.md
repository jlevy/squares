---
type: is
id: is-01m4f1axkb9bsgpb4pvwa82cy7
title: Contain drawings and captions in uniform Triangle tracks
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ez50758mp6g61k4z50eh23
hold: null
hold_until: null
created_at: 2026-10-09T00:34:45.471Z
updated_at: 2026-10-09T00:35:24.496Z
started_at: 2026-10-09T00:35:24.494Z
---
Fresh mandatory Chromium suite on the current uniform-height website found two regressions: inherited KPress drawing image margins are missing from the fixed track-height calculation, so captions and badges overflow the tile; the retained measurement helper still expects a half-drawing vertical transition gap. Include the actual existing image margins in the common caption-aware track height without changing drawing positions or scale, and update only the obsolete vertical-gap contract to ordinary line spacing. Preserve two-line grid markers, horizontal half-drawing separation, equal height/pitch, adaptive right alignment and interactions. Run focused/static checks and the complete current 82-test mandatory Chromium suite, preserving real failure and repair receipts.
