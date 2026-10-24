# Kevin Fang’s Lean Formalization of His Theorem 1, Pinned 2026-10-18

[TheSnakeFang/squarepack-lean](https://github.com/TheSnakeFang/squarepack-lean) is Kevin
Fang’s Lean 4 proof of Theorem 1 of his note, $s(n^2 - n + 1) < n$ for every $n \ge 15$,
with its quantitative form at side $n - 1/10000$, and of the two single-step bounds of his
Theorem 2, over Evan Daniel’s common specification `Spec.lean`. The record holds both
theorems as `T-163`, tracked on
[jlevy/squares#603](https://github.com/jlevy/squares/issues/603); Fang’s comment
[6255103888](https://github.com/jlevy/squares/issues/603#issuecomment-6255103888) of 18
October announced this pin, and the note,
[draft v0.9](../fang-excess-note-2026-10-19/README.md), cites it as [FanL26]. Bead
`think-494l` owns this retention.

Its Frontier key is **[Fang excess Lean 2026-10-18]**. Evan Daniel’s separate Lean proof
of both theorems is the
[18 October Daniel Lean packet](../evand-fang-ryu-lean-2026-10-18/README.md) (`T-236`).
Nothing here has built either one.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/TheSnakeFang/squarepack-lean> |
| Revision | `947bdaec40ead1105cfb00c2968e2484b7d1b40b`, tree `d4c36ad80b4f40557e479a5e6e4a2635116d31fb`, the head when read: “MIT licence; README points at the public certificate bundle” |
| Committed | 2026-10-18T20:41:46Z (13:41:46 by the author’s clock, `-07:00`), by Kevin Fang |
| History | `ab42135` 2026-10-13T08:25:22Z, the vendored specification and the integer checker with its soundness; `8bffb1f` 11:12:59Z, the rectangles, `glue`, the 18 base certificates and Theorem 1; `f09d710` 11:37:46Z, the $R'$ step of Theorem 2; `837eca1` 12:49:17Z, README and STATUS. The pin adds `LICENSE` and changes one line of `README.md`; the note names `837eca1` as the proof sources |
| Licence | MIT, “Copyright (c) 2026 Kevin Fang” (`LICENSE`); the vendored `Spec.lean` and `ExactPack.lean` and `certs/daniel/` are Evan Daniel’s, MIT |
| Retrieved | 2026-10-24T04:57Z, a blobless clone checked out at the pin |
| Scope | The whole tree: 141 files, 2,379,100 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 130 files, 2,181,052 bytes, byte-identical under [`source/`](source/) |

## Credit and AI Assistance, as the Source States Them

Kevin Fang is the author. `Sqlean/Vendor/NOTICE` says `Spec.lean` and `ExactPack.lean`
are “taken from Evan Daniel’s https://github.com/evand/square-packing, commit
29d0cee87c1d717f7b4497b8fb0ee17ac9d0087d”, and that only `ExactPack.lean`’s import line
was changed; `certs/daniel/NOTICE` credits Daniel’s certificates. The README’s
certificate table names de Winter’s packing of 211 and Daniel’s certificates of 241, 273
and the $m^2 - m$ bases. The pin’s commit carries a Claude (Anthropic) co-author trailer.
Fang states the Lean project’s AI assistance in his
[comment of 18 October 2026 on issue 603](https://github.com/jlevy/squares/issues/603#issuecomment-6255103888),
which announced this repository:

> The search, checkers, bundle and Lean project were written with Claude as a coding and
> research agent, directed and reviewed by me.

The note says of the formalisation only that it “reuses Evan Daniel’s specification and
certificate lemmas (MIT)”; its acknowledgements, quoted in the
[note packet](../fang-excess-note-2026-10-19/README.md#credit-and-ai-assistance-as-the-source-states-them),
say the search software, the verifiers, the gluing program and the bundle were written
and run with Claude (Anthropic), directed and reviewed by the author.

## What Is Retained

`devtools.acquire_source` wrote [`source/`](source/) from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin, and [acquisition/sources.json](acquisition/sources.json) is the
record.

Retained byte-identical at their upstream paths:

- **the hand-written Lean**: `Sqlean.lean`, `Sqlean/Main.lean` (`base`, `small`, `step`,
  `main`, `theorem1`), `Sqlean/Theorem2.lean` (`stepR`, `stepR'`, `packs_j16`,
  `packs_j21`, `jExc`, `main2`, `theorem2`), `Sqlean/Glue.lean` (`glue`, Lemma 3),
  `Sqlean/Rect.lean`, `Sqlean/CheckCore.lean` (the integer checker, core Lean only),
  `Sqlean/Check.lean` (`check_sound`), the axiom probe `Sqlean/Axioms.lean`, and
  `Sqlean/Vendor/ExactPack.lean` with `Sqlean/Vendor/NOTICE`;
- **the generated Lean**: the 17 piece modules `Sqlean/Pieces/*.lean`, each a `PacksR`
  fact at the side minus $1/10000$, and the 82 data and chunk modules under
  `Sqlean/Data/`, the integer-encoded certificates and one `decide +kernel` theorem per
  chunk, 1,162,331 bytes, which `scripts/gen_all.sh` regenerates from `certs/` and the
  kernel checks as they stand;
- **the certificates they encode**, `certs/ours/`: Fang’s eleven, the rectangles
  `r17x16_n0257` and `r22x21_n0443` and the square packings `n0308` to `n0651`, with
  `certs/daniel/NOTICE`. Less their `#` comment lines, each is the copy this repository
  already retains, in the
  [10 October two-wedge packet](../fang-two-wedge-certificates-2026-10-10/README.md)
  (`n0308`, `n0343`), the
  [direct-certificates packet](../fang-direct-certificates-2026-10-13/README.md)
  (`n0381` to `n0651`) or the
  [13 October packet](../fang-excess-theorem-2026-10-13/README.md) (the rectangles), as
  `diff <(grep -v '^#' A) <(grep -v '^#' B)` shows for all eleven. The comment line
  differs, and `r22x21_n0443` has none, so the files are not byte-identical and are kept
  here;
- **the build pins and the project’s own notes**: `lakefile.toml`, `lake-manifest.json`
  (Mathlib `0df444a360eaa60ab8c11dca51a86af692955474` at input `v4.33.1`), `README.md`,
  `STATUS.md`, `LICENSE` and `.gitignore`; and **the scripts** `scripts/gen_all.sh`,
  `scripts/fetch_211.sh` and `scripts/certinfo.py`.

Pinned by digest, each byte-identical to a copy this repository retains, compared by
`acquire_source`:

| Upstream path | Retained in |
| --- | --- |
| `Sqlean/Vendor/Spec.lean`, Git blob `fa4a6248` | [7 October Daniel packet](../evand-exact-and-local-reports-2026-10-07/README.md), `source/s12/lean/Sqpack/Spec.lean` |
| `lean-toolchain`, `leanprover/lean4:v4.33.1` | the same packet, `source/s12/lean/lean-toolchain` |
| `Sqlean/Vendor/LICENSE-evand`, `certs/daniel/LICENSE` | [7 October batch packet](../evand-batch-105-130-2026-10-07/README.md), `source/LICENSE` |
| `certs/daniel/n-110.cert` to `n-273.cert`, six files | [5 October Daniel packet](../evand-square-packing-2026-10-05/README.md), `square-packing/s12/search/exact/batch/certs/` |

Pinned by digest and not retained: `scripts/gen_cert.py` (8,775 bytes), the
certificate-to-Lean generator. Its Lean strings, such as `fun i hi => by`, are what this
repository’s embedded-JavaScript gate reads as arrow functions, and the gate admits no
exception, as for `lean_cert.py` in the Daniel Lean packet. A rebuild needs it only for
the 211 piece below.

**Not in the tree.** `Sqlean/Data/N211.lean`, its chunks and `Sqlean/Pieces/N211.lean`,
the base case $n = 15$, are gitignored: de Winter’s packing carries no licence, so
`scripts/fetch_211.sh` downloads Daniel’s certificate of it from `evand/square-packing`
at `29d0cee`, checks its SHA-256, `ca491d50bb17c976…`, and generates the modules with
`gen_cert.py`. The certificate with that digest is retained in the
[5 October Daniel packet](../evand-square-packing-2026-10-05/README.md), at
`square-packing/s12/search/exact/batch/certs/n-211.cert`.

**The closure.** [`receipts/lean-closure.json.gz`](receipts/lean-closure.json.gz),
written by `devtools.lean_closure` from the Git objects at the pin with the targets
`Sqlean` and `Sqlean.Axioms`, follows every import through the project’s own modules:
109 modules, 1,237,547 bytes: the ten written by hand, the two vendored from Daniel among
them, the 17 piece modules and the 82 data and chunk modules, with `Mathlib` the only
import outside them (one import line, in `Spec.lean`). It counts no `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`,
`unsafe`, `debug.skipKernelTC`, `+native`, `native := true`, `reduceBool`, `reduceNat`
or `trustCompiler` in their code, comments removed. It lists one module as missing,
`Sqlean.Pieces.N211`, the gitignored 211 piece. A token count is not a parse and not a
build: it says what the text holds, and the axiom set stays the source’s report until a
build prints it. From `packing/`, with a blobless clone of the source as `CHECKOUT`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.lean_closure CHECKOUT \
  --commit 947bdaec40ead1105cfb00c2968e2484b7d1b40b --root . Sqlean Sqlean.Axioms \
  --source-url https://github.com/TheSnakeFang/squarepack-lean --json OUT
```

## The Statements

`Packs` and `minSide` are Daniel’s, from `Spec.lean`: `Packs n s` holds when $n$ closed
unit squares, images of $[-1/2, 1/2]^2$ under a rotation and a translation, lie in
$[0, s]^2$ with pairwise disjoint interiors, and `minSide n = sInf {s | Packs n s}`.

```lean
theorem UnitSquarePacking.theorem1 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + 1) < n
theorem UnitSquarePacking.main (n : ℕ) (h : 15 ≤ n) :
    Packs (n ^ 2 - n + 1) ((n : ℝ) - 1 / 10000)
theorem UnitSquarePacking.theorem2 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + jExc n) < n
def jExc (n : ℕ) : ℕ := max ((n + 1) / 16) (1 + 2 * ((n - 15) / 21))
```

`main` is a strong induction on $n$: `base` for $15 \le n \le 26$ from the kernel-checked
pieces, 307 from 308 by `packs_of_le`; `small` and `step` for $27 \le n \le 30$; and
`step`, Lemma 3 with $R$, from $n - 16$ above. `theorem2` takes the larger of
`packs_j16` ($R$ steps only) and `packs_j21` ($R'$ steps on top of `main`). `glue` is the
note’s Lemma 3 on `PacksR` for any real $d$ with $0 \le d \le b, b'$, `a ≤ n`, `a' ≤ n`
and `n - a' ≤ a - d`. Each piece is `check_sound` applied to `decide +kernel` facts about
the literal data.

The [note packet](../fang-excess-note-2026-10-19/README.md#the-statements-against-t-163)
compares these statements with `T-163`’s claim, the note’s theorems and Daniel’s:
`theorem1` is Theorem 1, `main` is stronger, and `theorem2` is Theorem 2 with an excess of
$F(n)$ or $F(n) - 1$: equal to $F(n)$ for $15 \le n \le 51$, then one short wherever
$n - 15$ leaves 16 to 20 on division by 21 ($n = 52$–56, 73–77, 94–98, …), where mixing
the two steps gains, and equal otherwise.

**What the source says of its axioms and build.** The README and `Sqlean/Axioms.lean`:
`#print axioms` for `theorem1`, `main` and `theorem2` gives
`[propext, Classical.choice, Quot.sound]`, with “No `sorry`, no `native_decide`, no new
axioms”. A clean build on top of the Mathlib cache took “34 min wall, 373 s user + 392 s
sys” on a shared 10-core machine, and the 18 certificates about 3.2 CPU-minutes of
kernel time. No build log or axiom output is published.

## The Build Plan, Priced

From the retained files staged as the tree, with `scripts/gen_cert.py` fetched at the pin
and checked against the manifest, and the 211 certificate staged from the 5 October
packet:

```sh
lake exe cache get                                # Mathlib 0df444a3, about 6.5 GB
python3 scripts/gen_cert.py certs/fetched/n-211.cert N211 --W 15
lake build Sqlean Sqlean.Axioms                   # accept only the three standard axioms
```

| Item | Estimate |
| --- | --- |
| Toolchain | `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`, the pins of Daniel’s Lean (`think-dgrc`) and of the `s(13) = 4` and Bentz builds made here, so one cache serves them all; about 9 GB of disk with the toolchain |
| CPU | about 0.25 CPU-hours: the source’s 765 CPU-seconds on top of the cache, nearly all of it Mathlib imports, and 3.2 CPU-minutes of kernel checking; an estimate from the source’s report, not a receipt |
| Memory | at most about 2.9 GB for one declaration, by `STATUS.md` |

It is under every cap, and this host cannot run it: on 24 October it had 4.7 GB of free
disk.

## Limitations

- **Nothing was built or run here.** The axiom set and the build times are the source’s
  report.
- **The mixed-step Theorem 2 is not formalised here.** The note and the certificate
  repository’s README say so; this repository’s README says “Theorems 1 and 2”.
- **The generated modules are trusted to nothing.** The kernel checks the data as it
  stands, and whether each data module encodes its certificate is for the review or a
  rebuild to read.
- **No review has read the proof.**

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `receipts/lean-closure.json.gz` | receipt | `e3e00e1ec9230fe76492869c32973228ba216520` | `f4d3a3c23f46849a219541dd32d1711618c485371d782ee82cfc07e79e4fb227` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
