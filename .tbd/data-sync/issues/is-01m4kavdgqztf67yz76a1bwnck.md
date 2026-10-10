---
type: is
id: is-01m4kavdgqztf67yz76a1bwnck
title: "Import Evan Daniel: Hunt 3 packings at 132, 308, 343, 344 (#489)"
kind: task
status: open
priority: 1
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:38:00.983Z
updated_at: 2026-10-10T17:42:59.624Z
---
Issue https://github.com/jlevy/squares/issues/489 (2026-10-10T14:47Z). Quality-diversity basin explorer with a two-parent crossover (as #465). s(132) <= 11.985680198845808811522231964102, s(308) <= 17.998269879526255875387992744507, s(343) <= 18.978232523635611279730512106023, s(344) <= 18.994450514277401521114135796864; each below #488 (132) or #484 (308, 343, 344). evand/square-packing head 76a529bc6f36 (2026-10-10). 343 and 344 are beyond the n <= 324 horizon. Stages 1-3 through devtools.upper_bound_reports.

## Notes

2026-10-10 import lane (stages 1-2 and the replay), worktree branch worktree-agent-af1304354bf317e13, commit 46fe607cc (after the #488 packet at 9f0dbb8a7):

- Pin: evand/square-packing main head 76a529bc6f36ed05827cae3d1412d6acb5be00fc (committed 2026-10-10T14:48:25Z, tree c1f66266), parent c013f43cefd006f007a6f37bc3a56aadead815d6, the commit the issue names; the head changes only search/packer/PACKER.md and search/packer/pk/pending.yaml, so every retained byte is the same at both. MIT; packet packing/resources/web/evand-record-hunt3-2026-10-10 retains the five Hunt 3 certificates (132, 305, 308, 343, 344) with .exact.txt, .input.txt and .json, plus LICENSE, CREDITS.md and search/exact/README.md; verify_cert*.py pinned identical_to the issue-399 packet; PACKER.md digest only.
- Claims (read at main af17208c0): 132 smallest, below #488 by 1.27e-3 and below the case (T-098) by 5.65e-3; 308 smallest, below #484 by 1.04e-3 and the grid by 1.73e-3; 343 and 344 beyond the horizon, below #484 by 1.67e-2 and 1.04e-3 (beyond-horizon-claims.json holds only them). Unnamed 305: exactly #488's side; printed comparison undecided; same arrangement up to a quarter turn; the log at the pin drops it as Couzo's.
- Replay: certify --workers 2, 15 jobs, 1,319,598 pair decisions, 308.35 route CPU s, 3 min 33 s wall at load ~7; all 5 positives pass both routes, all 10 controls refused; check --replay serial 5 min 33 s, exit 0. Third route: decide-imports --imports '#488' '#489' --upstream, the four requested certificates pass with all 24 controls, retained files equal to upstream bytes, no disagreement; the unnamed 305 measured by arrangement_gap against #488's: one side, a quarter turn apart, 34 squares moved beyond 1e-9 (largest 1.77e-2).
- Register plan printed (T-NNN for 132 and 308; beyond-horizon rows at 343 and 344 that supersede #484's once both are registered); shared records not edited, proposed YAML handed to the coordinator.
- Validation at 46fe607cc: packing-validate --records 49/49 steps passed (59.7 s); --edit 65/65 passed (252.5 s at load ~10, over the 240 s ceiling, reported not enforced); touched tests 229 passed.
