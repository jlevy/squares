---
type: is
id: is-01m74fener751d3cv3kntesy95
title: "Import #943, #944, #945, #947: Doğa Özden's s(156), s(180), s(268), s(269) (kenaznia-doga, 10-11 November); plus #847's count comment and the evand / TheSnakeFang watched-repo commits"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l81
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-11T04:56:54.996Z
updated_at: 2026-11-11T05:43:25.523Z
started_at: 2026-11-11T04:57:02.266Z
---
#943 s(156) <= 12.977053087498, #944 s(180) <= 13.915618502791, #945 s(268) <= 16.872029849085 (below T-276, his own #928), #947 s(269) <= 16.900994579952; opened 2026-11-10T15:28Z (three) and 2026-11-11T03:35Z. Precedent: #927-#931 (PR #932), #935/#936 (PR #937). Also: #847 comment 6776987457 (mohsensbu-jpg, 2026-11-10T19:22Z, record-count update); watched repos evand/square-packing (10 commits to c801ab47) and TheSnakeFang/squarepack-certs (2 commits to be93eb16): read, import if any new result, else intake-watch reads.

## Notes

## Lane L81 (bold-ritchie-l81), 11 November 2026

Branch `claude/bold-ritchie-xo28us-l81`, cut from `origin/main` `f54ad1048`.

**Stage 2, retained.** Four packets, each pinned at its repository's one commit; every stated
SHA-256 holds; `acquire_source --check` PACKET_MATCHES_ITS_CONTRACT on all four:
`ozden-s156-upper-bound-2026-11-10` (87c9292), `ozden-s180-upper-bound-2026-11-10` (4cfcb90),
`ozden-s268-upper-bound-2026-11-10` (b027aba), `ozden-s269-upper-bound-2026-11-11` (6f93b07).
Pinned-only: the diff PNG by digest; verifier/README.md, sqcheck.py and Evan Daniel's MIT notice
identical_to the s299 (3 Nov), s232 (9 Nov) and evand-issue845 copies.

**Stage 4 replay.** Controls plan written before any run (scratch
`l81/notes/controls-plan.md`, SHA-256 2d353210…61c2, 05:04:42Z). `certify` 12 jobs, 600,144 pair
decisions, 246.2 route CPU-s; `check --replay` passed on all four; `sharp-controls` 44 controls,
all as expected (each wall-enlarged square grown by 0, accepted at contact). Least pair gaps
2.00e-13 to 2.03e-13; walls touched exactly.

**Measurements.**

| n | issue | house | gain | beyond 0.1 (assignment) | house margin | own margin |
| ---: | --- | --- | --- | ---: | --- | --- |
| 156 | #943 | T-186 (T-260 pending, held) | 2.113e-3 | 58 | 1.30e-39 | 2.42e-12 |
| 180 | #944 | T-174 | 1.375e-3 | 49 | 0 (pair touching) | 2.58e-12 |
| 268 | #945 | T-276 (his #928) | 4.400e-4 | 125 | 3.19e-12 | 3.20e-12 |
| 269 | #947 | T-174 | 5.190e-4 | 112 | 0 (pair touching) | 3.24e-12 |

None is one to one with its house under any symmetry. RV-3 (think-ruu2) reaches none: every gain
is at least 1.4e8 times the predecessor's padding. `l_step_scan` with all four sides stood in:
same L-step and monotonicity consequences as main; no bound propagates (landings 181, 207, 301,
302 all above their ceilings). 268's side is 3.27e-12 above 16 + .872029849081179973… (the
fractional part of T-145's exact sides at 129, 153, 302); contracted, 6.6e-14 above it; recorded
as a measurement only.

**Ledger** `upper-bounds-943-947-20261111`: all four recorded; 156's start includes T-260 pending.

**Stage 3.** T-285 (156), T-286 (180), T-287 (268), T-288 (269), V3/C3 on the replay, draft S3,
taken after main's T-284; L78 (think-2h88) may land T-285/T-286 first, in which case these
renumber. No case record moves: adoption waits on the blind stage 4 review
(select_houses.accepted_review). Deferrals in certificate-citation-deferrals.yaml name
think-xq4o as blocked_on until the review lane's bead exists.

**Follow-ups owed at adoption:** #593 (T-186 at 156), #574 (T-174 at 180 and 269), #928 (T-276 at
268, whose final reply named T-276 current).

**Scope 2.** #847 comment 6776987457 read: 5,601 = 5,308 + 5,134 − 4,841 holds in retained data,
versions 1 and 2 of #799 are subsets of v5's counts; nothing new; read_through moved, note added
(reply now due). evand/square-packing 10 commits to c801ab4: code/TODO only, read recorded.
TheSnakeFang/squarepack-certs 2 commits to be93eb1: Kevin Fang's claimed wedge note (slabs and
trapezoids, Bui's Conjecture 1); bead think-0fa1 opened, read recorded with that bead.
