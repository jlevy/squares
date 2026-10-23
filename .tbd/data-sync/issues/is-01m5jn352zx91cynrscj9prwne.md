---
type: is
id: is-01m5jn352zx91cynrscj9prwne
title: "Root cause and postmortem: why T-194 (S5) and 26 S3+ results got no News item"
kind: task
status: closed
priority: 0
version: 4
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:27.647Z
updated_at: 2026-10-23T00:45:39.116Z
closed_at: 2026-10-23T00:45:39.116Z
close_reason: "#735 + #738 merged (690e21857)"
resolution: null
duplicate_of: null
---
Read-only analysis of the announcement path (result-import.md announcement step, render_announcement, site-changelog.yaml, news_highlights, PR history of T-153/T-154/T-194 and the S3 batches); write a postmortem for docs/project/postmortems/. Epic think-s38d.

## Notes

2026-10-22 21:00Z coord-intake-1021b: postmortem done by c-rootcause-announce-1022 (scratchpad/announce/postmortem.md, 339 lines), to be committed by #735 as docs/project/postmortems/postmortem-2026-10-22-results-without-news.md. Root cause: a result's News article cannot be written in its registering PR (validate requires a retained merged delivery and the merge date) and the follow-up step had no owner and no check; nothing reads results.yaml against News. Contributing: two meanings of 'announcement', self-ticked checkbox, gated release ceremony crowding out ungated News, handoffs split work, score raises trigger nothing, S5-only home box and S4/S5 News default hid the gap. Recommendations filed as children of think-s38d. S3 audit (think-2252) also covers non-result S3 PRs #644, #645, #578. Close when #735 merges.

2026-10-23 00:46Z coord-intake-1021b: done. #735 merged by the owner (bfc04b659: the gate, T-194 News item, postmortem docs/project/postmortems/postmortem-2026-10-22-results-without-news.md); #738 merged as 690e21857 with #735 review A fixes and #738 review A fixes (gate fails only a PR that edits results.yaml or site-changelog.yaml; warns on unrelated PRs and always on main; frozen 15 exemptions; 40 mutants killed). T-194 News item is live on squaremath.org (home box leads with it since the 22:06Z deploy). Follow-ups: think-n51k (same-PR items), think-mh7q, think-r118, think-mubh, think-yelx, think-2252, think-gq0l.
