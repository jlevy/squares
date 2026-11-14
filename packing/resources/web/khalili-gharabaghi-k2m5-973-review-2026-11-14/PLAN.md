# Pre-Stated Plan for the L144 Review of Issue #973

Written 2026-11-14 at about 02:20Z, before any sample, replay or control below was run,
and frozen by its SHA-256 in `receipts/plan.sha256` at that time.
Nothing in this file was changed after the runs began; departures are recorded in the
README and the review.

Source: moh63-dev/k2m5-family at `2c0b1b9979bcb67d92eb215366dc5ee19286c1d8` (tag v1.0).
Checkers: evand/square-packing at `659ee62e4a9d39542a1146e8b011cc3ab6407ede`.
Budget: about 6 CPU-hours at `nice -n 19`, at most 2 jobs at once.
Randomness: Python `random.Random(973)` for every draw below, drawn in the order listed.

## Clean-Room Programs (Written Here From the Paper)

- **A1 cover.** Parse the board; exact total and D; D4 invariance as a measure; segment
  shape; build `mu_k` from the family file by the paper’s Definition 3 for k = 10 to 40;
  board equals built `mu_11`; totals equal k² − 4D; the premises Lemma 7’s proof uses;
  a window identity check for k = 10, 12, 13, 14, 20 and 25.
- **A2 axis face.** Exact Lemma Z over the whole axis-parallel face, centres in
  [1/2, 21/2]², with no symmetry: every one-sided corner limit of every 1/10 cell.
- **A3 pose evaluator.** Exact `mu_11(P)` for rational poses (segments clipped exactly,
  Lebesgue part by exact polygon clipping).
  Samples:
  - S1: 20,000 uniform admissible poses over [0,11]² × θ ∈ [0, 90°);
  - S2: for every base line of the Tight-Tile Lemma’s ranges (d0 ∈ {3/2, 5/2, 7/2}, both
    signs), 10 face points (p, q) uniform in [−4, 4]² at h = 10⁻⁵ and 10 at h = 10⁻⁷;
  - S3: 2,000 uniform poses in the root-9632 window Ω;
  - S4: the centre and the u > 0 corners of 2,000 boxes drawn uniformly from the
    1,255,023 leftover boxes of the authors’ coverage dumps;
  - S5: the authors’ “same limit, smaller growth” pose at h = 10⁻⁶ on `mu_11` and on
    their mutant.
- **A4 coverage.** Re-implementation of the coverage step: every leftover box against
  the Tight-Tile Lemma’s domain as the paper states it, and the job list against the
  lines and strips the lemma’s ranges need.
- **A5 vertex oracle.** On chosen regions, run the authors’ `ttbox.run` with its
  `analyse` wrapped to record each certified cell’s vertices and bound T, map each
  vertex with h > 0 to a pose by this review’s own chart formulas, and require exact
  `mu_11(P) − 1 ≥ T`. Regions: the C_u face [3/4, 5/4]² at (3/2, 9/2, +1); every chart of
  the first strip job and of the first line job in T-A below; one d0 = 7/2 line job’s
  W charts (the area term); the corner and ray zones of one `out_fix` job if T-B runs.

## Replays (Authors’ and Daniel’s Code, Read Before Running)

- **B0.** Build `zmx2` at the pin unpatched and patched; diff must be the one line.
- **B1.** The authors’ fast checks (`sanity_k2m5.py`, `locality_check.py`,
  `audit_zmx2.py`, `check_9632.py`, `summarize_tt.py`, `cov_check.py`) under the
  project interpreter with `-I`.
- **Z-A.** `zmx2 cert0 --d4` (2,500 roots) and `cert0 --full`.
- **Z-B.** First-order `--d4` sweep of 3 whole columns drawn from the columns whose
  recorded CPU is between 1 and 300 s; each column’s census must equal the source log.
- **Z-C.** 40 roots drawn from the 12,024 certified roots, each run alone with
  `--dump-tight` at `--tight 1e-3`, at most 1,800 s wall a root; each must certify.
- **Z-D.** Root 9632 with all uncertified boxes printed; the box set must equal
  `verification/r9632/dump.out`.
- **Z-E.** 3 of the 75 tight-tile roots, drawn from those whose dump records at most
  120 CPU-s, with all uncertified boxes printed and `--uncert-cap 100000000`; each box
  set must equal the authors’ `cov/r<id>.out`.
- **Z-F.** Tight-leaf probe: for the leaves Z-B and Z-C dump, exact `mu_11` at every
  admissible corner and at 2 random interior admissible poses must be at least the
  leaf’s certified bound. At most 30,000 evaluations, leaves drawn uniformly if more.
- **Q-A.** `qx2_zm.py` on `c9632.txt` over the window W; its uncertified boxes must equal
  `zm_unc.txt`; the closure check is then re-done by A4-style code of this review. Also
  check that `c9632.txt` is a sub-measure of `mu_11`.
- **T-A.** 8 Tight-Tile jobs drawn from the 174 main jobs whose outputs record at most
  120 s; per chart, cells, ok, fails and worst must equal the source output.
- **T-B.** The `out_fix` job `d3.5_s-1_line_3.5` (wedge-corner and ray zones), if its
  price here is under 1,500 CPU-s.

## Controls

The authors’ controls, replayed:

- `zmx2` at root (15, 36) bin 0, depth 24, node cap 2,000,000, on the real cover and on
  the ×0.999 and ×0.993 covers;
- `ctl_rise.py` on `mu_11` and on `ctl_rise.txt`;
- `locality_check.py` on `box12_onemutation.txt`;
- the qx2 ×0.999 control on the 9632 window, only if the budget remains after the rest.

This review’s own, stated now:

- **M-1.** The Lebesgue weight of the board times (1 − 10⁻⁶): `zmx2` first-order at root
  12096 (centre cell [5.4, 5.5]², bin 0, where every pose has `mu_11 = 1` exactly) must
  refuse; on `mu_11` it must certify. The exact evaluator confirms mass 1 − 10⁻⁶ there.
- **M-2.** Every segment weight lowered by one unit of 1/(2·10¹²): `zmx2 cert0 --d4` must
  refuse, and A2 must find a corner limit below 1.
- **M-3.** A first-order-only mutant of the Tight-Tile kind at a tile other than the
  authors’ (3/2, 9/2): at (d0, y_b, σ) = (5/2, 3.5, +1), then (3/2, 2.5, −1), then
  (5/2, 4.5, −1), the first where it exists, remove the one segment whose limit
  contribution is zero on the C_u face and whose removal gives an exact mass below 1 at
  some face point at h = 10⁻⁶. `ttbox` must refuse a C_u face box around that point and
  certify the same box on `mu_11`.
- **M-4.** One leftover box in a copy of one dump widened to u1 = U0 + 2⁻⁴⁰: the
  authors’ `cov_check.py` and A4 must both report it outside.
- **M-5.** One qx2-uncertified box of root 9632 moved to meet a zmx2 leftover box: the
  authors’ `check_9632.py` and this review’s closure check must both refuse.

## Freeze

Before reading anything of step 5 (the record’s T-064, T-081, T-252, T-066, T-184 and
k² − 5 material at n = 76 to 95), the verdicts and the SHA-256 of every program and
output are written to `receipts/freeze.sha256`.
