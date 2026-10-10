---
type: is
id: is-01m4kavd06vjy2knrcgbd036pr
title: "Import Francisco Couzo: certificates at 132, 175, 209, 237, 270, 305 (#488)"
kind: task
status: open
priority: 1
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:38:00.454Z
updated_at: 2026-10-10T17:42:58.906Z
---
Issue https://github.com/jlevy/squares/issues/488 (2026-10-10T14:08Z). franciscouzo/square-packing 3ef76349025bf4bfa99c9c3600bcc273f4c33e02 certificates/nN.cert (Evan Daniel's format). Below SQUISH's #481 at 209, 237, 270, 305; below this author's #476 at 132 and #460 at 175. Superseded at 132 by #489 (evand Hunt 3). Stages 1-3 through devtools.upper_bound_reports, comparing with #470, #476, #481, #489 and the register.

## Notes

2026-10-10 import lane (stages 1-2 and the replay), worktree branch worktree-agent-af1304354bf317e13, commit 9f0dbb8a7 (with the #489 packet at 46fe607cc):

- Pin: franciscouzo/square-packing 3ef76349025bf4bfa99c9c3600bcc273f4c33e02 (master head, committed 2026-10-10T13:52:27Z, tree 2978a99c), no licence; packet packing/resources/web/couzo-certificates-2026-10-10 retains the nine certificates the commit adds (209) or changes (132, 175, 237, 270, 303, 305, 338, 340) as factual data; the other 54 of the 63 are pinned by digest and identical_to the issue-476 packet's copies (9bf90e7 removed 102, 103, 272). certificates/README.md's SHA-256 column matches all 63.
- Claims (acquisition/claims.json, read at main af17208c0): every requested side is below its case ceiling. Smallest now: 132 #489 (Hunt 3, 1.27e-3 below); 175, 209, 237, 270, 305 this certificate (below #481 by 4.28e-7, 3.96e-5, 4.77e-6, 5.64e-5 at 209, 237, 270, 305; below T-130 at 175 by 3.44e-5). Unnamed: 303 above #481 by 4.30e-3; 338 and 340 below Couzo's own tracked beyond-horizon rows.
- Replay: certify --workers 2, 27 jobs, 1,899,504 pair decisions, 388.0 route CPU s, 3 min 30 s wall; all 9 positives pass both routes, all 18 controls refused; check --replay serial 6 min 42 s, exit 0. Third route: check_half_angle_area decide-imports --imports '#488' '#489' --upstream (both packets), 10 certificates, all 60 of its controls reach their required outcomes, retained files equal to upstream bytes, no disagreement, 19 s wall.
- 305: exactly the side of Hunt 3's hunt3_n305 (c013f43); same arrangement up to a quarter turn; the Hunt 3 log at 76a529b drops 305 as Couzo's.
- Register plan printed (T-NNN); shared records not edited, proposed YAML handed to the coordinator.
- Validation at 46fe607cc: packing-validate --records 49/49 steps passed (59.7 s); --edit 65/65 passed (252.5 s at load ~10, over the 240 s ceiling, reported not enforced); touched tests 229 passed.
