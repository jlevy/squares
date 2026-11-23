# Exact Certificate Data from Issue #1037

Joost de Winter submitted rational pose certificates for 202, 204, 210, 263, 264, 295
and 297 squares and credited the underlying packings to Sergio Fernández Rubio
(GeiserX). The issue says de Winter tightened GeiserX’s published coordinates with Evan
Daniel’s contact solver.
De Winter reports that OpenAI’s GPT-6.2 Sol produced the certificates and algebraic
forms under his direction and Anthropic’s Claude checked them.
[Issue #1037](https://github.com/jlevy/squares/issues/1037)

## Acquisition and Credit

The packet pins `GeiserX_exact.zip` by its 1,989,212 bytes and SHA-256
`19c069b42d6a6fbe87dd419d358e7b046eadbba20dbaadd7f519faab1152c5e9`. The issue dates to
18 November 2026 and its current text to 20 November.
The retained attachment copy dates to 22 November 2026 at 19:53:36 UTC. The acquisition
record identifies each original and stored member and the basis of the retrieval
timestamp. [Acquisition record](acquisition/sources.json),
[Original attachment](https://github.com/user-attachments/files/35051652/GeiserX_exact.zip)

The issue identifies the upstream `data/submission-best.csv.gz` at
`c00281c2fb4b42a1c7071dc4fd493347cfd5a87b` as CC BY 4.0. The archive retains the
selected exact certificate files as submitted mathematical data under the
[retained-factual-data policy](../known-best-packings/README.md#retained-factual-data).
The upstream coordinates and the submitted certificate versions have separate custody.
The producer programs, prose, and checker receipts stay in the externally preserved
attachment.
[Pinned upstream data](https://github.com/GeiserX/squares-in-squares/blob/c00281c2fb4b42a1c7071dc4fd493347cfd5a87b/data/submission-best.csv.gz)

## Certificate and Review Scope

The seven rational `.cert` files preserve the original rows and exact sides.
The quadratic files preserve the two complete configurations and the 202 corner indices.
The independent review also keeps the rational Witness/v2 corner inputs for 202 and 263
as alternate encodings.
All 12 math members decompress to the original bytes.
They total 1,939,969 bytes before compression and 264,658 bytes in the packet.
The acquisition check matched the exact side and every corner set between the two
original rational encodings at all seven counts. Its paths refer to the full
attachment's scratch extraction. [Encoding comparison](acquisition/encoding-comparison.json),
[comparison program](acquisition/inspect_packet.py.txt)

| Count | Submitted rational side, rounded up to 12 places |
| ---: | ---: |
| 202 | 14.724372709109 |
| 204 | 14.802436041462 |
| 210 | 14.971210662216 |
| 263 | 16.724372709109 |
| 264 | 16.772843152678 |
| 295 | 17.698042929358 |
| 297 | 17.739455512004 |

The independent Stage 4 review accepts finite feasibility of both rational and quadratic
configurations at 202 and 263. It checks the exact quadratic sides and the 202-square
lower-left restriction.
The rational restriction equals the submitted standalone 202-square rational
configuration. In the submitted frame, the quadratic restriction has 119 poses in common
with the standalone quadratic certificate.
The issue’s trigonometric identity uses the magnitude of the common tilt.
The signed angle in the data is negative.
[Stage 4 review](../../../../docs/project/reviews/review-2026-11-22-geiserx-1037-202-263.md)

Both maintained exact routes accepted all seven rational certificates and refused
both the duplicate-square and outside-box control at each count.
The maintained exact field verifier accepted the two quadratic certificates and
refused both whole-certificate controls for each.
[Maintained rational replay](receipts/native-rational.json.xz),
[quadratic field replay](receipts/native-quadratic-202-263.json.xz)

The 297-square algebraic witness, whose side is reported as a root of a degree-70
polynomial, still awaits replay.
At 297, the issue attributes a 66-square bottom portion to Asterios Panoras’s version 17
compilation.
Pose identity with the pinned upstream input, prior registered packings, and
adoption are separate decisions.
[Issue #1037](https://github.com/jlevy/squares/issues/1037)

## Comparison with the Current Retained Certificates

For 202 and 263, the submitted rational sides are strictly below the prior retained
exact configurations at first contact. The gains are about 0.003549352 and
0.008793299 respectively. The quadratic sides are smaller again.
These comparisons check the predecessor's exact wall and pair inequalities.
Report order against other submissions and the drawing decisions remain open.
[202 comparison](receipts/n202-first-contact.json.xz),
[263 comparison](receipts/n263-first-contact.json.xz)

## Reproduce the Independent Review

Use CPython 3.14.7 with PyYAML 6.0.3. Start at the repository root with the original
attachment in external scratch.
The unchanged checker pins the entire attachment and reads seven mathematical members.
An archive reconstructed from the selected files has a different archive identity.
Follow the local external scratch and memory observation rules for a fresh run.

```bash
: "${TMPDIR:?Set TMPDIR to the task directory on the external scratch volume}"
review_dir=packing/resources/web/geiserx-exact-1037-2026-11-22/review
python -B "$review_dir/verify_202_263.py.txt" "$TMPDIR/GeiserX_exact.zip" \
  > "$TMPDIR/geiserx-1037-independent-replay.json"
```

The frozen plan and digests use the checker’s original filename, `verify_202_263.py`.
The reading copy adds a `.txt` suffix and preserves every byte.
[Frozen plan](review/plan.txt), [digests](review/frozen-sha256.txt),
[reading copy](review/verify_202_263.py.txt)

The receipt records exact geometry, field and side checks, nesting and controls.
The guard summary records CPU and memory observations.
Raw host telemetry and its process details remain in external evidence.
[Receipt](review/verification.json), [guard summary](review/guard-summary.json)

A checkout replay of the reading copy matched every non-timing field of the original
receipt. [Integration replay](review/integration-replay.json),
[review retention record](review/retention.json)

For standalone use of any preserved math member, run `gzip -dc FILE.gz` to recover the
original bytes. With the repository’s Python environment, run
`python -m devtools.retained_data check resources/web/geiserx-exact-1037-2026-11-22`
from `packing/` to check the stored files and the following table.

## Derived number-field facts

The maintained reader derives the 202- and 263-square facts in the original
number field and coordinate frame. It preserves the original witness
identifiers and every exact square pose. The per-count native receipts carry
the original three job records for each witness.
[202-square jobs](receipts/algebraic-route1-n202.json.xz),
[263-square jobs](receipts/algebraic-route1-n263.json.xz)

## Compressed Files

| Stored file | Origin | Git blob of uncompressed bytes | Decompressed SHA-256 |
| --- | --- | --- | --- |
| `facts/alg-n-202.yaml.gz` | receipt | `23c970b8910a9fea332d2b92de653cd40261c189` | `0ef261ed19a26fd14d6704380908f34d73aeeecc835f9f608713f875b581524f` |
| `facts/alg-n-263.yaml.gz` | receipt | `4a3d9f0e260005f6104d59eb5ccf40c35537bb5f` | `40599d936846114c450454018aa3f79477d25e991fc9b1f505f9a09c330c9284` |
| `review/inputs/rational/n202.yaml.gz` | upstream | `1e1a452ecbfcd684444c2e5a1ab0876dd29f60f1` | `480b7da10f09d4f4ae56fab1cd145e2a6deb80993263209e8e314c42a84d44d8` |
| `review/inputs/rational/n263.yaml.gz` | upstream | `a13e5943ce3d2cfad3ab98c2ee01a3ea52a120ed` | `3600e8dadccd9208ffd2e90820f94506e807c4b137d81123ae2ef85fa3f546c7` |
| `source/algebraic/n202.minpoly.json.gz` | upstream | `060a9012956ba6950a26c7fb5976f15966b397a0` | `f588cdc40027ff01c4b49f8ad1dbadacb50449b4941133a242e70974be908ffc` |
| `source/algebraic/n202_corner.json.gz` | upstream | `ba60650887dd9d78427c1d119d73a073a5e1a292` | `2c2e42b94bfd12d8166118b7c9e67dae48c08d3ef1d8f0935ec571fb3d75b674` |
| `source/algebraic/n263.minpoly.json.gz` | upstream | `d5b787cbfbb710dc22f481794d296e035363ffe2` | `092d7599ff0b3ead6d5281cd7bd3ffaef4b4a950eda22118e151b18b183b200e` |
| `source/rational/n202.cert.gz` | upstream | `32b440add36328207f76f21e7664e132156e96cf` | `9366d463b9f51cc6ea573673ef44056e6a6cfb2fe5c6315055613c5cfeb60d1c` |
| `source/rational/n204.cert.gz` | upstream | `d8d786821ffe8a08d9988d45a422a055514becf8` | `a603c189bf4e0fb340106774966701f676f3ef24f3917e089c026be29b0bdbd7` |
| `source/rational/n210.cert.gz` | upstream | `e83e95e16d62fe5c2ec17ac5179b2e641bc0ea19` | `7d5ceffded302ef593a86e1a60f67ce595871f6094c1feccff201c587bf062c0` |
| `source/rational/n263.cert.gz` | upstream | `1be5293fb36eef3307a0aca8120805cfeeb4aae9` | `3dd2fe786e77a78b6d912c4ed364c17c1d2d0ae3ae324a060dd8cab0408bef00` |
| `source/rational/n264.cert.gz` | upstream | `40ad9cf75095a9508261dc8fc49559617d9df459` | `3748968ad0956d2b4d54272715ba10d139030e40b627a7e5b989890e36e083b3` |
| `source/rational/n295.cert.gz` | upstream | `044d18e2835dbd10cedc4920ebb9f2588cdac82f` | `a64679104231b98a4528d8dc20502a0e889032ac1f50f4ea5da383785eff5cc1` |
| `source/rational/n297.cert.gz` | upstream | `43e2fa4100d19f24a0a0aa30e4e5d8374e18aafc` | `395cf9641de59262aeac43fe8c34204941becfd2dcbb6c3cc003620a0cdbb258` |

## Comparisons with the earlier packings

The retained GeiserX coordinates correspond one-to-one by nearest center to
each rational certificate in the submitted frame. The comparisons measure these
correspondences. At every count the rational certificate is strictly below
GeiserX’s corresponding published packing contracted to first contact.
[Seven measured correspondences and exact comparisons](review/published-coordinate-comparison.json)

At 202 and 263 the reviewed quadratic sides lie strictly below the submitted
rational sides and the preceding certified houses at first contact. At 263 the
quadratic side also lies strictly below the pending T-244 side’s lower isolating
endpoint. [Exact quadratic ordering](review/quadratic-standing.json)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
