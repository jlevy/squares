---
type: is
id: is-01m4wrcwat4ft1zc55mrm29a8n
title: "Import evand: s(365) <= 19.621320343560, s(370) <= 19.767730746255, s(460) <= 21.959969683021, beyond the case corpus (#596)"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T08:27:54.586Z
updated_at: 2026-10-23T06:12:42.128Z
started_at: 2026-10-14T08:27:59.898Z
closed_at: 2026-10-23T06:12:42.128Z
close_reason: "Tracker audit 2026-10-23 (c-audit-b-1023, think-ioqe), checked by coord-intake-1023: STALE-CLAIM + DONE. #596 closed 2026-10-16. Its three beyond-horizon rows are registered via #602. check_requests: closed, 1 of 1."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/issues/596 (2026-10-14T06:51:07Z, unedited). evand/square-packing at 622cd2e21407700fe8d5ac5943af820725107921, search/packer/candidates/fresh_n365, n370, n460 (.cert, .exact.txt, .input.txt, .json). All three counts lie beyond n = 324: verified beyond-horizon rows in source-coverage.yaml, as #506 and #584. Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports, intake lane ostashev of 2026-10-14 (added by the coordinator).

## Notes

Issue: https://github.com/jlevy/squares/issues/596 (opened 2026-10-14T06:51:07Z by evand; label intake added; body never edited; no comments as of 2026-10-14T08:27Z). Added to lane ostashev by the coordinator during the pass.

## Stage 1 triage, 2026-10-14, intake lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev)

Pin: evand/square-packing 622cd2e21407700fe8d5ac5943af820725107921 (committed 2026-10-14T06:50:09Z), the commit the issue names and still the head at 2026-10-14T08:28Z; its three .cert SHA-256 match. MIT licence (LICENSE, CREDITS.md).

Claims the release makes, and their register map:
1. s(365) <= 19.621320343560, s(370) <= 19.767730746255, s(460) <= 21.959969683021 (12 places rounded up; exact sides 19.621320343559642573398746289751, 19.767730746254604158720695152869, 21.959969683020493134160191682454). All three lie beyond the case corpus: no register entry; three beyond-horizon rows in source-coverage.yaml (verified after review, as #506's and #584's).
2. 365 = s(26) + 14 = 14 + 7/2 + 3/sqrt(2): measured here, (side - 35/2)^2 = 9/2 + 8.3e-19, the 1 + 1e-20 scaling of that sum; a test holds it.
3. KKT / reduced Hessian / MILP: numerical evidence as the source says; not registered.
4. Lineage: fresh pass over #586/#593 packings; 365 = SQUISH s(199) + Friedman s(26); 370 = Couzo s(175) (#488) + author's 38-square (h+2) x h rectangle; 460 = crops of SQUISH s(306) (#481) and Couzo s(380) (#586). Claude (Claude Code) assistance disclosed, directed and reviewed by Evan Daniel.

Who else holds each value (frozen in acquisition/claims.json against main aeef99ef0; grid 20, 20, 22):
- No beyond-horizon row on main at 365, 370 or 460 (tracked counts near: 364, 369, 372-379); #584's rows are at 339/364/375. No other open report of this pass (#561, #570, #582, #583, #586, #593, ...) names them. Smallest at each: this certificate.
- Below the issue's L-step bounds (no row holds them): 365 by 1.28e-2 (s(293) + 2), 370 by 1.04e-2 (s(298) + 2), 460 by 1.64e-3 (#586's s(380) + 2 = 21.961611078671).

Validation plan (priced): evand-cert adapter; both maintained exact routes, --workers 1: 9 jobs, about 10 min each pass at load 4. Source checkers pinned against the issue-399 packet, not run. Review: records lane, as for #506.

## Draft acknowledgement (not posted)

Thank you, Evan. We received the three certificates at evand/square-packing 622cd2e (search/packer/candidates/fresh_n365, n370 and n460), and the three SHA-256 values match the files there. All three counts lie beyond the n <= 324 case corpus, so they go to the source register's beyond-horizon rows, as #584's do. We will retain the commit, read each certificate exactly, decide each packing with a duplicate-square and an outside-container control on our two maintained exact routes, and compare each side with what the record holds at its count; it tracks no row at 365, 370 or 460 today. Your 365 side is, to within its 1 + 1e-20 scaling, 14 + 7/2 + 3/sqrt(2), as you say.

## Stage 2 and the stage 4 replay, 2026-10-14, lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev, head 8d396177b)

Packet packing/resources/web/evand-fresh-compositions-2026-10-14 (source key [Daniel fresh compositions 2026-10-14], evidence E-evand-596-compositions-report): 12 fresh_* files, LICENSE, CREDITS.md, search/exact/README.md retained (15 files, 521,230 bytes); checkers pinned to the issue-399 packet, PACKER.md by digest.

certify --workers 1: 9 jobs, all 3 positives pass and all 6 controls refused on both routes, 1,441,590 pair decisions, 654.96 route CPU s, 13m54s at load 4-7; least wall >= 5.00e-21, pair just under 1e-20. check --replay: 9 jobs equal, 18m27s at load 7-10.

Register plan: scratchpad register-plan-evand-fresh-compositions-2026-10-14.yaml (evidence, source row, three beyond-horizon rows at 19.621320343560, 19.767730746255, 21.959969683021).

## Stage 1 acknowledgement posted, 2026-10-14

https://github.com/jlevy/squares/issues/596#issuecomment-6165053338 (states the pin, the retained and replayed certificates with controls refused, and the comparison at each count; the earlier draft above was not posted as written).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): #596's 365, 370 and 460 as new beyond-horizon rows.
