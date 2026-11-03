# Doğa Özden’s s(94) ≥ 1993/200 at 9d76ad5

This packet retains
[kenaznia-doga/s94-lower-bound](https://github.com/kenaznia-doga/s94-lower-bound/tree/9d76ad5549e99e952c899462b36d2bd765517969)
at `9d76ad5549e99e952c899462b36d2bd765517969` (committed 2026-11-03T01:19:36Z, the
repository’s one commit), which issue
[#890](https://github.com/jlevy/squares/issues/890) asks to register.
The issue and the repository were prepared and posted on Doğa Özden’s behalf by his AI
agent, which uses the GitHub account `kenaznia-doga`.

## What the Source Claims

- `certificate/n94_L9965.json.gz` proves $s(94) \ge 1993/200 = 9.965$. It is Hiroaki
  Hosono’s `mixed_n94_L995` rectangle measure (T-091, retained by the
  [wand125-mixed-bounds-evening-2026-10-04](../wand125-mixed-bounds-evening-2026-10-04/README.md)
  packet) with every coordinate multiplied by $\lambda = 1993/1990$ and the masses
  unchanged: 853 rectangle orbits of total mass $9399999/100000 < 94$, core side
  $B = 19884161/19900000$ (Hosono’s $9977/10000$ times $\lambda$), on a net the file
  declares (`proof_net`) of 600 half-angles of step $83/120000$, last tangent
  $49717/120000$, with $B(1 + D) = 2387749705363/2388000000000 < 1$.
- `tools/rescale.py` regenerates the certificate from Hosono’s `candidate.json`, and
  `verify.sh` regenerates it, checks both stated digests, builds this repository’s
  `sqverify-fast` at `e6e8d577` and runs it.
- `receipts/` holds the author’s two complete runs of that `sqverify-fast`, unmodified:
  rustc 1.98.0 (crate source `d97758bb…`) and rustc 1.93.1 with only the
  `rust-version` line removed, each VERIFIED at all 600 directions, least certified bound
  1.0000000000314, 296,805,699 nodes, 7,887 and 7,985 CPU-seconds.
- `second-checker/` is an exact-integer branch and bound that the source says an OpenAI
  Codex agent wrote for the review of this claim from `sqverify-fast`’s `SOUNDNESS.md`
  prose and not its source, with its full run (600 of 600 VERIFIED on Apple arm64,
  4,801 CPU-seconds) and the same Codex agent’s review of the argument, `GRADE.md`
  (verdict SOUND), an AI review and no human one, whose mutants (masses times 0.998, the
  heaviest orbit removed, $L = 9.975$) are refused with exact counterexamples.
  Its “supplied checker” is the author’s lab’s own floating-point checker, which the
  source does not offer as evidence, not `sqverify-fast`.
- `notes/n31-negative/` records the same move refused at $n = 31$: Hosono’s $2391/400$
  measure dilated to $2989/500$ on a step-$1/8600$ net, refused by `sqverify-fast` at
  direction 529. It claims no bound.

The README says the dilation is only how the candidate was found: the walls do not
scale, so the centre domain grows toward them, and Hosono’s net no longer admits the
larger core, so 400 of the 600 directions are new. The bound rests on the full check.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 25 files: 24 retained under
[source/](source/) (885,104 bytes) and `.gitignore` pinned by digest, since a retained
copy would act on this repository’s tree.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The
packet is under a megabyte, so it is kept in Git.

Every digest the issue and the source’s README state holds: the certificate’s stored
file `116c8342…16f8` (the receipts’ `input_sha256`), its JSON text `b8b03ee8…749c`, and
Hosono’s `candidate.json` at
[wand125/square-packing-bounds@797bdf6e](https://github.com/wand125/square-packing-bounds/tree/797bdf6e10eba5f9dccca9da06f8352e81ba9dde/certificates/mixed_n94_L995)
`64d81953…0667a`, read on 3 November 2026 from raw.githubusercontent.com and equal to
the T-091 packet’s retained copy.
No program of the source ran in writing the packet.

## Premises and the Dilation

`devtools.audit_dilated_measure audit` recomputes, from the retained bytes and in exact
rationals apart from the crate,
[receipts/dilation-audit.json](receipts/dilation-audit.json), status `PREMISES_HOLD`:

- **The file** is format M: 853 rectangle rows and no points, no `scaling_factor`, a
  `proof_net` of exactly `step` and `last`, no top-level `net` and no certificate
  metadata; every rectangle nondegenerate and inside $[0, L]^2$, every mass
  nonnegative, the total exactly $94 - 1/100000$.
- **Lemma N0** of `sqverify_fast/SOUNDNESS.md` holds on the declared net:
  $N_\theta = 600$; $B(1 + D) = 2387749705363/2388000000000 < 1$;
  $t_{\max}^2 + 2t_{\max} - 1 = 3860089/14400000000 > 0$ at
  $t_{\max} = 49717/120000 \le 1/2$; and the tangent form
  $B(1 + D/(1 - D^2/4)) = 1146119721592254871/1146239862908900000 < 1$.
- **The dilation** is exact: $L$ and $B$ are $\lambda$ times Hosono’s, each of the 853
  rows is $\lambda$ times his row in order, and each mass equals his.
- **The regeneration**: Hosono’s retained candidate, rewritten by the rule
  `tools/rescale.py` states and serialized as Python’s `json.dump` writes it, has the
  JSON text’s SHA-256 `b8b03ee8…749c`, byte for byte the certificate.
- **What the dilation does not carry**, reported apart and required of nothing: on
  Hosono’s net the dilated core has
  $B(1 + 83/40000) = 797016825363/796000000000 > 1$, so the finer net is needed; at the
  axis the centre domain grows by $3/3986$ in Hosono’s coordinates; and the route’s
  ceiling as the step goes to zero is $L_0/B_0 = 99500/9977 \approx 9.9729$, above
  $1993/200$.

None of it decides coverage.

## Complete Replay Here

`devtools.sqverify_fast_census` ran this repository’s `sqverify-fast`, built from the
reviewed crate source `d97758bb…` (binary `567a0fd5…`, rustc 1.98.0, release), on the
retained certificate at all 600 directions of its declared net on 3 November 2026, at
two threads under `nice -n 19` on a shared four-core host
([census row and receipts](../../../benchmarks/measure-verifier/census-mixed/ozden-s94-lower-bound-2026-11-03/README.md)):
VERIFIED, every direction verified, 296,805,699 nodes, least certified bound
1.0000000000314393 at direction 277, whose least-bound leaf’s centre captures at least
1 in exact rationals; 8,138.6 CPU-seconds (`wait4`) in 4,180 seconds of wall.

`devtools.audit_dilated_measure compare`
([receipts/replay-comparison.json](receipts/replay-comparison.json),
`EVERY_DIRECTION_AGREES`) finds every field of every direction’s row, timings aside,
equal to both of the author’s receipts, and their summaries equal in status, nodes,
refused directions and premises. The capture took 1.03 and 1.02 times the CPU the two
receipts record. It also reads the second checker’s output, without running it: 600
directions VERIFIED, 166,440,592 nodes, least bound $4398046511113/2^{42}$ at direction
587.

The whole-net control (`--control`, about two minutes of wall at two threads) verified
the original again at direction 277; refused every mass scaled by 99/100 at all 600
directions, each a coverage refusal at a centre in the per-bin domain where the mutant’s
exact capture, evaluated apart from the crate, is below 1; and refused the mutant scaled
to one part in a million below 1 at the least-bound leaf’s centre, with an exact witness.
The receipt is kept as it failed closed,
`mixed_n94_L9965.control-failed-v2.json`, on one bookkeeping rule: at the axis the exact
capture of the 99/100 mutant at the sweep’s least vertex, $0.99308601381$, sits
$1.12 \times 10^{-9}$ above the vertex sweep’s certified bound, beyond the census’s
constant tolerance of $10^{-9}$. The refusal there is sound, the bound lying below the
capture as it must; the constant is F-1 of the
[14 October review](../../../../docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md),
which n = 39’s control meets too, and think-4uun owns its fix.

The author ran the same checker, so this replay is reproduced with the producer’s code;
it is not a second implementation. On a declared net the census route stands as
evidence only beside a passing control receipt (the 6 October declared-net soundness
review, item 6) and once a review has read the certificate’s mathematics (item 7), so
no evidence entry cites the row yet.

## The Stage 4 Review

The stage 4 mathematical review of 3 November
([review](../../../../docs/project/reviews/review-2026-11-03-ozden-s94-dilated-measure.md)),
by a separately prompted lane at the strongest tier (think-222u), accepts the
certificate with no defect. Its programs and receipts are under
[review/dilated-measure-2026-11-03/](review/dilated-measure-2026-11-03/README.md): every
premise but coverage recomputed exactly, direction 0 decided in full apart from the
crate (least capture 1.003117185664 at the wall), every other direction’s least-bound
box held exactly, every refusal of the control receipt held exactly, and five mutants
refused. That run is `E-ozden-890-n94-9965-review-sample`, a sample that sets no rung.
Its F1 is the control’s axis tolerance above. Its notes for the source:

- **F3.** `notes/n31-negative/d529.jsonl` is a run on an input the packet does not
  keep: the retained `n31_L5978.json.gz` with every mass times $10000003/10000000$. At
  the receipt’s witness the retained file itself captures $0.99999969508 < 1$, and the
  README’s $0.99999999719$ is in no retained receipt.
- **F4.** The second checker checks the quadrant $[L/2, U_r]^2$, which covers each
  direction’s whole centre domain only through the quarter turn and the measure’s
  symmetry; the READMEs call it the full centre domain.
- **F5.** `tools/rescale.py`’s growth formula $\rho(1 - 1/\lambda)$ holds at $r = 0$ and
  on an unchanged net; on the finer net the growth at the shared nodes runs from
  $6.55 \times 10^{-5}$ to $1.062 \times 10^{-3}$, and the new nodes have no old domain.

## What Is Not Established

- **No passing control yet.** Until a control receipt passes (think-4uun), n-094’s
  verified lower bound stays T-091’s $199/20$.
- **No second complete implementation here.** The replay is this repository’s
  `sqverify-fast`, the checker the author ran, so it is reproduced with the producer’s
  code; the review decided one direction in full and sampled the rest, and the author’s
  second checker is retained and was not run.
- **Optimality** of any kind: a lower-bound certificate says nothing about the 10 × 10
  grid’s side.

## Credit and Licence

The certificate is Doğa Özden’s, after Hiroaki Hosono, whose measure, format and method
it dilates, after Tokoharu’s rectangle-density certificates; the source credits the
declared nets to issue #366 and the dilation move to this repository’s T-022 and T-024,
and the checker it decides with is this repository’s. The source says the search, the
certificate, the verification runs and its write-up were produced by AI agents in the
author’s research lab under his direction: Claude (Anthropic) agents, and an OpenAI
Codex agent, which wrote the second checker and reviewed the argument. The bibliography key is
**[Özden s94 dilation 2026-11-03]**.

The repository states no licence. It is retained on the presumption of permission that
an author’s own submission to this repository carries (the owner, 24 October 2026,
think-cnn7); the exact licence is asked on think-0so3. Hosono’s measure is published
under the MIT licence (Copyright (c) 2026 wand125), and his notice applies to the
dilated certificate as well.

## Original Gzip Files

The two upstream files whose own names end in `.gz` are retained as published, never
recompressed. The table binds their compressed bytes: the Git blob and SHA-256 of each
stored file, which are its blob at the pinned commit and, for the certificate, the
digest the issue states.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/certificate/n94_L9965.json.gz` | upstream | `2ff3a4429747f4a76184c74f80935323bcc1259b` | `116c83425959a943196287a910ad799b2fe1bb9dec433085ea222bd62d5a16f8` |
| `source/notes/n31-negative/n31_L5978.json.gz` | upstream | `307feb35401cf13ae6f137e17f1eaaee197e0ee1` | `d46ce612f17dbf0a5fb6980275fb6f7faa7bf242cdfa90a5284cdbfbb2c11c86` |

## Compressed Files

The second checker’s premises file, of more than 1,000 lines, is stored as deterministic
gzip made by `gzip -9n`, with no file name or timestamp in the header. The table gives
the Git blob and SHA-256 of the decompressed bytes, and
`python -m devtools.retained_data check PACKET` re-derives the row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `source/second-checker/full.premises.json.gz` | upstream | `c654f52c741ce645725a918943a892d7bec980ea` | `b11524d4a6b36f3fd108375e5a0588a23b970513e827824b5ae52466cde0e522` |

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ozden-s94-lower-bound-2026-11-03 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s94-lower-bound-2026-11-03 --check
python -m devtools.audit_dilated_measure audit ozden-s94-lower-bound-2026-11-03 --check
python -m devtools.audit_dilated_measure compare ozden-s94-lower-bound-2026-11-03 --check
python -m devtools.sqverify_fast_census --family mixed \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n94_L9965
python -m devtools.sqverify_fast_census --family mixed --control \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n94_L9965
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
