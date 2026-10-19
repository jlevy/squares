# A241 — the ROW cascade: what a full-window row is, what it is not, and what it costs

A238's finding (2026-09-16 13:00) is the brief: every geometric rule of the k5 toolkit acts on Theorem FC's
forced cells, `classes178.forced_cells` marks a cell usable only when the one-slot EXTENSION class carries a
FULL-window A56 scoreboard row, and the eight k4 classes A55 killed exactly (`k4_00`, `k4_01`, `k4_02`,
`k4_04`, `k4_07`, `k4_09`, `k4_10`, `k4_12`) have no such row. Rowing them hands every k ≤ 3 class 2–5
forced cells. Labels: [T] proved, [M] measured here, [F] finding.

## 0. The correction the attempt has to make to its own brief [T]

The brief states the cascade as

> a k4 class C gets a full-window row when EVERY one-slot extension of C is full-window closed
> (Lemma K1 on the window).

**That rule is unsound as an emptiness statement, and A241 does not use it.** Lemma K1
(`docs/proofs/instratum_bridge.md` E.1) climbs UP containment: a kill of S empties every S′ ≥ S. It says
nothing downwards. A packing whose skeleton is *exactly* C carries no fifth simple square, so none of C's
one-slot extension classes ever applies to it, and "every extension of C is dead" is consistent with C
being non-empty.

What closed extensions DO give is **Lemma SLOT-CROWD** (`docs/proofs/slot_crowds.md` §2): at a usable slot
p of C the single-meeter case teleports a square onto p and lands in the closed class C ∪ {p}, so p is met
by ≥ 2 non-pin squares. That is Theorem FC's forced cell — the toolkit's *traction* on C, which is exactly
what A238 measured and exactly what the k ≤ 3 tier is missing. Promoting "every usable slot of C is doubly
met" to "C is empty" is the crowd-counting certificate CS(S; s, m_lo; δ, e) of `slot_crowds.md` §4, and A94
measured that it **does not certify**: LP PASS at every window, runs B₂–B₄ FAIL with 30–32 exact holes, and
the Trump-image ceiling δ_T(S) makes the chain VOID for k4_03 / k4_06 / k4_08 anyway (§6).

So a row has exactly two sources, and `code/rowcascade241.py` implements only these:

* **(A) a direct window certificate** — `parametric-kill-certificate-v1` 4D PASS over
  [191/50, 969271/250000] + canary C2 (the unmodified A53 `verify_case.py` at 191/50, the midpoint and s0).
  `closed_disjoint_bridge.md` B.2 then instantiates `stratum_kill` at every m of the window: rationals are
  dense in each certified s-cell, ρ > 0 exactly, `nofams` empty.
* **(B) the Lemma K1(i) climb** — a class CONTAINING a rowed class inherits its row with the same window.
  The row records the contained class and the D4 element.

## 1. Why A55's eight exact kills were not already rows [T, and it is not bookkeeping]

A238's notes call the blockage "half bookkeeping". The precise statement is worse than that, and it is the
reason A241 is a compute campaign rather than a table edit:

`closed_disjoint_bridge.md` B.2 measures the corpus containment margin over all 68 scanned kill
certificates (A53 ×52, A54 ×4, **A55 ×10**, A55/k3_ext ×1, A57 base — uniform core parameters):

> ρ = 73787046228886605157/73786980692884783104003906250 ≈ 1.0000009·10⁻⁹, A = 5/2, so Corollary B′'s
> hypothesis (H′) reads **s″/m − 1 < 4.0000·10⁻¹⁰**.

An s0-anchored PASS therefore kills at sides m ∈ [s0/(1 + 4·10⁻¹⁰), s0] only — a shell of relative width
4·10⁻¹⁰ below s0 — while (s0 − ŝ)/ŝ ≈ 1.057·10⁻⁷ already exceeds it. **A55's k4 certificates instantiate
the kill at NO side of the window [3.82, ŝ] whatsoever.** The "scales 1.048–1.164" in A55's ledger are the
certificate's LP mass slack, not a dilation window; they buy nothing here.

The window statement is A56's parametric layer: re-express every atom and core position as an s-affine
function (`make_param.py`, C1 identity at s0), run the 4D (t, c_x, c_y, s) verifier over the window
(`verify_param.py`), canary C2. That is what produced the existing 52 rows, and it is what `code/param241.py`
runs on A55's base certificates — the same pipeline, the same frozen integer core, the same anchoring ladder
(gap → nearest-wall → mid-band; the anchoring is a COMPLETENESS choice, never soundness, `soundness.md` P3).

## 2. What can be rowed today [M]

`results/rows241.md` §3 carries the live table. In one line:

* **rowable today, blocked on nothing but CPU** — `k3_00` and the eight A55-killed k4 classes. Each already
  carries its own A55 `case-measure-certificate-v1` PASS; only the parametric re-expression and the 4D run
  are missing. `k4_00` / `k4_01` / `k4_02` each CONTAIN `k3_00` (D4 `id` — A55 `cap.json`'s own witness
  field), so they also row by (B) the moment `k3_00` rows.
* **not rowable, ever, by a certificate of this kind** — the six protected k4 classes and the ten open
  k ≤ 3 classes. Lemma K1(ii) forbids it: each is ≤ an open k5 class, so τ*(S) ≥ 11 − |S| and no certificate
  can exist (`instratum_bridge.md` E.3). Their rows come only from the P-TREE obligation O1, i.e. after the
  frontier.
* **waiting on the frontier, for forced cells rather than rows** — the protected k4 cells that extend into
  `trump5` / `k5_11` / `k5_16`; `corners4` is the extreme case at 0/8.

## 3. The cascade, and where it is wired in [M]

`code/rowcascade241.py` is idempotent: it re-reads the A56 scoreboard, adds an (A) row for every class whose
window statement has landed, then climbs (B) to a fixed point, writes tmp + `os.replace` (A114's atomic-write
rule, backup `scoreboard.json.bak_pre_a241`), and appends what changed to `results/cascade241.jsonl`. It is
run every 10 minutes by `docs/shadows/status_loop.sh` (installed by RENAME — the loop was running; the
pre-A241 copy is kept as `status_loop.sh.pre_a241`), so a class rows itself the moment its verification
lands and the k ≤ 3 tier gains its forced cells without another attempt.

`code/traction241.sh` is the measurement: A238's own benchmark (A211 coarse tree + A212 gate/tube + A224
SNAP + A230 EPS, unchanged, isolated `--cert-dir` / `--results`) on k3_02's 20 A100 head-to-head cover cells,
wall 300 s, against A238's blind run (0 DEAD / 20 ALIVE, mean 4.3 s, `kills_by_rule = {}`, max depth 0). It
waits for the cascade to give k3_02 a usable cell before it starts, so the number it reports is never a
re-measurement of the blind run.
