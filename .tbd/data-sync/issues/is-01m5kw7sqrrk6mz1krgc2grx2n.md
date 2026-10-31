---
type: is
id: is-01m5kw7sqrrk6mz1krgc2grx2n
title: Replay sqverify_continuous v4 on T-145's and T-157's densities (the second route for the continuous cover)
kind: task
status: in_progress
priority: 2
version: 6
delegate: bold-ritchie-l10
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:57:34.328Z
updated_at: 2026-10-31T23:43:38.345Z
started_at: 2026-10-31T20:02:09.390Z
---
The second route for the continuous cover of T-145 and T-157: a complete run here of wand125's sqverify_continuous, reviewed on 23 October 2026 (think-xzob; docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md) with no blocking or major finding. A replay moves the cover's mark to independently re-implemented after reading the producer's code, and no rung.

## Validation
- Claim: s(40) > 1340000/199529 (T-145, Hosono's rect_n40_L67 density at core 199529/200000) and s(40) > 3359/500 (T-157, Guzhou0806's 685-orbit density at core 3350/3359), tau 4999/5000, each by sqverify-fast --continuous v4 (source_sha256 619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5; packet wand125-sqverify-continuous-v4-2026-10-12, whose search is v3's text, packet wand125-sqverify-continuous-v3-2026-10-12). The source reports both VERIFIED at v3 with no receipt (README: 110,877,174 and 118,717,888 nodes).
- Run: in the v4 packet's crate, `cargo build --release --locked` (binary 31936c4dcfac398b729990f51820fd5a5b70e23a2e809b71de1ca5864e6de618); `review/programs/candidates.py` writes c6715.json, c6718.json and their mass controls from this repository's copies of the densities in the source's row order; then `sqverify-fast --candidate c6715.json --n 40 --continuous --core 199529/200000 --tau 4999/5000 --threads 2 --max-nodes 30000000 > c6715.jsonl`, the same for c6718.json at --core 3350/3359, both mass controls, and a counted oblique control (a mutant that keeps the axis patch and is refused at an oblique root by an exact capture below tau); judge each with `review/programs/judge_run.py` and the totals against the README's rows. Never pass --resume a file this run did not write (review finding SC-1).
- Cost: about 0.66 and 0.71 CPU-hours by this host's rate on the B = 3348/3359 control of 23 October (12,364,148 nodes in 266 CPU-s, about 46,000 nodes a CPU-second, load 21 to 24); high 2.39 and 2.78 CPU-hours by the source's six-thread walls (1,167 s and 1,355 s) times 1.23, the ratio the n = 28 sample measured. Mass controls about 2 CPU-s each, measured; the oblique control is not yet priced.
- Budget status: gated on decision: within the owner's 40 CPU-hour item cap, but the continuous-angle replay waits for the budget line the owner sets on #543.
- Possible subset under the cap: the whole run fits; a subset of roots is a diagnostic only.
- Depends on: think-xzob's review (done); the owner's budget; the design of the counted oblique control.
- Done when: both runs VERIFIED with every root a complete binary cover (nodes = 2 leaves - 1) at or above tau, inherited_roots 0, totals equal to the README's, the controls refused at legal poses with exact captures below tau, receipts retained in the v4 packet, and replayed-here evidence registered for T-145 and T-157 with relationship_to_generator independent-implementation (clean_room false, the author having read the producer's kernel), noting what it shares with V-sqverify-fast.
- Machine note: CPU-bound, tens of MB resident; at --threads 2 it shares a four-core host with a gate; node counts do not depend on the thread count.

## Notes

2026-10-23 coord-intake-1023: #533 status reply posted at 17:27Z after verifying the deploy (data revision c32b44, which includes #752): https://github.com/jlevy/squares/issues/533#issuecomment-6370778184. It is in the third person, since #533 is the owner's tracking issue. It names this bead and think-0arj as the queued replays, waiting on #543. To be recorded under #533's replies in result-requests.yaml in the next records change (#753 on merge day).

2026-10-31 bold-ritchie-l10 (intake lane L10, epic think-3guf; branch claude/bold-ritchie-xo28us-l10, PR #865). Basis: the pass's 40 CPU-hour item cap (L6's triage, think-ztcy, class f); #543's unticked budget line predates the cap.

**Done.** Built v4 from the packet in scratch with rustc 1.98.0: binary 31936c4d..., the recorded digest (25.6 s wall). candidates.py rebuilt c6715.json f4a1ae9b... and c6718.json 38e0eff1..., the review's digests. Runs at --threads 2 --max-nodes 30000000, no --resume, each judged by the review's judge_run.py with every check held:
- c6715 (T-145, core 199529/200000, tau 4999/5000): VERIFIED, 86/86 roots and the patch (min 0.99988263), 110,877,174 nodes (the README's), least bound 0.9998000000015764, inherited 0; 3,143.9 CPU-s, 1,624 s wall.
- c6718 (T-157, core 3350/3359): VERIFIED, 86/86 and the patch (min 1.00149865), 118,717,888 nodes (the README's), least 0.9998000000075916; 4,746.8 CPU-s, 2,448 s wall.
- Mass controls (x 985/1000): REFUSED, 86/86 legal refutations each, 7,714 and 5,979 nodes, least captures 0.98711 and 0.98648.
Receipts and outputs: packing/resources/web/wand125-sqverify-continuous-v4-2026-10-12/replay/ (README, receipts/, runs/; every output's SHA-256 equals its run receipt's). Registered E-n040-wand125-sqverify-continuous-6715-replay and -6718-replay (replayed-here, independent-implementation, clean_room false via V-wand125-sqverify-continuous); T-145 and T-157 cite them and their mark derives as independently re-implemented after reading the producer's code; no rung moves. #485's continuous-angle result maps to T-157; #533's ask is done.

**Oblique control design: the threshold shift does not work for these densities.** Each claim's own candidate at a threshold just below its patch's minimum (budget 4,000,000 a root): c6718 at tau 1 VERIFIED (124,136,598 nodes, least 1.0000000001, 4,935.5 CPU-s); c6715 at tau 24997/25000 VERIFIED (113,317,246 nodes, least 0.99988000008, 3,156.5 CPU-s); both judged faithful. A threshold shift equals scaling every weight, and both densities are tightest at or near the axis: c6715's least oblique capture is within 2.6e-6 of its patch minimum, c6718's is in [1, 1.00149865]. **What remains (this bead):** a counted oblique control by a density mutant that lowers oblique captures alone (e.g. weight moved off rows only tilted squares rely on), checked exactly to keep the patch, then run and judged; and whether the 23 October review joins T-145's and T-157's reviews (for T-157 it would be the second adversarial AI review toward rung 4) is the PR review's call. Lane compute: about 4.5 CPU-hours.

**Drafted replies, to post after #865 merges and its deploy verifies** (render with check_requests --draft 485 / --draft 533 from main first; footer per house style):
- #485 (answer bead think-3oi5; reply due): T-157 and T-145 stay V3/C3, confirmed; wand125's sqverify_continuous v4 was run here in full on both densities (110,877,174 and 118,717,888 nodes, the README's totals, mass controls refused at every root), so both now read independently re-implemented after reading the producer's code; the continuous-angle report maps to T-157; not a second method. check_requests --report marks #485 closeable after merge.
- #533 (answer bead think-flxm; third person, owner's tracking issue): the ask is done (retained, reviewed, built, both examples replayed with mass controls; receipts in the v4 packet's replay/); the counted oblique control stays with think-flxm; closeable after merge.
