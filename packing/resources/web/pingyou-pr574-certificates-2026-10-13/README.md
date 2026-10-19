# PingYou Ltd: Certificate Refinements of PR 574

[Pull request #574](https://github.com/jlevy/squares/pull/574) (BuddenPing, opened
2026-10-13T00:13Z), titled “research: submit 148 square-packing certificate refinements
with exact endpoints”, is read here as an intake report.
It was not merged, approved or commented on.
Its head is
[`4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde`](https://github.com/BuddenPing/squares/tree/4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde)
of the fork BuddenPing/squares, branch `codex/numerical-certificate-refinements` (tree
`b5273e75f92f8c5dee022bd778bb9713615adc3b`, committed 2026-10-13T01:58:38Z), eleven
commits over the base `e96e9ea95c15c6ad3a9a547a8cb02760e721cfc4`. It was fetched by
commit id and read at 2026-10-14T07:37Z, when it had no comments or reviews.

The pull request adds ten small files, three HostedData manifests and three submission
packets. The geometry is not in Git: the manifests pin four release assets of
[BuddenPing/square-packing-certificates](https://github.com/BuddenPing/square-packing-certificates)
by size and SHA-256, and the certificates are members of those zip archives.
This packet pins all of it and keeps derived exact facts.

## What the Pull Request Claims

It submits complete certificates at 148 counts from 5 to 308, each a tighter
certificate of a packing that someone else found:

| Part | Counts | Certificates |
| --- | ---: | --- |
| v2 release, rational, still current | 86 | Centre and half-angle JSON, and the same packing as a corners Witness/v2 |
| Algebraic supplement over Q(√2) | 48 | Centre-basis Witness/v2 over the field, and the author’s geometry JSON |
| Algebraic supplement, other fields | 10 | N18, N234, N299 over Q(√7); N54, N107, N178 quartic; N151 biquadratic; N53 degree 8; N70 and N207 degree 5 |
| Algebraic supplement, rational | 2 | N146, and N261, which is outside the 147 counts of v2 |
| Exact N153/N302 supplement | 2 | N153 in a degree-7 field, N302 in a cubic one |

The supplements replace 61 of the 147 v2 certificates; the v2 certificates they replace
are earlier claims of the same pull request and are not compared here.
The submission’s `COVERAGE-147.json`, in the algebraic archive, gives each v2 count a
disposition: 59 improved by the supplement, 82 kept pending algebraic reconstruction, N50
and N171 already exact rational (53/7 and 95/7), N153 and N302 already exact algebraic,
and N204 and N264, where the older radical constructions are dominated by the kept
rational ones.

The submission says that these are padding reductions and exact attainments of known
constructions, not 148 new nominal constructions, new algebraic optima or optimality
proofs. Its own checks are author reports: a standard-library exact SAT and polygon
checker accepting every certificate and its predecessor and refusing duplicate-square and
outside-container controls, with 2,678,449 pairs for v2 and 917,302 for the supplement, a
Sturm-count isolation of each declared root, and this repository’s two verifiers,
unchanged at `e96e9ea`, accepting every native witness.

## Source Custody

The pull request adds its files under `packing/resources/`, which the repository’s
`LICENSE` names as third-party material outside its grants, and each submission README
says that it asserts no new blanket licence over geometry or source material.
The release repository has no licence file, and GitHub detects none.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md) this packet keeps no
upstream byte, and no redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the acquisition record from a no-checkout worktree at the
pin, into which the ten files were extracted from the commit; each is bound to its Git
blob there. [acquisition/declaration.json](acquisition/declaration.json) is the
declaration, [acquisition/sources.json](acquisition/sources.json) the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `packing/hosted/pingyou-numerical-refinements-2026-10-13.yaml` | `635469d9b31db29ff959a8427d3c2112bd2a9e66` | 830 | `5626f0e1f887d2abf8fbcc168a5a2b12d00c6a8b014059737da1aea70f5acca0` |
| `packing/hosted/pingyou-algebraic-refinements-2026-10-13.yaml` | `2d6f67a9148dc3ce040d307dac91d9f96bd5ab12` | 616 | `e2696c0ca1cc4b9db5d208d56982f7a9af29bebe84eaf1e7f5d9321d84fb4a45` |
| `packing/hosted/pingyou-exact-153-302-2026-10-13.yaml` | `adc0b44f01a470f53e0bb436ef38faf99bd8d606` | 589 | `5a4aab8861e4c3aff36354e253e687402f5ba568f19dee636eea0f26e5de0ef0` |
| `packing/resources/web/pingyou-numerical-refinements-2026-10-13/README.md` | `345220ccfe9953e5a50a848416632de68b0ac3d2` | 6756 | `56e8c951c8cfd23254625d7fd3e17f2b4bc541533826b47c766421adf4aa97bd` |
| `packing/resources/web/pingyou-numerical-refinements-2026-10-13/claims.json` | `d394e65d4971c721a0a88164f8112e054a483038` | 753807 | `1cb5110dd26933812e0f340c17b466674a131e449d23f1691e92476e7e18980d` |
| `packing/resources/web/pingyou-numerical-refinements-2026-10-13/comparison.json` | `b0bac77770fbe0089feb647e7c038e0713e2a4cc` | 507124 | `a16fe93d193d5e0a5e002465cfe2989216b2135a99948da5c9a3083f857771ce` |
| `packing/resources/web/pingyou-algebraic-refinements-2026-10-13/README.md` | `0b92e236b2632f3f178987e9f47e48b2e348375e` | 4609 | `323a803ce81c95ad8558249d4f573cdb0c5f8323b9db5e7a45cf869dac225368` |
| `packing/resources/web/pingyou-algebraic-refinements-2026-10-13/claims.json` | `ba2258f8dc5005406d2c875701e09295cb596876` | 234016 | `2c1bd9340152abd6e2a234bb3e53c0cb13006ffa567c14836e99da3c1294c343` |
| `packing/resources/web/pingyou-exact-153-302-2026-10-13/README.md` | `b0aed888ad826aa89ea4de35b5dd10b8b5a8cb4d` | 4321 | `c1bbb6d7d963185333c21958c44b5cb62c433f3552b4dc74a25003caa84ed6be` |
| `packing/resources/web/pingyou-exact-153-302-2026-10-13/claims.json` | `7a64f128932878dfca984410d67e7d5f0c357a23` | 3061 | `d2cbe5ed5697b1a0d51001d253272f857013dcc0dbf29a7b8d7daee99ae93a30` |

### The Release Assets

All five release tags of the source repository point at its head
`318ab94e821ba7280a68fa8ce2942c9ecdbda41d`, which holds none of these files.
The assets were downloaded with `gh release download` at 2026-10-14T07:37Z, and each has
the size and SHA-256 its manifest pins and that GitHub reports for the asset:

| Tag | Asset | Bytes | SHA-256 | Published |
| --- | --- | ---: | --- | --- |
| `data/pingyou-numerical-refinements-2026-10-13-v2` | `pingyou-numerical-refinements-2026-10-13.zip` | 7754365 | `ced042973412d43217aab66b5c07fe6242e019a8280efc20bb99650c97892249` | 2026-10-13T00:24:11Z |
| `data/pingyou-numerical-refinements-2026-10-13-v2` | `pingyou-native-witnesses-2026-10-13.zip` | 21737024 | `da66aa5f4db954765988c3f7cf3d405b71aa9112ac494b6e3b82b2ea1dbdcb85` | 2026-10-13T00:24:11Z |
| `data/pingyou-algebraic-refinements-2026-10-13-v1` | `pingyou-algebraic-refinements-2026-10-13.zip` | 2815986 | `26b31abea665a7d22547f61eb041392b2bde303a9a702ac1a7ae35dc5f319062` | 2026-10-13T01:56:45Z |
| `data/pingyou-exact-153-302-2026-10-13-v1` | `pingyou-exact-153-302-2026-10-13.zip` | 235073 | `cea5e95dc3c7a719582a2f58f24fd89171c9b29424c913513373092465783814` | 2026-10-13T01:17:28Z |

Each archive’s own `SHA256SUMS` agrees with every file it lists: 603, 613, 444 and 41
files. The algebraic archive’s `claims.json` is byte-identical to the pull request’s; the
exact archive’s differs from it only in its release address.
The v1 assets of the numerical release, which v2 supersedes, were not downloaded.

## What Is Retained

Every certificate enters a decision only through a derived fact, written by `derive`
from a checkout at the pin and the assets: the manifest is read from the checkout, the
asset must have its size and digest, and the member must have the digest the declaration
states, which is the one the pull request’s claim record prints.

- **85 rational facts**, `facts/n-NNN.yaml.gz`, exact rational centre-basis Witness/v2,
  declared in [acquisition/report.json](acquisition/report.json) for
  `devtools.upper_bound_reports`. 83 come from the v2 certificates, each admitted at
  the 40-place side the claim record prints and each equal, pose for pose, to the
  corners Witness/v2 of the native archive; N146 and N261 come from the supplement’s
  rational centre-basis witnesses (the `witness-center-basis` adapter), admitted at the
  exact fractions the claim record prints.
- **60 algebraic facts**, `facts/alg-n-NNN.yaml.gz`, the field, side and squares of each
  algebraic witness exactly, declared in [acquisition/algebraic.json](acquisition/algebraic.json)
  for `devtools.algebraic_witness_reports`.
- The frozen comparisons, [acquisition/claims.json](acquisition/claims.json) and
  [acquisition/algebraic-claims.json](acquisition/algebraic-claims.json), and the replay
  receipts under `receipts/`.

Three rational counts are not declared. N11 lies above the case’s verified bound, the
root of `P_trump11` that the record holds as proved optimal, which no rational reader can
compare; N17 lies 1.04e-22 below the case’s verified bound, a rounded print of the
Kleddamag endpoint certificate, for which there is no house reader, and its relation to
Bidwell’s exact side L is not decided here. At N29 the case record’s verified value,
`5.93383346267692918974379895098`, is 5.43e-20 above its own exact form, T-155’s
`296691673133846459484473030817600957/50000000000000000000000000000000000`, so the
importer’s house check refuses it; the v2 certificate is 1.57e-36 below the exact form.
That inconsistency in `frontier/n-029.md` is reported, not fixed, here.

## Against the Record

The comparisons were read against `main` at `b8c930338ee3577a43faccb52472c6975ab7eccd`.

**The 85 rational certificates** are each below the case’s verified ceiling. At 73 counts
the margin is padding, 4.6e-61 to 5.3e-16, below a certificate of the same packing: Evan
Daniel’s exact optima and regularized lists, T-155’s views, and the certificates of
Couzo, Gupta, SQUISH, Ostashev, Barnett and others that hold the cases. At twelve the
certificate is a tighter copy of a newer packing that another open report holds, and lies
below the case by more: N129 (2.0e-3, Ostashev’s #562), N146 (2.1e-13, PingYou’s #566),
N156 (6.8e-6, Couzo’s #561), N175 (2.9e-3), N176 (1.7e-2, Ostashev’s #575), N204 (1.4e-2,
#562), N232 (3.3e-3), N237 (1.8e-6, #561), N261 (3.0e-13, #567), N264 (3.4e-3), N271
(1.2e-4, #561) and N303 (3.1e-3, #562). Against the reports it tightens it is smaller by
1.2e-19 to 1.8e-19 (#561, #562, #575 and #593), by 2.0e-21 than PingYou’s own #567 at
N261, and by 1.1e-79, 1.3e-79 and 1.7e-99 than PingYou’s #568, #566 and #569 at N105,
N146 and N272, which are the same packings.

By the printed sides alone it is decidably the smallest report only at N258 and N261.
#593 names 67 of the 85 counts, and its 16-place prints, binary64 renderings, leave the
relation undecided at 59 of them; the 12- and 40-place prints of #561, #573 and the
PingYou issues leave N103, N105, N146, N156, N271 and N272 undecided as well; at N106,
N152 and N177 the cut decimals of T-121 to T-123 do; and at the 18 counts that no open
report names, the case’s reported lane is a catalogue print. Where that lane states an
exact rational, the certificate equals it at N50 (53/7), N171 (95/7) and N230 (643/41)
and lies above it at N198 (102/7) and N293 (723/41); elsewhere the submission’s own
ledger keeps the counts for algebraic reconstruction, so the catalogue’s exact side is
likely below the certificate. The certificate is above #575, #583 and #593 at N211 and
N241, above #593 at N237, and above #575 and #593 at N304.

Read from Mykhailo Polkovskyi’s certificates at
[`46f638c`](https://github.com/Mishapolk/square-packing-records/tree/46f638ce0537beeb1bad24242c6a3d357eecd9ee),
whose digests are the ones #593 states, the exact sides decide every #593 count, and with
the Couzo and PingYou packets of this pass on their branches they decide every other
report: the certificate is below every report at 60 rational counts, N68, N84, N86, N88,
N102, N103, N105, N108, N110, N123, N126, N127, N129 to N132, N146, N155, N156, N172,
N175, N176, N179 to N182, N199, N204, N206, N208 to N210, N228, N232, N236, N238 to N240,
N258, N259, N261, N263, N264, N266 to N273, N292, N295, N297, N301, N303 and N305 to
N308, and at the algebraic N70, N153 and N207. Those sides were read as a diagnostic and
are not retained; the frozen records compare #593 by its prints.

**The 60 algebraic certificates** stand as follows:

- at 16 counts the side is the case’s verified closed form exactly: N5, N10, N18, N19,
  N26, N27, N38, N40, N51, N52, N65, N66, N67, N82, N85 and N89. A second certificate of a
  bound the record holds;
- at 37 the side is the closed form the case’s reported lane states, and below the
  rational certificate that holds its verified lane, by 7.2e-36 to 7.2e-15 (N53, N101,
  N104, N109, N122, N124, N125, N145, N147 to N151, N170, N173, N174, N197, N200 to N203,
  N226, N227, N229, N231, N233, N234, N257, N260, N262, N265, N290, N291, N294, N296, N298
  and N299). At N290, T-156’s exact side is 4.8e-33 above it, as T-156 says;
- at N54, N107 and N178 the quartic side is below the verified ceiling, and the reported
  lane is a catalogue print with no exact form;
- N70 (degree 5, Ryan Xu’s packing) is 8.9e-20 below the case; N153 (degree 7) is
  2.6e-12 below T-148’s ceiling, and N207 (degree 5) 1.5e-9 below T-147’s, PingYou’s own
  constructions attained exactly; N302 (cubic) is 1.75e-3 below the case and above
  Couzo’s #583 by 2.6e-4.

By prints, N207 is below every other report; N70 and N153 are undecided against #593’s
and #573’s prints and below Mykhailo Polkovskyi’s exact sides at `46f638c`, where #573’s N153
certificate has the digest of #593’s.

## The Replay

The full batch was priced above three hours on one worker. The counts where the
certificate is below every report, by the exact sides above, were replayed first; then,
with the owner’s budget, every count that the intake ledger of 14 October 2026
(`packing/campaign/issue-intake/upper-bounds-20261014/ledger.json` on the ledger branch)
records as a PR #574 refinement: 64 rational and 4 algebraic counts.

**Rational, on both maintained routes.** `devtools.upper_bound_reports` decides each
fact through the two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`’s
exact witness verifier and the independent rational corner checker, each deciding every
wall and every pair over Q. A positive job, a duplicate-square control and an
outside-container control ran for each count in its own child process, one at a time,
from a resumable driver that runs `decide-job` with no per-job deadline, in runs kept
inside the session’s two-hour ceiling on a background task, with other lanes on the
machine; `certify --finished` assembled one receipt per count,
`receipts/exact-certification-nNNN.json.xz`. The 64 counts:

- 08:11–10:13 UTC, 39 counts: N68, N84, N86, N88, N102, N103, N105, N108, N110, N123,
  N126, N127, N129 to N132, N155, N156, N175, N176, N179, N180, N206, N209, N232, N236,
  N238, N258, N259, N261, N264, N266 to N269, N271, N292, N303 and N305;
- 11:29–12:34, 14 counts: N172, N181, N182, N199, N204, N208, N210, N211, N228, N237,
  N273, N295, N301 and N304;
- 12:35–13:30, 8 counts: N146, N239, N240, N241, N263, N270, N272 and N307;
- 14:30–15:19, 3 counts: N297, N306 and N308.

The 192 jobs made 9,164,850 pair decisions in 14,497.02 route CPU seconds and 16,968.51
job wall seconds, the longest 509.89 seconds. All 64 positives pass both routes and both
routes refuse all 128 controls. The certificates are exact contact solutions: in every
positive a square touches the box, a least wall clearance of exactly 0, and at 63 counts
two squares touch, a least pair gap of exactly 0; at N261 the least gap is 4.84e-89. The
two routes find the same least clearance and gap at every count.
`check --replay` decided the jobs of these counts again, each run inside the same
ceiling, and every row was equal to the retained one: N129, N156, N175, N176, N258, N261
and N271 (21 minutes 43 seconds); N105, N172, N199, N297, N306 and N308 (69 minutes 29
seconds); N146, N232, N238, N240, N241, N259, N267, N272, N295 and N307 (61 minutes 47
seconds); N102, N204, N209, N210, N236, N239, N263, N264, N268 to N270, N273 and N303 to
N305 (58 minutes 5 seconds); and the other 26, N68, N84, N86, N88, N103, N108, N110,
N123, N126, N127, N130 to N132, N155, N179 to N182, N206, N208, N211, N228, N237, N266,
N292 and N301 (41 minutes 38 seconds). All 192 jobs have now been decided twice.

**Algebraic, on one route.** `devtools.algebraic_witness_reports` decided N70, N153, N207
and N302 on `sqpack`’s exact witness verifier over each witness’s field, with the same two
controls, each job in its own child process: 12 jobs, 242,445 pair decisions, 1,001.0 route
CPU seconds and 1,094.42 job wall seconds, the longest 166.45. The four positives pass,
every square and pair decided by exact signs in the field, and the eight controls are
refused. All four touch the box and touch between squares exactly. The receipts are
`receipts/algebraic-route1-nNNN.json.xz`.
`check --replay` decided the nine jobs of N70, N153 and N207 again in 12 minutes 57
seconds, and N302’s three in 5 minutes 2 seconds, with the same outcomes.

## What Is Not Established

- **The 21 declared rational counts the ledger does not record** were not replayed: N28,
  N37, N39, N41, N50, N55, N69, N71, N83, N87, N106, N128, N152, N171, N177, N198, N205,
  N230, N235, N293 and N300. At the rates of the 192 jobs they are priced at under an
  hour; `certify` continues from the finished jobs once `replayed` names them.
- **The other 56 algebraic counts** were not replayed. At the measured rates, about
  2.3 ms a pair over Q(√2), 6 to 8 ms in the degree-5 and degree-7 fields, 2.2 ms in N302’s
  cubic one and 305 seconds for N53’s degree-8 positive, they are priced at about 2.1
  hours on the one route.
- **A second route over a number field** does not exist here. The independent corner
  checker reads rational corners only. Run as a diagnostic on `sqpack.field` values, its
  geometry accepted N5, N10 and N40 unchanged, in 0.02 to 1.05 seconds; as a recorded
  route it would share the field arithmetic and sign decisions with the first, so it
  needs a W7 slice and a review of that relationship. A second implementation of
  number-field arithmetic is a larger slice.
- The source’s checkers (`VERIFY.py`, `verify_exact.py`, `exact_sat.py`,
  `exact_polygon.py`, `independent/verify_attainments.py` and the conversion scripts)
  were not run; the routes above decide the certificates from their own poses. The
  derivations in `CONSTRUCTION-NOTES.md`, the per-count credit records and the
  predecessor comparisons of the submission were not checked.
- N11, N17 and N29 are not declared, for the reasons above. The replay has not been
  reviewed. A finite certificate establishes an upper bound only.

## Credit

The submission asks that PingYou Ltd be credited with the certificate refinements, and
says that padding reduction does not transfer authorship of an existing packing.
Each count’s `credits.json` or provenance record names the construction’s finder and its
earlier refiners, among them Erich Friedman’s and David Ellsworth’s catalogue
constructions as Evan Daniel’s certificates state them, Ryan Xu, Robert Barnett,
Francisco Couzo, Daniil Ostashev, Nate Chaoweeraprasit (SQUISH), Siddharth Gupta, Kevin
Fang and Mykhailo Polkovskyi (Mishapolk), and Joshua Levy and this project for the native schema and verifiers.
N153, N207 and N302 are PingYou’s own constructions; N70 is Ryan Xu’s.
The pull request makes no statement about AI assistance; its branch is named
`codex/numerical-certificate-refinements`. For its #503 and #504 certificates the author
said on 12 October 2026 that they were “AI assisted by ‘PY’, an unreleased agentic AI
offering by PingYou Ltd.”

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source pingyou-pr574-certificates-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr574-certificates-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr574-certificates-2026-10-13 check --replay
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports pingyou-pr574-certificates-2026-10-13 derive --checkout CHECKOUT --assets ASSETS --check
uv run --frozen --all-extras --group dev python -m devtools.algebraic_witness_reports pingyou-pr574-certificates-2026-10-13 compare
uv run --frozen --all-extras --group dev python -m devtools.algebraic_witness_reports pingyou-pr574-certificates-2026-10-13 check --replay
uv run --frozen --all-extras --group dev python -m devtools.algebraic_witness_reports pingyou-pr574-certificates-2026-10-13 derive --checkout CHECKOUT --assets ASSETS --check
```

`--check` and the importers’ `check-claims`, `compare` and `check` run offline from the
facts. `derive --check` needs a checkout at the pin and a directory holding the assets by
name, and refuses a checkout that does not yield this packet’s record and an asset that
is not the one its manifest pins.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-028.yaml.gz` | receipt | `d17c2a9575c9d82632be1a84a770cf3edbff6a23` | `dd44c17bde898adfb7a4bf9fcefedb6910763ef93956d1d2d87542e110bc2fc4` |
| `facts/n-037.yaml.gz` | receipt | `5b35e4f0410bf929f372e81b91b981de5ea5776e` | `4f4cf37d45a2b640d70b506f87969835e102ef5203c7e6cca177d06cff930d14` |
| `facts/n-039.yaml.gz` | receipt | `0852c84b1f6f82bb49f9c3f954f46e008ca94e37` | `911c69e4c729e1af505518b17e1274c2024e848303d29a62e68b39b5a01c108c` |
| `facts/n-041.yaml.gz` | receipt | `2cadc8f55ecb39cc9dbbfb145367f41bb4fbf7e8` | `43b559a845235f4c3827b5ca9ec51f41aec048eefe6b1f1c4218790a0ee95aeb` |
| `facts/n-050.yaml.gz` | receipt | `ae59ae8a14dfa34531740b7b473c50ca538cbf7e` | `19ff8ffc9df5f5b6a2c53e5fbf02c2de2d2a7c76d742b284fb2a1cab9a70b611` |
| `facts/n-055.yaml.gz` | receipt | `ee6fb867cdba008959fac0bfc041f6d3da893e5c` | `5079aae968149ea6310e0694c0fb7e005444ef9fed91a487b1b63617800c558c` |
| `facts/n-068.yaml.gz` | receipt | `16dfaa73d345dd00502d0b7f2697f08057ce11d9` | `05567a1d6dfc69870fbfffaa1834f2430acc8428dbd579338de228279c5b5245` |
| `facts/n-069.yaml.gz` | receipt | `2af4b3e702fdba7ae37d2efe07edb972d76684e6` | `6c66a232705aa306d2f2f404634eded47096533cc87204ded67779a178d34631` |
| `facts/n-071.yaml.gz` | receipt | `27cd0198173e973e7d16478131c22538e19d8501` | `0b3dc99a124295857794d2e6ce0775db3401dda7dd92cb8e2b69d0773da92d38` |
| `facts/n-083.yaml.gz` | receipt | `7eeb028795fd9f11f823df70ec3d19b61f2ab480` | `ce7da5bafb68d748352f7a17f999be4a6d67e65640f041412302dba2de83bb43` |
| `facts/n-084.yaml.gz` | receipt | `d768492aca1284f31defc6b4357bd5cc324a062c` | `1f806b64ad84a45cac5bad3739af16fa8828030d423d525ca58d0ceab13e713b` |
| `facts/n-086.yaml.gz` | receipt | `39210e2e524f28cbe436808406426bba673f63c6` | `ada2693f9bdc2fc339e98a2d2152a87176269bbb6137d53944a45ccd38967713` |
| `facts/n-087.yaml.gz` | receipt | `824772e8d47ef49a31208a859a5c57f006e052f4` | `4066676de4d4f048abe88a6c6ddf8faa6b68534b3ec3c8d7502f9333f045e641` |
| `facts/n-088.yaml.gz` | receipt | `d3b0b74a81064efad9e9fa393972f9676bf7929b` | `353e2094906543303d80bb04a1fd0dbd57997bb84db73c8cb54658630b89966a` |
| `facts/n-102.yaml.gz` | receipt | `95336f42784a310dfd0f25d2e1398466192dd5b9` | `7a0e9bc1338a78ae74c7eeef92c948350cecd411d1e4fcb8e8405ebe218c7802` |
| `facts/n-103.yaml.gz` | receipt | `a6abd7e53aa24104c7c172bc27b5a084b818a554` | `18db21b6f3c739dc3067b3dacbe6beb1dfceae7814ad2e370664da85c9ee6bbb` |
| `facts/n-105.yaml.gz` | receipt | `5b3e14daf74038201f827268731dc31ab41bbac1` | `58b5cfaa24337fa9d5b77fe94ba38109530c996e4b50f629d86468b60f01a3d6` |
| `facts/n-106.yaml.gz` | receipt | `554380c1a7ea3ed8d20aa87b0de074fdc4e998b8` | `4600f7a7914790dc21bee188dbf925dba2b008f73ad2416f736d0d3cde24ae6c` |
| `facts/n-108.yaml.gz` | receipt | `3b8484910ab6f357a78278ceaf9b5c6611b04691` | `7d7dc6eab2c50358e484e8333bd9c2775e744bd2c78230314e417ecbe4ae663f` |
| `facts/n-110.yaml.gz` | receipt | `0d3b2ad139c4ee4f4d7a8805df91c79686474043` | `3435b005948f491f5b81e9ba3cb072f59dd90a01bbfbd8e536e310c5553339b3` |
| `facts/n-123.yaml.gz` | receipt | `6758e900184c0e4834d110aeb0d3540f609d132d` | `ec4ac4b63809f2abde2588f95b7efdef25b835591832b86bdb27d755f827017b` |
| `facts/n-126.yaml.gz` | receipt | `0d846e4170a6dfb132e2dea494c57106aa7e9b25` | `fbef8a864cbbe71fdcbacd0ff274e350e277a77bd42f974fad3b290ebfb59ffd` |
| `facts/n-127.yaml.gz` | receipt | `fc7a29e76f13103bf88bec294c71bf0472920021` | `9be6d289c5f1df5388cbc99c313bdb182504a75cca795f065831fc6b32b97ff1` |
| `facts/n-128.yaml.gz` | receipt | `f49955b9c7cbf7092b93b88135411f56e5f58f06` | `3530856fb7072dd8433f1a3689231a3305fe3fdd3bcef3674ecaae8e3663599c` |
| `facts/n-129.yaml.gz` | receipt | `477d75c9733488bbe101e089b936bcc79282eedd` | `d78cab993647082733ebda50dcaf3781269dfa1c85118f258dc68556b15c4eed` |
| `facts/n-130.yaml.gz` | receipt | `ff7fd4ecc1ed4981b15f0b2d82ad829d8c814253` | `5d17774638f29613b6baa894559bd4e63448bc36762e8d52d96023330bd24201` |
| `facts/n-131.yaml.gz` | receipt | `0ae89d52173ce87661bdc95a39d05c378a197bbc` | `5e6bbc056506038eedb475e7e372b1aafd57d195f487209c752da27f8200ce28` |
| `facts/n-132.yaml.gz` | receipt | `e5e00fd07407dc19f7bca2b5f5de07cab3aceb8f` | `d666bdaa14be477f178f214c240374c7ac347b9ca1f1238137349700f75b0bd2` |
| `facts/n-146.yaml.gz` | receipt | `d4055b3f1eebf5205a956b9b7d8bde9f9342dbe0` | `4d1f9b667f91ba0ed01e5e962f8bcab71e198c3bb69d70a7411523cc41721bfe` |
| `facts/n-152.yaml.gz` | receipt | `8abe39d72b19bc63f2e3566efd4b420d0f7677d2` | `525ff01380fdd8804715344b9095d6d6ae157106a294d55493c0a963137c86ca` |
| `facts/n-155.yaml.gz` | receipt | `c06f82ab4fb0e3cdca4d6ac8104e987448a082e0` | `2653bf61b2281a858ae4494b675ccfc92b8c2b836bddd357cd686a04c1e728fa` |
| `facts/n-156.yaml.gz` | receipt | `5a304f32f09d46fd038ba71e336a04c76250557f` | `b9a2adf70c742eaaa2c92a929a586e16098d0986ab452a3fd0951e6826d4d173` |
| `facts/n-171.yaml.gz` | receipt | `4a8b52899c9fdb4f774eed86efaf3d741c5914cd` | `87c3cd4f2ea2fb54d0204a019037d676d057495aa61dece9ac191abba971d986` |
| `facts/n-172.yaml.gz` | receipt | `e85a50ade70789a4048bcd47b0416d2409ef3b85` | `f5b289428e49c8eb8a6349783a41981e274f20976d7fa3d01eddf29c29733fd6` |
| `facts/n-175.yaml.gz` | receipt | `282cf5df14632648ff4841ec4b749cdabccb0a33` | `b729bc53c5cc3e0a6c25a93ff454df7872b810444bd1f29865cd3bd60a4d5a3f` |
| `facts/n-176.yaml.gz` | receipt | `bf2540563f53597f39b4a55aa5b785de5ec9b6ac` | `3d88e0d98202647d868e8be2e7cd4919c3259e85fb4b94b00cb220e9b9b4097d` |
| `facts/n-177.yaml.gz` | receipt | `f34ec6fa2baeecf08acd1925c03dfb5656d3c279` | `7f14b41db51f5d7a06a1e44ee41dae824136871655bfb651b2b18b41c666c2e9` |
| `facts/n-179.yaml.gz` | receipt | `460e645369d89ffd673b15b3203853672bae3fec` | `75684b08b83208ffc197e60de21456612e9ccf638c482d01e80605db62ecab7d` |
| `facts/n-180.yaml.gz` | receipt | `e8f65f6d8ddd429186a9490ba83b177b5a4d5a04` | `d17ac723fa0eb400c03a90ed452e2f2543861177d71e4d819f9944ff2e3dfaea` |
| `facts/n-181.yaml.gz` | receipt | `13a7a429b95a822af4ba2a791156a1ead8433260` | `79bb839cdea19a8f2a4351f41f578636f866027d1807fbf738f28b2ef22a8cc8` |
| `facts/n-182.yaml.gz` | receipt | `44f21561c9a1065705fd38e0fca17e546e8e0721` | `41c0aada1ce729551dceb4c45867bf7df345e04312aff6ded50f3f5348a49e38` |
| `facts/n-198.yaml.gz` | receipt | `5636f36d1cab678d4bfce841dc1c7722d4086ce2` | `606cc8bc4c2fbd172db06f0e46cf83970f015ad615c17f6c20f7ce63bbe4f5dc` |
| `facts/n-199.yaml.gz` | receipt | `5ae65e1bd02ba9e32322c3303e6d84e643e32ee0` | `eb660c6a63442ecdffa7a73a53db452d272d416d1941e29a31c7bec3f91bb494` |
| `facts/n-204.yaml.gz` | receipt | `31a0bb194d62a0a1b86fa36aca30403b5ffc26e0` | `e88914853fa3bcbb0df779274903e2ec93d680b80432a18812cb256483d3589c` |
| `facts/n-205.yaml.gz` | receipt | `dc74650e5e342050611fc68b15d3ce561519bddd` | `b2d61e40c08a4797f6b756ec4cfb66e75a4a5cfb428ea4280ab2164fc58ef38b` |
| `facts/n-206.yaml.gz` | receipt | `225020f04d914e163a6a55b46a72edbc77cea793` | `de19cfb1b9efbb3d8000adf9cc4870be6b1a68731e058c1d12115dec84b09d11` |
| `facts/n-208.yaml.gz` | receipt | `c2042ad81ad1f78575ce5bd30c9ee54ee834f390` | `713c6756027d42f710f60cb25db419a9ff1db78a825fcfc7081919b2ecce7e39` |
| `facts/n-209.yaml.gz` | receipt | `ec3e577f5bd7e6e223743f1595e6d5dfb8efac47` | `29cec47068f90881ffea8b1746119ba882d49704ee1cbe6e446a48aed5a68095` |
| `facts/n-210.yaml.gz` | receipt | `cf24071f7ddbdf1e49c693a24b3d83438e5e8180` | `794dec0f6fb0c0f93df6076e8ffc313e1ca9771c9ea1961d350bd473e81a78f6` |
| `facts/n-211.yaml.gz` | receipt | `c7affbf173653be04b251fe80606c87b67153557` | `72bc9194027862042ad25752db3193c0ba1b0f6a8132825aeac548e8497c8022` |
| `facts/n-228.yaml.gz` | receipt | `5b21ce78714f3c7bfc8c91ecb23cc8af92ea94bd` | `06768c1cce95f7a659ee5048c52d0a49a42f6c81356a37d198614937f2632105` |
| `facts/n-230.yaml.gz` | receipt | `cbfbe52594c8385fe567c122f722c027d683e9ff` | `8c106f5f9155a4cbe7abf0ee04b99682c370b0d090c3e855b80128df9e5d2260` |
| `facts/n-232.yaml.gz` | receipt | `ac723fd9563cac4a392040d258e0496e77cf0f7a` | `81771c637d2998fc3f69c482dca82bfba434ebeff80987406df5794ac0c20cf2` |
| `facts/n-235.yaml.gz` | receipt | `2f66f0600a579a876b3520aaa9990561343c5465` | `896af7c60314cfa4ebd2a0736f688205ca61301586b86ada963a76677631ef7f` |
| `facts/n-236.yaml.gz` | receipt | `84871e709c0c2e158b03fc877ccab418f35dca87` | `7db4077f7d1b9d48c29a6dce2f04de8187b3d2fcb5331388286735711bb54ca0` |
| `facts/n-237.yaml.gz` | receipt | `d812ee6a1c46c66f2c88541c6cd9354fb2e9769e` | `86712a107a8c6ea2d01b9a86a791715dcc8afdd531068ae77b2223689e24c1d2` |
| `facts/n-238.yaml.gz` | receipt | `aec695cd86a0049ee5040899c2daacf6ac818f10` | `fbb796c79cbf389199b0686a555c6526b488bade1424f4b882731f6fed7b3e24` |
| `facts/n-239.yaml.gz` | receipt | `99c25221c1487b097924f1e2a2bffcd267314422` | `913780ff9f3ebceade829dc11542697b973987460de8742ca02b35de3dfff29f` |
| `facts/n-240.yaml.gz` | receipt | `a18175085d4333ad3d5bfc26adffbc998948f539` | `d63cd210038ad8f7c8ce145c124b56299ae56e55d9b7a7b84da6348a52646c3d` |
| `facts/n-241.yaml.gz` | receipt | `9ce0f7019f5420ddd5db9b7b18c37d44f1b4ffa1` | `505b863f2fb42c68e242aab04e9939d3d47b1646be23b09950b316b0faeb9ecd` |
| `facts/n-258.yaml.gz` | receipt | `767dbde678b6ea24a7920997fcc4be5f8b0760df` | `4cb01bbfa3028146b104cce3c6ff646f1b784f6fdc8e4dd1c07124bcd924eb1e` |
| `facts/n-259.yaml.gz` | receipt | `3deeff167641bf9c107220d49f6d24c2fe6ed188` | `4578be349e31c82695ef7e4f4e44709d250ba162dc3a1883ba767b039b2450fe` |
| `facts/n-261.yaml.gz` | receipt | `e73d161060a0a12f2afcd1d3ba0df365b629a8c4` | `e75795eb10345b00f914fa4e32b4faf55f8439af98f7799867c8503fbce9db83` |
| `facts/n-263.yaml.gz` | receipt | `191ed001dd20bf22a154c1f09682458e6bdc30ed` | `76ce4b680c4758087bd911b7c3545720447d351ef9e52b7843a95661278c18dc` |
| `facts/n-264.yaml.gz` | receipt | `7443aae4f580b057f617e4c91dbbe9735096b7ed` | `e7e92edf1e37f8f270163344c7e365fd038d566ca7f99a6509efbe1a93b34766` |
| `facts/n-266.yaml.gz` | receipt | `357095bf0e7be0983b60104579a143ae23f8b94d` | `73fbbd2666423c3908b0fa67ca54b5d266e5c913b09e4c435c6a42658fbfa7cb` |
| `facts/n-267.yaml.gz` | receipt | `38b6709e32e7dcdd9c3ba628f50925024e997851` | `29bd652da65d2a3e4b0eb1d086d200ff42702d88e93663beb37b54c66c2d1aa7` |
| `facts/n-268.yaml.gz` | receipt | `a78110f61bd781542efbb25560f395493a45c854` | `4c6385a33ed79a97b36dec62172414ad1550e53d24263161c617a5f4cfeaf1b0` |
| `facts/n-269.yaml.gz` | receipt | `f0638ca085a23b83cfd97f94b24404acf750ac45` | `640520170bf063f26cb5b8f4a6d8080d8be5128c5bd1de381f27a532f7436279` |
| `facts/n-270.yaml.gz` | receipt | `9cdecf40b8bfbfc8330979cb9d5abf2126359540` | `9fcf6f7e4972a4762817c02f0aae2027e892dd432d5a8880a2bf873d01072de3` |
| `facts/n-271.yaml.gz` | receipt | `80246baef2f27fa55428c422378e4bfc66c5f856` | `12e5290621f1f91a15fddeddf83c157f301b9178f7768d5c4badf09b27c068e7` |
| `facts/n-272.yaml.gz` | receipt | `b385fb95fa2f34f8d1b09b95b4b5106462b5bd0c` | `2f69bfa19747328da398483f26020c2e46cc8334f29a86b7fc4e9c34143330eb` |
| `facts/n-273.yaml.gz` | receipt | `52ecc748f52fb6e7d7f55fbfa249f3a85c15281a` | `d4cb6638c718a2fd86839870dad201db0f2b821a8cd9a45349bdfe0fd5b67a11` |
| `facts/n-292.yaml.gz` | receipt | `501219de5b30eb7cc924620af56a1e83d537efd5` | `72616ad88611f8fdf247b08c0a44298fe1b77780d7f0c7f81580497236e75fed` |
| `facts/n-293.yaml.gz` | receipt | `5112cdf6e4145c0871ef28eee0814e86f71ece27` | `1ebb099a80206ff4e0e32493116079300ba818d0616a792cd0ec54fa18469b8b` |
| `facts/n-295.yaml.gz` | receipt | `40466385e57992839d453279b0fcbe383839a9ae` | `606fc70f593aa72e1013ed47fdf0779064e625edcbfc6904e963bc0613b80cc9` |
| `facts/n-297.yaml.gz` | receipt | `33d65491834441f45d1abbd7657ee8ac00b97ece` | `48116303d76971843fcbe047cdb7a7195c68c17d062c0d83229b143fc44a3606` |
| `facts/n-300.yaml.gz` | receipt | `19c0880d6fd6329c27443657f0fdbe9859f3edc8` | `e11da68c836579e497f1936c341f86eaf281e2e4dfbf5eccd42a223fa6165453` |
| `facts/n-301.yaml.gz` | receipt | `dfa1e5ec7eaa5e7f06419af324a095ec5ec6c9ba` | `4e4610e23d56aa096c74302642cc2b99fb14e00ac99a0889f738dd4c7affbfc2` |
| `facts/n-303.yaml.gz` | receipt | `d7fed353b72fc7ec7b6915642c8b32ab19658854` | `e395f9d9c77bbdc264b369efbeaa21a9c91f1cf072f9c52a76e25c791247fc05` |
| `facts/n-304.yaml.gz` | receipt | `8c2841ed711997addccfabeb543ec461c5027a8c` | `80575492f70fa78310cd00cb895254b5bd5774539cf1fe175ed423f9cd262ebb` |
| `facts/n-305.yaml.gz` | receipt | `99de853a22d2caa75e521016447a044a114cf167` | `514bd24bceae34f98054e6a5d2ff1732e7fa08c8ae24cf656127de319ae7fac6` |
| `facts/n-306.yaml.gz` | receipt | `120eccb5cbbd60cbebdc30a37f0d2e1ae5039bc4` | `2b92a456e3d328a3836b090241e608b920eb7f31a9188a25c874e3fa384f192f` |
| `facts/n-307.yaml.gz` | receipt | `ad7962cb64a00c1d1d2c55202728b42a4648d695` | `90711919a84dc9ff750ea4104b620010216cfe00fd6068d3e4953f22ef8927ca` |
| `facts/n-308.yaml.gz` | receipt | `856b01f6fad1ac63e50a6e054251b35352a46403` | `ab5be546138a73ff56374ff15d4192db45eec5431f34e270bfa399f55454cb61` |
| `facts/alg-n-005.yaml.gz` | receipt | `8b80b231c7e399ea5d7f54af329c7e994324c029` | `9754e26a102db13b0ea8b16f79c1d67706ad08e328051edff33ba65f775ac876` |
| `facts/alg-n-010.yaml.gz` | receipt | `430f35f0f9fbf75cf9d6ff772b058ada9f08408c` | `3247a54071cf566b2d6c509ba9a3177e5ef3597af9d6f0fd9e3b51d77e4db0e0` |
| `facts/alg-n-018.yaml.gz` | receipt | `cb6bdd8dd1065ab2fcc660979a37584f4d461e51` | `4de66adb517b9ff46d26f150d31d1cd3ed5536db3ae43f7462bbe5b167dae795` |
| `facts/alg-n-019.yaml.gz` | receipt | `db53c1e7326f6e55d2dd57c89d43f26590510d15` | `5965f75d72f5497bb499d1db73010dd453955802940ec664e3159df91abe4ba5` |
| `facts/alg-n-026.yaml.gz` | receipt | `4710586dffa646338df2862a37430bcbf7337dc6` | `9477911c7237f647f96f170d57a7cdfc1145dae6bc1cfe561fbedf73e7fd8973` |
| `facts/alg-n-027.yaml.gz` | receipt | `6230fb12439ca6c3cde1b418ad06824763a8a6a8` | `5cc7b6b071235bfdaea3adb3331a4dd12f0431ea0cea8288993446469860a806` |
| `facts/alg-n-038.yaml.gz` | receipt | `d1298c75a45d081cdd179250a87a9a3b2620c7a8` | `baa23a720c6e83101583bf7875ff7a99dbfde57fcd45171d620b5a4ea0c9c816` |
| `facts/alg-n-040.yaml.gz` | receipt | `39ceff1aea0d95d2c05967275ea171857122e806` | `a21fea6d14f5d2fb1b718ea4c74de63340edf61864181ff8a103eb441434023d` |
| `facts/alg-n-051.yaml.gz` | receipt | `60d16ee87a6b695c1dc5a9a7e77f6316d7839d1e` | `1a6dc0cfbb5fb5b078917f514d9217e1ba6442804902064865ef90caea727e96` |
| `facts/alg-n-052.yaml.gz` | receipt | `9b93152f33b07104e4b308e4fd1dc232ded44371` | `6588aee4cac685e249353c6dc279c2d9482c918cd92cb2dc1cbfa2a042d7d65c` |
| `facts/alg-n-053.yaml.gz` | receipt | `6cd33a1e217efd8d03f40536d292167444fa5d4f` | `0f1fbc7eb4e2e4d6594c93b9c12e94c5ef52a988d3b386a00752b6b7073ae839` |
| `facts/alg-n-054.yaml.gz` | receipt | `4def9b9f11d85f4d24ba3efa9429930979ec045d` | `23bb7c175bcdf95d1ed25f191d9191e65693fdecec93cef037d03229f08b1fe4` |
| `facts/alg-n-065.yaml.gz` | receipt | `646c271701b88819f575ba9944efd9265bd73018` | `5f7b13d77ad0999876ec5a1c6a637bc3247ccf6836213cd8ef457e62c91ac3d8` |
| `facts/alg-n-066.yaml.gz` | receipt | `f072432e78bb18b331318fec112a1e27c31dcd48` | `175f43a8401a64dc2ce8b413237620bccac82857e9079141f820d10e398debab` |
| `facts/alg-n-067.yaml.gz` | receipt | `91b70e193a4dd98a9d03ea30516294594ae4bdde` | `94e20a4570fa61763944f21069de96067379b5823d51c8a8c68d38e352af2ba7` |
| `facts/alg-n-070.yaml.gz` | receipt | `3b4e7355e1463050c5aaeb83d11dddf69a0c44b8` | `e93a06c4a548cce4dea0947cc015e908bab952241d95162ebc1485fa0258c7fa` |
| `facts/alg-n-082.yaml.gz` | receipt | `aa3df9ef96280635b04b6bb9446f780764a7e00f` | `17bcc6617fb6802e6eb6c71ffb63c837c9766dfd6aa9039ded0308f8fb2db4cf` |
| `facts/alg-n-085.yaml.gz` | receipt | `3f6880709c577d05ed4b423fc3aa36be6597adb9` | `572c1dea0c54846ba637449745a8de3a44408b75d3f6d0073d63ff3d8070a5e2` |
| `facts/alg-n-089.yaml.gz` | receipt | `0b630513e434b5b55c54aaaaa1fcc5634d3b07a3` | `556bbf9daf62675c67912141e1d9b3f598c1fb90ba14e23f3c2e017c3407d988` |
| `facts/alg-n-101.yaml.gz` | receipt | `ab96526c9b109eabc822e4b78b66eddefdb978f7` | `647d02547b3f98d112aed32f343dbe1854162da2c99120cd9a627006ddbf1169` |
| `facts/alg-n-104.yaml.gz` | receipt | `df6d37482de5d1c88dd3c984690807209717e605` | `6cd77f15d1bcf2d3eb1ba0f819be5ecbbbd7b9e1e7eb189566afd2bdab2e9f61` |
| `facts/alg-n-107.yaml.gz` | receipt | `cb26fc9eef53348844da78eff607f902ff3504e4` | `ea867721eea374c7409599547a3a9c1c4dede1e253674ba7d718c925822ca04b` |
| `facts/alg-n-109.yaml.gz` | receipt | `697748ff4c5f0e58dd449be10e81d94c5f74a1c8` | `56afaff8eed47f36bbeb5dfae91a09fe5bf472d0492cc5f3a15b4eb3c434ad36` |
| `facts/alg-n-122.yaml.gz` | receipt | `d796b128eee324bdb846d96f2e6a50c6d312f579` | `8f6a31fb895563e89199364c1f0a1d2e6224e5a3559d52038d9f6b6e8fc9b2df` |
| `facts/alg-n-124.yaml.gz` | receipt | `81e1922df0f7e24fc36156a88c6c43286ad9f45d` | `13640935428470acce264f7ef9b662bb198e5b77d606c0d2f99609728742f857` |
| `facts/alg-n-125.yaml.gz` | receipt | `73d99f24aea36fbdcb5c5673eea90b59e745e08a` | `e4541ef021b9e7f4f8f3b9705fdfd1c2d0f155025317269d5edd7799a1af0baa` |
| `facts/alg-n-145.yaml.gz` | receipt | `de2da5975134937971b8ade0838e6e9fa675c1ab` | `0a72a0970b3d572f43c64a5b2aea8abf63091e2dd014cd4025a63664bc1ae850` |
| `facts/alg-n-147.yaml.gz` | receipt | `40dbac3682342e305d62dc7c3e44c83f07b391a5` | `4d59fe5c94ea38569cf7eb6115b8c1bcfef32389e4114a2dd62d19fd7b90d48f` |
| `facts/alg-n-148.yaml.gz` | receipt | `8bb5b148176f1341c61965c8ca1a76334d2754c9` | `678a4cf67c01584cd325974d44e01f0a9a45e8df9ee5a61f4484ed99cd13486d` |
| `facts/alg-n-149.yaml.gz` | receipt | `4734c8fbfe6207dc433abd6d43265ec951b09f76` | `eb3e145e9073e50cf03925a83d8972ee5d95a64b4e40219e2cadc00120bda9ea` |
| `facts/alg-n-150.yaml.gz` | receipt | `8fc39b2f743f87ffbcb54b13eb0fd045a0e498a4` | `e52879a7ec9c00587e63d46e0a15c0876f76b1545e324bf8339b733a7b636e67` |
| `facts/alg-n-151.yaml.gz` | receipt | `edcc0bf7b2e1ea5ded88087d75f807d6743f58b1` | `3611ed346d6e8ec33b0339dd25bea3a4829b5e1e338f89a615e6d1d47be927d1` |
| `facts/alg-n-153.yaml.gz` | receipt | `959c0bc77430dc1ec723d4be30bf30a4e876675f` | `c76e45c6be2f66e9fcd4e854728d479e0fdab87fd15f4b92eedd9fdbaa48d0a4` |
| `facts/alg-n-170.yaml.gz` | receipt | `bd20220586e51e574d034e28170eb22be833d182` | `445f0941147524a52045fc39d06d5a2b6bff084104ed9ae8e6200061c0cbfc70` |
| `facts/alg-n-173.yaml.gz` | receipt | `d8b321b6b46b12e78e9859418e70a90c7d901fd0` | `86c10f57c9efe473916751d5d0dee37ef2f7c157996f20da9fc3a567e8cceca0` |
| `facts/alg-n-174.yaml.gz` | receipt | `73a66903ab514306bdf2b85ce4fa1337c76deb8f` | `6808148115c4ecc5a784d8f59a8214bc74473aed6abdb913022642e5a473f9d9` |
| `facts/alg-n-178.yaml.gz` | receipt | `b74135c1c6a533b3ec2723ae95378bc9380918de` | `b2f18af01100683c180d2196ca53bd57f0f08505508f9af7ed7d7aac7ff50d17` |
| `facts/alg-n-197.yaml.gz` | receipt | `9f4cd99ec45b99167cd5f79530fa4643d4089b7d` | `e1863f538b65e33cb6d8c046010ff834cb2ffbb27a55c8ddbfb97b07fe68e876` |
| `facts/alg-n-200.yaml.gz` | receipt | `ac074583f3f71e93fd260d53b718a2e92a23d325` | `66073bda9b55af96268e379fc4665955f32366e11d9704f4b19707b5e108a79f` |
| `facts/alg-n-201.yaml.gz` | receipt | `98446c49027a90f38530d320f32b478a91bcf6ce` | `a4863850bc73f86d83f40f58159395a61465ed54e778f978e25c863ea4439e10` |
| `facts/alg-n-202.yaml.gz` | receipt | `232d9882ebd897b9521a721a41a5dd1ada23afc4` | `f135c1ec8f8c1299d694af416d6b97e82cfaa7a8bbc74c907c52e2ebb0f474e1` |
| `facts/alg-n-203.yaml.gz` | receipt | `175a78c436622bd418dfb3b6831484ba1ccf0287` | `8de91747b02f431d5dfc3ef4bc1278f4e19946f77f3a63e4f08353b91d8ab927` |
| `facts/alg-n-207.yaml.gz` | receipt | `3764fad317448d2832819cee164b8915ab9bc49f` | `5706dc719c601366a84c8ca61113ba8d6f63896f6f64371cb2184c5ff3a41d8f` |
| `facts/alg-n-226.yaml.gz` | receipt | `3c63bfa7227cc6dddec8b38a2f6c1cf90ba52bb4` | `fba0ab164148d51e56053431b06bfb26bcfb6a9951bde5e71fa0121f76baf2cb` |
| `facts/alg-n-227.yaml.gz` | receipt | `8bbfea2f004422f8b33bbb98c71b9878e0f8f8a0` | `4de444403bea74d06cdec3b36bf7359343b3b3c79c53d00b673fd6d8acc5a02d` |
| `facts/alg-n-229.yaml.gz` | receipt | `bd11f27a4a29207364290b4b8370bcdccb2ff8f2` | `53e56830992be8add58199372d4c46ca4ceab6643e0e8e3f6b95043550fb571e` |
| `facts/alg-n-231.yaml.gz` | receipt | `1669787de15319943928ddcc8f84dfe3c79def76` | `a67672da006f6d79bd840b828eeff7e90a770c08c6bab3ccc3937ca816bf6d23` |
| `facts/alg-n-233.yaml.gz` | receipt | `e228df3a4c8bf5e1f2749fba3ef1c6cf87ed6fb2` | `2d124f21d5ce5e29fd4cf079282ba310217bd158793446a0153c09ab918dac47` |
| `facts/alg-n-234.yaml.gz` | receipt | `9e5f48534690cbd69ff48da8afb6644dd98a43cb` | `e20458c063802226dcf73d26bc0eb02e36858042db7b3bc7f43bc8e0c329c351` |
| `facts/alg-n-257.yaml.gz` | receipt | `805fb8d38c4813e8f69b7b5c949c577b1d1141bd` | `e9d1dacfc4757146c1b45c87306527d0b8772f2194db7af15c1cd4314673a208` |
| `facts/alg-n-260.yaml.gz` | receipt | `e9fcf8e6a5a1c4f9f4bfe835c2b0b3c148a855f3` | `0142eb5c0399975c08dd6adc725eeaec5e6dd422ca0f2599064c321d2e8a5a6a` |
| `facts/alg-n-262.yaml.gz` | receipt | `f1f68e36c51665974757ae9b24f2ea84a24c978b` | `83b917dfda3b5f830656bec683e7310c60240c74185b3cabf2c2c793d07c3422` |
| `facts/alg-n-265.yaml.gz` | receipt | `77fe3f9719385362836405c8b99d2ab8ea95eecd` | `743091ae7f4ac06a1253b804fa1431e517118715ba9c1759ffe77547569bd91c` |
| `facts/alg-n-290.yaml.gz` | receipt | `e1d279012b5b5a6d4545a83d859e782841abe259` | `6a8a47b7cb830e4a906d076d1c887997c1a8bba9986756991d324d02847995b3` |
| `facts/alg-n-291.yaml.gz` | receipt | `282cab5d4b470a5ffea608d58ac8ae0d40cc2b36` | `1c475711dcd2239ae18ca7b2213ffe78d941f4faa244931494b9705a701867af` |
| `facts/alg-n-294.yaml.gz` | receipt | `924a2fd4c8994284bb3b50eb6d24e6ad51352330` | `5c8dbfcd694373ce14ce5bbc47460c7cbeab3af46893e049a73c85a3baeb83d7` |
| `facts/alg-n-296.yaml.gz` | receipt | `4c81d3b3fdb1d85bf50fc2d8ceca94abf89bd6dd` | `1288cd02c54c06cd686d6b614d83cc3f36b9f9ce4ea85af43d79188718eb3d66` |
| `facts/alg-n-298.yaml.gz` | receipt | `798a266701b33a61c7903a5696e3512e6fdc33a6` | `ffcec527649fafc6717e7862a82d97074caac1dde48be97b5a33a260dd29128a` |
| `facts/alg-n-299.yaml.gz` | receipt | `5a967b6826d6a48808ea1f22578d461e70a5bc2c` | `b907527614de970e1c3b96c918455f1ffe5d2ad2b5e1f92a5732e963ba82b739` |
| `facts/alg-n-302.yaml.gz` | receipt | `db56fa2b6aab42c45727609e303b5f45af830f7d` | `8be9b59cff78030ea2443a4c799824d98643e17c0b24adf1b267d8aaea1b895a` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
