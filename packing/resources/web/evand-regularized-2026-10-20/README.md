# Evan Daniel’s Regularized Record Lists: Four Solved Views of 20 October

Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/0075967bace18a3deabcc0baa64c2fb294fc80a0/search/regularize)
refreshed its display-regularized record lists at six counts in `0075967`
(2026-10-20T02:36:12Z), whose message reads “Site up to date: records at 183, 229, 308
(ours) and 204, 227, 260 (Couzo), certified and regularized”.
No issue reports them.
The 21 October intake sweep compared the six new certificates exactly with the record.
At 183 and 308 each states the case’s own exact side (T-220, T-221).
At 204, 227, 229 and 260 each is below every value the record holds or has pending, and
this packet retains those four.

The packet pins that commit, `0075967bace18a3deabcc0baa64c2fb294fc80a0` (tree
`8c3b50451122acb21593dfbd7b86c406c7e8af7f`), the first to hold these bytes, which dates
the claim. The eight retained certificate and JSON files are byte-identical at the
branch head on 21 October, `88385ab`, whose three later commits change nothing under
`search/regularize/lists/`. The sources were retrieved at 2026-10-21T19:58Z.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 204 | `14808642840591493923068442871459/1000000000000000000000000000000` | 14.8086428405914940 |
| 227 | `7781812826162574542396221861851/500000000000000000000000000000` | 15.5636256523251491 |
| 229 | `15650161513876431064009548865321/1000000000000000000000000000000` | 15.6501615138764311 |
| 260 | `4161438312629953048686574163329/250000000000000000000000000000` | 16.6457532505198122 |

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the format of the 10
October lists ([evand-regularized-2026-10-10](../evand-regularized-2026-10-10/README.md),
T-146). Its 50-digit JSON beside it, `n-NNN.json.gz`, prints the same side exactly as
`S_cert`, which is the side each row of the import declaration offers, and `S_exact`,
the side of the solved packing, which `S_cert` lies above by less than $2 \times
10^{-19}$: the method log’s scaling by $1 + 10^{-20}$ about the origin corner.

## The Author’s Framing

The source does not claim these as records, and the import keeps that framing.
Every certificate’s JSON says:

> regularized display view of a certified packing at the same side; not a new bound

Each JSON names the packing’s finder under `by`: Francisco Couzo at 204, 227 and 260 and
Evan Daniel at 229.
The commit says of 229: “229 after the slp2 polish, 2e-11 below the posted float: the
exact optimum of the same packing”. The JSON at 229 names its input `polished`; the
other three name the store’s packing (`input`).
So the author regards each side as the exact optimum of a packing already posted, below
its posted side only by rounding.
The record held those packings at their posted sides, each a little above, and none of
these. Each side is a value the record did not hold, and a finite certificate of it is
an upper bound the record did not have; by the house rule a regularized view below a
case’s house best packing is a smaller packing, registered as a result
([result-import.md](../../../campaign/result-import.md#the-house-rule)).

Each JSON also reports the certificate VALID under the source’s checkers and verified
at 80 digits, the `conservative` policy, and level 2, “same packing: traversable
without expansion (angle moves path-checked; slides by construction)”. Its
`angle_changes` at the four counts are free angles kept, none turned or merged.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
19 files, 432,151 bytes, of which 11 files and 75,999 bytes are retained.

The four certificates and their four JSON files are retained as the upstream gzip files
they are, `search/regularize/lists/certs/n-NNN.cert.gz` and `n-NNN.json.gz`, never
recompressed; the [Original Gzip Files](#original-gzip-files) table binds their
compressed bytes. The importer decompresses them to read them.
The packet also retains the method log `search/regularize/REGULARIZE.md`, last changed
in `60517c1` (14 October), with `LICENSE` and `CREDITS.md`.

Eight files are pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why |
| --- | --- | --- | --- |
| `search/exact/verify_cert.py` | 3401 | `3299ca0c0f02f7c221deeea69a9a85b5a90db6bc410b20727fdff211c92bed52` | The source’s first exact checker, which each certificate’s header names |
| `search/exact/verify_cert2.py` | 3101 | `55140a35d95d9eaa64a14c3b044641efbcda94ebfc3b12b7dec9fa52692e31d3` | Its second |
| `search/regularize/refresh.py` | 4486 | `7927878fffc8510f86ec9994df9390ab5ecc1ac941abc82aa059c4f9bbb1f049` | The refresh that solves each store packing to its exact side (exactsolve, else the slp2 polish) |
| `search/regularize/samepacking.py` | 5698 | `b50e43a8dca66317c48ba30c36cae6b20892c68834dc3879e852bc4a090036b9` | The sampled path test behind each view’s level |
| `search/regularize/lists/best.csv` | 54431 | `9212d2028ef4e4f72c134298617d01b720b088262ebddf532dd2649e33915cdd` | The best-choice list of all 324 counts, whose rows name each certificate, its finder, variant, level, rotation groups and input |
| `search/regularize/lists/best.json` | 120726 | `ea7cab2028bd699ce141de6a0a53fc643ef94673aff841afd371c3b067c79dc7` | The same list as JSON |
| `site/data/lineage.yaml` | 2894 | `1e319b3ddadb8ae33565202a8233a03d9507d99824c3221ea81312ce7c895a7e` | The site’s credit lineage, which this commit extends with #674’s 229 from #672’s packing |
| `site/data/records2026.json` | 161415 | `72adf7e8ca37655d22de4e3411119bd1172fcb8aed6a631c2be30dc5d4f20a89` | The site’s record provenance, with the postings #668 to #689 |

The two checkers are byte-identical to the copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains, and were not run.
The same commit’s certificates at 183 and 308, the lists’ other certificates, their
JSON, the alternates and the rest of the tree are pinned by the commit alone and were
neither retained nor run.

## Exact Replay

Only the four certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
by the declaration-driven importer `devtools.upper_bound_reports`, as the 10 October
lists did (T-146): `sqpack`’s exact witness verifier and the independent rational corner
checker (`devtools.check_rational_witness_independent`), each deciding every wall and
every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

All four positives pass both routes.
Both routes refuse all eight controls: each duplicated square as an overlap with its
copy, at a pair gap of $-1$, and each translated square as outside the container.
In every positive the two routes find the same least wall clearance, exactly
`1/200000000000000000000` ($5 \times 10^{-21}$), the origin-corner scaling’s, and the
same least pair gap, just under $10^{-20}$ ($9.99 \times 10^{-21}$).
The 12 jobs made 636,798 pair decisions in 63.0 route CPU seconds and 71.44 job wall
seconds, summed; the longest job, the positive at 260, took 7.07 seconds.
The two-worker run took 40.8 seconds of wall time on 21 October 2026, under `nice` on a
four-core machine other lanes shared, and a serial `check --replay` decided all 12 jobs
again, equal to the retained rows apart from timing, in 66 seconds.

[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record as it stood on `main` at `7eeab1f5e`, 21 October 2026.
`check-claims` rebuilds it, the case ceilings and T-198’s and T-199’s sides from their
own retained packets. The issue-678 packet (T-223) and the issue-668 packet (T-196)
carry no import declaration on `main`, so their sides, and those of the unregistered
#670, #672 and #675, are compared at the twelve places each issue prints, rounded up:

| n | Case ceiling, holder | Below it by | Other reports at the count, each above the certificate by |
| --- | --- | --- | --- |
| 204 | 14.80866323438695657, Daniil Ostashev, improved by PingYou Ltd and Mishapolk (T-186) | $2.04 \times 10^{-5}$ | T-223 (#678, Francisco Couzo) $1.39 \times 10^{-9}$; #675 $1.53 \times 10^{-6}$; #670 $1.58 \times 10^{-6}$ |
| 227 | 15.57106781186548, the Kingbird catalogue (David Ellsworth), T-155’s exact ceiling | $7.44 \times 10^{-3}$ | #672 (Francisco Couzo) $1.79 \times 10^{-11}$; T-196 (#668, Joost de Winter) $1.71 \times 10^{-4}$ |
| 229 | 15.6501615138955532, Evan Daniel (T-199) | $1.91 \times 10^{-11}$ | T-198 (#674) $1.74 \times 10^{-6}$; #672 $1.32 \times 10^{-5}$; T-196 $1.32 \times 10^{-5}$ |
| 260 | 16.65685424949239, the Kingbird catalogue (David Ellsworth), T-155’s exact ceiling | $1.11 \times 10^{-2}$ | T-223 (#678) $2.52 \times 10^{-11}$; T-196 (#668) $2.56 \times 10^{-5}$ |

The margins against a print are taken at the print; against the exact sides
[measure/identity.json](measure/identity.json) reads from the packets, they are
$1.389753 \times 10^{-9}$ and $2.514377 \times 10^{-11}$ below T-223 at 204 and 260,
$1.710513 \times 10^{-4}$ and $2.555366 \times 10^{-5}$ below T-196 at 227 and 260,
and $1.757785 \times 10^{-11}$ below #672’s exact side at 227.

At every count the certificate is the smallest side the record holds or has pending.
Each side also lies below the verified upper bound at the next count, so each bound is
new by the monotonicity test $s(n) \le s(n + 1)$: 14.82445114612409 at 205,
15.60460147572967 at 228, 15.68292682926830 at 230 and 16.67877987534291 at 261.
No registered certificate states any of the four sides.
Two pull requests move these houses before this import’s adoption: #704, merged on 21
October, adopted T-196 at 227 and 260, and #706 adopts T-223 at 204 and 260. #706’s own runs of Evan Daniel’s
regularizer on T-223’s witnesses found solved views $1.39 \times 10^{-9}$ and
$2.51 \times 10^{-11}$ below the witness at 204 and 260, the margins of the views here,
and listed them as register candidates (row 3), not drawn.

### Pose by Pose

The register credits each certificate to the packing its source names
([Credit and Licence](#credit-and-licence)). [measure/identity.py](measure/identity.py)
measures how far each is from that packing, square by square, and writes
[measure/identity.json](measure/identity.json). Under each of the box’s eight
symmetries it matches every square to the nearest centre of the other
(`devtools.check_half_angle_area.arrangement_gap`), keeps the symmetries where that is
one to one, and reports the best; and it pairs the squares by an optimal assignment,
the least total squared centre displacement, which pairs them where nearest centres do
not. It is a measurement, and decides nothing:

| n | View against | Below it by | Nearest centres | Squares moved beyond $10^{-9}$, $10^{-6}$, $10^{-3}$, $10^{-1}$ (assignment) | Largest move | Largest turn |
| --- | --- | --- | --- | --- | --- | --- |
| 204 | T-223 (#678) | $1.39 \times 10^{-9}$ | one to one, half turn | 154, 72, 58, 4 | 0.442 | 0.159° |
| 227 | #672 | $1.76 \times 10^{-11}$ | one to one, half turn | 60, 33, 16, 3 | 0.168 | 2.54° |
| 227 | T-196 (#668) | $1.71 \times 10^{-4}$ | one to one | 227, 226, 58, 3 | 0.208 | 5.84° |
| 229 | T-199 (#674 update) | $1.91 \times 10^{-11}$ | none one to one | 165, 134, 112, 13 | 0.650 | 0.055° |
| 260 | T-223 (#678) | $2.51 \times 10^{-11}$ | none one to one | 53, 53, 41, 20 | 0.643 | below $10^{-6}$° |
| 260 | T-196 (#668) | $2.56 \times 10^{-5}$ | none one to one | 260, 254, 79, 21 | 0.646 | 24.5° |

At 227 the view is #672’s packing: 194 of its 227 squares lie within $10^{-6}$ of
#672’s, and its side is $1.76 \times 10^{-11}$ below #672’s exact side,
`71427829379429597600111901507/4589408083628500000000000000`. Against de Winter’s
packing (T-196) 226 squares move beyond $10^{-6}$; #672’s own packing moves no square
beyond a tenth from T-196’s (largest 0.080, 58 turned), so #672 refines de Winter’s
packing, and the view is #672’s packing solved lower and regularized. #672’s
certificate is `certificates/n227.cert` at
`franciscouzo/square-packing@af8cb7959aead318c0cf5e9f873de3caa763f77a`, SHA-256
`65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17`; no packet retains
it (think-2vjc owns #672’s import), and the program reads a copy fetched at that commit
and refuses any other bytes.
At 260, 207 of the 260 squares lie within $10^{-9}$ of T-223’s and none turns; the 53
that move slide, as the method log says the regularization does. At 204 and 229 the
slides are larger, and at 229 large enough that nearest centres pair the squares one to
one under no symmetry. So each view differs from the credited certificate pose by pose,
by the regularization’s slides and turns at the solved side. That each is still the
same packing is the source’s path-test statement, and is not replayed here.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source makes three statements about them that are not replayed here: each side is
the exact optimum of the store’s best packing at its count; each regularized view is
the same packing at that side, level 2 of the method log’s scale, by a path test that
samples the path and that the log says is not a continuous proof; and every view is
verified at 80 digits and accepted by both of the source’s checkers.
Novelty, local or global optimality and rigidity are not established.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which say the work was produced by Claude (Anthropic) under human
direction; the pinned commit names Claude Opus 5.5 as co-author and says its commit and
push were approved by Evan Daniel.
The record credits each packing to the finder the source names, as T-146 did:

- Francisco Couzo at 204 and 260, the packings of issue #678 (T-223); at 204 his source
  credits Mykhailo Polkovskyi’s construction, and at 260 it says it seeded Joost de
  Winter’s #668 packing from Evan Daniel’s exact-form certificate;
- Francisco Couzo at 227, his #672 refinement of Joost de Winter’s #668 packing
  (T-196), measured above;
- Evan Daniel at 229, his #674 packing (T-199), which started from Couzo’s #672 packing,
  which refines de Winter’s, as the site’s `lineage.yaml` records.

Evan Daniel refreshed each packing from his store, solved it to the exact side stated
(at 229 after a polish), regularized it for display at that side and wrote the
certificate. The bibliography records the source as building on this project, as the
10 October lists’ entry does.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-regularized-2026-10-20 --check
python -m devtools.upper_bound_reports evand-regularized-2026-10-20 check-claims
python -m devtools.upper_bound_reports evand-regularized-2026-10-20 certify \
    --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-regularized-2026-10-20 check --replay
python -m devtools.upper_bound_reports evand-regularized-2026-10-20 register-plan
git -C COUZO cat-file blob 8172d9215ddad902df2e77e038b20a8145437867 > n227.cert
python resources/web/evand-regularized-2026-10-20/measure/identity.py \
    --couzo-672 n227.cert --out resources/web/evand-regularized-2026-10-20/measure/identity.json
```

where `COUZO` is a blobless clone of `franciscouzo/square-packing` holding `af8cb79`.

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/regularize/lists/certs/n-204.cert.gz` | upstream | `9c17f133e7988965854373faddf87b8284266943` | `69e00fd0869aa0bc35e189abeedac70af53a3b0c224acdee8751a5b6c31b002f` |
| `source/search/regularize/lists/certs/n-204.json.gz` | upstream | `4e49b3b2381e38b970d269c30551f31ab2c4f6e0` | `565dd7e6d226ca5ca74c4d83ad11ead8ac765679c72bd5e8a59290e2f8d74de1` |
| `source/search/regularize/lists/certs/n-227.cert.gz` | upstream | `1bb6672f0d5cc4edd43acaa7bf78e0663bad5768` | `dcfaa52b29885220a90faebf86814c29be9a1125989f6d930776a6e0c40f9c3f` |
| `source/search/regularize/lists/certs/n-227.json.gz` | upstream | `9b29981b605124a22b5d278279e6177fe809f39b` | `2c4965ed1827d3d5c10f914f00aec1d1ac2e692fd26f2afea8f12bf977e406d4` |
| `source/search/regularize/lists/certs/n-229.cert.gz` | upstream | `2c04b9525bec405f41919300b705f3ea04d27c28` | `e613256d8fd143026cf3d9a4221f0a525e0ab8d1ee9a2c321033fcfd4916adcc` |
| `source/search/regularize/lists/certs/n-229.json.gz` | upstream | `ee582eec3c01c2c4a86c4e76ec6e48e84e85795f` | `21fc6d7596be3a02987e57febb92f19310d7c2e6c1e3bda98444e63ad97b99cb` |
| `source/search/regularize/lists/certs/n-260.cert.gz` | upstream | `b68dce87585eeed48e6854dbd36588975d7ad58c` | `098be6c5f9ce5b8d2990584187823d808ce153e433b8fa1884ce679da720f037` |
| `source/search/regularize/lists/certs/n-260.json.gz` | upstream | `9a3b756712aae7b8b2da72f4fc4a0726875d7e95` | `cb3dea1d586244cd1bee36cb0a03c7997e5e169f9edc40b41feea1f59f7dc923` |
