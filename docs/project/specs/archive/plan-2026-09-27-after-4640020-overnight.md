# Plan: An Overnight Queue After s(17) > 4.640020

**Date:** 2026-09-27 · **Workflow:** W10 review, planning and oversight · **Agenda:**
[agenda-042](../../../../packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md),
BC-392 · **Supersedes in part:**
[the 2026-09-25 plan](plan-2026-09-25-after-r052-planning.md)

Two days after R052, Kleddamag published v1.1.0 of the n = 17 certificate
(`github.com/Kleddamag/17-squares-certified-bound` at `13821ddfa241`), proving
$s(17) > 232001/50000 = 4.640020$, and wand125 published rectangle-density certificates
for n = 18 to 78 that pass every low-n rung this repository held.
The owner asked for a deeper look at what should run next, with an eye to CPU-bound work
that can run overnight and confirm or move something.
This document keeps one Fable max assessment, its probes, and the queue it settles on.
Nothing in it moves a bound.
The 4.640020 review lives at
`docs/project/reviews/review-2026-09-27-n17-kleddamag-4640020.md` on the intake branch;
the certificate is registered at `V4/C3` there, superseding R052.

**Update, 2026-09-27, after $4.66001$.** Later the same day Kleddamag published
$s(17) > 466001/100000 = 4.66001$ (`57519bb`), superseding v1.1.0’s $4.640020$; the
[4.66001 review](../../reviews/review-2026-09-27-n17-kleddamag-466001.md) found no
mathematical defect, every rule again of capacity one, and the ledger flat at its
minimum on all 2,168 rows.
The passages below that depend on the n = 17 bound (“Where Things Stand”, the ceiling
bullet, BC-393, BC-387, “Not selected”, BC-393’s command and the expected gains) are
retargeted as that review’s §7 lists.
The probe readings of v1.1.0 are kept as they were measured.

## Where Things Stand

- **n = 17.** $s(17) > 4.66001$ (Kleddamag `57519bb`, `V4/C3` on replay, superseding
  v1.1.0’s $4.640020$), against Bidwell’s $4.67553$: a gap of $0.0155$, down from
  $0.0555$ three days ago.
  The 4.640020 review proved the capacity-one ceiling lemma (its §8) that the previous
  plan left unreviewed.
  Guzhou0806’s R052 continuation at $4.62003$ is superseded.
- **n = 11.** Unchanged: $31/8 < s(11) \le U$, rung 0 closed (T-035, T-036), rung 1
  priced out with the present relaxation, BC-384 blocked on BC-388 and BC-389. The
  owner’s hold of 2026-09-14 reads: “The owner has paused heavy computer-assisted proof
  work aimed at very small lower-bound increments.
  The current objective is either a material improvement to the $n = 11$ bound or a
  substantially simpler proof of `s(11) >= 3.82`.”
- **Other n.** wand125’s rectangle certificates (tokoharu’s format, his verifier) now
  stand at $4.695$, $4.815$, $4.895$, $4.985$ for n = 18 to 21 and cover n = 26 to 32,
  37 to 45, 51 to 61 and 66 to 78; another lane is registering them.
  After that intake the weakest verified rows below n = 100 are n = 50
  ($1 + \sqrt{37} = 7.083$ against $7.571$), n = 65 ($8.071$ against $8.536$) and n = 82
  to 89 ($9.06$ to $9.49$ against $9.54$ to $9.95$), each a gap of about $0.45$ to
  $0.49$; n = 12 stays at $3.96$ against $4$. (Daniel’s claims, which arrived during
  this block and are handled under “Late Additions” below, would move n = 12 to
  $3.968616$, n = 21 to $4.995$ and settle n = 32.)

## What the Probes Found

Probe scripts are kept in `attic/planning-160/`, outside the record, as the previous
plan kept its own in `attic/planning-159/`. Each ran under fifteen minutes on at most
two cores of a shared four-core Linux host; none is a measurement the record relies on.

### n = 17: the certificate’s shape, its saturation, and the ceiling

- **Every atom still has capacity one, and the native route needs one new atom.** v1.1.0
  has 2,048 angular rows of equal half-tangent width $2.02\times10^{-4}$, 8,876 physical
  sites and 4,328 charged images: 2,216 points (280 orbits), 1,224 two-of-three, 432
  three-of-four with coefficients $[2,1,1,1]$ (budget $\lfloor5/3\rfloor = 1$), 208
  three-of-five, 8 four-of-seven, and 240 intersecting-rule images (30 orbits of 8) on
  seven sites with listed winning subsets that pairwise intersect (`n17/rule_census.py`,
  `rule_census2.py`). The declared budget $16{,}978{,}369{,}232$ re-derives exactly when
  each intersecting-rule image counts one.
  The parent-core loader (`verify_guzhou_r052_native.py`) handles points and $k$-of-`m`
  thresholds with multiplicities already; the winning-subset rule is the one atom class
  it lacks, and 8,876 sites exceed the frozen 8,192-site ceiling, so the BC-386 cap lift
  is still needed. R052’s sizing rows ran 1.9 to 11 s each on 8,937 atom rows; at 4,328
  atom rows and 2,048 rows the full native run is about 1 to 6 CPU-hours, not the 15
  R052 needed.
- **The dictionary is saturated at a plateau.** From the source’s own ledger
  (`n17/saturation.py`): 895 rows sit at exactly $1{,}000{,}000{,}031$ units and 1,901
  within $10^{-4}$ of it; one row is at the binding $\Gamma = 998{,}727{,}933$, a
  relative $1.27\times10^{-3}$ below the plateau, 18 rows are within $10^{-4}$ of
  $\Gamma$ and 65 within $10^{-3}$. If the source’s LP was optimal, reweighting the same
  dictionary raises the ratio $17\Gamma/M$ from $1.0000003$ to at most $1.00127$; what
  that buys in side is not measured here (the fixed-weight charge falls in steps, by
  `6.5 %` on row 0 within $\Delta S = 0.0005$), and
  $S \times 1.27\times10^{-3} \approx 0.006$ is an order of magnitude under the
  assumption that charge and side trade one for one.
  A larger gain needs new sites, which is Kleddamag’s unpublished “4.65 research”.
  (It published the same day as $4.66001$, with 20,856 sites and a ledger flat on every
  row; see the update above.)
- **The ceiling lemma covers v1.1.0 whole, and its sharp form is clique-weighted.** Two
  cores that both fire a coefficient threshold with $\lfloor\Sigma a_i/k\rfloor = 1$
  share a site, as do two that both contain a winning subset of a pairwise-intersecting
  list, so every firing set is pairwise overlapping.
  Hence for any family $F$ of unit squares in $[0,S]^2$ and any weights $y \ge 0$ with
  $y(K) \le 1$ on every clique $K$ of $F$’s interior-overlap graph, or of any supergraph
  of it such as the conservative graph the checker builds, $\Sigma y \le M/\Gamma$ for
  every certificate of this architecture at side `S`, and $\alpha^{\ast}(G_F) \ge 17$
  refutes them all there.
  The triangle-free family of 34 with $y = \tfrac{1}{2}$ is the special case.
  Since valid capacity-one certificates exist at $4.640020$ and $4.66001$, no such
  family fits at any $S \le 4.66001$: **H-243’s $4.63$ and H-248’s $4.65$ and $4.66$
  targets are refuted by the certificates themselves**, and the architecture’s ceiling
  lies in $[4.66001, s(17)]$, so below $4.67553$.
- **At $4.65$ the family search is neither easy nor hopeless.** A two-minute anneal
  (`n17/triangle_free_probe.py`) over 34 squares, started from two reflected copies of
  Bidwell’s packing (114 triangles) and from random, ends at 2 triangles from both
  starts, with $\alpha^{\ast} = 16$ on the resulting graph against the 17 needed, which
  at $N = 34$ is what two disjoint triangles cost; the anneal’s objective is the
  $y = \tfrac{1}{2}$ special case, and the BC-387 search should optimise $\alpha^{\ast}$
  over families of any size up to 64, $K_4$-free 51-families included.
  Eight-minute runs at $4.65$ from both starts end the same way, two triangles and
  $\alpha^{\ast} = 16$; at $4.66$ the two-copies start ends at three triangles,
  $\alpha^{\ast} = 16$ (`n17/probe-466.log`). Read as a price: the anneal does not find
  the family, and it does not show one is far away either, so the exact search is worth
  its three hours of build.
  The exact checker for a found family mostly exists: `geometric_graph_certificate`
  binds squares to a conservative overlap graph and `check_weighted_clique_certificate`
  proves a weighted-clique bound on up to 64 vertices, so only containment and a driver
  are new.

### n = 11: prices only

- **The census costs about 15 s a start** (`n11/census-timing`): six jolted starts about
  Trump at scale $0.1$ took 11 to 19 s each on one worker with the 8 s quench cap and a
  20 s filter cap, all four controls passing.
  BC-388’s 20,000 starts are about 80 CPU-hours, about 12 hours on seven workers; the
  frozen-angle variant skips the angle bracket and should be cheaper.
- **BC-390 is launcher-only and admitted at half-width $10^{-4}$.** `box_setup` admits a
  box holding $t^{\ast}$ while `2·max(root_hi − t_lo, t_hi − root_lo) < ρ = 4.04×10^-3`;
  at half-width $10^{-4}$ the reach is $2.02\times10^{-4}$. exp-232’s rate was about
  4,450 nodes/s on nine workers, so $1.7\times10^{8}$ nodes is about 95 CPU-hours: 12
  hours on eight workers, resumable by subtree.

### n = 12 and the weak rows: the rectangle ladder from a trivial seed

- tokoharu’s `push.py` from its trivial seed at n = 12 (`n12/push-n12.log`, pinned clone
  at `84bebef`) starts at $L = 3.3808$ and accepts $1/200$ rungs every 60 to 100 s with
  LP mass $9.009$ against budget 12, so the certificate has room and the climb to $3.96$
  is about two hours at that step and under one at `--step 1/50`. The informative part
  begins above T-017’s $3.96$; the probe cannot say where it stops.
- The same driver is documented from seed at n = 53, so the trivial seed reaches the
  weak rows; per-rung cost there is not measured here and is the first thing the run
  reports.
- The [tokoharu review](../../reviews/review-2026-09-22-tokoharu-density-mathematics.md)
  found DENS-1: `push.py --from` accepts a wrong count and stale metadata.
  From-seed runs do not take that path, and no rung is admitted on the driver’s status;
  admission is the exact-rational preflight and an unmodified `run_verify.py` replay,
  the route the wand125 intake is building.

## Decisions

Each selected item is an agenda-042 BC with a bead.
The overnight budget is the record’s host, about ten workers for one night; the day
builds are about three agents.

| BC | Case | Commitment | Kind | Routing and price | Stop or reconsider |
| --- | --- | --- | --- | --- | --- |
| BC-393 | 17 | Native `C4` decision of the $4.66001$ certificate (`57519bb`): a loader for its schema (`sets`, `coefficients`, `winning_masks`), a winning-subset atom taking masks on up to 12 sites in the parent-core and interval routes with its capacity-one lemma reviewed, the cap lift to at least 20,856 sites behind a byte budget, then all 2,168 rows | tool validation | Opus xhigh 3–4 h build; Fable xhigh 1 h on the atom’s lemma and the box bounds of a monotone rule; about 2–12 CPU-h on 2 workers | A refused row is a refusal; a row below $\Gamma$ contradicts two exact sweeps and is a loader defect until shown otherwise |
| BC-394 | 82, 50 | Rectangle-density ladders from the trivial seed with the pinned `push.py`, n = 82 toward $\frac{93}{10}$ and n = 50 toward $\frac{73}{10}$; every accepted rung admitted only by preflight plus verifier replay | research | Launcher only tonight; one search worker each plus two verify workers; per-rung cost read from the first rungs | The driver gives up below target, or the first rung’s certificate fails preflight; an accepted rung above the register is a candidate for the wand125-format intake, never a bound by itself |
| BC-395 | 12 | The same ladder at n = 12 toward $\frac{399}{100}$ | research | Launcher only; one worker; about an hour to reach $3.96$, unknown after | Gives up below $3.9687$, which prices the rectangle route at n = 12 as no better than Daniel’s $3.968616$ |
| BC-396 | 45 | Daniel’s zero-margin closed cover transferred to $k = 7$ (H-252), after the intake review | research | Fable xhigh 1–2 h on the method; Opus xhigh half a day if the search needs adapting; about 4 CPU-h per cover at $k = 7$ | The cover search stalls at or above mass 45, a negative about the search only |
| BC-390 | 11 | Rung 0 widened to half-width $10^{-4}$ (H-247), unchanged instrument | research | Launcher only; eight workers overnight, resumed the next night if needed; then the reader | As registered: the enclosure reach meets $\rho$, or a verified non-degenerate leaf below $U$ |
| BC-387 | 17, 12 | Retargeted again: the clique-weighted family search ($\alpha^{\ast} \ge 17$) at $\frac{4675}{1000}$ first and $\frac{467}{100}$ second, H-248; $\frac{465}{100}$ and $\frac{466}{100}$ are refuted by the $4.66001$ certificate; the exact checker is assembled from the graph and clique tools; n = 12 unchanged (H-244) | research | Opus xhigh 3 h build; runs of minutes in any free slot | No family found is inconclusive; a found family, exactly checked, caps the architecture and prices the first-party producer |
| BC-388 | 11 | Unchanged; second night, after its build | research | Opus high 2 h build; about 80 CPU-h on seven workers | None; a measurement |

**Retired or retargeted.** BC-386 (native R052) is superseded by BC-393: R052 is no
longer the bound, and the BC-393 loader accepts R052’s schema as a subset if a second
data point is ever wanted.
BC-391 (n = 21 at $4.89$) and idea 255 are superseded by wand125’s $4.985$; BC-380’s
parent clip loses its n = 18 and n = 21 targets ($4.695$ and $4.985$ stand) and keeps n
= 12 only. BC-384 stays blocked on BC-388 and BC-389. H-243’s $4.63$ and H-248’s $4.65$
and $4.66$ targets are refuted by Kleddamag’s certificates; H-248 continues at
$4675/1000$ and $467/100$.

**Not selected.** A first-party n = 17 producer beyond $4.66001$: the published
dictionary’s ledger is flat at its minimum on all 2,168 rows, the next cell value within
$10^{-7}$, so its reweighting is worth nothing and idea 259 closes; the producer for
intersecting rules does not exist, and BC-387’s price at $4675/1000$ decides whether the
architecture can close the remaining $0.0155$ at all.
The Kleddamag/Guzhou family at n = 18 to 21: the rectangle route now leads there by
$0.015$ to $0.1$, and the point parent-core lock at n = 18 was $4.68 < 4.695$. BC-389 is
a build, not CPU. Any n = 11 lower-bound increment stays under the owner’s hold; BC-390
is a restricted-family theorem, not an increment.

## Tonight’s Queue

On the record’s macOS host, in this order, with the commands as they would be typed from
the repository root.
The rectangle ladders need tokoharu’s dependencies (`numpy`, `scipy`, `numba`,
`highspy`) in a scratch Python 3.12 environment; `uv venv --python 3.12` then
`uv pip install -r requirements.txt` in the clone.

1. **BC-390, eight workers, launched first.** From exp-232’s frozen box
   $[91442076901/250000000000, 73154061521/200000000000]$, centre
   $t^{\ast} = 0.3657693076045$, the widened box is
   $[731338615209/2000000000000, 731738615209/2000000000000]$.

   ```bash
   cd packing && .venv/bin/python3 -m cases.trump11.fixed_angle_tree box \
     --t-lo 731338615209/2000000000000 --t-hi 731738615209/2000000000000 \
     --strong 6 --node-cap 20000000 --split-depth 3 --workers 8 \
     --out ../attic/rung0-wide/h247.jsonl.gz --summary ../attic/rung0-wide/h247-summary.json \
     --stop-launching-at <08:00 local, ISO> --stop-at <08:45 local, ISO>
   # next night, if subtrees remain: add --resume-subtrees <indices from the summary>
   # then the reader:
   .venv/bin/python3 -m cases.trump11.fixed_angle_tree_check ../attic/rung0-wide/h247.jsonl.gz --workers 10
   ```

   The `--out` and `--summary` spellings follow exp-232’s frozen command; the digests of
   `fixed_angle_tree.py` and `fixed_angle_tree_check.py` are checked against exp-232’s
   before launch, as that record did.

2. **BC-394, n = 82 then n = 50, two workers.** From the pinned clone of
   `tokoharu/square-packing-density-bounds` at `84bebef`:

   ```bash
   cd <clone> && <venv>/bin/python src/push.py --n 82 --target 9.3 --step 1/50 \
     --workers 2 --out <attic>/ladders/n82
   cd <clone> && <venv>/bin/python src/push.py --n 50 --target 7.3 --step 1/50 \
     --workers 1 --out <attic>/ladders/n50
   ```

   Each accepted rung leaves a self-contained certificate directory.
   In the morning the highest rung of each goes through the intake route: the exact
   preflight generalised from `devtools.audit_tokoharu_density` (which today binds only
   the three retained cases) and an unmodified `run_verify.py --workers 4` replay, then
   a Fable max W2 review before any register row.
   A mass below 82 at side $L$ covers every n ≥ 82 whose verified row is below $L$.

3. **BC-395, n = 12, one worker,** after the n = 50 ladder ends or in the spare slot:

   ```bash
   cd <clone> && <venv>/bin/python src/push.py --n 12 --target 3.99 --step 1/50 \
     --workers 1 --out <attic>/ladders/n12
   ```

   The intake lane’s `--full` replay of Daniel’s two $s(32)$ covers (about 5.2
   CPU-hours) shares the two ladder workers once n = 50 ends; see “Late Additions”.

4. **Day builds, so that the second night runs BC-393 on two workers, BC-388 on seven
   and BC-387’s searches in the gaps:** the $4.66001$ loader and winning-subset atom
   with the cap lift (BC-393), the frozen-angle census (BC-388), and the family search
   with its checker driver (BC-387). The first two land as reviewed commits before their
   runs start. BC-393’s run:

   ```bash
   cd packing && uv run --frozen --all-extras --group dev python -m devtools.verify_kleddamag_n17_native \
     --all --workers 2 --output resources/web/<n17-kleddamag-466001 packet>/receipts/native/full.json
   ```

   (`verify_kleddamag_n17_native` is the tool BC-393 writes, on the pattern of
   `verify_guzhou_r052_native`.)

## Late Additions From the Coordinator

Three discoveries arrived while this plan was being written.
Other lanes review and register them; this section only says what they change here.

- **evand/square-packing (`167d842`) claims $s(32) = 6$,
  $s(12) \ge 15680/3951 = 3.968616$ and $s(21) \ge 5000/1001 = 4.995$.** The $s(32)$
  proof is a weighted closed cover of $[0,6]^2$ of mass $31.71 < 32$ in which every
  closed unit square captures at least 1, checked at margin zero by two checkers sharing
  no code, with a Lean top theorem from that one hypothesis.
  Its `--full` replay is about $2.8 + 2.4$ CPU-hours over 7,200 root boxes per cover, so
  the intake lane’s replay fits tonight on two workers in about three hours; it is that
  lane’s item, not one of this plan’s. For transfer: the construction reached the
  endpoint at $k = 6$ and fell short at $k = 5$ and $k = 4$, where Daniel’s own record
  pins the pure cover LP at exactly $12.000$ on every pose set tried, so the $n = 12$
  endpoint is not where it goes next and $n = 11$ is below Kleddamag’s bound already
  ($3.8143$). The transfer is upward in $k$: **$n = 45$ at side $7$** (wand125 holds
  $6.955$), then $n = 60$, $77$ and $96$. That is H-252 and BC-396: a Fable xhigh
  reading beside the intake review, then the cover search and the margin-zero check at
  $k = 7$, about 4 CPU-hours per cover by scaling the $k = 6$ census, on the second
  night if the tools take $k$ as a parameter.
  At n = 12 the $3.968616$ bound passes H-249’s first target, so H-249 and BC-395 now
  aim at $399/100$ and give up below $3.9687$; at n = 21 $4.995$ passes wand125’s
  $4.985$, and BC-391 stays retired.
- **Upper-bound reports** (franciscouzo and griffcass for many n in 68 to 307,
  JoostdeWinter at n = 211, $14.9979607$): an exact replay of a reported packing costs
  seconds per case through the
  [upper-bound certification pipeline](plan-2026-09-22-upper-bound-certification-blocks.md),
  so the intake is an idle-slot item for whichever lane owns it; it moves reported, not
  verified, rows until certified.
- **Guzhou’s C++ kernel** runs an R052-scale sweep (15,727 rows) in about 39 minutes on
  one core. It shares the source’s geometric lineage, so it is a faster replay of the
  same method and not the method-distinct decision BC-393 exists for.

## Expected Gain, Ranked

1. **BC-394.** The largest prize on the board: $+0.2$ to $+0.35$ of verified side on
   gaps near $0.49$, at n = 50 and at n = 82 with n = 83 to 85 carried by mass coverage,
   for a few CPU-hours of an external tool this repository has already reviewed.
   It certifies at `V4/C3` through tokoharu’s interval verifier plus the exact
   preflight.
2. **BC-393.** A method-distinct `C4` decision of the current n = 17 bound, the rating n
   = 11 has and n = 17 lacks; about 2 to 12 CPU-hours once built.
   It moves no bound.
3. **BC-390.** T-035 widened a hundredfold in tilt: a theorem about the settlement
   ladder, launcher-only, and the one item that is pure overnight CPU today.
4. **BC-387 retargeted.** Decides in minutes of CPU whether any certificate of the
   present architecture can reach $4.675$, which is the decision behind building a
   first-party n = 17 producer at all.
5. **BC-396.** If Daniel’s construction carries to $k = 7$, an exact value, $s(45) = 7$,
   for about 4 CPU-hours of checking; the uncertainty is whether the search finds a
   cover, which it did at $k = 6$ and not at $k = 5$.
6. **BC-395.** A possible $+0.01$ to $+0.02$ at n = 12 above Daniel’s $3.968616$ on an
   endpoint-friendly case, with no prior evidence either way.
7. **BC-388.** Pricing only; it moves no bound and selects BC-384’s design.

## Order

1. **Tonight:** BC-390 on eight workers; BC-394’s two ladders on two; BC-395 in the slot
   that frees first.
2. **Day:** BC-393’s loader, atom and cap lift as a reviewed commit; BC-388’s census
   build; BC-387’s search and checker driver.
   The morning also admits or rejects the ladders’ top rungs.
3. **Second night:** BC-393 on two workers, BC-388 on seven, BC-387’s searches in the
   gaps; BC-390 resumed if subtrees remain; BC-396’s $k = 7$ check if the day’s reading
   admits it.
4. **Next:** BC-389’s build; a Fable max reading of BC-388 and BC-389 selects BC-384’s
   design, as before.

The selected entry for this order is BC-390 under its existing bead, with BC-394 beside
it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
