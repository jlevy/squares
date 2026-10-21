# packer: searching for square packings

Started 2026-10-04.  Goal: better packings of n unit squares in a square, first target s(90) < 10 (WISHLIST §P1); method goal:
a general solver (any n), since all known approaches fail in ways we now partly understand.  `PACKER.md` is the chronological lab
log (what was tried, in order, with numbers); this file is the map.  Everything here is **screening** (f64) unless stated.

## Status (10-14)
* Current state and next steps: `HANDOFF-2026-10-14.md`, then `../../TODO.md` "Packings" and `../../tasks/packer-arch-2026-10-14/`
  (architecture review, TT2 plan).  Strategy numbers: `CLAIMS.md`; open anomalies: `CONFUSIONS.md`; full log: `PACKER.md`.
* Records so far from this engine: s(266), s(270), s(272) (sweep, 10-06), hunts 1-3 (132, 155, 308, 343, 344, ...),
  time travel 154 (#552), compositions 339 / 364 / 375 (#584) and 365 / 370 / 460 (#596).  None at n <= 324 since 10-12.
* Production paths: `chain.py` -> `explore.py` (local search over 139 non-grid n), `fresh.py` -> `compose2.py` (new public
  packings -> pieces -> two-piece compositions), `harden.py` (opt-in soft-to-rigid).  All finish in `fq`; records go
  through `candidate.py`.  The store (`pk/`, `runs/store.sqlite`) holds every packing; `expansion` is the ledger of
  CPU spent per expanded packing (10-14).
* The s(110) material below (10-04 .. 10-06) is the calibration history; `s110-landscape.md`, `landscape/`.

## Tools
| file | what |
|---|---|
| `src/main.rs` (`packer`) | Rust engine.  `relax [--squeeze \| --squeeze-pen]`: L-BFGS on SAT overlap energy at fixed side; bisection squeeze; penalty-continuation squeeze over (config, s) (μ0 = stiffness: low = soft/exploring, high = precise).  `hop`: basin hopping, descending target.  `hhop`: hard-square basin hopping with event chains (slide until contact, pass remainder on), `--forbid-lines k`, `--soft p` (soften/re-harden). |
| `chain.py` | **Production record hunter.**  Rounds of `explore.py` per n (start = best(n) from `--src`, n + k removal / insertion seeds, carries, library); dirty-first scheduling; 10-14 defaults: value reward with store-wide novelty (`--reward legacy --novel run` = pre-10-14), `--as-of` for time travel, ledger rows per round. |
| `explore.py` | Quality-diversity basin explorer: archive of polished minima, cell-uniform parents (+ elite / frontier / sparse shares), 11 live move kinds with a Thompson bandit (`pk/bandit.py`), fq screen -> polish per proposal. |
| `harden.py`, `src/harden.rs` | Nakajima soft-to-rigid momentum dynamics + fq polish (10-14; opt-in). |
| `candidate.py` | **Record candidate → registration packet** (10-12).  exactsolve, both exact checkers, read-only live check (register witness + case page, issues naming n, Ellsworth's catalogue, store frontier), matching distance, optimality facts, `--chain` lineage, regularized view (private REFRESH dir), `--stage` into `candidates/`, `--import`.  `candidate.py --live N [S]`: just the live check.  The issue text is still drafted by hand in `outreach/`. |
| `pk.py ingest` (`pk/ingest.py`) | **Standing ingestion** (10-14): sync-register + watch --apply + `fresh.py run --since <last ingest>` (n <= 324) in one command; fresh outputs + store rows added since -> near-miss queue.  State `runs/ingest/state.json` (advanced only when every step succeeds).  Dry run by default; nothing posted. |
| `pk.py nearmiss` / `pk.py finish` (`pk/nearmiss.py`) | **Near-miss queue + finisher** (10-14): our packings (no public sighting) at n <= 324, not grid, 1e-6 < gap to frontier_now < 1e-3, <= 2 per n, from the store (chain / explore runs, battery, ...) and from compose2 / fresh / harden output dirs (`nearmiss tag --from DIR`); store table `nearmiss` + tag `nearmiss`.  `finish` drains it cheapest first: fq long polish, harden 1 round, NM harden recipe (gap < 5e-4); results into the store (`finish:<stage>`) + ledger (mechanism `finish`); below frontier_now - 1e-9 -> candidate.py (`--candidate`, else printed). |
| `fresh.py` | **Fresh-packing pass** (10-13): new public packings -> corner crops (rectlib) + whole pieces -> `compose2 --new-from` -> polish -> `candidate.py`.  Run after every sync. |
| `compose2.py` | Two-piece composer: store pieces in opposite corners + exact upright fill, bandit arms per n, probe / rank / polish / what-if (`--cf-eps`) / three-piece; `--new-from`, `--target public`. |
| `relax.py` | fq soft / shrink relax ops on composer layouts or store packings (`--ids`), iterated MBH (`--rounds`).  Its ops table lives in `pk/schedules.py` (10-20). |
| `submission.py` | registration-request draft from a `candidate.py` work dir (10-20): claim table, certificate files + SHA-256, checkers, local optimality, relationship to the prior record and to each `--start` (polish + compare: same minimum = refinement, else a new packing found from it; jlevy's 0.1 move counts), open questions on our issues.  Style guide and template: `SUBMITTING.md`. |
| `fillbench.py` | refill benchmark for `pk/fill.py` (10-20): delete the uprights or a disc at the band boundary from a good packing, refill with a config (`placer:k=v+schedule`), CS1 evaluate; rows scored at their own count (count - n, recovered, d_ref, pen, CPU). |
| `vband.py` | V-band constructor (staircase arms + exact fill) and `fit` of arms from a packing; idealised arms lose ~20 squares (PACKER 10-13). |
| `arms.py` | Real-arm library (6,760 arms), local operators, arm-pair composer, `holdout` yardstick (C31, C36). |
| `bench110.py` | n = 110 basin-entry benchmark (`refsets/h110_basinA`): `race` (pk/benchkit) and `report`; baseline C34. |
| `landscape_depth.py` | Is depth regional?  kNN / variogram / concentration over certified minima + parent -> child heritability (C32, C33). |
| `pk/benchkit.py` | Race benchmarks: replicates restart on event, rates per CPU, rate ratios, sequential rule (reusable for any n / event). |
| `fqreplay.py` | fq replay equivalence benchmark (10-13): record real explorer fq calls, replay under arms (binary / env / 1e-13 jitter null), compare class frequencies + speed, certify; `--skip` / `--stage` for held-out slices; class margins from the jitter arm (Q9b); C37-C41. |
| `perfbench.py` | End-to-end throughput: explorer proposals per measured CPU-h at n = 110 / 237 (8 x 6 min, frozen starts), perf score = geometric mean vs pre-session; resolves only ~+-10 % at 237 per pair of runs (C40). |
| `chainreplay.py` | Screen -> polish chain replay: does a screen-side change alter the cost of the polish after it?  Paired, with a jitter null; needs >= ~1,000 chains for ~5 %. |
| `src/lpipm.rs`, `src/ldl.rs` | fq's LP solver (10-13): Mehrotra IPM on the normal equations with native bounds (Q7, C39), factored by a schedule-replay LDL bit-identical to qdldl (Q10).  `FQ_LP_IPM=0` restores Clarabel; `FQ_IPM_PROF=1` prints section times. |
| `pk/bands.py`, `pk/effort.py` | Tilted bands / angle families of a packing; CPU per n from run manifests vs record events. |
| `chain_lineage.py` | Lineage of a `chain.py` result through its rounds (carries, library picks, `seed_k` seeds from n + k) back to a chain start, for credit.  Matches starts by their seed files' header sides. |
| `slp2.py` | **The local minimiser.**  Trust-region SLP on min s s.t. linearised separation, incidence contact model (`inc.py`), second-order correction, repair by uniform scaling; final jam test exhaustive over corner–corner branches (MILP).  20–50 iterations, ~3–5 s per descent at n = 110; outputs go straight into `../exact/exactsolve.py`.  `budget=` wall cap. |
| `inc.py` | Incidence contact model (f64 twin of `../exact/find_contacts`): corner-on-side rows; corner–corner pairs as disjunctions (relax-and-round LP; `shrink_milp` exhaustive). |
| `jobpool.py` | Process pool with a hard per-job kill (a HiGHS call can hang in C; `multiprocessing.Pool` cannot recover).  All census drivers use it. |
| `rigid.py` | Old one-axis-per-pair jam LP (false jams: kept for `slp2 --axis` comparison) and per-coordinate rigidity.  Pins BLAS threads to 1. |
| `gen.py` | Geometry helpers; `mis_fill2`: exact max axis fill (corner lattices + staircase candidates; HiGHS MILP).  Recovers record counts of 54, 71, 87, 88, 110, 132 from their tilted squares. |
| `layout.py` | Channel-row constructions (w, θ, set-back) + exact fill; `hyb` mode: genome MC scored by squeezed side, rejecting full lines. |
| `ftmc.py` | Free-tilted MC: perturb tilted squares, re-solve axis fill exactly, squeeze, Metropolis on side. |
| `census_exact.py` | Exact dedupe of census3 runs (every sub-k output through `../exact/exactsolve.py`, classes by S to 1e-20) + coupon statistics (f1/N, Chao1) per run, σ, pooled. |
| `census_roles.py` | Square roles per census trial (bands / axis / other) vs the start, by index. |
| `movegen.py` | Structural band moves (add / del / transfer / row / shift / rotate / drop_J; `--focus` adds uniform / rebuild) with keep-axis evaluation → slp2; several starts per run. |
| `beam.py` | Count-pair beam: best packing per role-count key from movegen/crop runs → movegen from them (`--n --k --procs --focus`). |
| `crop.py` | Side k+1 → k seeds: remove a row and a column strip, shift, fix the count, squeeze, slp2 (132 → 110 pass test, 110 → 90). |
| `mcmin.py` | Minima PT: Metropolis over slp2-quenched minima with replica exchange; moves kick / lkick / reinsert (hole-weighted) / crot / aswap / band, 1 + Poisson(λ) per proposal; time-based epochs, swap sweeps; `log.jsonl` per proposal. |
| `sweep.py` | Neighbour sweep over register records (`../exact/batch/inputs`): n+1 minus a square, kicks of n, quench, compare to register. |
| `census3.py` | Perturb (σ) → soft squeeze → slp2 → side, jam, full lines, fingerprint.  `basin.py`, `census2.py`: earlier variants. |
| `contacts.py`, `stress.py` | Feature-level contact graphs (corner-on-side, side-side, corner-on-wall); force networks (jam-LP duals). |
| `homotopy.py` | Rotate chosen squares between two configurations with everything else re-minimised; prints s(t) (barrier estimates). |
| `channel.py`, `surgery.py`, `gadget_mc.py`, `mkseed.py`, `slp.py` | Earlier experiments (superseded; kept for the record). |
| `lit-*.md` | Literature: optimizer techniques, stat-mech / basin counting, provenance of records n = 50–135. |

Formats: text `n s` + `x y deg` per line (centres).  `site2txt.py` / `txt2site.py` convert the site JSON.  Build: `cargo build --release`.

## Lessons (the short version; evidence in PACKER.md)
0. **Compare against jlevy's register, not our site mirror**: the mirror (Ellsworth's page, 09-30) is stale at the frontier
   (Couzo 09-27: s(110), s(130), s(132)).
1. **Grid attractor.**  Any state with a full line of k axis squares has side ≥ k; these states are a huge attractor at every
   level (random search, hopping, event chains, layout genomes all drift to them).  Reject full lines explicitly.
2. **s < k needs a transversal**: the tilted part must cross every row and column.  Local moves don't create one; structure does.
3. **Descent map matters more than it looks.**  L-BFGS on the SAT penalty stalls at kinks (face-to-face contacts): its "minima"
   are not first-order jammed (LP finds shrink directions), which made early censuses and search comparisons noisy at ~1e-3.
   slp2 fixes this.  Soft penalty squeeze (low μ0) is a useful *coarse* descent (funnel-level compaction); slp2 is the finisher.
4. **Integer count is the wrong objective** (needle landscape); squeezed side with full-line rejection works.
5. **Records' channels are not rigid lattice rows** (staggered, mixed angles, resting on axis squares): row genomes can't express
   them; they find relatives in other funnels (our 11.0076).
6. Records near n = 50–135 mostly come from constructions + seeded annealing; Ellsworth: plain SA "almost always gets stuck just
   above the trivial size due to stacked rows and/or columns".

7. **(10-06)** Grid obstructions include *staggered* axis chains (k axis squares, consecutive ones overlapping in the other
   projection), not just straight lines (`layout.axis_chain`).  Under our moves the grid is absorbing: hot replicas sink into it.
8. **(10-06)** Temperature alone doesn't connect funnels (minima PT runs A, B at 110 missed); reinsert-into-hole moves are
   destructive in every variant tried (a jammed packing has no hole: best insert costs ~0.4 penetration).
9. **(10-06)** Kick + good descent is short-range: reliable to matching distance ~0.02, rare beyond 0.05 (rediscovery, 51 record
   pairs).  It still finds records: s(266), s(270), s(272) (jlevy#399).  Kicking *older* packings finds basins the current
   record's kicks don't (272).  At n ≈ 270 give slp2 ≥ 180 s (60 s left 13 % unconverged, and that changed detection).

## Open threads (see also `../../TODO.md`)
* Exact solver (`../exact/`, done): KKT Newton + rational certificates; known gap: corner–corner contacts first-order only.
* Census: counting contact graphs honestly needs the force-bearing (max-support dual) network (parked).
* Funnel-level moves (junction flips; structure classes).
* Other targets for the same instrument: s(147) and the rest of WISHLIST §P; other "not yet analytically optimized" records.
