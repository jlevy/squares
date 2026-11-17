# s(94) ≥ 2493/250 = 9.972

Claimed by Doğa Özden (@dogaozden, live tracker: https://dogaozden.com/math/live/square-packing/)

This is a lower bound for the side of a square containing 94 non-overlapping unit squares. It improves the registered lower bound [T-262](https://squaremath.org/result/t-262.html), `1993/200 = 9.965`, by `7/1000`. **This is a rescaled Hiroaki Hosono density measure, not a new packing arrangement.** It supplies no new upper bound.

The measure is Hiroaki Hosono's (`wand125`) `mixed_n94_L995`, after Tokoharu's rectangle-density certificates. Credit also belongs to Joshua Levy and the [jlevy/squares project](https://github.com/jlevy/squares), its declared-net work ([#366](https://github.com/jlevy/squares/issues/366)), verifier, review and T-262. The new contribution here is the exact dilation to 9.972, its finer declared net and exhaustive verification. No endorsement by those authors is implied.

## Exact certificate

| Quantity | Exact value |
| --- | --- |
| n | 94 |
| L | `2493/250` |
| λ relative to Hosono's 9.95 measure | `4986/4975` |
| B | `24872661/24875000` |
| half-angle net step D | `1/12000` |
| last index | `4971` (4,972 directions, indices 0–4971) |
| last half-angle tangent | `1657/4000` |
| total mass | `9399999/100000 = 94 − 1/100000` |
| B(1+D) | `99498934887/99500000000 < 1` |

There are 853 listed rectangle orbits, with every coordinate multiplied by λ and every mass unchanged; there are no points or segments. The native verifier reports 6,720 expanded rectangle terms. `certificate/n94-L9972.json` is canonical JSON (sorted keys, compact separators, no final newline); the gzip contains those exact bytes.

The density is nonnegative and D4-symmetric. The net and shrink inequality put a closed B-core strictly inside each appropriately oriented open unit square. Every admitted core centre captures mass at least 1; 94 pairwise interior-disjoint squares would then require total mass at least 94, contradicting the exact mass above. Details and arithmetic assumptions of the retained Rust implementation are in [`verifier/sqverify_fast/SOUNDNESS.md`](verifier/sqverify_fast/SOUNDNESS.md).

**Domain wording.** The checked quadrant `[L/2,U_r]²` represents the whole admissible centre domain **via quarter-turn symmetry of the square and the D4-symmetric measure**. It is not literally the full domain. The margin is per-bin, not a single global margin; the native summaries explicitly say `centre_domain: per-bin`.

**Dilation is not a coverage proof.** In old coordinates the outward growth at a shared angle t is

```
m_old(t) − m_new(t)/λ,
```

where m is the old/new per-bin wall margin for the domain actually used. In sqverify-fast format M, `m(t) = ρ(max(0,t−D/2))`, with `ρ(a)=(1+2a−a²)/(2(1+a²))`; the exploratory C front end additionally takes the maximum with the B-core's half-width, so its quadrant can be smaller. The Rust checks cover the larger native domain, not merely that exploratory quadrant. Finer nets change these margins. There is no universal `ρ(1−1/λ)` formula on the changed net. Coverage over the full domain and full new net must be checked; it is not automatic under dilation. The limiting ceiling of this unchanged-measure dilation route is `99500/9977 ≈ 9.97294`, not a claimed bound.

## Evidence and what was checked

The lab ran the unmodified interval branch-and-bound implementation **sqverify-fast**, from `jlevy/squares`. Every final direction has an authentic individual native receipt, verified at threshold exactly `1`, with a finite certified lower bound at least `1`. The exhaustive archive has **4,972 unique indices 0–4971**. Its least certified bound is `1.0000000000003892`, at direction `3663`; this is a certified leaf bound, not an assertion that the exact minimum capture equals that number.

The final archive is a union of actual native executions, not a fabricated monolithic `VERIFIED` summary. A native `PARTIAL` summary means a **successful strict subset of the net** (return code 0), not a failed direction. Every stream includes its original native summary; all refuse lists are empty and fault injection is null. No omitted row is inferred from a summary.

| Neutral evidence ID | Requested scope | Native rows | Selected final rows |
| --- | --- | ---: | ---: |
| A | contiguous 2486–4971 | 2486 | 2486 |
| B | explicit list in index | 801 | 801 |
| C | explicit list in index | 800 | 800 |
| D | explicit list in index | 800 | 800 |
| E | declared sample (formula checked by audit) | 150 | 84 |
| F | positive control: 0, 1198 | 2 | 1 |

[`receipts/INDEX.json`](receipts/INDEX.json) records the exact scopes, hashes of compressed and original retained streams, native summaries, return codes and compaction metadata. [`receipts/selection.csv`](receipts/selection.csv) maps each final direction to its original neutral-named native evidence stream. Every final line is byte-for-byte the selected original native line, including the original numerical bound.

Streams B/C/D were compacted at production: the native index, verdict, threshold, certified bound and method, and the whole native summary, were retained unchanged; auxiliary timing/search diagnostics on direction rows were omitted. Their original pre-compaction stream hashes are retained as recorded provenance statements. Those pre-compaction streams are **not available here**, and their digests cannot be independently rehashed from this packet. The retained compact streams themselves are hashed and audited; no absent diagnostic data is claimed to have been reconstructed.

### Controls and local audit

- `controls/mass-99-100.json.gz` has every mass exactly multiplied by `99/100`. The same native verifier refuses it at directions 0 and 1198 (return 1). `controls/native-mutant.jsonl` retains its actual receipts. This is a two-direction control, not a whole-net mutant replay.
- `controls/control.json` retains the exact rational witness at r=1198, x=`3477717289/625000000`, y=`7444849783253/1000000000000`, with capture approximately `0.991109005346039 < 1`. The exact fraction is retained in full. The audit recomputes its geometry, admissible quadrant membership and capture using rational polygon clipping. It also recomputes the separate native binary64 witness exactly; these are distinct centres and must not be conflated.
- `tools/audit.py` rechecks all exact premises (including native N0(e)'s stronger tangent-shrink condition, density/size caps, exact coalesced D4 mass and native domains), every rescaled row and unchanged mass, the original-source and candidate identities, pinned verifier source identity, all native summaries/scopes, native finite bounds ≥1, exhaustive uniqueness and selected-line provenance, plus the mutant construction and witnesses. `checks/archive-audit.json` records its result.
- `tools/test_audit.py` proves that duplicates, out-of-range indices, nonfinite/subthreshold bounds, a wrong native source identity and modified verifier source are refused, even with corrupted fixture archive hashes recomputed. `checks/negative-tests.json` records the result.
- `exploratory/` retains the prior lab C checker, its 4,972 `VERIFIED` rows, exact Python front end and original `SOUNDNESS.md`. **That C checker is not interval arithmetic:** it relies on the floating-point error analysis in that document, with double/long-double arithmetic and safety terms. Its archive is supplementary, not substituted for the Rust receipts. Its historical document paths refer to the original public checker layout; the files here are colocated in `exploratory/`.

**An archive/exact audit is not a fresh whole-net numerical replay.** The retained executions generated the coverage receipts. The quick packet audit checks those retained records and exact premises/witnesses; it does not repeat branch and bound at all 4,972 directions. No proof-assistant formalization, human review of this new certificate, or independent institution's replay of 9.972 is claimed. Running third-party sqverify-fast in the lab gives an independent **implementation**, not an independent institution's replay. In particular, jlevy/squares' published replay of T-262 was of 9.965, not this new 9.972 certificate.

## Reproduce

### Quick offline archive and exact audit

Python 3.11+ and its standard library suffice. Exact gzip regeneration was tested with Python 3.14.4 / zlib 1.3.1. The generator fixes mtime=0, compression level=9 and the gzip OS byte=255; different deflate implementations must reproduce the recorded digest or return an explicit error, never silently accept different bytes.

```sh
python3 tools/audit.py
python3 tools/test_audit.py
python3 tools/rescale.py --output /tmp/s94-regenerated
cmp certificate/n94-L9972.json /tmp/s94-regenerated/n94-L9972.json
cmp certificate/n94-L9972.json.gz /tmp/s94-regenerated/n94-L9972.json.gz
```

Regeneration requires a new output directory's file names, so an existing output is not overwritten. The source is retained: no network fetch is needed for this audit. `MANIFEST.json` inventories the packet; build products and Python caches are not publication evidence.

### Fresh numerical replay (separate, much slower)

Install rustup/cargo and **Rust 1.98.0**, as pinned by the unmodified `rust-toolchain.toml`. The first build may fetch Cargo.lock's pinned dependencies. No compiler-version downgrade or source edit is applied. Run outside any short-lived command timeout; these commands do real numerical work and write durable logs to a new directory.

```sh
# Sample only: does not establish the full net.
python3 tools/replay.py --directions 0,1198,3663,4971 --threads 4 --timeout-seconds 3600 --output /tmp/s94-replay-sample

# Full net: all 4,972 directions. Timing is machine-dependent.
python3 tools/replay.py --directions all --threads 4 --timeout-seconds 86400 --output /tmp/s94-replay-all

# Native negative control: expected refusal at both requested directions.
python3 tools/replay.py --mutant --directions 0,1198 --threads 2 --timeout-seconds 3600 --output /tmp/s94-replay-mutant
```

`replay.py` builds the unmodified source with `cargo build --locked --release`, requires the embedded source/input identities and exact native premises, passes `--threshold 1 --confirm`, and checks the exact requested scope. A timeout, build error, refusal of the positive certificate or missing toolchain is an explicit error, not an acceptance. Fresh output is distinct from the historical archive. The packet-preparation host performed the quick exact/archive audit; it did **not** have Rust installed and did **not** run these fresh replay commands. The historical native summaries record the actual producing builds (rustc 1.98.0, release, x86_64 Linux).

## Immutable identities and source pins

All SHA-256 values below are full digests:

| Artifact | SHA-256 |
| --- | --- |
| candidate gzip / native `input_sha256` | `f59d4c9562d7246f41c8c389a5bc118da9cf268a794e6416d146a195fb03360c` |
| candidate canonical JSON | `d1df3bc69bb12c0eebcb51d6b3636593079fbb82ae1128938ec5c07c83cc951c` |
| Hosono published source JSON | `64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a` |
| retained Hosono gzip | `df3ae678029f3da1f0fd4c9b1ba9d331c582478e46c453f238c36e476d9fd27c` |
| native verifier source identity | `d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88` |
| exhaustive receipts gzip | `041284d5031375054f3ddfdd2bb3e34a2ec0ae86c0802cb9c172fd3014287a59` |
| exhaustive receipts JSONL | `02906bb0f77db4d51d94446fec571a74a2dadb503d0698a482d5c2200213312a` |
| 99/100-mass mutant gzip | `2f72d2ddedd70e6be97fa58494b8508eb3020c2e8bbad5b2f429cac134c01532` |
| original licence declaration | `5b8e14499bddd521ce875b7b1b30da6f7ea215f3c44e15cfabce3a493f18da4c` |

Hosono source file: [`wand125/square-packing-bounds@797bdf6e10eba5f9dccca9da06f8352e81ba9dde`, `certificates/mixed_n94_L995/candidate.json`](https://github.com/wand125/square-packing-bounds/blob/797bdf6e10eba5f9dccca9da06f8352e81ba9dde/certificates/mixed_n94_L995/candidate.json). Its decompressed bytes, not an assumed upstream gzip encoding, identify the published source.

Verifier: [`jlevy/squares@e6e8d57726db80cd0e6a1523166a96c5d36a3119`, `packing/sqverify_fast`](https://github.com/jlevy/squares/tree/e6e8d57726db80cd0e6a1523166a96c5d36a3119/packing/sqverify_fast), copied without source changes. `verifier/PROVENANCE.json` records the Git blob identity and SHA-256 of every retained upstream file. The source digest is computed as upstream `build.rs` does: filename, NUL, contents, NUL for Cargo.toml, Cargo.lock, build.rs, then sorted src/*.rs. README, SOUNDNESS, INDEPENDENCE and toolchain pin are retained unchanged but are not covered by that embedded digest; the packet manifest covers them separately.

## Corrections and follow-up to #890

This packet incorporates the notes in [#890 and all three replies](https://github.com/jlevy/squares/issues/890):

1. The licence is explicit below and its existing declaration is preserved byte for byte.
2. The quadrant represents the whole domain through symmetry, rather than literally being the whole domain.
3. The rescale growth formula must use the old and new per-bin margins; a finer net changes them.
4. The earlier reply truthfully said intermediate sides had not been tried **then**. This later campaign did try finer intermediate sides and verified 9.972. No claim is made for the 49,707-direction 9.97285 partial.
5. The n=31 negative example discussed in #890 was not this campaign's control. Its previously mismatched retained input/receipt and quoted capture are not reused here; the retained 99/100 n=94 mutant above has its own exact inputs and witnesses.

## AI assistance and licences

AI agents in Doğa Özden's lab constructed/rescaled the certificate, ran checks and prepared this submission under his direction. Both Claude (Anthropic) and OpenAI Codex agents assisted this research/review campaign. The third-party verifier's own public independence record is retained; using it here is not a claim that its authors or an independent institution replayed this new certificate. There is no claim of formalization or human review.

[`LICENSE.md`](LICENSE.md) is the existing declaration copied byte for byte: Doğa Özden's certificates, witnesses, receipts, data and write-ups are **CC BY 4.0**; his source code is **MIT**. Prior rights are preserved, not reassigned: Hosono's source and original MIT notice are in `source/`; sqverify-fast is Joshua Levy/the squares project's MIT code, with CC BY 4.0 documentation and its full upstream licence in `verifier/sqverify_fast/UPSTREAM-LICENSE`. Please attribute "Joshua Levy, the squares project (https://github.com/jlevy/squares)" for that documentation. The packet's new or adapted material is marked and credited above. Cargo dependencies retain their own upstream terms; their source is not vendored here.
