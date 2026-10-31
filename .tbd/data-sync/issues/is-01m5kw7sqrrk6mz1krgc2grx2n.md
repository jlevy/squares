---
type: is
id: is-01m5kw7sqrrk6mz1krgc2grx2n
title: Replay sqverify_continuous v4 on T-145's and T-157's densities (the second route for the continuous cover)
kind: task
status: in_progress
priority: 2
version: 3
delegate: bold-ritchie-l10
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T07:57:34.328Z
updated_at: 2026-10-31T20:02:09.390Z
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
