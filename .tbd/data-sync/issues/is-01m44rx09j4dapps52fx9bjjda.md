---
type: is
id: is-01m44rx09j4dapps52fx9bjjda
title: "Import Guzhou0806: s(17) R070 and R071 (4.6604427, 18641771/4000000), above the verified 116511/25000"
kind: task
status: in_progress
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g51s5a06f0r0qsqy5tte3
hold: null
hold_until: null
created_at: 2026-10-05T00:54:56.562Z
updated_at: 2026-10-06T08:47:57.990Z
started_at: 2026-10-05T03:10:51.428Z
---
Found in stage 1 of the evand site import (think-plrl): evand's lower_bounds.json at evand/square-packing 7ff3b21 (retained in packing/resources/web/evand-square-packing-2026-10-04/) lists Guzhou0806 R070, s(17) > 46604427/10000000 (29 Sept, tree 8988d9333, certificates/R070-4.6604427) and R071, s(17) > 18641771/4000000 = 4.66044275 (30 Sept, tree 8c11f696, certificates/R071-C029; the repository's own CI replay 'R071 exact replay' passed; its README notes the old C027 partition records are missing), both above this record's verified s(17) > 116511/25000 (R068, T-043). Neither is in the register, an evidence entry or source coverage. By packing/campaign/result-import.md stage 1 a claim in scope that a request does not mention is an import of its own, from the author's own publication (github.com/Guzhou0806/n17-square-packing), not from evand's site. Kleddamag's 46601/10000 (29 Sept) is below R068 and stays a packet note. Pin the source, retain R070/R071 with their checkers, record as reported, price the paired replay (R068's took the C++ checker and Kleddamag's Node BigInt checker).

## Notes

Workflow: W1 import, stages 1-3 of packing/campaign/result-import.md, plus the R068-style pre-replay audit. Branch claude/ecstatic-pascal-pothtx-guzhou, commits 7ae4194dd, cd1b88195 (not pushed).

Pin: Guzhou0806/n17-square-packing 8c11f6962506940c5de67a9fa73b3d1e2e151196 (2026-09-30T22:53:43Z, main at retrieval 2026-10-05T03:11Z); R070 at 8988d933 (2026-09-29T07:56:05Z). Packet packing/resources/web/n17-guzhou-r071-2026-09-30 (acquire_source declaration; 153 retained, 33 pinned-only: 32 byte-identical to the R068 packet's upstream/ checker and notices, 1 research output; --check PACKET_MATCHES_ITS_CONTRACT). Keys [Guzhou0806 n17 R071] (dated 2026-09-30), [Guzhou0806 n17 R070] (context). Coverage guzhou-n17-r071-2026.

Claim map (claim -> action -> id):
- R071 s(17) > 18641771/4000000 = 4.66044275, C027 cert 15b6bf6a, R068's charge unchanged, 5,114 intervals -> new entry (later release raising T-043's value), reported -> T-093 (provisional; V0/C0, S2 draft), E-n017-guzhou-r071-report, n-017 reported lane
- R070 s(17) > 46604427/10000000 = 4.6604427, cert 8438cae4, 5,107 intervals -> none: superseded by R071 (built on it) the next day, never replayed; stays in packet and n-017 prose
- R070 319-orbit same-budget overlay; parent-separation obstruction at 186417711/40000000 in a fixed-weight class -> none (no bound, source says so)
- R071 C028/C029 conditional joint geometry at 9321/2000 in one first-anchor box (17 conflicts, 2 forced holes, 9<=Vmax<=11, 8 unknown pairs) -> none (source: does not prove s(17)>4.6605)
- T-043 (R068) keeps the verified field; coverage note added.

Pre-replay audit (devtools.audit_guzhou_r071, receipts in packet): both certificates' point orbits, rules, budget and requested minimum equal R068's; chains refine R068's (R070 +116, R071 +7 bisections over R070); all cores rebuilt (same angle, new side). R070 published 4+4 ledgers agree row by row: min 1000026844 on all 5,107 rows, cells 2,260,759,562,719, surplus 7404. R071 C027 summary consistent with its cert; names R068's verify_global_variable.js and replay.js digests and R068/R070's executable. R071 row records missing (source says so). Source CI: R070 run 36539632653 and R071 run 36788162356 both success (bound job 16m43s); artifacts unreachable (Azure blob 403).

Price (stage 4, not run): R071 complete paired replay (run_public.js bound or replay.js at 2 partitions, then audit_guzhou_r071 compare R071 FRESH --published FRESH) ~ 4,200 CPU-s (~70 CPU-min), ~80 min wall on 2 contended cores, scaled from R068's measured 4,093 CPU-s by R070's published cells (x1.023). Source: C027 1,694 s at 3 partitions; R070 869 s at 4. Needs Boost headers (libboost1.83-dev; absent here). R070 needs no replay of its own. Cheaper diagnostic first: the r071-bound CI artifact (expires 2026-12-29) holds fresh partitions, from a host that can reach the blob store.

Kleddamag/17-squares-certified-bound 17d18245 (4.6601, below T-043): read recorded in intake-watch.yaml; overlaps think-nkzt's list.


The parent of this bead is:
---
type: is
id: is-01m44qz3phdnc1yfv76nxp6cak
title: "Import evand: the Square Packing Atlas site (evand.github.io/square-packing, incl. problems.html) and repository results since 2eb15455"
kind: task
status: in_progress
priority: P1
version: 5
delegate: claude-code@vm
labels:
  - result-import
# Blocks: think-aygi
dependencies:
  - type: blocks
    target: is-01m44qz5cez2hhdr2b5p4m1sya
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
child_order_hints:
  - is-01m44rx09j4dapps52fx9bjjda
hold: null
hold_until: null
created_at: 2026-10-05T00:38:37.009Z
updated_at: 2026-10-05T01:12:30.330Z
started_at: 2026-10-05T00:41:15.310Z
---
Retain the site pages (index, explore, compare, bounds, proofs, problems, sources) and the new s12 notes at evand/square-packing 7ff3b21 in a packet, add bibliography keys, write a mapped review of the site's claims against the register (docs/project/reviews/), map each claim: s(20) > 3 + 4 sqrt(2)/3 (2010d63, below wand125's 1959/400), Lean LebMass (LEB/CAP leaves kernel-checked), SpecChelokot, CEILINGS_17_20, open problems/conjectures. evand.github.io is blocked by egress; use the git repository (site/www is the Pages root).


Workflow: W1 import, stages 1-3 of packing/campaign/result-import.md, plus a citation review of the site. Branch claude/ecstatic-pascal-pothtx-evand, commits 5c4626b95, 6d48ab842, 4e72c1156 (+ validation fix-ups if any).

Pin: evand/square-packing 7ff3b2113532889708a3baa4d56bc44294022e63 (2026-10-04T20:17:38Z), retrieved 2026-10-05T00:34Z, main at retrieval. evand.github.io blocked by egress; pages read from the commit (site/www = Pages root, s12/docs served under it).
Packet: packing/resources/web/evand-square-packing-2026-10-04 (acquire_source declaration; 69 retained, 2 pinned; --check PACKET_MATCHES_ITS_CONTRACT). Keys: [evand square-packing 2026-10-04], [evand square packing atlas 2026-10-04]. Coverage: evand-square-packing-2026-10-04.

Claim map (claim -> action -> id):
- s(11), s(21), s(32), s(45), s(59), s(60), s(61), s(77), s(78) as site states -> already registered -> T-060, T-052, T-051, T-053, T-066, T-062, T-063, T-067, T-064
- s(k^2-3)=k k>=6 -> already registered -> T-064; s(k^2-4)=k k>=5 -> already registered, reported -> T-081 (replay think-4uir)
- s(k^2-1), s(k^2-2) re-proofs -> already registered -> T-084, T-086, T-085
- s(12) >= 15680000/3949423 -> already registered -> T-079
- s(20) > 3+4sqrt2/3 (point cover side 2443/500, S20_LB.md, REPORT.md) -> below standing 1959/400, stays in packet -> reported evidence E-n020-evand-point-cover-4886-report cited by n-020 only
- pure-cover ceilings n=17-20 (CEILINGS_17_20.md) -> none (method limit by others, not acted on)
- Lean LebMass (689 LEB + 374 CAP leaves of ValidTilt7), ValidSplit7 -> evidence update on T-064 (next_rung, notes, artifacts); no rung moves
- SpecChelokot -> evidence update on T-086 (notes); no rung moves
- floors table n<=100 -> checked: devtools.compare_site_floors, receipt in packet: 99/100 equal verified lane, n=96 = reported T-081, all 20 'verified' marks held, 24 family-ring counts past 100 held
- Guzhou0806 R070/R071 (s(17) > 18641771/4000000, above verified) -> import of its own -> think-1qms
- Kleddamag 4.6601 -> below standing, packet note
- open problems/conjectures -> none (questions), checked in review §5
Review: docs/project/reviews/review-2026-10-05-evand-square-packing-atlas.md (mapped). Non-blocking S-1..S-7 for the author: s(211)<15 listed as target though T-057; n=77 floor credited to k2m4 route; T-043 shown V4/C3; T-060 'independently'; Nagamochi gap credited to Karakus alone; root README stale; zeromargin.roots() latent gap (not hit here).
Stage 7 draft (owner posts, no issue): none filed; reply to Daniel optional with the review's S-items.


Validation: --records fails only on register id contiguity (T-093 before T-088..T-092 land); in a throwaway copy with T-093 renumbered to T-088, check_results and tests/test_results_register.py (75) pass. --push (once, 2,166 s): same contiguity step, and reachable behavioral tests (whole suite selected) timed out at 1,800 s under two concurrent full suites, ~50% through with 4 failures, the count of test_results_register's contiguity failures; the targeted 418-test subset over the changed records passed except those 4. Stage 4 replay waits for a budget; this bead stays open.
