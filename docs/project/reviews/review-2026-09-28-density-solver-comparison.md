# Density Solvers Compared: Tokoharu’s and wand125’s Rectangle-Density Tools Against This Repository’s Certificate Stack

As a generator of lower bounds for $n$ between 18 and 95, Tokoharu’s rectangle-density
solver, driven by wand125, is more productive than anything this repository has built:
fifty standing certificates in three days, past every first-party point rung at $n = 18$
to $21$ by $0.015$ to $0.11$ and past the register’s previous best at 44 further counts,
27 of them Green’s or Nagamochi’s. As a verification stack it is narrower than this
repository’s: one checker, one method, a floating-point interval kernel of 126 lines
with a compiled-in margin, a runner that decides coverage but not the bound, and a
ladder driver with a known admission defect.
This repository cannot read its certificates natively at all, so the 47 rectangle bounds
still awaiting replay sit in the reported lane, and the three replayed ones sit at
`V4/C3` with no second method in sight.

The two are complementary rather than competing, and the recommendation follows from
that: leave generation of one-body density certificates to the community’s solver, run
it here only where nobody else is working and only behind the exact preflight and the
unmodified verifier, and spend this repository’s own build effort on what it alone does,
which is replay at scale, the register, and a method-distinct decision of the rectangle
language. The ranked plan is three bounded commitments: the replay queue for the 47
pending certificates (about 134 CPU-hours), the $n = 12$ ladder already queued as BC-395
with BC-394 retargeted away from wand125’s announced counts, and a rectangle-density
atom in the native interval route, priced by a pilot before it is committed to the 50.

This is a W3 insight document with a W2 check of every capability claim, written by a
Fable max sub-agent for Session 161 under bead `think-64le`. It registers nothing and
moves no bound.

## Scope and Sources

| Source | Pin | What was read |
| --- | --- | --- |
| [tokoharu/square-packing-density-bounds](https://github.com/tokoharu/square-packing-density-bounds) | `84bebef51856d46a19c145b035664324ba9572d3` (2026-09-23) | Every file of `src/` (22 Python files, 2,346 lines, and the 126-line `verify.cpp`), `tests/` (7 files, 531 lines), `README.md`, `requirements.txt`, `LICENSE`; `push.py`, `engine.py`, `certify.py` and `run_verify.py` in full |
| [wand125/square-packing-density-bounds](https://github.com/wand125/square-packing-density-bounds) | `096294aeb5f8b604df5890beda6cd601d05f4561`; branches `add-push-driver` (`93c0edd`) and `fix-ladder-driver` (`4aa6b7a`) | The tree and both branches, diffed against upstream |
| [wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) | `39d8ecc74d651b54ec977c331c8f2015b442a6c4` (2026-09-28) | `README.md`, `docs/`, `src/` (four point tools, 641 lines), `point_n21_L5/`, `point_n45_L7/`, the three `mixed_n50_*` directories; the 2,295-file tree manifest and the shipped `nagamochi_research` snapshot (411 files) |
| wand125’s X messages | [`supplied-messages.txt`](../../../packing/resources/web/wand125-x-update-2026-09-28/supplied-messages.txt) | The seven tool groups, each checked against the public trees |
| [evand/square-packing](https://github.com/evand/square-packing) | `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3` | `README.md`, `s12/README.md`, `s12/VERIFICATION.md`, the checker and Lean layouts |
| Kleddamag $4.66001$, Guzhou R052 and R068 | `57519bb7`, `3bf1095c`, `815b1626` | The retained packet READMEs and their reviews |
| This repository | working tree at `8b65af10c` | `sqpack.fractional` (every module’s contract), the native and audit tools under `packing/devtools/`, the certificate cases, `SYNOPSIS.md`, `CERTIFICATE-REACH.md`, `epistemics.md`, agenda-042 and the [post-4.640020 plan](../specs/archive/plan-2026-09-27-after-4640020-overnight.md) |

Prior reviews relied on: the
[density mathematics review](review-2026-09-22-tokoharu-density-mathematics.md), the
[checker-scaling review](review-2026-09-27-wand125-rectangle-scaling.md), the
[n = 50 mixed-verifier review](review-2026-09-28-wand125-n50-mixed-verifier.md), the
[native parent-core review](review-2026-09-22-native-n11-parent-core.md), the
[integration review](review-2026-09-22-external-square-certificates-integration.md), the
[4.66001 review](review-2026-09-27-n17-kleddamag-466001.md), the
[R052 review](review-2026-09-25-n17-guzhou-r052.md) and the
[evand review](review-2026-09-27-evand-s32-s12.md).

Two probes were run, each on one core for under ten minutes, from copies of the pinned
trees in the session scratchpad; they are recorded in [Probe](#probe) and nowhere else.
No file outside this document was changed.

## 1. Capability Matrix

Every cell names its evidence.
“Reported” marks a claim the source makes that no public file supports; where a
message’s claim has a public counterpart, the counterpart is named.

### 1a. Certificate language, generation and trust

| Capability | Tokoharu’s solver | wand125’s fork, drivers and certificates | This repository | evand | Kleddamag and Guzhou0806 |
| --- | --- | --- | --- | --- | --- |
| Language generated | D4-expanded rectangle densities: axis-aligned rectangles with rational masses, core side $B = \frac{9977}{10000}$, 201-direction net (`certify.py`, `docs/continuous-density-certificate.ja.md`) | The same, at $n = 18$ to $95$ (251 rectangle directories, [packet](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-28/README.md)); rectangle densities at threshold $\Gamma = 1$ (`mixed_n50_L740`); point measures at the closed unit side (`point_n21_L5`, `point_n45_L7`); earlier point certificates (`src/lp.py`) | Point atoms (`generate.py`, `colgen.py`), threshold $k$-of-`m` atoms (`threshold.py`, T-025), class certificates (`classcert.py`), relational and floor atoms (`relational.py`), exact ceilings and cutting planes (`ceiling.py`, `cutting.py`) | Weighted point covers at the closed unit side and on an angle net; mixed point-plus-segment covers on the interior grid lines (`s12/certificates/s21`, `s45`) | Points, $k$-of-`m` and coefficient thresholds, winning-subset (intersecting-rule) charges over adaptive parent-core rows $(a, b, t, B)$ ([4.66001 review](review-2026-09-27-n17-kleddamag-466001.md) §1; [R052 review](review-2026-09-25-n17-guzhou-r052.md)) |
| Language verified by its own checker | Rectangle densities only; `verify.cpp` reads one hex-float interval file | Tokoharu’s `verify.cpp` unmodified for the rectangle ladder; a 144-line copy with $\Gamma$ and the centre domain read from input for $n = 50$; `src/verify.py` for points (float64, `EPS = 1e-9`); evand’s `zmx2` for $n = 45$; a rational replay bundle for $n = 21$ | Points and thresholds by two routes (`certificate.py` sweep and `interval.py`; `threshold.py` and `threshold_interval.py`); relational atoms by two exact routes; adaptive parent-core certificates of points and thresholds (`parent_core.py`, `parent_core_interval.py`), which read Kleddamag’s $n = 11$, Guzhou’s R012 and R052 schema and evand’s angle-net files. **Not readable:** rectangle densities, mixed segment covers, winning-subset rules | `verify` (Rust, `i128` arrangement sweep), `zeromargin.py`, `zm_mixed.py`, `zmx2` (Rust); Lean 4 kernel checks for $s(13) = 4$ and $s(32) = 6$ (`s12/README.md`) | Exact integer event sweeps in Python and JavaScript (Kleddamag); a C++ arbitrary-precision kernel that sweeps R052’s 15,727 rows in about 39 minutes on one core (Guzhou, per the [plan](../specs/archive/plan-2026-09-27-after-4640020-overnight.md)) |
| How certificates are found | HiGHS covering LP with `rhs = 1.001` (`master.py`), dual-priced free rectangles at six widths (`pricing.py`), Sobol-plus-Nelder–Mead separation (`separation.py`), long-axis bisection (`refinement.py`), numba float screening over the 201 net angles (`net_screen.py`, `global_separation.py`); `engine.py` at fixed $L$, `advance.py` to grow $L$ from a certified incumbent, `seed_full_cover.py` for a trivial seed | Tokoharu’s engine, plus: fixed-support re-solves at a new side with exact rescaling of weights to $n - \frac{1}{100}$ (`scaling_experiment` in every candidate; README “fixed support, then scaling”); parents taken from point certificates with atoms replaced by small rectangles (README, $n = 45$, $n = 18$ to $28$); for $n = 50$ a separate initialisation, pricing and repair pipeline (`mixed_ladder_prepare.py`, `mixed_ladder_price.py` in the shipped snapshot, importing an unshipped `rectangle_budget_optimization`). **Reported only:** edge-rectangle budget recovery, parallel counterexample screening (3 to 4×), batched feedback of 16, LP warm start (40 to 50 % less solve time), a low-memory working LP for the rectangle engine, an axis-direction cache | Row generation with the exact sweep as separation oracle (`generate.py`), dual-driven site column generation (`colgen.py`, `run_fractional_colgen.py`), exact cutting planes on the packing side (`cutting.py`), threshold-atom separation (`produce_threshold_certificate.py`, G4 scale); floats propose, rationals decide | LP over candidate supports with the exact verifier as separation oracle, reweighted-L1 sparsification, column generation with exact reduced-cost pricing (`s12/VERIFICATION.md`, `search/TIGHTEN.md`) | Unpublished LP pipelines run by AI agents under direction; only certificates, checkers and controls are released (packet READMEs) |
| Verifier trust boundary | Outward-rounded binary64 intervals via `nextafter`; certified inscribed-polygon area; FTC derivative bound over centre boxes; `g++ -O2 -std=c++17 -fno-fast-math -ffp-contract=off`; divisor and rounding-mode guards are `assert`s live only without `NDEBUG` ([density review](review-2026-09-22-tokoharu-density-mathematics.md) §“Inscribed-polygon area”) | The same kernel; the $n = 50$ copy keeps `area_lower` and `slice` byte-identical and reads $E$, $c$, $s$, $\Gamma$ as Python-enclosed rationals ([n = 50 review](review-2026-09-28-wand125-n50-mixed-verifier.md) table); the point checker `verify.py` is float64 with an argued error budget, not directed rounding | Exact rational sweep (`Fraction`, or `int64` partial sums under a `2**60` mass limit with fallback, `sweep.py`) and a directed-rounding interval branch and bound that never expands an atom into signed rectangles (`interval.py`, `threshold_interval.py`); `decide_certificate` requires both to accept and to agree on the least cell mass | Exact integers and rationals throughout `verify`, `zeromargin.py` and `zm_mixed.py`; `zmx2` uses binary64 intervals for chord ends only ([evand packet](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md)) | Exact integer arithmetic on the certificate’s own scale; $17\Gamma - M$ is $2$ units for R052 and $54{,}340$ units for $4.66001$ |
| Margin the checker needs | Coverage at least $\frac{10001}{10000}$ on every box, compiled in (`verify.cpp:99`); the LP builds at $1.001$ and screens at $1.0005$ | $\Gamma = 1$ accepted by the modified copy; the standard ladder keeps $\frac{10001}{10000}$; every ladder candidate scaled to mass $n - \frac{1}{100}$ | The exact route decides at any margin, including endpoint certificates (T-025 at $\frac{191}{50}$); the interval route refuses a box it cannot resolve rather than accepting it, so a positive margin is needed for a complete interval verdict (`interval.py`) | Margin zero in the scale direction by construction for the closed covers ($s(32)$, $s(21)$, `s(45)`) | Positive integer margins; Kleddamag’s ledger flat at the binding $\Gamma$ on every row |
| Second method for the same certificate | None: one implementation, one method; the Python preflight decides the exact premises only | None; the $n = 50$ axis direction uses integer tables, a second implementation for one of 201 directions, not a second method ([n = 50 review](review-2026-09-28-wand125-n50-mixed-verifier.md) “Verdict”) | Built in for points and thresholds (`C4` on T-025 to T-036); the native parent-core route gives `C4` to Kleddamag’s $n = 11$ (`E-n011-kleddamag-3875-native-parent-core`), evand’s $s(12)$ (`E-n012-evand-15680-3951-native-parent-core`) and Guzhou’s R012 (`E-n017-guzhou-r012-interval-decision`) | Two independently written exact checkers per closed cover, sharing no code (`s12/README.md`); Lean kernel for two values | Two implementations of one event-cell method (`C3`, not `C4`, per both reviews) |
| Admission of an incoming certificate | `advance.py` binds the incumbent’s digest, summary and verifier hash; `push.py --from` does not (DENS-1, High); `run_verify.py` checks coverage, never `mass < n` (DENS-2) | Publication replays every standing certificate on a second machine with the unmodified verifier and byte-compared inputs (README “Checking them”); `verify_mixed_full_proof.py` binds digests, net and source hash for $n = 50$ | `audit_tokoharu_density` and `audit_wand125_rectangles`: duplicate-key refusal, exact decimals, interval enclosure of every datum, complete axis-event set, orbit mass, `mass < n`, candidate $n$ and $L$ against the pin, regenerated input digest against the accepting run, archive binding of 62 source files | `verify.sh` and CI rebuild the checkers and re-check every certificate on push (`.github/workflows/verify.yml`) | `check_integrity.py` over a 135-file manifest; `SOURCE_PIN.json` |

### 1b. Reach, cost, automation, licence and maintenance

| Capability | Tokoharu’s solver | wand125’s fork, drivers and certificates | This repository | evand | Kleddamag and Guzhou0806 |
| --- | --- | --- | --- | --- | --- |
| Demonstrated reach | $s(11) \ge 3.81$, $s(26) \ge 5.508$, $s(29) \ge 5.71$ (README) | 50 standing rectangle certificates, $n = 18$ to $95$, sides $4.695$ to $9.8418$, 116 to 931 orbits, 5.8 M to 45.2 M verifier nodes each (README standing table); $s(50) \ge \frac{37}{5}$ at $\Gamma = 1$; $s(21) = 5$ and $s(45) = 7$ by points | Own generator: $s(11) \ge 3.82$ (T-025, thresholds), $s(12) \ge 3.96$ (T-017), $s(17) \ge 4.59$ (T-019), $s(18) \ge 4.679$ (T-030), $s(19) \ge 4.80$ (T-020), $s(20) \ge 4.85$ (T-021), $s(21) \ge 4.88$ gate-accepted (exp-229). Native decisions of external certificates at $n = 11$, $12$, $17$ | $s(12) \ge \frac{15680}{3951}$ (still the best known), $s(13) = 4$ case-free, $s(21) = 5$, $s(32) = 6$, $s(45) = 7$ | $s(11) > \frac{31}{8}$, $s(17) > 4.66001$ (Kleddamag), $s(17) > 4.66044$ (Guzhou R068, replayed here, not yet reviewed) |
| Cost per certified rung, measured | Verifier: 73.5 s, 178.7 s, 92.7 s wall at 4 workers for $n = 11$, $26$, $29$ ([density review](review-2026-09-22-tokoharu-density-mathematics.md) table). Search plus certification: the probe below, 72 to 269 s per accepted rung at $n = 12$ from seed on one core, the verifier taking 40 to 142 s of it | Verifier: 495 s to 13,737 s wall per certificate at `ad43d29`, the axis direction alone up to 6,114 s ([checker-scaling review](review-2026-09-27-wand125-rectangle-scaling.md)); 47 pending replays about 134 CPU-hours ([packet](../../../packing/resources/web/wand125-rectangle-certificates-2026-09-28/README.md)); $n = 50$ L740 7.88 CPU-hours oblique plus 59 s axis; $n = 21$ point bundle 8,577 s on two M1 workers; $n = 45$ `zmx2` 204 s on 8 threads. Search cost: not published; one $n = 29$ rung “spent six hours” before scaling rescued it (README) | Search: row loop 320 to 650 s wall to converge at $n = 18$ (T-028 to T-030 rows of [covering-values](../../../packing/frontier/CERTIFICATE-REACH.md)), 1,616 s at $n = 20$ (T-021), eleven minutes at $n = 21$ (exp-229). Decision: 15 s exact and 67 s interval at $n = 21$; native $n = 11$ 6,197 s on two workers over 12,028 rows and 136 M boxes; evand $s(12)$ 752 s summed row time; R012 226 s on four workers; R052 priced at 8 to 49 CPU-hours by sizing; $4.66001$ priced at 2 to 12 CPU-hours once its atom exists | $s(32)$ cover 2.77 CPU-hours per `--d4` sweep; `zmx2 --full` 223 s CPU for $s(21)$ and 394 s for $s(45)$ here; Lean $s(32)$ 13.8 CPU-hours ([evand packet](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md)) | $4.66001$: 5,454 CPU-seconds for the independent sweep here; R052-scale C++ sweep 39 minutes on one core |
| Automation and resumability | `push.py`: one command from $n$ to a certified ladder, one directory per accepted rung, JSONL log, step halving and widening, stops after four consecutive failures; `engine.py` and `advance.py` checkpoint state and a HiGHS basis; `advance.py --resume` | Reported: GCP Spot ladders with memory-aware scheduling and a 30-minute monitor that continues, advances, retries or moves each ladder and restarts from saved state; parallel pre-publication replays with pinned hashes. Public: the README’s rung tables and `scaling_experiment` records; `mixed_proof_pipeline.py` (“sequential stages, at most three CPU workers, never publishes”) | `run_fractional_colgen` with `--deadline-seconds`, `--row-log`, `--freeze`, `--seed-certificate`; `decide_certificate` as the retention gate; the audit tools with `--resume`, per-case receipts and `--replay-plan`; `verify_*_native --resume JOURNAL`; no ladder driver that climbs $L$ unattended | `verify.sh --full`; CI on push; bundles with `SHA256SUMS`, `manifest.json`, `roots.jsonl` | Release manifests, CI (Guzhou), controls scripts; no public search automation |
| Runtime and dependencies | Python 3.10+, NumPy, SciPy, Numba, `highspy`, Matplotlib; Shapely for the geometry test; a C++17 `g++` (`requirements.txt`) | The same for the rectangle ladder; NumPy for the $n = 50$ axis tables; Rust 1.86+ for `zmx2`; Lean 4 for the overlay; `requirements-tested.txt` pins `numpy==2.5.3`, `scipy==1.18.1` | Python 3.14 under `uv --frozen`; NumPy and SciPy (HiGHS through `linprog`); Rust for `sqsearch`, which proposes packings for upper bounds and plays no part in certificates | Rust, Python 3, Lean 4 with Mathlib | Python 3, Node.js (JavaScript checker), C++ (Guzhou kernel) |
| Licence | MIT (`LICENSE`, “Copyright (c) 2026 tokoharu”) | MIT; evand’s MIT retained for the derived $n = 21$ support (`UPSTREAM-LICENSE.txt`) | MIT for code, CC BY 4.0 for documents and records, third-party material excluded (`LICENSE`) | MIT for code; the packings are Ellsworth’s (`README.md`) | Kleddamag MIT (`LICENSING.md`); Guzhou has no repository-wide licence, only Kleddamag’s retained MIT for the reused engine ([R052 packet](../../../packing/resources/web/n17-guzhou-r052-2026-09-25/README.md)) |
| Maintenance state | 14 commits, 2026-09-21 to 23, one author plus wand125’s two merged `push.py` pull requests; no tags, releases or CI; unit tests for geometry, LP updates, search and the driver | 89 commits from 2026-09-15 to 29, 38 of them on the 26th and 19 on the 28th; the fork’s public branches carry nothing beyond upstream’s `push.py` (`git diff 84bebef origin/fix-ladder-driver -- src/push.py` is empty); the research snapshot (411 files, 136 test modules) ships inside the $n = 21$ bundle without a README of its own | Daily; `packing-validate` runs Ruff, BasedPyright and the test tiers on every change | 428 commits by 2026-09-28; CI green on push | Kleddamag: releases with changelog; Guzhou: R068 published without a local run or CI observation ([R068 packet](../../../packing/resources/web/n17-guzhou-r068-2026-09-28/README.md)) |

## 2. Where Each Is Stronger

### F1. Rectangle densities are the productive parametrisation of the one-body covering LP above `n = 17`

Tokoharu’s own comparison at $n = 29$: $5.71$ with 552 expanded rectangles against
wand125’s point certificate at $5.57$ with 748 atoms, a gain of $0.14$ from fewer basis
elements (README “How this differs”); at $n = 26$, $+0.058$. wand125 then carried the
same solver past every point rung this repository holds: $4.695$ against T-030’s $4.679$
at $n = 18$, $4.815$ against $4.80$ at $n = 19$, $4.895$ against $4.85$ at $n = 20$,
$4.9875$ against exp-229’s $4.88$ at $n = 21$, and past Green and Nagamochi at $n = 37$
to $95$. This repository’s own runs show why: at $n = 18$ three site sets of 538 to 618
orbits lock at exactly $18.000000$ at side $4.68$, and at $n = 20$ both constructions
cross twenty at $4.865$ by $2.23$ parts in a hundred thousand (the covering-values table
in [`CERTIFICATE-REACH.md`](../../../packing/frontier/CERTIFICATE-REACH.md)). A point on
a fixed grid is captured or missed outright; a rectangle is captured in proportion to
overlap, so the LP can spend mass continuously near the covering wall.

The limit of this advantage is exact.
[X-027](../../../packing/campaign/explorations/X-027-stromquist-fractional-and-structural-strategy.md)
proves that finite-atom and absolutely continuous covering infima coincide under the
interior-incidence convention, so rectangles are a better search basis for the *same*
theorem, subject to the same covering-value ceiling that
[`ceiling_side_for_net`](../../../packing/src/sqpack/fractional/certificate.py) and
X-014’s packing cap describe.
They cannot pass what threshold atoms pass: T-025’s ceiling family shows no one-body
certificate exists at $n = 11$, side $3.82$, on any net containing its six directions,
and the threshold atoms do.
At $n = 17$ the frontier is Kleddamag’s and Guzhou’s charge certificates, a stronger
relaxation again (rank-1 Chvátal–Gomory cuts, in
[`threshold.py`](../../../packing/src/sqpack/fractional/threshold.py)’s words), and no
rectangle certificate exists there at all.
At the integer endpoints evand’s margin-zero closed covers and mixed segment covers
reach values ($s(21) = 5$, $s(32) = 6$, $s(45) = 7$) that no positive-margin certificate
of any basis can, since every certificate on a finite net sits strictly below
$\lceil\sqrt{n}\rceil$. So the languages nest by strength, not by author: one-body
measures (points, densities, mixed covers) at the bottom, charges above them, and the
endpoint technique to one side.

### F2. Tokoharu’s verifier is small, reviewed three times, and still one method

The proof kernel is 126 lines and has been read line by line on 2026-09-22, again
against sides to $8.955$ on 2026-09-27, and again in the stricter $\Gamma = 1$ setting
on 2026-09-28, with no defect found and bit-identical reproduction across compilers and
architectures. That is more review than any other checker in this comparison has had
here. It remains one implementation of one method: the FTC derivative bound with a
certified inscribed-polygon area.
A modelling error in `slice()` or `area_lower()` would reproduce on every replay, and
there is no exact route to catch it, which is exactly what `C4` exists to rule out
([`epistemics.md`](../../../epistemics.md)). Its surroundings are weaker than its
kernel: `run_verify.py` never checks `mass < n` (DENS-2), `push.py --from` accepts a
certificate for the wrong count (DENS-1, retained controls under
[`density-adversarial-final`](../../../packing/resources/web/external-square-certificates-2026-09-22/receipts/density-adversarial-final/driver-controls/driver-controls.json)),
every acceptance in the Python is an `assert`, and the $n = 50$ copy exits zero on an
unresolved angle (MV-1). The intake wraps all of that and trusts none of the driver’s
outputs, so none of it reaches the register; it does mean the tool cannot be adopted as
a bound decider by itself.

### F3. This repository’s decision stack is broader and method-distinct, and cannot read the two languages that now carry the frontier

For points and thresholds the gate decides every retained rung by an exact sweep and an
interval branch and bound that must agree on the least cell mass
([`decide_certificate`](../../../packing/devtools/decide_certificate.py)); the native
parent-core route has decided three external certificates by a method sharing nothing
with their sources. Nothing else in the field has a second method for its own
certificates except evand’s paired checkers.
The two languages that now hold most of the frontier are the two the native route does
not read: rectangle densities ($n = 18$ to $95$, and $n = 50$ at $\Gamma = 1$) and
winning-subset charges ($n = 17$). The refusals are concrete: R052 is refused at the
frozen 8,192-site ceiling before any box is searched
([R052 review](review-2026-09-25-n17-guzhou-r052.md) F1), and $4.66001$ needs an atom
class that does not exist (BC-393). Every rectangle bound in the register therefore
rests on Tokoharu’s C++ alone, which is `V4/C3` and correct by the admission rule, and
the question this document was asked is whether that should stay so.

### F4. The verification lane is where this repository is ahead, and it is falling behind on volume

`audit_tokoharu_density` and `audit_wand125_rectangles` decide, without importing any
source Python, every exact premise the C++ trusts: interval enclosure of every datum,
the complete axis-event set, orbit mass, `mass < n`, the candidate’s own $n$ and $L$,
and the regenerated input’s digest against the accepting run.
wand125’s pre-publication replay checks byte equality and node counts on a second
machine (README “Checking them”), which is determinism, not direction (MV-4). The
receipts here are what let a bound move into the verified lane.
The cost is that the lane is throughput-bound: three of the 44 standing certificates at
`ad43d29` were replayed ($n = 27$, $31$, $32$), the 09-28 pin raised 32 and added six,
and the plan now lists 47 replays at about 134 CPU-hours.
wand125 made 19 commits on 2026-09-28 alone, most of them new or raised certificates.
Without a queue that runs unattended, the verified lane will trail the reported lane by
weeks, and the register’s distinguishing claim, that “verified means formal”, becomes a
statement about backlog.

### F5. Generation cost is comparable per rung; reach per rung is not

The probe below prices an accepted rung of Tokoharu’s ladder at $n = 12$ in the easy
regime at 72 to 269 s on one core, search and 201-direction certification included; this
repository’s column generator at the same side ran 246 s to its deadline without
converging, because the side sits on a packing bound and its row loop carries no gap
between the row threshold and the oracle, while the record’s converged rungs at $n = 18$
to $20$ cost 320 to 1,616 s. The difference is not speed; it is what a rung buys near
the wall. wand125’s $n = 29$ ladder from Tokoharu’s $5.71$ reached $5.7775$ in 21 rungs,
one of which stalled for six hours until exact rescaling of the incumbent converted it
into a certificate (README “How the 5.74125 rung was obtained”), and the fixed-support
route then carried it in $1/400$ steps.
This repository’s ladders at $n = 18$ to $20$ stop at the covering wall in 320 to 1,616
s per rung and have no rescaling or fixed-support move.
Both of wand125’s moves are elementary and could be added to the point generator, but
they would be added to the weaker basis.

### F6. wand125’s tool list is mostly unpublished, and two items are already built here

Of the seven groups in the X message, the public trees support: exact rescaling and
inheritance by mass (every candidate’s `scaling_experiment`; the README’s inheritance
tables; `monotone_bounds` in
[`audit_wand125_rectangles.py`](../../../packing/devtools/audit_wand125_rectangles.py)
does the same here), the Lean overlay (`point_n21_L5/lean`), the pre-publication replays
with pinned hashes, the ladder driver (upstream `push.py`), and the ceiling
`L < B · UB(n)`, which is X-014’s argument and is computed here for every case with a
tilt inventory as `packing_side_cap` in
[`render_certificate_reach.py`](../../../packing/devtools/render_certificate_reach.py).
The shipped `nagamochi_research` snapshot holds a 35-line `working_measure_lp.py`, a
`fixed_angle_geometry_cache.py` and `inherit_monotone_cover_roots.py`, all on the point
and mixed side. The rectangle-engine improvements (parallel screening, batches of 16,
warm start, the working LP for long continuations, the axis cache, edge-rectangle budget
recovery), the lazy `zmx2` variant, the Spot-instance ladders and the monitor are not in
any public tree: the fork’s branches diff empty against upstream’s `push.py`, and the
package `rectangle_budget_optimization` that four shipped modules import has zero files
in the 2,295-file manifest.
Those items are reported, and their measured speed-ups (3 to 4×, 40 to 50 %) are the
source’s figures.

### F7. The `n = 50` route is a certificate-language departure with no independent decider

`mixed_n50_L740` is Tokoharu’s language at $\Gamma = 1$ with per-node centre domains,
decided by a modified copy of the checker that ships in the bundle.
The [n = 50 review](review-2026-09-28-wand125-n50-mixed-verifier.md) found the argument
sound and the copy no looser than the original, but the $10001/10000$ margin that
insured the standard family against an undetected over-estimate below $10^{-4}$ is gone,
and the only control run so far is that review’s 72-box one-sided probe.
This is the certificate where a method-distinct decision would be worth the most, and it
is exactly the language the native route cannot read.

### F8. Automation: one public ladder driver, and everything unattended is elsewhere

`push.py` is the only public ladder driver in the field, and it is good at the thing a
ladder needs: each accepted rung is a self-contained certificate directory, so a killed
run keeps what it proved.
Its admission defect matters only on `--from`. Neither upstream nor the fork has CI;
wand125’s unattended machinery (Spot instances, the 30-minute monitor, memory-aware
scheduling) is reported.
This repository’s drivers stop on deadlines and log per round, and every audit tool
resumes, but nothing climbs $L$ unattended, and BC-394 and BC-395, the two ladders the
plan queued for 2026-09-27, have not run ([ledger](../../../packing/campaign/ledger.md)
rows `BC-394`, `BC-395`: `ready`).

## Probe

One question could not be settled by reading: what a rung of Tokoharu’s pipeline costs
on one core, search and certification together, against this repository’s generator at
the same count and side.
Both runs used a scratch copy of the pinned trees under the session scratchpad, a Python
3.12 environment with NumPy 2.5.3, SciPy 1.18.1, Numba 0.67.0 and `highspy` 1.15.1
(upstream pins `>=`, not exact versions), `g++` 13.3.0, and `taskset` to one core with
every thread pool set to one.

### The ladder from the trivial seed

From the scratch copy of `84bebef`, with `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`,
`MKL_NUM_THREADS` and `NUMBA_NUM_THREADS` all $1$:

```bash
taskset -c 3 timeout 590 ../venv312/bin/python src/push.py \
  --n 12 --target 3.6 --step 1/20 --workers 1 --out probe/n12
```

| Step | Side $L$ | Search (`engine.py`) | Certify, 201 directions | Verifier nodes | Positive rectangles of basis | Mass | Rung wall |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| seed | $\frac{2113}{625} = 3.3808$ | about 19 s | 28.3 s | 480,459 | 5 of 37 | 10.371 | 47.9 s |
| rung 1 | $\frac{8577}{2500} = 3.4308$ | 27.9 s | 40.1 s | 1,423,401 | 6 of 73 | 9.009 | 72.5 s |
| rung 2 | $\frac{4351}{1250} = 3.4808$ | 68.1 s | 75.0 s | 1,738,257 | 10 of 109 | 9.0097 | 147.3 s |
| attempt | $3.5308$ | `ENGINE_FAILED` after 12.1 s: `HiGHS call failed: HighsStatus.kError` | — | — | — | — | 16.2 s |
| attempt | $3.5058$, step halved to $\frac{1}{40}$ | the same error after 11.9 s | — | — | — | — | 15.6 s |
| rung 3 | $\frac{34933}{10000} = 3.4933$, step $\frac{1}{80}$ | 122.2 s | 141.6 s | 2,136,014 | 9 of 145 | 9.009 | 269.4 s |
| — | $3.5058$ again | killed by the 590 s cap (exit 124) |  |  |  |  |  |

Three readings. The cost of an accepted rung on one core is 72 to 269 s and rises with
the basis: the verifier is 55 to 60 % of each rung and runs at about 15,000 nodes per
second here, so a wand125-size certificate of 30 million nodes is about 35 CPU-minutes
to certify once found, which agrees with the upstream per-angle sums.
The mass sits at $9.009 = 1.001 \times 9$ on every rung: nine disjoint $B$-squares fit
once $L > 3B = 2.9931$, so the LP sits on that packing bound and these rungs say nothing
about $n = 12$; the informative region begins above T-017’s $3.96$, as the plan already
noted, and the cost there is unmeasured.
Two of the five attempts failed inside HiGHS with `kError` after twelve seconds each;
the driver reads that as a failed rung and halves its step, so a solver-call failure
under `highspy` 1.15.1, a version upstream’s `>=1.10` pin admits but never names, cost
28 s and three quarters of a rung’s width.
The `--from` path with its DENS-1 defect was not exercised.

### This repository’s generator at the same side

From `packing/`, with the project interpreter, at the ladder’s first accepted side and
the driver’s defaults (grids `auto`, 181 directions, $B = 9977/10000$, scale 200,000,
support cap 32):

```bash
taskset -c 3 timeout 400 .venv/bin/python3 -m devtools.run_fractional_colgen \
  --n 12 --side 8577/2500 --column-rounds 2 --max-rounds 40 --deadline-seconds 240 \
  --freeze candidate.json --json run.json --row-log rows.jsonl
```

It stopped at its deadline after 246 s, 13 row rounds and two column rounds, with 9,547
rows held, the objective at $8.999999999999975$ from the first round on, the least
covered placement at $0.9456$, and nothing frozen, so `decide_certificate` had nothing
to decide. The reason is the same packing bound: any covering has mass at least 9 here,
the row loop asks every placement to reach mass 1 with no gap to its oracle
(`colgen.py`, $b_{ub} = -1$, violated below `1 − tolerance`), so it can only converge on
a tight covering, and it kept finding placements at $0.95$. Tokoharu’s LP asks for
$1.001$ on its rows and screens at $1.0005$; that gap is what turns $9$ into $9.009$ and
converges in 28 s. The record shows the same lock at $n = 18$, side $4.68$, where three
site sets hold $18.000000$ through their stops.
So the probe settles the cost of a certified rectangle rung and shows one design
difference, and it does not give a converged timing for the point generator at a
non-degenerate side; for that the record’s own rows stand (320 to 650 s at $n = 18$,
1,616 s at $n = 20$), which are of the same order as the ladder’s rung cost measured
here.

## 3. Options for the Path Forward

The replay question runs through every option, so it is taken first.
At the 09-28 pin 47 standing certificates would raise a verified bound, about 134
CPU-hours by upstream per-angle times, and each certificate’s axis direction is one
process of up to 6,114 s (WSC-2), so wall per certificate is bounded below by that
however many workers it gets.
The record’s host has about ten workers; this container has four cores and 15 GB. At
nine workers the set is about 15 wall-hours if every direction ran in parallel; three
certificates concurrently at `--workers 3` each, with the axis direction serial inside
each, makes it about two nights on the host, and three four-core cloud sessions in
parallel finish in about the same two nights.
Every option below assumes that queue exists, because without it no rectangle bound
enters the verified lane whoever generated it.

### (a) Adopt Tokoharu’s solver as a pinned external dependency behind the preflight and an unmodified replay

**What it buys.** First-party rungs in the rectangle language at counts nobody else is
working, at 72 to 269 s per rung in the easy regime (probe) and unknown near the wall;
the $n = 12$ question (BC-395) that no other route can now ask; ladders at the top of
the prize table ($n = 103$ and $105$, $+0.54$ each in `CERTIFICATE-REACH.md`). **Cost.**
A scratch environment and clone at `84bebef` (an hour; done today in the scratchpad),
`audit_tokoharu_density` generalised from its three pinned cases to any certificate
directory (the plan prices this at one to two hours), and CPU per rung.
Not vendoring into `sqpack`: the tree is already retained byte for byte in the September
22 packet with archive binding, and the pin is the dependency.
**Risk.** Dependency drift: the probe’s HiGHS `kError` at `highspy` 1.15.1 shows the
solver call can fail under a version upstream never ran, and the driver’s halving then
spends rungs on a non-mathematical failure; pin the four packages to versions that
complete a ladder and record them.
DENS-1 is avoided by never using `--from`, or closed by (e). Duplication: wand125 has
announced $n = 65$ and $n = 82$ as next targets, so BC-394’s $n = 82$ ladder would race
a faster, better-provisioned run of the same solver.

### (b) Port rectangle densities, and the winning-subset atom, into the native interval route

**What it buys.** A method-distinct decision (`C4`) for every rectangle certificate,
including the $\Gamma = 1$ family at $n = 50$, and for Kleddamag’s and Guzhou’s $n = 17$
charges. `C4` is not an admission prerequisite, so this moves no bound; it is the
assurance the register cannot otherwise claim for the 50 counts that now rest on one C++
file. **Estimate.** The atom is a *sure-core* bound: for a box of centres at a net angle
the intersection of all cores is a concentric rotated rectangle with half-widths
$B/2 - (d_x|c| + d_y|s|)$ and $B/2 - (d_x|s| + d_y|c|)$, and the mass surely captured is
`Σ ρ_j · area(R_j ∩ sure core)`, a convex clipping of an axis-aligned rectangle against
a rotated one, evaluated with directed rounding; a monotone lower bound that never
computes a derivative, so it shares no step with `verify.cpp`. It loses linearly in the
box radius, as the FTC bound does, so node counts should be of Tokoharu’s order (5.6 M
at $n = 11$, 5.8 M to 45 M for wand125’s). The reader is the preflight’s existing exact
parser; the premises (`mass < n`, D4 expansion, net reach, $B(1 + D) < 1$) are already
decided there. Build: 700 to 1,000 lines on the pattern of
[`parent_core_interval.py`](../../../packing/src/sqpack/fractional/parent_core_interval.py)
with tests, three to five agent-days, plus a Fable review of the sure-core lemma and the
axis direction, where the bilinear-cell argument allows an exact rational check at
vertices instead. CPU: the point engine runs about 11,000 boxes per second per worker
(136 M boxes in 6,197 s on two workers); rectangle clipping over hundreds of images per
box is heavier, so a Tokoharu-size certificate is one to ten CPU-hours and a
wand125-size one ten to fifty in NumPy, which is why the plan pilots on `cert_n11_L381`
before committing to the 50. A compiled kernel, for which `sqsearch` is the toolchain
precedent, would cut that by an order of magnitude at one to two more weeks.
The winning-subset atom is BC-393’s scope (three to four hours build, one hour review, 2
to 12 CPU-hours) and is independent of the rectangle atom.
**Risk.** The port is worth nothing if the sure-core bound needs far more boxes than the
derivative bound near thin, dense rectangles (densities here reach $1.4 \times 10^{5}$
and sides $3.2 \times 10^{-4}$); the pilot decides that before the 50 are queued.

### (c) Build a native density generator

**What it buys.** Independence from an external solver for generation, and one codebase
for search and decision.
**Cost.** Two to four weeks to reach parity with a 2,346-line engine that exists, is
MIT, has been run at 50 counts, and is being improved by its users faster than this
repository could follow; no bound that (a) would not reach with the same CPU. **Risk.**
Duplication for its own sake; the covering-value ceiling caps the prize regardless of
who writes the LP. Not warranted now.
The one generator gap worth closing here is three elementary moves in the point and
threshold generator, because those are the bases with no external solver: wand125’s
exact rescaling and fixed-support re-solves, and Tokoharu’s gap between the LP row
threshold and the screening target, which the probe shows deciding whether a rung
converges at all on a packing-bound side.

### (d) Leave generation to the community and specialise in independent verification, replay at scale, and the register

**What it buys.** The thing the field otherwise lacks: an exact preflight, a
method-distinct decision, provenance binding and a register whose verified lane means
what it says. Every external result of the last week arrived with its own checker and
none with a second method; wand125’s README already points readers here as “the stronger
check”. **Cost.** The replay queue (above) and a hosted runner; the build in (b) for the
two unread languages; the reviews, which are the expensive part and already run at one
Fable max reading per new argument.
**Risk.** The verified lane lags when replay lags (F4); and a verification-only
repository stops learning what a search can and cannot reach, which is the knowledge
X-014 and the covering-values table encode.
The remedy is (a) in the gaps rather than instead of (d).

### (e) Contribute upstream

**What it buys.** A canonical checker that gains what the reviews found, instead of a
fork: the DENS-1 guard (factor `advance.py`’s `load_incumbent` into `push.py --from`;
`think-c0xc`), a `mass < n` and identity check in `run_verify.py` or a `preflight.py`
(DENS-2), and a partition of the axis direction into vertex ranges (WSC-2), which cuts
the wall per certificate by nearly the worker count and is a checker revision that
should happen upstream so every published certificate is checked by the same file.
The ceiling wand125 lists is already known to both sides and needs no transfer; the
tilt-inventory refinement of it could be offered as a note.
The replay receipts and the preflight tool are worth offering as the second machine
wand125’s publication step already uses.
**Cost.** One to two days; the pull requests are small and upstream has merged two from
wand125 in two days.
**Risk.** None to the record; an unmerged pull request changes nothing here.

## 4. Recommendation and Ranked Plan

Adopt (d) as the lane, (a) in the gaps, (b) as the one build, (e) alongside; not (c).
The selected next entry is the replay queue.

1. **Replay queue for the 47 pending rectangle certificates.** *Entry:* the 09-28
   packet’s preflight receipt, all 50 `PASS` (exists).
   *Instrument:*
   `audit_wand125_rectangles --packet 2026-09-28 --replay --resume --workers 3` in
   `apply_wand125_rectangles --replay-plan` order (largest rise first), three
   certificates concurrently, then `apply_wand125_rectangles` per batch; each batch
   committed with its receipts.
   *Exit:* every certificate on the plan replayed with `PASS`, or a named failure with
   its case held in the reported lane.
   *Budget:* about 134 CPU-hours, two nights on the record host or on three cloud
   sessions in parallel; a wall ceiling of 24 hours per certificate (the tool’s
   default), and a stop if any replay fails, which is a review item before anything else
   runs.
2. **BC-395 first, BC-394 retargeted.** *Entry:* the pinned clone at `84bebef` in a
   scratch environment with the four packages pinned to versions that complete a ladder
   (today’s `highspy` 1.15.1 threw `kError` at one rung), and `audit_tokoharu_density`
   generalised to any certificate directory.
   *Instrument:* `push.py` from the trivial seed, never `--from`; admission only by
   preflight plus unmodified `run_verify.py` replay.
   *Exit:* at $n = 12$, a rung above $3.968616$ replayed, or the driver giving up below
   $3.9687$ (as BC-395 states); for BC-394, retarget from $n = 82$ and $50$ to counts
   wand125 has not announced, $n = 103$ and $105$ at the top of the prize table, or hold
   until their $65$ and $82$ land.
   *Budget:* one worker per ladder, one night each, at most 12 CPU-hours per ladder,
   first-rung cost read from the log before the second is allowed to start.
3. **A rectangle-density atom in the native route, piloted before it is committed.**
   *Entry:* the first replay batch landed (so the atom has certificates to decide) and a
   Fable review of the sure-core bound and the axis-direction argument.
   *Instrument:* a `devtools.verify_rectangle_density_native` on the pattern of
   `verify_evand_angle_net_native`, reading Tokoharu’s `certified_candidate.json`
   through the preflight’s parser.
   *Exit:* `cert_n11_L381` decided at all 201 directions with the per-certificate CPU
   cost measured, then the decision whether the 50 are affordable in NumPy or need a
   compiled kernel. *Budget:* three to five agent-days of build, one Fable review, at
   most 10 CPU-hours for the pilot.
   BC-393’s winning-subset atom stays as planned beside it.

Alongside, at one to two days: the three upstream pull requests of (e), and the three
elementary generator moves of (c) in the point and threshold generator.

**What would change the recommendation.**

- wand125 publishes the rectangle-engine improvements and the Spot ladder under MIT: run
  ladders from the fork instead of upstream, and drop (c)’s generator moves entirely.
- A defect is found in `verify.cpp` or its $\Gamma = 1$ copy: (b) becomes urgent and the
  affected replays are re-run; every rectangle bound in the register rests on that file.
- wand125’s $n = 65$ and $82$ land before BC-394 starts: the ladder prize there is gone
  and commitment 2 is $n = 12$ alone plus the counts above 100.
- evand’s mixed covers extend to positive-margin sides (segments plus points at general
  $L$), or the $n = 50$ mixed pipeline generalises: the segment atom, not the rectangle
  atom, becomes the port worth making, since a language that reaches endpoints and
  interior sides both would supersede the rectangle basis.
- The replay backlog cannot be cleared in about two weeks on the available hosts: a
  hosted replay farm becomes the first commitment and (b) waits.
- Upstream goes quiet for a month or changes the checker’s semantics: vendor the tree at
  `84bebef` behind the archive binding that already exists, which is a policy change,
  not a build.

## Claims by Evidential Status

- **Proved here in exact arithmetic or by reading the code:** every cell of the matrix
  that names a file; the emptiness of the fork’s public diff; the absence of the
  `rectangle_budget_optimization` package from the 2,295-file manifest; the nesting of
  the languages by X-027 and T-025’s ceiling family.
- **Computationally measured:** the two probes above, on one core, with their commands
  and outputs; the replay costs cited from receipts.
- **Reported by the sources, not verified here:** wand125’s speed-up figures and
  unattended infrastructure; wand125’s search times at $n = 29$; upstream wall times
  where no replay here exists; Guzhou’s C++ kernel timing (from the plan’s probe).
- **Estimated:** the build and CPU costs of option (b), which the pilot in commitment 3
  exists to replace with a measurement.

## Update, 2026-09-29

The first part of wand125’s tools became public the day after this comparison, at
[wand125/square-packing-tools](https://github.com/wand125/square-packing-tools) (MIT,
first commit `325f32ff`): the transfer and ladder drivers, the `B · UB(n)` ceiling,
rescaling, the working-row LP with basis reuse, batched and angle-parallel
counterexample screening, a search-only cached-axis verifier and a faster `zmx2` patch
for point certificates.
The matrix’s cells that call those capabilities unpublished describe the state on
2026-09-28 and are superseded; `think-664t` re-evaluates them from the released code.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
