# contpose_check3 — second, independent continuous-pose checker (spec for Codex)

Written 2026-10-11. Work only inside this folder (`contpose_check3/`).

## Goal

Build a second, independent checker for "continuous-pose" rectangle-density certificates, using the
MIT-licensed kernel of Guzhou0806/n40-square-packing (commit 71c97d0, copied unchanged in `upstream/`)
as its core. It must accept two input formats and print a machine-readable receipt.

The claim being checked: let μ be the certificate's measure on K = [0, L]². For a core side B and a
threshold τ, every closed square P of side B with P ⊆ K, at **any** centre and **any** angle, has
μ(P) ≥ τ. If additionally n·τ > M (M = total mass, checked exactly with rationals), then n unit
squares do not fit in a square of side L/B, i.e. s(n) > L/B. Read `upstream/PROOF.md` §2–9 for the
method (t = tan(θ/2) slabs, (u, v, t) branch and bound, concave-section trapezoid lower bound,
translation derivative bound, near-horizontal axis patch with the integer grid).

## Independence rule (important)

Do NOT open, read or copy anything outside `contpose_check3/`. In particular do not read
`../contpose_check2/` (another team member's implementation of the same idea) or any `sqverify_fast`
source. Everything you need is in `upstream/`, `inputs/` and this spec.

## Inputs

1. **Guzhou n40 format** — `upstream/certificate/certified_candidate.json` with
   `upstream/certificate/parameters.json`. Handle it exactly the way `upstream/verifier/exact.py` does
   (rectangles + weights, D4 expansion, outward rounding). This is the regression case.

2. **Mixed rectangle format** (ours) — e.g. `inputs/x28-57425-b9977-net05.json`:
   ```json
   {"n": 28, "L": "22917169/4000000", "B": "0.9977", "proof_net": {...}, "total_mass": "2799999/100000",
    "points": [], "rectangles": [{"rectangle": [x1, y1, x2, y2], "mass": "p/q"}, ...]}
   ```
   - All numbers are exact decimal or rational strings. `L` may be a decimal string; parse exactly.
   - Each listed rectangle is an orbit representative: its mass m is spread **uniformly over its eight
     images under the symmetries of K** (D4 about the centre of K), each image getting m/8 spread
     uniformly over its area. Coinciding images simply add. Check exactly that the sum of the listed
     masses equals `total_mass` and refuse otherwise.
   - `points` must be empty for this version (refuse with a clear message if not; ignoring points would
     be sound but is not needed now). Ignore `B` and `proof_net` in the file: the core side for the
     continuous check is given on the command line.

Controls: `inputs/x28-57425-b9977-net05.mass0985.json` is the same certificate with every mass × 0.985.
Make the n40 control yourself the same way (all weights × 0.985, written to `inputs/`).

## What to build

1. **Input generator** (Python 3, standard library + `fractions` only): reads either format and writes
   the kernel's input file. Requirements:
   - D4 expansion and **outward** intervalisation in the safe direction for a lower bound on capture
     (follow exact.py: the kernel must never see more mass than the certificate has).
   - Axis patch input for `upstream/verifier/axis_integer_grid.cpp`: an axis-parallel side A < B with
     the integer grid at denominator 10^9 (or the upstream denominator if that is what the code
     needs), with inward/downward integer rounding as in exact.py. Choose ε (near-horizontal band) and A
     so that B − A·(cos θ + sin θ) > 0 holds for all θ ∈ [0, atan-band], checked exactly; record the
     margin in the receipt.
   - Writes a manifest with the SHA-256 of the input certificate and of every generated file.

2. **Driver** (`check.py`): command line
   `python3 check.py --candidate FILE [--params FILE] --n N --core B --tau TAU [--workers K] [--node-budget N] [--endpoints ...]`
   - Builds the C++ kernels (`c++ -O2 -std=c++17`) into `build/` if missing.
   - Splits t ∈ [ε, last_t] into slabs (default: the upstream endpoints scaled to the denominator, but
     allow a finer list) and runs the kernel per slab in parallel (`--workers`, default 2).
   - Runs the axis patch.
   - Acceptance, per slab: kernel reports verified, `nodes == 2*leaves - 1`, and the arguments and input
     SHA echoed by the kernel match what was passed. Overall: every slab verified, axis verified, the
     slabs cover [ε, last_t] with last_t ≥ tan(π/8) checked exactly, n·τ > M exactly, L² > 2B² exactly.
   - Writes `runs/<label>/receipt.json`: status `VERIFIED` or `REFUSED`, claim `s(n) > L/B` as an exact
     fraction, all premises as exact fractions, per-slab nodes/leaves/seconds/min lower bound, the
     refused slabs with their witness pose if any, build info (compiler version, source SHA-256 of every
     kernel file), and input SHA-256.
   - Exit code 0 only for VERIFIED.

3. **Limit changes** in the kernel copy (put modified kernel files in `kernel/`, leave `upstream/`
   untouched): raise the rectangle cap (`nr ≤ 10000`) to at least 20000, the side cap (L < 10) to at
   least 12, and the axis-grid cap (nx·ny ≤ 15,000,000) as needed for the inputs above (memory must stay
   below 8 GB). Keep every soundness check. Record each change with the reason in `CHANGES.md`, with
   a unified diff against `upstream/`.

4. **Splitting policy** (allowed, optional): the upstream kernel decides which of u, v, t to bisect by a
   heuristic. Our certificates contain very heavy small boxes (density up to ~6e5 on a 0.001 × 0.001
   box) and long thin heavy bars, so a policy that never splits t can hit the node budget. You may
   change the heuristic (for example: compare the loss terms and split the variable whose contribution
   to the bound's slack is largest, including t). The heuristic must not affect acceptance. Record any
   change in `CHANGES.md`.

## Tests and runs to do here (on this machine, ≤ 2 threads, each run capped at 40 minutes)

- Unit tests (`tests/`): the generator's D4 expansion and mass sum on a tiny synthetic certificate; a
  certificate with one mass removed must REFUSE; parse both formats.
- Regression: n40 main with `--core 199529/200000 --tau 4999/5000 --n 40` → VERIFIED with claim
  1340000/199529 (upstream reports 61.86M nodes, 511 s on 4 workers).
- Controls: n40 mass × 0.985 → REFUSED; x28 mass × 0.985 with `--n 28 --core 499/500 --tau 1` → REFUSED.
- Do NOT run the x28 main case here (it is large); write the exact command for it in README.md.
  It is expected to be VERIFIED with `--core 499/500 --tau 1` (claim 22917169/3992000); the other team
  member's checker needed about 1.1 billion nodes for it.

## Deliverables

- `README.md`: what it checks, usage, the claim, the acceptance rule, how to reproduce on a plain Ubuntu
  machine (packages needed), results of the runs above (copy the receipt summaries), and the exact x28
  command.
- `PROVENANCE.md`: Guzhou0806/n40-square-packing, commit 71c97d0, MIT licence (keep `upstream/LICENSE`
  and copy it as `kernel/LICENSE`); what is reused unchanged, what is modified (pointer to CHANGES.md),
  what is new.
- `CHANGES.md` as above.
- All code under this folder. No absolute paths, user names or machine names in any committed file.
