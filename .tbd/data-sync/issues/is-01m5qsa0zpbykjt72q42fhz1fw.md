---
type: is
id: is-01m5qsa0zpbykjt72q42fhz1fw
title: "Import #797: Kevin Fang's c*(k) < 4√(2k)+1 for every k ≥ 6 (squarepack-certs theorem-a at b1b3f6b)"
kind: task
status: in_progress
priority: 2
version: 14
delegate: c-import-797-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5rbw9b5qbj55pjw1pewd6b2
  - is-01m5rbwekd4y8cvxgnqx3xdsj1
  - is-01m5rewz05vzetqmgbmhz9ch93
hold: null
hold_until: null
created_at: 2026-10-24T20:23:19.286Z
updated_at: 2026-10-25T02:49:50.326Z
started_at: 2026-10-24T20:24:12.105Z
---
New 2026-10-24 issue https://github.com/jlevy/squares/issues/797 (TheSnakeFang, 18:52:48Z): for every k >= 6, k^2 - ceil(sqrt(32k)) - 1 unit squares fit in a square of side < k, so c*(k) < 4 sqrt(2k) + 1. Ryu's L packing (Theorem 1.3) with filled band ends, b the odd integer nearest sqrt(2k); a 5-page note. Source TheSnakeFang/squarepack-certs@b1b3f6b theorem-a/ (note PDF+TeX, lband.py exact construction, windowed_check.py, certificates k=6..40 and 101, SHA-256 for k=300 and 600 with regenerate.sh). The repository head db1ed62 (3 commits past the last read) adds note v0.2 crediting Evan Daniel's earlier bound (doi:10.5281/zenodo.23624565): read for priority and credit. Bears on the deficiency rows (Ryu's Theorems 1.2-1.4, T-163). Stage 0 owner; stage 1 triage is read-only first. Source claims are unverified.

## Notes

2026-10-24 stage 1 triage (c-triage-797-1024, read-only, main 84d4a75af).
Pin: squarepack-certs db1ed6220731fce432fa3b1ef3b994b5ab6c3663 (head; theorem-a code/certs byte-identical to b1b3f6b; note v0.2 = Zenodo 10.5281/zenodo.23624565, v0.1 = 23624412 = note at 31bdc2d). Correction: 23624565 is Fang's own v0.2, not Daniel's; Daniel's bound is evand/square-packing 4b456fe/aa12b98 (pushed 2026-10-18T15:47:56Z), held by think-f8py (stalled in_progress since 10-19), not registered.
Claim map: theorem-a -> new reported row in asymptotic-waste-bounds deficiency_upper_bounds (no T-NNN; settles no n <= 324, #471 precedent); 36 certificates -> retained + replayed, no rows (every count <= 1024 already below k in the record); optimized constructions -> prose only, not registered.
Checked: independent exact re-implementation from the note: bound holds k=6..60000 (both b at ties), Lemma 2 and B(k) hold; full geometry valid k=6..40,101; controls refused k=6..30; least slack 8019401/78023840599 at k=19705 reproduced; all comparison claims hold exactly (Ryu 1.2/1.3/1.4/1.6, T-163, Daniel counts 495210/255215/249568).
Consequence: adding the row forces deficiency_family Statement + T-163 assessment recompute ([15,41]; with Daniel [15,34]u[36,39]).
Price: cert replay 15-45 CPU-min (36 shipped); k=300/600 1-2 CPU-h, recommend skip; stage 4 review tbd-strong-max ~150-250k tokens; maintained module W7 ~100-150k tokens.
Drafts: scratchpad triage-797/ result-requests-797.yaml, import-plan-797.md, acknowledgement-797.md, intake-watch-squarepack-certs.yaml (schemas validate).

2026-10-24 coord-intake-1024 on c-triage-797-1024's report: decided by stated rules, not owner questions. (1) Theorem A gets its own reported row in deficiency_upper_bounds, credited after Daniel (his c*(k) <= 4 ceil(sqrt(2k-7)) - 1, 4b456fe, pushed 2026-10-18T15:47:56Z, came first; the axis-row fill is his; neither bound dominates per k). (2) Daniel's row (think-f8py, stalled since 19 Oct) lands in the same change. (3) T-163's assessment is recomputed as the deficiency gate requires. (4) k = 300 and 600: author's hashes only; the 36 shipped certificates replayed. (5) Theorem A's construction check promoted to a maintained module (OR-1). Lane c-import-797-1024, worktree wt-797, branch claude/intake-2026-10-24-deficiency-797. Fang's stage 4 note review follows in its own lane once the PR is open. Correction: doi 10.5281/zenodo.23624565 is Fang's note v0.2, not Daniel's bound.

2026-10-25 import (c-import-797-1024), draft PR https://github.com/jlevy/squares/pull/801 (labels intake, S2), branch claude/intake-2026-10-24-deficiency-797, head 7fff8acc7 (main 755ef426b merged). Theorem A is a reported row of frontier/asymptotic-waste-bounds.yaml deficiency_upper_bounds, key [Fang Theorem A 2026-10-24], credited after Daniel's row (think-f8py, same PR); no T-NNN. Packet packing/resources/web/fang-theorem-a-2026-10-24/ (theorem-a/ at db1ed62, both Zenodo records). Maintained check cases/asymptotic/fang_theorem_a.py (bound 6..60000, identities, geometry 6..40 and 101, sharpness, certificates) with tests/test_fang_theorem_a.py. Replay: 36/36 certificates accepted on both routes, 216/216 filtered controls refused, 143/143 sharp controls (k <= 18) as expected; k = 300/600 recorded as the author's SHA-256 only. T-163's assessment recomputed by deficiency_family: smallest [[15,34],[36,39]], tied [[34,34],[39,39]], as the triage said. Significance draft S2 (Daniel's row arguably S3; the reviewer decides). Remaining: stage 4 review of the note (its own lane); the stage 7 acknowledgement below, to post after the merge.

Stage 7 acknowledgement draft for #797 (post after #801 merges; names no T-NNN):
Thank you, Kevin. We have received Theorem A and your correction on priority, and the record now holds it.

**What we pinned.** `theorem-a/` in TheSnakeFang/squarepack-certs at the head, `db1ed6220731fce432fa3b1ef3b994b5ab6c3663`. Its code, certificates, `LARGE.sha256` and `regenerate.sh` are byte for byte those of `b1b3f6b`, which the issue names. Its note is v0.2, and the PDF and TeX are identical to the files of [10.5281/zenodo.23624565](https://doi.org/10.5281/zenodo.23624565). We also keep v0.1 ([10.5281/zenodo.23624412](https://doi.org/10.5281/zenodo.23624412)).

**How it is recorded.** Theorem A is a reported row of the asymptotic register's deficiency bounds, `c*(k) ≤ ⌈√(32k)⌉` for every k ≥ 6, credited as an independent second proof after Evan Daniel's `c*(k) ≤ 4⌈√(2k − 7)⌉ − 1` (k ≥ 7, in Lean, evand/square-packing `4b456fe` and `aa12b98`, 18 October). Daniel's bound came first and has its own row just before yours; the axis-row fill of the band ends of Ryu's L is his idea, as your v0.2 says. Per k neither integer bound is always the smaller, which is why both rows stand. Since the theorem settles no count up to 324, it is not a numbered result.

**What we checked.** We wrote the construction afresh from the note, in exact rationals, without running or consulting `lband.py`:

- For every k from 6 to 60,000, at both odd widths where there are two, it packs k² − w squares in a side below k with w < 4√(2k) + 2, and Lemma 2 and B(k) < 4√(2k) + 2 hold. The least B(k) − w for k ≤ 20,000 is 8019401/78023840599 at k = 19,705, as the note states.
- The identity behind B(k) < 4√(2k) + 2, 6b⁴ − b³ − 2b² − b, and Lemma 2's value at t = 1/b hold exactly.
- At k = 6 to 40 and k = 101, every square is inside the box and no two overlap. Mutated layouts are refused, and the waste is exactly 4b at k = (b² − b + 8)/2.
- Your 36 shipped certificates are accepted by this repository's two exact routes, over every wall and every pair whose centres are closer than √2, and all six controls of each are refused by both; at k ≤ 18 the sharp controls, at contact and 10⁻³⁰ past it, behave as expected.
- Your comparisons hold in exact integers, including the counts of 495,210, 255,215 and 249,568 against Daniel's bound below 10⁶.

**What comes next.** The note gets a mathematical review, and we will reply here when it lands. Daniel's Lean proof is recorded as reported until it is built here.

Two questions, neither of which holds anything up:

1. Will you publish the optimized constructions of section 6 as certificates? These are the waste of at most 4√(2k) + 1.18 for 15 ≤ k ≤ 300, the 9,946 squares below side 100, and the gains at k = 25, 30 and 40. For now we note them as stated and do not register them, as you asked.
2. Would you publish the k = 300 and 600 certificates, for example on the Zenodo record? Then they could be checked without rebuilding them. Until then we record their SHA-256 values as your statement.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

2026-10-25 01:50Z (c-import-797-1024): PR #801 head a3e826606, hosted CI green (packing-required and pages-required pass; runs 40151160097, 40151160004); still a draft. The first head 7fff8acc7 failed three tests in suites A and C (credits-project keys must name Levy; nine new credit spans resolved in contributors/occurrences.yaml; fang_theorem_a declared as a verified_upper_bound consumer), answered in a3e826606.

2026-10-25 coord-intake-1024: PR https://github.com/jlevy/squares/pull/801 (draft, intake, S2) at a3e826606, CI green (40151160097, 40151160004): Daniel's and Fang's rows, T-163 window [[15,34],[36,39]], fang_theorem_a.py, 36 certificates replayed, Daniel's Lean closure retained at aa12b98 (build: think-fqp6). Senior review A c-rev-801-1024 (think-3fbz) and the stage 4 review of the note c-review-797-math (think-qmqq, wt-rev797) running. The lane declined Daniel's junction variant at a435c97 (finite, not in Lean); review A checks it.

2026-10-25 (c-import-797-1024): review A of #801 (issuecomment-6392315606) addressed in one round, dispositions https://github.com/jlevy/squares/pull/801#issuecomment-6392419441; new head a716db43c (fixes 25f021693, re-pin a716db43c). Significance relabelled S3 by review A2 (supersedes the S2 draft above); News draft in the PR body. The stage 4 review of Fang's note is think-qmqq.

2026-10-25 coord-intake-1024: #801 merged (3e1349802, 02:35:38Z; S3 by review A, dispositions issuecomment-6392419441); Pages 40155040155 verified. #797 acknowledgement posted https://github.com/jlevy/squares/issues/797#issuecomment-6392638719; recorded by c-map-qmqq-1024 (think-vfz9) with the stage 4 review of the note (accept with findings). The review's six author questions follow after that PR merges.
