# Mathematical Review: wand125’s Fine-Net Lower Bounds at n = 37, 39 and 44 and the Linear Lower Bound at n = 145

Reviewed 2026-10-14 from the two packets retained that day,
[`wand125-fine-net-n37-n39-n44-2026-10-13`](../../../packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/README.md)
and
[`wand125-linear-n145-2026-10-13`](../../../packing/resources/web/wand125-linear-n145-2026-10-13/README.md),
their register plans and receipts, and the four release assets of
`square-lower-bounds-v1` unpacked in scratch space and read as data, by an AI agent: the
stage-4 mathematical review lane of the import think-u0av, Fable, strong tier, max
reasoning.
The lane worked in a worktree of its own, read the source as data and executed
no program of it; the one program it ran that it did not write is this repository’s
reviewed `sqverify-fast` (crate source `d97758bb…`, binary `567a0fd5…`). No earlier
review of any of the four results exists; the route reviews it read are listed in §0.
Nothing was posted, the author was not contacted, and nothing of the source is proposed
for retention beyond what the packets hold.

This review registers nothing and moves no bound.

## Summary for the Author

Four lower bounds are under review, all published on 13 October 2026 in
wand125/square-packing and reported on no issue: $s(37) \ge 2599/400$,
$s(39) \ge 533/80$ and $s(44) \ge 2799/400$, by check2 certificates on the
2,073-direction declared net of core $4999/5000$ and step $1/5002$; and
$s(145) \ge 306/25$, by a linear measure of 594 point, 1,541 segment and 9 rectangle
orbits on the 201-angle standard net, which by its mass also gives $s(N) \ge 12.24$ for
every $N \ge 145$ and so raises the record at $n = 145$ to $149$.

Everything that the retained documents and the release assets let a reader recompute was
recomputed here with code written for this review, in exact arithmetic and apart from
every checker: the four measures and their masses, the digests, the nets and lemma N0’s
premises, the per-bin domains, the author’s run logs (every direction, every certified
bound, the node totals, the premises each run read), all 96 witnesses of the author’s
control runs, the linear measure’s $D_4$ invariance, its 201 records and the inputs of
six of its angles, and the values of Green, Nagamochi and Karakuş that the scope rests
on. The reviewed `sqverify-fast` was run here at 18 further directions of the three
check2 certificates and reproduced the author’s node counts and bounds to the last
digit, and at six directions of the 99/100 mutant, each refused with a witness this
review’s own evaluator confirms.

No step read here is false, and no finding is blocking or major in any certificate.
The argument from each certificate to its bound is the one the route’s reviews derived
(§§2 and 3), and every premise an instance must meet holds for all four.
What no retained material can discharge is the coverage itself: the author’s runs decide
it, and a complete replay here has not run.
Each certificate is therefore **accepted** as a reported result in the record’s
vocabulary: the review supports `C1` once it is recorded, and `V0` until the replays
run.

Two matters are outside the certificates and are the review’s main content beyond the
checks. The census control’s axis tolerance (§5): the n = 39 refusal the intake lane
found uncounted is sound, and the constant `AXIS_ROUNDING` is below the vertex sweep’s
own enclosure, which this review reproduced bit for bit; a well-posed rule compares the
exact capture with that enclosure.
The author’s nested verifier (§4): its archive’s build digest is the one every receipt
names, and against the reviewed source of 3 October it differs by 34 lines of
`certificate.rs` that read the net declaration, which this review read; what that means
for the rung is set out there.

For the author, four minor matters and some questions (§§7 and 8): the check2 bundles
ship a soundness note that predates the declared-net lemma their reader relies on; the
bundle README names a control file that does not exist; the control’s mutant input is
not bound to any shipped file; and the linear certificate’s records carry no per-angle
bound.

## 0. What Was Read, Run and Not Reached

**Read in full.** Both packet READMEs, `register-plan.yaml` and every receipt under
`receipts/`; the retained `README.md`, `ASSET.json`, `bundle.json` and
`files-sha256.json` of the three check2 directories, and the retained `README.md`,
`ASSET.json`, `manifest.json` and `completion-audit.json` of `mixed_n145_L1224`; from
the assets, each `candidate.json`, `check2/receipt.json`, `check2/control.json`,
`verification/prepublication-receipt.json`, the run and control logs, the n = 145
`certificate.json`, and the proof bundle’s `result.json` and `input.txt` at six angles;
the nested crate’s diff against `packing/sqverify_fast` at `e020eb1e2` (the 34-line hunk
of `certificate.rs`, read in scratch, not retained); in
`packing/sqverify_fast/SOUNDNESS.md`, the claim, N1 to N4, N0, C1, D, A1, A2, B1 to B5,
Z1, Z2, I1, I2, F2 and F3; `src/axis.rs` whole, `src/interval.rs` whole,
`exact::enclose`, `certificate.rs` (`admit`’s net reading, `domain_upper`, `d4_images`,
the expansion, `float_rect`) and `lib::run_direction_inner`; in `devtools`,
`sqverify_fast_census.py` (`refusal_record`, `domain_bounds`, `scaled_sweep`,
`sweep_held`, `control`), `check_sqverify_fast.py` (`direction`, `net_step`,
`mixed_exact`, `mixed_mutant`), `fine_net_followup.py` (`premises`, `direction`,
`sample`, `linear_premises`, `linear_sample`), `audit_wand125_declared_net.py`
(`measure`, `declared_net`, `semantic_digest`, `audit_check2`) and
`audit_wand125_linear.py` (`_orbit`, `linear_measure`, `d4_invariant`,
`semantic_digest`, `check_inputs`); the retained producer modules `unified_measure.py`
and `unified_linear_verify.py` of the 2 October packet, for the export order and the
input format; bead think-u0av’s and think-i85v’s notes; jlevy/squares#543, read only;
stage 4 of `result-import.md`; and in `epistemics.md`, “Which Code Confirmed It”, “Every
Run’s Code Is Kept” and “Review Records”.

**Route reviews read, none of them of these results.** The
[declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md)
of 6 October (whole, including its checklist (b)), its
[fix check](review-2026-10-06-sqverify-fast-declared-net-fix-check.md) (whole, for
FC-1), the [FC-1 review](review-2026-10-06-sqverify-fast-census-control-fc1.md) and its
[re-check](review-2026-10-06-sqverify-fast-census-control-fc1-recheck.md) (whole, for
CC-1 to CC-8 and CR-5), the
[route review](review-2026-10-05-wand125-october-5-and-independent-replays.md) of 5
October (“Carrying the Route”), the
[linear review](review-2026-10-02-wand125-linear-certificates-and-n76.md) of 2 October
(whole), and the [check2 review](review-2026-10-06-wand125-check2-ten-certificates.md)
of 6 October (its verdict, its scope table and its findings’ headings).

**Run.** Eleven programs written for this review, kept with their outputs under each
packet’s `review/` directory and listed in §6; and the reviewed `sqverify-fast`, driven
by one of them.
The computation totalled about three CPU-minutes on a host of four shared
cores.

**Not reached.** A complete capture of any check2 certificate; the census’s whole-net
99/100 control and its near-threshold mutant; the author’s C++ checker on the check2
candidates; any replay of a linear angle (the intake lane’s two-angle sample is the only
one here); the proof bundle’s inputs at the other 195 angles, which the maintained
reader `check_inputs` bound on intake; and the nested crate’s 55 added test lines, which
were counted and not read.

## 1. The Claims

### 1.1 The Three Check2 Certificates

For $(n, L) \in \{(37, 2599/400), (39, 533/80), (44, 2799/400)\}$: no packing of $n$
closed unit squares with pairwise disjoint interiors lies in the closed square
$K = [0, L]^2$; hence $s(n) \ge L$. The claim is the theorem of `SOUNDNESS.md` (“The
Claim”) on the net the candidate declares, with these hypotheses, each instance’s values
in the table of §2:

- **(H1) The measure.** Orbit representatives $R_j = [x_1, x_2] \times [y_1, y_2]$
  inside $K$ with masses $w_j \ge 0$, all exact rationals; the density
  $g = \sum_j \frac{w_j}{8|R_j|} \sum_{S \in D_4} \mathbf 1_{S(R_j)}$; and
  $M = \sum_j w_j = n - 1/100000 < n$.
- **(H2) The net.** $B = 4999/5000$, $D = 1/5002$, $N_\theta = 2073$, with lemma N0’s
  (a) to (e): $2 \le N_\theta \le 2^{16}$; $B(1 + D) < 1$; $t_{\max} = 2072 D$ with
  $t_{\max}^2 + 2t_{\max} - 1 > 0$; $t_{\max} \le 1/2$; and $B(1 + D/(1 - D^2/4)) < 1$.
- **(H3) The coverage.** For every $r = 0, \ldots, 2072$ and every centre $c$ of lemma
  D’s per-bin domain $[\rho(a_r), L - \rho(a_r)]^2$, $a_r = \max(0, rD - D/2)$, the
  closed square $Q_r(c)$ of side $B$ at angle $\theta_r = 2\arctan(rD)$ has
  $\int_{Q_r(c)} g \ge 1$. This is the statement the author’s runs decide.
- **(H4) The fold.** The per-bin domain is a domain for the fold at $\pi/4$: the last
  node’s bin $[t_{2072} - D/2, t_{2072} + D/2]$ holds an orientation of $[0, \pi/4]$,
  that is $(2071.5\,D)^2 + 2 (2071.5\,D) - 1 < 0$.

### 1.2 The Linear Certificate

For $n = 145$ and $L = 306/25$: no packing of 145 closed unit squares with pairwise
disjoint interiors lies in $K$; hence $s(145) \ge 12.24$, and since every packing of
$N \ge 145$ unit squares contains a packing of 145, $s(N) \ge 12.24$ for every
$N \ge 145$. The hypotheses are the 2 October review’s:

- **(H1′) The measure.** 594 point, 1,541 segment and 9 rectangle orbit representatives
  with exact rational geometry inside $K$ and masses $m \ge 0$; the measure $\mu$ that
  gives each of a representative’s eight $D_4$ images $m/8$ (a point image at its point,
  a segment image uniformly by parameter length, a rectangle image uniformly by area);
  and $\mu(K) = 14499999/100000 < 145$.
- **(H2′) The net.** $B = 9977/10000$, $D = 83/40000$, 201 angles: $B(1 + D) < 1$ and
  $t_{200}^2 + 2t_{200} - 1 > 0$.
- **(H3′) The coverage.** At every angle $r$ and every centre of the quadrant
  $[L/2, L/2 + E_r]^2$, $E_r = (L - B(c_r + s_r))/2 > 0$, the closed core has
  $\mu \ge 1$: the statement `unified_linear_verify.cpp` decides.
- **(H4′) The folds.** The quarter turn and the diagonal reflection carry the quadrant
  and $[0, \pi/4]$ to the whole domain and every orientation; both need only $\mu$’s
  $D_4$ invariance.

## 2. The Fine-Net Argument, Re-derived

The argument is the theorem’s proof in `SOUNDNESS.md`, read with lemma N0 in place of
the standard net’s constants, and nothing in it depends on $n$, $L$ or the rows.

**N1, the net.** With $t_r = rD$ the half-angle tangents are $D$ apart, so every
$t \in [0, t_{\max}]$ is within $D/2$ of a node.
Here $t_{\max} = 2072/5002 = 1036/2501
\approx 0.4142343$, and $t_{\max}^2 + 2t_{\max} - 1 = 367/6255001 > 0$, so
$t_{\max} > \tan(\pi/8) \approx 0.4142136$: the net reaches past $\pi/4$, by
$2.1 \times 10^{-5}$ in the tangent.
The last bin $[2071.5 D, 2072.5 D] \approx
[0.414134, 0.414334]$ contains $\tan(\pi/8)$, so node 2072 is assigned orientations of
$[0, \pi/4]$ and premise (H4) holds: $(2071.5 D)^2 + 2(2071.5 D) - 1 < 0$ (recomputed).

**N2, the orientation.** A square at $\varphi \in (\pi/4, \pi/2)$ is reflected in the
diagonal, which preserves $K$, $g$ (by $D_4$ invariance) and disjointness, to
$\pi/2 - \varphi$. For $\varphi \in [0, \pi/4]$ take the node $r$ with
$|\tan(\varphi/2) - t_r| \le D/2$; then $z = \tan(\delta/2) \le D/2$ for the angle
$\delta$ between the square and the node.
The fold is at $\pi/4$, which is why lemma D’s $\rho(a_r)$ is a valid lower bound on the
square’s distance from the walls (N2’s remark, and (H4)).

**N3, the shrink.** The concentric core of side $B$ at angle $\theta_r$, seen in the
square’s frame, has extent $B(1 + 2z - z^2)/(1 + z^2) \le B(1 + 2z) \le B(1 + D) =
25009997/25010000 < 1$, with a margin of $3/25010000$ per side, so it lies in the open
unit square and its centre in $[a_r, L - a_r]^2$ with $a_r = B(c_r + s_r)/2$. Admission
also checks the tangent form (e), $500400014977/500400075000 < 1$. Lemma D then
restricts the centres to $[\rho(a_r), L - \rho(a_r)]^2$, since a square assigned to node
$r$ has half-angle tangent at least $a_r = \max(0, t_r - D/2)$ and
$\rho(\tan(\varphi/2)) = (\cos\varphi + \sin\varphi)/2$ increases on $[0, \pi/4]$; lemma
C1’s quarter turn reduces it to the quadrant $[L/2, L - \rho(a_r)]^2$ the search covers.
The domain is nonempty at every node: its width $L - 2\rho(a_r)$ is least at node 2072,
5.08, 5.25 and 5.58 for the three certificates.

**N4, the count.** The $n$ cores are pairwise disjoint closed subsets of $K$, each of
$g$-measure at least one by (H3), so $n \le \int_K g = M < n$.

**The two methods.** At $r = 0$ the crate runs the vertex sweep (lemmas A1 and A2): the
capture is bilinear on the cells of the event grid $\{x_i \pm B/2\} \times
\{y_j \pm B/2\}$, so its minimum is at a vertex, and each column is swept in interval
arithmetic (lemma I1) from a directly evaluated foot.
Here the grids are $3{,}970^2$, $4{,}498^2$ and $3{,}935^2$ vertices.
At $r \ge 1$ the branch and bound of R1 to R6 runs on the quadrant, and with `--confirm`
a refusal carries an exact witness.
Lemma F3’s caps hold with room: the densest image is at $25{,}439$, $15{,}368$ and
$19{,}392$ against $2^{96}$, and eight times it, the densest row, is below $2^{32}$; the
least rectangle side is $0.001000$, and no rectangle is nearer than $0.20$ to a wall.

**The instances.** Every value below was recomputed here by
`review/programs/check_candidate.py` and `check_source_logs.py` (§6), apart from the
crate and the tools:

| Premise | n = 37 | n = 39 | n = 44 |
| --- | --- | --- | --- |
| Candidate SHA-256; semantic digest | `f6e32978…`; `23387d7d…` | `03eef5c3…`; `3b464f3f…` | `584a8319…`; `02f4933f…` |
| Rows, all positive, inside $K$, nondegenerate; images, no two coincident | 612; 4,896 | 687; 5,496 | 606; 4,848 |
| Mass, equal to `total_mass` and to $n - 1/100000$ | $3699999/100000$ | $3899999/100000$ | $4399999/100000$ |
| `proof_net` exactly `{step, last}`; no `net`, `certificate` or `scaling_factor` key; `points` empty | yes | yes | yes |
| Lemma N0 (a) to (e) and (H4), on $B = 4999/5000$, $D = 1/5002$, 2,073 nodes | hold | hold | hold |
| Per-bin domain’s least width, at node 2072 | 5.083 | 5.248 | 5.583 |
| Densest image; eight times it | 25,439; 203,512 | 15,368; 122,947 | 19,392; 155,139 |
| Source run: directions, all `verified` at threshold `1`; nodes; direction CPU | 2,073; 864,953,550; 13,474 s | 2,073; 881,271,470; 13,502 s | 2,073; 1,166,443,954; 35,894 s |
| Source run read the published candidate (`input_sha256`) | yes | yes | yes |
| Least certified oblique bound, at direction | 1.0000000000166 (1919) | 1.0000000000654 (1804) | 1.0000000000027 (622) |
| Axis: certified bound; exact capture at its vertex, recomputed | 1.0023692790476681; 1.002369279116849 | 1.0020921702344088; 1.0020921715116728 | 1.002336408087091; 1.0023364082168984 |
| Exact capture at the 12 tightest leaf centres | all $\ge$ bound and $\ge 1$; least 1.0022 | least 1.0026 | least 1.0036 |
| Control (197/200): refusals; witnesses in domain, below 1, equal to the crate’s | 32; all | 32; all | 32; all |
| Pre-publication run, same build `ab6e33e1…`, published bytes | 619 s | 697 s | 1,654 s |

**What this instance cannot discharge from retained material.**

1. **The coverage (H3).** It is decided by the author’s two runs of the nested crate,
   whose logs and receipts the assets hold and whose per-direction records this review
   read; here it has been sampled, at 8 directions by the intake lane and 6 more by this
   review, bit for bit the author’s rows.
   Until a complete census from reviewed source runs, (H3) is the author’s report.
2. **The candidate.** The release assets are pinned by digest and not retained, so the
   candidate a census here would read is in no packet; the owner’s question on
   jlevy/squares#543 for `T-132`, `T-142` and `T-143` applies.
3. **The author’s build.** The binary `ec04d332…` cannot be rebuilt from retained bytes;
   the archive it was built from is pinned, and this review recomputed its build digest
   `ab6e33e1…` from the archive (§4), which ties the receipts to those bytes.
4. **The controls.** The author’s 32-direction control and the pre-publication run are
   attributed outcomes; the census’s whole-net control (FC-1) has not run here, and at n
   = 39 cannot pass under the present axis rule (§5).

Everything else the theorem needs holds exactly in the retained and pinned material.

## 3. The Linear Argument, Re-derived

The argument is the 2 October review’s, which read the checker; nothing in it depends on
the count or the rows, and this review re-derived it on the instance.

**The measure.** `validate` expands every positive representative to its eight images
under the maps $(x, y) \mapsto (y, x)$ or not, then $x \mapsto L - x$ and
$y \mapsto L - y$ or not, each with mass $m/8$; those eight maps are $D_4$, so the
expanded family is $D_4$-invariant whatever the representatives are.
Recomputed here with an invariance test of its own (`check_linear_candidate.py`): 4,752
point, 12,328 segment and 72 rectangle images, and the multiset of (kind, set, weight)
is carried onto itself by the diagonal swap and by $x \mapsto L - x$. A point image
carries $m/8$ at a point; a segment image carries $m/8$ uniformly along its length,
which is uniform in the parameter $\lambda$ of $P_0 + \lambda(P_1 - P_0)$; a rectangle
image has density $m/(8|R|)$. $\mu \ge 0$ and $\mu(K) = 14499999/100000$, equal to
`total_mass` and to $145 - 1/100000$. The nearest primitive is $0.0998$ from a wall, so
the container’s boundary convention is not exercised.

**Containment.** $B(1 + D) = 399908091/400000000 < 1$ and $t_{200} = 83/200$ with
$t_{200}^2 + 2t_{200} - 1 = 89/40000 > 0$: N1 to N3 as in §2, on the standard net.
Every unit square contains, strictly inside, a closed core of side $B$ at the nearest
net angle, with its centre in Tokoharu’s domain $[a_r, L - a_r]^2$,
$a_r = B(c_r + s_r)/2$.

**The two folds.** The checker covers the quadrant $[L/2, L/2 + E_r]^2$ with
$E_r = L/2 - a_r$. Lemma C1’s quarter turn carries a core at angle $\theta_r$ centred at
$p$ to the core at $\theta_r + \pi/2$, as a set the core at $\theta_r$, centred at
$\rho(p)$, and $\mu(\rho A) = \mu(A)$; the four images of the quadrant are the four
quadrants of $[a_r, L - a_r]^2$. The orientation fold is the diagonal reflection, as in
N2. Both need only the invariance checked above.
$E_r > 0$ at every angle, least $5077628753/937780000 \approx 5.4145$ at angle 200.

**The count and the transfer.** Cores strictly inside pairwise interior-disjoint squares
are pairwise disjoint closed sets; a point mass on a core’s boundary belongs to that
core alone and a segment’s length inside the cores is additive; so
$145 \le \mu(\bigcup_i C_i) \le \mu(K) < 145$. For $N \ge 146$ any 145 of the $N$
squares give the same contradiction, so $s(N) \ge 306/25$.

**The scope.** Recomputed here from the case records and the closed forms
(`check_linear_candidate.py`), with Green’s $G_{12} = 2\sqrt2 - 1 + 11(132 +
2\sqrt6)/145$ bounded from 100-digit integer square roots:

| n | Nagamochi $1 + \sqrt{n - 2\lfloor\sqrt n\rfloor + 1}$ | Karakuş $1/2 + \sqrt{n - \lfloor\sqrt n\rfloor + 1/4}$ | Reported lower on record | Verified upper on record | 12.24 beats every lower; below every upper |
| --- | --- | --- | --- | --- | --- |
| 145 | 12.0454 | 12.0434 | 12.2139 (Green) | 12.5355 | yes; yes |
| 146 | 12.0905 | 12.0866 | 12.2139 (Green) | 12.5838 | yes; yes |
| 147 | 12.1355 | 12.1297 | 12.2139 (Green) | 12.6569 | yes; yes |
| 148 | 12.1803 | 12.1726 | 12.2139 (Green) | 12.6569 | yes; yes |
| 149 | 12.2250 | 12.2154 | 12.2250 (Nagamochi) | 12.7071 | yes; yes |
| 150 | 12.2694 | 12.2580 | 12.2694 (Nagamochi) | 12.7782 | no |

So the certificate raises both lower lanes at $n = 145$ to $149$ and nothing at 150,
where both lanes already exceed $12.24$; no count is settled, the upper bounds being at
least $0.29$ above. The two forms of $G_{12}$, the README’s and the case records’
$22\sqrt6/145 + 2\sqrt2 + 1307/145$, are the same number; the source’s 90-digit rational
`compared_with` exceeds $G_{12}$ by $4.0 \times 10^{-91}$, so it is the upper bound it
is said to be, and the stated margin $306/25 - \text{compared\_with} =
0.026133052\ldots$ is exact and above the README’s $0.0261330$.

**The checker’s hypotheses on this instance.** Of the eleven the 2 October review
listed: the inputs enclose the expanded exact measure (six angles here, every interval
within one ulp; all 201 by the maintained reader on intake); `gamma` is exactly one; the
per-angle domain is positive; the 201 records are `LINEAR_ANGLE_REPLAYED` with distinct
input digests and 124,435,707 nodes, most 3,330,973 at the axis and fewest 168,149 at
angle 35, under the manifest’s node limit of 12,000,000 (the earlier certificates’
3,000,000); every one of the bundle’s 202 `verify.cpp` copies is the retained checker
`0249726a…`; and the stored per-angle lower bounds are tight (the six read here lie
between $1 + 1.5 \times 10^{-10}$ at angle 200 and $1 + 4.5 \times 10^{-8}$ at angle
35), which is the branch and bound’s termination margin, not the measure’s slack.
The fifteen exact captures evaluated here at the domain’s centre, corners and edges at
angles 0, 100 and 200 are all above one (least 1.00206, the container’s centre at angle
200); they decide nothing about the other centres.

**What this instance cannot discharge from retained material.** The coverage (H3′) at
201 angles is the author’s checker’s decision, the same implementation a replay here
would run; two angles were replayed on intake and none here.
The candidate, the certificate and the proof bundle are in the release asset, pinned by
digest and not retained.
The author’s replay “on a fresh machine” (2 h 8 min at 30 workers) has no published
receipt.

## 4. Trust Boundaries

| Checker | Decides | Trusts | Shares with the others |
| --- | --- | --- | --- |
| `sqverify-fast`, this repository, source `d97758bb…` (reviewed 3 and 6 October) | (H3) at the directions it runs, by the vertex sweep at $r = 0$ and interval branch and bound at $r \ge 1$ | binary64 round-to-nearest without FMA (I1), `enclose` (I2), the lemmas R1 to R6, A1, A2, D and N0, and admission’s exact checks | with the author’s crate, every file of `src/` but `certificate.rs` (and three lines of `lib.rs`, one of `rotated_tests.rs`): the same kernel, byte for byte |
| The author’s nested crate, archive `e495f9bf…`, build `ab6e33e1…`, binary `ec04d332…` | (H3) at all 2,073 directions, in the author’s two runs | the same, and its own 34-line reading of `proof_net` | `e020eb1e2`’s source `7c49cf79…` (the 3 October reviews’ object) with 32 lines added and 2 changed in `admit`, 55 test lines, and prose; against main it lacks f007d7afd’s declared-net change (lemma N0’s reader, DN-5) and the DN fixes |
| The premise readers (`audit_wand125_declared_net`, `audit_wand125_linear`, `fine_net_followup`) | nothing: exact premises, custody, bindings | Python fractions, SHA-256 | the project’s mathematics and the formats; no code with either crate |
| The census control’s evaluator `check_sqverify_fast.mixed_exact` | the mutant’s capture at the crate’s witnesses, in the whole-net control | fractions and `sqpack`’s exact clipping | nothing with the crate’s code; its net step from the file |
| This review’s programs (§6) | the captures at the poses they evaluated; the sampled directions, with the binary | fractions; for the sweep emulation, Python’s binary64 | nothing imported; the sweep emulation transcribes `axis.rs` and `interval.rs` |
| The author’s C++ `unified_linear_verify.cpp`, `0249726a…` (reviewed 2 October) | (H3′) at every angle, in the author’s run | Tokoharu’s kernel under binary64 at fixed flags; its point and segment bounds | nothing with `sqverify-fast`; it was not run on any of these certificates |

**What the author’s crate is.** `nested_crate.py` recomputed, by `build.rs`’s rule, the
`source_sha256` a build of the archive embeds: `ab6e33e1…`, the digest every check2
receipt, control summary and pre-publication receipt names, so the receipts are runs of
those bytes.
Against the reviewed source `e020eb1e2` (`7c49cf79…`), sixteen of the twenty
members are byte-identical: `Cargo.toml`, `Cargo.lock`, `build.rs`, the toolchain pin,
`clippy.toml`, `INDEPENDENCE.md`, `independence-record.yaml`, `.gitignore`, and
`src/axis.rs`, `exact.rs`, `interval.rs`, `lib.rs`, `main.rs`, `oracle.rs`,
`rotated.rs`, `rotated_tests.rs`. `src/certificate.rs` differs by 32 added and 2 changed
lines, all in `admit`: when a format M file carries `proof_net`, the block must be an
object with exactly `step` and `last`, no `certificate` metadata may sit beside it,
`step` is read as an exact rational and `last` as a `u32` plus one, and the standard-net
pin is skipped; the shared premise checks that follow, $B(1 + D) <
1$, the endpoint polynomial, $t_{\max} \le 1/2$, the tangent form and the $2^{16}$ cap,
then run on the declared step and count.
I read the hunk; it is lemma N0’s admission in a shorter form, without f007d7afd’s
duplicate-key visitor, its `count` field and its refusal of `proof_net` outside format
M. `tests/adversarial.rs` gains 55 lines, counted and not read, and `README.md` and
`SOUNDNESS.md` carry prose additions (5 and 11 lines).

**What that means for the rung.** The author’s runs rest on code no review here read,
but the unread part is confined to those 34 lines, whose effect, the net and domains the
search uses, is observable: the author’s summaries report `D 1/5002` and
`angle_count 2073`, and the reviewed `d97758bb…`, which reads the same declaration under
lemma N0, reproduces the author’s node count and least certified bound at every one of
the 24 directions sampled here and on intake, numbers that depend on the step, the
domains and the search.
That is consistency, not review.
For the record: the author’s runs are the reported entries’ evidence and stay `V0`,
`same-implementation` with `V-wand125-sqverify-proof-net` deciding, as the register
plans have it; a census here from `d97758bb…` would be *re-implemented sharing the
producer’s components*, as the plans’ `composition` says and `T-104`’s precedent reads,
since the producer adapted this repository’s crate; no second implementation stands
beside the kernel, and a defect in the shared `rotated.rs`, `axis.rs` or `interval.rs`
would pass both. The independent checks of that kernel are the exact evaluators: this
review’s and the census control’s, which agree with the crate’s exact witnesses at 99
poses here.
The nested crate’s unreviewed and unretained state therefore lowers nothing a
replay here can reach, and blocks no registration at `V0/C0`; it should not be run here,
and its receipts should not be cited as a confirmation by a reviewed checker.

## 5. The Axis Tolerance

**The rule.** The census control’s `refusal_record`
(`packing/devtools/sqverify_fast_census.py`, line 604 and lines 652 to 658) counts the
axis row of the 99/100 mutant as a refusal only if, besides the sweep’s `refused`, the
vertex in the domain and the exact capture there below one, the exact capture $F$
satisfies $b \le F \le b + 10^{-9}$ with $b$ the sweep’s certified bound,
`AXIS_ROUNDING` being “its binary64 rounding over a few thousand terms” (CR-5 of the
FC-1 re-check). On intake the gaps $F - b$ were $6.9 \times 10^{-11}$ (n = 37),
$1.26 \times 10^{-9}$ (n = 39) and $1.3 \times 10^{-10}$ (n = 44); `T-142`’s is
$2.15 \times 10^{-9}$.

**What the sweep certifies.** By lemmas A2 and I1 the column sweep keeps, at every
vertex, an interval $[\ell, u]$ with $\ell \le F \le u$, and reports $\min \ell$ and its
vertex.
`review/programs/sweep_emulation.py` rebuilds the event grid and walks one column
as `axis.rs` does, with `interval.rs`’s directed steps
$\mathrm{dn}(x) = x - (|x| 2^{-52} + 2^{-1074})$ written in Python floats:

|  | n = 37 | n = 39 | n = 44 |
| --- | --- | --- | --- |
| Column’s $y$ events; the reported vertex’s index | 3,970; 766 | 4,498; 4,497 | 3,935; 1,565 |
| Rectangles active in the column; greatest $\lvert\sigma\rvert$ | 1,044; 126 | 1,100; 176 | 1,050; 122 |
| Emulated $\ell$ equals the crate’s bound, original and mutant | yes | yes | yes |
| Enclosure width $u - \ell$, original; mutant | $1.38 \times 10^{-10}$; $1.37 \times 10^{-10}$ | $2.55 \times 10^{-9}$; $2.53 \times 10^{-9}$ | $2.60 \times 10^{-10}$; $2.57 \times 10^{-10}$ |
| $F - \ell$, mutant; $u - F$, mutant | $6.85 \times 10^{-11}$; $6.84 \times 10^{-11}$ | $1.264 \times 10^{-9}$; $1.264 \times 10^{-9}$ | $1.286 \times 10^{-10}$; $1.286 \times 10^{-10}$ |

In all six runs the emulated lower end equals the crate’s reported bound to the last
digit, so the emulation walked the crate’s path, and the exact capture sits at the
midpoint of the enclosure.
The gap the census measures is half the enclosure’s width.
That width is not a constant of the arithmetic: the sweep reaches vertex $j$ of a column
by $j$ steps $V \leftarrow V + \sigma_j (y_{j+1} - y_j)$, and each step widens $V$ by
about $|\sigma_j|$ times the width of the event difference (two ulps of $y$, about
$1.8 \times 10^{-15}$ here) plus the directed steps, so the width grows with the
vertex’s index and with the slopes, which are sums of up to 1,100 weights
$\rho_k\,o^x_k$ with image densities up to 25,439. At n = 39 the least vertex is the
last of its column (index 4,497 of 4,498), whence $2.5 \times 10^{-9}$; at n = 37 it is
at index 766, whence $1.4 \times 10^{-10}$.

**The mathematics of the n = 39 refusal.** The vertex
$(2811937607608141/625000000000000,
493/80)$ lies in the domain ($493/80 = L - 1/2$ is its upper edge); the mutant’s exact
capture there, recomputed here, is $0.99207124979\ldots < 1$ (the original’s is
$1.00209217151\ldots$); and the sweep’s bound $0.9920712485323058$ is below it, as a
certified lower bound must be.
The mutant’s claim is false at a centre where it must hold, which is what
`coverage_refusal`, `in_domain` and `capture_below_1` record, and the crate’s refusal is
right. The failed field, `captures_agree`, is a consistency test between the crate and
the evaluator, not a soundness condition, and it fails only because the constant is
smaller than the enclosure the crate itself certified: the crate’s own answer to “is $F$
consistent with the sweep?”
is $\ell \le F \le u$, which holds here with $u - F = 1.264 \times 10^{-9}$.

**What would make the control well-posed.** The test should compare $F$ with the
enclosure, not with a constant:

1. **The crate reports the enclosure.** Have the axis row carry the upper end $u$ at the
   least vertex (or $u - \ell$), and have the control require $\ell \le F \le u$. That
   is the interval contract itself, well-posed for every certificate, and it needs no
   tolerance. It changes a receipt field and no verdict, but any change to `src/` is a
   new `source_sha256` and, by the soundness review’s list, a re-review before a row
   built from it counts.
2. **The control recomputes the enclosure.** Without a crate change, the control can
   walk the column as `sweep_emulation.py` does and require $\ell' = b$ (which shows the
   transcription walked the crate’s path) and $\ell' \le F \le u'$. It is a
   transcription of the crate’s arithmetic, so it is a consistency check of the same
   strength as the crate reporting $u$, at about one second per certificate, and it is a
   change to control logic that needs a reviewer.
3. **One-sided.** Require only $b \le F$, the direction soundness needs, beside the
   exact refutation $F < 1$ at a vertex in the domain.
   It drops the tightness check CR-5 asked for and is the smallest sound change.

A larger constant is a stopgap: it would have to exceed half the enclosure’s width at
every future certificate, and nothing bounds that width but the sweep.
For the six 2,073-direction certificates seen so far (gaps from $6.9 \times 10^{-11}$ to
$2.15 \times 10^{-9}$) a constant of $10^{-8}$ would hold with a factor of four, with no
guarantee for the next.
Which option to take is the owner’s decision on jlevy/squares#543 for `T-142`, which
decides n = 39 as well; the mathematics is that the refusals are sound under every
option, and that options 1 and 2 are the ones that measure what the rule means to
measure.
The n = 37 and n = 44 axis legs count under the present rule, as the intake lane
found and the emulation confirms.

## 6. Checks Made Here

Every program is kept, with the output it printed, under
[`wand125-fine-net-n37-n39-n44-2026-10-13/review/`](../../../packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/review/README.md)
and
[`wand125-linear-n145-2026-10-13/review/`](../../../packing/resources/web/wand125-linear-n145-2026-10-13/review/README.md),
whose READMEs say what each read, how to run it and what it printed.
They ran under `python3 -I` with the project interpreter, reading the assets as data.

| Program | Read | Printed |
| --- | --- | --- |
| `check_candidate.py`, three runs | the three candidates | the table of §2: every exact premise holds; digests as stated |
| `check_source_logs.py`, three runs | the run logs, control logs, receipts, pre-publication receipts and `bundle.json` | every direction once and verified; nodes and premises agree; the receipt’s embedded summary equals the log’s; the axis bound a true lower bound; the twelve tightest leaf centres at least one; all 96 control witnesses genuine, 93 equal to the crate’s rational digit for digit (the three axis witnesses carry no exact value) |
| `sweep_emulation.py`, six runs | the candidates; the sweeps’ vertices and bounds | the table of §5 |
| `sample_directions.py`, six runs with the reviewed binary | the candidates and run logs | 18 directions verified, node counts and bounds equal to the author’s, build `d97758bb…`; exact captures at every leaf centre at least the bound (least 1.0020); 6 mutant refusals with witnesses below one in the domain (least 0.99256); about 174 CPU seconds in all |
| `nested_crate.py`, one run | the archive from the n = 39 asset; `git archive` copies at `e020eb1e2` and head | §4’s digest and diff counts |
| `check_linear_candidate.py` | the n = 145 candidate, completion audit and case records | §3’s measure, invariance, net, scope and Green comparison |
| `check_linear_records.py` | `certificate.json`, `manifest.json`, `completion-audit.json`, the proof bundle, the retained checker | §3’s records and digests |
| `check_inputs_sample.py` | the proof bundle at angles 0, 1, 35, 100, 111 and 200 | every line encloses its image within one ulp; results and manifests as recorded; 201 checker copies equal to the retained one |
| `point_checks.py` | the n = 145 candidate | fifteen captures, all at least one |

Nothing the brief asked for went unestablished because of a tool or permission failure.
One correction along the way: the first `check_source_logs.py` compared the receipt’s
embedded summary, read with decimals as text, against the log’s, read with floats, and
reported them unequal; both are now read alike and they are equal.

## 7. Findings

No finding is blocking, and none is major in a certificate.
Grades are for the claims first and the record second.

### F-1, major for the records lane, not a defect of the certificates: the axis tolerance is a constant where the test needs the enclosure

`packing/devtools/sqverify_fast_census.py`, line 604 (`AXIS_ROUNDING`) and lines 652 to
658 (the axis branch of `refusal_record`). As §5 shows, the gap the rule measures is
half the sweep’s enclosure width, which varies by a factor of twenty across these three
certificates alone and exceeds the constant at n = 39. The n = 39 whole-net control
cannot end `CONTROLS_REFUSED` under this rule although its refusal is sound.
Fix: one of §5’s options 1 to 3, as a change to control logic read by a reviewer.
It affects `T-142` as well, and no certificate.

### F-2, minor, in the source: the check2 bundles’ soundness note predates the lemma their reader relies on

`check2/src/SOUNDNESS.md` in all three directories is this repository’s edition at
`e020eb1e2` (Git blob `cadf59b6…`, 3 October), which has no section on declared nets;
the copy inside the nested archive adds eleven lines of the author’s own.
The statement of why a declared net is admissible is lemma N0 of f007d7afd, which this
review used. Fix: ship or cite the edition with lemma N0, or state the author’s own
argument for the net in the bundle.

### F-3, minor, in the source: the bundle README names a control file that does not exist

Each directory’s `README.md`, line 15, lists
`check2/control.json, check2/control.jsonl.gz`; the shipped log is
`check2/control-197_200.jsonl.gz`, in both the directory and the sealed bundle.
The nine check2 READMEs of 6 October retained here carry the same line.

### F-4, minor, in the source: the control’s input is not bound to a shipped file

The control log’s summary names an input digest (`a119e249…` at n = 39, `f44bdc5e…` at
37, `071c59fc…` at 44) that is no member of the asset or the sealed bundle, and
`check2/control.json` records the factor and the counts but no digest.
The control is recoverable only through its summary’s `mass_exact`, which is $197/200$
of the candidate’s mass in all three, and through its witnesses, which this review
evaluated on the scaled candidate.
Fix: record the mutant’s digest in `control.json`, or ship the mutant.

### F-5, minor, in the source, the linear certificate: the records carry no per-angle bound

`certificate.json`’s 201 records hold `index`, `status`, `input_sha256` and `nodes`;
each angle’s `lower` lives only in the proof bundle (LC-4 of the 2 October review, still
open). Fix: carry `lower` in the record, and the least of them in the README.

### F-6, note, in the record: the intake’s control samples came from an unmerged command

`receipts/control-sample-n*.json` were written by `fine_net_followup control-sample` of
`fc3199fc0` on the unmerged branch `claude/wand125-confirmations-2026-10-11`, as the
packet README says at line 109, and judged with this tree’s `refusal_record`. They are
diagnostics, as the README says at line 126; they must not be cited as evidence from a
reviewed control driver.
This review reproduced their oblique legs at other directions with code in the tree
(`sample_directions.py --factor 99/100`) and their axis legs’ numbers with the sweep
emulation.

### F-7, note, in the source: “independent second-system check”

`check2/receipt.json`, line 90, calls the run “an independent second-system check (built
from the certificate specification only, without reading the search code)”. True of the
author’s search code; a reader should not take it as independent of the certificate’s
kind: the check is this repository’s crate, whose clean room is recorded in
`packing/sqverify_fast/INDEPENDENCE.md`, adapted by the author.

### F-8, note, in the source: the comparisons in the README

The n = 145 README says the certificate “improves on $\sqrt N$ for $N = 145, \ldots,
149$”; it does, by at least $0.03$, and it improves on every bound on record at those
counts (§3). The README’s and `completion-audit.json`’s Green comparison are exact as
stated.

## 8. Questions for the Author

1. Would you ship, in the check2 bundles, the `SOUNDNESS.md` edition that states lemma
   N0, or your own statement of why the declared net is admissible, beside the reader
   that admits it (F-2)?
2. Would you record the mutant input’s SHA-256 in `check2/control.json`, or ship the
   mutant, so that the control binds to a file (F-4)? And correct the README’s control
   file name (F-3)?
3. For the linear certificate, would you carry each angle’s `lower` in
   `certificate.json` (F-5), and publish a receipt of the fresh-machine replay (its
   machine, time and final line), so that the record can cite it as an attributed second
   run?
4. Are the check2 candidates and the n = 145 candidate and certificate, now only in
   release assets, published under the directory’s MIT notice so that a record may
   retain them in Git? The owner’s question on jlevy/squares#543 is the record’s side of
   this.
5. Have you run the C++ checker of the earlier bundles on any of the three check2
   candidates, as the README says it can be, and if so at which directions?

## 9. What V and C the Evidence Supports

All four entries are `V0/C0` as planned: the cited evidence is the author’s report, and
no replay has run here.
This review, recorded as `external_review` on each reported evidence entry and listed in
each entry’s `reviews` as an adversarial AI review with an accepting verdict, supports
`C1` for all four, reading being the one confirmation that needs no verification rung
(`epistemics.md`, “Scope and Composition”). `V` stays `V0`.

What would move each:

- **n = 37, 39 and 44 to `V3/C3`.** A complete `sqverify-fast` census from `d97758bb…`
  at all 2,073 directions of each certificate, from a candidate retained where the
  census reads it, with restored positives, a `CONTROLS_REFUSED` whole-net receipt
  (FC-1) and this review: *re-implemented sharing the producer’s components*. The n = 37
  and n = 44 receipts can pass under the present axis rule; n = 39’s needs F-1 resolved.
  The intake lane priced the three at about 6.5, 7.1 and 17 CPU-hours; the samples here
  ran at 0.89, 0.84 and 0.86 of the author’s CPU on the same directions, consistent with
  that price.
- **n = 145 to `V3/C3`.** The complete 201-angle replay by the T-080 route
  (`linear-replay` from the retained `code/`, the certificate registered in
  `audit_wand125_linear` with its candidate and certificate retained), the
  `linear-control` receipt and this review: *reproduced with the producer’s code*, as
  `T-080` and `T-144` are, with no second implementation of the point and segment bounds
  anywhere. Priced on intake at about 37 CPU-hours on a loaded host.
- **Beyond `C3`.** A second route, the author’s C++ checker on a check2 candidate or an
  independent implementation of the linear bounds, would be recorded beside the rung and
  is a condition of nothing.

**Significance.** The drafts score each entry `S3`. Confirmed: each is a further size
from one generator by a certificate kind and route the record holds at `S3` (`T-132`,
`T-142`, `T-143`; `T-080`, `T-144`), with no new technique.
The n = 44 value is worth a sentence in its case record if it confirms:
$2799/400 = 6.9975$ against the upper bound $7$, a gap of $1/400$. The n = 145 value is
the first certificate-backed bound above Green’s reported value at $k = 12$, and it
carries five counts; that is what `T-144` did at $k = 11$, so `S3` stands.

## 10. Proposed Registry Entries

For `packing/frontier/verifiers.yaml`, to be applied by the records lane; the paths are
the packets’ `review/programs/`. `R` below stands for
`docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md` and
`FN` for
`packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/review/programs`, `LN`
for `packing/resources/web/wand125-linear-n145-2026-10-13/review/programs`.

```yaml
  - id: V-wand125-lb-review-fine-net-premises
    program: check_candidate.py, check_source_logs.py and nested_crate.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Recomputes, apart from the crate and the tools, every exact premise of a check2
      candidate on its declared net (the measure and its mass, lemma N0's premises and
      the last bin, the per-bin domains, lemma F3's caps, the semantic digest), reads
      the source's run and control logs and receipts against the candidate, and ties
      the nested verifier archive to its build digest and, file by file, to reviewed
      source.
    source: [FN/fine_net_exact.py, FN/check_candidate.py, FN/check_source_logs.py, FN/nested_crate.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review lane of the wand125-lb import (think-u0av), strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          The source's commits name Claude as co-author. Written by a Claude agent
          prompted separately from the source and from the intake lane, in files of
          their own that import nothing from the crate, the tools or the source.
      note: >-
        Written after reading SOUNDNESS.md, the crate's axis, interval, exact and
        certificate modules, the census control and the exact evaluator in devtools,
        and the source's candidate format and digest rule. The producer's checker is
        this repository's crate adapted, so no clean room with respect to it is claimed.

  - id: V-wand125-lb-review-fine-net-exact-capture
    program: fine_net_exact.capture, driven by check_source_logs.py and sample_directions.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The exact mass a closed core at a given centre and net angle captures from a
      format M measure on a declared net, by Sutherland-Hodgman clipping of the rotated
      core against each D4 image in fractions. Decides the capture at the poses it
      evaluates: the source's control witnesses, the tightest leaf centres of the
      source's runs, and the leaves and witnesses of the reviewed sqverify-fast at the
      directions sample_directions.py runs. It agrees with the crate's exact witnesses
      digit for digit at 99 oblique poses.
    source: [FN/fine_net_exact.py, FN/check_source_logs.py, FN/sample_directions.py]
    independence_record: R
    independence:
      read: [mathematics, specification, certificate-format, producer-code, producer-output]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review lane of the wand125-lb import (think-u0av), strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        Clipping and areas in fractions, written from the claim's definition of the
        density; no code of the crate's oracle, of mixed_exact or of the source.

  - id: V-wand125-lb-review-axis-sweep-emulation
    program: sweep_emulation.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [numerical-f64, exact-algebraic]
    role: premises
    summary: >-
      A transcription of sqverify-fast's axis vertex sweep and directed rounding into
      Python floats, walked at one column, which reproduces the crate's certified bound
      to the last digit and reports the enclosure the crate does not: a diagnostic of
      the census control's axis tolerance. It decides nothing.
    source: [FN/sweep_emulation.py, FN/fine_net_exact.py]
    independence_record: R
    independence:
      read: [mathematics, producer-code, producer-output]
      clean_room: false
      shares: [axis::verify_axis, interval::Iv]
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review lane of the wand125-lb import (think-u0av), strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: >-
          Transcribed from the crate's Rust by eye, not imported; the crate is this
          repository's, which the producer adapted.
      note: >-
        Its purpose is to share the sweep's arithmetic: equality of its lower end with
        the crate's bound is what shows the enclosure it reports is the crate's.

  - id: V-wand125-lb-review-linear-premises
    program: check_linear_candidate.py, check_linear_records.py and check_inputs_sample.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: premises
    summary: >-
      Recomputes, apart from the tools, every exact premise of a linear certificate (the
      measure, its mass, its D4 invariance, the digest, the net, the centre domains),
      the arithmetic of its scope against the closed forms and the case records, its
      201 records and the digests its documents state, and a sample of the proof
      bundle's inputs against the exact images.
    source: [LN/linear_exact.py, LN/check_linear_candidate.py, LN/check_linear_records.py, LN/check_inputs_sample.py]
    independence_record: R
    independence:
      read: [mathematics, certificate-format, producer-code, producer-output, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review lane of the wand125-lb import (think-u0av), strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
      note: >-
        The export order of the images and the digest rule were read from the
        producer's retained unified_measure.py; the checker was not re-read, the 2
        October review having read it.

  - id: V-wand125-lb-review-linear-exact-capture
    program: linear_exact.capture, driven by point_checks.py
    author: Squares Project (Levy)
    provenance: first-party
    language: [Python]
    methods: [exact-algebraic]
    role: decides
    summary: >-
      The exact mass a closed core captures from a point, segment and rectangle measure
      at a given centre and net angle, in fractions. Decides only the fifteen captures
      point_checks.py evaluated, which are no evidence of the claim.
    source: [LN/linear_exact.py, LN/point_checks.py]
    independence_record: R
    independence:
      read: [mathematics, certificate-format, producer-code, earlier-review]
      clean_room: false
      shares: []
      written_by:
        - kind: ai
          system: Claude (Anthropic)
          setting: the stage-4 mathematical review lane of the wand125-lb import (think-u0av), strong tier, max reasoning
      overlaps_producer:
        extent: system-family
        separate_prompt: true
        separate_code: true
        note: As above.
```

An evidence entry for each thing a run here decided or sampled would cite these, with
`coverage: {extent: sample, checked: …, of: …}`, `origin: replayed-here`,
`relationship_to_generator: independent-implementation` for the exact captures and
`shared-components` for the sampled directions, and be cited by the case records at n =
37, 39, 44 and 145 and by no result: the 96 control witnesses of the three check2
certificates (checked 96 of 96, deciding the author’s controls), the 36 tightest leaf
centres and the 18 directions run here (samples of (H3)), and the fifteen linear
captures (a sample that decides nothing).

## 11. Disclosure

No review of these four results existed when this one was written, so nothing of the
kind was read. Before writing, the lane read the intake lane’s packets, receipts,
register plans and bead notes, and the route reviews of §0, which review the crate, the
census control, the check2 route and the linear checker on other certificates; the 6
October check2 review’s FN-1 is why `check_source_logs.py` reads each run’s
`input_sha256`, which is the published candidate’s in all three runs here.
The lane also read jlevy/squares#543, where the owner’s questions on retention and on
the axis tolerance stand, before writing §5; §5 answers the mathematical question and
leaves the decision where it is.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
