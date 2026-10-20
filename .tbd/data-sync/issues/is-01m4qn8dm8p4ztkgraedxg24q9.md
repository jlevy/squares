---
type: is
id: is-01m4qn8dm8p4ztkgraedxg24q9
title: "Read evand/square-packing 2b89650..ad86d42 (26 commits, 11-12 Oct): no new bound; s(29) minimal polynomial and grade-C local minima retained (#545)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-12T08:56:50.568Z
updated_at: 2026-10-12T09:08:36.788Z
---
Watched-repository read for lane W of the 2026-10-12 intake (think-mq0k); nothing on GitHub asked. Not an issue: neither result below was reported on jlevy/squares.

**Range.** evand/square-packing, the 26 commits of 11 and 12 October (UTC) from 2b89650 (19:14Z) to ad86d42d0f743076d735036702ba04a41ce24a8c (2026-10-12T04:39:01Z), past the last recorded read, 675a5ea (think-0ayk, 2026-10-11), the same on l4, origin/main and b4c030f11. ad86d42 was still the head at 08:46Z (git ls-remote). Sibling repositories: evand/square-packing-12 is archived (head e683e24, 2026-09-11, "Moved to evand/square-packing"); evand/open-math-problems (last push 2026-10-07) is a tier list of open problems, outside this record. No read of either is recorded, and neither has anything to import.

**Claims, mapped by the stage 1 table.**

| Commit(s) | Claim | Map |
| --- | --- | --- |
| 169a827, 7ea600b | the s(29) record side 5.933833462676929189689460616352... is a root of an irreducible integer polynomial of degree 7213 (homotopy continuation; irreducibility, Krawczyk and link rigorous, two identity checks Monte Carlo); polynomial not published | an exact value the record does not hold (n-029.md: no minimal polynomial "in the literature or here"); new entry or evidence update, think-6gti |
| 0d0146e, e493eea, 7ea600b | grade-C local minima (strict modulo exact flat motions, IsLocalMinPacking): 233 of the source's 250 configurations of field degree <= 4 VALID; certificates not published | a later release adding counts to T-124's kind; new entry, think-7scz |
| 7e3176f, 563aa47 | s(12) strip leaf: Lean wallStripBound_117 and guillotine_false_117 (unconditional, no sorry, standard axioms), the stitch strip_leaf given SeamOK and RegionOK; a point cover cannot prove the region lemma (by the fractional packing bound, any point cover weighs at least about 7.97 in the main case, at most 0.03 below 8); paused | a method and a negative toward s(12) = 4; no bound; nothing to import |
| ad86d42, d446e93, f472179, 8cb7561, b83c185, c600809, cf2d756, aac54a1, 3cf51d0, 8bf8f3d, 7bd1dc4, a340932, f00f56b, fd9cb93, aa3e04f, a7fcf1f, 775f52d, 0772aab, 28ff25b | s(110) packer census (store 778 certified minima below 11 after the re-solve; published snapshot census110_1011b: 780 minima, 740 certified and 40 weak; site landscape110.json 775), census v2 and v3 results, finisher and kick-retry negatives, CLAIMS/CONFUSIONS, review, manifests, refsets | nothing to import: the least census minimum is S = 10.99678339663159163950277843399, the exact KKT side of T-098's packing, 1.10e-19 below the case's verified rational 10.996783396631591639612746267957 (its outward rounding); the next is 3.72e-6 above; no census certificate is published |
| 2b89650 | Mondrian corner-overlap sweep: 43,388 fills, 0 wins, 164 ties | a negative; nothing to import |
| c600809 (notes/refresh-2026-10-11.md) | the author's read of #506, dostashev, Kingbird and other repositories | nothing to import (values already owned by think-om5l, think-9fjl and the #501 import) |

**n = 110 and n = 261 (the coordinator's questions).** n = 110: nothing below the case ceiling; see above. n = 261: the grade-C run at 261 is on the roster configuration of side 684/41 = 16.682926829..., 4.15e-3 above T-150's 16.678779875343207747... (Robert Barnett, #505); it says nothing about T-150's packing. No commit in the range adds a certificate at 261 or at 110.

**Packet.** packing/resources/web/evand-exact-and-local-reports-2026-10-12/ on branch intake-watch-1012 pins ad86d42 and retains the two reports' paths (47 files retained, 1 pinned only; acquire_source --check: PACKET_MATCHES_ITS_CONTRACT).

**Proposed intake-watch.yaml read** (for the records lane): read_through ad86d42d0f743076d735036702ba04a41ce24a8c, read_on 2026-10-12, no bead (the packet pins the head and retains the claim paths; the read covers the commits' other paths). Text in the lane W scratch file intake-watch-reads.yaml.

Close when the records lane lands the read.

## Notes

GitHub issue: https://github.com/jlevy/squares/issues/545 (opened 2026-10-12 by the coordinator to track this watched-repository read).
