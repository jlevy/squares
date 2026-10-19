# 06 — The capped compute plan

*Written 2026-09-10 (A195) against `docs/budget.md` §A.0 as regenerated in commit `5b3c68a0`. **Every dollar
figure on this page is an ASSUMPTION, not a provider quote**, and each carries the rate it was computed at. The
compute quantities are the repo's own measurements; the money is a model laid over them.*

## 1. Units, and the hardware normalisation

The repo's measurements are in **desktop worker-hours** on an i7-12700K (6 usable LP slots, BLAS pinned). A
cloud vCPU is not one of those. Two facts set the conversion, and both are measured, not assumed:

* **[M] RAM per LP.** The current runners impose a **6,144 MB commit gate per LP process**. A 16-vCPU instance
  in the 64 GB class therefore supports about **10 concurrent LP slots, not 16**. Memory-optimised instances
  (128 GB) restore all 16 at a higher hourly rate; the plan below assumes the cheaper, memory-gated shape.
* **[M] The LP is single-threaded** HiGHS plus numpy row oracles, so one LP = one vCPU (A191's convention).

| quantity | value | basis |
|---|---|---|
| **A1** — on-demand 16-vCPU instance | **≈ $0.70 / instance-hour** | **ASSUMPTION.** An order-of-magnitude on-demand figure for a 16-vCPU / 64 GB general-purpose instance. Not a quote; CPU, memory, disk and network are billed separately by real providers |
| **A2** — usable LP slots per instance | **10 of 16** | the 6,144 MB commit gate against 64 GB [M] |
| **A3** — vCPU-hours per desktop worker-hour | **2.0** | **ASSUMPTION.** A vCPU is a hyperthread on a slower, memory-bandwidth-shared part; the repo's CPU-h are physical-core hours |
| **⇒ effective rate** | **$0.14 per desktop worker-hour** (= per repo CPU-h) | $0.70 ÷ (10 ÷ 2.0) = $0.70 ÷ 5 |
| sensitivity band | **$0.10 low / $0.14 central / $0.28 at 2×** | the review's own §3 band is $0.10–$0.20; the 2× column is the plan's stress case |

One instance-hour therefore delivers **5 repo CPU-h** of LP work under the memory gate. Both figures appear
below: "instance-h at 16 vCPU" is the naive division the brief asked for; "effective instance-h" is the one to
pay against.

## 2. Reconciled components

From `docs/budget.md` §A.0. The components sum by construction; the OVERHEAD row is an estimate and is labelled.

| component | CPU-h (central) | instance-h at 16 vCPU | effective instance-h | $ at $0.14 | $ at $0.28 (2×) |
|---|---:|---:|---:|---:|---:|
| A57 window trees (k5_11 + k5_16) | 1,800 | 113 | 360 | $252 | $504 |
| Window stragglers | 0 | 0 | 0 | $0 | $0 |
| Protected tier: trump5 residual + 14 image-bearing classes | 3,800 | 238 | 760 | $532 | $1,064 |
| corners4 = k4_13 | **not priced** — [O] theory-limited (pair row) | — | — | — | — |
| k4_05 | **not priced** — [O] theory-limited (NoFam in window rows) | — | — | — | — |
| k0_00, theorem route | **0 — CONDITIONAL** on obtaining a theorem | — | — | — | — |
| **Search subtotal** | **5,600** | 350 | 1,120 | $784 | $1,568 |
| **OVERHEAD (+25 %) — ESTIMATE** | 1,400 | 88 | 280 | $196 | $392 |
| **TOTAL, theorem route** | **≈ 7,000** | **438** | **1,400** | **≈ $980** | **≈ $1,960** |
| range (low 4,700 – high 13,200) | | 294–825 | 940–2,640 | $658–$1,848 | $1,316–$3,696 |

### The k0 cascade route, by the one unmeasured input

| k0 deep kill rate at S4+ | total CPU-h | effective instance-h | $ at $0.14 | $ at $0.28 | within the $7,500 ceiling? |
|---|---:|---:|---:|---:|---|
| **1.00** (the S3 layer closes each cell) | ≈ 25,900 | 5,180 | **$3,626** | $7,252 | yes at the central rate; at the line at 2× |
| **0.99** | ≈ 65,400 | 13,080 | **$9,156** | $18,312 | **no** |
| **0.95** — the S3 sample's own measured rate, carried down | ≈ 4.95 × 10⁶ | 990,000 | **$693,000** | $1.39 M | **no, by two orders of magnitude** |

**This table is the whole argument for the pilot.** The scenario with an empirical basis is the one that is not
purchasable; the purchasable scenarios assume the search closes faster below S3 than it did at S3. Nothing in the
repo decides between them, and one shard of S4 work would.

## 3. The calibration pilot — capped at $300–$500

**Runs on the CORRECTED verifier only**: v5 at sha `f93958cca421` (post-fix commits `f590c4db`, `12f8b9c6`), the
frozen v1 at `521cb01fe656`, with `attempts/A190-guardline-clause/tests/repro_v5_false_kill.json` in the
regression suite and expected to FAIL the checker. Any pilot output produced by a pre-fix verifier is discarded.

At $0.14 per worker-hour a $300–$500 cap buys **2,140–3,570 CPU-h** (430–715 instance-h). A *smoke test* of the
four lanes costs about **200 CPU-h ≈ $28**; the cap is deliberately larger, because what the pilot is for is
statistical power on the S4 kill rate, not a demonstration that the pipeline runs.

| lane | share | CPU-h | what it buys | what it must report |
|---|---:|---:|---|---|
| **Ordinary A57 work** | 40 % | 860–1,430 | includes the budget's own named top lever: draining ~300 level-2 LP jobs (**24 CPU-h**) collapses a factor-2.4 spread in an 1,800 CPU-h row by measuring `D_2` | throughput per instance-hour, peak RSS per LP against the 6,144 MB gate, measured `D_2`, kill rate by level and by prior verdict |
| **One protected hard case** | 15 % | 320–535 | one trump5 residual / P-TREE cover node **end to end**, chosen for difficulty, not convenience | whether A100's η law holds off its two pilot classes; cost per closure against the 3,800 CPU-h row |
| **One k0 S3 shard, then S4** | 35 % | 750–1,250 | `l1_104`'s **entire S3 layer is 5,432 nodes = 360.5 CPU-h**. This lane completes it and spends the remainder on **S4 — the first measurement below S3 that exists** | the S4 kill rate and fan-out. This single number moves the k0 line between $3,626 and $693,000 |
| **One complete certificate replay** | 10 % | 210–355 | S02T (1.9 CPU-h), S33T (1.06), `Measure382` (0.67), the frozen-v1 corpus replay, **and one concrete tree-file → `cover`/`ClosedTree` check** | replay wall-time per certificate; whether an emitted tree actually covers its parent (the review's joint-first item) |

**Replay allowance (standing, not only in the pilot).** 10 % of any allocation is reserved for Lean replay, the
adversarial v5 regression, and re-verification of the frozen corpus after any verifier change. It is inside the
OVERHEAD row of §2, not additional to it.

## 4. Stop conditions

Each is a hard stop, not a review trigger.

1. **Soundness.** Any certificate that fails replay, or any new false-PASS regression, stops **all** lanes until
   the checker is fixed and the corpus is re-replayed. (This condition has already fired once — it is what the
   external review's P0 finding produced.)
2. **The k0 S4 rate.** If the measured S4 kill rate is **below 0.99**, the k0 cascade lane stops. Below that the
   eleven-cell price leaves the ceiling by more than 10×, and the correct next move is theory, not compute.
3. **Frontier growth.** If a lane's outstanding-work count grows rather than shrinks over a full allocation, stop.
   Precedent: A159's `l1_158` went 15 → 349 open pieces from depth 9 to depth 15.
4. **2× overrun.** Any lane that reaches twice its priced central without a measured reason stops.
5. **The ceiling.** Hard stop at **$7,500** total, regardless of progress.

## 5. The ceiling

**≈ $7,500 (ASSUMPTION, at the $0.14 central rate; ≈ 53,500 CPU-h).** What it does and does not cover:

* **Covers** the theorem route (≈ $980) with roughly seven times headroom, at the 2× rate too.
* **Covers** the optimistic k0 cascade scenario ($3,626 central); at the 2× rate that scenario lands at $7,252,
  i.e. on the line with no headroom.
* **Does not cover** the 0.99 k0 scenario ($9,156) and is nowhere near the 0.95 one.

So the ceiling is not a completion budget. It is a budget for *finding out which world we are in*, plus the
theorem-route work that is priced today.

## 6. API credits — stated separately

The dollar figures above are **raw compute only**. The model/agent spend that writes the clauses, emits and
re-emits certificates, reads the galleries and drives the cascade is a **separate line item**, is not convertible
into CPU-h, and is not priced on this page. A191's own note records the campaign waiting on API credits. Any
request should name the two separately and never net one against the other.

## 7. Exit criteria — the bar for "only compute remains"

The review sets a higher bar than "the search is priced", and this plan adopts it verbatim. **None of the
following is satisfied today**, and until all are, the honest claim is "certified results plus a priced,
partially-calibrated campaign", not "only compute remains".

| # | criterion | today |
|---|---|---|
| E1 | a sound **fixed** certificate chain: the v5 fix landed, the adversarial regression in CI, the corpus replayed | fix landed (`f590c4db`, `12f8b9c6`), all six v5 kills replay PASS, four certificates relabelled to the frozen v1. **Regression not yet in CI**; T3 still enshrines the old inequality direction |
| E2 | all non-computational proof/transfer obligations **discharged or separately committed** | **open**: `stratum_kill`, `trump_residual`, `a22_exact_structure`; K0-O1 (every cascade kill is conditional on it); the pair row for corners4; NoFam-in-window-rows for k4_05; the guard-line checker-half bridge; Sideband Theorem B |
| E3 | an **exhaustive** outstanding-work manifest — immutable identity and parent, exact hypothesis/window, verifier version, result class, next permitted operation, measured time and memory, remaining covering obligation; deduplicated by **(tree, node id)**, never by page name | **not built.** The A57 frontier is counted id by id (1,817 owing) but not in this schema, and the galleries are a 3.8 % review sample, not a manifest. A149 found 19 open G1 nodes masked by a same-id L1 row — exactly the deduplication failure this criterion names |
| E4 | **independently checked tree composition** on one complete example | **not done.** The generic theorem exists; no emitted tree file has been checked to cover its parent. In the pilot's replay lane |
| E5 | a workload estimate **calibrated on representative complete branches** | **not done.** No k0 cell is closed; no A57 branch is closed to depth. This is what lanes 1 and 3 of the pilot buy |

**"Estimated closure" is estimated.** At five desktop workers the theorem route is an **estimated** ≈ 58
wall-days of compute; that is a forecast from measured per-node costs and kill rates with an assumed tail
(`docs/budget.md` §A.0, "two forecasts that must be read as forecasts"), and it is not a date, a guarantee, or a
statement that the proof completes at the end of it.

## 8. The request this plan supports

Technical review of the certified results and of the workflow, plus discussion of a **capped** completion
campaign: the **$300–$500 pilot first**, on the corrected verifier, reporting throughput, memory, exact closed
work, remaining fan-out and every timeout; then a revised allocation **against the refreshed manifest and cost
model**, inside the $7,500 ceiling. Success of a single selected k0 cell is **not** the gate — the gate is E1–E5
above plus the measured S4 rate.

*See `05_status_sheet.md` for what is proved, checked and open; `docs/budget.md` §A.0 for the arithmetic these
dollars are laid over.*
