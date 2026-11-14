# Stage 4 Review Packet: Khalili and Gharabaghi’s `s(k² − 5) = k`, Issue #973

This packet holds the programs, frozen inputs and small outputs of the stage 4
mathematical review lane L144 for issue
[#973](https://github.com/jlevy/squares/issues/973) (bead `think-h10k`). The review
itself is
[review-2026-11-14-khalili-gharabaghi-k2m5-973.md](../../../../docs/project/reviews/review-2026-11-14-khalili-gharabaghi-k2m5-973.md).

The source is [moh63-dev/k2m5-family](https://github.com/moh63-dev/k2m5-family) at
`2c0b1b9979bcb67d92eb215366dc5ee19286c1d8` (tag v1.0, committed
2026-11-13T15:50:51−08:00, MIT licence for code, CC BY 4.0 for text and data).
The checkers are Evan Daniel’s evand/square-packing at
`659ee62e4a9d39542a1146e8b011cc3ab6407ede`. Neither is retained here: the import lane
retains the source. This packet keeps only what this lane wrote and what its runs
printed, in small form.

## Plan and Freeze

- [`PLAN.md`](PLAN.md) is the pre-stated plan, frozen by
  [`receipts/plan.sha256`](receipts/plan.sha256) before any sample or control ran.
- [`receipts/freeze.sha256`](receipts/freeze.sha256) lists the SHA-256 of every program
  and output, written before the lane read the record’s own material on the claim (step
  5 of the brief).

## Programs

All Python ran under the project interpreter (CPython 3.14.7) with `-I`, from
`packing/`, as `.venv/bin/python3 -I programs/NAME.py ...`, at `nice -n 19`.
“Clean-room” means written here from the paper’s statements, importing no code of the
source or of evand/square-packing.
“Driver” means it runs the source’s own code.

| Program | Kind | What it does |
| --- | --- | --- |
| `k2m5_cover.py` | clean-room | Reads the board; exact total and D; D4 invariance as a measure; builds `mu_k` from the family file by Definition 3 for k = 10 to 40; board = built `mu_11`; totals k² − 4D; the premises of Lemma 7’s proof; Lemma 7’s window identity for k = 10, 12, 13, 14, 20, 25, with a planted one-weight mutation as its own control |
| `k2m5_axis.py` | clean-room | The θ = 0 face exactly: every one-sided corner limit of every 1/10 cell of [1/2, 21/2]², no symmetry used |
| `k2m5_exact.py` | clean-room | Exact `mu(P)` of a rational pose: segments clipped in `Fraction`s (a binary64 pre-test with margin 10⁻⁹ only skips segments wholly in or out), Lebesgue part by exact polygon clipping |
| `k2m5_samples.py` | clean-room | Evaluates the pre-stated pose samples S1 to S5 and confirms control M-1 |
| `k2m5_coverage.py` | clean-room | The coverage step: every leftover box against the Tight-Tile Lemma’s domain as the paper states it, the needed job list, and every needed job’s charts |
| `draw_samples.py` | clean-room | Draws every pre-stated sample from one `random.Random(973)` stream |
| `make_mutants.py`, `mutate_cov.py`, `m3_search.py` | clean-room | Mutant covers and dumps for the controls; `m3_search.py` finds the first-order-only mutant M-3 by exact evaluation |
| `submeasure.py`, `boards_vs_family.py`, `lean_data_link.py` | clean-room | The cropped 9632 cover is a sub-measure of the board; the source’s built boards equal the family build; the Lean data is the board verbatim, with no kernel-escape token |
| `compare_uncert.py` | clean-room | Compares two `zmx2` outputs: census, header and the exact set of uncertified boxes |
| `zmx2_leaf_probe.py` | clean-room | Exact `mu` against `zmx2`’s certified bound in its tightest certified leaves |
| `tt_region.py` | driver and oracle | Runs the source’s `ttbox.run` on one chart and face region; wraps `ttbox.analyse` to record each certified cell’s vertices and bound T, maps each vertex to a pose by this file’s own chart formulas, and requires exact `mu(P) − 1 ≥ T` |
| `run_jobs.sh` | driver | Runs a job list one or two at a time under `nice -n 19` with a wall cap, recording real, user and system time |

## Departures From the Plan

- **The queue’s first start.** `zmx2` jobs first started two at a time; the host was
  shared with another lane’s runs, so the queue was stopped after three `cert0` jobs and
  restarted one at a time.
  The two runs in flight were discarded and run again from the start.
- **Z-F’s draw.** It uses a fresh `random.Random(973)`, since its leaves exist only
  after the runs. Two additions were made before it ran: the 300 leaves of least bound,
  and for leaves whose `u` range starts at 0, the four centre corners at `u = u₁·2⁻²⁰`
  and `u₁·2⁻⁴⁰`.
- **M-4’s box.** The pre-stated box, the first box of the first dump, lies in one of the
  five ranges certified at `u₀ = 1/2000`. There `u₁ = 1/4000 + 2⁻⁴⁰` is genuinely
  covered, and both checkers accepted it, correctly.
  The control was run again on the first box, in file order, that lies outside those
  ranges (`mutate_cov.py`); both checkers refused it.
- **A5’s regions.** The `d₀ = 7/2` region is the `W` charts of `d3.5 σ=+1 line 4.4`, the
  cheapest `d₀ = 7/2` line job whose tile meets the Lebesgue square.
  The corner and ray zones were replayed exactly (T-B) but not passed through the
  oracle.
- **S1’s tilt.** θ was drawn uniformly and `u = tan(θ/2)` rationalised to denominator
  10⁶.
- **Additions.**
  - `boards_vs_family.py`, `submeasure.py` and `lean_data_link.py`, and a check that the
    source’s ×0.999 window cover is `c9632.txt` with every weight scaled and floored;
  - the source’s fast checks under the project interpreter;
  - the authors’ `qx2` ×0.999 control, which the plan allowed if budget remained.

## Outputs

`outputs/` holds the JSON and text the programs printed, and the small receipts of the
replays (headers, census lines, per-chart lines).
Bulk files are not kept: the `zmx2` box dumps of the replayed roots are summarised by
their census and by the digest of their sorted box lists.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
