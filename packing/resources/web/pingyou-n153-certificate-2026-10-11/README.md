# PingYou Ltd: An Exact Packing of 153 Squares

[Issue #504](https://github.com/jlevy/squares/issues/504) (BuddenPing,
2026-10-11T10:39Z) reports an exact rational certificate for 153 unit squares in
[BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates/tree/bc328a7d727aedd0eabebd6ea80285f572b65d2d)
at `bc328a7d727aedd0eabebd6ea80285f572b65d2d` (tree
`ff4acf16f612e26c5c64576bfa399c6a2b9b2061`, committed 2026-10-11T10:39:06Z, parent
`9dc93b6ac2f8fefe038062a74c9a75bf05afdba6`), the revision the issue names and the branch
head when the source was retrieved at 2026-10-11T20:33Z. The parent is the n207 release
of [issue #503](https://github.com/jlevy/squares/issues/503), which
[its own packet](../pingyou-n207-certificate-2026-10-11/README.md) retains.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 153 | `6435006925203522001385040447/500000000000000000000000000` | 12.8700138504070441 |

## Who the Source Is

As for the n207 release: the README is headed “Square-packing certificates — PingYou
Ltd” and asks that **PingYou Ltd** be credited with the new n153 construction; the
commit is authored as `BuddenPing`, from an address at the `pingyou.com` domain; and the
source names no individual author, so this packet names none.

The record already holds an undated abstract with the author line “PINGYOU LTD”, *The
Fibonacci Geometry of Eleven Squares*
([packet](../pingyou-fibonacci-torus-2026-10-07/README.md), bead `think-aj43`). This
release’s `evidence/mechanism.txt` speaks of a “PhiMath transfer” and says that “No
Fibonacci Q operator has been demonstrated for this 153 construction”.
It does not name the abstract, and the record does not link the two.

## Source Custody

The tree has no licence file, and GitHub detects none.
The README says that included upstream material keeps its own attribution and licence
terms and that the repository adds no new licence grant for third-party material; it
grants none for the source’s own files.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[n207 packet](../pingyou-n207-certificate-2026-10-11/README.md), this packet keeps no
upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The scope is the paths the pinned commit changed: the six n153 files it adds, and
`README.md` and `SHA256SUMS`, which gain an n153 section and six lines.
All eight are pinned only; the declared `source/` directory is empty by design.
The five n207 files are unchanged at this pin, blob for blob, and belong to the n207
packet.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `n153.cert.json` | `62c83e0a045561f75613147c66563a79697d5f59` | 21910 | `31b3fb3cba73528fab21d085a34f3209684a868e7116059ea5c21e664bca1ff2` | The certificate |
| `pingyou-n153-rational.yaml` | `aedd6acdb80d1cfb742c962fcbddb1ccbee83802` | 114594 | `963d6ca7cce053e7ff22baf6438bdf5776b7b06d01e1509e654c73966b9e4d41` | The same packing as a corners Witness/v2 |
| `n153-squares-project.zip` | `79027273d1d1828981ee6e35450a8e9f8c904579` | 114499 | `dcc512828a8b6629d2d414f4ac20d417c2a4d5dc2968b9abe586676abe868d97` | The complete package, below |
| `README.md` | `564bf3fcaec273a0b8fc133128247e722a62fdd2` | 6798 | `1bacc3e76c7a9e5c5692bdd6320028fd99a1b3b09a7f7eba801f39760e2f010a` | Author prose for both releases |
| `SHA256SUMS` | `29570470a1290b6c8514504b91a9d80e0f67e254` | 1026 | `919ab6fbaad50b77a5f9d72d7a79f775a973ef18f9afa620c914c989de495997` | The source’s digests of the other twelve files |
| `n153-SHA256SUMS` | `640d0c04a79692e46bc7b4b6c38a3f780d0c5dd8` | 435 | `4d73c078bc411060661d34ce757d27abee1db9ca7b62d36876e97ca43006a9f3` | The source’s digests of the five n153 files |
| `n153-verified-comparison.pdf` | `436ed9847a4557eeb0a1dc8e683a2de17c7c65de` | 19150 | `ded1ee63d71f13f613edaa7473171a337918ec7a7d7f68733a1b41a7df27aaef` | Two-page comparison |
| `n153.svg` | `df5b5c22a36cd8d4b46778df6e5df800fff7673d` | 26524 | `4458251287d4a1d7982db1c9a9d79eaa9020872380dd66e6f8f9894c07dedf31` | Drawing |

The three digests the issue states, for the certificate, the witness and the package,
are the ones above, and both of the source’s digest lists agree with every file they
name, here and in the n207 packet.

## What the Package Holds

`n153-squares-project.zip` unpacks to `n153-squares-project/`, 40 files.
Its `manifest.json` lists a SHA-256 for each of the other 39, and every one equals the
digest of the bytes unpacked here.
Nothing in it is retained; no program in it ran here.

| Member | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `evidence/packing.cert.json` | 21910 | `31b3fb3cba73528fab21d085a34f3209684a868e7116059ea5c21e664bca1ff2` | The certificate, byte-identical to `n153.cert.json` |
| `native/pingyou-n153-rational.yaml` | 114594 | `963d6ca7cce053e7ff22baf6438bdf5776b7b06d01e1509e654c73966b9e4d41` | The witness, byte-identical to the top-level one |
| `evidence/rational_recipe.json` | 13974 | `63a46fb6a0400bcddccd1eec200b7c9652ca2aae989d69b6908c2a506afcbfce` | The construction table: 153 poses before the guard, and the guard |
| `evidence/parents/n070.cert.json` | 11399 | `d508ee05fd6b33b2ccd6cbd592d94a47f8458a46f5f580b0d63285b1535d7e8a` | The n70 source, byte-identical to the n207 package’s |
| `evidence/parents/cycle-hit-153.cert.json` | 45461 | `55091e63ee7a3a6f0c05d426e0fb74a6c83e4bfcfb7d0485e92966b017127b54` | An intermediate n153 control, below |
| `evidence/baselines/prior-153.cert.json` | 53938 | `f29e06ec8e8b481620ab4fbf2c9cada4663bfe91f291513eec895dc519ff3eb2` | SQUISH’s #481 n153 certificate, byte-identical to the one the [SQUISH packet](../squish-481-third-request-2026-10-09/README.md) pins |
| `evidence/baselines/regularized-153.cert.gz` | 2373 | `46b76905c084e2fa120f8fe172a632d81c17c84b8c1dd384703f402498c6f11c` | Evan Daniel’s regularized n153, byte-identical to the file the [T-146 packet](../evand-regularized-2026-10-10/README.md) retains |
| `evidence/baselines/regularized-153.cert.json` | 27505 | `4ad03b734191447659541d17490748baaf8bb08523ec640e433133393f599204` | The same certificate as JSON, the author’s conversion |
| `evidence/ATLAS-LICENSE.txt` | 1068 | `c51886c0f7e6724a7d89fc22cb237a1688ba1bbff04cb21a13b8e1a01fb15578` | Evan Daniel’s MIT licence, for his certificates |
| `evidence/reproduce.py` | 3094 | `95b50fe643beb375d0d269fc31c12fa3a36ceeeb8db3741d17f7de5e0d0d1b22` | Rebuilds the certificate from the table and the guard, and runs the three checkers |
| `evidence/audit_all.py` | 2593 | `49d2a1f386e89556d9d0d32cdc8feabcb9703deaf092a46d38ae8c294f6a817b` | Centre and support-radius separating axes |
| `evidence/vertex_check.py` | 4914 | `0635bd472cb4f066a9bc060f018c57350d2d3dea2c127f286a3ec94b136b4028` | Vertex projections, the n207 package’s file |
| `evidence/polygon_check.py` | 2118 | `85b881c132f6b0502fd1fe2eb5cfb0ba8949095c60f1ba8d3b142df737c1f0dd` | Rational polygon clipping, the n207 package’s file |
| `evidence/derive_half_return.py` | 1598 | `183a0ac05a6d3367f7d9ba1cef05ab57b8fc228dbe65e6a9560c70cf65221e6c` | SymPy derivation of the angle |
| `VERIFY.py` | 2388 | `7e5067e2a35bebca64424038d37108917829eab732472900b477aeeae0d71a05` | Checks the manifest, then runs `reproduce.py` and the conversion check |
| `native/convert_witness.py` | 6438 | `9ffba811e31bdfc8fecd837d9e4b5c3bf27f54c2d23375d944ca92b6143e6611` | Writes or checks the witness from the certificate |
| `native/replay_upstream.py` | 3710 | `ecbb9c01d5fe0efb1502653697c3ca1c5abf81b947a1c0768ec571ec03300c06` | Imports this repository’s two exact checkers from a checkout |
| `evidence/reproduction_audit.json` | 4984 | `01d7ce12f67954a789af0c8a5a6600aa3fbae5e9110195ef8484808a392c5222` | Receipt of `reproduce.py` |
| `evidence/exact-guard-audit.json` | 1897 | `f1e7988e965d242fbc14620283e24b4c13fd825dd94cc95f38e9312e41e9086b` | The guard the table needs, and the one used |
| `native/native-replay.json` | 2079 | `503be16453a65bb2f12ef2e405d8117a88964f9cc29ac02a5e000bc0a4c37b86` | Receipt of the two checkers here, at `5b0eb012` |
| `native/conversion-check.json` | 557 | `604bbeb4e5d22d51aaf3b9bebc0441876c5b69fd315ab2c6e313bfb752ed35c8` | Receipt of the witness check |
| `native/conversion-creation.json` | 557 | `f9bbc1ee765d04b0e20030211c3b5a8d37647ddabb268ced070091be0b7db8d0` | Receipt of the witness’s writing |
| `native/upstream-source-manifest.json` | 3318 | `8a811c11a3d2dccda25ae4a4724eb8c9b01d94c4a64600c487cc1590c6260986` | Digests of eleven files here, at `5b0eb012` |
| `native/witness.schema.yaml` | 9013 | `754ddd6eea0558344c174302318ed1e7235d9665f37ef4f6fdea1f1e627664dc` | This repository’s witness schema, byte-identical at `5b0eb012` |
| `native/UPSTREAM-LICENSE.txt` | 21153 | `7428341239cf4ee78c4b951b7fd8a2284b24835aeb0ede82f032b2e95e92cc00` | This repository’s `LICENSE`, byte-identical at `5b0eb012` |
| `native/credits.json` | 244 | `d6cbf4802f79c69b4a59fefdeca5bc4e10619f20b3c20b8c723f2f9bc4b6c864` | The credit lines the witness carries |
| `native/README.txt` | 4050 | `27c13cca6c6fbeb2ddfa3b92d0d017890304fd783839f5fdad9d021359c5751a` | The witness and its replay |
| `README.txt` | 2095 | `53d46d2563bbe0d1cc3ffe8368b076efe567e493cf56f0781b25bb974559d859` | The package’s account of the result |
| `evidence/mechanism.txt` | 5629 | `fd7386b70cb3eacdb70020beda13301690fa4ba9f246cb09df3526223c89115e` | How the construction was found, below |
| `evidence/PROVENANCE.txt` | 1349 | `74dddf8a5a80035eee1c906f737a63f9926905ccf3d790a34423c5b9eaab7e8e` | Maps the certificate’s path labels to the bundled files |
| `evidence/public-comparison.json` | 4567 | `4f3c069fa6d2b6d38f8139f2ddb1c9ac9a558959206ca42bd04ca1591425b11a` | The author’s dated survey of prior n153 sides |
| `evidence/document-binding.json` | 587 | `10f4466261c1f68a57b2f0fceade878c90ed45927ec1b58fc4260ba77aba1fec` | Digests of the certificate and the PDF |
| `evidence/derivation/half-return-replay.json` | 717 | `2e1f42d136e2a02d236bb02e48e35de6ac881494f123b409dd91002c58e1cb94` | Output of `derive_half_return.py` |
| `evidence/derivation/independent_physical_return_audit.json` | 53624 | `d84ad4386c86446b0be81a96d87f01347e3b9d528c54820916ae93dbf7701854` | Contact-family audit data |
| `evidence/derivation/n153-second-derived-crossing-return.json` | 12124 | `28fc26ca431020a759c4e3263fa577b4196667983f72769e678c315bae85c989` | The floating-point configuration at the derived angle |
| `evidence/derivation/n178-critical-return-points.json` | 649 | `42d81be54657ee2291fb11112cacc5552506fa8277f1f103e4d84a6669ef9f5f` | Critical angles of the return bounds |
| `evidence/derivation/n178-remaining-return-algebra.json` | 1523 | `6926fc1d9c25b09e1db701473cf7729df4820c87057d102aa35289d4bf06bbe2` | The return algebra of a companion 178 control |
| `evidence/n153-verified-comparison.pdf` | 19150 | `ded1ee63d71f13f613edaa7473171a337918ec7a7d7f68733a1b41a7df27aaef` | The top-level PDF |
| `evidence/n153.svg` | 26524 | `4458251287d4a1d7982db1c9a9d79eaa9020872380dd66e6f8f9894c07dedf31` | The top-level drawing |
| `manifest.json` | 4271 | `449991070c25942356bcbd648097a9d159435af4f002bc2d222750bdba1a29a3` | The package’s digest list |

The intermediate control `cycle-hit-153.cert.json` states a side of
`128809603728436756319410591381175501178639/10000000000000000000000000000000000000000`,
about 12.88096, above the case ceiling at 153; the source does not offer it, it asks for
nothing, and it stays in the package.
The n178 files hold analysis of a companion control and state no side at 178.

## The Certificate

`n153.cert.json` is a JSON object with `n`, `s_exact`, `squares`, one `[x, y, t]` triple
of rational strings per square, the centre in $[0, S]^2$ and $t = \tan(\theta/2)$, and
the source’s `note`, its guard `dilation_exact`, its undilated floating-point side
`raw_side` and its construction record `provenance`. `devtools.upper_bound_reports`
reads it with the `pingyou-json` adapter, which takes `s_exact` and `squares` and reads
the other four without believing them.

The construction, as the source states it: two complementary patches of the n70 source,
one at $(0, 0)$ and one reflected and placed at $(4, 4)$, with their upright completion,
give 121 upright squares and tilted populations of 17 and 15. The surviving contacts are
reclosed at the angle where two lower bounds on the fractional side $f$ cross; with
$u = \tan(\theta/2)$ that is the root of $u^7 - 9u^6 + 3u^5 - u^4 - u^3 + u^2 - 3u + 1$
near $u = 0.355$, $\theta \approx 39.09°$, $f \approx 0.8700138504044643$. The
certificate takes the tilted squares at the rational $t = -35500514903623/10^{14}$ and
$-47600915127337/10^{14}$, so the explicit table has the side
$1287001385040447/10^{14}$; every centre and the box are then dilated by
$5000000000001/5000000000000$, the squares keeping side 1, and the two multiply to
`s_exact`. The source says that the table came from an exploratory selection and a
floating-point solve that the release does not repeat, and that the degree-seven
equation explains the angle while only the full rational witness proves the bound.

`pingyou-n153-rational.yaml` states the same 153 squares as rational corners in this
repository’s Witness/v2 format, in JSON syntax.
The `witness-corners` adapter recovers each pose from its corners exactly.

## Against the Record

At `main` `3a5a91a90` the case record’s reported and verified ceilings are both
Siddharth Gupta’s refinement of a SQUISH packing, side
`2575935874665862918815262035657/200000000000000000000000000000` (T-127,
`E-gupta-438-exact-feasibility`). The certificate is below it by
`1933104584454118261245856857/200000000000000000000000000000`, about
$9.67 \times 10^{-3}$.

Two register entries are pending at 153, each rebuilt exactly from its packet:

- Evan Daniel’s regularization of SQUISH’s packing, T-146,
  `402250932783786874180075932249/31250000000000000000000000000`. The certificate is
  below it by `125999917133498187021808623/62500000000000000000000000000`, exactly the
  0.002015998674135970992348937968 the issue states.
- SQUISH’s T-136 (#481), $12.8720298490811808\ldots$, which T-146 regularizes.
  The certificate is below it by $2.0159986741368190 \times 10^{-3}$.

Of the other reports of 11 October, #500, #501, #503, #505 and #506 state no side at
153\. [acquisition/claims.json](acquisition/claims.json) freezes these comparisons, and
`devtools.upper_bound_reports` rebuilds them from the retained packets.

## Derived Fact and Exact Replay

`devtools.upper_bound_reports derive` read `n153.cert.json` from a checkout at the pin,
after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests above.
It admitted the certificate at the exact fraction the issue prints.
It then read `pingyou-n153-rational.yaml` from the same checkout, as the row’s
`same_packing` file: all 153 poses and the side are the certificate’s exactly.
It wrote the certificate as an exact rational `center-basis` Witness/v2,
[facts/n-153.yaml.gz](facts/n-153.yaml.gz), naming the certificate’s SHA-256 as
`revision_sha256`. The fact is this repository’s derivation; offline it must rebuild
itself from the certificate it states, and `derive --check` with a checkout compares the
fact and the witness again.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. A positive job, a duplicate-square control and an outside-container
control each ran in their own child process, one worker at a time.
The positive passes both routes and both routes refuse both controls.
Both routes find the least wall clearance exactly $1/10000000000000$ and the least pair
gap
`33179597140421157926909562845849204519671/175941977475349355327789470765625000000000000000000000`,
about $1.89 \times 10^{-13}$, the margins the source’s `native-replay.json` and
`exact-guard-audit.json` record.
The three jobs made 69,768 pair decisions in 24.09 route CPU seconds and 70.27 job wall
seconds, summed; the longest took 24.79 seconds, and the run 1 minute 23 seconds of wall
time, with other lanes on the machine.
`check --replay` decided all three jobs again in 49 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method.

The issue reports that `packing-witness verify` and
`devtools.check_rational_witness_independent` at `5b0eb012` accept the source’s own
witness file. The eleven files of this repository that
`native/upstream-source-manifest.json` names have the digests it records, and they and
the `packing-witness` command are unchanged from `5b0eb012` to `3a5a91a90`. Run here on
the pinned bytes of `pingyou-n153-rational.yaml`, both accept all 153 squares and 11,628
pairs with the margins above, in about 6 and 3 seconds including start-up.
Their outputs were not kept; the receipt above is the replay.

## What Is Not Established

The source reports that its three exact checkers accept all 11,628 pairs and every wall,
that `reproduce.py` rebuilds the certificate exactly from the table and recomputes the
guard, and that `derive_half_return.py` checks the symbolic identity behind the angle
and isolates its root.
Those are author reports.
`VERIFY.py`, `reproduce.py`, the three checkers, `derive_half_return.py`,
`convert_witness.py` and `replay_upstream.py` were read here and not run: the two
maintained routes decide the certificate from its own poses, so none is needed for the
bound. The derivation of the angle and the origin of the table in the n70 source bear on
the account of the construction and on credit, and were not checked here.
The replay above has not been reviewed.
The certificate establishes a finite upper bound only; the source claims no local or
global optimality, and no feasibility of the undilated algebraic contact solution.

## Credit

The source credits PingYou Ltd with the new n153 construction, Ryan Xu with the
underlying n70 construction ([#432](https://github.com/jlevy/squares/issues/432)), Evan
Daniel with the exact retention of that construction and with the refined prior n153
certificate (T-146), and Nate Chaoweeraprasit (SQUISH) with the prior n153 construction
([#481](https://github.com/jlevy/squares/issues/481)). The construction develops the
boundary-patch approach of its n207 result.
It claims neither the n70 packing nor patch composition in general.
The source makes no statement about AI assistance at this pin.
Asked on [issue #503](https://github.com/jlevy/squares/issues/503#issuecomment-6129716138)
which account stands, the author answered there on 12 October 2026, for this release and
the n207 one: “Both solutions were AI assisted by ‘PY’, an unreleased agentic AI offering
by PingYou Ltd.”

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-n153-certificate-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-certificate-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-certificate-2026-10-11 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-n153-certificate-2026-10-11 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone.
The importer’s `check-claims` and `check --replay` run offline from the fact;
`derive --check` needs a checkout at the pin, refuses one that does not yield this
packet’s record and manifest, and compares the fact and the source’s witness with the
certificate.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-153.yaml.gz` | receipt | `bd0b7599d516268fc197f84d797791adaa0a76d9` | `a7d54f513e4b1acdc710a0b39af9e2cca84fd09ee9c7dfdbc86ee2737bc85331` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
