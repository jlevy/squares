# Mathematical Review: wand125’s Fine-Net Lower Bound at n = 29

Reviewed on 2026-11-04 from these inputs, all read as data:

- the packet
  [`wand125-fine-net-n29-2026-10-10`](../../../packing/resources/web/wand125-fine-net-n29-2026-10-10/README.md)
  on `main` at `c03183f66`, with the release asset’s six data members under `release/`,
  retained there on 2 November at `219bc1268`;
- the release asset `certificates__mixed_n29_L582.tar.gz` of `square-lower-bounds-v1`,
  fetched again and held to the packet’s size and SHA-256 pin;
- the certificate directory’s eleven pinned documents and the enclosing `LICENSE`,
  fetched at the pinned revision `22a23c8` and held to the manifest’s digests.

It covers `T-132`.

The reviewer is an AI agent, Claude (Anthropic), at the tbd-strong-max tier with maximum
reasoning, acting as the stage-4 mathematical reviewer of record (bead think-1lri) for
the import think-r333. The lane worked in a worktree of its own and shares no context
with the intake, records or replay lanes.
It executed no program of the source.
The one program it ran that it did not write is this repository’s reviewed
`sqverify-fast` (crate source `d97758bb…`), which it built in its own worktree to binary
`567a0fd5…`.

Nothing was posted, and the author was not contacted.
This review registers nothing and moves no bound.

## Summary for the Author

**The bound.** wand125/square-packing published it on 10 October 2026 at `22a23c8`, and
the issue jlevy/squares#446 reports it: $s(29) \ge 291/50 = 5.82$, by `mixed_n29_L582`.
It is a check2 certificate on the 2,073-direction declared net, of core $4999/5000$ and
step $1/5002$. Its measure has 650 rectangles and mass $2899999/100000$.

**What was recomputed here.** All of it was done in exact arithmetic, or in binary64
under a proved error bound, by code written for this review and apart from every
checker:

- the measure and its mass, and the digests;
- the net, lemma N0’s premises, the last bin, and the per-bin domain at all 2,073 nodes;
- lemma F3’s caps;
- your run log: every direction, the sums, the premises, the embedded summary;
- your check2 and pre-publication receipts, and `bundle.json`;
- all 31 oblique witnesses of your 197/200 control, and its mutant file;
- the exact capture at the leaf boxes of the 12 tightest directions of your run;
- direction 0, decided over its whole per-bin domain by a method that shares nothing
  with the crate’s;
- nine oblique directions, among them the four with the least certified bounds and the
  net’s first and last, decided over their whole per-bin domains by a branch and bound
  written for this review, which shares no code and no search lemma with the crate.

This repository’s reviewed `sqverify-fast` was also run at seven directions, among them
the four with the least certified bounds.
It reproduced your per-direction records exactly, in node count, leaves, depth, least
bound and least-bound box.
It refused the 99/100 mutant at three directions, with witnesses this review’s evaluator
confirms.

**The verdict.** No step read here is false, and no finding is blocking or major.

- The argument from the certificate to the bound is lemma N0’s, on the declared net
  (§2), and every premise it needs holds.
- The coverage at all 2,073 directions is decided by your run.
  Here it has been decided at ten directions by this review’s own code, direction 0 and
  nine oblique ones, all verified, and the same code refuted the 99/100 mutant.
  A complete replay has not run here.

The certificate is therefore **accepted with findings**, as a reported result in the
record’s vocabulary.
The findings are minor or notes, all in the bundle’s documents and the record, none in
the argument or the data.
The review supports `C1` once it is recorded, and the bound stays at `V0` until the
census runs.

**Seven matters for you** (§§8 and 9):

- the bundle’s `SOUNDNESS.md` predates the declared-net lemma its reader relies on, and
  its fold, like `SPEC.md`’s, reflects the whole configuration;
- the README names a control file that does not exist;
- the published receipt was written by a program the bundle does not ship;
- the pre-publication run has a receipt and no log;
- the verifier’s stated branch and commit are not in jlevy/squares;
- the receipt’s “independent second-system check” is independent of your search code,
  not of the crate a replay here also runs;
- `REPRODUCE.md`’s timings and the provenance note describe other bundles or themselves.

**Two matters in your favour.** Rebuilding the 197/200 mutant from the candidate by your
shipped script’s rule reproduces the input digest the control log records, so the
control is bound to the candidate.
And the pre-publication receipt’s 4,306 seconds, against the check2 run’s 1,057.9, set
it apart from that run, which is what a second complete run would look like.

## 0. What Was Read, Run and Not Reached

**Read in full.**

- In this repository:
  - bead think-1lri, and the notes of think-r333;
  - the packet’s `README.md`, `source-manifest.json` and
    `acquisition/release-assets.json`, at `6a02a660e` and again at `c03183f66`, where
    #903 changed only the README’s tables of stored files and the manifest’s `raw_bytes`
    fields;
  - in `result-import.md`, stage 4;
  - in `epistemics.md`: Verification, Confirmation, Which Code Confirmed It, The
    Independence Record, The Independence Ladder, Every Run’s Code Is Kept, Review
    Records, and Scope and Composition;
  - T-132’s register entry, `E-wand125-fine-net-n29-582-followup-report` and
    `V-wand125-sqverify-proof-net`;
  - the frontmatter of `n-029.md`, for the bounds on record.
- In `packing/sqverify_fast/SOUNDNESS.md`, at `main`: the claim, N1 to N4, Declared Nets
  (lemma N0), C1, A1, A2, the oblique lemmas R1 to R5 and the acceptance rule, lemma D,
  B5, Z1, Z2, I1, I2, F2, F3, R6, R7, A3 and the list of tests; and the commit
  `8bf4b5748` that made N2 fold square by square.
- In the crate: `build.rs`; and in `certificate.rs` at `e020eb1e2`, `admit`,
  `domain_upper` and `direction`. This review did not read `axis.rs`, `rotated.rs`,
  `interval.rs` or `lib.rs`. Its oblique decision (§4) was written without reading the
  crate’s search code; its axis decision (§3) adapts the precedent’s, whose authors read
  `axis.rs`.
- In the census tools, read and not run: the header of `devtools/sqverify_fast_axis.py`
  and `axis_captures_agree` in `devtools/sqverify_fast_census.py`.
- From the source, as data:
  - the eleven pinned documents (`README.md`, `bundle.json`, `ASSET.json`,
    `files-sha256.json`, `SPEC.md`, `REPRODUCE.md`, `fine_net_check.sh`,
    `UPSTREAM_COMMIT`, `provenance/search-notes.md`, and `SOUNDNESS.md` and
    `INDEPENDENCE.md`, each identified by its Git blob) and the enclosing `LICENSE`;
  - the candidate, the check2 receipt, `control.json`, the run log, the control log and
    the pre-publication receipt;
  - the sealed bundle’s member list and README;
  - the nested verifier archive’s `certificate.rs` hunk against `e020eb1e2`, and its
    `SOUNDNESS.md` and `README.md` additions, read in memory and not retained.

**Route reviews read, none of them a review of this result.**

- The
  [declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md)
  of 6 October, whole, including its checklist (b).
- The 4 November review of `mixed_n28_L57425` and `mixed_n30_L58925` (bead think-4ul6),
  whole, with its programs, as the brief’s structural precedent.
  It is not yet on `main`. Its programs were re-read line by line and adapted (§7), and
  its conclusions were not taken over: every number in this review was recomputed for
  this certificate.
- The
  [14 October fine-net review](review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md):
  its outline, §2’s list of what an instance cannot discharge, and §5 on the axis
  tolerance.
- The [23 October #446 review](review-2026-10-23-wand125-446-fine-net.md): its outline
  and opening.
- The
  [3 November review of Özden’s dilated measure](review-2026-11-03-ozden-s94-dilated-measure.md):
  its F1 and F2, found while tracing main’s change to N2.

**Run.** The programs written for this review, kept with their outputs for the packet’s
`review/` directory and listed in §7, and the reviewed `sqverify-fast`, driven by one of
them. Outside the programs, these commands also ran:

- `cargo build --release --locked -j 2` of the crate, in the worktree, at `nice -n 19`;
- `git ls-remote origin 'refs/heads/wand125*' 'refs/heads/*proof-net*'`, read-only;
- `curl` fetches of the asset, the eleven documents and the `LICENSE`, each held to its
  pin by the programs.

Everything ran at `nice -n 19` on at most two cores, beside another lane’s census.

**Not reached.**

- A complete capture of the certificate.
- The census’s whole-net 99/100 control and near-threshold mutant, which the import lane
  runs after this review.
- The upper end of the axis sweep’s enclosure at the 99/100 mutant’s vertex, which the
  census’s enclosure rule compares with (§3).
- The author’s C++ checker of the earlier bundles, which no one has run on this
  candidate.
- The nested archive’s 55 added test lines, which were counted and not read.
- The intake lane’s receipts (`receipts/premises.json`,
  `receipts/sample-diagnostic.json`) and the packet’s `reported-n29-followup.json`. They
  were left unopened until §§1 to 11 were written, to keep this review apart from that
  lane’s conclusions, and are compared in §12. The packet README’s summary of them was
  read first (§13).

## 1. The Claim

No packing of 29 closed unit squares with pairwise disjoint interiors lies in the closed
square $K = [0, L]^2$, $L = 291/50$. Hence $s(29) > 291/50$, and in particular
$s(29) \ge 291/50$. This is `T-132`.

The claim is the theorem of `SOUNDNESS.md` (“The Claim”) on the net the candidate
declares, with these hypotheses:

- **(H1) The measure.** The rows $R_j = [x_1, x_2] \times [y_1, y_2] \subseteq K$ carry
  masses $w_j > 0$, all exact rationals, and the density is
  $g = \sum_j \frac{w_j}{8|R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)}$. The total is
  $M = \sum_j w_j = 29 - 1/100000 < 29$.
- **(H2) The net.** $B = 4999/5000$, $D = 1/5002$ and $N_\theta = 2073$ satisfy lemma
  N0’s (a) to (e): $2 \le N_\theta \le 2^{16}$; $B(1 + D) < 1$; $t_{\max} = 2072 D$ has
  $t_{\max}^2 + 2t_{\max} - 1 > 0$; $t_{\max} \le 1/2$; and $B(1 + D/(1 - D^2/4)) < 1$.
- **(H3) The coverage.** For every node $r = 0, \ldots, 2072$ and every centre $c$ of
  the per-bin domain $[\rho(a_r), L - \rho(a_r)]^2$, the closed square $Q_r(c)$ of side
  $B$ at angle $\theta_r = 2\arctan(rD)$ has $\int_{Q_r(c)} g \ge 1$. Here
  $a_r = \max(0, rD - D/2)$ and $\rho(a) = (1 + 2a - a^2)/(2(1 + a^2))$. This is the
  statement the author’s run decides.
- **(H4) The fold.** Every $a_r$ lies below $\tan(\pi/8)$, and the last bin
  $[2071.5\,D, 2072.5\,D]$ contains $\tan(\pi/8)$.

**Against the record.**

- The claim is above `T-108`’s $581/100$, the reported and verified lower bound at
  $n = 29$, by $1/100$.
- It is above the $1163/200$ that jlevy/squares#446 reported on 8 October, by $1/200$,
  and above the author’s unreported `mixed_n29_L58175` ($2327/400$), by $1/400$.
- It is below the upper bound on record, $5.9338334626\ldots$, reported and verified, by
  $0.1138$.

## 2. The Argument, Re-derived

The argument is the theorem’s proof in `SOUNDNESS.md`, read with lemma N0 in place of
the standard net’s constants and with main’s fold square by square.
Every value below was recomputed here (`check_candidate.py`).

**N1, the net.** The half-angle tangents $t_r = r/5002$ are $D$ apart, so every
$t \in [0, 2072.5\,D]$ is within $D/2$ of a node.
The endpoint is $t_{\max} = 2072/5002 = 1036/2501$, and
$t_{\max}^2 + 2t_{\max} - 1 = 367/6255001 > 0$. So $t_{\max} > \tan(\pi/8)$, by
$2.07 \times 10^{-5}$ in the tangent.

**N2, the orientation, one square at a time.** Take a unit square of the packing, with
angle $\varphi \in [0, \pi/2)$.

- If $\varphi > \pi/4$, let $\sigma$ be the reflection in $y = x$. It maps $K$ to itself
  and $g$ to itself, by $D_4$ invariance, and $\sigma$ of the square has angle
  $\pi/2 - \varphi < \pi/4$. A core found for $\sigma$ of the square, reflected back,
  lies in the square and captures the same mass.
- So each square has a core of its own, whatever the angles of the others.
  The cores lie in the squares’ open interiors, which are disjoint.
- For $\varphi \in [0, \pi/4]$, $t = \tan(\varphi/2) \le \tan(\pi/8) < 2072.5\,D$. With
  $r$ the nearest node, $z = \tan(\delta/2) = |t - t_r|/(1 + t\,t_r) \le D/2$.

One reflection of the whole configuration, as the bundle’s `SOUNDNESS.md` and `SPEC.md`
word it, cannot fold a packing with squares on both sides of $\pi/4$ (F-1).

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
  $1 - 2a - a^2$, positive on $[0, \sqrt 2 - 1)$. With $a_r \le t \le \tan(\pi/8)$ this
  gives $\rho(t) \ge \rho(a_r)$, so the square’s centre, which is the core’s, lies in
  $[\rho(a_r), L - \rho(a_r)]^2$.
- The largest $a_r$ is $a_{2072} = 4143/10004$, where
  $a^2 + 2a - 1 = -22423/100080016 < 0$; the last bin’s upper end $4145/10004$ is past
  $\tan(\pi/8)$. So (H4) holds, and the fold at $\pi/4$ is what makes the last bin
  sound: a square between $\tan(\pi/8)$ and $2072.5\,D$ would have a smaller $\rho$ than
  $\rho(a_{2072}) = 0.70710677\ldots$.
- $\rho(a_r)$ increases strictly over all 2,073 nodes, from $\rho(0) = 1/2$. At every
  node it is at least Tokoharu’s $B(c_r + s_r)/2$, by $1.1 \times 10^{-7}$ at the least,
  so a core centred at the domain’s corner lies in $K$ and the per-bin domain is the
  smaller of the two. Its least width is $4.406$, at node 2072.

**C1, the quarter turn.** The rotation $T$ by $\pi/2$ about $(L/2, L/2)$ preserves $g$
and carries $Q_r(c)$ to $Q_r(Tc)$, so the crate checks only the quadrant
$[L/2, L - \rho(a_r)]^2$. The decisions made here (§§3 and 4) cover the whole domain and
do not use C1. `selftest.py` checks the invariance on the evaluator, and that a
reflection does not preserve an oblique capture.

**N4, the count.** The 29 cores are pairwise disjoint closed subsets of $K$, each of
$g$-measure at least one by (H3). So $29 \le \int_K g = M = 29 - 1/100000$, a
contradiction.

**The two methods of the source’s run.**

- At $r = 0$ the crate runs the vertex sweep (lemmas A1 and A2) on the quadrant’s event
  grid, $4{,}291^2 = 18{,}412{,}681$ vertices here.
- At $r \ge 1$ it runs the interval branch and bound, with the release audit at every
  1,024th box (A3).
- Lemma F3’s caps hold with room.
  The densest image density is 50,974, against $2^{96}$; eight times the densest row is
  $3.26 \times 10^6$, against $2^{32}$; $s_1 = 3.998 \times 10^{-4} > 2^{-18}$; and
  $c_{2072} = 5181705/7328297 \ge 3/5$.
- Every row has both sides at least $0.0010000013$. No rectangle is nearer than $0.361$
  to a wall. Every coordinate is a decimal on the grid $10^{-17}$.

**The instance.** Every value in the table was recomputed here by the programs of §7,
apart from the crate and the tools:

| Premise | Value |
| --- | --- |
| Candidate SHA-256; semantic digest by REPRODUCE.md’s rule; the retained `.gz` | `c9171c92…`; `377bcd7b…`; `16750ea3…` |
| Rows, all positive, inside $K$ and nondegenerate; repeated rectangles | 650; none |
| Images; distinct (the crate’s `expanded_rectangles`) | 5,200; 5,156, eleven rows having coincident images |
| Mass, equal to `total_mass` and to $29 - 1/100000$ | $2899999/100000$ |
| `proof_net` exactly `{step, last}`; no `net`, `certificate`, `schema` or `scaling_factor` key; `points` empty; no duplicate key; every number a canonical decimal or ratio | yes |
| Lemma N0 (a) to (e) and (H4) | hold |
| Per-bin domain’s least width, at node 2072 | 4.406 |
| Source run: directions, all `verified` at threshold `1` | 2,073 |
| Source run: nodes; direction CPU; wall at 12 threads | 649,871,818; 12,615.9 s; 1,057.6 s |
| Source run read the published candidate (`input_sha256`) | yes |
| Least certified oblique bound, at direction | 1.0000000000047 (1947) |
| Axis: the source’s certified bound; the exact capture at its vertex | 1.000873084701422; 1.0008730852291343 |
| Direction 0 decided here over $[1/2, 133/25]^2$: least vertex, exact | 1.0008730852291343 |
| Oblique directions decided here over their whole per-bin domains (1, 312, 603, 886, 1173, 1595, 1947, 2068, 2072) | 9 of 9 verified; least capture found 1.000583 (direction 886) |
| The 12 tightest directions: exact capture at each leaf box’s centre and corners | all at least the bound and 1; least 1.000990 (direction 886) |
| Control (197/200): refusals; witnesses in the domain, below 1, equal to the crate’s | 32; all 31 (axis exact 0.98586) |
| Control mutant rebuilt from the candidate by the shipped rule: SHA-256 equal to the log’s input | `8e786a9c…`, yes |
| Sampled here by the reviewed crate: rows equal to the source’s | 7 of 7 |

**What this instance cannot discharge from retained material.**

1. **The coverage (H3).** The author’s run decides it at all 2,073 directions; its log
   is retained and was read here direction by direction.
   Here it has been decided at ten directions, direction 0 and nine oblique ones, by
   this review’s own code, and at seven of those nine the reviewed crate reproduced the
   author’s row exactly.
   Until a complete census from reviewed source runs, (H3) at the other directions is
   the author’s report.
2. **The author’s build.** The binary `ec04d332…` cannot be rebuilt from retained bytes,
   since the archive is pinned and not retained.
   This review recomputed the archive’s build digest `ab6e33e1…` from the asset fetched
   again (§6), which ties the receipts to those bytes.
3. **The controls.** The author’s 32-direction 197/200 control was checked here in full
   (§5). The census’s whole-net control (FC-1) has not run.

Everything else the theorem needs holds exactly in the retained and pinned material.

## 3. Direction 0, Decided Here

`axis_decide.py` decides direction 0 over the whole per-bin domain $[1/2, 133/25]^2$,
without the quarter-turn reduction.
The method was derived for this review from lemma A1’s mathematics, not from `axis.rs`,
which this review did not read.

1. **Vertices suffice.** $F(x, y) = \sum_k g_k\, o^x_k(x)\, o^y_k(y)$, summed over all
   eight images of every row (unmerged), with $g_k$ the image’s density,
   $o^x_k(x) = \lvert[x - h, x + h] \cap [x_1, x_2]\rvert$ and $h = B/2$.
   - Each $o^x_k$ is continuous and affine between consecutive points of
     $\{x_1 \pm h, x_2 \pm h\}$.
   - On each cell of the grid $E \times E$, where $E$ holds every such point inside the
     domain and the domain’s two ends, $F$ is bilinear.
     Its minimum over the closed cell is therefore at a corner.
2. **Exact overlaps.** Every event and edge is an integer multiple of $1/S$, with
   $S = 10^{17}$, so every overlap is exact in int64.
3. **A proved error bound.** Each vertex value is a dot product of nonnegative terms
   $(g_k/S^2)\,O^x_k\,O^y_k$, with $O^x_k = S\,o^x_k$ and $O^y_k = S\,o^y_k$ the integer
   overlaps. Three correctly rounded inputs, one rounded product and a $K$-term dot
   product in any summation order give $\hat F = \sum_k t_k (1 + \theta_k)$ with
   $\lvert\theta_k\rvert \le \gamma_{K+4}$, so $F \ge \hat F/(1 + \gamma_{K+4})$.
   - The grid is certified when the least $\hat F$, read exactly as a rational, is at
     least $1 + \gamma_{K+4}$: an exact comparison, where the precedent compared in
     binary64.
   - The bound needs no subnormal term, and none arises: the least positive term, at one
     unit of overlap on each axis, is $6.0 \times 10^{-37}$.
4. **Exact checks.** The 24 lowest vertices, the least vertex’s orbit under $D_4$, 40
   random vertices and the source’s reported vertex are evaluated in fractions.

| Quantity | Value |
| --- | --- |
| Events per axis; vertices | 8,580; 73,616,400 |
| Events per axis in the quadrant $[L/2, L - 1/2]$, counted as lemma A1 defines them | 4,291, the crate’s `x_events` and `y_events` |
| $\gamma_{K+4}$; worst relative binary64 error seen at the exact checks | $5.8 \times 10^{-13}$; $3.5 \times 10^{-16}$ |
| Least vertex value, exact; certified lower end | 1.0008730852291343; 1.0008730852285557 |
| Vertices where it falls | a plateau, among them the orbit of $(1/2, 2.4994977524465363)$: eight vertices, one value |
| The source’s argmin $(3.3205022475534637, 133/25)$, on the domain’s upper edge, is in that orbit | yes |
| The source’s certified bound, below the exact capture by | $5.28 \times 10^{-10}$ |
| Vertices below 1.001; below 1.002; below 1.005 | 1,660; 162,648; 371,076 |
| Verdict | verified |
| CPU; wall | 16.5 s; 10.0 s |

**The mutants.** Each mutant’s capture is the factor times the original’s, so each
mutant’s least vertex is the same, and its refusal there is exact:

- 197/200: 0.9858599889506973;
- 99/100: 0.9908643543768428.

The source’s 197/200 axis row reports a bound $5.20 \times 10^{-10}$ below its exact
value. The reviewed crate’s 99/100 axis row, run here, reports a bound
$5.23 \times 10^{-10}$ below.
Every axis bound read here lies below its exact capture, on the side soundness needs.

The census control’s axis rule now accepts a refusal when the exact capture lies in the
enclosure the sweep held at that vertex (#892, `axis_captures_agree`): the walk’s lower
end must equal the crate’s bound to the bit, and the capture must lie in the walk’s
interval.
This review did not compute that interval’s upper end, so it does not say which
way that leg falls.
It says only that the refusal is mathematically sound: the capture is
below one at a vertex of the closed domain, and the bound is below the capture (F-8).

**What the slack looks like.** Direction 0’s least capture is 1.000873, decided exactly.
At the oblique directions decided here the least found is lower: 1.000583 at direction
886, 1.000708 at direction 603, 1.000714 at direction 2068, 1.000718 at direction 1947
(§4). So the certificate’s slack is at most $5.83 \times 10^{-4}$ at direction 886; that
is an upper end, not the minimum.
The least certified oblique bounds, $1 + 5 \times 10^{-12}$ or so, are the branch and
bound’s termination margin, not the measure’s slack.

## 4. Oblique Directions, Decided Here

`oblique_decide.py` decides a direction $r \ge 1$ over its whole per-bin domain
$[\rho(a_r), L - \rho(a_r)]^2$, without the quarter turn.
It was written for this review from the claim’s definitions.
It shares no code with the crate and uses no lemma of the crate’s search, which bounds a
derivative (R3 to R5); its one borrowed idea, a concave section bounded by trapezoids,
is lemma R2’s, which this lane read.

1. **The bound over a box (lemma S).** For a box of centres
   $C = [c_x \pm d_x] \times [c_y \pm d_y]$, the rotated rectangle
   $Q'' = \{q : \lvert u \cdot (q - p_0)\rvert \le h - (c\,d_x + s\,d_y),\
   \lvert v \cdot (q - p_0)\rvert \le h - (s\,d_x + c\,d_y)\}$, with $u = (c, s)$,
   $v = (-s, c)$ and $p_0$ the box’s centre, lies in the core $Q(p)$ of every $p \in C$,
   by the triangle inequality.
   Since $g \ge 0$, every $p \in C$ has $F(p) \ge \int_{Q''} g$. Nothing about
   derivatives is used.
2. **Areas from below (lemmas E and I).** $\int_{Q''} g$ is a sum over images of a
   density times $\lvert R \cap Q''\rvert$. That area is $\int \max(0, \eta(\xi))\,d\xi$
   over $R$’s abscissae, where $\eta$, the vertical section’s length, is a minimum of
   affine functions minus a maximum of affine functions, so concave.
   A trapezoid sum of lower bounds of $\eta$ at any nodes inside $R$’s range is below
   the area.
   - The nodes sit at the approximate breakpoints, the four vertices and the eight
     crossings with $R$’s top and bottom, so the sum is nearly exact.
     Their accuracy affects only tightness.
   - Every operation is one correctly rounded binary64 operation moved outward by one
     ulp (`numpy.nextafter`). $c$ and $s$ enter as enclosures of the exact rationals,
     the half-sizes rounded down, and $R$ as its inner binary64 rectangle, so every
     replacement is a subset.
   - The weighted sum over images, of nonnegative lower bounds in any order, is
     multiplied by $1 - 2\gamma_K$.
3. **Classification (lemma C).** In binary64 with slack $10^{-12}$, far above the
   $10^{-14}$ error of the quantities tested: an image whose outer binary64 rectangle
   lies in $Q''$ contributes its exact mass $m/8$ rounded down; one that misses the
   superset square of half-sizes $h + c\,d_x + s\,d_y$ and $h + s\,d_x + c\,d_y$ meets
   no core of the box and is dropped for its children too; the rest go through 2.
4. **The search.** A box is accepted when its bound is at least 1, and otherwise split:
   across its longer side, or with `--split adaptive` across the side whose halving at
   the same centre raises its bound more, which is an order of search and accepts
   nothing. At depth 20 and below, a failing box’s centre is screened by the full core’s
   bound, and a possible counterexample is evaluated exactly in fractions: a capture
   below one at a centre in the domain refutes the direction.
   The least screened centre is also evaluated exactly, which gives each direction an
   exact upper end for its least capture.

**The tests** (`oblique_selftest.py`, nine passes):

- the area bound against exact rational clipping on 3,000 random pairs, thin rectangles,
  large ones and ones crossing a vertex among them: never above the exact area, and
  within $1.9 \times 10^{-15}$ of it;
- two seeded errors, a core 0.01% too wide and nodes past the rectangle, each caught
  above the exact area at about 175 of 600 pairs;
- the box bound on the candidate’s own measure, at 24 random boxes over five directions:
  at most the exact capture at the box’s centre, its four corners and three random
  interior points;
- the centre screen, within $1.9 \times 10^{-12}$ below the exact capture.

The tests also cover a second bound kept beside the first, lemma Q of the docstring.
By the Brunn–Minkowski inequality, $\lvert R \cap (Q_0 + p)\rvert^{1/2}$ is concave in
the translation $p$ wherever the two meet, so each image’s capture over a box is least
at a corner. The bound was checked exactly at 1,600 interior points.
It is never weaker than lemma S, but it costs four area evaluations an image where S
costs one. At direction 312 it needed 49,029 boxes against S’s 51,001, at 62.4 against
18.8 CPU-seconds, so the decisions below use S.

**The decisions.** Every direction run was verified over its whole per-bin domain:

| Direction (angle) | Split | Boxes; greatest depth | CPU (s) | Least capture found, exact | Source: nodes; CPU (s) |
| --- | --- | --- | --- | --- | --- |
| 1 (0.02°) | adaptive | 35,487; 34 | 35.1 | 1.0009817 | 192,311; 2.9 |
| 312 (7.14°) | adaptive | 35,607; 30 | 29.0 | 1.0009319 | 211,919; 3.3 |
| 603 (13.75°) | adaptive | 74,535; 32 | 67.6 | 1.0007081 | 226,303; 4.2 |
| 886 (20.09°) | longer | 306,739; 32 | 155.5 | 1.0005828 | 295,115; 6.0 |
| 1173 (26.40°) | adaptive | 382,679; 32 | 326.6 | 1.0007765 | 349,637; 6.4 |
| 1595 (35.37°) | longer | 399,019; 30 | 184.3 | 1.0008154 | 384,671; 8.3 |
| 1947 (42.54°) | longer | 615,811; 31 | 322.7 | 1.0007177 | 448,209; 9.8 |
| 2068 (44.92°) | longer | 972,979; 31 | 518.8 | 1.0007141 | 472,517; 10.4 |
| 2072 (45.00°) | longer | 975,021; 31 | 521.7 | 1.0007196 | 472,383; 7.5 |

In all, 2,161.4 CPU-seconds for the nine directions.
The least capture found is the exact capture at the least of the centres the search
screened, an upper end for the direction’s minimum and not the minimum itself.

**The controls.**

- The 99/100 mutant at direction 1947 is refuted in 7.4 CPU-seconds, at depth 20: the
  screen found the centre $(0.7085998344818537, 0.7085998344818537)$, in the domain near
  its lower corner, where the mutant’s exact capture is $0.99100523\ldots < 1$.
- The measure scaled by $9991/10000$ at direction 312 is refuted in 13.4 CPU-seconds,
  with an exact capture of $0.9999948560\ldots < 1$ at a centre in the domain.
  That scale must be refuted: at the least centre the $9993/10000$ run screened, the
  original’s exact capture is $1.0008771\ldots$, which the scale takes to
  $0.9999763\ldots < 1$.
- The measure scaled by $9993/10000$ at direction 312 is verified after 45,367 boxes and
  31.8 CPU-seconds. Its least screened capture is $1.0001765\ldots$, so the search
  resolved a margin of at most $1.8 \times 10^{-4}$, and the original’s least capture at
  312 lies between $10000/9993 = 1.0007005\ldots$ and $1.0008771\ldots$.

**What the decisions show.** At each of the nine directions, (H3) holds over the whole
per-bin domain, decided by code that shares nothing with the crate.
The decisions are a sample: 9 of the 2,072 oblique directions, among them the four whose
certified bounds were least in the author’s run, the one with the most nodes, the net’s
first and last, and the one whose least-bound leaf captured least.
The cost is 9 to 69 times the crate’s CPU per direction.
The bound is of order zero, so it takes no credit for the cancellation a derivative
bound sums when a band entering one side of the core leaves by the other; that is the
likely reason. Splitting a box where its bound gains more (`--split adaptive`), rather
than across its longer side, cut direction 1 from more than 560 CPU-seconds unfinished
to 35. The least captures found show that the slack at some oblique angles is smaller
than at direction 0: under $6 \times 10^{-4}$ at direction 886, against
$8.7 \times 10^{-4}$ at direction 0.

## 5. The Source’s Records

**The run log** (`check_source_logs.py`).

- The log has 2,074 lines: one row per direction for 0 to 2072, each once, and the
  summary last. The rows are not in index order, as twelve threads wrote them.
- Every row is `verified` at threshold `1`. The axis was decided by the vertex sweep and
  every other direction by branch and bound, each with at least one audit at
  `audit_every` 1,024. No row carries a witness.
- The summary’s nodes, direction CPU and direction seconds equal the rows’ sums.
- Its premises equal this review’s recomputation, key for key: `B`, `D`, `L`,
  `angle_count` 2073, `centre_domain` `per-bin`, `format` `M`, `input_sha256` (the
  published candidate’s), the masses, `source_rectangles` 650, and `expanded_rectangles`
  5,156, which is the distinct images counted here.
- The summary’s status is `VERIFIED`, `refused_directions` is empty and
  `fault_injected_at_box` is null.
- The author’s build predates the summary fields `net_origin`, `net_last_tangent` and
  `shrink_bound`. Its `D` and `angle_count` show the declared net was read.
  The reviewed build’s summary, run here, carries all three, as the checklist’s item 3
  wants (§10).
- The least oblique bound is at direction 1947, the most nodes at 2068 (472,517) and the
  fewest 191,843. Maximum depth 33. The direction CPU, 12,615.9 s, is 0.994 of twelve
  threads’ wall, so the run had its cores to itself.

**The receipts.**

- `check2/receipt.json` wraps an inner `fine-net-check2-receipt/v1`. That receipt’s
  fields match the candidate, the log and each other: $n$, `L` and `B` as the
  candidate’s own strings `5.82` and `0.9998`, the net, the mass, 2,073 expected,
  checked and verified, the digests, `PASS`, 12 threads, start 2026-10-09T22:57:00Z,
  1,057.9 s, and the verifier’s source `ab6e33e1…` and binary `ec04d332…`. Its
  `verifier_summary` equals the log’s summary line.
- `control.json` is the inner receipt’s control plus the source digest.
- `bundle.json`’s net block holds exactly, as do its candidate and receipt digests, its
  verifier sources against the sealed bundle, and its stated improvement: `endpoint`
  $1036/2501$, `endpoint_check` $367/6255001$, `rotated_side_upper` $25009997/25010000$,
  the margins $3/25010000$ and $3/50020000$, and $1/400$ over $2327/400$.
- The README states the digest, the mass and the 2,073 directions.

**Two reported complete runs, one with its log.**

- **The check2 run.** Its log, receipt and summary agree, as above.
- **The pre-publication run.** `verification/prepublication-receipt.json` is in the
  shape the shipped `fine_net_check.sh` writes: a `build` block, integer `seconds`, the
  control as “every mass x 0.985, 32 directions”, and no start time, thread count or
  binary digest. Its `build` block equals the log summary’s, its digests the candidate’s,
  and its control outcome the check2 control’s (32 refused, 31 with an exact capture
  below one).
- It states 4,306 s, against the check2 run’s 1,057.9 s, and the README says it ran on
  “a fresh Ubuntu 24.04.5 LTS (x86_64), Rust 1.98.0 machine”.
- So, unlike the n = 28 receipt of the precedent, it cannot be the check2 run’s own
  record. It is what a second complete run of the shipped script on a slower machine
  would write. No log of it is shipped, so it is an attributed outcome (F-4).

**The control** (`check2/control-197_200.jsonl.gz`).

- **The directions.** It ran at the 32 directions $\mathrm{round}(2072\,i/31)$,
  $i = 0, \ldots, 31$, the shipped script’s rule.
- **The mutant.** Its summary’s mass is exactly $197/200$ of the candidate’s, and every
  other premise and the build are the run’s.
- **The mutant’s identity.** The log’s `input_sha256`, `8e786a9c…`, names the mutant
  file, which the bundle does not ship.
  Rebuilding it by the shipped script’s rule reproduces that digest exactly:
  `json.load`, every mass times $985/1000$ written as `str(Fraction)`, `total_mass`
  re-summed, and `json.dump` with its defaults.
  So the control is bound to the candidate.
- **The 31 oblique refusals.** Each is a `counterexample-candidate`. Each witness pose
  is the stopping box’s centre, in the per-bin domain and in the quadrant.
  Its exact capture of the 197/200 measure, recomputed here, equals the crate’s
  `exact_coverage` digit for digit and is below one, from 0.99446 to 0.9999999998. The
  original captures at least 1.0096 at those poses.
- **Witnesses near one.** Nine witnesses lie within $1.04 \times 10^{-9}$ of one, eight
  of them within $10^{-9}$. Every one of the nine stopped at the depth limit of 60,
  where the search evaluates the first deep boxes’ centres exactly; a centre so close to
  one cannot trigger the estimate’s refusal.
  The other 22 stopped at depths 20 to 31, below one by $4.4 \times 10^{-5}$ to
  $5.5 \times 10^{-3}$. All 31 are exact refutations.
- **The axis refusal.** It carries no exact value in the log.
  Its exact value is in §3, below one at a vertex of the closed domain.

All 32 refusals are genuine.
The shipped script would pass a control with a single exact refutation
(`exact_below_threshold > 0`), so the control as designed shows only that the check is
not vacuous. This one does better than its rule asks.

## 6. Trust Boundaries

| Checker | Decides | Trusts | Shares with the others |
| --- | --- | --- | --- |
| The author’s nested crate: archive `e495f9bf…`, build `ab6e33e1…`, binary `ec04d332…` | (H3) at all 2,073 directions, in the author’s logged run | binary64 without FMA (I1), `enclose` (I2), lemmas R1 to R6, A1, A2, D and N0, and its own 32-line reading of `proof_net` | `e020eb1e2`’s source `7c49cf79…` with `certificate.rs` +32 −2; every other `src/` file, the lockfile, `build.rs` and the toolchain pin byte-identical to `e020eb1e2`, and so to the reviewed kernel |
| `sqverify-fast`, this repository, source `d97758bb…` (reviewed 3 and 6 October), binary `567a0fd5…` | (H3) at the seven directions run here, and the 99/100 mutant’s refusal at three | the same lemmas, and main’s lemma N0 reader | with the author’s crate, every `src/` file but `certificate.rs`, `lib.rs` (three summary lines) and `rotated_tests.rs` (one line): the same kernel |
| This review’s `axis_decide.py` | direction 0 over the whole per-bin domain | Python fractions; int64 overlaps; binary64 dot products under the proved bound $\gamma_{K+4}$ (OpenBLAS, any order) | nothing: written from lemma A1’s mathematics, importing nothing |
| This review’s `oblique_decide.py` | (H3) at the nine oblique directions it ran, each over its whole per-bin domain; the 99/100 mutant’s refutation at direction 1947; and the two scaled controls at 312 | Python fractions for the net, the measure and the witnesses; binary64 with every operation moved outward by one ulp (`numpy.nextafter`); lemmas S, E, I and C of its docstring | nothing: written for this review from the claim’s definitions and lemma R2’s idea of a concave section; no derivative bound and no code of the crate |
| This review’s `fine_net_exact.capture` | the capture at the poses evaluated (§7) | Python fractions | nothing; written from the claim’s definition of the density |
| This review’s premise programs | nothing: exact premises, custody, records | fractions, SHA-256, `git show` | nothing |
| The census control’s evaluator `check_sqverify_fast.mixed_exact` | the mutant’s capture at the crate’s witnesses, in the whole-net control | fractions and `sqpack`’s exact clipping | not run here |

**What the author’s crate is.** `custody_and_nested.py` read the archive inside the
re-fetched asset and recomputed, by the crate’s `build.rs` rule, the `source_sha256` a
build embeds. It is `ab6e33e1…`, the digest every receipt and summary names, so the
receipts are runs of those bytes.

Against the reviewed source `e020eb1e2` (`7c49cf79…`), 16 of the archive’s 20 files are
byte-identical: `src/axis.rs`, `exact.rs`, `interval.rs`, `lib.rs`, `main.rs`,
`oracle.rs`, `rotated.rs` and `rotated_tests.rs`, together with `Cargo.toml`,
`Cargo.lock`, `build.rs`, the toolchain pin, `clippy.toml`, `.gitignore` and the two
independence files. The other four differ:

- `src/certificate.rs`, by 32 added and 2 changed lines;
- `tests/adversarial.rs`, by 55 added lines;
- `README.md`, by 5 added and 2 changed lines;
- `SOUNDNESS.md`, by 11 added lines.

I read the `certificate.rs` hunk and `e020eb1e2`’s `admit` around it.

- When a file carries `proof_net`, the block must be an object with exactly `step` and
  `last`, and no `certificate` metadata may sit beside it.
  `step` is read as an exact rational and `last` as a `u32` plus one, into the same
  `step` and `angle_count` the rest of `admit` reads.
- The checks that follow at `e020eb1e2` are lemma N0’s (a) to (d) on those values, then,
  once the format is known, the refusal of a declared net outside format M and, for the
  per-bin domain, the tangent form (e).
- `domain_upper` and `direction` read the same `step`: $a = t - D/2$ for $t > D/2$, else
  0, and $U_r = L - \rho(a)$.
- The archive keeps `e020eb1e2`’s duplicate-key reader, which is byte-identical to
  main’s. Compared with main’s declared-net reader, the archive lacks the optional
  `count` field and DN-5’s refusal of a top-level `net` key outside format L. The
  candidate has neither key, and this review’s own reader found no duplicate key.

The 11 `SOUNDNESS.md` lines restate lemma N0’s premises without its proof (F-1).

Against the head of this tree, the archive’s `src/certificate.rs` is +38 −98, `lib.rs`
−3 and `rotated_tests.rs` −1, and it has no `tests/declared_net.rs`. Those are counts
only; the 6 October review describes main’s side.
The head’s crate digest is still `d97758bb…`.

**What that means for the rung.**

- The author’s run rests on the reviewed kernel and on 34 lines read here.
  What those lines decide, the net and the domain, is observable: the author’s summary
  reports `D` $1/5002$, `angle_count` 2073 and `centre_domain` `per-bin`, and the
  reviewed build, reading the same declaration through main’s lemma N0 reader,
  reproduces the author’s node count, leaves, depth, least bound and least-bound box at
  all seven directions sampled here.
  Those numbers depend on the step, the domain and the search, so the agreement is
  strong consistency, though not review.
- For the record, the author’s run is the reported entry’s evidence, at `V0`, read as
  `same-implementation` with `V-wand125-sqverify-proof-net` deciding.
- A census here from `d97758bb…` would be *re-implemented sharing the producer’s
  components*, as the entry’s `composition` says.
  No second implementation of the oblique search stands beside the kernel at all 2,073
  directions, and a defect in the shared `rotated.rs`, `axis.rs` or `interval.rs` would
  pass both.
- Independent of that kernel stand this review’s exact evaluator, at every pose it
  evaluated, its decision of direction 0, and its decisions of nine oblique directions,
  among them the four least-bound ones, which are independently re-implemented for those
  directions: their bound, search and arithmetic are this review’s.

## 7. Checks Made Here

Every program is kept, with the output it printed, for
[`wand125-fine-net-n29-2026-10-10/review/`](../../../packing/resources/web/wand125-fine-net-n29-2026-10-10/review/README.md).
Its README says what each program read, how to run it and what it printed.
The programs ran under `python3 -I` with the project interpreter, reading the packet and
the asset as data.

| Program | Read | Printed | CPU |
| --- | --- | --- | --- |
| `selftest.py` | synthetic data | nine passes, among them a seeded wrong clip caught and a reflection shown not to preserve an oblique capture | 0.2 s |
| `check_candidate.py` | the retained candidate; the manifest | the table of §2: every exact premise holds | 0.2 s |
| `check_source_logs.py` | the retained run log, control log, receipts, `control.json` and pre-publication receipt | §5: every record consistent; 31 witnesses genuine; 60 leaf poses at least their bound and one; the mutant rebuilt to the logged digest | 4.9 s |
| `axis_decide.py` | the retained candidate; the run and control logs’ axis rows | §3: direction 0 verified over the whole domain | 16.5 s |
| `custody_and_nested.py` | the asset, in memory; the packet; `git show` at `e020eb1e2`, `34e87a86b` and head | custody of every member and retained copy; the sealed bundle against its manifests; the archive’s build digest and file comparison (§6) | 0.3 s |
| `check_source_docs.py` | the eleven fetched documents and the `LICENSE`; the asset; `git show` | the documents equal their pins; `bundle.json` exact; the facts of F-1 to F-7 | 0.1 s |
| `sample_directions.py`, with the reviewed binary | the retained candidate and run log | seven directions equal to the source’s rows; 35 leaf poses at least their bound and one; item 3’s premises; three 99/100 refusals with exact witnesses | binary 38.7 s; Python 2.2 s |
| `oblique_selftest.py` | synthetic data; the retained candidate | nine passes (§4) | 8.8 s |
| `oblique_decide.py`, one run a direction | the retained candidate | §4 | 29.0 to 521.7 s a direction, 2,161.4 s for the nine; the controls in §4 |

The build took 19.8 seconds of wall at two jobs, 26.4 CPU-seconds.
The crate’s sample ran at 0.756 of the author’s CPU on the same directions.

What failed along the way, and what was redone:

- `/usr/bin/time` is not installed, so CPU was taken from `getrusage` inside the
  programs and from the shell’s `time`.
- `main` moved from `6a02a660e` to `c03183f66` (#903) during the review.
  #903 changed only the packet’s README tables and the manifest’s `raw_bytes` fields,
  not the crate or any retained byte; the worktree was moved to `c03183f66`, and the
  cheap programs were run again there for the receipts kept.
- `check_candidate.py`’s first test of a decimal coordinate grid factored the grid’s
  least common multiple by trial division, which a large prime factor would have made
  slow. It was replaced by dividing out 2 and 5 before the first run.
- `oblique_decide.py`’s first run stopped at once: the root’s pair list named one box
  for 5,200 images. Fixed and rerun.
- `oblique_selftest.py`’s first comparison of the two bounds required the corner bound
  to be at least the intersection bound exactly; four of 24 boxes fell short by at most
  $1.8 \times 10^{-14}$, rounding where no image separates them.
  The test now allows $10^{-12}$ and reports the largest gain, $1.5 \times 10^{-2}$.
- The first versions of `oblique_decide.py` processed deep refinements in small numpy
  batches, and the corner bound was first the default.
  Timing runs of those versions at directions 312, 1947, 2068 and 1 were stopped or
  superseded: about 30 CPU-minutes in all, listed in the README. The decisions kept are
  from the batched program, with the intersection bound.

Nothing the brief asked for went unestablished because of a tool or permission failure.

## 8. Findings

No finding is blocking, and none is major.
The grades are for the claim first and the record second.
Line numbers refer to the files at the pinned revision `22a23c8`.

### F-1, minor, in the source: the bundle’s soundness note predates the declared-net lemma, and its fold reflects the whole configuration

`check2/src/SOUNDNESS.md`, listed in `bundle.json`’s `verifier_source_sha256`, is Git
blob `cadf59b6…`: this repository’s edition at `e020eb1e2`, byte for byte.

- It mentions neither `proof_net` nor a declared net, and states the claim for “(here
  $83/40000$ and $201$)” (line 19) and the fold’s reason with $t_{200}$ (line 53). The
  statement the certificate’s admissibility rests on is lemma N0 (main’s `SOUNDNESS.md`,
  “Declared Nets”), which this review used.
- Its N2 folds by “reflect the whole configuration in the diagonal” (line 43). `SPEC.md`
  says the same in other words: the orientations “may be restricted to θ ∈ [0, π/4]”
  because μ is $D_4$-invariant (lines 46 and 47), and `README.md` line 26 says they
  “reduce by D4 symmetry”.
  One reflection cannot fold a packing whose squares lie on both sides of $\pi/4$.
  Main’s `SOUNDNESS.md` has folded square by square since `8bf4b5748` (3 November),
  after F2 of the 3 November review of Özden’s certificate.
- The archive’s own copy adds 11 lines that list the premises admission checks on a
  declared net, without N0’s proof.
  A reader is not told why the fold at $\pi/4$, and not at the net’s end, makes the
  per-bin domain valid.

The mathematics holds (§2): the argument needs one core per square, which the fold
square by square gives.
Fix: ship or cite main’s edition, which has lemma N0 and the fold square by square, or
state the argument for the declared net in the bundle, and reword `SPEC.md` §4’s first
bullet to fold each square separately.

### F-2, minor, in the source: the README names a control file that does not exist

`README.md`, line 15, lists `check2/control.json, check2/control.jsonl.gz`. The shipped
log is `check2/control-197_200.jsonl.gz`, in the asset, in the sealed bundle and in
`files-sha256.json`. No file of the README’s name is in the asset, the sealed bundle or
the pinned directory.

### F-3, minor, in the source: the published receipt was written by a program the bundle does not ship

The shipped `check2/src/fine_net_check.sh` (SHA-256 `a4069c4b…`) writes a receipt with a
`build` field, integer `seconds`, the control kind “every mass x 0.985, 32 directions”
and no `schema` or `tries`. That is the shape of the pre-publication receipt.

The published `check2/receipt.json` instead wraps `fine-net-check2-receipt/v1`, with
`verifier`, decimal `seconds`, a start time, the binary digest and a control given as
`tries` at factor `197/200`. `REPRODUCE.md` names `fine_net_check.py` in
wand125/square-packing-tools at `5fba675` as an alternative source, which is likely the
writer, but the bundle does not carry it.

The outcomes agree, and `candidate_digest` and `status`, which the README asks a
reproducer to compare, sit at the top level of both shapes.
But a reproduction by the bundle’s own steps yields a receipt of another shape than the
one published. Fix: ship the program that wrote the published receipt, or say which
program wrote which.

### F-4, note, in the source and the record: the second complete run has a receipt and no log

`README.md`, line 54, says the candidate “was checked again … on a fresh Ubuntu 24.04.5
LTS (x86_64), Rust 1.98.0 machine … 2073/2073 directions VERIFIED in 4306 s”, and the
sealed edition of the README lacks that section.

The pre-publication receipt states 4,306 s against the check2 run’s 1,057.9 s, so it is
not the check2 run’s own record (§5). It carries no start time, thread count, binary
digest or run log.

So the record can count two reported complete runs, one logged and one attested by a
receipt alone. If the second run’s log was kept, publishing it, with the start time and
the binary digest, would make it citable on the same footing as the first.

### F-5, note, in the source: the stated verifier location is not in jlevy/squares

The receipt’s `verifier` reads “jlevy/squares packing/sqverify_fast, branch
wand125/sqverify-proof-net, commit fe12e036c”, and `check2/src/UPSTREAM_COMMIT` holds
`42534d959…`. jlevy/squares has no such branch: `git ls-remote` on 4 November lists only
`wand125/n17-native-cert` under `wand125/`. This repository’s full clone holds no object
`fe12e036c` and no object `42534d959…`.

The code exists here only as the archive `e495f9bf…` the bundle carries, which this
review read, and, by `REPRODUCE.md`, in wand125/square-packing-tools at `5fba675`. Fix:
name the repository that holds `fe12e036c`.

### F-6, note, in the source: “an independent second-system check”

`check2/receipt.json`’s `checked_by` calls the run “an independent second-system check
(built from the certificate specification only, without reading the search code)”, and
`README.md` line 12 says the same.
That is true of the author’s search code.
The check is this repository’s crate, whose clean room is recorded in
`packing/sqverify_fast/INDEPENDENCE.md`, adapted by the author.

A reader should not take the phrase as independence from the crate a replay here would
also run. That is why §6 reads a census here as sharing the producer’s components.

### F-7, note, in the source: documents that describe other bundles or themselves

- `REPRODUCE.md`, lines 59 to 61, gives times for “832 directions, n around 30” and says
  “n = 29 at L = 5.81 took 584 seconds”.
  Neither is this certificate, whose check took 1,057.9 s at twelve threads and 4,306 s
  on the pre-publication machine.
- `provenance/search-notes.md`, line 3, ends “see provenance/search-notes.md”, itself.
- `README.md`, line 5, compares the bound with the author’s unreported
  `mixed_n29_L58175` ($5.8175$), and `bundle.json`’s `improvement_lower` is $1/400$ over
  it. Against the published record the improvement is $1/100$ over `T-108`’s $581/100$,
  and $1/200$ over the issue’s $1163/200$.

None of these touches the certificate.

### F-8, note, for the records lane: the axis leg of the census control

At the axis vertex $(3.3205022475534637, 133/25)$, on the closed domain’s upper edge,
the exact capture sits above the crate’s certified bound by:

- $5.28 \times 10^{-10}$ for the original;
- $5.20 \times 10^{-10}$ for the 197/200 control;
- $5.23 \times 10^{-10}$ for the 99/100 mutant, run here with the reviewed crate.

Every refusal is sound (§3). #892’s rule judges the census’s axis leg by the enclosure
the sweep held there, which this review did not compute.
Where it has been measured, at s(37), s(39) and s(44) by the 14 October review’s
emulation and at s(94) by #892’s, the exact capture sat at the enclosure’s midpoint; if
it does so here, the enclosure is about $1.05 \times 10^{-9}$ wide and the leg passes.
That is an expectation, not a measurement.
No change is needed in the certificate.

## 9. Questions for the Author

1. Would you ship, in the check2 bundle, main’s `SOUNDNESS.md`, which states lemma N0
   and folds square by square, or your own statement of why the declared net and the
   per-bin domain are admissible, and reword `SPEC.md` §4’s fold to match (F-1)?
2. Would you correct the README’s control file name (F-2), and ship the program that
   wrote the published `fine-net-check2-receipt/v1` receipt (F-3)?
3. Did you keep the pre-publication run’s log?
   If so, would you publish it, with its start time and binary digest (F-4)?
4. Where is commit `fe12e036c` published, and is `fine_net_verifier/` at
   wand125/square-packing-tools `5fba675` byte-identical to the archive `e495f9bf…`
   (F-5)?
5. The README says the candidates “can still be run through the shipped verifier of the
   earlier bundles”. Have you run that C++ checker on this candidate, and at which
   directions?
6. Does the directory’s MIT notice extend to the nested verifier archive, which carries
   no notice of its own?

## 10. Verdict, and What V and C the Evidence Supports

**`mixed_n29_L582` (T-132), $s(29) \ge 291/50$: accept with findings.** The argument
from the certificate to the claim holds, every exact premise holds, and every record of
the source is consistent with the candidate and with every other record.
Direction 0 and nine oblique directions are decided here, over their whole per-bin
domains, by code that shares nothing with the crate; the rest of the coverage is the
author’s run, consistent at every point read.
F-1 to F-8 are minor matters or notes in the source’s documents and the record.
None is a defect of the certificate or of its argument.
In the register’s vocabulary the verdict is `accepted`.

**The rungs.** The entry is `V0/C0`: the cited evidence is the author’s report, and no
replay has run here.
The records lane would record this review in two places:

- as `external_review` (`informally-verified`) on
  `E-wand125-fine-net-n29-582-followup-report`;
- in T-132’s `reviews`, as an adversarial AI review with verdict `accepted`.

It then supports `C1`. `V` stays `V0`.

**To `V3/C3`.** The certificate needs all of the following:

- a complete `sqverify-fast` census from `d97758bb…` at all 2,073 directions, from the
  candidate retained where the census reads it;
- restored positives;
- a `CONTROLS_REFUSED` whole-net receipt (FC-1), with the axis leg judged by #892’s
  enclosure rule;
- this review as the audit record.

The relation would be *re-implemented sharing the producer’s components*. think-r333
prices the run and its controls at 4.3 to 5.5 CPU-hours.
The sample here ran at 0.756 of the author’s CPU on the same directions, against the
intake’s 0.613 on a more loaded host, consistent with that price.
The decisions here are a sample, 10 of 2,073 directions, and set no rung.
Beside the rung they read: sampled, 10 of 2,073 directions, independently re-implemented
after reading the producer’s code, by a Claude agent, a system family the producer also
used.

**The 6 October checklist (b).**

| Item | State | Where |
| --- | --- | --- |
| 1. The file | holds: format M, `points` empty, no `scaling_factor` key (format M reads none), `proof_net` exactly `{step, last}`, no `net`, no metadata; eight times the densest row $3.26 \times 10^6$, at most $2^{32}$ | §2 |
| 2. The case | pending: the census row | census lane |
| 3. The premises | hold in the reviewed build’s summary run here: `M`, `per-bin`, `proof_net`, `D` $1/5002$, `angle_count` 2073, `net_last_tangent` $1036/2501$, `B` $4999/5000$ and `shrink_bound` $25009997/25010000$, mass $29 - 1/100000$, no points or segments, `fault_injected_at_box` null. Lemma N0 recomputed apart from the crate | §§2, 7 |
| 4. The candidate | the retained `.gz` file’s SHA-256 is `16750ea3…`, which the reviewed build reports as `input_sha256`; it decompresses, as one gzip member, to the pinned bytes. `retained_data check` is the census lane’s | §7 |
| 5. The build | `d97758bb…`, profile `release`, rustc 1.98.0, in the run here | §7 |
| 6. The control | pending: the whole-net receipt | census lane |
| 7. The mathematics | this review, accepting the certificate | here |
| 8. The words | for the evidence text: name the declared net’s step $1/5002$ and count 2,073 and the accepted build by the 6 October review, say *re-implemented sharing the producer’s components* for the census, and cite this review beside the route review | records lane |

**Significance.** The draft scores the entry `S3`, and this review confirms it.
It is a further size from one generator, by a certificate kind and route the record
holds at `S3`, with no new technique.
It would be the strongest lower bound on record at $n = 29$, $0.01$ above `T-108`, and
stands $0.1138$ below the verified upper bound.

## 11. Proposed Registry Entries

These are for `packing/frontier/verifiers.yaml`, to be applied by the records lane.
`R` stands for `docs/project/reviews/review-2026-11-04-wand125-fine-net-n29.md` and `P`
for `packing/resources/web/wand125-fine-net-n29-2026-10-10/review/programs`.

```yaml
  - id: V-wand125-n29-review-premises
    program: check_candidate.py, check_source_logs.py, check_source_docs.py and custody_and_nested.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Recomputes, apart from the crate and the tools, every exact premise of the check2
      candidate mixed_n29_L582 on its declared net (the measure and its mass, the
      distinct D4 images, lemma N0's premises and the last bin, the per-bin domain at
      every node, lemma F3's caps, the canonical form of every number, the semantic
      digest); reads the source's run log, receipts, control and pinned documents
      against the candidate, rebuilds the control's mutant to its logged digest, and
      ties the nested verifier archive to its build digest and, file by file, to
      reviewed source.
    source: [P/fine_net_exact.py, P/check_candidate.py, P/check_source_logs.py, P/check_source_docs.py, P/custody_and_nested.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-1lri of the wand125 n29 import (think-r333), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source's commit names Claude as co-author. Written by a Claude agent
          prompted separately from the source and from the intake and replay lanes, in
          files of its own that import nothing from the crate, the tools or the source.
          Adapted from the programs of the n28 and n30 review (think-4ul6), another
          Claude lane, after reading them line by line.
      note: >-
        Written after reading SOUNDNESS.md, the crate's admission (certificate.rs's admit,
        domain_upper and direction) and build.rs, the source's SPEC.md, REPRODUCE.md and
        fine_net_check.sh, and the n28 and n30 review's programs. The producer's checker
        is this repository's crate adapted, so no clean room with respect to it is claimed.

  - id: V-wand125-n29-review-exact-capture
    program: fine_net_exact.capture, driven by check_source_logs.py, sample_directions.py and oblique_decide.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The exact mass a closed core at a given centre and net angle captures from a format
      M measure, by Sutherland-Hodgman clipping of the rotated core against each D4 image
      in fractions. Decides the capture at the poses it evaluated: the 31 oblique
      witnesses of the source's 197/200 control, the 60 leaf poses of the source's 12
      tightest directions, the 35 leaf poses and 2 oblique mutant witnesses of the
      reviewed sqverify-fast's runs here, and the least-capture centres the oblique
      decisions found; it agrees with the crate's exact witnesses digit for digit at all
      33 it was compared with.
    source: [P/fine_net_exact.py, P/check_source_logs.py, P/sample_directions.py, P/oblique_decide.py, P/selftest.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-1lri of the wand125 n29 import (think-r333), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Clipping and areas in fractions, written from the claim's definition of the
        density; no code of the crate's oracle, of mixed_exact or of the source. Adapted
        from the n28 and n30 review's module. This lane read the crate's admission and
        not its oracle.

  - id: V-wand125-n29-review-axis-decision
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
      proved a priori bound gamma_{K+4} (5.8e-13 here, against a margin of 8.7e-4) and
      certified by an exact comparison, and the least vertices, their D4 orbit and a
      random sample evaluated exactly in fractions. Decided direction 0 of
      mixed_n29_L582 verified.
    source: [P/axis_decide.py, P/fine_net_exact.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-1lri of the wand125 n29 import (think-r333), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Its method is lemma A1's mathematics with its own arithmetic: it covers the whole
        domain rather than the quadrant, and certifies by an error bound and exact checks
        rather than interval sweeps. This lane did not read axis.rs, but the program
        adapts the n28 and n30 review's, whose authors read axis.rs before writing it, so
        no clean room is claimed.

  - id: V-wand125-n29-review-oblique-decision
    program: oblique_decide.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [interval-certified, exact-algebraic]
    role: decides
    summary: >-
      Decides one oblique direction of a format M certificate over its whole per-bin
      domain by a branch and bound of its own. A box of centres is accepted when the
      capture of the intersection of its cores, a rotated rectangle, is at least 1, with
      every area bounded below by a concave section and trapezoids in binary64 moved
      outward one ulp at every step (numpy.nextafter), images classified with slack
      1e-12, and possible counterexamples evaluated exactly in fractions. Decided
      nine oblique directions of mixed_n29_L582 verified, among them the four with the
      source's least certified bounds; refuted the 99/100 mutant at direction 1947; and
      at direction 312 refuted the measure scaled by 9991/10000 and verified it scaled by
      9993/10000.
    source: [P/oblique_decide.py, P/fine_net_exact.py, P/oblique_selftest.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review think-1lri of the wand125 n29 import (think-r333), tbd-strong-max tier, maximum reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Written for this review. Its bound uses no derivative, where the crate's search
        bounds one (lemmas R3 to R5), and its interval steps are numpy.nextafter, not the
        crate's lemma I1. Its concave-section area bound takes lemma R2's idea from
        SOUNDNESS.md. This lane read the crate's admission and not its search code
        (rotated.rs, interval.rs, axis.rs).
```

**Evidence entries.** An evidence entry for each thing a run here decided or sampled
would cite these. Each would carry `coverage: {extent: sample, checked: …, of: …}` and
`origin: replayed-here`. Its `relationship_to_generator` would be
`independent-implementation` for the exact captures, the axis decision and the oblique
decisions, and `shared-components` for the directions sampled with the reviewed crate.
The case record at n = 29 would cite them, and no result would.
The entries are:

- the 32 refusals of the 197/200 control (checked 32 of 32, deciding the author’s
  control);
- direction 0 (checked 1 of 2,073, by independent code);
- the nine oblique directions decided here (checked 9 of 2,073, by independent code),
  with the 99/100 mutant’s refutation at direction 1947 and the two scaled runs at
  direction 312 as their controls;
- the seven directions run here with the reviewed crate (checked 7 of 2,073);
- the 60 leaf poses of the source’s 12 tightest directions, a sample of (H3).

## 12. Earlier Reviews and Records Compared

This section was written after §§1 to 11. Six documents under `docs/project/reviews/`
mention `T-132`, and the packet holds the intake lane’s receipts.
None of them read the certificate.

- **[The 11 October final review of PR 487’s lower bounds](review-2026-10-11-final-lower-bounds.md)**
  read the record and the intake’s receipts, and says its read “is not a `C1` read of
  those four”. It agrees with this review in several places:
  - its exact differences ($1/100$, $1/200$, $1/400$), its
    $B(1 + D) = 25009997/25010000$ and its endpoint value $367/6255001$;
  - its `S3`, and its reading of the rungs as `V0/C0`;
  - its F1-3 on the price, which `T-132`’s record now carries as 4.3 to 5.5 CPU-hours.

  One of its sentences is looser than the argument.
  It says that “the nearest node to any angle in $[0, \pi/4]$ is within $\arctan D$”,
  but the angle to the nearest node can reach $2\arctan(D/2)$, which exceeds $\arctan D$
  by about $D^3/4$. The crate’s N2 says so.
  The argument needs only $z = \tan(\delta/2) \le D/2$ (§2), so the conclusion that
  review drew, that the core lies strictly inside, stands.
  The 4 November review of n = 28 and n = 30 made the same note, and no record changes.
  Its F1-2 left `T-132`’s significance a draft until the review that reads the
  certificate; this is that review, and it keeps `S3`.

- **[The 11 October grading review](review-2026-10-11-final-asymptotic-and-grading.md)**
  grades `T-132` `V0/C0` and `S3`, and reads a replay as *re-implemented sharing the
  producer’s components*. That agrees with §§6 and 10.

- **[The 11 October rungs review](review-2026-10-11-recent-register-rungs.md)** finds
  `V0/C0` right because no qualifying read was recorded.
  This review is that read, and supports `C1` once recorded.
  The holds it lists for `T-132`, the retention of the candidate and the tooling, have
  since been met: the candidate is retained in `release/` (`219bc1268`) and the census
  reads it.

- **[The 14 October fine-net review](review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md)**
  and **the 23 October reviews of
  [#446’s fine-net certificates](review-2026-10-23-wand125-446-fine-net.md) and of
  [`mixed_n31`](review-2026-10-23-wand125-n31-fine-net.md)** cite `T-132` only for the
  candidate’s retention, the family’s credit line and as an `S3` comparison.
  All three agree with this review’s credit and significance.
  The 14 October review’s F-1 on the census’s axis tolerance has since been acted on
  (#892), and F-8 here records `T-132`’s numbers under it.

- **The 4 November review of `mixed_n28_L57425` and `mixed_n30_L58925`**, not yet on
  `main`, is the structural precedent, read before writing (§13). Its description of the
  nested archive (16 identical files, `certificate.rs` +32 −2, build digest `ab6e33e1…`)
  was re-derived here from this asset’s bytes, and agrees.
  Its F-4 does not carry over: this bundle’s pre-publication receipt is not the check2
  run’s record. Its direction-0 method was re-run here with an exact certification, and
  its oblique sampling was extended by this review’s own branch and bound (§4).

- **The intake lane’s receipts**, opened for this section:
  - `receipts/premises.json` (`EXACT_PREMISES_HOLD`) agrees with §2 at every value both
    state: 650 positive rows, the mass, the core, the step, 2,073 directions, lemma N0’s
    (a) to (e), the last bin, the net block, the digest, the source run’s nodes and CPU,
    and the pre-publication run’s 4,306 s.
  - `receipts/sample-diagnostic.json` ran the same binary, `567a0fd5…`, at 0, 296, 592,
    888, 1184, 1480, 1776 and 2072, none of the seven directions sampled here; direction
    2072 is among the nine this review decided with its own code.
    Its eight rows agree with the source’s log in node count and least bound.
    Its CPU ratio to the source’s, 0.613 at a load of 12.5 on four cores, is lower than
    the 0.756 measured here at a load near 4; the price it sets, 4.3 CPU-hours, stands
    within its upper end of 5.5.
  - `reported-n29-followup.json` agrees with this review’s reading of the source: the
    comparisons, the declared net, core, mass, archive and build digests, the two runs’
    times and the control’s 32 refusals with 31 exact.

No earlier document found a defect in the certificate, and this review found none.

## 13. Disclosure

No review of this certificate’s mathematics existed when this one was written.
§12 compares the earlier documents that mention `T-132`, read only after §§1 to 11 were
written.

Before writing, the lane read the material §0 lists.
Four parts of it carry conclusions of others about this certificate or its route:

- **The bead notes of think-1lri and think-r333.** These are the intake and records
  lanes’ findings: that the maintained readers returned `EXACT_PREMISES_HOLD`, that
  eight sampled directions matched, that n = 29’s axis gap is $5.2 \times 10^{-10}$, and
  the prices.
- **The packet README’s summary** of the same, including its table of the eight sampled
  directions.
- **T-132’s register entry and its evidence entry’s `limitations`.**
- **The 4 November review of n = 28 and n = 30**, read whole as the brief’s structural
  precedent, with its programs.
  Its findings concern those two bundles.
  Its F-1 to F-7 bear on the same shipped files as this review’s F-1 to F-6 and F-8, and
  each was checked again here from this bundle’s bytes.
  For F-4 the result differs: this bundle’s pre-publication receipt is not the check2
  run’s own record (§5). Its F-1 did not note the whole-configuration fold, which this
  review’s F-1 adds.

The axis gap was measured again here, with the reviewed crate and with this review’s
exact evaluator, and the premises were recomputed by this review’s own programs.
The intake lane’s receipts and its follow-up record were opened only for §12.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
