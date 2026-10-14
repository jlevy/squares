# 08 — A confirmation record: our independent replay of T-037 (Kleddamag, s(11) > 31/8)

**Abstract.** On 2026-10-07 the lab replayed Kleddamag's threshold certificate at the reviewed release v1.0.2
(the T-037 of your register, Part II of the n = 11 series): the exact Python sweep row by row (12,028 of 12,028
rows, 0 differ from the retained evidence), the stdlib controls, the integrity check twice, and an independent
spot-check in our own exact arithmetic (scaling, budget, 3,240 exact poses, the strict counting inequality).
Verdict PASS.  We record one integrity note (a script of theirs rewrites a pinned file with CRLF; restored) and
what the window [31/8, s0] does to our trees (99 nodes dead at once).  Offered as a confirmation record, not a result.

Repository https://github.com/Esummins/packing (paths under `blob/master/`): `attempts/A242-replay-31-8/` (pin
`ext/PIN.json`, verdict `results/replay242.md`, `results/replay242.json`, `results/spot242.{json,jsonl}`,
`results/controls242.json`, `results/integrity242.txt`, `results/adopt242_dryrun.{txt,json}`, logs);
`docs/proofs/threshold_bound.md`; Lean `Statements/Open/ThresholdBound.lean`.

## 1. What ran (`results/replay242.md`)

* **Pin.** https://github.com/Kleddamag/11-squares-certified-bound tag v1.0.2 (tag object 59dc5626, commit
  6a733f339395c3514f2ab63d8c4aa64cf63c0b5a); every file's SHA-256 in `ext/PIN.json`.  Certificate
  `global-certificate.json` SHA-256 `57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458` (matches
  the release; NOT with `core.autocrlf=true` — the clone was re-checked-out with `autocrlf=false`).
* **Every script read before running** (external code is untrusted input in this lab): `check_integrity.py`
  (54 pinned files), `verify_threshold_algebra.py` (exhaustive k-of-m identity + budget for m = 3, 5),
  `exact_mixed.py` + `integer_sweep.py` (the exact sweep: validate, geometry, segment tree), `independent_controls.py`
  (stdlib containment quadratics + 16 rows of boundary samples).  **Refused**: `prepare_secondary.py` /
  `replay_secondary_parallel.py` / `verify.py` — they download R038's upstream JavaScript at run time (urllib to
  raw.githubusercontent.com) and need node; the secondary BigInt checker was therefore not run.  Nothing suspicious
  found: no shell-outs except node / `sys.executable` in the launchers, no writes outside the repository except the
  user-chosen output paths, the only network access the documented upstream fetch.
* **The replay.** `code/rows242.py` drives their `exact_mixed` + `integer_sweep` over all 12,028 angle rows in two
  shards (pure-Python kernel, BelowNormal; shard walls 3,935 s and 4,164 s, CPU 8,089 s): status
  `PASS_REPLAY_PYTHON_ALL_ROWS`; minimum 999962528 (= Γ) at row 11962; budget 10999479944; surplus 107864;
  86,299,918 slabs, 511,649,694,680 cells.  **Row by row against their retained evidence (minimum, cells, slabs):
  0 rows differ, histogram equal, totals equal** — for both the initial and the portable evidence files.
* **Controls** (`independent_controls.py`, rerun): containment 48,112 checks; boundary samples 5,586 centres,
  minimum 1000047518.  **Integrity**: PASS 54 pinned files, twice (2026-10-07 by the agent; 2026-10-11 by the
  coordinator on the pinned clone).

## 2. The exact spot-check in our own arithmetic (`code/spot242.py`, no import from their repository) — PASS

(a) **Scaling**: (191/50)/(764/775) = 31/8 exactly (Fraction).  (b) **Budget**: M = Σ_p w_p + Σ_S ⌊|S|/k_S⌋ w_S
re-summed over the D4-expanded data from `global-certificate.json`: 5,284 sites (496 with positive point weight),
2,220 threshold sets, families in units of 10⁻⁹: point 2247714156, 2-of-3 3188007592, 2-of-5 989672288, 3-of-5
4574085908; M = 10999479944 = the certificate's `budget_units`; D4 invariance checked.  (c) **Charges at poses**:
3,240 exact (row, legal centre) pairs — 2,000 random rows, 1,000 draws from the 47 critical rows, 60 corner
domains — each k-of-m charge re-evaluated exactly at the pose with our SAT-based containment test: 0 failures,
minimum charge 1000047518, never below the recorded row minimum.  (d) **Counting**: 11Γ − M = 107864 units > 0.
10.7 s total.  Rows written to `results/spot242.jsonl` (1.4 MB).

## 3. The two lemmas in our notation, and what the verifier trusts (`docs/proofs/threshold_bound.md` §1–2)

* **Scaling lemma** [T]: Fits(11, s) with s ≤ 31/8 implies eleven parents of side A = 764/775 fit in [0, 191/50]²,
  since (191/50)/(764/775) = 31/8; so "no eleven parents in L" gives s > 31/8 for EVERY s — strict without
  compactness (their PROOF.md uses attainment; not needed).  Lean `scaling_arith`, `scaling_side`.
* **Budget lemma** [T], n-general: for pairwise disjoint Q₁…Q_q, Σᵢ C(Qᵢ) ≤ M — a site lies in at most one Qᵢ, and
  the qualifying Qᵢ of one threshold set hold disjoint k-subsets of S, so q′k ≤ |S|.  Lean `budget_lemma`; the
  conclusion 11Γ > M is Lean `counting`.
* **Trusted by the replay**: CPython integer / Fraction arithmetic and numpy int64 (sums < 2⁵⁰); the JSON parse;
  the correctness of their `geometry` (rectangle construction, slab cover, query ranges — read, found conservative);
  the four hand lemmas (inclusion–exclusion for k-of-m, upper semicontinuity at boundary centres, D4 folding, scaling).
  What the verifier checks: catalogue coverage of [0, u_max] with u_max > √2 − 1; the core–parent angle range; the
  strict core margin (≥ 10⁻¹²); the parent envelope; the counting; and the sweep's per-row minimum ≥ Γ.
* **Lean** (`Statements/Open/ThresholdBound.lean`): the bound is a documented axiom `threshold_bound_31_8` citing
  T-037 and this replay; `lb382_of_threshold` (3.82 follows), `window_restrict`, `stratum_kill_of_wnd′`,
  `trump_residual_of_wnd′` (the window statements restricted to [31/8, s0] follow) are theorems.

## 4. Integrity note, and the window consequence (`results/adopt242_dryrun.txt`; nothing was edited)

* **CRLF.** Their `verify_threshold_algebra.py` writes `threshold-algebra.json` inside the repository and, on a
  Windows checkout, rewrote that pinned file with CRLF line endings; the integrity check then disagreed with the
  pin until the file was restored from the release.  Recorded in `results/integrity242.txt` (PASS ×2 after the
  restore) and `logs/algebra242.log`.  No defect in the certificate or the sweep; a portability note for the
  retained package: run their algebra check on a copy, or pin `core.autocrlf=false`.
* **If adopted, W = [191/50, s0] → W′ = [31/8, s0] = [3.875, 3.877084]** (a coordinator decision; nothing on the
  running campaigns was changed).  The pads π₀..π₂ shrink from 0.025510 / 0.040454 / 0.055397 to 0.000918 /
  0.001456 / 0.001994 (×1/27.8).  Node ledger (A211 + A270 + A269, last pass per node and pad): 1,795 nodes, dead on
  W 1,444, dead on W′ 1,543 — **99 nodes DEAD AT ONCE** (k5_11 68, k5_16 31); alive on W′ 252 (k5_11 99, k5_16 133,
  trump5 c0 17, other 3).  Tube certificates: 54, reaching the whole window 31 on W and 53 on W′.  Slabs wholly below
  31/8 become void (A57's grid sides 2–4, A269's trump5 sub-slab); A270's g2/g3/g4 and A269's pad campaigns are
  needed only for (3.82, 3.861637] and are void on W′; `certs/measure_certificate_3.8{0,1,2}.json` are superseded as
  bounds (Theorem 1 stays a Lean theorem; T-037 is an axiom).  The eleven k0 cells' implied window shrinks with the
  pad (K0-WIDEN 0.025509 → 0.000918).

## 5. Relationship to your record

Your register holds T-037 at the rung your review gave it (verified 2026-09-22, replay receipt on your side) and
T-060 / T-112 settle s(11) = T and uniqueness.  This replay is a second, independent route on T-037 only: the
author's own exact Python checker re-run in full (`same-implementation` in your terms) plus a spot-check that
shares nothing with their code (our exact SAT containment, our Fraction budget).  We claim no rung and no new
bound; we offer the receipts for retention beside T-037 if they are useful, and the CRLF note for the packet.

## What we ask

1. If you retain this, pin `attempts/A242-replay-31-8/` at the commit named in `00-README.md` §4; the certificate
   hash above is the join key.
2. Whether a confirmation of this shape (full re-run of the author's checker + an independent spot-check of the
   premises) is worth a "replayed" annotation on T-037, or belongs only in the packet.
3. The secondary (JavaScript BigInt) checker we refused to run for network reasons: if your records lane has a
   retained offline copy, we would run it on the same pin.

Sources (https://github.com/Esummins/packing/blob/master/): `attempts/A242-replay-31-8/{BRIEF.md,results/replay242.md,results/replay242.json,results/spot242.json,
results/controls242.json,results/integrity242.txt,results/adopt242_dryrun.txt,ext/PIN.json}`;
`docs/proofs/threshold_bound.md`; `lean/PackingCertMathlib/PackingCertMathlib/Statements/Open/ThresholdBound.lean`;
your `packing/frontier/n-011.md` and the n11 threshold-bound review (Part II).
