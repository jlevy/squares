---
type: is
id: is-01m5frzavxzvcqht1tf2edbfxp
title: "Import Evan Daniel: solved views below the record at 204, 227, 229 and 260 (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: coord-intake-1021b
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T17:43:33.500Z
updated_at: 2026-10-21T17:44:15.833Z
started_at: 2026-10-21T17:43:35.847Z
---
Stage 0 owner for four certificates Evan Daniel published, with no issue, in evand/square-packing at 0075967bace18a3deabcc0baa64c2fb294fc80a0 (committed 2026-10-20T02:36:12Z, "Site up to date: records at 183, 229, 308 (ours) and 204, 227, 260 (Couzo), certified and regularized"): search/regularize/lists/certs/n-NNN.cert.gz, each with n-NNN.json.gz beside it. Found by the read-only triage of the 21 October sweep (c-triage-sweep-1021b). Nothing has been retained, replayed or registered.

Claims (exact sides from the certificate headers, margins exact):
- s(204) <= 14808642840591493923068442871459/10^30 = 14.8086428405914939…, 1.389753e-9 below T-223 (Couzo, #678). JSON "by": Francisco Couzo.
- s(227) <= 7781812826162574542396221861851/(5*10^29) = 15.5636256523251490…, 1.710513e-4 below T-196 (de Winter, #668), and at least 1.68e-11 below anything the upward print 15.563625652343 of Couzo's #672 can stand for (think-2vjc, not registered). JSON "by": Francisco Couzo.
- s(229) <= 15650161513876431064009548865321/10^30 = 15.6501615138764310…, 1.912210e-11 below T-199 (Daniel, #674 update, the house). JSON "by": Evan Daniel; input "polished". The commit says: "229 after the slp2 polish, 2e-11 below the posted float: the exact optimum of the same packing".
- s(260) <= 4161438312629953048686574163329/(2.5*10^29) = 16.6457532505198121…, 2.514377e-11 below T-223 (Couzo, #678). JSON "by": Francisco Couzo.

Each JSON says "regularized display view of a certified packing at the same side; not a new bound", at level 2, "same packing: traversable without expansion". Each side is below the verified bound at n + 1 (205, 228, 230 and 261), so each bound is new by the regularization guide's test. At 183 and 308 the same commit's certificates equal T-220 and T-221 exactly, and at 153 and 207 the lists lie about 1.3e-19 and 1.5e-19 above T-174's algebraic sides (think-ot5c), so this import has nothing there.

Rule: the house rule ("a regularized view below the house best packing's side is a smaller packing") and docs/project/guides/regularization-process.md, Register Candidates (row 3): register it as a result, credit the packing's finder and the regularizer, validate it and adopt it. The precedent is T-146, Daniel's regularized lists at 15 counts with no issue. The report-order ledger reads a watched-repository publication from its first commit, here 2026-10-20T02:36:12Z. PR #706 lists the 204 and 260 views as register candidates deferred to the owner. PR #704 adopts T-196 at 227 and 260 and PR #706 adopts T-223 at 204 and 260, so this import's adoptions come after those two in merge order.

Plan and price: a stage 2 packet from 0075967 by devtools.acquire_source (the four .cert.gz and .json.gz files, LICENSE, CREDITS.md and the exact checkers, well under 1 MB); ledger rows at 204, 227, 229 and 260; a replay on both maintained exact routes with duplicate-square and outside-container controls (12 jobs, about 2 CPU-minutes, scaled from #702's 343 at 51.74 route CPU-seconds for 3 jobs); one batch result with a regularizations item per count, as T-155 was registered through devtools.register_regularized_bounds; a stage 4 review; then adoption with both strong generators at each count, about 0.2 CPU-h a count and 0.8 CPU-h in all, under the 40 CPU-h item cap. Credit: Couzo's packings at 204, 227 and 260 regularized by Evan Daniel, and Daniel's own at 229, in T-199's lineage. At 227 the packing's own report, Couzo's #672, is think-2vjc's and is not retained here, so the identity of the view with #672's packing is measured, not assumed. No issue asks for this, so the bead closes when the result is integrated.
blocked_on: none

## Notes

2026-10-21 coord-intake-1021b: created from the triage of the 21 October sweep (evand/square-packing 0075967). Disposition by the written House Rule and the regularization guide's Register Candidates (row 3): register the four views as one batch result through devtools.register_regularized_bounds, as T-155 did, crediting the packings' finders and Evan Daniel for the regularization; take it through stages 3 and 4; adopt and regularize each count once validated. No owner decision is needed: "No adoption waits for the owner's word" (result-import.md, The House Rule).
Order: one records PR after #704 and #706 merge (both change the houses at 227, 204 and 260). That PR also carries the intake-watch.yaml reads from the triage (scratchpad triage-1021b/proposed-intake-watch.yaml.patch, which names this bead on the 0075967 read).
Related: think-cvu0 and think-o4y3 (#704 review B6) hold Daniel's earlier solved views of T-196 at 227 and 260 (1.66e-8 and 1.81e-8 below T-196); the 0075967 views are smaller at both counts (1.71e-4 below T-196 at 227; 2.51e-11 below T-223 at 260), so those two close as superseded by this import once it registers.
blocked_on: jlevy/squares#706
