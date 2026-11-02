---
type: is
id: is-01m4ce7h7xx85mb7345f5s8svx
title: "Answer Sungjoon Ryu: two asymptotic deficiency preprints (#414)"
kind: task
status: closed
priority: 2
version: 9
delegate: codex@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m4bxdtbvasjn91jwhz448s7b
hold: null
hold_until: null
created_at: 2026-10-08T00:22:22.715Z
updated_at: 2026-11-02T05:36:17.043Z
started_at: 2026-10-18T08:47:56.034Z
closed_at: 2026-11-02T05:36:17.043Z
close_reason: "#414 answered and closed: strongest-tier review accepted (#879, f54c74f6b); final comment issuecomment-6569593647 posted after deploy verified; recorded in https://github.com/jlevy/squares/pull/881 (7a4521582). Remaining: think-k3tk (Lemma 4.10 box labels)."
resolution: null
duplicate_of: null
---

## Notes

2026-11-02, lane L25 (bold-ritchie-l25): #414's final comment is posted and the issue closed. Posted at 05:11:12Z, https://github.com/jlevy/squares/issues/414#issuecomment-6569593647, after #879 merged (f54c74f6b) and its Pages run 41391360284 passed verify-deployment (job 125105691468, 6,036 of 6,036 checks). Rendered with check_requests --draft 414 from that main and reconciled with think-u1kq's L23 draft; a stray pair of backticks the post put around the receipts link was removed at 05:11:46Z, and the comment then read back identical to the draft. check_requests --report on main gave #414 closeable with a final comment; closed as completed at 05:11:58Z. The reply (kind final, beads [think-k3tk]) and the close are recorded in packing/campaign/result-requests.yaml on draft PR #881 (claude/bold-ritchie-xo28us-l25, labels intake + S1). Not closed here: the coordinator closes this bead after #881 merges and check_bead_tree --before-close passes.

## Stage 7 draft for the strongest-tier review, 2026-11-02 (think-yf8j, lane L23) — not posted

Ledger: post only once the review is merged (PR #879). On that branch (claude/bold-ritchie-xo28us-l23) #414's review ask is `done` with the verdict below, and `check_requests --report` reads #414 as closeable. So this is the final comment: from main, check it against `check_requests --draft 414`, which may add the closing sentence it expects, then post it and close the issue. This draft supersedes the 11 October draft further down, whose last paragraph ("The review request stays open under `think-6ptr`") is out of date. Links point at `main` and resolve once the branch merges.

@squarepacker, thank you again for both preprints. A second, fuller review of them is now in the record: [review-2026-11-02-ryu-quarter-cube-strongest-tier.md](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-11-02-ryu-quarter-cube-strongest-tier.md). It ran at our strongest review tier, and it wrote its findings before it read the review of 8 October.

**Verdict: accepted, for both preprints.** The quarter-power argument (Theorems A and A₁₃, Corollary A) and the cube-root argument (Theorems 1.1 and 1.2, Corollary 1.3) are complete as written, under the closed-set convention and [R, Lemma 2.1]. They are conditional on the lemmas you import from k2-minus-c v1.2. No finding is a defect or a gap; there are eight notes.

**What was checked.**
- Both chains, re-derived step by step, with the lemmas of v1.2 that they use, except two parts: the case analysis of v1.2's Proposition 4.5 was read and its numbers recomputed, and the box labels of its Lemma 4.10 were not decided (below).
- Every constant and threshold, recomputed in exact-rational interval arithmetic written for the review. It shares nothing with your scripts, none of which ran here. That is 193 values of the quarter-power paper and 95 of the cube-root paper, each in the direction your proofs need; the 57 and 24 of them that are displayed also hold in their displayed rounding.
- Your supplementary Tables 4 and 5 and the sensitivity record of Section 12.6, which nothing here had run before. They reproduce in full. For instance, condition (i) holds exactly from k* = 4,616,673,963,026.36…, and each tolerance in (a)–(f) is the largest admissible value, rounded down.
- The finite angle check that ends the proof of v1.2's Lemma 4.9, redone from the text. Every class sequence with sum 15 or more fails by more than 25.94°, and only (5,2,5,2) is feasible at 14.
- Your quotations of v1.2: 19 statements and 12 sentences, all v1.2's text, except that one quotation of its Remark 4.11 drops the emphasis on "all". Also the cube-root paper's 44 citations of the quarter-power paper.
- The cube-root liminf constants can be made explicit. Take τ₀ = 1/6, τ₁ = 1/6 − 10⁻⁶ and ν₀ = 10⁻⁵. Then conditions (i)–(iii) of your Proposition 5.1 hold at k_a = 10²⁴ for γ = 0.06285, and at k_a = 10²² for γ = 0.05229 with the analytic constants.

**Three questions**, from the review:
1. Would you state the all-pairs form of v1.2's Lemmas 4.9 and 4.10, which Proposition 2.1 of the quarter-power paper uses, as a lemma of v1.2 with its proof? v1.2's Remark 4.11 says it is not used in v1.2's proofs, while the quarter-power proofs use it.
2. Is github.com/squarepacker/k2-minus-c-power, named in the quarter-power README and in its verification status, the same repository as squarepacker/k2-minus-c-quarter?
3. Theorem A's threshold sits 7.2·10⁻⁴ above k*. Would you consider a threshold with more margin, or printing k* beside it?

**What it does not settle.** Theorem A, c_∞ and the cube-root Theorem 1.1 use the computer-assisted Lemma 4.10 of v1.2. Its box labelling has one implementation, which was replayed here with your programs. An independent labelling is still open, as `think-k3tk`. The Lemma 4.9 variants do not need it. This is one adversarial AI review, by a Claude agent, the system family your preprints were developed with. It confirms the chains at the level of a read, with the constants recomputed independently in the reviewer's own exact arithmetic. It is not a human peer review or oversight record. Neither theorem settles a count n ≤ 324, so the record gives them no result-register entry and no rung.

---
_Generated by [Claude Code](https://claude.ai/code)_

## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: not closeable (`check_requests --report` at c6bf2d46f: the review ask is queued under think-6ptr). Restates think-mtwe's 10 October draft from main; the facts are unchanged at c6bf2d46f (the ask note's stale "merge-readiness gates" clause, mtwe finding 4, is fixed on main). No register entry or site row is involved.

@squarepacker, thank you. Both preprints are imported on `main` as reported results in the [asymptotic waste-bounds record](https://github.com/jlevy/squares/blob/main/packing/frontier/asymptotic-waste-bounds.yaml), through [PR #439](https://github.com/jlevy/squares/pull/439). The papers and programs are retained at their v1.0 pins (abbedcf and 15045f9) with their licences.

**Why there is no register entry.** Neither theorem settles a count n ≤ 324, and those counts are what the result register covers. Both are recorded as reported, with their statements checked against your TeX.

**What was reviewed.**
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-08-quarter-cube-proof-chains.md), merged in [PR #441](https://github.com/jlevy/squares/pull/441), read both new proof chains in full and accepted them at source-review scope, conditional on the imported lemmas and numerical premises. It found no blocking gap.
- A second reviewer accepted this repository's own check of the deciding constants, `cases/asymptotic/quarter_cube_constants.py`. It evaluates them from the published formulas in interval arithmetic: 108 of 108 checks hold, covering both quarter-power parameter vectors and all eight cube-root ranges.

None of your programs ran here. Neither review is a human peer review, and no confirmation is claimed.

**What remains.** The constants that use the computer-assisted Lemma 4.10 of k2-minus-c rest on its box labelling. The independent re-implementation of that labelling is still open, as `think-k3tk`. The analytic Lemma 4.9 variants avoid it but keep Lemma 4.9's accepted finite angle enumeration. The review request stays open under `think-6ptr` until that is settled. This issue stays open while it is queued, and a reply follows each change in the record.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-18 W1 intake (think-xmxb): New watched source evand/square-packing 8475bdf41571c59c8c240aedaddc48e19e0e4707 formalizes Ryu c*(k)<=8ceil(sqrt(k-4))-1 for k>=6 (think-ahr2). a645fe3610425507ddfb9825045094028c1d28f4 adds improved c*(k)<=4ceil(sqrt(2k-7))+5 for k>=7 (think-f8py). These are separate new import lanes, not completed #414 review or consent to source execution. Coordinates retained in W1 audit.
