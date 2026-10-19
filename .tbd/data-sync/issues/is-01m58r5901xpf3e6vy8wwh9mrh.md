---
type: is
id: is-01m58r5901xpf3e6vy8wwh9mrh
title: "Import franciscouzo: 85 upper bounds at 204–998 (#678)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-19T00:14:38.592Z
updated_at: 2026-10-19T00:25:23.040Z
started_at: 2026-10-19T00:15:01.708Z
---
New 2026-10-18 issue https://github.com/jlevy/squares/issues/678 reports 85 upper-bound rows from franciscouzo/square-packing commit 7b6c87e129cf80b5ff9847b90b47fd30b4563c54, parent c6da0fc7524d667bf3d224559724ba9b60762e60 (#675). Stage 0 owner for the new report; source claims are unverified. Read-only table triage finds 55 counts overlapping #675, each tighter than its earlier displayed value, and 30 new counts; #675 also has 24 counts absent here. Preserve both chronologies and credits, including two deletion-derived rows n545/n641. Next: add pending request/read-through, retain pinned source custody and report-order comparison; price exact replay, independent review and any later house adoption. #678 n260 is below pending T-196 in #676, so later registration must supersede it in merge order without rewriting that earlier report. Do not infer certificate validity or allocate a T number before merge. Draft author reply after the relevant records merge and deployed-site verification. Coordinate with think-pvav (#675). blocked_on: none

## Notes

2026-10-19 independent Astra Stage1 read-only triage. #678 has 85 claimed rows bound to 83 distinct linked witnesses; n545/n641 delete from n546/n642. Declared displayed values are upward rounded exact sides and declared exact sides improve the preceding c6da0fc index, but no witness replay or public priority check occurred. n260 new exact side 146417594016514621500994169/8796093022208000000000000 (display 16.645753250545) is later than T-196 and must not rewrite it. Material lineage gap: preceding c6da0fc index claims intermediate 16.645778786062 / decompressed SHA e90993...4934e, but its retained n260 cert/manifest still carry original T-196 side and SHA df90e5...2d31. New metadata attributes e90993 to evand search/regularize/lists/certs/n-260.cert.gz, but at pinned evand 0f37f49 that path decompresses to SHA 0f8bc736897812b792a787bfe45277b4a90943147ff522c1df44e8244925ef07 with a different 16.656854... side. No e90993 parent artifact found in those source trees. Preserve intermediate as source-reported unresolved provenance and request exact source bytes before adoption. Retain 83 witnesses, mappings, parents, indexes, checker and MIT notice; selected certs 8,107,636 bytes by source metadata. Independent arithmetic, corruption controls, replay, and math review required; source corner bucket uses float centers, so exhaustive-pair replay or exact-filter justification needed. Review: https://github.com/franciscouzo/square-packing/blob/7b6c87e129cf80b5ff9847b90b47fd30b4563c54/certificates/best/manifest.json . No claim of verification or optimum.
