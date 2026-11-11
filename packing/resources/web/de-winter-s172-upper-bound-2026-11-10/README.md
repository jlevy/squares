# Joost de Winter’s s(172) Certificate at c4e65d0

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/c4e65d0b8c4d32e45bf32a907e8b760502f137af)
at `c4e65d0b8c4d32e45bf32a907e8b760502f137af` (committed 2026-11-10T21:26:23Z), the head
of `main` when it was read, which [issue #946](https://github.com/jlevy/squares/issues/946)
names 47 seconds later.

The folder `n172/` first appeared at `8c0de9d` (21:20:44Z), with a certificate 1.4 × 10⁻⁹⁹
above the same root; `c4e65d0` overwrote it, and that version is pinned by its commit
alone. The four commits between this source’s pin for #939 (`702c7af`, the
[s199 packet](../de-winter-s199-upper-bound-2026-11-09/README.md)) and these add
certificates at 37 counts above 324 under `above324/` and `above324_refined/`. They are
outside this scope and left for triage.

Intake lane L78 (think-2h88) retained it, replayed it and registered it on 11 November
2026 as **T-286, held at V0/C0** for the owner’s RV-3 (think-ruu2), beside #939’s T-285.
The house at 172 stays T-282, and the case record is not touched.

## What the Source Claims

- `n172/n172_witness.yaml` states 172 unit squares by centre and the unit direction of one
  edge, every number an exact rational. Like #939’s witness, it follows Witness/v2’s
  `witness` object without the schema’s envelope. `n172/n172_exact.json` states the same
  packing as `[center_x, center_y, cos, sin]` rows, with the quintic’s coefficients.
  `n172/n172_optimum_300_digits.txt` gives the optimum cut at 300 decimals; the squares
  that can move without changing the side keep their certificate positions.
- **The side.** #946 prints it cut at 56 places, 13.61468985328358057514628890087947061618972730200175769881…,
  and the root README rounds it up at 12, 13.614689853284, which the packet admits.
- **The quintic.** The side lies 1.6 × 10⁻³¹⁹ above the real root near 13.6147 of
  62x⁵ − 4116x⁴ + 107933x³ − 1397031x² + 8918035x − 22427977, which the issue calls the
  arrangement’s exact local optimum. A solution of the contact equations at about 390
  digits closes all contacts with a residual below 10⁻³⁸⁹. The equations have rank 285
  and fix the side to first order, and non-negative contact forces in balance exist (in
  floating point). The polynomial, identified from 108 digits of an earlier 130-digit
  solution, agrees with the 390-digit side to 386 digits. Local optimality has no formal
  proof.
- **The arrangement** is #935’s (T-282: Evan Daniel’s packing, improved by Doğa Özden),
  with no square added, removed or moved to another place in the contact structure. It is
  the core of #939’s packing at 199. The issue calls it the same type of result as T-098
  and says it understands that such results await the RV-3 ruling.
- **The checker.** `verify_exact.py`, in Python’s `Fraction`, is the one checker, written
  for this certificate and not run against this repository’s. It was not run here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of `n172/`,
9 files: 7 retained under [source/](source/) and 2 pinned by digest (`LICENSE`, against the
byte-identical copy the October packet retains, and the figure). `n172/SHA256SUMS` states
the digests of the six other files of `n172/`, and they match. `n172_exact.json` is
stored as deterministic gzip.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `f54ad1048`. The certificate is 2.6345292 × 10⁻¹² below T-282, the house, across its
12-place print (13.614689853284 against …287). It is #939’s core side less 1.36 × 10⁻⁹⁹,
the padding of #939’s certificate. The
[ledger of 11 November](../../../campaign/issue-intake/upper-bounds-939-946-20261111/README.md)
records it as a refinement of T-282’s packing. #939’s certificate already bounded s(172),
but #939 claims 199 only, and the record carries no deletion of an L inside the corpus. So
#946 is the first report at 172.

## The Quintic

Checked exactly by the lane test. The quintic is #939’s, shifted by one, and is
irreducible over Q. Exactly one of its roots lies in [S − 10⁻³¹⁸, S] (a Sturm count), and
S lies between 1.56 × 10⁻³¹⁹ and 1.57 × 10⁻³¹⁹ above it. The certificate proves s(172) ≤
S and nothing about the root.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, through the readers written for
#939’s files: 3 jobs, all 14,706 pairs a job and route, 131 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes. The least wall clearance
is 1.5 × 10⁻³²⁰ and the least pair gap 10⁻³²⁰. `sharp-controls` took it to exact contact
and 1e-30 past it on both routes ([receipts/sharp-controls.json](receipts/sharp-controls.json),
505 CPU seconds), and every control behaved as the module predicts:

- **Wall, pair and near-wall.** The box lowered to the extent (by 1.5 × 10⁻³²⁰), the
  tightest pair (square 20 against 17) closed by its gap of 10⁻³²⁰, and every square moved
  to its near wall: each is accepted at exact contact and refused 1e-30 past it.
- **Enlarged to a pair.** No square can close one pair alone, since the contacts are dense
  at 10⁻³²⁰. Square 20, enlarged against 17, is refused at contact for its shape alone.
- **Enlarged to a wall.** Square 48, a free square 1.088 × 10⁻³ from its wall, is refused
  at contact for its shape, and past contact for the wall as well.
- **Duplicate.** A duplicated square is refused.

The lane stated its expectations before the run, and they held. As at #939, the module
chose the enlarged squares.

## Pose by Pose and Padding

`devtools.measure_identity` wrote [measure/identity-n172.json](measure/identity-n172.json),
and `devtools.contraction_margin` the `contraction-*.json` receipts under
[measure/](measure/):

- **Against T-282.** One to one under the identity. 84 squares move beyond 10⁻⁹ and none
  beyond 10⁻³ (largest 1.414 × 10⁻⁴), and 16 turn by 0.00573 degrees, exactly as #939’s
  core does: the non-load-bearing squares the source moved off their contacts. T-282’s own
  uniform-contraction margin is 2.533458 × 10⁻¹² (1 − λ\* = 2.008 × 10⁻¹³), and the gain
  is 1.0399 of it ([contraction-n172.json](measure/contraction-n172.json)). That is the
  same share as Evan Daniel’s held solve below T-282 (think-wju3).
- **Against #939’s core** (`l-base`), 1.36 × 10⁻⁹⁹ above it. Every square lies within
  2.3 × 10⁻⁹⁹, and the gain is exactly that core’s own margin, 1.0000
  ([contraction-n172-against-939-base.json](measure/contraction-n172-against-939-base.json)).
- **Against Evan Daniel’s held solve** (its view regenerated byte for byte as the s199
  packet says, Git blob `d641e969`). The gain is 1.3615 × 10⁻¹⁹, again 1.0000 of that
  certificate’s own margin
  ([contraction-n172-daniel-held.json](measure/contraction-n172-daniel-held.json)). The
  88 load-bearing squares agree within 10⁻⁹, and the other 84 lie on its flat motions.
- **Its own margin** is 1.56 × 10⁻³¹⁹ (1 − λ\* = 10⁻³²⁰;
  [contraction-n172-own.json](measure/contraction-n172-own.json)). It is the same point
  as #939’s core and as the held solve, with less padding each time.

## The Register

T-286 records the claim, held at V0/C0, S1, with a regularization item naming T-282. The
replay is not entered as evidence and nothing is adopted. Whether a re-certification at
its predecessor’s own padding is a new result is the owner’s RV-3 (think-ruu2). The same
answer settles T-285 at 199 and the held solve at 172 (think-wju3). The stage 4 review is
to be written by a separate blind lane and mapped at C1 when it returns.

## What Is Not Established

- **The root as the local optimum**, and any optimality: not replayed here.
- **Independent review**: none mapped yet.
- **Human oversight**: no record is retained.

## Credit and Licence

The arrangement is Evan Daniel’s packing as Doğa Özden improved it (T-282, #935). The
re-solve and the certificate are Joost de Winter’s, and the issue asks that he be
credited as its improver, the arrangement’s credit staying with Daniel and Özden. The
issue says the local optimization, high-precision solution, rational certificate,
checking and figure were produced with Claude Fable 5.2 (Anthropic) under his direction.
The arrangement starts from this repository’s regularized atlas, so the lineage builds
on this project. The bibliography key is **[de Winter s172 upper bound 2026-11-10]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files.

## Commands

From `packing/`, with the project interpreter; `check-claims` reads the case records as
they stood at `main` `f54ad1048`, and `VIEW` is the held solve’s regenerated view, as in
the s199 packet:

```bash
P=de-winter-s172-upper-bound-2026-11-10
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.contraction_margin --n 172 'T-282=packet:ozden-s172-upper-bound-2026-11-09' \
  --against "#946=packet:$P" --out resources/web/$P/measure/contraction-n172.json
python -m devtools.contraction_margin --n 172 "#946=packet:$P" \
  --out resources/web/$P/measure/contraction-n172-own.json
python -m devtools.contraction_margin --n 172 '#939=l-base:packet:de-winter-s199-upper-bound-2026-11-09' \
  --against "#946=packet:$P" --out resources/web/$P/measure/contraction-n172-against-939-base.json
python -m devtools.contraction_margin --n 172 "daniel-held=witness-center-basis:$VIEW" \
  --against "#946=packet:$P" --out resources/web/$P/measure/contraction-n172-daniel-held.json
python -m devtools.measure_identity --n 172 "#946=packet:$P" \
  'T-282=packet:ozden-s172-upper-bound-2026-11-09' \
  '#939=l-base:packet:de-winter-s199-upper-bound-2026-11-09' \
  "daniel-held=witness-center-basis:$VIEW" \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-172-regularized.yaml.gz' \
  --out resources/web/$P/measure/identity-n172.json
```

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n172/n172_exact.json.gz` | upstream | `1f478e01ef7497c4a3f331b69d36b01f3925ac88` | `cb0a29ac42b4631c56d2243f02ea4430a17c1e627574f7fb48bbc6ecba983afb` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
