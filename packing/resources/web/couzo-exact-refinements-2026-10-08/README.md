# Francisco Couzo: Eight Exact Rational Refinements

[Issue #451](https://github.com/jlevy/squares/issues/451) reports constructions at
$n=105,108,127,131,155,180,228,306$. This packet retains all eight complete rational
certificates and all eight decimal poses from
[the pinned source](https://github.com/franciscouzo/square-packing/tree/ffd900dfff6d2674ad995359208c2f0714915c82).

The certificates contain exact centres and rational half-angle parameters.
The decimal poses are separate source context: their printed side and geometry need not
equal the certificate.
Only the certificates enter maintained geometry decisions.

The author credits Ryan Xu’s #432 constructions at 105, 108, 127 and 131; Nate
Chaoweeraprasit’s SQUISH constructions at 155 and 180, with 180 refined through
Siddharth Gupta’s #438; and Couzo’s constructions at 228 and 306. Reported refinement
tools include David Ellsworth’s refine_packing, Couzo’s basin hopping and Evan Daniel’s
fq. The issue also credits Claude Code under Couzo’s direction.
These are source attributions, not independent priority findings.

The source reports passes from Evan Daniel’s checker and a copy of this repository’s
sqpack verifier. The maintained replay uses existing exact_verify and independent
arrangement routes; both share certificate parsing, half-angle conversion, Fraction
arithmetic and the separating-axis method.
One source checker derives from this repository, so route count alone does not establish
implementation independence from the source producer.

Acquisition and source admission are complete.
Maintained native replay remains pending.
No standing house or bound changes occur in this preparation packet.
Optimizer, KKT, local-minimum, global-optimality, rigidity, novelty and human-review
claims remain outside the admitted scope.

## Source Custody

All 16 factual source files match their pinned Git blob, size and SHA-256. Their 310,209
decoded bytes occupy 61,867 deterministic gzip bytes.
The two upstream READMEs are hash-pinned without copying unlicensed prose; the full
126-blob Git tree is retained as acquisition metadata.
The optimizer’s MIT notice does not license the complete bundle.
No author program executes.

The maintained acquire_source and retained_data contracts check the declaration,
complete original-byte map and compression table.
Derived facts bind each full source text to that independent acquisition map before
parsing. A proposed native receipt must retain all 24 jobs: positive, duplicate square
and outside-container controls for every certificate, with both complete route results
and pair counts. The unchanged child deadline is 45 seconds.

## Compressed Files

| Stored file | Origin | Git blob of decompressed bytes | SHA-256 of decompressed bytes |
| --- | --- | --- | --- |
| `source/certificates/n105.cert.gz` | upstream | `d2e337c9217b3b2a29a4e8de4668936d6cd647f6` | `6f22b0cf51cf6ff8d4c2d930995a044daada5de8c4a99e211ae7fe545211384b` |
| `source/certificates/n108.cert.gz` | upstream | `b7bc8379c1180e20be6c06e410ed9ff0b2c4d7ed` | `528741a37ad0ae6ddd4c08d6d6efa72a29700bd95fde137b44c987f18d44d69e` |
| `source/certificates/n127.cert.gz` | upstream | `9a0f17cd25525ee8c90d98743275cc9bd6c2da61` | `2e039a654aa7afbeb9c8f447833aa8e9ff64f70e218c5fce0f2eb13435cda3a9` |
| `source/certificates/n131.cert.gz` | upstream | `00253359b72a422af851a7142ead7dcffbd9d708` | `9ce74fda03fac60e997a3e0d1175cb6d3a6563523d7305ab3af08a9ad30b169c` |
| `source/certificates/n155.cert.gz` | upstream | `22e0d557802f0df172ae6fd7d4304435d9b57c49` | `cc9f7c800211acc21c66196c43fab392dd96c920eba8f13851ff313c8e1bb477` |
| `source/certificates/n180.cert.gz` | upstream | `54efb6b67c0fbe217e1472ebd210684e8ccb7928` | `a66d49e35a3c841df0ca1daf5bb364f36139b36ae5126fbf21200ebd6db4128e` |
| `source/certificates/n228.cert.gz` | upstream | `c3351d524d41eec2221cccaf285a9b87e6bd6cef` | `cb5e49904ac5e4b548bf6c20cbcb4d0a72f52ccc0eee6a36c784d4c3495d38ad` |
| `source/certificates/n306.cert.gz` | upstream | `601038fdfae10fbac4395da6bd6ca3d4bfa11541` | `f58de39d385fcc006f7e6f967e16640ff3471534b6cb54aadcd59be14df0b3c7` |
| `source/n105.txt.gz` | upstream | `b5258293beedc27d5deb22e986762af179087384` | `f7e35af93307e169f6f5db6715085e336d15c25b76b46bfec45c068893783bfd` |
| `source/n108.txt.gz` | upstream | `05d614e217868d25a9983be658d85b2752e8b1b4` | `8fc5b716f2bd761c544490e82c81b22a27b61ef91e415e9ab463a82fd55d40f7` |
| `source/n127.txt.gz` | upstream | `98c9e2602dfe78758380da53001d47517c89a683` | `510c4f816468050006892a294f49d794de16b71356dbf55d0de3d3f749800bf2` |
| `source/n131.txt.gz` | upstream | `8a047ed58bbd9960d5704962eb141ea07bbfbc2f` | `196daf9edfbd987efa18d92b1708b5df42a050d3043748e7a146f4eff91d4c7e` |
| `source/n155.txt.gz` | upstream | `f6ba1c3e5aef6d27a83976ba3aa8ee84ddf1e13b` | `b2dd538c4f102058b1561652fa5f83c79c1e995fae6f3da3fbcb4573511c48ee` |
| `source/n180.txt.gz` | upstream | `431aca33894de053400c9dfaaf5ef7cb65ce648b` | `855a88d9bbbe5b8558f380ac5368eb50b8a78837c547d5b5bdb40a4d7204b638` |
| `source/n228.txt.gz` | upstream | `bf97337668c13514cdacda5ffefc71e88146a358` | `157be40980af0925adf87b3272e95e6db81c4a881f46c1d45dd0449a347c21e0` |
| `source/n306.txt.gz` | upstream | `0cdfc9f02c6eb7e25e50e9ef00758ed39968ed0e` | `2c3ecf4b3937b5b33ee2cebfeeb89ac2080d4c69a989317f0512b2f94850ee44` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
