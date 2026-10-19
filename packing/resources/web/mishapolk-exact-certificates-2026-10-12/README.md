# Mishapolk: Nineteen Exact Certificates at 336bdf5, n = 103 to 306

[Issue #573](https://github.com/jlevy/squares/issues/573), opened 2026-10-12T23:58Z,
reports exact rational certificates at six counts, in
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/336bdf5efab4784e54e0ac32edf3ed12f9c8af7e/certificates)
at `336bdf5efab4784e54e0ac32edf3ed12f9c8af7e` (tree
`fd1ce3dadf7e5125647a216cc0b11fc527c845c0`, committed 2026-10-12T23:52:23Z), the
revision the issue pins.
The source was retrieved at 2026-10-14T07:09Z, when the repository’s head was `ec87dc6`;
every certificate of this commit is unchanged there and at `46f638c`, the pin of the
same author’s [issue #593](../mishapolk-records-2026-10-14/README.md).

The issue was opened as “Exact rational certificates for 19 packings below register (n =
103–306)” and renamed by its author eight minutes later to the six it now names.
It had no comments when it was read at 2026-10-14T07:10Z.

| n | Printed by the issue, or else by the README at the pin | Requested |
| --- | --- | --- |
| 103 | 10.679232047362 | yes |
| 153 | 12.870013850405 | yes |
| 207 | 14.880960371558 | yes |
| 209 | 14.946223226448 | yes |
| 258 | 16.563448002138 | yes |
| 270 | 16.929775353544 | yes |
| 108, 127, 131, 154, 175, 180, 236, 237, 263, 267, 302, 303, 306 | the exact fraction the README’s table states | no: dropped when the issue was renamed |

The issue prints each side rounded up at 12 places from the certificate’s header, and
each of the six admits at its print.
The README at the pin states every side as an exact fraction, and each of the other 13
certificates’ headers equals it.
All six SHA-256 digests the issue lists are the digests of the pinned files.

## What the Issue Reports

- **Lineage.** 103 continues Ryan Xu’s arrangement (#432), refined by SLSQP on active
  contact graphs and exact rational finishing, “Please retain his construction credit”;
  258 continues Nate Chaoweeraprasit’s (SQUISH) arrangement from the register; 153, 207
  and 209 are new arrangements from basin hopping with tilted boundary corridors, and
  270 a new arrangement from basin hopping, each with exact rational finishing.
- **Checks.** This repository’s `sqpack/verify.py` at `562fdbd` and Evan Daniel’s
  `verify_cert.py` at `31523f8` accept all six in exact arithmetic.
  The README at the pin lists five engines and attributes all five to David Ellsworth,
  among them `devtools.check_rational_witness_independent`,
  `devtools.check_half_angle_area` and `devtools.decimal_pose_margins`, which are this
  repository’s tools. No source program ran here.
- **Not claimed.** Feasibility only; no local or global optimality proof.
- **AI assistance.** “The search implementation, verification orchestration, and issue
  preparation used Gemini.
  I directed the work.”

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for Mishapolk’s
[#470 packet](../mishapolk-decimal-poses-2026-10-09/README.md), this packet keeps no
upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
All 117 files of the declared scope, 3,249,073 bytes, are pinned only: the README
(SHA-256 `c84e622d2e268c1b245f05fd7c72a0bc9a7c33f8cd84336cc59303a6a44a5d75`),
`certificates/census.json`
(`004d850158172b4a8e82e175ee16452e5e6d278b53d2dad5f5d866b801677fe3`), the 19
certificates, 48 decimal poses and 47 drawings, and the copy of `check_packing.py`,
never executed here.

| n | Certificate | Bytes | SHA-256 |
| --- | --- | --- | --- |
| 103 | `certificates/square-103.cert` | 8589 | `044ab54af75be78261f64fe7e6bd99f02f0a650fe13c5355714102e31432365c` |
| 153 | `certificates/square-153.cert` | 12540 | `8c012a7207a4762c48fbd68577f5b20771d0be66a401a90b7d09b549a50f15bf` |
| 207 | `certificates/square-207.cert` | 16173 | `3cc901c7096406d0c1d7a2daf23860ad65758b3b133a103d0e5ebd3ab9a34b41` |
| 209 | `certificates/square-209.cert` | 16852 | `f5aa5aa77ce5b95914b9048884d519ef03ce2a14fe95a14ab01517a157b8ea1d` |
| 258 | `certificates/square-258.cert` | 20373 | `580be390e8307ffc9e3ce1f613098e8c6734f8b5cf9266d2ca29255fc9948a45` |
| 270 | `certificates/square-270.cert` | 21403 | `7dd96e6455e03cfab11a6b63d6fbce4b071b16445d1beec0b7f5288c7abe0185` |

The certificates at 103, 153, 207 and 258 are, byte for byte, #593’s `n103.cert`,
`n153.cert`, `n207.cert` and `n258.cert`; those at 209 and 270 are not.

## Derived Facts

`devtools.upper_bound_reports` read all 19 certificates from the checkout at the pin,
after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests above.
It wrote each as an exact rational `center-basis` Witness/v2 under `facts/`, naming the
certificate’s SHA-256 as `revision_sha256`. The facts are this repository’s derivation;
offline each must rebuild itself from the certificate it states.
Every side is a short terminating decimal, with 11 to 14 places.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each of the 19 certificates
against the record at `main` `b8c930338` (14 October 2026), and `check-claims` rebuilds
it: each case ceiling from its holder’s own packet, each register entry at the count
from its own packet or the bound its claim states, and each open report from the side it
prints. The open reports are those of the
[#593 packet](../mishapolk-records-2026-10-14/README.md#against-the-record), with #593
itself read from its own packet at 209 and 270, where its certificates differ from
these.

**No certificate of this release is the smallest known side at its count.** Of the six
the issue requests:

- **153 and 207 are below the case**, PingYou Ltd’s T-148 and T-147, by
  $2.56 \times 10^{-12}$ and $1.49 \times 10^{-9}$, the margins the issue states, and
  below PingYou’s later #504 and #503 refinements by $2.55 \times 10^{-12}$ and
  $5.56 \times 10^{-13}$. PR #574 states smaller sides at both, by
  $1.57 \times 10^{-14}$ and $2.42 \times 10^{-12}$.
- **103 and 258 are above the case**, by $4.36 \times 10^{-14}$ and
  $3.38 \times 10^{-12}$. Both cases now hold Evan Daniel’s regularization (T-146) of
  Mishapolk’s own #470 packings, registered on 10 October; the issue compares with the
  ceilings before it.
- **209 is above the case**, Couzo’s T-140, by $1.55 \times 10^{-12}$, and #593’s 209 is
  the case’s certificate itself, byte for byte.
- **270 is above the case**, SQUISH’s T-151, by $1.58 \times 10^{-3}$; #593’s later 270
  equals the case to within $10^{-21}$.

Of the 13 the renamed issue dropped, 154 and 175 are below the case, by
$5.04 \times 10^{-4}$ and $2.95 \times 10^{-3}$, and Couzo’s #586 (at 154, by
$1.36 \times 10^{-3}$) and PR #574 (at 175, by $1.40 \times 10^{-12}$) are smaller.
The other 11 are above the case, by $1.7 \times 10^{-12}$ to $7.2 \times 10^{-3}$. At
108 the side equals Mishapolk’s own #470 ceiling (T-138).

The full comparison, smallest first among the other reports:

| n | Side, rounded up at 16 places | Against the case ceiling (holder) | Smaller or tied reports | Smallest |
| --- | --- | --- | --- | --- |
| 103 | 10.6792320473613500 | above by $4.36 \times 10^{-14}$ (ry-xu, improved by Mishapolk, Evan Daniel, T-146) | PR #574 (PingYou) smaller by $4.36 \times 10^{-14}$ | PR #574 (PingYou) |
| 108 | 10.9048210123240000 | above by $3.64 \times 10^{-12}$ (ry-xu, improved by Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $3.64 \times 10^{-12}$; T-138 (#470) equal | PR #574 (PingYou) |
| 127 | 11.8108787875930000 | above by $3.82 \times 10^{-12}$ (ry-xu, improved by Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $3.82 \times 10^{-12}$; T-138 (#470) smaller by $3.00 \times 10^{-12}$ | PR #574 (PingYou) |
| 131 | 11.9511124689660000 | above by $1.45 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), T-136) | PR #574 (PingYou) smaller by $1.45 \times 10^{-3}$; T-128 (#451) smaller by $7.08 \times 10^{-6}$; T-138 (#470) smaller by $7.08 \times 10^{-6}$ | PR #574 (PingYou) |
| 153 | 12.8700138504044800 | below by $2.56 \times 10^{-12}$ (PingYou Ltd, T-148) | PR #574 (PingYou) smaller by $1.57 \times 10^{-14}$ | PR #574 (PingYou) |
| 154 | 12.9225664019360000 | below by $5.04 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), T-136) | #586 (Couzo) smaller by $1.36 \times 10^{-3}$ | #586 (Couzo) |
| 175 | 13.7641743174880000 | below by $2.95 \times 10^{-3}$ (ry-xu, improved by Francisco Couzo, T-140) | PR #574 (PingYou) smaller by $1.40 \times 10^{-12}$ | PR #574 (PingYou) |
| 180 | 13.9169935224830000 | above by $5.17 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $5.17 \times 10^{-12}$; T-138 (#470) smaller by $1.00 \times 10^{-12}$ | PR #574 (PingYou) |
| 207 | 14.8809603715580000 | below by $1.49 \times 10^{-9}$ (PingYou Ltd, T-147) | PR #574 (PingYou) smaller by $2.42 \times 10^{-12}$ | PR #574 (PingYou) |
| 209 | 14.9462232264480000 | above by $1.55 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-140) | PR #574 (PingYou) smaller by $1.55 \times 10^{-12}$; #593 (Mishapolk) smaller by $1.55 \times 10^{-12}$ | PR #574 (PingYou) |
| 236 | 15.8639557471610000 | above by $1.73 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $1.73 \times 10^{-12}$; T-136 (#481) smaller by $1.73 \times 10^{-12}$ | PR #574 (PingYou) |
| 237 | 15.9029496076800000 | above by $2.17 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-140) | PR #574 (PingYou) smaller by $1.83 \times 10^{-6}$; #561 (Couzo) smaller by $1.83 \times 10^{-6}$ | undecided: #561 (Couzo), PR #574 (PingYou) |
| 258 | 16.5634480021371700 | above by $3.38 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Mishapolk, Evan Daniel, T-146) | PR #574 (PingYou) smaller by $3.38 \times 10^{-12}$ | PR #574 (PingYou) |
| 263 | 16.7404126537570000 | above by $7.25 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $7.25 \times 10^{-3}$; T-136 (#481) smaller by $7.25 \times 10^{-3}$ | PR #574 (PingYou) |
| 267 | 16.8388152699500000 | above by $1.74 \times 10^{-12}$ (ry-xu, improved by Francisco Couzo, T-134) | PR #574 (PingYou) smaller by $1.74 \times 10^{-12}$ | PR #574 (PingYou) |
| 270 | 16.9297753535440000 | above by $1.58 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), T-151) | PR #574 (PingYou) smaller by $1.58 \times 10^{-3}$; #593 (Mishapolk) smaller by $1.58 \times 10^{-3}$; T-140 (#488) smaller by $2.64 \times 10^{-12}$ | PR #574 (PingYou) |
| 302 | 17.8720298490830000 | above by $1.82 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | #583 (Couzo) smaller by $2.02 \times 10^{-3}$; PR #574 (PingYou) smaller by $1.75 \times 10^{-3}$; #564 (PingYou) smaller by $1.75 \times 10^{-3}$; T-136 (#481) smaller by $1.82 \times 10^{-12}$ | #583 (Couzo) |
| 303 | 17.9130654627410000 | above by $2.47 \times 10^{-12}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | PR #574 (PingYou) smaller by $3.11 \times 10^{-3}$; #562 (Ostashev) smaller by $3.11 \times 10^{-3}$; T-136 (#481) smaller by $2.47 \times 10^{-12}$ | PR #574 (PingYou) |
| 306 | 17.9634337174980000 | above by $6.57 \times 10^{-12}$ (Francisco Couzo, T-128) | PR #574 (PingYou) smaller by $6.57 \times 10^{-12}$; T-138 (#470) smaller by $1.00 \times 10^{-12}$ | PR #574 (PingYou) |

## Exact Replay of Four Counts

Only the facts enter geometry decisions, through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. No certificate here is the smallest at its count, so the replay covers the
four below the case: 153 and 207, which the issue requests, and 154 and 175. Each ran a
positive job, a duplicate-square control and an outside-container control, each in its
own child process, on one worker.

All four positives pass both routes, and both routes refuse all eight controls, each on
the overlap or the wall it was built to break.
In each positive the two routes find the same least wall clearance and the same least
pair gap: at 153, $1.20 \times 10^{-15}$ and $6.38 \times 10^{-16}$; at 154,
$7.43 \times 10^{-14}$ and $1.50 \times 10^{-13}$; at 175, $5.19 \times 10^{-14}$ and
$1.01 \times 10^{-13}$; at 207, $8.07 \times 10^{-14}$ and $1.61 \times 10^{-13}$. The
12 jobs made 359,730 pair decisions in 93.79 route CPU seconds and 205.66 job wall
seconds, summed; the longest job took 23.93 seconds.
The one-worker `certify` took 4 minutes 17 seconds of wall time, 07:35:08Z to 07:39:25Z,
at a load average of 9 to 13 on four cores, and a fresh serial `check --replay` decided
all 12 jobs again, equal to the retained rows apart from timing, in 1 minute 49 seconds,
07:44:34Z to 07:46:23Z.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the source’s code.
The third exact route (`devtools.check_half_angle_area`) has not read these
certificates.

The other 15 were not replayed.
By the kernel jobs measured for this lane they are 18 to 31 minutes of one-worker wall
for `certify` and as much again for `check --replay`, with no job near the kernel’s
600-second limit. Each is above its case, and the certificates at 103 and 258 are also
#593’s files.

## What Is Not Established

The replay establishes that the four packings at 153, 154, 175 and 207 are packings at
the exact sides their certificates state.
It establishes nothing about the 15 not replayed, or about optimality, which the source
does not claim.
The source’s checks are the author’s reports; no source program ran here.
This packet compares sides only and makes no finding about where a packing came from.

## Credit

The issue credits Ryan Xu’s construction at 103 and Nate Chaoweeraprasit’s (SQUISH) at
258, and calls 153, 207, 209 and 270 new arrangements.
At 103 and 258 the case now holds Evan Daniel’s regularization of Mishapolk’s #470
packing, below these sides.
The README at the pin calls 153, 154, 175, 207, 209, 237, 263, 267 and 270 “brand new
geometric topologies” and the others refactorings or quenches of named authors’ layouts.
The issue discloses that Gemini was used for the search implementation, verification
orchestration and issue preparation, directed by the author.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source mishapolk-exact-certificates-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-exact-certificates-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-exact-certificates-2026-10-12 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-exact-certificates-2026-10-12 derive --checkout CHECKOUT --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-exact-certificates-2026-10-12 register-plan
```

`CHECKOUT` is a clone of the source at the pin.
`check-claims` and `check --replay` run offline from the facts; `derive --check` refuses
a checkout that does not yield this packet’s record and manifest, and compares each fact
it derives with the retained one.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-103.yaml.gz` | receipt | `8b4e2c9ef246161200fa0184b697b87a4a4b7c5d` | `91a818074c50f25d2957174f85b28e1a30ba91fe487cdee28afc454642167e02` |
| `facts/n-108.yaml.gz` | receipt | `efb6108fdaad349bfc6c8b63f05cbacaf057ad87` | `0f079df555e11bac050f17b0fdb465b483e700936ae4909d67286035ee4b9bd1` |
| `facts/n-127.yaml.gz` | receipt | `720f2b0ed6182763a4080a01717726e51391420e` | `6db8d9ca9a14f1a4d2123ea1488c55902ac86d2924bc3e904d1df74843a4ee27` |
| `facts/n-131.yaml.gz` | receipt | `d6f94de395614b67974972b56017a80638007034` | `d5cccf4867304d3b5a957e2c32995076d723127da504c3ce2bcf3b54cb373c01` |
| `facts/n-153.yaml.gz` | receipt | `0c82ef0562f8d9bdd55018d938f2f6eb79ec1b57` | `4e2e5ebd1e7adb67f64ab82a45ef8de7f791ba3235737e035a071a831c53e4c4` |
| `facts/n-154.yaml.gz` | receipt | `221096b6aca9c6c65d3fcef972879fff1558d822` | `512f3f96379861ba0c911c30a7a552d5c4b366933da7adc86d554e30c819429a` |
| `facts/n-175.yaml.gz` | receipt | `85707a1ddc32246eec10593d2ca1406d06744cd1` | `9076667185d845ea8d98b6c925f99b3cdf6265f5d3e327a7be5895a06cddbf34` |
| `facts/n-180.yaml.gz` | receipt | `741fee84f6c44babf4ffd0d9c0fb5e57069667bd` | `191a3548e948887cff967adfdd6e953e704b0f90300fe5e1dd57a10ca33032e6` |
| `facts/n-207.yaml.gz` | receipt | `145eb49047bb3b634c5804b5ce7f67b972956c9a` | `becee043a7f4e68a5fcb43e4f2723f4ca8f511348679f39d222a475432af3a8e` |
| `facts/n-209.yaml.gz` | receipt | `6a13cdf14c549a3cf3476d3f7959b7135555c47c` | `f4159ca1e28889f170f5057ade6ad1adc40cebe84dab70aa0f224bea70ea00d8` |
| `facts/n-236.yaml.gz` | receipt | `e67decc0af46818df081780d36ebdc64fc6c733a` | `e27346e01a869b39529526a3408283b17875ddc3b358ce7e68a8f1eb3da40f9b` |
| `facts/n-237.yaml.gz` | receipt | `b28942908bcd0c727d3f7b1f8a29c30da67ab8b1` | `875cde3248dabb01cdb971b6d47f97cd002878de0810bdf182747b616183cddf` |
| `facts/n-258.yaml.gz` | receipt | `aa42be615c77b80059bb72fbf320800dd590bb6c` | `55cc697d06375f6e165a0ef12bed04bcaf51cd9060c1ad5bde36d7161316ecb8` |
| `facts/n-263.yaml.gz` | receipt | `f6192c50c87fcc46dee685d8fdcb0430c8365ec0` | `d23c34245293de774c9cf7ef8720c3237389906554fed3b697beb0071d7622df` |
| `facts/n-267.yaml.gz` | receipt | `252c5d717dccc272cf813c65a232001b05ce09d4` | `58bbee74aa5b2b057ecb0dcac8434e3a8e08ca272a68dcf3e687ef567917c249` |
| `facts/n-270.yaml.gz` | receipt | `50259026901fe37981769de7c56d60e28b4df0f5` | `2ff8a737ba051369267b7ca9ae8383bee82d0aa1398549f31394922d0dea3965` |
| `facts/n-302.yaml.gz` | receipt | `46dbb16b17fe9edf19cc70856169505189db1314` | `36dd30d0a8ba4bb06b57898db086023b885b534a493b883bd546e5076cdf155c` |
| `facts/n-303.yaml.gz` | receipt | `5a5cc80e41018f8744986c416808156c0267d27e` | `49348c9b515d28d21a5400715a77a11be1a5d9dd00c20ce745d0c2cb345f652a` |
| `facts/n-306.yaml.gz` | receipt | `05e887848157ebd46ef240b53c756759e3d4e5e5` | `904b908945925be90f06ad6eb02365409e242afe874b30ef19c761bb368884dd` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
