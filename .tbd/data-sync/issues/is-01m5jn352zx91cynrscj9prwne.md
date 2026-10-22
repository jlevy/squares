---
type: is
id: is-01m5jn352zx91cynrscj9prwne
title: "Root cause and postmortem: why T-194 (S5) and 26 S3+ results got no News item"
kind: task
status: open
priority: 0
version: 2
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:27.647Z
updated_at: 2026-10-22T20:57:56.106Z
---
Read-only analysis of the announcement path (result-import.md announcement step, render_announcement, site-changelog.yaml, news_highlights, PR history of T-153/T-154/T-194 and the S3 batches); write a postmortem for docs/project/postmortems/. Epic think-s38d.

## Notes

2026-10-22 21:00Z coord-intake-1021b: postmortem done by c-rootcause-announce-1022 (scratchpad/announce/postmortem.md, 339 lines), to be committed by #735 as docs/project/postmortems/postmortem-2026-10-22-results-without-news.md. Root cause: a result's News article cannot be written in its registering PR (validate requires a retained merged delivery and the merge date) and the follow-up step had no owner and no check; nothing reads results.yaml against News. Contributing: two meanings of 'announcement', self-ticked checkbox, gated release ceremony crowding out ungated News, handoffs split work, score raises trigger nothing, S5-only home box and S4/S5 News default hid the gap. Recommendations filed as children of think-s38d. S3 audit (think-2252) also covers non-result S3 PRs #644, #645, #578. Close when #735 merges.
