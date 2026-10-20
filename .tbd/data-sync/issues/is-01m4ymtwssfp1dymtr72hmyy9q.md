---
type: is
id: is-01m4ymtwssfp1dymtr72hmyy9q
title: "Validation (#610, think-ribz): zmx2 --full and zm_mixed.py on its failing roots for s(95), about 6 CPU-h, priced, gated on decision"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-15T02:04:08.377Z
updated_at: 2026-10-15T02:04:08.377Z
---
Priced validation item for the #610 import (think-ribz): the unreduced route, zmx2 cert --full over the whole pose space of the s(95) cover, with zm_mixed.py on the sub-roots its failing roots leave. Not run, by the coordinator's rule of 15 October: run it only if reaching T-184's rung for s(95) needs it.

## Why it is not run
T-184's rungs (registered 14 October, PR #602) cite E-bengreff-594-cover-report and E-basic-grid-upper, at V0/C0, and its next_rung names what C3 needs: the retained zmx2 and zm_mixed.py reproduction recorded as evidence, case 76 registered in devtools.replay_evand_zmx2 and devtools.audit_evand_mixed_covers, and a review of the cover, the composite over the D4 region and the wall segments. The #594 import bead (think-osvq) priced zmx2 --full as an optional second sweep, and result-import.md stage 4 says one complete replay is what C3 needs and a second route is recorded beside the rung. No separate 14 October rung review of T-184 was found on main or the open branches beyond PR #602's description, which records T-184 as reported and continues it in think-osvq. So by #594's precedent zmx2 --full is not needed for the same rung for s(95).

The other precedent differs: T-066's C3 replay for s(59) (E-n059-wand125-mixed-cover-zmx2-replay) ran zmx2 in both d4 and full modes, and its assumptions note that the D4 reduction for measures is proved in Lean upstream but not built here, which the --full sweep does not use. A stage 4 reviewer may ask for the same here; that is the decision this bead waits on.

## Validation
- Claim: s(95) >= 10, cover 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c at bengreff/s95-certificate dd7297d, retained in packing/resources/web/bengreff-s95-certificate-2026-10-15/. Checkers: zmx2.rs 6b7f0f79 built from retained bytes (binary cba78a9e), and zm_mixed.py ee3e2915 with bb89de15 and 640fe453.
- Run: the packet's receipts/programs/run_zmx2.sh with a full mode (zmx2 cert COVER --full --threads T --uncert-cap 200000 --log OUT/n95_zmx2_full_roots.log: 80,000 roots, pass 0 over [0,10]^2 and pass 1 over its mirror y -> 10 - y, four u bins each); then zm_mixed.py cert COVER --full --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 --nproc 1 with --cx-lo .. --u-hi on each 1/20 sub-root of every root zmx2 --full leaves, one job each; then a coverage check of the unreduced composite (no repository tool reads one; the author's check_coverage.py is D4-only), part of think-ribz's W7 slice.
- Cost: about 6 CPU-hours, an estimate. zmx2 --full about 8 x 293 = 2,350 CPU-s (0.65 CPU-h), by s(59)'s full/d4 box ratio of 8.04 and this replay's 293 CPU-s for the D4 sweep. zm_mixed.py on the failing roots' sub-roots: up to the 8 D4 images of the 19 failing roots, 8 x 304 jobs at 2,371 CPU-s per 304 (this host's measured replay), about 5.3 CPU-h; fewer if zmx2 leaves fewer images.
- Budget status: runnable (under the 40 CPU-h cap), gated on decision: not needed for T-184's rung; run if the stage 4 review or the owner asks for the route that avoids the D4 reduction.
- Possible subset under the cap: the whole item fits; zmx2 --full alone (0.65 CPU-h) is a cheap first step that shows how many roots zm_mixed.py would need.
- Depends on: the decision above, and the W7 slice for an unreduced composite coverage reader.
- Done when: every root of the unreduced pose space is certified by zmx2 --full or by zm_mixed.py on sub-roots that tile it exactly, read by a repository tool, receipts committed; recorded as a second route beside the rung.
- What it would raise: no rung by #594's precedent. It removes the dependence on the D4 reduction lemma, as T-066's replay did for s(59).
- Machine note: CPU only; zmx2 is multithreaded, run it at one or two threads beside other lanes.
