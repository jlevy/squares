# E. Summins’ Simple-Square Stratification Series at 651a9a5

Issues [#521](https://github.com/jlevy/squares/issues/521) to
[#527](https://github.com/jlevy/squares/issues/527), filed between 2026-10-12T04:12:24Z and
04:12:50Z by Esummins, carry an eight-note outreach series from the n = 11 lab of
E. Summins (PI) at
[Esummins/packing](https://github.com/Esummins/packing/tree/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb)
`651a9a54688341880e9c0dc9fcfc19f2c04cd3cb` (tree `62ae9dc3bd990436b35cb9c6719d491b6047a7be`,
committed 2026-10-12T04:11:54Z, the commit every issue names). The series index is
`writeup/outreach/00-README.md`, and its section 4 is the manifest this packet follows.
Nothing in the series claims a bound: the n = 11 value and uniqueness are left to T-060
and T-112, and T-037 is replayed, not claimed.

| Issue | Note | What it is | Bead |
| --- | --- | --- | --- |
| #521 | `08-t037-replay.md` | A third party’s replay of Kleddamag’s v1.0.2 certificate (T-037): the exact Python sweep re-run in full, 12,028 of 12,028 rows, 0 differing; a spot check in the lab’s own arithmetic | think-6t6q |
| #522 | `01-stratification-program.md`, `07-timeline.md` | The stratification as a proof strategy; the n = 11 census (a Lean theorem) and scoreboard (52 of 52 k5/k6 classes empty on [191/50, 969271/250000]); a Lean layer on three named axioms | think-3m7d |
| #523 | `06-climb-17-19.md` | A 2,500-class census at the n = 17 and n = 19 windows, 632 with four corners; the n = 17 descent (k = 16 and 15 dead at the root, k = 14 67 of 68); a compute request | think-j891 |
| #524 | `04-simple-square-conjecture.md` | Conjecture ONE-FLUSH(n), its equivalences, the extremal reduction to LOCKED-CROWD-FREE(n), refuted routes, measured support | think-s1ru |
| #525 | `02-ladder-requirements.md` | Lemma SLOT-CROWD and Theorem FC for any n; the forced-cell traction finding; a refuted cascade rule; four local lemmas | think-3nc2 |
| #526 | `03-k0-status.md` | k = 0 at n = 11: theorems, ten refuted routes with witnesses, measured facts, the open chains | think-tnfo |
| #527 | `05-toolkit.md` | The geometry-before-LP toolkit for stratum trees, its leaf rules, kernels and measured speed-ups | think-kok7 |

The lab says every campaign, program, certificate, Lean file and note “were produced by AI
agents (Claude, Anthropic) under the PI’s direction and readings”, and that the executable
evidence and stated trust bases, not the prose, are offered for review. The credit name is
E. Summins (PI), n = 11 lab.

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless, shallow, sparse clone checked
out at the pin (`--filter=blob:none --depth 1`, fetched 2026-10-12T08:12Z, the sparse
checkout widened at 08:30Z), from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the
acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
856 files, 28,037,432 bytes in scope, of which 548 files (14,509,766 bytes) are retained
under `source/` and 308 (13,527,666 bytes) are pinned by digest only.

The pinned tree is much larger than the scope: 71,035 files and about 20.75 GB, 68,442 of
them under `attempts/`. The scope is the manifest in `00-README.md` section 4, read as the
series cites it:

- the series, `writeup/outreach/` (ten files), and the lab’s write-up, status sheet and
  compute plan under `writeup/`;
- the lemma corpus `docs/proofs/` (93 files), `docs/residue_ledger.md` and
  `docs/shadows/STATUS.md`;
- the Lean readable layer: `lean/AUDIT.md`, the package’s `lean-toolchain`,
  `lakefile.toml`, `lake-manifest.json`, `Main.lean`, `TopLevel.lean` and `Statements/`
  with `Statements/Open/` (71 files); the core library, the Corpus library and the stdlib
  `PackingCert` project are pinned by the commit;
- `certs/`: the measure certificates at 3.80, 3.81 and 3.82, Trump’s exact data, the octic
  isolation, the CIDL identity, the tube certificates and the stdlib verifiers;
- `attempts/REGISTRY.md`, the A53 census files, the A56 scoreboard, the frozen verifiers
  (`verify_case.py` v1, v3, v4, v5 and `verify_swap232.py`), the live engine
  `attempts/A211-coarse-tree/code/`, the A202, A203, A213 and A214 code and notes, the
  A215 benchmark, the A221 note, the A238 and A241 notes and summaries, the A243 census,
  verdicts, code and notes, all of `attempts/A242-replay-31-8/`, the A217 witnesses, all
  of `attempts/A226-one-flush/`, and the A275 brief.

Pinned by digest and not retained, each with its reason in the declaration: `LOG.md` (the
1.1 MB notebook), the 248 gzipped spine certificates of A243 (8.8 MB), three raw
engine-row files (`rows211_raw.jsonl`, `bench238.jsonl`, `raw211_n17.jsonl` and its probe
file), the uncited `certs/a82/`, `certs/uladder/` and one unavoidable-set certificate, and
the committed byte code under `certs/__pycache__/`. The tube certificates’ verifier,
`certs/verify_tube.py`, was retained by the import lane and is pinned by digest since
the records layer of 12 October: one of its verdict format strings, `checker %s => %s`,
reads as a JavaScript arrow function to `devtools.check_no_embedded_js`, which scans every
tracked Python file and admits no exception. The galleries under
`docs/residue_map/` and `docs/shadows/`, the figures, the tree records and the logs are
pinned by the commit alone, as the manifest itself says they may be.

The repository states its licence in the pinned commit, which added it: `LICENSE` at the
root says code is MIT (`LICENSE-MIT`) and documents and data are CC BY 4.0
(`LICENSE-CC-BY-4.0`), by the PI on 2026-10-11. GitHub’s API reports NOASSERTION because
the root file is a pointer. The retained files are copied under those terms.

One commit follows the pin at the read, `eb3ae15` (2026-10-12T04:13:07Z), which adds only
`writeup/outreach/POSTED.md`.

## What Was Checked Here

Only the cheap checks of a stage 1 triage; nothing was replayed in the record’s sense.

- **#521, the join keys.** The lab’s `ext/PIN.json` names Kleddamag’s certificate at
  SHA-256 `57e9927d…cd44458` and the release’s `evidence/portable/python.json` at
  `68b6f360…7bc0`; both equal the copies the
  [external-square-certificates-2026-09-22](../external-square-certificates-2026-09-22/README.md)
  packet retains. The lab’s `replay242.json` totals (minimum 999962528 at row 11962,
  budget 10999479944, surplus 107864, 86,299,918 slabs, 511,649,694,680 cells) agree with
  the source replay recorded here (`E-n011-kleddamag-3875-source-replay`).
- **#521, the spot check re-run.** `code/spot242.py` and `code/rows242.py` were read
  first (no network, no writes outside `results/`, a Windows-only priority call caught by
  `try`). `spot242.py` ran here from a scratch layout outside both repositories, against
  the retained certificate and evidence file, with CPython 3.14.7 and the lab’s arguments
  `2000 1000 242`: `all_pass` true, 3,240 poses, 0 failures, minimum charge 1000047518,
  M = 10999479944, 11Γ − M = 107864, and its `spot242.jsonl` byte-identical to the lab’s
  retained rows (SHA-256 `256a47d4…8bcbf8f`). It took 67.1 s at a load average of 18 on
  four cores (10.7 s at the lab). [receipts/spot242-rerun-2026-10-12.json](receipts/spot242-rerun-2026-10-12.json)
  is the output and [receipts/spot242-rerun-2026-10-12.sha256](receipts/spot242-rerun-2026-10-12.sha256)
  the digests of what ran. A sample of 3,240 poses is a diagnostic, not a decision; the row
  sweep itself (8,089 CPU-s at the lab) was not re-run, since the source replay here
  already decides it.
- **#522 and #523, the counts.** `scoreboard.json` holds 52 rows, each FULL on
  [191/50, 969271/250000] (4 by the single-corner transfer theorem, 48 by certificate).
  `census243_n17.json` and `census243_n19.json` hold 2,500 rows each with the per-k counts
  the note gives and 632 four-corner classes each; `verdicts243_n17.jsonl` holds 120 rows:
  k = 16 DEAD 17, k = 15 DEAD 35, k = 14 DEAD 67 and ALIVE 1. No k = 13 row is committed
  at the pin, and `certs/n17/` holds 248 files where the note says 276.
- **The Lean layer, read not built.** Toolchain `leanprover/lean4:v4.34.0-rc1` with
  Mathlib `v4.34.0-rc1` at `de5ce8a9`; no `sorry` in `Main.lean`, `TopLevel.lean` or
  `Statements/`; the three main theorems rest on the standard axioms, three project axioms
  (`stratum_kill`, `trump_residual`, `a22_exact_structure`) and six `native_decide`
  evaluations, as `AUDIT.md` (generated 2026-10-07) tabulates; `Statements/Open/` declares
  93 axioms in all for the open-lemma layer. A cold build here is priced at one to three
  hours of wall and was not run.
- **The verifier digests.** The notes quote `verify_case.py` at SHA-256 `521cb01fe656…`
  and `verify_measure.py` at `2a735939d67f…`; those are the digests of the files with CRLF
  line endings. The committed blobs are LF and digest `1574ddbdcd57e642…` and
  `87fa3d31cb91c7ef…`, which the manifest records. The join key is line-ending dependent.

What this packet does not do: no certificate here enters the register, no
`upper_bound_reports` record exists (the series holds no upper bound), and no stratum
kill, census row or Lean theorem was decided here. The triage, the claim map and the
priced review routes are in the beads named above.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/attempts/A241-row-cascade/results/rows241.json.gz` | upstream | `0346a6d288dff0157d6057693d151bd00483801f` | `9c7fccf03f26667c02de289cf3132c164e7f9fa6e64ae98391767a6025d13dbf` |
| `source/attempts/A242-replay-31-8/results/replay242_shard0of2.jsonl.gz` | upstream | `237cbea0310314c835308cba82bf2fcaed43a6dc` | `375fb4d3536590e905da0165acd1690abba5ca7b3bc13d3372a77281eafc516d` |
| `source/attempts/A242-replay-31-8/results/replay242_shard1of2.jsonl.gz` | upstream | `56e913566d10ea97cc9c10b1312b368003eee93d` | `c146e923520be05362940a02a5bbf6968ed42c31f67f01f346841179c7590ad5` |
| `source/attempts/A242-replay-31-8/results/spot242.jsonl.gz` | upstream | `c4df785902671db569c70fe45cfcc97870b564f2` | `256a47d4ba2f491842880b322ea86218ea8a6ac84ce9970c486710539f38bcb9` |
| `source/attempts/A243-climb-17-19/results/census243_n11.json.gz` | upstream | `98788494c2f4ace44d7a7e2d0e38742af1c259fd` | `bcc89584c8de050ce715f88ad46835bf28e695fe8577fb44ed938bb10cd274a2` |
| `source/attempts/A243-climb-17-19/results/census243_n17.json.gz` | upstream | `db3e9ccb7f1b7da9773653bff68e23d968c0dbc7` | `f4be17bd6386eb54354aad1aa2a2386671f303cb48a0acfaf29c4c5bfa8e684c` |
| `source/attempts/A243-climb-17-19/results/census243_n19.json.gz` | upstream | `f698f7a17d6406cc72b14a40f7f3cac3d6ba5034` | `4e236abd32d5555cf2a9a59fb411bf938d1f17f0d65687e449824cef787da794` |
| `source/attempts/A53-simple-strata/results/name_to_slots.json.gz` | upstream | `a14ee42177c116fc4f7d576f1a981dcbc67eb63c` | `9eb801d95fe2894a8b6864657089cd530a7063faa347ddf1aec7badeedf6d7ba` |
| `source/attempts/A53-simple-strata/results/skeletons.json.gz` | upstream | `a42793a663ad69068b330483bc5f94f1d09e20c1` | `9f3c180cec39ae1c59bb8cfadb36d751db39d8f580be6ca3cbd74c671c7177f9` |
| `source/attempts/A53-simple-strata/results/skeletons_young.json.gz` | upstream | `37c27abe45698fda14fb9e88b94ecdfb267667af` | `b0f7df7bef8ba43f4ed5033ec9ca10459220ca28ca96be75ade4d427ea9706e5` |
| `source/attempts/A56-sparametric/results/scoreboard.json.gz` | upstream | `36c014b6c0efc84f4ed610720269cae71a88ca34` | `e92f1c2516a388f0051e3cf7abad6eb107db104008cf1975683c1f45a2b28579` |
| `source/certs/measure_certificate_3.80.json.gz` | upstream | `59e25a385ba23dfa4353fc11d03fd94778d0cb65` | `275b3518ca1c5ad45c73ea8113066ceb62dda1065427ff15a2b96ae6e55fb9d1` |
| `source/certs/measure_certificate_3.81.json.gz` | upstream | `f12a512cb4217eba68b3af9c285403a592e4275e` | `5bafd581f004838bfaba9486aae7e2b65248f5cb164e3635c1077a12888dadc9` |
| `source/certs/measure_certificate_3.82.json.gz` | upstream | `7462ecb029317ab0a628fe4d79d40ee94e70470d` | `70a6cd820c4505851adc6f0047167e05a69156273d95ca5548e7111b65a7478e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
