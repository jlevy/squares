# Review 2026-09-04 — Hostile Third-Party Check of the s(11) ≥ 19/5 Package (T-018)

A review of `packing/cases/n11_fractional_certificate/thirdparty/`, written as the
outside mathematician the package is addressed to: no trust in the repository, the
theorem re-derived from the README, the verifier read line by line against it, the
package run in an empty environment from a copy outside the repository, an independent
implementation of the expensive condition written and run, and the package attacked with
inputs of my own. The reviewer owned only this file and modified nothing else.

## Verdict

**The package establishes `s(11) ≥ 19/5` to a hostile reader.** The theorem in the
README is correct as written, `verify.py` decides exactly that theorem and nothing
weaker, the certificate is accepted with the numbers the README states, the control
reproduces Massaccesi’s published value by an implementation that did not see his code,
every perturbation in the package’s falsifier and every perturbation of my own is
refused for the right reason or accepted because it is in fact a valid certificate, and
an independent implementation of C4 agrees with the verifier to the last cell.

The verdict rests on two things the package cannot supply and says so: CPython’s
arbitrary-precision integers and `fractions` module, and the reader’s own reading of the
six-step proof and of the finite reduction behind C4. I did both readings from scratch;
they are in sections 1 and 2.

**No defect found threatens the result.** Three defects affect the packaging (a
misattributed sentence about the control, tracebacks where a labelled refusal is
promised, an overstated “nothing short-circuits”), and five are cosmetic.
None changes any verdict the verifier prints.
They are ranked in section 7.

## What Was Reviewed

Commit `5673ecac9a67a257830e76504a51376bc923dcde`, working tree clean for the package
directory. SHA-256 of the files:

| File | SHA-256 |
| --- | --- |
| `README.md` | `017d884e5d0843f7fbfb335f3407f7f1a24d5e6a35e54f9499805c5829717c88` |
| `verify.py` (506 lines) | `40a7d8abaa69fb2f1dbc78ef1b5009afb3bb78a5d3e4435d2da3893d08ca0bdc` |
| `certificate.json` | `60ac0c33e2e5a55874a10b0d09c6aaf3f891db921b063cc860114c2d4588c055` |
| `control-n17-massaccesi.json` | `32e83142768b96cf861896b5a4a07829070a245b55d7c61f22b3c81a0eaf1d97` |
| `build_n17_control.py` | `f3b22054f2f209cdbdb5255e48c38724832e048aecc2986d138005ff4745dd40` |
| `falsify.py` | `72fc0afc39d47bcc79631b93763827e4cdfcc9fdc96335e753c31fa4e2b05ffc` |
| `check.py` | `444855e449838af1ac91891d26a2ce4b84940b2eaae21ba572931f750f19b36b` |

The certificate’s hash equals the one the README states, and the file is byte-identical
to `../certificate-19-5.json`.

## 1. The Theorem as Written Implies the Bound

I re-derived the six steps of the README’s proof without reference to the repository’s
other documents. All six hold.
The three points the assignment singled out:

**Why the bound is `L` and not `L/B`.** The conclusion of the theorem is “no `n` unit
squares with disjoint interiors fit in `[0, L]²`”, and the shrunken side `B` never
touches the container.
`B` is spent entirely on orientation: a unit square at an arbitrary angle contains a
concentric `B`-square at the nearest net angle, and C4 speaks only about `B`-squares *at
net angles*. A bound `L/B` would need the scaled statement “no `n` `B`-squares at *any*
angle fit in `[0, L]²`”, which C4 does not give, because a `B`-square between net angles
contains no `B`-square at a net angle.
The control makes the point numerically: `L/B` would read `4.517999` for Massaccesi’s
certificate, which is not his published `4.5058`, and `3.808760` here.
Massaccesi’s own source prints `s(17) >= {L}` (section 4), so the published value is `L`
under the same reading.

**Why strictness in C3 gives disjointness.** Step 3 puts `Q` in the *open* interior of
`S'_j`: for each edge normal of `S'_j` the support of `Q` is `(B/2)(cos d + sin d)`, and
`B(cos d + sin d) = B cos d (1 + tan d) ≤ B(1 + D) < 1`. So `P_j ⊂ int(S_j)`, the
interiors are pairwise disjoint by hypothesis, hence the `P_j` are pairwise disjoint.
An atom on the boundary of the closed `Q` is therefore in `int(S_j)` and in no other
`int(S_k)`, so it is counted once.
Without strictness `Q` could reach `∂S_j`, and an atom on an edge shared by two packed
squares would be counted twice, which is exactly the double count that the counting step
forbids. (Strictness is sufficient rather than necessary: with `B(1 + D) = 1` one still
has `B(cos d + sin d) ≤ cos d < 1` for `d > 0` and `B < 1` at `d = 0`, since `D > 0`.
The proof uses the strict form and is correct as written; the verifier checks the strict
form, which is the safe side.)

**Whether the net covers every real orientation.** Orientation is defined modulo a
quarter turn, so `φ ∈ [0, π/2)`. For `φ ∈ [0, π/4]` the net covers directly: `t₀ = 0`
(precondition P3) and C2 give `[0, π/4] ⊆ [θ₀, θ_K]`, so `φ` lies in a closed gap
`[θ_k, θ_{k+1}]`, and the worst case is the midpoint, where `d` equals the half-gap and
`tan d = (t_{k+1} − t_k)/(1 + t_k t_{k+1}) ≤ D` exactly, the tangent subtraction formula
being valid because each half-gap is below `π/2`. There is no seam.
For `φ ∈ (π/4, π/2)` the diagonal reflection `R` gives orientation `π/2 − φ ∈ (0, π/4)`;
`R(Q)` is not at a net direction and need not be, because only `mass(R(Q)) = mass(Q)` is
used, and that follows from C0 (`R` is one of the eight maps the verifier checks, and
invariance of the aggregated weight function under `R` is what `condition_c0` decides).
The direction net is not uniform in angle; `D` is the maximum over gaps and is attained
at `k = 0`, where `D = T/K = 207107/90000000`, which I recomputed.

Two further checks on the statement.
C1 must be strict, and is: with `Σw = n` step 6 gives `n ≤ n`, no contradiction (the
falsifier’s eighth row shows the verifier refusing exactly this).
C4 may be non-strict, and is: `mass(Q) ≥ 1` is all step 6 needs (my attack 2 in section
5 shows the verifier accepting a certificate whose least covered weight is exactly `1`,
correctly). The closing infimum argument is right: the set of feasible sides is upward
closed, so a container of side exactly `L` failing gives `s(n) ≥ L`.

## 2. `verify.py` Implements That Theorem, Not a Weaker Cousin

Read line by line against the README.

- **Loading.** Every rational passes the regex `^-?[0-9]+(/[1-9][0-9]*)?$` before
  `Fraction`; the net is generated as `T·k/K` in `Fraction` arithmetic; `direction(t)`
  returns `c = (1 − t²)/(1 + t²)`, `s = 2t/(1 + t²)` and asserts `c² + s² = 1`. I
  confirmed the assertion holds for `t = 0`, `t = 207107/500000` and `t = 1/3`.
- **P1 to P5** are the shape the theorem assumes: `n ≥ 1`, positive sides, non-negative
  weights and at least one atom, `t₀ = 0` with a strictly increasing net of at least two
  terms, triples, and the `claim` string equal to `s(n) >= L` for the parsed `n` and
  `L`. A failing precondition returns before C0 to C4, which is reasonable but
  contradicts the README’s “nothing short-circuits” (defect D3).
- **C0** aggregates weight by site and requires, for every site and each of the eight
  maps, that the image site carries the same total weight.
  Because each map’s inverse is in the group and the check runs over every site, this is
  full invariance of the weight function on the plane, including that the support maps
  onto itself. It is the reflection `(x, y) ↦ (y, x)` the proof needs, plus seven maps it
  does not, which is the safe direction.
- **C1, C2, C3** are the closed-form tests of the README, in the same rationals.
  C3 computes `D` as the maximum of `(b − a)/(1 + ab)` over adjacent pairs, which is the
  tangent of the half-gap, as the README’s remark says.
- **C4** decides, for each direction, the exact minimum of the covered weight over the
  closed set `F` of admissible centres, `h ≤ X, Y ≤ L − h` with `h = B(|c| + |s|)/2`.
  That is “every closed `B`-square at angle `θ_k` inside `K`”, closed containment, a
  superset of the placements the proof meets.
  The reduction to open grid cells is the one place the verifier could be subtly weaker
  than the theorem, so I re-derived its five claims (the comment block at lines 201 to
  233): (a) the covered weight is constant on an open cell because every atom box is
  closed with edges on breakpoint lines; (b) a point on a cell’s boundary covers at
  least the cell, for the same reason; (c) every point of `F` is in the closure of some
  open cell that meets `F`, because `F` is a closed square of positive side (the code
  checks `2h < L`) and so has interior points arbitrarily near each of its points; (d)
  hence the minimum over `F` is the minimum over open cells meeting `F`, and cell
  boundaries never need visiting; (e) an open cell `(a, b) × (c', d)` meets `F` iff
  `c' < hi` and `lo < d`, where `[lo, hi]` is the `V`-projection of `F` clipped to the
  closed strip `[a, b]`. For (e) I checked the step the comment relies on:
  `G = F ∩ {a ≤ U ≤ b}` is a convex polygon with non-empty interior whenever the open
  strip meets `F`, and the projection of the interior of a planar convex body is the
  interior of its projection, so the open strip’s `V`-projection is squeezed between
  `(lo, hi)` and `[lo, hi]`, and both give the same test against an open interval.
  The bisect bounds `j0 = bisect_right(v, lo)`, `j1 = bisect_left(v, hi)` are exactly
  the cells satisfying that test, including the two unbounded ones, and `lo < hi`
  guarantees `j0 ≤ j1`.
- **Mechanics.** The 2D difference array marks rows
  `[u_index(u_k − B/2) + 1, u_index(u_k + B/2)]` and the matching columns, then two
  prefix-sum passes; I checked the index arithmetic against the cell convention at lines
  312 to 316. Weights are scaled to integers by the least common denominator (`200000`
  here) and divided back at the end.
  The minimising cell’s weight is recomputed by direct summation in the original
  coordinates at a witness point that is asserted admissible; a disagreement aborts.
  `--audit N` re-sums `N` random feasible cells per direction the same way.
- **Unit tests of the geometry.** I ran `clip` on the unit square against `x ≥ 1/2`,
  `x ≤ 1/2`, a box `[1/4, 3/4] × [1/3, ∞)` and a wholly excluded half-plane, and on a
  diamond against the strips `[0, 1/2]` and `[1/2, 1]` (expected `V`-ranges `[−1, 1]`
  and `[−1/2, 1/2]`). All correct, with the repeated-vertex output the docstring warns
  about and nothing downstream minding.
- **The verdict** is computed from the list of recorded checks, not from the results
  dictionary, and the printed conclusion uses the parsed `n` and `L`. The `total_mass`
  and `least_cell_mass` fields are compared and reported as `info`/`NOTE` only.

Where the verifier is stricter than the theorem it is always on the safe side: C0 checks
the full group; a zero-weight atom at an asymmetric site is refused (defect D6); a
direction at which no `B`-square fits with room raises instead of being treated as
vacuous. I found no place where it is weaker.

## 3. Runs: Observed Numbers

All runs from a copy of the directory in a session scratch directory outside the
repository, with `env -i PATH=/usr/bin:/bin`, on a 4-core box with load average about 4
from other work.

| Run | Interpreter | Result |
| --- | --- | --- |
| `check.py` | CPython 3.14.7 (project venv, invoked by absolute path) | control rebuilt identical; certificate `VERIFIED: s(11) >= 19/5`, least covered weight `50003/50000` at direction 0, centre `(53/100, 53/100)`, `90546593` cells over 181 directions in 25.4 s; control `VERIFIED: s(17) >= 22529/5000`, least covered weight `1`, centre `(364907/560000, 364907/560000)`, `16562293` cells in 7.4 s; bounded negative-weight control refused; `all four steps passed`; exit 0 |
| `check.py` (the README’s stranger run) | `/usr/bin/python3` = CPython 3.11.15 | identical numbers; C4 33.3 s and 10.0 s; real 43.7 s; exit 0 |
| `verify.py control-n17-massaccesi.json` | CPython 3.10.20 | `VERIFIED`, least covered weight `1`, `16562293` cells in 9.3 s; exit 0 |
| `verify.py certificate.json --audit 3` | CPython 3.14.7 | `VERIFIED`, same numbers, 30.7 s; exit 0 |
| `falsify.py` | CPython 3.14.7 | ten rows, every cell identical to the README’s table; real 4 m 21.6 s; exit 0 |

The ten falsifier rows as observed (C4 column is the recomputed least covered weight):

| Perturbation | C0 | C1 | C2 | C3 | C4 | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| tight atom’s weight −1/10000 | FAIL | PASS | PASS | PASS | FAIL `24999/25000` | REFUSED |
| its orbit’s weights −1/10000 | PASS | PASS | PASS | PASS | FAIL `49993/50000` | REFUSED |
| tight atom dropped | FAIL | PASS | PASS | PASS | FAIL `49189/50000` | REFUSED |
| its orbit dropped | PASS | PASS | PASS | PASS | FAIL `387/400` | REFUSED |
| tight atom shifted +1/1000 in x | FAIL | PASS | PASS | PASS | PASS `50003/50000` | REFUSED |
| container side 4, atoms unchanged | FAIL | PASS | PASS | PASS | FAIL `0` | REFUSED |
| container side 4, atoms translated +1/10 | PASS | PASS | PASS | PASS | FAIL `0` | REFUSED |
| weights scaled to total exactly 11 | PASS | FAIL `11` | PASS | PASS | PASS `1100066/1084775` | REFUSED |
| angle limit 41/100 | PASS | PASS | FAIL `−119/10000` | PASS | FAIL `195849/200000` | REFUSED |
| `B = 1/(1 + D)` | PASS | PASS | PASS | FAIL `1.000000000` | PASS `50003/50000` | REFUSED |

The README’s side arithmetic also checks: `(19/5 − 2)²·5 = 81/5 > 16`, the movement
`19/5 − (2 + 4/√5) = 0.0111456…`, Trump’s polynomial has its real root at
`3.8770835900…`, `B(1 + D) = 899996306539/900000000000` with margin `4.10 × 10⁻⁶`, the
C2 slack `309449/250000000000`, and `K = 180` is the least net size for this `B`
(`K > BT/(1 − B) = 179.68`; at `K = 179` C3 fails, section 5).

## 4. Independent Cross-Checks

**An independent implementation of C4.** I wrote one from the theorem and the reduction,
sharing no code with `verify.py`: per-strip one-dimensional difference arrays instead of
a 2D prefix sum, the `V`-range of `F` within a strip from `F`’s vertices and edge
crossings instead of Sutherland-Hodgman clipping, cell selection by linear counting
instead of `bisect`, and rank arithmetic for the cells.
Over all 181 directions it reports least covered weight `50003/50000` at direction 0 and
`90546593` cells, both equal to the verifier’s, and its per-direction cell counts agree
at every direction both programs print (`34969`, `512197`, `505529`, `499545` at
`k = 0, 60, 120, 180`). Runtime 101 s.

**A hand summation at the witness.** At direction 0 the closed square of side
`9977/10000` centred at `(53/100, 53/100)` contains 24 atoms, listed and summed by a
five-line script with no grid machinery: `50003/50000`. The same 24 atoms and the same
weight are covered by the corner placement centred at `(h, h)`, `h = 9977/20000`.

**Random sampling by a third method.** 181 directions × 4000 random admissible centres
in floating point with numpy, a quarter of them forced onto the boundary of `F`: least
covered weight `1.000060000`, never below the exact minimum.

**The control against its published source.** I fetched Massaccesi’s post (dated
2026-08-21) rather than trusting the transcription.
The constants `L = 45058/10000`, `M = 15513/10000`, `B = 9973/10000`,
`T = 207107/500000`, `KMAX = 180`, `WEIGHT_SCALE = 576`, `NGRID = 29`, the coordinate
formula `M/2 + step·i`, the eight-image `orbit` function and all 23 triples appear
verbatim as in `build_n17_control.py`. His prose states “168 somewhat interesting points
in a square of side 4.5058 in a 29x29 grid.
They sum only 16.9166…”; `16.9166…` is `203/12 = 9744/576`. His code asserts
`total < 17 * WEIGHT_SCALE`, `contain < 1` and `global_min >= WEIGHT_SCALE`, and prints
`s(17) >= {L}`: the same three conditions and the same reading of the bound.
(The asserts `len(atoms) == 268` and `total == 169476` in his file are commented out and
belong to Burns’s earlier certificate.)
He writes the value as “4.5058(?)”, and the post is not peer reviewed; the README says
the latter.

## 5. Adversarial Inputs of My Own

Each row is a perturbation I constructed; the full decision was run unless the row says
closed-form. “Right reason” means the failing condition is the one the perturbation
should trip, with the numbers to match.

| Input | Observed | Right reason |
| --- | --- | --- |
| 1. Whole orbit of the tight atom `(1/2, 29/30)` moved to `x − 1`, outside the container, symmetry kept | C0 PASS; C4 FAIL `387/400 = 0.9675`; `all atoms lie in [0, L]^2: no`; REFUSED | Yes: an outside atom is never covered, so the value equals the orbit-dropped row |
| 2. Orbit weights lowered by exactly `3/100000` each | C4 PASS, least covered weight exactly `1`; total `1084751/100000 < 11`; VERIFIED | Yes: `mass(Q) ≥ 1` is the hypothesis, and this is a valid certificate of the same bound |
| 3. Orbit weights lowered by `3/100000 + 10⁻¹⁵` each | C4 FAIL `499999999999999/500000000000000`; REFUSED | Yes: the drop is exactly `2 × 10⁻¹⁵`, two orbit members in the tight cell; the boundary is decided exactly |
| 4. One direction fewer, `K = 179` (closed-form) | C3 FAIL `B(1 + D) = 895007806539/895000000000 = 1.0000087` | Yes |
| 5. `K = 90` (closed-form) | C3 FAIL `1.0022918` | Yes |
| 6. `K = 90` with `B = 995/1000` so C3 passes (`0.99958`) | C4 FAIL `17771/20000 = 0.88855` at direction 50; REFUSED | Yes: a thinner net bought with a smaller square covers less |
| 7. Container `381/100`, atoms scaled by `L'/L` | C0 PASS; C4 FAIL `17771/20000` at direction 101; REFUSED | Yes |
| 8. Container `381/100`, atoms translated by `1/200` | C0 PASS; C4 FAIL `22443/25000 = 0.89772` at direction 0, centre `≈ (0.49992, 0.49992)`; REFUSED | Yes |
| 9. Container `19/5 + 10⁻⁶`, atoms translated by `5 × 10⁻⁷` | C0 PASS; C4 PASS `50003/50000`, `90546641` cells; VERIFIED `s(11) >= 3800001/1000000` | Yes, and see below |
| 10. Orbit of the tight atom shifted by `+1/1000` in `x` on all eight images | C0 PASS; C4 PASS `50003/50000`, `90547389` cells; VERIFIED `s(11) >= 19/5` | Yes: a different, equally valid certificate |
| 11. `claim` changed to `s(11) >= 4`, `L` unchanged (closed-form) | P5 FAIL | Yes |
| 12. `L = 4`, `claim` unchanged (closed-form) | P5 FAIL and C0 FAIL (`(7/2, 29/30)` has no weight) | Yes |
| 13. `n = 12`, `claim` `s(12) >= 19/5` (closed-form) | all pass | Correct: `Σw < 12` and the same C4 prove the weaker `s(12) ≥ 19/5` |
| 14. `outer_side` written `38/10` (closed-form) | P5 PASS: `Fraction` normalises | Correct |
| 15. Float weight `0.01628`; decimal string `"0.01628"`; `direction_steps = 0` | `ValueError` / `ValueError` / `ZeroDivisionError` tracebacks, exit 1 | Refused, but by traceback (defect D2) |
| 16. `angle_limit` negated | P3 FAIL, C2 FAIL (C3 passes with `D < 0`; irrelevant, refused) | Yes |
| 17. `B = 1` | C3 FAIL `1.0023` | Yes: `B < 1` is forced by C3 whenever `D > 0` |
| 18. Negative weight `−100` at `(−5, −5)` | P2 FAIL and C0 FAIL | Yes |
| 19. Zero-weight atom at an asymmetric site | C0 FAIL | Conservative (defect D6) |
| 20. Tight atom split into two entries at the same site | all pass, `426 atoms on 425 distinct sites` | Correct: weights aggregate by site |
| 21. `n = 11.9` | `int()` truncates to 11; verdict printed for `n = 11` | Cannot mislead, but lenient (defect D4) |

Row 9 is the one acceptance I engineered and the one place I refused to take the
verifier’s word. My independent implementation gives the same minimum `50003/50000` and
the same `90546641` cells on that file, and the sampler finds `1.000060`. The acceptance
is therefore mathematically correct: the certificate carries geometric slack (the atom
at `(587491/588940, 587491/588940)`, `0.99754…`, sits `1.6 × 10⁻⁴` inside the corner
square’s far edge at `0.9977`), so translating the atoms by `5 × 10⁻⁷` certifies a
container `10⁻⁶` wider.
The claim made is `19/5`; that a hair more is available is a property of the
certificate, not a hole in the verifier.
The README’s sentence that “any rounding, in either direction, would change the verdict”
is true of the weights (row 3) and not of the positions (rows 9 and 10); it could say
which.

No tampering was accepted wrongly.

## 6. Self-Containment

Verified, not assumed.
The seven files were copied to a directory outside the repository and run under
`env -i PATH=/usr/bin:/bin`, so nothing from the project was importable and no
environment variable leaked; `check.py` uses `sys.executable`, so its subprocesses run
under whichever interpreter started it.
The imports across the four scripts are
`json, random, re, sys, time, bisect, fractions, itertools, operator, subprocess, pathlib, os, tempfile`,
all standard library; `falsify.py` imports `verify` from its own directory.
A grep for `sqpack`, `packing/`, `../` and `sys.path` finds only that one local import
and `check.py`’s own directory.
The package ran to the same verdicts on CPython 3.10.20, 3.11.15 and 3.14.7. The
README’s references to `../certificate-19-5.json` and `../certificate-189-50.json` are
provenance, not dependencies.
Someone with a stock Python and these seven files reaches a verdict.

One provenance note, not a defect: the README’s pasted stranger run names
`/usr/bin/python3` at version 3.11.15, which is this machine’s system interpreter, so
that run was by the package’s author on the same box.
The README already states that no one outside the project has reviewed the result.

## 7. Defects, Ranked

**Threatens the result:** none found.

**Threatens the packaging** (could confuse a careful reader or misdescribe behaviour; no
verdict changes):

- **D1. “The control” misattributed.** README, section “The Verifier”, last sentence
  (“the control below (a container too large for its atoms) shows this one scores the
  cells beyond the atoms’ reach”) and section “What a Sceptic Could Still Object To”,
  second bullet (“the control on a container too large for its atoms”). The `n = 17`
  control is not a container too large for its atoms; its least covered weight is
  exactly `1`. The demonstration meant is the falsification row “container side 4, atoms
  translated”, whose least covered weight is `0`. A reader who takes “control” in the
  README’s own defined sense will look for a `0` in the control’s output and not find
  it.
- **D2. Refusal by traceback.** For a float or decimal rational, `direction_steps = 0`,
  or an atom with fewer than three entries, `verify.py` exits with an uncaught
  `ValueError`, `ZeroDivisionError` or `IndexError` rather than a `REFUSED` line.
  Exit status is 1, so no false acceptance is possible and `check.py` still reports the
  step as failed, but the README’s “the verifier refuses any other form” promises a
  labelled refusal that does not happen.
- **D3. “Nothing short-circuits” overstated.** True of C0 to C4; a failing precondition
  P1 to P5 returns before them (`decide`, line 454). The README should say so.

**Cosmetic:**

- **D4.** `int(record["n"])` and `int(record["direction_steps"])` truncate a non-integer
  silently (`11.9 → 11`); the verdict printed is for the truncated value, so it cannot
  mislead, but a strict integer check is cheap.
- **D5.** The `claim` must spell `L` in lowest terms (`19/5`); `s(11) >= 38/10` is
  refused at P5 although `outer_side` may be written `38/10`. A false refusal only.
- **D6.** A zero-weight atom at a site without a full orbit fails C0
  (`None != Fraction(0)`). Harmless conservatism.
- **D7.** Timing prose disagrees: README “Expect about a minute”, `check.py` docstring
  “Expect about half a minute”.
  Observed 33 s and 44 s on a loaded box.
- **D8.** A direction at which `2h ≥ L` raises instead of being vacuous.
  Unreachable here and conservative.

## 8. What I Could Not Decide From the Package Alone

- **CPython.** The decision rests on `int` and `fractions.Fraction`. I did not verify
  the interpreter; three versions agree, which is evidence of consistency, not of
  correctness. The README says this.
- **The strict inequality.** The README remarks that `s(11) > 19/5` follows by
  compactness and claims only the weak form.
  I did not check the compactness argument; nothing in the verdict depends on it.
- **Novelty.** Whether `19/5` is the first movement since Stromquist 2003 is a claim
  about a corpus, and the README says which corpus and that no arXiv or MathOverflow
  sweep is on record. Out of scope here and candidly stated there.
- **Method independence.** The verifier and my implementation are two programs for the
  same reduction, and I re-derived that reduction by hand.
  A method-distinct check (interval branch and bound over the unit square, or a
  formalisation) would be stronger still; the README lists this as an open objection and
  I agree it remains one.

## Method Notes

Scratch work lived in the session scratch directory `review-t018/` (a copy of the
package, `indep_c4.py`, `attack.py`, `sample_c4.py`, and the logs quoted above) and does
not survive the session; every number it produced is in this document.
The project interpreter `packing/.venv/bin/python3` (3.14.7) was used for all work on
repository code; the system interpreters 3.10 and 3.11 were used only for the package’s
own portability claim, on the copy outside the repository.
Total compute: about eleven full C4 decisions plus two runs of the independent
implementation, under fifteen CPU minutes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
