# Joost de Winter’s s(108) ≥ 10.630037940829… at cc20a26

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/cc20a26845789c2502950041c26709eda8a71081),
a watched repository, at `cc20a26845789c2502950041c26709eda8a71081` (committed
2026-11-17T22:26:24Z, “Add the new n = 127 certificate, the lower bound for n = 108 and
the packings for n between 1,036 and 9,928”), the commit
[issue #1018](https://github.com/jlevy/squares/issues/1018) names 70 seconds later; it was
pushed with the next commit, `67fb815`, at 22:26:28Z. It first commits `lower_n108/`;
`67fb815` adds `lower_n108/REGISTRATION.md`, the issue’s text in the registration
template’s form, and `lower_n108/SHA256SUMS`, whose 36 digests match the pin’s files but
for `REGISTRATION.md` itself, and later commits leave `lower_n108/` unchanged through the
head, `838c5ea`. The same pin’s `n127/` is #1017’s certificate, which the
[de-winter-s127-issue1017-2026-11-17](../de-winter-s127-issue1017-2026-11-17/README.md)
packet retains, and its `above1000/` is #1019’s, held for think-1tkk; neither is in this
packet’s scope. The lane fetched the repository at 01:21Z on 18 November, when
`git ls-remote` read the head as `838c5ea`.

Intake lane w6-dewinter-1118 (think-i5en) retained it, audited it and replayed it on 18
November 2026. It is a lower bound, so the house rule does not reach it: the case’s lower
lanes move by stage 4’s exit alone.

## What the Source Claims

- **The bound.** $s(109) \ge s(108) \ge 1700799526134255846599/159999384348528500000 =
  10.6300379408297263703\ldots$, rounded down at 12 places as 10.630037940829, the 109
  because a packing of 109 squares contains one of 108. The issue names the record’s
  lower bound at 108, 10.62 (T-216, Hiroaki Hosono), and the gain, 0.0100, at both
  counts. At 109 the record held more modest bounds, Hosono’s closed form
  $a(109) = 10.5512903697\ldots$ reported (T-180) and Karakuş’s strip bound
  $10.4624294225$ verified, so the gain there is $0.0787$ and $0.1676$.
- **The certificate.** `evidence/n108_measure.json.gz` is Hosono’s measure of T-216
  (`evidence/Hosono_n108.json.gz`, his `mixed_n108_L1062`) with every rectangle
  coordinate multiplied by $1063/1062$ and every mass kept: 823 rectangle orbits under
  the square’s eight symmetries, total mass $10799999/100000 < 108$, in the square of
  side $L = 1063/100$, with the core side $B = 12487/12500$ and a net the file declares
  of 401 half-angle tangents $r \cdot 83/80000$, $r = 0, \ldots, 400$.
  `stretch_measure.py` writes it from Hosono’s file.
- **The runs.** `evidence/direction_runs/` holds twelve native outputs of this
  repository’s `sqverify-fast` (crate source `d97758bb…`, the source at `f9ddfeeef`,
  built by rustc 1.100.0), each a successful part of the net (status `PARTIAL`), together
  every direction verified, 266,337,510 branch-and-bound nodes. `sqverify_fast/` is that
  crate’s source as the author built it, and `evidence/SOUNDNESS.md` and
  `evidence/squares-project-license.txt` this repository’s soundness argument and licence.
- **The argument** (`proof_n108.pdf`, one page). For each direction the verifier
  certifies that every closed square of side $B$ at that direction, centred in
  $[w(a_r), L - w(a_r)]^2$, captures mass at least one, where
  $w(t) = (1 + 2t - t^2)/(2(1 + t^2))$ and $a_r = \max(0, rD - D/2)$. With $z_0 = D/2$,
  $u = 2Bw(z_0) = 319998768697057/320000086112500$ and $h = 707107/10^6 > 1/\sqrt 2$, the
  claimed side is $S = 2h + (L - 2h)/u$. A packing of 108 unit squares in $[0, S]^2$,
  scaled by $u$ and translated by $h(1 - u)$, lies in $[0, L]^2$ with every square’s
  centre clear of each wall by at least its axis half-width; each contains a core of side
  $B$ at its nearest net direction, centred in the verified domain, and the 108 cores,
  with disjoint interiors, would capture at least 108, more than the total mass.
- **The author’s checks.** `check_lower.py` (`fractions.Fraction`, standard library) is
  said to rebuild the measure from Hosono’s file, check the input and source digests of
  every run and one verified record per direction, integrate all eight images of every
  rectangle at the axis direction independently (least capture 1.007478833692, and
  0.997404045355 with every mass reduced by 1%), and check the enlargement;
  `lower_checks.txt` is its output, and `replay_lower.sh` rebuilds the crate and replays
  every direction. The issue says the full replay has not been repeated independently and
  that the bound is not claimed to be close to optimal. Those statements are the author’s;
  no source program ran here.
- **Credit and AI assistance.** It asks for credit to Joost de Winter, Delft University
  of Technology, after Hiroaki Hosono. The rescaling, the computation and the proof were
  produced with GPT-6.2 Astra (OpenAI), and the repository files and checks with Claude
  (Anthropic), both under his direction.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence, the root README and the whole of
`lower_n108/`, 37 files: 20 retained under [source/](source/), the certificate and the
twelve runs as their original gzips (below), and 17 pinned only. `LICENSE` is pinned
against its byte-identical copy in the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet. `Hosono_n108.json.gz` is byte for byte the copy of T-216’s candidate the
[wand125-fine-net-lower-bounds-2026-10-16](../wand125-fine-net-lower-bounds-2026-10-16/README.md)
packet retains, the crate copy is file for file this repository’s
`packing/sqverify_fast/` (crate source `d97758bb…` by `build.rs`’s rule), and
`SOUNDNESS.md` and the two licence copies are this repository’s files; each was compared
at intake and is pinned by digest. The proof, the scripts and the author’s output are
retained; `check_lower.py`, `stretch_measure.py` and `replay_lower.sh` were never run
here.

## Premises and the Dilation

`devtools.audit_dilated_measure audit` recomputed every premise from the retained bytes
in exact rationals, apart from the crate
([receipts/dilation-audit.json](receipts/dilation-audit.json), `PREMISES_HOLD`):

- **The file and the measure.** Format M, 823 rectangle rows, no scaling factor, a
  `proof_net` of exactly `step` and `last`, every mass nonnegative and every rectangle
  inside $[0, L]^2$, total mass exactly $10799999/100000$.
- **Lemma N0 on the declared net.** 401 directions, last tangent $83/200$, past
  $\tan(\pi/8)$; $B(1 + D) = 999996421/1000000000 < 1$.
- **The dilation.** $L = (1063/1062) \cdot 1062/100$, the same 823 rows, each
  rectangle $1063/1062$ times T-216’s row by row and each mass equal. The core is the
  source’s own $12487/12500$, above $1063/1062$ times T-216’s $9977/10000$
  ($10605551/10620000$), which the finer net admits; the tool was extended for it
  (`Dilation.core`).
- **The regeneration.** T-216’s retained candidate, rewritten by `stretch_measure.py`’s
  rule (`Dilation.stretch`), is byte for byte the certificate’s decompressed text,
  SHA-256 `d4d16090…`.
- **The enlargement’s arithmetic** (`Enlargement`): $u$ as above, $0 < u < 1$,
  $h^2 > 1/2$, $z_0^2 + 2z_0 - 1 < 0$, $2h < L$, $uS + 2h(1 - u) = L$, and
  $S = 2h + (L - 2h)/u$ equal to the claimed fraction exactly. That these carry the bound
  is the review’s question, not the audit’s.

## The Author’s Runs

`devtools.audit_dilated_measure receipts`
([receipts/native-receipt-audit.json](receipts/native-receipt-audit.json),
`RECEIPTS_HOLD`) read the twelve runs without running anything (`NativeRuns`): together
each of the 401 directions once; every row verified at threshold 1 with a finite
certified bound of at least 1, the least 1.0000000000543 at direction 76; nothing
refused or fault-injected; each summary’s premises the audit’s own, and each run’s input
the certificate’s decompressed text; every build of reviewed crate source for declared
nets, `d97758bb…`, by rustc 1.100.0 where the census binary is rustc 1.98.0; 266,337,510
nodes and 5,407.8 direction CPU seconds in all.

## Complete Replay Here

The checks below were planned before any of them ran: the expected outcome of the
premise audit, the complete replay and the whole-net controls was written down and hashed
at 01:49:49Z on 18 November (SHA-256 `52296592…ed37a`, recorded on think-i5en at 01:50Z),
and the plan is retained, committed and pushed before any receipt
([receipts/controls-plan-108.txt](receipts/controls-plan-108.txt), commit `5b11ce3af`).
Every outcome was the one stated.

`devtools.sqverify_fast_census` ran this repository’s `sqverify-fast`, built here from
reviewed crate source `d97758bb…` by rustc 1.98.0 (the census binary `567a0fd5…`, bit for
bit the one the census rows of #890 and #910 name), on the retained certificate at all 401
directions of its declared net, at threshold 1, from 01:52Z to 03:14Z on 18 November at
`nice -n 19` on two threads of a shared host: VERIFIED, exit 0, 266,337,510
branch-and-bound nodes, 4,624 CPU seconds and 4,943 seconds of wall. The axis direction was
decided by the exact-event vertex sweep over 30,713,764 vertices, least certified capture
1.0074788336; the least certified bound over the net is 1.0000000000543061, at direction 76,
and the exact capture at that leaf’s centre is 1.0295, clearing 1
([census row](../../../benchmarks/measure-verifier/census-mixed/census.json),
[direction log](../../../benchmarks/measure-verifier/census-mixed/de-winter-s108-lower-bound-2026-11-17/mixed_n108_L1063.jsonl.gz)).

`devtools.audit_dilated_measure compare`
([receipts/replay-comparison.json](receipts/replay-comparison.json),
`EVERY_DIRECTION_AGREES`) holds the capture to the author’s twelve runs: all 401 rows equal
on every field but the two timings, the premises equal but the input digest (the author ran
the decompressed text, the census the stored gzip), and the node totals equal. The two
builds are of one reviewed source by two compilers, 1.98.0 here and 1.100.0 the author’s,
so the replay is reproduced with the producer’s code, not a second implementation.

## Controls

`devtools.sqverify_fast_census --control` (receipt kind `sqverify-fast-control/v2`,
[mixed_n108_L1063.control.json](../../../benchmarks/measure-verifier/census-mixed/de-winter-s108-lower-bound-2026-11-17/mixed_n108_L1063.control.json),
`CONTROLS_REFUSED`, 03:15Z to 03:24Z) verified the original again at direction 76; refused
every mass scaled by 99/100 at all 401 directions, each a coverage refusal at a centre in
the per-bin domain where the mutant’s exact capture, evaluated again by an exact evaluator
written apart from the crate, is below 1, at the axis inside the enclosure the sweep held,
[0.9974040452859079, 0.9974040454240194]; and refused every mass scaled by 0.9713, which
puts the exact capture at the least-bound leaf’s centre at most one part in a million below
1, a counterexample candidate there. The exact capture at that centre, 1.0295, is the same
by the crate and by the independent evaluator. The author’s twelve runs carry no controls of
their own, so these are the only controls on the certificate.

The triage priced the census at about 1.2 CPU-hours, from T-216’s 136,113,602 nodes in
2,087 CPU-seconds scaled to the author’s 266,337,510 nodes; it ran in 4,624 CPU-seconds.

## Stage 4 Review

The blind stage 4 review of #1018 is lane R-108’s (under think-i5en); this lane has not
read it. The verified lower lanes at 108 and 109 move only once it is accepted and mapped
(`check_results`, `verified_lane_review_problems`); until then they stay at T-216’s
$531/50$ at 108 and Karakuş’s strip bound at 109.

## What Is Not Established

- **The enlargement.** The audit checks the proof’s arithmetic, not that its premises
  carry the bound: that a square of side $u$ at angle $\theta$, centred at least its axis
  half-width from each wall, holds a concentric core of side $B$ at its nearest net
  direction inside the per-bin domain of `sqverify_fast/SOUNDNESS.md`, lemma D, is the
  review’s to read. The format M theorem the census decides proves $s(108) \ge L = 10.63$
  by itself.
- **Independence.** The source decided the certificate with this repository’s
  `sqverify-fast`, so the census replay is reproduced with the producer’s code; no second
  complete implementation or second method stands beside it.
- **The author’s checks.** `check_lower.py` was not run here; its axis integration and
  hash checks are the author’s statements.
- **Optimality and human oversight**: none is claimed; no oversight record is retained.

## Credit and Licence

The bound is Joost de Winter’s, after Hiroaki Hosono, whose T-216 measure it dilates, and
through T-216’s credit after Tokoharu and this repository’s verifier: the record credits
**de Winter after Hosono, Tokoharu, Levy**, and the issue asks for “Joost de Winter, after
Hiroaki Hosono”. The record credits people, not AI agents
([attribution.md](../../../../attribution.md)), and states the assistance in the source’s
words. The bibliography key is **[de Winter s108 lower bound 2026-11-17]**. `LICENSE` at
the pin is de Winter’s MIT licence, and the root README says all files are released under
it; the crate copy and `SOUNDNESS.md` are this repository’s, under its own licence.

## Original Gzip Files

The upstream files whose own names end in `.gz` are retained as published, never
recompressed, except `Hosono_n108.json.gz`, pinned above. The table binds their compressed
bytes: the Git blob and SHA-256 of each stored file, its blob at the pinned commit, and for
the certificate the digest `67fb815`’s `SHA256SUMS` states.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/lower_n108/evidence/n108_measure.json.gz` | upstream | `78a44e7835e5b55818aaddf06464ae30414c4147` | `bd471f6541874a6f6a057c57b8804812563859d83a0f2e1a1aa7595dad32d0da` |
| `source/lower_n108/evidence/direction_runs/directions_000_030.jsonl.gz` | upstream | `5a501ddacf97d62ba1ea6ff59b13a3a25395922f` | `bc786015c7613c75563bd13ff646baba9ba7253ffd7e6d11fe7d1f3cf1a26ffd` |
| `source/lower_n108/evidence/direction_runs/directions_031_061.jsonl.gz` | upstream | `3f1e912f5591eb2bab41078d9bfe5378f724a3ae` | `88c93de96e6404368a83f272b526034fd552d4852f4aab429050c00f06c35a95` |
| `source/lower_n108/evidence/direction_runs/directions_062_092.jsonl.gz` | upstream | `021e3a100bc445ed83d3d6b410f643fda596598e` | `2f28406229e2abb4dbbdac44af7e5504703ba380b90edc244dfd336552969cb3` |
| `source/lower_n108/evidence/direction_runs/directions_093_122.jsonl.gz` | upstream | `2090daaa1991ee9fd72667d2e03735617443dd22` | `0ce36929a8ecbd1a78fb5625b1d361a17c9bc42cff64f46ad62800016476a483` |
| `source/lower_n108/evidence/direction_runs/directions_123_157.jsonl.gz` | upstream | `e462e959e45bc2278090c6aebecda2a535a9e587` | `635cfafe171138da889c5834430127f6d37389e905815ec8707c875852b5cf5a` |
| `source/lower_n108/evidence/direction_runs/directions_158_192.jsonl.gz` | upstream | `436cd444c67016615d4499aa03368d4514aa95e5` | `1f4fa06e916d83adb27731fb6d674cae3782fd1c71ed71520d826218b0b39da7` |
| `source/lower_n108/evidence/direction_runs/directions_193_227.jsonl.gz` | upstream | `ac415c554e0492833157d215dad891146ac58e96` | `0c2ded363c6a023593a1d246ddb620ad92df86fa5243b7a186c289e02425bef4` |
| `source/lower_n108/evidence/direction_runs/directions_228_262.jsonl.gz` | upstream | `26fb2acdeaf14462530e9e61d48004bb050cd498` | `5c10e8a74815df23bfd234182bcd6d6cdf91d237a31a72c4e26deb688b531802` |
| `source/lower_n108/evidence/direction_runs/directions_263_297.jsonl.gz` | upstream | `d12b41bc97fcd3d8c3f24c45b8c56989c42b58b1` | `6177b9f11292ff792a9fa1381dc92ad013b4c2447d9ed736ac87a69492c9dfaa` |
| `source/lower_n108/evidence/direction_runs/directions_298_332.jsonl.gz` | upstream | `3439c6a2e9ce124b4bbcb7f4144dc244de3e0077` | `0259bbc80ca60fe7951c665eed56362070553366cbb8fdefb618fa2b26ce9c61` |
| `source/lower_n108/evidence/direction_runs/directions_333_367.jsonl.gz` | upstream | `1c84c42d7ea04b1b6c5d9fdd94119a4c64ec2e42` | `a417861f032707759539f1013656b433cb95f080e2966b8a6becba2bf89edf15` |
| `source/lower_n108/evidence/direction_runs/directions_368_400.jsonl.gz` | upstream | `37c8fa88836786abbae1a9488508ea8386d2c933` | `93a66b9c0ba8959da14063ddaa6c70f03d3c022505fbb085f4103e1454543fcb` |

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-s108-lower-bound-2026-11-17
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.audit_dilated_measure audit $P --check
python -m devtools.audit_dilated_measure receipts $P --check
nice -n 19 python -m devtools.sqverify_fast_census --family mixed \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n108_L1063
nice -n 19 python -m devtools.sqverify_fast_census --family mixed --control \
  --binary sqverify_fast/target/release/sqverify-fast \
  --out benchmarks/measure-verifier/census-mixed --threads 2 --only mixed_n108_L1063
python -m devtools.audit_dilated_measure compare $P --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
