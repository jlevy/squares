# Mathematical Review: wand125’s Fine-Net Lower Bounds at n = 28 and n = 30

Reviewed on 2026-11-04 from these inputs, all read as data:

- the packet
  [`wand125-fine-net-n28-n30-2026-10-10`](../../../packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/README.md),
  as retained on branch `claude/bold-ritchie-xo28us-l42` at `7ccb06b3c`, with each
  release asset’s six data members under `release/`;
- the two release assets of `square-lower-bounds-v1`, fetched again and held to the
  packet’s size and SHA-256 pins;
- each certificate directory’s four pinned documents, fetched at the pinned revisions
  and held to the manifest’s digests.

It covers `T-142` and `T-143`.

The reviewer is an AI agent, Claude (Anthropic), at the tbd-strong-max tier with maximum
reasoning, acting as the stage-4 mathematical reviewer of record (bead think-4ul6) for
the import think-i85v. The lane worked in a worktree of its own and shares no context
with the intake or replay lanes.
It executed no program of the source.
The one program it ran that it did not write is this repository’s reviewed
`sqverify-fast` (crate source `d97758bb…`), which it built in its own worktree to binary
`567a0fd5…`.

Nothing was posted, and the author was not contacted.
This review registers nothing and moves no bound.

## Summary for the Author

**The two bounds.** wand125/square-packing published them on 10 October 2026, at
`36b85b9` and `ff9f269`, and no issue reports them:

- $s(28) \ge 2297/400 = 5.7425$, by `mixed_n28_L57425`;
- $s(30) \ge 2357/400 = 5.8925$, by `mixed_n30_L58925`.

Both are check2 certificates on the 2,073-direction declared net, of core $4999/5000$
and step $1/5002$. The measures have masses $2799999/100000$ and $2999999/100000$.

**What was recomputed here.** All of it was done in exact arithmetic, by code written
for this review and apart from every checker:

- the two measures and their masses, and the digests;
- the net and lemma N0’s premises, the last bin, and the per-bin domain at all 2,073
  nodes;
- lemma F3’s caps;
- your run logs: every direction, the sums, the premises, the embedded summaries;
- your check2 and pre-publication receipts, and `bundle.json`;
- all 62 oblique witnesses of your two 197/200 controls;
- the exact capture at the leaf boxes of the 12 tightest directions of each run;
- direction 0 of each certificate, decided over its whole per-bin domain by a method
  that shares nothing with the crate’s.

This repository’s reviewed `sqverify-fast` was also run at 12 further directions, among
them the least-bound ones.
It reproduced your per-direction records exactly, in node count, leaves, depth, least
bound and least-bound box.
It refused the 99/100 mutant at six directions, with witnesses this review’s evaluator
confirms.

**The verdict.** No step read here is false.
Neither certificate has a blocking or major finding.

- The argument from each certificate to its bound is lemma N0’s, on the declared net
  (§2), and every premise an instance must meet holds for both.
- The coverage itself is decided by your runs.
  It is sampled here at seven directions of each certificate: direction 0, decided by
  independent code, and six run with the reviewed crate.
  The intake lane reports eight more of each, direction 0 among them, as matching your
  log. A complete replay has not run here.

Each certificate is therefore **accepted with findings**, as a reported result in the
record’s vocabulary.
The findings are minor or notes, all in the bundles’ documents and the record, none in
the argument or the data.
The review supports `C1` once it is recorded, and the bound stays at `V0` until the
census runs.

**Six matters for you** (§§7 and 8):

- the bundles’ `SOUNDNESS.md` predates the declared-net lemma their reader relies on;
- the README names a control file that does not exist;
- the published receipts were written by a program the bundle does not ship;
- the “pre-publication check” is not a second recorded run;
- the verifier’s stated branch and commit are not in jlevy/squares;
- the receipts’ “independent second-system check” is independent of your search code,
  not of the crate a replay here also runs.

**One matter in your favour.** Rebuilding the 197/200 mutant from the candidate by your
shipped script’s own rule reproduces the input digest each control log records.
So each control is bound to its candidate, not only to a stated mass.

## 0. What Was Read, Run and Not Reached

**Read in full.**

- In this repository:
  - bead think-4ul6, and the notes of think-i85v;
  - the packet’s `README.md`, `source-manifest.json` and
    `acquisition/release-assets.json`;
  - in `result-import.md`, stage 4;
  - in `epistemics.md`: Verification, Confirmation, Which Code Confirmed It, Every Run’s
    Code Is Kept, Review Records, and Scope and Composition;
  - `packing/frontier/verifiers.schema.yaml`, for the registry’s vocabulary;
  - T-142’s register entry, and `E-wand125-fine-net-n28-57425-report`;
  - the frontmatter of `n-028.md` and `n-030.md`, for the upper bounds on record.
- In `packing/sqverify_fast/SOUNDNESS.md`: the claim, N1 to N4, Declared Nets (lemma
  N0), C1, A1, A2, the oblique lemmas R1 to R6 and the acceptance rule, D, I1, I2, F2,
  F3 and A3.
- In the crate:
  - `axis.rs` whole;
  - in `certificate.rs`: `d4_images`, `domain_upper`, `direction`, the format M reader,
    the expansion, and `admit`’s premise checks (at `e020eb1e2` and at the head);
  - `lib.rs`’s `run_direction_inner`;
  - the leaf, witness and depth-limit bookkeeping of `rotated.rs`’s branch and bound;
  - `build.rs`.
- In `devtools/sqverify_fast_census.py`, `axis_captures_agree` and the header of
  `devtools/sqverify_fast_axis.py`, both read and not run.
- From the source, as data:
  - SPEC.md (blob `eefbaf59…`), REPRODUCE.md (`d5192e13…`) and `fine_net_check.sh`
    (`8cc96e65…`), read from the 6 October check2 packet, which retains the same blobs;
  - both directories’ `README.md`, `bundle.json`, `ASSET.json` and `files-sha256.json`,
    fetched at the pins;
  - both candidates, the check2 receipts, `control.json` files, run logs, control logs
    and pre-publication receipts;
  - the sealed bundles’ member lists, their README and `SOUNDNESS.md`;
  - the nested verifier archive’s `certificate.rs` hunk against `e020eb1e2`, and its
    `SOUNDNESS.md` additions, both read in memory and not retained.

**Route reviews read, none of them a review of these two results.**

- The
  [declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md)
  of 6 October, whole, including its checklist (b).
- The [fine-net review](review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md)
  of 14 October, whole, as the brief’s structural precedent.
  It reviews other certificates of the same kind, and §11 says what of it this review
  relies on.

**Run.** The programs written for this review, kept with their outputs under the
packet’s `review/` directory and listed in §6, and the reviewed `sqverify-fast`, driven
by one of them. Outside the programs, three commands also ran:

- `cargo build --release --locked -j 2` of the crate, in the worktree;
- `git ls-remote origin 'refs/heads/wand125*' 'refs/heads/*proof-net*'`, read-only;
- `curl` fetches of the two assets and eight documents, each held to its pin by the
  programs.

The computation totalled about four CPU-minutes, at `nice -n 19` and two threads.

**Not reached.**

- A complete capture of either certificate.
- The census’s whole-net 99/100 control and near-threshold mutant, which the import lane
  runs after this review.
- The upper end of the axis sweep’s enclosure at the 99/100 mutant’s vertex, which the
  census’s enclosure rule compares with (§3).
- The author’s C++ checker of the earlier bundles, which no one has run on these
  candidates.
- The nested archive’s 55 added test lines, which were counted and not read.
- The intake lane’s receipts (`receipts/premises-*.json`,
  `receipts/sample-diagnostic-*.json`) and the packet’s `reported-n*-followup.json`.
  They were left unopened to keep this review apart from that lane’s conclusions.
  The packet README’s summary of them was read (§12).

## 1. The Claims

For $(n, L) \in \{(28, 2297/400), (30, 2357/400)\}$: no packing of $n$ closed unit
squares with pairwise disjoint interiors lies in the closed square $K = [0, L]^2$. Hence
$s(n) > L$, and in particular $s(n) \ge L$. These are `T-142` and `T-143`.

Each claim is the theorem of `SOUNDNESS.md` (“The Claim”), on the net the candidate
declares, with these hypotheses:

- **(H1) The measure.** The rows $R_j = [x_1, x_2] \times [y_1, y_2] \subseteq K$ carry
  masses $w_j > 0$, all exact rationals, and the density is
  $g = \sum_j \frac{w_j}{8|R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)}$. The total is
  $M = \sum_j w_j = n - 1/100000 < n$.
- **(H2) The net.** $B = 4999/5000$, $D = 1/5002$ and $N_\theta = 2073$ satisfy lemma
  N0’s (a) to (e): $2 \le N_\theta \le 2^{16}$; $B(1 + D) < 1$; $t_{\max} = 2072 D$ has
  $t_{\max}^2 + 2t_{\max} - 1 > 0$; $t_{\max} \le 1/2$; and $B(1 + D/(1 - D^2/4)) < 1$.
- **(H3) The coverage.** For every node $r = 0, \ldots, 2072$ and every centre $c$ of
  the per-bin domain $[\rho(a_r), L - \rho(a_r)]^2$, the closed square $Q_r(c)$ of side
  $B$ at angle $\theta_r = 2\arctan(rD)$ has $\int_{Q_r(c)} g \ge 1$. Here
  $a_r = \max(0, rD - D/2)$ and $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$. This is the
  statement the author’s runs decide.
- **(H4) The fold.** Every $a_r$ lies below $\tan(\pi/8)$, and the last bin
  $[2071.5\,D, 2072.5\,D]$ contains $\tan(\pi/8)$.

**Against the record.**

- At n = 28 the claim is above T-107’s $1147/200$ by $3/400$, and above the $287/50$ of
  jlevy/squares#446, never adopted, by $1/400$.
- At n = 30 it is above T-109’s $11767/2000$ by $9/1000$.
- Both are below the upper bounds on record, by 0.0819 and 0.1075: $5.82444\ldots$, the
  verified upper bound at n = 28, and the grid’s $6$ at n = 30.

## 2. The Argument, Re-derived

The argument is the theorem’s proof in `SOUNDNESS.md`, read with lemma N0 in place of
the standard net’s constants.
Every value below was recomputed here (`check_candidate.py`).

**N1, the net.** The half-angle tangents $t_r = r/5002$ are $D$ apart, so every
$t \in [0, 2072.5\,D]$ is within $D/2$ of a node.
The endpoint is $t_{\max} = 2072/5002 = 1036/2501$, and
$t_{\max}^2 + 2t_{\max} - 1 = 367/6255001 > 0$. So $t_{\max} > \tan(\pi/8)$, by
$2.07 \times 10^{-5}$ in the tangent.

**N2, the orientation.** Take a unit square’s angle $\varphi \in [0, \pi/2)$. If
$\varphi > \pi/4$, reflect that one square in $y = x$. The reflection maps $K$ to itself
and $g$ to itself, by $D_4$ invariance, and sends $\varphi$ to $\pi/2 - \varphi$. A core
found for the image, reflected back, lies in the square and captures the same mass.
For $\varphi \in [0, \pi/4]$, $t = \tan(\varphi/2) \le \tan(\pi/8) < 2072.5\,D$. With
$r$ the nearest node, $z = \tan(\delta/2) = |t - t_r|/(1 + t\,t_r) \le D/2$.

**N3, the shrink.** The concentric core of side $B$ at $\theta_r$, seen in the square’s
frame, has extent
$B(1 + 2z - z^2)/(1 + z^2) \le B(1 + 2z) \le B(1 + D) = 25009997/25010000 < 1$. The
margin is $3/25010000$, or $3/50020000$ per side, so the core lies in the open unit
square.

- The sharp extent at $z = D/2$ is
  $B(1 + D - D^2/4)/(1 + D^2/4) = 500400014977/500400085000$.
- Admission also checks the tangent form (e), $500400014977/500400075000 < 1$. N3 does
  not need it.

**Lemma D, the per-bin domain.**

- A square assigned to node $r$ has $t \ge a_r$. Its half-width is
  $\rho(t) = (\cos\varphi + \sin\varphi)/2$, and $\rho'(a)$ has the sign of
  $1 - 2a - a^2$, positive on $[0, \sqrt 2 - 1)$. With $a_r \le t \le \tan(\pi/8)$, this
  gives $\rho(t) \ge \rho(a_r)$, so the square’s centre, which is the core’s, lies in
  $[\rho(a_r), L - \rho(a_r)]^2$.
- The argument needs every $a_r$ below $\tan(\pi/8)$, which is (H4). The largest is
  $a_{2072} = 4143/10004$, where $a^2 + 2a - 1 = -22423/100080016 < 0$, and the last
  bin’s upper end $4145/10004$ is past $\tan(\pi/8)$.
- This is why N2 folds at $\pi/4$ and not at the net’s end.
  A square between $\tan(\pi/8)$ and $t_{\max} + D/2$ would have a smaller $\rho$ than
  node 2072’s $\rho(a_{2072}) = 0.70710677\ldots$.
- $\rho(a_r)$ increases strictly over all 2,073 nodes, from $\rho(0) = 1/2$. At every
  node it is at least Tokoharu’s $B(c_r + s_r)/2$, so the per-bin domain is the smaller
  of the two.

**C1, the quarter turn.** The rotation $T$ by $\pi/2$ about $(L/2, L/2)$ preserves $g$
and carries $Q_r(c)$ to $Q_r(Tc)$, so the crate checks only the quadrant
$[L/2, L - \rho(a_r)]^2$. The decision of direction 0 here (§3) covers the whole domain
and does not use C1. `selftest.py` checks the invariance on the evaluator.

**N4, the count.** The $n$ cores are pairwise disjoint closed subsets of $K$, each of
$g$-measure at least one by (H3). So $n \le \int_K g = M = n - 1/100000$, a
contradiction.

**The two methods.**

- At $r = 0$ the crate runs the vertex sweep (lemmas A1 and A2) on the quadrant’s event
  grid, of $4{,}107^2$ and $3{,}017^2$ vertices here.
- At $r \ge 1$ it runs the interval branch and bound, with the release audit at every
  1,024th box (A3).
- Lemma F3’s caps hold with room.
  The densest image density is 77,055 and 53,206, against $2^{96}$. Eight times the
  densest row is $4.93 \times 10^6$ and $3.41 \times 10^6$, against $2^{32}$.
- Every row has both sides at least $0.0010001$. No rectangle is nearer than 0.519 and
  0.207 to a wall.
- Every coordinate is a decimal, on the grid $10^{-16}$ (n = 28) or $10^{-17}$ (n = 30).

**The instances.** Every value in the table was recomputed here by the programs of §6,
apart from the crate and the tools:

| Premise | n = 28 | n = 30 |
| --- | --- | --- |
| Candidate SHA-256; semantic digest by REPRODUCE.md’s rule | `5ef20511…`; `a1ea15ca…` | `981a17db…`; `716bcb62…` |
| Rows, all positive, inside $K$ and nondegenerate | 631 | 463 |
| Images; distinct (the crate’s `expanded_rectangles`) | 5,048; 5,036, three rows having coincident images | 3,704; 3,672, eight rows |
| Mass, equal to `total_mass` and to $n - 1/100000$ | $2799999/100000$ | $2999999/100000$ |
| `proof_net` exactly `{step, last}`; no `net`, `certificate` or `scaling_factor` key; `points` empty; no duplicate key | yes | yes |
| Lemma N0 (a) to (e) and (H4) | hold | hold |
| Per-bin domain’s least width, at node 2072 | 4.328 | 4.478 |
| Source run: directions, all `verified` at threshold `1` | 2,073 | 2,073 |
| Source run: nodes; direction CPU; wall at 12 threads | 594,284,796; 9,204 s; 771.6 s | 702,952,674; 14,335 s; 1,790.1 s |
| Source run read the published candidate (`input_sha256`) | yes | yes |
| Least certified oblique bound, at direction | 1.0000000000107 (1088) | 1.0000000000293 (1585) |
| Axis: the source’s certified bound; the exact capture at its vertex | 1.0014141477613605; 1.0014141499366220 | 1.0017528833353533; 1.0017528835255092 |
| Direction 0 decided here over $[1/2, L - 1/2]^2$: least vertex, exact | 1.0014141499366220 | 1.0017528835255092 |
| The 12 tightest directions: exact capture at each leaf box’s centre and corners | all at least the bound and 1; least 1.00225 | least 1.00257 |
| Control (197/200): refusals; witnesses in the domain, below 1, equal to the crate’s | 32; all (axis exact 0.98639) | 32; all (axis exact 0.98673) |
| Control mutant rebuilt from the candidate by the shipped rule: SHA-256 equal to the log’s input | `10db6906…`, yes | `545519bb…`, yes |
| Sampled here by the reviewed crate: rows equal to the source’s | 6 of 6 | 6 of 6 |

**What this instance cannot discharge from retained material.**

1. **The coverage (H3).** The author’s run decides it at all 2,073 directions; its log
   is retained and was read here direction by direction.
   Here it has been sampled:
   - direction 0 of each certificate is decided by this review’s own code;
   - the reviewed crate ran six directions of each certificate here, and every row
     equals the author’s;
   - the intake lane reports the same of its eight per certificate (0, 296, …, 2072).

   Until a complete census from reviewed source runs, (H3) at the oblique directions is
   the author’s report.

2. **The author’s build.** The binary `ec04d332…` cannot be rebuilt from retained bytes,
   since the archive is pinned and not retained.
   This review recomputed the archive’s build digest `ab6e33e1…` from the asset fetched
   again (§5). That ties every receipt to those bytes.

3. **The controls.** The author’s 32-direction 197/200 controls were checked here in
   full (§4). The census’s whole-net control (FC-1) has not run.

Everything else the theorem needs holds exactly in the retained and pinned material.

## 3. Direction 0, Decided Here

`axis_decide.py` decides direction 0 of each certificate over the whole per-bin domain
$[1/2, L - 1/2]^2$, without the quarter-turn reduction.
The method was derived for this review from lemma A1’s mathematics, not transcribed from
`axis.rs`.

1. **Vertices suffice.** $F(x, y) = \sum_k g_k\, o^x_k(x)\, o^y_k(y)$, summed over all
   eight images of every row (unmerged), with $g_k$ the image’s density,
   $o^x_k(x) = \lvert[x - h, x + h] \cap [x_1, x_2]\rvert$ and $h = B/2$.
   - Each $o^x_k$ is continuous and affine between consecutive points of
     $\{x_1 \pm h, x_2 \pm h\}$.
   - On each cell of the grid $E \times E$, where $E$ holds every such point inside the
     domain and the domain’s two ends, $F$ is bilinear.
     Its minimum over the closed cell is therefore at a corner.
2. **Exact overlaps.** Every event and edge is an integer multiple of $1/S$, with $S$
   the least common multiple of the denominators ($10^{16}$ and $10^{17}$). So every
   overlap is exact in int64.
3. **A proved error bound.** Each vertex value is a dot product of nonnegative terms
   $(g_k/S^2)\,O^x_k\,O^y_k$, with $O^x_k = S\,o^x_k$ and $O^y_k = S\,o^y_k$ the integer
   overlaps. With three correctly rounded inputs, one rounded product and a $K$-term dot
   product in any summation order, the computed value is
   $\hat F = \sum_k t_k (1 + \theta_k)$, with $\lvert\theta_k\rvert \le \gamma_{K+4}$.
   So $F \ge \hat F/(1 + \gamma_{K+4})$, and a vertex is certified when
   $\hat F(1 - 2\gamma_{K+4}) \ge 1$. The bound needs no subnormal term, and none
   arises: the least positive term, at one unit of overlap on each axis, is
   $2.8 \times 10^{-34}$ (n = 28) and $2.1 \times 10^{-36}$ (n = 30).
4. **Exact checks.** The 24 lowest vertices, the least vertex’s orbit under $D_4$, 40
   random vertices and the source’s reported vertex are then evaluated in fractions.

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Events per axis; vertices | 8,212; 67,436,944 | 6,032; 36,385,024 |
| $\gamma_{K+4}$; worst relative binary64 error seen at the exact checks | $5.6 \times 10^{-13}$; $5.5 \times 10^{-16}$ | $4.1 \times 10^{-13}$; $1.1 \times 10^{-15}$ |
| Least vertex value, exact | 1.0014141499366220 | 1.0017528835255092 |
| A vertex where it falls; its $D_4$ orbit | $(1/2, 1.4996999791220121)$; eight vertices, one value | $(2.3932002286619028, 2.4997728504734369)$; eight vertices, one value |
| The source’s argmin is in that orbit | yes, $(4.2428000208779879, 2097/400)$ | yes, $(3.4992997713380972, 3.3927271495265631)$ |
| The source’s certified bound, below the exact capture by | $2.18 \times 10^{-9}$ | $1.90 \times 10^{-10}$ |
| Vertices below 1.002; below 1.005 | 51,972; 167,604 | 100,872; 364,052 |
| Verdict | verified | verified |
| CPU; wall | 17.9 s; 11.0 s | 6.9 s; 4.5 s |

**The mutants.** Each mutant’s capture is the factor times the original’s, so each
mutant’s least vertex is the same, and its refusal there is exact:

- 197/200: 0.9863929376875726 at n = 28 and 0.9867265902726265 at n = 30;
- 99/100: 0.9914000084372557 and 0.9917353546902541.

The source’s 197/200 axis rows report bounds $2.14 \times 10^{-9}$ (n = 28) and
$1.87 \times 10^{-10}$ (n = 30) below those exact values.
The reviewed crate’s 99/100 axis rows, run here, report bounds $2.15 \times 10^{-9}$ and
$1.88 \times 10^{-10}$ below.
Every axis bound read here lies below its exact capture, on the side soundness needs.

The census control’s axis rule now accepts a refusal when the exact capture lies in the
enclosure the sweep held at that vertex (#892, `axis_captures_agree`). Under the earlier
constant of $10^{-9}$, T-142’s gap of $2.15 \times 10^{-9}$ would have failed that leg
closed (F-7). This review did not compute the enclosure’s upper end, so it does not say
which way that leg falls.
It says only that the refusal is mathematically sound: the capture is below one at a
vertex of the closed domain, and the bound is below the capture.

**What the slack looks like.** The least exact capture at any pose evaluated here is at
direction 0: 1.00141 and 1.00175. At oblique poses the least seen is 1.00168 (n = 28,
the 197/200 witnesses at directions 67, 134, 201 and 468, a plateau of one value) and
1.00367 (n = 30, a leaf at direction 2071). These numbers bound each certificate’s slack
from above. The least certified oblique bounds, 1 plus $10^{-11}$ or so, are the branch
and bound’s termination margin, not the measure’s slack.

## 4. The Source’s Records

**The run logs** (`check_source_logs.py`).

- Each log has 2,074 lines: one row per direction for 0 to 2072, each once, and the
  summary last.
- Every row is `verified` at threshold `1`. The axis was decided by the vertex sweep and
  every other direction by branch and bound, each with at least one audit at
  `audit_every` 1,024. No row carries a witness.
- The summary’s nodes, direction CPU and direction seconds equal the rows’ sums.
- Its premises equal this review’s recomputation, key for key: `B`, `D`, `L`,
  `angle_count` 2073, `centre_domain` `per-bin`, `format` `M`, `input_sha256` (the
  published candidate’s), the masses, `source_rectangles`, and `expanded_rectangles`
  5,036 and 3,672, which are the distinct images counted here.
- The summary’s status is `VERIFIED`, `refused_directions` is empty and
  `fault_injected_at_box` is null.
- The author’s build predates the summary fields `net_origin`, `net_last_tangent` and
  `shrink_bound`. Its `D` and `angle_count` show the declared net was read.
  The reviewed build’s summaries, run here, carry all three, as the checklist’s item 3
  wants (§9).
- n = 28: the least oblique bound is at direction 1088, the most nodes at 2070 (438,813)
  and the fewest 169,449. Maximum depth 34.
- n = 30: the least bound is at 1585, the most nodes at 2071 (469,029) and the fewest
  213,729. Maximum depth 33.
- The n = 30 run’s per-direction wall seconds sum to 21,422 against 14,335 of CPU. Its
  twelve threads shared fewer cores.
  This bears on the price, not the verdict.

**The receipts.**

- Each `check2/receipt.json` wraps an inner `fine-net-check2-receipt/v1`. That receipt’s
  fields match the candidate, the log and each other: $n$, $L$, $B$, the net, the mass,
  2,073 expected, checked and verified, the digests, `PASS`, and the verifier’s source
  `ab6e33e1…` and binary `ec04d332…`. Its `verifier_summary` equals the log’s summary
  line.
- `control.json` is the inner receipt’s control plus the source digest.
- `bundle.json`’s net block holds exactly, as do its candidate and receipt digests and
  its stated improvement: `endpoint` $1036/2501$, `endpoint_check` $367/6255001$,
  `rotated_side_upper` $25009997/25010000$, and the margins $3/25010000$ and
  $3/50020000$.
- Each README states the digest, the mass and the 2,073 directions.

**One complete run each.**

- **n = 30.** The pre-publication receipt is identical, field for field, to the check2
  receipt’s inner record: start 12:01:39Z, 1,790.3 s, 12 threads, binary `ec04d332…`. It
  is that run’s record.
- **n = 28.** The pre-publication receipt is in the older shape the shipped
  `fine_net_check.sh` writes, with `build`, integer `seconds` and no start time or
  binary digest. It states 772 s against the check2 run’s 771.9 s, and the same control
  outcome, so nothing distinguishes it from that run.

So each certificate carries one reported complete run (F-4).

**The controls.**

- **The directions.** Each control ran at the 32 directions
  $\mathrm{round}(2072\,i/31)$, $i = 0, \ldots, 31$, the shipped script’s rule.
- **The mutant.** Its summary’s mass is exactly $197/200$ of the candidate’s.
- **The mutant’s identity.** The control log’s `input_sha256` names the mutant file,
  which the bundle does not ship.
  Rebuilding it by the shipped script’s rule reproduces that digest exactly at both
  counts: `json.load`, every mass times $985/1000$ written as `str(Fraction)`,
  `total_mass` re-summed, and `json.dump` with its defaults.
  So each control is bound to its candidate.
- **The 31 oblique refusals.** Each witness pose is the stopping box’s centre, in the
  per-bin domain and in the quadrant.
  Its exact capture of the 197/200 measure, recomputed here, equals the crate’s
  `exact_coverage` digit for digit and is below one.
  The range is 0.98665 to 0.99999999998 (n = 28) and 0.98942 to 0.99999999998 (n = 30).
- **Witnesses near one.** Sixteen of the 62 witnesses (9 and 7) sit within $10^{-8}$ of
  one, where the original captures about $200/197$, and 12 of them within $10^{-9}$.
  Every one of the 16 stopped at the depth limit of 60. Each came from the path that
  evaluates the first deep boxes’ centres exactly, since a centre within $10^{-9}$ of
  one cannot trigger the estimate’s refusal.
  They are exact refutations all the same.
- **The axis refusal.** It carries no exact value in the log.
  Its exact value is in §3, below one at a vertex of the closed domain.

All 32 refusals of each control are genuine.

## 5. Trust Boundaries

| Checker | Decides | Trusts | Shares with the others |
| --- | --- | --- | --- |
| The author’s nested crate: archive `e495f9bf…`, build `ab6e33e1…`, binary `ec04d332…` | (H3) at all 2,073 directions, in the author’s one run of each | binary64 without FMA (I1), `enclose` (I2), lemmas R1 to R6, A1, A2, D and N0, and its own 32-line reading of `proof_net` | `e020eb1e2`’s source `7c49cf79…` with `certificate.rs` +32 −2. Every other `src/` file, the lockfile, `build.rs` and the toolchain pin are byte-identical to `e020eb1e2`, and so to the reviewed kernel |
| `sqverify-fast`, this repository, source `d97758bb…` (reviewed 3 and 6 October), binary `567a0fd5…` | (H3) at the 12 directions run here, and the 99/100 mutant’s refusal at six | the same lemmas, and main’s lemma N0 reader | with the author’s crate, every `src/` file but `certificate.rs`, `lib.rs` (three summary lines) and `rotated_tests.rs` (one line): the same kernel |
| This review’s `axis_decide.py` | direction 0 of each certificate over the whole per-bin domain | Python fractions; int64 overlaps; binary64 dot products under the proved bound $\gamma_{K+4}$ (OpenBLAS, any order) | nothing: written from lemma A1’s mathematics, importing nothing |
| This review’s `fine_net_exact.capture` | the capture at the poses evaluated: 182 from the source’s records and 64 in the runs here | Python fractions | nothing; written from the claim’s definition of the density |
| This review’s premise programs | nothing: exact premises, custody, records | fractions, SHA-256, `git show` | nothing |
| The census control’s evaluator `check_sqverify_fast.mixed_exact` | the mutant’s capture at the crate’s witnesses, in the whole-net control | fractions and `sqpack`’s exact clipping | not run here |

**What the author’s crate is.** `custody_and_nested.py` read the archive inside the
re-fetched asset and recomputed, by the archive’s own `build.rs` rule, the
`source_sha256` a build embeds.
It is `ab6e33e1…`, the digest every receipt and summary names, so the receipts are runs
of those bytes.

Against the reviewed source `e020eb1e2` (`7c49cf79…`), 16 of the 20 files are
byte-identical: `src/axis.rs`, `exact.rs`, `interval.rs`, `lib.rs`, `main.rs`,
`oracle.rs`, `rotated.rs` and `rotated_tests.rs`, together with `Cargo.toml`,
`Cargo.lock`, `build.rs`, the toolchain pin, `clippy.toml`, `.gitignore` and the two
independence files. The other four differ:

- `src/certificate.rs`, by 32 added and 2 changed lines;
- `tests/adversarial.rs`, by 55 added lines;
- `README.md`, by 5 added and 2 changed lines;
- `SOUNDNESS.md`, by 11 added lines.

I read the `certificate.rs` hunk.

- When a format M file carries `proof_net`, the block must be an object with exactly
  `step` and `last`, and no `certificate` metadata may sit beside it.
  `step` is read as an exact rational and `last` as a `u32` plus one, into the same
  `step` and `angle_count` the rest of `admit` reads, and the standard-net pin is
  skipped only for format M.
- The shared checks that follow at `e020eb1e2` are then lemma N0’s (a) to (e) on the
  declared values: the positive step and $2 \le N_\theta \le 2^{16}$; $B(1 + D) < 1$;
  the endpoint polynomial; $t_{\max} \le 1/2$; and, for the per-bin domain, the tangent
  form.
- After the format is known, a declared net outside format M is refused (“proof_net is
  accepted only for format M”).
- `domain_upper` and `direction` read the same `step`.
- The archive keeps `e020eb1e2`’s duplicate-key reader unchanged, and that reader is
  byte-identical to main’s. Compared with main’s declared-net reader, the archive lacks
  the optional `count` field and DN-5’s refusal of a top-level `net` key outside format
  L. Neither candidate has a `count` or a `net` key, and this review’s own reader found
  no duplicate key in either file.

The 11 `SOUNDNESS.md` lines restate lemma N0’s premises without its proof (F-1).

Against the head of this tree, the archive’s `src/certificate.rs` is +38 −98, `lib.rs`
−3 and `rotated_tests.rs` −1, and it has no `tests/declared_net.rs`. Those are counts
only; the 6 October review describes main’s side.
The head’s crate digest is still `d97758bb…`.

**What that means for the rung.**

- The author’s runs rest on the reviewed kernel and on 34 lines read here.
  What those lines decide, the net and the domain, is observable.
  The author’s summaries report `D` $1/5002$, `angle_count` 2073 and `centre_domain`
  `per-bin`. The reviewed build, reading the same declaration through main’s lemma N0
  reader, reproduces the author’s node count, leaves, depth, least bound and least-bound
  box at every one of the 12 directions sampled here, and the intake lane reports node
  counts and least bounds equal at its 16. Those numbers depend on the step, the domain
  and the search, so the agreement is strong consistency, though not review.
- For the record, the author’s runs are the reported entries’ evidence, at `V0`, read as
  `same-implementation` with `V-wand125-sqverify-proof-net` deciding.
- A census here from `d97758bb…` would be *re-implemented sharing the producer’s
  components*, as the entries’ `composition` says and T-104 reads.
  No second implementation of the oblique search stands beside the kernel, and a defect
  in the shared `rotated.rs`, `axis.rs` or `interval.rs` would pass both.
- Independent of that kernel stand this review’s exact evaluator, at every pose it
  evaluated, and its decision of direction 0, which is independently re-implemented for
  that one direction of each net.

## 6. Checks Made Here

Every program is kept, with the output it printed, under
[`wand125-fine-net-n28-n30-2026-10-10/review/`](../../../packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/review/README.md).
Its README says what each program read, how to run it and what it printed.
The programs ran under `python3 -I` with the project interpreter, reading the packet and
the assets as data.

| Program | Read | Printed | CPU |
| --- | --- | --- | --- |
| `selftest.py` | synthetic data | six passes, one of them a seeded wrong clip caught | 0.2 s |
| `check_candidate.py`, two runs | the retained candidates; the manifest | the table of §2: every exact premise holds | 0.5 s |
| `check_source_logs.py`, two runs | the retained run logs, control logs, receipts, `control.json` and pre-publication receipts | §4: every record consistent; 62 witnesses genuine; 120 leaf poses at least their bound and one; both mutants rebuilt to the logged digest | 8.4 s |
| `axis_decide.py`, two runs | the retained candidates; the run and control logs’ axis rows | §3: direction 0 verified over the whole domain at both counts | 24.8 s, after a first pair of runs (21.8 s) without the subnormal field |
| `custody_and_nested.py` | both assets, in memory; the packet; `git show` at `e020eb1e2`, `34e87a86b` and head | custody of every member and retained copy; sealed bundles against their manifests; the archive’s build digest and file comparison (§5) | 0.3 s |
| `check_source_docs.py` | the eight fetched documents; the assets; `git show e020eb1e2` | the documents equal their pins; `bundle.json` exact; F-1, F-2 and F-3’s facts | 0.1 s |
| `sample_directions.py`, two runs, with the reviewed binary | the retained candidates and run logs | 12 directions equal to the source’s rows; 60 leaf poses at least their bound and one; item 3’s premises; six 99/100 refusals with exact witnesses | binary 64.9 s; Python 3.1 s |

The build took 42 seconds of wall at two jobs, about 85 CPU-seconds at most.
The samples ran at 0.78 (n = 28) and 0.74 (n = 30) of the author’s CPU on the same
directions.

What failed along the way, and what was redone:

- `/usr/bin/time` is not installed, so CPU was taken from `getrusage` inside the
  programs and from the shell’s `time`.

- `fine_net_exact`’s first multi-member gzip test could not detect a second member.
  It was rewritten with `zlib.decompressobj` before any run.

- `check_candidate`’s first monotonicity test of the per-bin domain was a convoluted
  expression. It was replaced by a strict test and rerun, with the same result.

- `check_source_docs`’s first run had three faults of its own:
  - it looked up the README’s named files only in the outer asset, not in the sealed
    bundle and the Git directory;
  - its pattern for the directions rule was a parenthesis short;
  - it looked up `bundle.json`’s verifier sources in the outer asset.

  All three were corrected and the program rerun.
  Only `check2/control.jsonl.gz` remained absent.

- `sample_directions`’ first n = 28 run flagged `input_sha256` because the binary had
  read the retained `.gz`, whose digest it rightly reports.
  The check was corrected to that file’s digest, as the checklist’s item 4 reads, and
  the run repeated. Its rows were the same.

- `axis_decide` was run a second time, to record the least positive term, which the
  error bound’s no-underflow condition needs.
  Its results were the same.

- `custody_and_nested` was run a second time, to record as facts the admission rules §5
  reads from the archive’s `certificate.rs`. No line of the archive is kept.

Nothing the brief asked for went unestablished because of a tool or permission failure.

## 7. Findings

No finding is blocking, and none is major in either certificate.
The grades are for the claims first and the record second.
Line numbers refer to the files at the pinned revisions.

### F-1, minor, in the source: the bundles’ soundness note predates the declared-net lemma their reader relies on

`check2/src/SOUNDNESS.md` in both directories, listed in `bundle.json`’s
`verifier_source_sha256`, is Git blob `cadf59b6…`. That is this repository’s edition at
`e020eb1e2`, byte for byte, and it mentions neither `proof_net` nor a declared net.
The statement the certificates’ admissibility rests on is lemma N0 (the crate’s
`SOUNDNESS.md`, “Declared Nets”, since `f007d7afd`), which this review used.

The archive’s own copy adds 11 lines that list the premises admission checks on a
declared net. Without N0’s proof, a reader is not told why the fold at $\pi/4$, and not
at the net’s end, makes the per-bin domain valid.

The mathematics holds (§2). Fix: ship or cite the edition with lemma N0, or state the
argument for the declared net in the bundle.

### F-2, minor, in the source: the README names a control file that does not exist

`README.md`, line 15, of both directories lists
`check2/control.json, check2/control.jsonl.gz`. The shipped log is
`check2/control-197_200.jsonl.gz`, in the asset, in the sealed bundle and in
`files-sha256.json`. No file of the README’s name is in the asset, the sealed bundle or
the Git directory.

### F-3, minor, in the source: the published receipts were written by a program the bundle does not ship

The shipped `check2/src/fine_net_check.sh` (SHA-256 `a4069c4b…`) writes a receipt with a
`build` field, integer `seconds`, the control kind “every mass x 0.985, 32 directions”
and no `schema` or `tries`. That is the shape of the n = 28 pre-publication receipt.

Both published `check2/receipt.json` files instead wrap `fine-net-check2-receipt/v1`,
with `verifier`, decimal `seconds` and a control given as `tries` at factor `197/200`,
and so does the n = 30 pre-publication receipt.
REPRODUCE.md names `fine_net_check.py` in wand125/square-packing-tools at `5fba675` as
an alternative source, and that is likely the writer, but the bundle does not carry it.

The outcomes agree, and `candidate_digest` and `status`, which the README asks a
reproducer to compare, sit at the top level of both shapes.
But a reproduction by the bundle’s own steps yields a receipt of another shape than the
one published. Fix: ship the program that wrote the published receipts, or say which
program wrote which.

### F-4, note, in the source and the record: one recorded run each, not two

`README.md`, line 54, says the candidate “was checked again … on a fresh Ubuntu 24.04
(x86_64), Rust 1.98.0 machine”, and the sealed edition of the README lacks that section.

The n = 30 pre-publication receipt is the check2 run’s record, field for field (§4). The
n = 28 one cannot be told apart from that run.

So the record should count one reported complete run per certificate, and the README’s
“again” should not be read as a second, independent run.
If there was a second run on another machine, its log and receipt, with a start time and
a binary digest, would make it citable.

### F-5, note, in the source: the stated verifier location is not in jlevy/squares

Each receipt’s `verifier` reads “jlevy/squares packing/sqverify_fast, branch
wand125/sqverify-proof-net, commit fe12e036c”, and `check2/src/UPSTREAM_COMMIT` holds
`42534d959…`. jlevy/squares has no such branch: `git ls-remote` on 4 November lists only
`wand125/n17-native-cert` under `wand125/`. This repository’s full clone holds no object
`fe12e036c` and no object `42534d959…`.

The code exists here only as the archive `e495f9bf…` the bundle carries, which this
review read, and, by REPRODUCE.md, in wand125/square-packing-tools at `5fba675`. Fix:
name the repository that holds `fe12e036c`.

### F-6, note, in the source: “an independent second-system check”

`check2/receipt.json`’s `checked_by` calls the run “an independent second-system check
(built from the certificate specification only, without reading the search code)”. That
is true of the author’s search code.
The check is this repository’s crate, whose clean room is recorded in
`packing/sqverify_fast/INDEPENDENCE.md`, adapted by the author.

A reader should not take the phrase as independence from the crate a replay here would
also run. That is why §5 reads a census here as sharing the producer’s components.

### F-7, note, for the records lane: T-142’s axis leg and the census rule

At T-142’s axis vertex, $(4.2428000208779879, 2097/400)$, on the closed domain’s upper
edge, the exact capture sits above the crate’s certified bound by:

- $2.18 \times 10^{-9}$ for the original;
- $2.14 \times 10^{-9}$ for the 197/200 control;
- $2.15 \times 10^{-9}$ for the 99/100 mutant, run here with the reviewed crate.

T-143’s gaps are $1.9 \times 10^{-10}$. Every refusal is sound (§3).

The census’s former constant of $10^{-9}$ would have failed T-142’s whole-net control
closed. #892’s enclosure rule now judges the leg by the enclosure the sweep held there,
which this review did not compute.
No change is needed in either certificate.

## 8. Questions for the Author

1. Would you ship, in the check2 bundles, the `SOUNDNESS.md` edition that states lemma
   N0, or your own statement of why the declared net and the per-bin domain are
   admissible (F-1)?
2. Would you correct the README’s control file name (F-2), and ship the program that
   wrote the published `fine-net-check2-receipt/v1` receipts (F-3)?
3. Was the pre-publication check a separate run on another machine?
   If so, would you publish its run log and receipt, with its start time and binary
   digest (F-4)?
4. Where is commit `fe12e036c` published, and is `fine_net_verifier/` at
   wand125/square-packing-tools `5fba675` byte-identical to the archive `e495f9bf…`
   (F-5)?
5. The README says the candidates “can still be run through the shipped verifier of the
   earlier bundles”. Have you run that C++ checker on either candidate, and at which
   directions?
6. Does the directory’s MIT notice extend to the nested verifier archive, which carries
   no notice of its own?

## 9. Verdicts, and What V and C the Evidence Supports

**`mixed_n28_L57425` (T-142), $s(28) \ge 2297/400$: accept with findings.** The argument
from the certificate to the claim holds, every exact premise holds, every record of the
source is consistent with the candidate and with every other record, and direction 0 is
decided here independently.
F-1 to F-7 are minor matters or notes in the source’s documents and the record.
None is a defect of the certificate or of its argument.
In the register’s vocabulary the verdict is `accepted`.

**`mixed_n30_L58925` (T-143), $s(30) \ge 2357/400$: accept with findings.** The same
holds, word for word.
The verdict is `accepted`.

**The rungs.** Both entries are `V0/C0`: the cited evidence is the author’s report, and
no replay has run here.
The records lane would record this review in two places:

- as `external_review` (`informally-verified`) on `E-wand125-fine-net-n28-57425-report`
  and `E-wand125-fine-net-n30-58925-report`;
- in T-142’s and T-143’s `reviews`, as an adversarial AI review with verdict `accepted`.

It then supports `C1` for both.
`V` stays `V0`.

**To `V3/C3`.** Each certificate needs all of the following:

- a complete `sqverify-fast` census from `d97758bb…` at all 2,073 directions, from the
  candidate retained where the census reads it;
- restored positives;
- a `CONTROLS_REFUSED` whole-net receipt (FC-1), with the axis legs judged by #892’s
  enclosure rule;
- this review as the audit record.

The relation would be *re-implemented sharing the producer’s components*. think-i85v
prices the two runs at 3.3 to 4.5 and 4.5 to 6.1 CPU-hours.
The samples here ran at 0.78 and 0.74 of the author’s CPU, consistent with that price.

**The 6 October checklist (b), for each certificate.**

| Item | State | Where |
| --- | --- | --- |
| 1. The file | holds: format M, `points` empty, no `scaling_factor` key (format M reads none), `proof_net` exactly `{step, last}`, no `net`, no metadata; eight times the densest row $4.93 \times 10^6$ and $3.41 \times 10^6$, at most $2^{32}$ | §2 |
| 2. The case | pending: the census row | census lane |
| 3. The premises | hold in the reviewed build’s summaries run here: `M`, `per-bin`, `proof_net`, `D` $1/5002$, `angle_count` 2073, `net_last_tangent` $1036/2501$, `B` and `shrink_bound` $25009997/25010000$, masses $n - 1/100000$, no points or segments, `fault_injected_at_box` null. Lemma N0 recomputed apart from the crate | §§2, 6 |
| 4. The candidate | the retained `.gz` files’ SHA-256 are `4f7afe45…` and `20856f76…`, which the reviewed build reports as `input_sha256`; they decompress to the pinned bytes. `retained_data check` is the census lane’s | §6 |
| 5. The build | `d97758bb…`, profile `release`, rustc 1.98.0, in the runs here | §6 |
| 6. The control | pending: the whole-net receipt | census lane |
| 7. The mathematics | this review, accepting both | here |
| 8. The words | for the evidence text: name the declared net’s step $1/5002$ and count 2,073 and the accepted build by the 6 October review, say *re-implemented sharing the producer’s components* for the census, and cite this review beside the route review | records lane |

**Significance.** The draft scores each entry `S3`, and this review confirms it.
Each is a further size from one generator, by a certificate kind and route the record
holds at `S3`, with no new technique.
At n = 28 the claim stands 0.082 below the verified upper bound; at n = 30 it stands
0.1075 below the grid’s 6, which is still the best known there.

## 10. Proposed Registry Entries

These are for `packing/frontier/verifiers.yaml`, to be applied by the records lane.
`R` stands for `docs/project/reviews/review-2026-11-04-wand125-fine-net-n28-n30.md` and
`P` for `packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/review/programs`.

```yaml
  - id: V-wand125-n28-n30-review-premises
    program: check_candidate.py, check_source_logs.py, check_source_docs.py and custody_and_nested.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Recomputes, apart from the crate and the tools, every exact premise of a check2
      candidate on its declared net (the measure and its mass, the distinct D4 images,
      lemma N0's premises and the last bin, the per-bin domain at every node, lemma F3's
      caps, the semantic digest); reads the source's run logs, receipts, controls and
      pinned documents against the candidate, rebuilds each control's mutant to its
      logged digest, and ties the nested verifier archive to its build digest and, file
      by file, to reviewed source.
    source: [P/fine_net_exact.py, P/check_candidate.py, P/check_source_logs.py, P/check_source_docs.py, P/custody_and_nested.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-4ul6 of the wand125 n28 and n30 import (think-i85v), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source's commits name Claude as co-author. Written by a Claude agent
          prompted separately from the source and from the intake and replay lanes, in
          files of their own that import nothing from the crate, the tools or the source.
      note: >-
        Written after reading SOUNDNESS.md, the crate's axis and certificate modules and
        the branch and bound's bookkeeping, and the source's SPEC.md, REPRODUCE.md and
        fine_net_check.sh. The producer's checker is this repository's crate adapted, so
        no clean room with respect to it is claimed.

  - id: V-wand125-n28-n30-review-exact-capture
    program: fine_net_exact.capture, driven by check_source_logs.py and sample_directions.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The exact mass a closed core at a given centre and net angle captures from a format
      M measure, by Sutherland-Hodgman clipping of the rotated core against each D4 image
      in fractions. Decides the capture at the poses it evaluated: the 62 oblique
      witnesses of the source's 197/200 controls, 120 leaf poses of the source's 12
      tightest directions of each run, and the 60 leaf poses and 4 mutant witnesses of
      the reviewed sqverify-fast's runs here; it agrees with the crate's exact witnesses
      digit for digit at all 66 it was compared with.
    source: [P/fine_net_exact.py, P/check_source_logs.py, P/sample_directions.py, P/selftest.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-4ul6 of the wand125 n28 and n30 import (think-i85v), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Clipping and areas in fractions, written from the claim's definition of the
        density; no code of the crate's oracle, of mixed_exact or of the source.

  - id: V-wand125-n28-n30-review-axis-decision
    program: axis_decide.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [numerical-f64, exact-algebraic]
    role: decides
    summary: >-
      Decides direction 0 of a format M certificate over its whole per-bin domain
      [1/2, L - 1/2]^2: every vertex of the grid of overlap breakpoints, with overlaps
      exact in int64, evaluated as a binary64 dot product of nonnegative terms under the
      proved a priori bound gamma_{K+4} (below 6e-13 here, against margins of 1.4e-3 and
      1.8e-3), and the least vertices, their D4 orbit and a random sample evaluated
      exactly in fractions. Decided direction 0 of mixed_n28_L57425 and mixed_n30_L58925
      verified.
    source: [P/axis_decide.py, P/fine_net_exact.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-4ul6 of the wand125 n28 and n30 import (think-i85v), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Its method is lemma A1's mathematics with its own arithmetic, not a transcription
        of axis.rs: it covers the whole domain rather than the quadrant, and certifies by
        an error bound and exact checks rather than interval sweeps. Its authors read
        axis.rs before writing it.
```

**Evidence entries.** An evidence entry for each thing a run here decided or sampled
would cite these. Each would carry `coverage: {extent: sample, checked: …, of: …}` and
`origin: replayed-here`. Its `relationship_to_generator` would be
`independent-implementation` for the exact captures and the axis decision, and
`shared-components` for the sampled directions.
The case records at n = 28 and n = 30 would cite them, and no result would.
The entries are:

- the 64 control refusals of the two 197/200 controls (checked 64 of 64, deciding the
  author’s controls);
- direction 0 of each net (checked 1 of 2,073, by independent code);
- the 12 directions run here with the reviewed crate (checked 6 of 2,073 each);
- the 120 leaf poses, a sample of (H3).

## 11. Earlier Reviews Compared

This section was written after §§1 to 10. Six earlier documents under
`docs/project/reviews/` mention `T-142` or `T-143`. None of them read either
certificate.

- **[The 11 October final review of PR 487’s lower bounds](review-2026-10-11-final-lower-bounds.md)**
  read the record and the premises and says that “nothing here read wand125’s four
  certificates”. It agrees with this review in several places:
  - its exact differences ($3/400$, $1/400$, $9/1000$), its
    $B(1 + D) = 25009997/25010000$ and its endpoint value $367/6255001$;
  - its `S3`;
  - its F1-3’s axis gap of $2.15 \times 10^{-9}$, which matches the
    $2.153 \times 10^{-9}$ measured here.

  One of its sentences is looser than the argument.
  It says that “the nearest node to any angle in $[0, \pi/4]$ is within $\arctan D$”,
  but the angle to the nearest node can reach $2\arctan(D/2)$, which exceeds $\arctan D$
  by about $D^3/4$. The crate’s N2 says so.
  The same wording in the crate was the 3 October soundness review’s obligation R1,
  which the 6 October review lists as closed.
  The argument needs only $z = \tan(\delta/2) \le D/2$ (§2), so the conclusion that
  review drew, that the core lies strictly inside, stands.
  This is a note on that review’s wording, and no record changes.
  Its F1-4 and F1-5, on the case records and on T-143’s wording, are left to the records
  lane.

- **[The 11 October grading review](review-2026-10-11-final-asymptotic-and-grading.md)**
  grades both `V0/C0` and `S3`, and reads a replay as *re-implemented sharing the
  producer’s components*. That agrees with §§5 and 9.

- **[The 11 October rungs review](review-2026-10-11-recent-register-rungs.md)** finds
  `V0/C0` right because no qualifying read was recorded.
  This review is that read, and supports `C1` once recorded.
  The two holds its RR-6 lists are now answered: retention by the owner’s answer of 17
  October, and the axis tolerance by #892’s enclosure rule, both as T-142’s `next_rung`
  records.

- **[The 14 October fine-net review](review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md)**,
  the structural precedent, reviews other certificates on the same net and with the same
  nested archive (`e495f9bf…`).
  - Its §4 description of the archive (16 identical files, `certificate.rs` +32 −2,
    build digest `ab6e33e1…`) was re-derived here from the bytes, and agrees.
  - Its §4 also says the hunk lacks “f007d7afd’s duplicate-key visitor, its `count`
    field and its refusal of `proof_net` outside format M”. Read here, the archive’s
    duplicate-key reader is `e020eb1e2`’s, which is byte-identical to main’s, and the
    archive does refuse `proof_net` outside format M (“proof_net is accepted only for
    format M”). Only the `count` field, and DN-5’s refusal of a top-level `net` key, are
    missing. Nothing either candidate exercises turns on the difference.
  - Its F-2, F-3 and F-7 concern files these bundles ship too.
    This review checked them again here as F-1, F-2 and F-6.
  - Its F-4, that the control’s input is bound to no shipped file, does not carry over
    as stated. Here each mutant is rebuilt from the candidate to the logged digest by the
    shipped script’s rule.
    Whether the same holds for the n = 37, 39 and 44 controls was not checked here.
  - Its F-1, on the census’s axis tolerance, has since been acted on (#892), and F-7
    here records T-142’s numbers under it.

- **The 23 October reviews of
  [#446’s fine-net certificates](review-2026-10-23-wand125-446-fine-net.md) and of
  [`mixed_n31`](review-2026-10-23-wand125-n31-fine-net.md)** cite T-142 and T-143 only
  for the family’s credit line and as `S3` comparisons.
  Both agree with this review’s credit and significance.

No earlier document found a defect in either certificate, and this review found none.

## 12. Disclosure

No review of these two certificates’ mathematics existed when this one was written.
§11 compares the earlier documents that mention them, read only after §§1 to 10 were
written.

Before writing, the lane read the material §0 lists.
Four parts of it carry conclusions of others about these certificates or their route:

- **The bead notes of think-i85v.** These are the intake lane’s findings: that
  `audit_check2` first refused n = 30’s pre-publication receipt at its newer shape, that
  T-142’s 99/100 axis gap is $2.15 \times 10^{-9}$, that 16 sampled directions matched,
  that one run is reported for each, and the prices.
- **The packet README’s summary** of the same.
- **T-142’s register entry and its evidence entry’s `limitations`.**
- **The 14 October fine-net review, read whole as the brief’s structural precedent.**
  Its findings concern the n = 37, 39 and 44 bundles.
  Its F-2, F-3, F-4 and F-7 bear on the same shipped files as this review’s F-1, F-2,
  F-6 and the control’s binding.
  Each of those was checked again here from the bytes of these two bundles, and for the
  control the result differs: these mutants are rebuilt to their logged digests (§4).

The axis gap was measured again here with the reviewed crate and with this review’s
exact evaluator, and the run count was read again from the receipts.
Neither the intake lane’s receipts nor its follow-up records were opened.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
