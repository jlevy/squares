# ebdeleeuw: An Exact Rational Refinement at n = 70

[Issue #483](https://github.com/jlevy/squares/issues/483) reports an exact rational
certificate for 70 unit squares, a precision refinement of Ryan Xu’s packing, in
[ebdeleeuw/square-packing-n70](https://github.com/ebdeleeuw/square-packing-n70/tree/24221d5e51244ca5290d5b1c43f1fbe36f9749e0)
at `24221d5e51244ca5290d5b1c43f1fbe36f9749e0` (tree
`60b3fba53a2b752e13370c2c096e2851859122e6`, committed 2026-10-10T02:04:48Z, the
repository’s only commit). The source was retrieved at 2026-10-10T09:54Z.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 70 | `888096037156625096037155737/100000000000000000000000000` | 8.8809603715662510 |

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[Couzo twenty reports](../couzo-extended-reports-2026-10-08/README.md), this packet keeps
no upstream byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the
manifest. All six files of the tree are pinned only; the declared `source/` directory is
empty by design. Each is bound below to its Git blob at the pin and its SHA-256.

| Upstream path | Git blob | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- | --- |
| `certificate.json` | `f3002ff1e04111353258c3b12a347dbe60965de2` | 13908 | `eeebf55cf3c1614a96f51339695f28443e35f33b0195bfc24ef0549b50550cb1` | The certificate |
| `external-positive.txt` | `86b1e98488aef55bcef1bb2f7cc3d915c29fc533` | 9454 | `afc9376fae3baa1dfb43d037dce7eb88a0c85369622af1fb4974a56b2f829b87` | 60-digit decimal export |
| `external-positive.log` | `a3e5ca60998ba352b04c984843e6e9ed25d5a4d2` | 159 | `0c80020cb4bcdb8f339acaceb2cedcea3d9bdd2a65ab5b28034de2e1b4b30f85` | Author’s check output |
| `verification.json` | `6d012bd512e662f069a8a97e2d1ea393be4b8527` | 1617 | `fe7852ee34986ff89c76e8ca94a02fe5dcf4ce7f9e2b90d57c2bd11213dcf3e8` | Author’s results and timings |
| `verify_exact.py` | `9c07f0d0ada492d966a5767f7e2892752844f0cd` | 4164 | `8a7373a53119fd751ea38c5d65955d5260d8e4b4e3d70c4ce8a170feccdeb5fe` | Author’s checker, not run |
| `README.md` | `70153079ff7755c696da584e42dc6921dd91bdd9` | 1509 | `ab84a4599bd809e4823be132cf0daa2b6b63772a9b99968fc91284ac9588760c` | Author prose |

The certificate’s digest is the one the issue states, and `verification.json` records
the same digests for the certificate, the export, its log and the checker.

## The Certificate

`certificate.json` is a JSON object with `n` (70), `side` (a rational string),
`coordinate_system: "centered"` and `squares`, one `{x, y, t}` object per square, each a
rational string. The box is $[-S/2, S/2]^2$; a square’s rotation is
$\cos\theta = (1-t^2)/(1+t^2)$, $\sin\theta = 2t/(1+t^2)$, so every square is exactly a
unit square. The object’s `schema` field reads `sqpack-rational-v1`, which is the
source’s own label; this repository defines no format of that name.

## Against the Record

At `main` `657cc4861` the case record’s reported and verified ceilings are both Ryan
Xu’s certificate side `88809603717088809603717/10000000000000000000000`
(8.8809603717088810, T-125, `E-ryxu-432-rational-feasibility`). The claimed side is
exactly `14263000000014263/100000000000000000000000000` ($1.4263 \times 10^{-10}$)
below it, as the issue states. No other pending report names $n = 70$.
[acquisition/claims.json](acquisition/claims.json) freezes that comparison, and
`devtools.upper_bound_reports` rebuilds it with the case ceiling read from Ryan Xu’s own
packet.

## Derived Facts and Exact Replay

`devtools.upper_bound_reports` read `certificate.json` from a checkout at the pin, after
`devtools.acquire_source` showed that the checkout yields this packet’s acquisition
record and manifest, so the bytes it read have the digests above.
It translated every centre by $S/2$, exactly, into $[0, S]^2$ and wrote the certificate
as an exact rational `center-basis` Witness/v2,
[facts/n-070.yaml.gz](facts/n-070.yaml.gz), the deciding witness of the maintained exact
route, naming the certificate’s SHA-256 as `revision_sha256`.
The fact is this repository’s derivation; no upstream byte is retained.
Its side is the issue’s exactly, and offline the fact must rebuild itself from the
certificate it states.
The declaration of the import is [acquisition/report.json](acquisition/report.json).

Only the fact enters geometry decisions, through the two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. A positive job, a duplicate-square control and an outside-container
control each ran in their own child process.
The positive passes both routes and both routes refuse both controls, each on the
overlap or the wall it was built to break.
Both routes find the least wall clearance $6.01 \times 10^{-13}$ and the least pair gap
$1.20 \times 10^{-12}$. The three jobs made 14,490 pair decisions in 3.31 route CPU
seconds and 3.34 job wall seconds, summed; the longest took 1.12 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method.

## What Is Not Established

The source reports that its own exact checker accepts all 2,415 pairs and all 280
corners with zero tolerance, and that David Ellsworth’s `check_packing.py` at
`79f8a378d52e757d70f7cfb2c2f7a24a53da0204` accepts the 60-digit export at
$\varepsilon = 10^{-40}$. Those are author reports; no program of the source has run
here, and the replay above has not been reviewed. The certificate establishes a finite
upper bound only. The source claims no new arrangement family and no optimality, and its
generator and exact checker were written together.

## Credit

The source credits Ryan Xu with the arrangement, from his published warm-start
coordinates at `8dc415296f697f5140caea27c7a0193d52deb4e6` (issue #432), and Eric
Deleeuw (ebdeleeuw) with the refinement and the rational certificate. It discloses
OpenAI Codex assistance with the refinement, certificate generation, verification tools,
the external-checker replay and the submission.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source ebdeleeuw-n70-refinement-2026-10-10 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports ebdeleeuw-n70-refinement-2026-10-10 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports ebdeleeuw-n70-refinement-2026-10-10 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports ebdeleeuw-n70-refinement-2026-10-10 derive --checkout CHECKOUT --check
```

`--check` re-derives the record from this packet alone. The importer’s `check-claims`
and `check --replay` run offline from the fact; `derive --check` needs a checkout at the
pin, refuses one that does not yield this packet’s record and manifest, and compares
the fact it derives with the retained one.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-070.yaml.gz` | receipt | `e228ec3670ff2c6f1f29ce853abadf4d2c0013a8` | `211f669047683e84c5571dae7437e53d83679d2105d239641e6c442a33898f6c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
