---
type: is
id: is-01m7c65j5dk876m77ftewkck4q
title: Review zmx2's area-density and first-order lemmas (Lemmas 1-3, K, K(d), U, V) for T-298's Valid11 (#973 review F1)
kind: task
status: open
priority: 2
version: 3
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-14T04:48:34.989Z
updated_at: 2026-11-14T08:13:53.822Z
---
Finding F1 of the stage 4 review of #973 (docs/project/reviews/review-2026-11-14-khalili-gharabaghi-k2m5-973.md, lane L144, think-h10k), held for the owner as a priced option: the record has never reviewed zmx2's area-density lemmas or its first-order lemmas, and T-298's 12,024 general-position roots of Valid11 rest on them.

## Validation
- Claim: zmx2 (evand/square-packing 659ee62, zmx2.rs e2bb84e9, retained in packing/resources/web/evand-square-packing-2026-10-04/) is sound in its --first-order mode with an area density: Lemma 1 (containment), Lemma 2 (cap), Lemma 3 (corners), Lemma K and K(d) (search/ZMX2_AREA.md sections 2 to 5 and 11.7), Lemma U per base cell and Lemma V (section 11), which certify every box meeting the Lebesgue square and every pose with 0 < theta < 0.014 degrees at a zero-limit germ. Daniel's own notes (sections 12 and 13) call U and V the least mature part and their self-audit the only reader. ZMX2_AREA.md at 659ee62 is byte-identical to the 4 October packet's copy.
- Run: an adversarial review lane at the strongest tier (tbd-strong-max, maximum reasoning), in its own worktree: re-derive each lemma, read zmx2.rs's area and first-order code paths against them, and run controls that break each lemma's premise on small covers (a polygon density lowered by 1e-6, a germ weight moved), each refused where the published board certifies; or, in place of the review, an independent decider for the tilted part of Valid11 (the record's sqverify family has no segment-and-polygon mode yet).
- Cost: one review lane, about 4 to 8 hours of agent wall at the strongest tier; under 1 CPU-hour of runs for its controls. Basis: the size of the material (ZMX2_AREA.md, 525 lines, of which sections 2 to 5 and 11 to 13 are the lemmas; the corresponding parts of the 4,342-line zmx2.rs) against the 2 October zmx2 reviews.
- Budget status: gated on decision (the owner's choice of review effort; the CPU is negligible).
- Possible subset under the cap: Lemmas U and V alone, the part the source's author calls least reviewed.
- Depends on: nothing; independent of think-0h7r's replay, which reruns the producer's code and would not close F1.
- Done when: a mapped review document reads the lemmas against zmx2.rs, with its controls retained and V-evand-zmx2's note updated; T-298's next_rung and the Valid11 report's external_review say F1 is closed or what remains.
- Machine note: the controls need zmx2 built from retained bytes (devtools.replay_evand_zmx2 build --checker e2bb84e9) and small covers; shares the host with anything.

## Notes

2026-11-14 06:55Z coordinator: #973 is answered and closed (T-298 merged in #974). This lemma review (review F1) is held for the owner's decision: one strongest-tier review lane, under 1 CPU-hour.
blocked_on: the owner's decision
