---
type: is
id: is-01m42wgpehmgc90djvxxb2sw4a
title: "Import wand125: 14+ mixed certificates (#282)"
kind: task
status: closed
priority: 1
version: 9
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-04T07:19:38.704Z
updated_at: 2026-10-05T07:19:56.861Z
started_at: 2026-10-04T07:32:04.027Z
closed_at: 2026-10-05T07:19:56.861Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Mixed rectangle-measure certificates posted on jlevy/squares#282 from 2026-10-03 19:33Z (14 at upstream 3554616; two more at 6832.. and 8aa6.. after 07:00Z). Stages 1-2 on branch import-282-mixed14 (packet wand125-mixed-bounds-2026-10-04, W7 audit binding by pinned digest). Stage 3 (new T-NNN) was held for jlevy/squares#305, which merged 2026-10-04; it is done as T-090 on PR 353. Replays (~124 CPU-h for 14) held with think-wpuu. Separate import needed: c56b9b7 (T-066 F1/F2, #280).

## Notes

2026-10-05: #305 merged 2026-10-04T23:00Z, so stage 3 is unblocked; taken by the follow-up epic think-05m9 (wand125 lane, T-090).


The parent of this bead is:
## Notes

2026-10-03 18:30 Owner: once everything is landed, comment on each issue and tag the contributor (@evand, @wand125, @squarepacker, @XiaoLiaoShe, @franciscouzo as applicable) where their results are imported; one final reply per issue from main with register ids and disposition (check_requests --draft N), evand's #316, #256 and #238 first; close the issues check_requests reports closeable.

2026-10-05 02:45Z stage 3 done on branch claude/ecstatic-pascal-pothtx-wand125 (tbd-moderate wand125 lane, re-scoped by the coordinator), commit 905621e8b: T-090 registers the 16 at 8aa6a10 (n = 42, 43, 44, 51, 56, 57, 67, 69, 72, 75, 84, 86, 88, 93, 94, 95) at V0/C0, S3 draft; 16 report evidence entries; coverage entry wand125-mixed-bounds-2026-10-04; reported lanes of 14 case records (n88/n94 report T-091's later 481/50 and 199/20; T-090 keeps its claim there). #282 results oct3-oct4-mixed-14 and oct4-n86-n69 map to T-090. The 150939e OC-1/OC-2 answer is recorded as an evidence update on T-082's 22 report entries and T-075's two mixed_n96_L996 entries. Replays (146.5 CPU-h planned, mixed-shard --runners 8) stay with think-wpuu. Blind review not done: this lane had no sub-agent tool; brief ready for the coordinator. Not pushed.

2026-10-05 04:00Z blind review (separately prompted reviewer, commit 64d710577, not pushed): docs/project/reviews/review-2026-10-05-wand125-october-4-certificates.md accepts T-090 and T-091 with no blocking defect; OF-1 judges the WITHOUT_SOURCE_AUDIT binding (digest at the pin, README, mixed-fetch) sufficient, all 28 tarballs re-downloaded with their pinned SHA-256; OF-4 corrects two measurements of the 3 October review; OF-5 n86-L9503 priced 10.2 vs 10.3 CPU-h in the two packet READMEs. Spot replay n88-L96125 index 92 from a regenerated input returned its record (235 s here). T-090 now V0/C1 (external_review on its 16 report entries, reviews entry, notes split into two paragraphs for check_prose_ceremony). S3 confirmed. Records tier fails only id contiguity.
