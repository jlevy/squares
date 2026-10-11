---
type: is
id: is-01m3xrx8b86kp8t1k6gj71p4ej
title: "Reply on #295 (T-007, Nagamochi Lemma 1 false): the follow-up after PR #305's register change"
kind: task
status: closed
priority: 1
version: 13
delegate: claude-code@vm
labels:
  - result-import
  - packing
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
hold: null
hold_until: null
created_at: 2026-10-02T07:40:23.784Z
updated_at: 2026-10-06T22:27:20.726Z
started_at: 2026-10-05T03:21:49.383Z
closed_at: 2026-10-06T17:02:06.742Z
close_reason: "Done and on main via #382 (d087422ed); reply posted 2026-10-06 and recorded"
resolution: null
duplicate_of: null
---
J. PR jlevy/squares#305 (session-168) reviewed T-007 and changed the register; it merged on 2026-10-04. Lemma 1 is false for every a > 3, b > 2 (Karakus family, exact). T-007 is at V0/C1 with the defect recorded, the 287 verified floors that rested on it are re-derived (D-516), and T-083 to T-086 are registered. This bead answers #295. Note for the 2 October stack: verified lower bounds raised by replayed rectangle certificates removed T-007 from 17 more counts (46 operative left then).

## Replies due on #295 (2026-10-02)

Answer jlevy/squares#295 (wand125, opened 2026-10-02): T-007 (Nagamochi 2005): Lemma 1 is false; published counterexamples and replacement results

Replies due, from `python -m devtools.check_requests --report` on 2026-10-02:
- an acknowledgement: nothing has been posted on this issue
- lemma1-false: T-007 at V3/C1, E-nagamochi-lower (verified, external): open, and no reply has said so
- karakus-2026: an acknowledgement; not yet imported
- chelokot-2026: an acknowledgement; not yet imported

Closeable now: no: lemma1-false is open; karakus-2026 is queued; chelokot-2026 is queued; asked: Re-derive the 63 operative values T-007 supplies from the replacements or stronger results.
Close condition: The record holds the Lemma 1 defect against T-007, the values it supplies are re-derived, and the two replacement sources are registered or declined.

Sequence: once the pull request holding the ids above is on main, from packing/ on main run `uv run --frozen --all-extras --group dev python -m devtools.check_requests --draft 295`; the owner posts it (or an agent at the owner's request); record the comment's URL, date, kind and reported state under the issue's `replies` in packing/campaign/result-requests.yaml; rerun --report and close the issue with a final comment when it says closeable. Import beads: think-bmze.

## Notes

2026-10-05 (intake triage, think-nkzt): #305 merged on 2026-10-04 and think-yl2j closed on 2026-10-03, so the dependency is removed and the description is current. A reply is due. On origin/main d54cba554, check_requests --report finds that the 2026-10-04 follow-up gave T-007 as V3/C1, reviewed, and it is now V0/C1 with the defect recorded. Since that reply, T-085 and T-086 are confirmed and T-083 and T-084 are reviewed. The draft below is check_requests --draft 295 rendered on that commit. Re-render it on main before posting, post it on the owner's word, then record it under #295's replies in result-requests.yaml. #295 stays open after this reply while karakus-2026 is open: T-083 and T-084 at C1 need a replay of Proposition 5.1, and no bead names that replay yet.

## Draft reply on #295 (not posted)

Where this request stands in the record on `main`.

**Corrections to earlier replies.**

- The reply of 2026-10-04 gave T-007 as V3/C1, reviewed; it now reads V0/C1, incomplete.

**What is registered.**

- Nagamochi 2005, Lemma 1 is false, so the published proof of Theorem 2 is incomplete: the record holds this defect.
  - T-007, a defect is recorded against it: the read of 2026-10-02 found a defect in E-nagamochi-lower, and no replay here has passed.
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-nagamochi-lower, a defect is recorded against it: the read of 2026-10-02 found a defect.
  - E-nagamochi-lemma1-counterexample, confirmed here: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
- Karakuş, arXiv:2609.37410: s(k^2 - 1) = k for every k >= 2, and s(N) >= 1/2 + sqrt(N - floor(sqrt N) + 1/4) for every nonsquare N >= 8:
  - T-083, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
  - T-084, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
- chelokot, s(n^2 - 2) = n for every n >= 2, kernel-checked in Lean:
  - T-086, confirmed at V3/C3: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-chelokot-square-minus-two-lean, confirmed here: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).

**What is still queued, and how it will be completed.**

- T-083: C2 and above need a replay: a machine check of Proposition 5.1, that every square of side in (1, 1.01] gets more than one from the strip measure, over its three-parameter pose space. A stronger floor at any n is a new result, not a rung change.
- T-084: C2 and above need a replay of the lower half: a machine check of Proposition 5.1, or a replay of chelokot's Lean proof of the same family by an augmented measure, which is reported and was not built here.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`packing/frontier/STATUS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/STATUS.md).

This issue stays open while anything above is queued, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-05 after PR 353 merged (62f81e3a6): reply draft for #295 rendered by `check_requests --draft 295` on main. NOT POSTED; awaiting the owner.

Where this request stands in the record on `main`.

**Corrections to earlier replies.**

- The reply of 2026-10-04 gave T-007 as V3/C1, reviewed; it now reads V0/C1, incomplete.

**What is registered.**

- Nagamochi 2005, Lemma 1 is false, so the published proof of Theorem 2 is incomplete: the record holds this defect.
  - T-007, a defect is recorded against it: the read of 2026-10-02 found a defect in E-nagamochi-lower, and no replay here has passed.
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-nagamochi-lower, a defect is recorded against it: the read of 2026-10-02 found a defect.
  - E-nagamochi-lemma1-counterexample, confirmed here: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
- Karakuş, arXiv:2609.37410: s(k^2 - 1) = k for every k >= 2, and s(N) >= 1/2 + sqrt(N - floor(sqrt N) + 1/4) for every nonsquare N >= 8:
  - T-083, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
  - T-084, reviewed: its argument has been read here and no blocking defect found, and no replay here has passed yet (V3/C1).
- chelokot, s(n^2 - 2) = n for every n >= 2, kernel-checked in Lean:
  - T-086, confirmed at V3/C3: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).
  - T-085, confirmed at V3/C3: re-verified here by an independent implementation (devtools.check_nagamochi_lemma1_counterexample).
  - E-chelokot-square-minus-two-lean, confirmed here: reproduced here with the author's own checker (The source's Lean development (formal/), built by lake at its pinned toolchain, devtools.replay_chelokot_lean).

**What is still queued, and how it will be completed.**

- T-083: C2 and above need a replay: a machine check of Proposition 5.1, that every square of side in (1, 1.01] gets more than one from the strip measure, over its three-parameter pose space. A stronger floor at any n is a new result, not a rung change.
- T-084: C2 and above need a replay of the lower half: a machine check of Proposition 5.1, or a replay of chelokot's Lean proof of the same family by an augmented measure, which is reported and was not built here.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`packing/frontier/STATUS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/STATUS.md).

This issue stays open while anything above is queued, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-06 (lane R6, after the review): a reply is due once R6 merges. On the lane branch, #295 is closeable with a final comment. Re-render the reply with check_requests --draft 295 from main, then close the issue. The lane's draft, not posted:

@wand125, the last open item here is done, so this closes the issue.

**Corrections to earlier replies.** The reply of 5 October gave T-083 and T-084, Karakuş's results, at V3/C1, reviewed. They now read V3/C3, confirmed.

- **Karakuş, arXiv:2609.37410.** T-083 (Corollary 6.2, every nonsquare 8 ≤ N ≤ 324) and T-084 (Corollary 1.2, s(k² − 1) = k, held here for k = 3 to 18) are confirmed, independently re-implemented. Proposition 5.1 is the step the rectangle bound rests on: the strip measure gives the interior of every square of side in (1, 1.01] more than one. It is decided here by [`check_karakus_strip_measure`](https://github.com/jlevy/squares/blob/main/packing/devtools/check_karakus_strip_measure.py), an exact branch and bound over the square's orientation, side and the height at which the strip's line cuts it. The checker splits the cases its own way, by which strip lines cut the square, so the paper's Lemma 5.2 is not used and stays read. The cover is 5,939 boxes in exact rational arithmetic, retained and replayed box by box. It is tight at one pose: the axis-parallel square on the container's floor, where the measure is 1 + (λ − 1)(λ + ½). The four boxes there close by an exact expansion in λ − 1. Three mutated measures are refused, each with a counterexample. The steps that stay read are elementary: the reduction of a square's measure to its vertical profile, the case symmetries, and Theorem 1.1's scale-and-sum. A [separately prompted review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-06-karakus-proposition-5-1-machine-check.md) accepted the check, with non-blocking findings since addressed. It re-checked the reduction, scored 271,932 squares exactly with its own evaluator and found none at or below one, and assessed V3/C3 for both results.
- **Nagamochi's Lemma 1** is unchanged since the last reply. T-007 records the defect at V0/C1, and T-085, the finding, is confirmed at V3/C3.
- **chelokot** is unchanged. T-086, s(k² − 2) = k, is confirmed at V3/C3, reproduced here with the author's own checker.

The close condition holds: the record holds the Lemma 1 defect against T-007, every value it supplied is re-derived, and both replacement sources are registered and confirmed. Thank you for the report.

On `main`: [`RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md).
