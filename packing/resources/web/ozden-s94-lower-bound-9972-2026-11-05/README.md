# Doğa Özden’s s(94) ≥ 2493/250 at 7d21f9b

This packet retains
[kenaznia-doga/s94-lower-bound-9972](https://github.com/kenaznia-doga/s94-lower-bound-9972/tree/7d21f9bdf707102dd4ebf47e52f81b502a01004d)
at `7d21f9bdf707102dd4ebf47e52f81b502a01004d` (committed 2026-11-05T06:51:31Z, the
repository’s one commit), which issue
[#910](https://github.com/jlevy/squares/issues/910) asks to register.
The issue and the repository were prepared and posted on Doğa Özden’s behalf by his AI
agent, which uses the GitHub account `kenaznia-doga`. It is the lab’s second dilation of
Hiroaki Hosono’s `mixed_n94_L995`, after #890’s `s(94) ≥ 1993/200` (T-262, retained by
[ozden-s94-lower-bound-2026-11-03](../ozden-s94-lower-bound-2026-11-03/README.md)).

## What the Source Claims

- `certificate/n94-L9972.json.gz` proves $s(94) \ge 2493/250 = 9.972$, $7/1000$ above
  T-262. It is Hosono’s `mixed_n94_L995` rectangle measure (T-091) with every coordinate
  multiplied by $\lambda = 4986/4975$ and the masses unchanged: 853 rectangle orbits of
  total mass $9399999/100000 < 94$, core side $B = 24872661/24875000$ (Hosono’s
  $9977/10000$ times $\lambda$), on a net the file declares (`proof_net`) of 4,972
  half-angles of step $1/12000$, last tangent $1657/4000$, with
  $B(1 + D) = 99498934887/99500000000 < 1$. `certificate/n94-L9972.json` is its
  canonical JSON text, the gzip’s decompressed bytes. The README calls it “not a new
  packing arrangement”.
- `tools/rescale.py` regenerates the certificate and its gzip from
  `source/hosono-candidate.json.gz`, Hosono’s `candidate.json` at
  [wand125/square-packing-bounds@797bdf6e](https://github.com/wand125/square-packing-bounds/tree/797bdf6e10eba5f9dccca9da06f8352e81ba9dde/certificates/mixed_n94_L995).
- `receipts/` holds the lab’s runs of this repository’s `sqverify-fast` at `e6e8d577`,
  unmodified (crate source `d97758bb…`, rustc 1.98.0, release, x86_64): six native
  streams A to F, each a successful strict subset of the net (status `PARTIAL`, return
  code 0), and `directions.jsonl.gz`, which takes one line per direction from them by
  `selection.csv`, VERIFIED at all 4,972 indices, least certified bound
  1.0000000000003892 at direction 3663. Streams B, C and D were compacted at production
  to the native proof fields; their pre-compaction digests are the lab’s statements and
  cannot be rehashed from the packet.
- `controls/` multiplies every mass by $99/100$, refused natively at directions 0 and
  1198, and states an exact rational witness at 1198 capturing
  $0.991109005346039\ldots < 1$. The README says this is a two-direction control, not a
  whole-net one.
- `exploratory/` is the lab’s earlier C checker with its 4,972 VERIFIED rows. The README
  says it is not interval arithmetic and offers it as supplementary, not as evidence.
- `verifier/` is the copy of `packing/sqverify_fast` at `e6e8d577` the lab built, with
  its provenance record; `tools/audit.py` and `tools/test_audit.py` are the lab’s own
  archive audit and its negative tests, with their results in `checks/`.

The README also answers three notes of #890’s stage 4 review: the checked quadrant
$[L/2, U_r]^2$ stands for the whole centre domain through the quarter turn and the
D4-symmetric measure; the outward growth at a shared angle is
$m_{\mathrm{old}}(t) - m_{\mathrm{new}}(t)/\lambda$, not $\rho(1 - 1/\lambda)$; and the
n = 31 aside of #890 is not reused. It keeps the route’s ceiling at
$99500/9977 \approx 9.97294$ and claims nothing for a 49,707-direction run toward
9.97285 that it calls partial.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the whole tree, 56 files: 54 retained under
[source/](source/) (2,177,278 bytes) and two pinned by digest.
`.gitignore` is pinned, since a retained copy would act on this repository’s tree.
`source/hosono-candidate.json.gz` is pinned because this repository already keeps it:
its stored bytes, SHA-256 `df3ae678…d27c`, are byte for byte the gzip the
[wand125-mixed-bounds-evening-2026-10-04](../wand125-mixed-bounds-evening-2026-10-04/README.md)
packet keeps of Hosono’s `candidate.json` for T-091, and `devtools.audit_dilated_measure`
reads the base from there.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about two megabytes, so it is kept in Git.

Every digest the issue and the README state holds, checked on the clone and again by
the receipts below:

- the certificate as stored, `f59d4c95…360c` (the receipts’ `input_sha256`);
- its canonical JSON, `d1df3bc6…951c`, which is also `certificate/n94-L9972.json`;
- Hosono’s `candidate.json`, `64d81953…0667a`, equal to the T-091 packet’s copy, and the
  lab’s gzip of it, `df3ae678…d27c`;
- the merged receipts, `041284d5…7a59` as stored and `02906bb0…312a` decompressed;
- the mutant, `2f72d2dd…1532`;
- the verifier’s embedded source, `d97758bb…1c88`;
- and `LICENSE.md`, `5b8e1449…a18da4c`.

No program of the source ran in writing the packet or its receipts.

## Premises and the Dilation

`devtools.audit_dilated_measure audit` recomputes, from the retained bytes and in exact
rationals apart from the crate,
[receipts/dilation-audit.json](receipts/dilation-audit.json), status `PREMISES_HOLD`:

- **The file** is format M: 853 rectangle rows and no points, no `scaling_factor`, a
  `proof_net` of exactly `step` and `last`, no top-level `net` and no certificate
  metadata; every rectangle nondegenerate and inside $[0, L]^2$, every mass
  nonnegative, the total exactly $94 - 1/100000$.
- **Lemma N0** of `sqverify_fast/SOUNDNESS.md` holds on the declared net:
  $N_\theta = 4972$; $B(1 + D) = 99498934887/99500000000 < 1$; the last tangent
  $t_{\max} = 1657/4000 \le 1/2$ covers the endpoint, since
  $t_{\max}^2 + 2t_{\max} - 1 = 1649/16000000 > 0$; and the tangent form
  $B(1 + D/(1 - D^2/4)) = 14327846598855339/14327999975125000 < 1$.
- **The dilation** is exact: $L$ and $B$ are $\lambda = 4986/4975$ times Hosono’s, each
  of the 853 rows is $\lambda$ times his row in order, and each mass equals his.
- **The regeneration**: Hosono’s retained candidate, rewritten by the rule
  `tools/rescale.py` states and serialized as it writes canonical JSON, is byte for byte
  the certificate’s text; and its gzip as the README states it (level 9, mtime 0, OS byte
  255) is byte for byte the stored file under this repository’s Python 3.14.7.
- **What the dilation does not carry**, reported apart and required of nothing:
  - On Hosono’s net the dilated core has
    $B(1 + 83/40000) = 996970870863/995000000000 > 1$, so the finer net is needed.
  - The new net shares 20 nodes with Hosono’s 201, and 4,952 of its 4,972 directions
    are new.
  - At the shared nodes the centre domain grows by
    $m_0(t) - m(t)/\lambda$ in Hosono’s coordinates, each margin the per-bin
    $\rho(\max(0, t - D/2))$ on its own net: from $1.93 \times 10^{-4}$ to
    $1.52 \times 10^{-3}$, and $11/9972$ at the axis.
  - The route’s ceiling as the step goes to zero is $L_0/B_0 = 99500/9977$, above
    $2493/250$.

The same growth measured on #890’s net, 200 shared nodes and 400 new, runs from
$6.55 \times 10^{-5}$ to $1.062 \times 10^{-3}$, which is F5 of that certificate’s stage
4 review. None of it decides coverage.

## The Lab’s Receipts

`devtools.audit_dilated_measure receipts`
([receipts/native-receipt-audit.json](receipts/native-receipt-audit.json), status
`RECEIPTS_HOLD`) reads the retained streams and runs nothing.

- **Each stream** A to F holds exactly the scope the index states, once each. Its
  summary is the separate summary file and refuses nothing, with no fault injected.
  Every row is verified at threshold 1 with a finite certified bound of at least 1. Its
  premises are the certificate’s as recomputed above, with `input_sha256` the stored
  certificate’s and 6,720 expanded rectangles.
- **The build** is the same in every stream: crate source `d97758bb…`, which
  `REVIEWED_SOURCES` admits for declared nets (910b6b12c), rustc 1.98.0, release,
  x86_64-unknown-linux-gnu. These are the same compiler, profile and target as the
  census binary `567a0fd5…` (row `mixed_n94_L9965`). The lab’s receipts record no binary
  digest, so “the same build” rests on these build facts. The retained crate copy under
  `verifier/sqverify_fast` is that source by `build.rs`’s rule.
- **Coverage**: the merged archive holds each of the 4,972 indices 0 to 4971 once,
  every one verified, threshold 1, finite bound at least 1. Each line is byte for byte
  the line of the stream `selection.csv` names. The selection takes 2,486 lines from A,
  801 from B, 800 each from C and D, 84 from E and 1 from F, as the index states.
- **The least certified bound** is 1.0000000000003892, at direction 3663.
- **Nodes**: the selected rows hold 2,462,923,881 nodes. Of these, 1,416,273,774 are
  recorded row by row; the rest are the totals of the compacted streams B, C and D,
  every row of which is selected. All six streams hold 2,499,604,169 nodes over 5,039
  rows in 51,190 direction CPU-seconds at four threads (F at two).
- **The control**: `mass-99-100.json.gz` is the certificate with every mass exactly
  $99/100$ times its own and nothing else changed but its `derived_from` label. It is
  refused natively on coverage at directions 0 and 1198, a build of the same reviewed
  source. Each witness is recomputed by `check_sqverify_fast.mixed_exact`, an exact
  evaluator written apart from the crate:
  - at 1198, the lab’s rational centre $(3477717289/625000000,\,
    7444849783253/1000000000000)$ captures exactly the stated
    $0.991109005346039\ldots$, in the per-bin domain and the searched quadrant, where
    the original captures $1.00112\ldots$;
  - the crate’s own binary64 witness there captures $0.99764492\ldots$, equal to its
    stated exact coverage;
  - at the axis, the sweep’s least vertex captures $0.99305598\ldots$, above its
    certified bound $0.9930559807565953$.

  It is a control at two directions, not over the whole net, as the source says.

This is an audit of the lab’s receipts: it decides no coverage, and it is not a replay.

## The Replay Here, Priced

The replay this repository runs is `devtools.sqverify_fast_census` over all 4,972
directions, then `--control` over the whole net. It has not run. The census reads the
packet’s certificate (`MIXED_FILES`, `mixed_n94_L9972`), and the producer relation is
`same-implementation` (`SAME_CRATE_PACKETS`), as for #890.

`devtools.fine_net_followup sample`
([receipts/sample-diagnostic.json](receipts/sample-diagnostic.json),
`DIAGNOSTIC_SAMPLE`) ran this repository’s binary `567a0fd5…` on 5 November 2026. It
covered 13 directions: 0, every 497th to 4473, 1198, 3663 and 4971. Each ran at one
thread, two at a time, under `nice -n 19`, in 154.2 process CPU-seconds and 81.7 seconds
of wall.

- Every direction verified, with its certified bound equal to the lab’s selected line.
- At the 8 directions where the lab’s line records nodes, the nodes are equal too.
- Direction 3663’s bound is 1.0000000000003892, the archive’s least.

The price:

| Item | Basis | CPU-hours |
| --- | --- | ---: |
| Census, 4,972 directions | the sample’s mean | 16.4 |
| Census, 4,972 directions | the sample’s 24.99 µs a node, times the 2,462,923,881 selected nodes | 17.1 |
| Census, 4,972 directions | #890’s census, 8,138.6 CPU-seconds over 600 directions and 296,805,699 nodes | 18.8 |
| Whole-net control | #890’s control, 134.9 seconds of wall at two threads for 600 directions, scaled | 0.6 |
| Census and control | #890’s numbers | 19.4 |
| Census and control | the sample tool’s conservative model, which prices the control as a second full sweep | 32.8 |

Every basis is under the owner’s 40 CPU-hour item cap, so the replay is runnable after
review, about ten hours of wall at two threads; it is not held. A sample decides only
the directions it ran.

## The Stage 4 Review

Not yet run. A separately prompted stage 4 mathematical review at the strongest tier is
briefed on its own bead; the import lane does not review its own import.

## What Is Not Established

- **The coverage, here.** The lab’s receipts are audited and 13 directions were
  sampled; this repository has not decided the certificate at every direction, and no
  review here has read it.
- **A second implementation.** The lab ran this repository’s checker, so the replay here
  will reproduce it with the producer’s code; the exploratory C checker is retained and
  was not run.
- **Optimality** of any kind: a lower-bound certificate says nothing about the 10 × 10
  grid’s side.

## Credit and Licence

The certificate is Doğa Özden’s, after Hiroaki Hosono, whose measure, format and method
it dilates, after Tokoharu’s rectangle-density certificates. The source also credits
Joshua Levy and this project, for the declared nets of #366, the verifier, its review
and T-262. The source says AI agents in Özden’s lab, Claude (Anthropic) and OpenAI Codex
agents, constructed and rescaled the certificate, ran the checks, audited the receipts
and prepared the submission under his direction. It claims no human review, no
formalization and no replay by an independent institution. The bibliography key is
**[Özden s94 lower bound 2026-11-05]**.

[LICENSE.md](source/LICENSE.md) is byte for byte the declaration the
[ozden-s94-lower-bound-2026-11-03](../ozden-s94-lower-bound-2026-11-03/README.md) packet
keeps (Git blob `9803370f8c382515d3769896adb8d04b201aebd6`): the certificates,
witnesses, receipts, data and write-ups are published under CC BY 4.0, and the lab’s
source code under the MIT licence, copyright (c) 2026 Doğa Özden. Hosono’s measure keeps
its MIT notice, `source/UPSTREAM-LICENSE` (Copyright (c) 2026 wand125), which applies to
the rescaled certificate as well. The crate copy keeps this repository’s licence,
`verifier/sqverify_fast/UPSTREAM-LICENSE`.

## Original Gzip Files

The upstream files whose own names end in `.gz` are retained as published, never
recompressed, except the one pinned above. The table binds their compressed bytes: the
Git blob and SHA-256 of each stored file, which are its blob at the pinned commit and,
for the certificate, the merged receipts and the mutant, the digests the issue states.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/certificate/n94-L9972.json.gz` | upstream | `b84fce8ae203a46db33fd5ea59d3dbdbc49260fe` | `f59d4c9562d7246f41c8c389a5bc118da9cf268a794e6416d146a195fb03360c` |
| `source/controls/mass-99-100.json.gz` | upstream | `915a5904ac09753652d0a37115c24c1c12242424` | `2f72d2ddedd70e6be97fa58494b8508eb3020c2e8bbad5b2f429cac134c01532` |
| `source/receipts/directions.jsonl.gz` | upstream | `b36f36e78dcfc4bfbc386843844e361b9c48efb6` | `041284d5031375054f3ddfdd2bb3e34a2ec0ae86c0802cb9c172fd3014287a59` |
| `source/receipts/native/A.jsonl.gz` | upstream | `b8fd5c8ed4192d7c68a05f53f78405c5d5de9651` | `98badbd01c18b6e8e280307eee893c6c5199bff43f55530d3f9baf578ad19d33` |
| `source/receipts/native/B.jsonl.gz` | upstream | `73467c845ccacdeae38691187eb9e1c132b15ce3` | `fe423335f6da99e19b5f188af29d50c77a3a52d82ed91d81841e64a431817f2a` |
| `source/receipts/native/C.jsonl.gz` | upstream | `746e5b64c5f75e11e6aa470b821f8682603ad687` | `00cd08920c78a5fcc37b27d1c3e986b539ed6a04f299d43bb21534c1ee1219c4` |
| `source/receipts/native/D.jsonl.gz` | upstream | `ea63bc22bd5cbde8fa94f228825355aaed00b0bf` | `4c88aece994b52e388c769535c48042ae75af781fbbfc49705bd44da99f5697a` |
| `source/receipts/native/E.jsonl.gz` | upstream | `5de4035ada325a80ba1bbfc6c22885b11b0d6cc9` | `d70d80dca37ae6a1dc4c56ba129b0b4f30bfae34bf3494511ec95d4d957429be` |
| `source/receipts/native/F.jsonl.gz` | upstream | `308d245868954e6883736b25e90946f63980566d` | `6fd192c28ab064f99528170e4f87a378ea7aad3446be4e2ae38a128d746d6cae` |

## Compressed Files

Two data files of more than 1,000 lines are stored as deterministic gzip made by
`gzip -9n`, with no file name or timestamp in the header. The table gives the Git blob
and SHA-256 of the decompressed bytes, and `python -m devtools.retained_data check
PACKET` re-derives each row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `source/exploratory/directions.jsonl.gz` | upstream | `918d4ef6254efe1cb31c5bbb5113970f94cf5046` | `c0f14c2a474839c668c4e10f359b6a43778f546cd70b9d55ed9020ac2bdafc6c` |
| `source/receipts/INDEX.json.gz` | upstream | `b83afc5a665558348dfa929954d582c6526f60a9` | `77212ccb4b4acf54759c6714ca6f1f1f748f0c76266314babc81326f5165096f` |

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ozden-s94-lower-bound-9972-2026-11-05 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s94-lower-bound-9972-2026-11-05 --check
python -m devtools.audit_dilated_measure audit ozden-s94-lower-bound-9972-2026-11-05 --check
python -m devtools.audit_dilated_measure receipts ozden-s94-lower-bound-9972-2026-11-05 --check
nice -n 19 python -m devtools.fine_net_followup sample \
  --binary sqverify_fast/target/release/sqverify-fast \
  --candidate resources/web/ozden-s94-lower-bound-9972-2026-11-05/source/certificate/n94-L9972.json.gz \
  --source-run resources/web/ozden-s94-lower-bound-9972-2026-11-05/source/receipts/directions.jsonl.gz \
  --directions 0,497,994,1198,1491,1988,2485,2982,3479,3663,3976,4473,4971 --workers 2 \
  --n 94 --side 2493/250 \
  --out resources/web/ozden-s94-lower-bound-9972-2026-11-05/receipts/sample-diagnostic.json
# After the stage 4 review (the replay, not run here):
python -m devtools.sqverify_fast_census --family mixed \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n94_L9972
python -m devtools.sqverify_fast_census --family mixed --control \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n94_L9972
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
