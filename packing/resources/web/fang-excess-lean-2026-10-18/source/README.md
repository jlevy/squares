# squarepack-lean

Kernel-checked Lean 4 proof of Theorems 1 and 2 of the note "Packing n² − n + 1 unit squares in a
square of side less than n" (certificates and note: https://github.com/TheSnakeFang/squarepack-certs), in Evan Daniel's specification
(`Sqlean/Vendor/Spec.lean`, unchanged: closed unit squares, any rotation, inside `[0, s]²`,
pairwise disjoint interiors; `minSide n = sInf {s | Packs n s}`).

```lean
theorem UnitSquarePacking.theorem1 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + 1) < n
theorem UnitSquarePacking.main (n : ℕ) (h : 15 ≤ n) :
    Packs (n ^ 2 - n + 1) ((n : ℝ) - 1 / 10000)
theorem UnitSquarePacking.theorem2 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + jExc n) < n
-- jExc n = max ((n + 1) / 16) (1 + 2 * ((n - 15) / 21))
```

`#print axioms` (`Sqlean/Axioms.lean`) for all three: `[propext, Classical.choice, Quot.sound]`.
No `sorry`, no `native_decide`, no new axioms; the certificates are checked by `decide +kernel`.

## Build

```sh
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
lake exe cache get            # Mathlib v4.33.1 oleans (~6.5 GB in .lake/packages/mathlib/.lake)
./scripts/fetch_211.sh        # de Winter's 211 (no licence, so fetched + hashed, not committed)
lake build Sqlean Sqlean.Axioms
```

`scripts/gen_all.sh` regenerates every other data file byte for byte from `certs/`.

Clean build of this project on top of the Mathlib cache (MacBook, 10 cores, 16 GB, other jobs
running at load ~13, oleans on an external SSD): **34 min wall, 373 s user + 392 s sys**. Nearly
all of the wall time is importing Mathlib (each Mathlib-importing file takes 1.5–5 min wall here
for ~10 s of CPU). The kernel checks of all 18 certificates together take about **3.2 CPU-min**.

## Layout

| file | what |
|---|---|
| `Sqlean/Vendor/{Spec,ExactPack}.lean` | Daniel's specification and `packs_of_cert` (MIT, `Sqlean/Vendor/NOTICE`) |
| `Sqlean/Rect.lean` | `containerR`, `PacksR`, `InBoxR`; `disjoint_of_far` (centres > √2 apart); `packsR_of_cert` (rectangles, far-pair shortcut) |
| `Sqlean/CheckCore.lean` | the checker, core Lean only (no Mathlib): `unitOK`, `boxOK`, `farOK`, `sepOK`, `pairOK`, `rowOK`, `headsOK`, `sortedX` |
| `Sqlean/Check.lean` | soundness: `check_sound`, `headsOK_chunks` |
| `Sqlean/Glue.lean` | `PackIn`, translation, integer blocks, `packIn_sigma`, `packs_of_le`, `packs_mono`, `minSide_le_of_packs`, **`glue`** (Lemma 3), `glue_sq` |
| `Sqlean/Data/<P>.lean`, `Sqlean/Data/<P>/Chk*.lean` | generated: certificate data, and one `decide +kernel` theorem per chunk (no Mathlib) |
| `Sqlean/Pieces/<P>.lean` | generated: `PacksR n (W − 1/10000) (H − 1/10000)` for each certificate |
| `Sqlean/Main.lean` | `base`, `small`, `step`, `main`, `theorem1` |
| `Sqlean/Theorem2.lean` | `stepR`, `stepR'`, `packs_j16`, `packs_j21`, `main2`, `theorem2` |
| `scripts/gen_cert.py` | certificate → Lean (with an exact Python mirror of the checker that must pass first) |

## The checker

A certificate line `x y t` (rationals) becomes integers `⟨X, Y, C, S, N⟩` with `x = X/D`, `y = Y/D`
(`D` the lcm of the coordinate denominators) and `(cos θ, sin θ) = (C/N, S/N)`, `C = q² − p²`,
`S = 2pq`, `N = q² + p²` for `t = p/q`. All tests are integer inequalities:

* `unitOK`: `C² + S² = N²`, `N > 0`;
* `boxOK`: the four corners in `[0, Wn/Sd] × [0, Hn/Sd]`, here always `[0, n − 1/10000]` (or
  `(17 − 1/10000) × (16 − 1/10000)` for the rectangle), not the certificate's own header side;
* per pair: `farOK` (`ΔX² + ΔY² > 2D²`, proved sound by `disjoint_of_far`) or a separating side
  of either square (`sepOK`: one test per side covers all four corners,
  `Ni Nj D + D(|u| + |v|) ≤ 2 Nj (A ΔX + B ΔY)`, sound via Daniel's `disjoint_of_sepSide`);
* the squares are sorted by `X` (`sortedX`, checked) and each row stops at the first square more
  than √2 to the right (`cutX`), so only ~25–35 partners per square are touched.

Nothing generated is trusted: the soundness theorem holds for any data, and each chunk is a
kernel evaluation of the checker on the literal data.

## Certificates used

| piece | file | side used |
|---|---|---|
| n = 15 (211) | Daniel's `n-211.cert` of de Winter's packing (sha256 `ca491d50…`) | 15 − 10⁻⁴ |
| n = 16, 17 (241, 273) | Daniel's `n-241`, `n-273` | 16, 17 − 10⁻⁴ |
| n = 18 (307) | our `n0308.cert`, one square dropped in Lean | 18 − 10⁻⁴ |
| n = 19..26 | our `n0343` … `n0651` | n − 10⁻⁴ |
| m² − m, m = 11..14 | Daniel's `n-110`, `n-132`, `n-156`, `n-182` | m − 10⁻⁴ |
| R | our `r17x16_n0257.cert` | (17 − 10⁻⁴) × (16 − 10⁻⁴) |
| R' (Theorem 2 only) | our `r22x21_n0443.cert` | (22 − 10⁻⁴) × (21 − 10⁻⁴) |

All gluings are at the single squeeze `d = 1/10000`, so every composite has side exactly
`n − 1/10000`.

## Lemma 3 as proved

```lean
theorem glue {nA nB a b a' b' n : ℕ} {d : ℝ} (hA : PacksR nA (a - d) (b - d))
    (hB : PacksR nB (a' - d) (b' - d)) (hn : n = b + b') (hd : 0 ≤ d) (hdb : d ≤ b)
    (hdb' : d ≤ b') (ha : a ≤ n) (ha' : a' ≤ n) (hc : ((n - a' : ℕ) : ℝ) ≤ a - d) :
    Packs (nA + (n - a) * b + (n - a') * (n - b) + nB) (n - d)
```

The four pieces sit in boxes with pairwise disjoint interiors (`packIn_sigma` over `Fin 4`); the
integer blocks are axis-parallel squares at half-integer centres (`packIn_grid`).
