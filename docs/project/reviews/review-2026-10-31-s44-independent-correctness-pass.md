# Independent Correctness Review: Khalili and Gharabaghi’s `s(44) = 7`

**Date:** 2026-10-31. **Lane:** stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md#stage-4-validate) for
issue [842](https://github.com/jlevy/squares/issues/842), T-252, bead `think-1v4b` (epic
`think-3guf`). **Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at
maximum reasoning.
It ran as a separately prompted lane in its own worktree and shared no
context with the import lane that retained the source, replayed the checker and wrote
the first review.

This is the independent review of T-252. The first review,
[review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md](review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md),
was written by the import lane in a distinct pass that shared its context.
It says so, and it is not independent.
This one meets the runbook’s condition for stage 4: two lanes that share no context, the
review at the strongest tier, its findings written before it read the earlier review.

## How This Record Was Made

The review was posted as Review A on pull request
[851](https://github.com/jlevy/squares/pull/851#pullrequestreview-5721837491), a senior
engineering review with a dedicated correctness pass.
It was submitted on 31 October 2026 at 07:38:43Z against head
`e88b6e0b2dea3a5abe564ac2649da7f6aab78c21`, with base `main` at `3978a7f61`. Its finding
A2 noted that the record’s only stage 4 review was not independent.
It offered to serve as that review, and the pass coordinator chose that option.
The import lane then wrote this document and moved the reviewer’s programs and logs into
the packet, at
[`review/independent-2026-10-31/`](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/review/independent-2026-10-31/README.md).

The sections from [Summary and Verdict](#summary-and-verdict) on are the review’s own
text, edited only for layout:

- typography and line breaks;
- headings, set at this document’s level;
- some paragraphs set as lists, with their sentences split where a list needed it;
- links to the retained files;
- the eight findings about the pull request, summarized rather than quoted.

The review as posted is the authority where this copy differs.
Its eight findings are about the pull request, not the mathematics, and their
dispositions are on the pull request.

## The Reviewer’s Receipt

The reviewer’s `--d4` run printed this, kept in
[`outputs/d4_receipt.log`](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/review/independent-2026-10-31/outputs/d4_receipt.log)
between its start line (07:14:33Z) and its end line:

```text
D4: measure invariant under x->s-x and x<->y (exact)
# zmx2 cert hash=bd68795e5855deda mode=d4 atoms=grid depth=40 node_cap=20000000 kappa=1.5 K=30 region=x0-34,y0-34,bins0-3
cover: s = 7/1, 15525 points, 3912 segments, total 2199755099/50000000 = 43.99510198000
done in 119s wall: roots 4900 (missing 0), boxes 16792446, certified 8321795, empty 76878, uncertified 0, max depth 39, cpu 236s
VERIFIED-D4: every closed unit square in [0,s]^2 has mu >= 1 (D4-reduced sweep, all roots)
# exit 0 wall 119.099080740 s; end 2026-10-31T07:16:32Z load 3.02 2.78 3.28
```

Its root log, retained as `outputs/d4_roots.log.gz`, has SHA-256
`b09128e74a30da5285ac8c6e2a3421b39827fc68f97e0d82d5ae060bbf815865` decompressed.
The import lane compared it with `devtools.audit_evand_mixed_covers compare-zmx2`. It
has headers identical to `receipts/n44_zmx2_d4_roots.log` and to the source’s
`verification/logs/zmx2_d4.log`, and all 4,900 roots identical to each, `ms` aside.

## Summary and Verdict

**The mathematics stands.** Every closed unit square in $[0,7]^2$ captures mass at least
1 from a $D_4$-invariant measure of total $2199755099/50000000 < 44$. So 44 unit squares
do not fit in any side below 7, and the grid gives $s(44) = 7$.

- I replayed the reduced `zmx2` sweep myself from the retained bytes, with a binary
  whose digest equals the PR’s. Every root’s census is identical to the PR’s receipt and
  to the source’s log.
- Three controls of my own design are refused.
- The pin chain holds back to upstream GitHub.
- My reading of the logic matches the record: the reduction, the closed semantics, the
  $D_4$ fold, and the fact that interval certification is rigorous.

V3/C3, *confirmed, reproduced with the producer’s code*, is the right rung, and S3 is
the right score.

**Verdict: changes requested (2 blocking, both small); mathematics accepted.**

## Findings on the Pull Request

The review raised eight findings, summarized here:

| Finding | Severity | Subject |
| --- | --- | --- |
| A1 | blocking | The slow composite test pinned the rebuilt poster at 45 equalities; a rebuild now prints $s(44) = 7$ as well |
| A2 | blocking (process) | The record’s only stage 4 review was not independent. This document is the fix it offered |
| A3 | suggestion | The mixed-cover audit’s whole-cover path, which case 44 uses, had no test |
| A4 | suggestion | The pull request description had the largest blob, the full sweep’s CPU figure, the atlas test subset and the stage 4 row wrong |
| A5 | suggestion | The report entry’s review note announced F1 to F6 and described four |
| A6 | suggestion | `result/t-046.html`’s page ceiling grows with every result at T-046’s counts |
| A7 | suggestion | The explainer’s patch v0.4.33 may renumber at merge, and its first-published date must match the deploy |
| A8 | suggestion | The branch conflicted with `main` |

It also listed what not to fix:

- `verify2/src/main.rs` differs at `659ee62`; it builds another binary.
- Pinning v1.1, not v1.0, is right: the certificate is the same blob.
- `method: interval-certified` is the accurate label.
- The case record’s heading and its lower bound’s kind match the precedents.

## Correctness Pass

The timebox was about 2 h; the pass used about 25 minutes of wall, of which the `--d4`
sweep took 119 s. Everything ran on a shared 4-core host, at `nice 5`, with at most 2
threads.

### 1. Pin Chain, from Upstream

I fetched both upstreams into empty scratch directories, ran nothing from them, and
hashed files only.

- **`moh63-dev/s44-equals-7`.** `main` = `v1.1` =
  `b5b1bc9d7354a8f62efcb6b7abeb30d1eb576aaf`, and `v1.0` =
  `063c4d656212a7cf7cc0d104f2846f05b6b043c9`. `certificate/s44_cover_7.txt` is blob
  `6dc71a7c` at both, with SHA-256
  `c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0`. That is the
  issue’s digest, and the retained `.gz` decompresses to it.
- **The retained tree** equals `b5b1bc9`’s tree (`6a63c99e`) in all 212 files; only
  `.gitignore` is absent, as declared.
- **v1.0 → v1.1** edits `README.md` and `verify.sh` (the `zm_mixed` stage and an audit
  only), adds `zm_mixed_check.py` and `.gitignore`, and deletes `.DS_Store`. The `zmx2`
  pin `659ee62e4a9d39542a1146e8b011cc3ab6407ede` and the two `zmx2` commands are
  unchanged.
- **`evand/square-packing@659ee62`.** `verify2/src/bin/zmx2.rs` (`e2bb84e9e05938db…`),
  `Cargo.toml` (`4e0f078e…`) and `Cargo.lock` (`e1daec4d…`, no dependencies) are
  byte-identical to the retained copies.
  `src/main.rs` differs, which is benign.

### 2. Build and Replay

- **Build.** I assembled the crate by hand from the retained bytes, not through
  `replay_evand_zmx2`, and ran `cargo build --release --bin zmx2 -j 2` with rustc 1.97.0
  (`2d8144b78 2026-07-07`), 17.5 s. The binary’s SHA-256 is
  `d68a2e3540344a0e5ad8af33847e3c473b099cf922b150afd184cc715e038787`. That equals
  `receipts/n44_zmx2_build.log`’s, though it was built in another directory.
- **Run.** `zmx2 cert s44_cover_7.txt --d4 --threads 2 --log d4_roots.log` printed the
  receipt above. Exit 0, 119.1 s wall, host load about 3.
- **Census.** All 4,900 `ROOT` lines, every field but `ms`, are byte-identical to
  `receipts/n44_zmx2_d4_roots.log.gz` and to the source’s
  `verification/logs/zmx2_d4.log.gz`, under identical headers.
  The leaves (8,398,673) equal the internal nodes (8,393,773) plus the 4,900 roots, so
  the search forest closed with no uncertified leaf.
- **`--full`.** I did not re-run it, since `--d4` agreed.
  I read its retained root log with my own script: 39,200 distinct roots, 134,880,184
  boxes, 0 uncertified and 0 capped, every root identical to the source’s
  `zmx2_full.log.gz`.
- **Audit tool.** `devtools.audit_evand_mixed_covers check` is clean (s44 whole-clean in
  both modes, every root identical), 13 s.

### 3. Controls of My Own (None of Them the PR’s Orbit Drops)

| Mutant (SHA-256) | Change | Run | Result |
| --- | --- | --- | --- |
| `drop1pt` `7da2a210…` | the first point row, (0.6, 2.9) with weight 10026, alone, without its orbit | `cert --d4` | refused at the precondition: `ERROR: --d4: cover is not D4-invariant: point (2900,600) weight 10026 has no D4 image at (600,2900)`, exit 2 |
| `drop1seg` `46aa26b4…` | the first segment row, (1, 0.06)–(1, 0.08), alone | `cert --d4` | refused: `vertical line x=1000 density not matched by x=6000`, exit 2 |
| `scale99` `f5409e87…` | $W$ changed from $10^8$ to 101,010,102, so every mass is scaled by exactly $10^8/101010102 \approx 0.99$; still $D_4$-invariant, total 43.555 | `cert --d4` on root x18 y24 bin 1 (the $D_4$ image of the source’s float minimum) and on root x12 y14 bin 3 (the hardest root, 378,875 boxes) | NOT VERIFIED, 212 and 209 uncertified. The refused boxes’ float minima are 0.999222 at (1.846, 2.419, u 0.15619) and 0.999799 at (1.25, 1.45, u 0.43466), genuinely below 1. The published cover on the same two roots: REGION CLEAN (37,817 and 378,875 boxes) |

The first two show that `--d4` checks its own precondition, which is what makes the
reduced sweep sound on its own.
The third shows that a uniform 1% deficit is caught where the cover is tight.

The `scale99` logs and the published cover’s logs on the same two roots are in
[`outputs/controls/`](../../../packing/resources/web/moh63-dev-s44-equals-7-2026-10-29/review/independent-2026-10-31/outputs/controls/).

### 4. Exact Preflight of My Own

`exact_check.py` uses its own parser and `Fraction`s. It shares no code with
`sanity.py`, `zmx2`, `zm_mixed.py` or the audit tool.
It found:

- side 7, $D = 1000$, $W = 10^8$; 15,525 points, 3,912 segments, 0 polygons, no trailing
  rows;
- every weight positive, every coordinate in $[0, 7000]$, every segment axis-parallel
  with positive length, and all of them on the 12 interior grid lines;
- **total $2199755099/50000000 = 43.99510198 < 44$**, slack 0.00489802 (points
  117146551/10000000, segments 201752793/6250000);
- the point measure and the line measure (canonical step densities) **invariant under
  all 8 symmetries**.

As a self-check, it flags `drop1pt` and `drop1seg` as non-invariant and passes
`scale99`. `zmx2` does not itself check that the total is below $n$, since $n$ is not
one of its inputs. That premise therefore rests on the parsers.
Four of them agree: mine, the source’s `sanity.py`, the in-tree review’s and the audit
tool’s.

### 5. The Mathematics, Checked

1. **What the mixed cover format proves.**

   $\mu = \sum w_i \delta_{p_i} + \sum m_j \cdot (\text{length measure on } \sigma_j)/|\sigma_j|$
   is a finite nonnegative Borel measure on $[0,7]^2$. `zmx2` reads each segment weight
   as the segment’s total: `per = wt*(lc/len)`, with the line’s cumulative mass asserted
   equal to $\sum \mathrm{wt} \cdot \mathrm{lc}$.

   Suppose 44 unit squares with disjoint interiors fit in a square of side $t < 7$.
   Scaling by $7/t > 1$ puts squares of side $7/t$ into $[0,7]^2$, still with disjoint
   interiors. Their concentric closed unit squares $Q_i$ lie inside those interiors, so
   they are pairwise disjoint closed subsets of $[0,7]^2$. The cover gives
   $\mu(Q_i) \ge 1$, and additivity gives
   $44 \le \sum \mu(Q_i) = \mu(\bigcup Q_i) \le \mu([0,7]^2) < 44$, a contradiction.
   So no packing exists at any $t < 7$. $s(n)$ is attained (by compactness), so
   $s(44) \ge 7$, and the grid gives $s(44) \le 7$.

   Closed semantics is exactly what the argument needs: the closed $Q_i$ are the
   disjoint sets, and the closed square is the weakest case to certify.
   **“Side $< 7$” versus “$\le 7$” is handled right.** The cover excludes every side
   below 7 and correctly says nothing about side 7, which the grid attains.

2. **The $D_4$ reduction is sound for this $D_4$-invariant cover.**

   - `cert --d4` runs `check_d4` (`zmx2.rs:756-819`). It tests invariance in exact
     integers under $x \to s - x$ and $x \leftrightarrow y$, the generators of $D_4$,
     and dies otherwise; my controls show both refusals.
   - Rotations about $(7/2, 7/2)$ carry any centre into $[0, 7/2]^2$ and keep
     $\theta \bmod 90°$. The diagonal reflection keeps that quadrant and sends $\theta$
     to $90° - \theta$.
   - So $[0, 7/2]^2 \times [0°, 45°]$ is a fundamental domain.
     It lies inside the swept region $[0, 7/2]^2 \times u \in [0, 1/2]$, that is
     $\theta \le 53.13°$.
   - `--full` needs no invariance at all: its pass 1 sweeps `reflect_y` of the cover,
     covering $\theta \in [36.87°, 90°)$.
   - I re-checked the invariance independently (§4).

3. **Interval certification with the stated rounding yields a rigorous proof**, under
   conditions that hold here:

   - Every float operation on the decision path is a correctly rounded IEEE-754 binary64
     +, −, ×, ÷ or √ in round-to-nearest.
     Each result is widened one ulp outward with `next_down`/`next_up`, which is enough
     because a correctly rounded result is within half an ulp of the exact value.
   - Integers enter only below $2^{53}$ (asserted in `Iv::rat`), so every conversion is
     exact.
   - Chord endpoints go to the integer grid as `floor(next_down(v·G))` and
     `ceil(next_up(v·G))`, with $G = 1000 \cdot 2^{30}$ exactly representable
     (`glo`/`ghi`, `zmx2.rs:935-957`).
   - The only transcendental calls (`atan`) are in box display and diagnostics.
   - The float-only steps (`initial_candidates`, `pt_float_class`) only drop candidates
     or route them to the exact integer test (Lemma P). That can lower a bound, never
     raise it.
   - Rust neither contracts `a*b+c` into an FMA nor uses x87 on x86-64.

   What this does not establish is that `ZMX2.md`’s lemmas (C, Z, W, P, R, including
   R(iii)’s clamp) are right and that the code implements them.
   Neither is formally verified.
   Both are trusted as the 28 September and 2 October reviews derived them for
   `6b7f0f79`, along with the host’s hardware and compiler.
   That is the trust boundary the record states (`E-khalili-842-cover-replay`’s
   assumptions), the same as for T-052, T-053, T-062 and T-066.

4. **The checker version does not change the decision.** My own function-level
   comparison of `zmx2.rs` `6b7f0f79` and `92a4cfe8` against `e2bb84e9` finds this
   cover’s decision path unchanged:

   - `eval_node` → `mass_bound`, which is `segment_bound` when there are no rectangles
     and no `--first-order`;
   - `segment_bound_lines` + `frames` is the old `segment_bound` verbatim;
   - `family_bound_ex(…, &[])` is the old `family_bound` plus a skip test that an empty
     list makes vacuous;
   - `build_lines` is identical;
   - `build_cover`’s new grid-line loop yields $\lbrace 1, \ldots, 6 \rbrace$ at the
     integer side 7.

   This agrees with the in-tree review’s §6.1, which also ran `6b7f0f79` to an identical
   census.

5. **The record says exactly what was proved, at the right rung.**

   - **T-252:** kind optimality, claim $s(44) = 7$, with the “side below 7” argument and
     the $7 \times 7$ grid.
   - **V3/C3.** An interval-certified replay here, with certificate, replay command,
     passing status and named controls; the upper half is `E-basic-grid-upper`.
   - **The required phrase:** “confirmed, reproduced with the producer’s code”.
   - **`n-044.md`.** Proved; lower bound exactly 7, taken from
     `E-khalili-842-cover-replay`; the reduction stated for side $s < 7$, with the
     0.011% margin.
   - **Supersession.** T-090 and T-177 are superseded at $n = 44$ only.
   - **No higher rung.** V4/C4 are correctly not claimed.

   One wording nit needs no change.
   The claim’s “would capture at least 44” leaves out “in 44 disjoint closed unit
   squares, above the total 43.995”, which `n-044.md` says in full.

6. **F1–F6: I agree with all six.**

   - **F1:** confirmed, and answered in item 3.
   - **F2:** confirmed independently in item 4.
   - **F3:** my run also reaches depth 39 of 40. That is not a soundness question,
     because a box at the depth limit is reported uncertified (`run_root`).
   - **F4:** off the decision path, since `zmx2` decides the whole claim; I did not
     examine `zm_mixed.py`.
   - **F5:** my slack, 244901/50000000, matches.
   - **F6:** the reduction is elementary and re-derived in item 1, so the Lean proofs
     are not needed for this claim.

7. **Significance S3: I concur.**

   T-053 ($s(45) = 7$), T-062 ($s(60) = 8$), T-066 ($s(59) = 8$), T-184 ($s(76) = 9$)
   and T-191 ($s(95) = 10$) are all S3. Each is one linear-programming solve of Daniel’s
   method at a new count, and the source’s separation step is search, not proof.

   This result closes an open case, as T-066 did at the same score.
   It brings no new technique, family or disputed value (S4) and is not a central open
   case (S5).

**Verdict on the mathematics: $s(44) = 7$ is correct and correctly recorded at V3/C3,
confirmed, reproduced with the producer’s code.
I found no mathematical defect.**

### 6. Comparison with the In-Tree Review

Before writing my findings I had seen only the PR body and the two evidence entries,
which quote F1–F4 in a line each.
I read the review itself afterwards.
It is careful, and nothing in it contradicts what I found.
Its §3–§6 and my items 1–4 reach the same conclusions by separate routes.
My additions are:

- A1, A2 and A3;
- an independent build and replay;
- three controls aimed elsewhere: the $D_4$ precondition and a uniform scale-down;
- an exact preflight with no shared code;
- the pin chain checked against upstream GitHub rather than against the packet.

The programs I wrote are `exact_check.py`, `make_controls.py` and `fn_compare.py`, with
the `--d4` root log, its receipt and the control logs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
