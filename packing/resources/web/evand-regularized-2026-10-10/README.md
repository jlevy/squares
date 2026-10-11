# Evan Daniel’s Regularized Record Lists: Fifteen Certificates

Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7/search/regularize)
added display-regularized drawings of the record packings for $n = 1$ to $324$ in
`346c6ed` (2026-10-10T18:05:38Z), with one exact rational certificate per count under
`search/regularize/lists/certs/`. Commit `122d0ba` (2026-10-10T19:21:18Z) refreshed the
lists and the method log, and nothing under `search/regularize/` has changed since.
No issue reports them.
Lane L26 of the 10 October intake compared all 329 of the lists’ certificates exactly
with every value the register held. At fifteen counts the certificate is below all of
them, and this packet retains those fifteen.

The packet pins the branch head when the sources were retrieved,
`ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7` (tree
`ce00909386d0a1b4800a21d7d36436156a447a81`, committed 2026-10-10T20:37:25Z). The pass
had read the head at `baf9143`. The one commit after it changes only the n = 17 Lean
modules, their generator `search/exact/lean_batch.py` and `TODO.md`.
Every file retained here is the same at `122d0ba`, `baf9143` and the pin, and the
fifteen certificates and their JSON are unchanged since `346c6ed`, which dates the
claim. Nothing the claim depends on is older than the head, so the head is the pin, as
stage 1 of the import runbook asks. The sources were retrieved at 2026-10-10T20:45Z.

| n | Exact side of the certificate | Rounded up at 16 places |
| --- | --- | --- |
| 70 | `8880960371555579594785501178639/1000000000000000000000000000000` | 8.8809603715555796 |
| 102 | `10605828696431578360490734944053/1000000000000000000000000000000` | 10.6058286964315784 |
| 103 | `10679232047361306442680936279997/1000000000000000000000000000000` | 10.6792320473613065 |
| 123 | `2897844536374424539887715795867/250000000000000000000000000000` | 11.5913781454976982 |
| 129 | `371000932783786874179763432249/31250000000000000000000000000` | 11.8720298490811800 |
| 146 | `6291891138707538440974154877957/500000000000000000000000000000` | 12.5837822774150769 |
| 153 | `402250932783786874180075932249/31250000000000000000000000000` | 12.8720298490811800 |
| 236 | `3172791149431853484523540541259/200000000000000000000000000000` | 15.8639557471592675 |
| 258 | `16563448002133789379765816191273/1000000000000000000000000000000` | 16.5634480021337894 |
| 263 | `16733166007899378970679613144039/1000000000000000000000000000000` | 16.7331660078993790 |
| 269 | `16901513582189132198548012552701/1000000000000000000000000000000` | 16.9015135821891322 |
| 292 | `4397844536374424539902715795867/250000000000000000000000000000` | 17.5913781454976982 |
| 295 | `1106514549421001897378505810757/62500000000000000000000000000` | 17.7042327907360304 |
| 302 | `558500932783786874181638432249/31250000000000000000000000000` | 17.8720298490811800 |
| 303 | `8956532731369266152919876895603/500000000000000000000000000000` | 17.9130654627385324 |

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the format of issues
#375, #399 and #465.
Every side terminates within 30 places. The certificate’s 50-digit JSON beside it,
`n-NNN.json.gz`, prints the same side exactly as `S_cert`, which is the side each row
of the import declaration offers.
The method log says that each certificate is the regularized packing scaled by
$1 + 10^{-20}$ about the origin corner, so that $S' = S^* + {\sim}10^{-19}$, where $S^*$
is the exact side of the packing. Every certificate’s side is the `S_exact` its JSON
prints times a factor within $10^{-22}$ of $1 + 10^{-20}$.

## The Author’s Framing

The source does not claim these as records, and the import keeps that framing.
The method log, `REGULARIZE.md`, under “Refresh from the store”, says:

> No refreshed side is below the store's best beyond rounding (2e-12 .. 8e-10, the exact
> optimum of the same packing; 305 matched a pending Couzo packing that arrived mid-run,
> both certificate checkers VALID).

Every certificate’s JSON says:

> regularized display view of a certified packing at the same side; not a new bound

So the author regards each side as the exact optimum of a packing he already had, below
its posted side only by rounding.
The register held the sides those packings were posted at, each a little above, and
none of these.
Each side is a value the register did not hold, as T-139’s unclaimed `n126_xu`
certificate and T-137’s refinement of Ryan Xu’s 70 were, and a finite certificate of it
is an upper bound the record did not have.
The certificate header calls itself an “exact certificate (regularized display view,
search/regularize)”.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
38 files, 371,794 bytes.

The fifteen certificates and their fifteen JSON files are retained as the upstream gzip
files they are, `search/regularize/lists/certs/n-NNN.cert.gz` and `n-NNN.json.gz`,
never recompressed; the [Original Gzip Files](#original-gzip-files) table binds their
compressed bytes. The importer and the third route decompress them to read them.
The packet also retains the method log `search/regularize/REGULARIZE.md`, `LICENSE` and
`CREDITS.md`: 33 files and 168,133 bytes in all.

Five files are pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why |
| --- | --- | --- | --- |
| `search/regularize/lists/best.csv` | 53983 | `f696b02a76a06c23f915b7be92fd7aea558ec121c913869b77264533907fbf05` | The best-choice list of all 324 counts, whose rows name each certificate, its variant, its path-test level and the source’s finder |
| `search/regularize/lists/best.json` | 120299 | `f98c94ab165287d71c177ad2a3961998b3acf2049a76568df2dfbfa7e1614af9` | The same list as JSON |
| `site/data/records2026.json` | 22877 | `16f0f4fa722345ffa8ad5927c08a15003ecc74e8888b69f8904b77ea391e12c4` | The source site’s provenance of the records newer than the catalogue, which credits each to its first posting (see [Credit and Licence](#credit-and-licence)) |
| `search/exact/verify_cert.py` | 3401 | `3299ca0c0f02f7c221deeea69a9a85b5a90db6bc410b20727fdff211c92bed52` | The source’s first exact checker |
| `search/exact/verify_cert2.py` | 3101 | `55140a35d95d9eaa64a14c3b044641efbcda94ebfc3b12b7dec9fa52692e31d3` | Its second |

The two checkers are byte-identical to the copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run. The lists’ other 314 certificates, their JSON, the alternates, the atlas images and
the rest of the tree are pinned by the commit alone and were neither retained nor run.

## Exact Replay

Only the fifteen certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
by the declaration-driven importer `devtools.upper_bound_reports`, which the 10 October
imports also used.
The two routes are `sqpack`’s exact witness verifier and the independent rational corner
checker. Each decides every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All fifteen positives pass both routes.
Both routes refuse all thirty controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance, exactly
`1/200000000000000000000` ($5 \times 10^{-21}$), the origin-corner scaling’s, and the
same least pair gap, just under $10^{-20}$.
The 45 jobs made 2,155,368 pair decisions in 413.8 route CPU seconds and 566.29 job wall
seconds, summed. The longest job, the outside-container control at 295, took 39.16
seconds. The two-worker run took 5 minutes 2 seconds of wall time.
Other lanes held the four-core machine at a load average of 6 to 8 during the run, so
the walls overstate the work and the route CPU seconds do not.
A fresh serial `check --replay` decided all 45 jobs again, equal to the retained rows
apart from timing, in 7 minutes 56 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Each certificate was also decided by the third exact route,
`devtools.check_half_angle_area decide-imports --imports regularized`, which reads the
certificate with its own parser, after decompressing the upstream gzip itself, and
decides containment by each square’s half-extent and overlap by exact clipping.
That route accepts all fifteen and reaches the required outcome on all 90 of its
controls. It finds the same least wall clearances as both maintained routes and a least
Euclidean distance between squares of $1.00 \times 10^{-20}$ at every count.
Run with `--upstream` against the checkout at the pin, it holds each retained gzip,
certificate and JSON alike, to its upstream bytes as stored, and each offered side to
the `S_cert` its JSON prints: 30 checks, no disagreement.
The run decided 359,228 pairs in 111 seconds on two workers.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record as it stood when it was read: the intake branch at `125b0340f`, on `main` at
`af17208c0`, 10 October 2026.
`check-claims` rebuilds it, the case ceilings and every pending report from their own
retained packets, so nothing here is compared at a print:

| n | Case ceiling, holder | Below it by | Pending reports at the count, each above the certificate by |
| --- | --- | --- | --- |
| 70 | 8.8809603717088810, Ryan Xu (T-125) | $1.53 \times 10^{-10}$ | #483 (T-137, Eric Deleeuw) $1.07 \times 10^{-11}$ |
| 102 | 10.6058286965106059, Ryan Xu (T-125) | $7.90 \times 10^{-11}$ | none |
| 103 | 10.6792320475106793, Ryan Xu (T-125) | $1.49 \times 10^{-10}$ | #470 (T-138, Mishapolk) $6.94 \times 10^{-13}$ |
| 123 | 11.5913781457115914, Ryan Xu (T-125) | $2.14 \times 10^{-10}$ | none |
| 129 | 11.8720298492118721, Ryan Xu (T-125) | $1.31 \times 10^{-10}$ | none |
| 146 | 12.5837822775125838, Ryan Xu (T-125) | $9.75 \times 10^{-11}$ | none |
| 153 | 12.8796793733293146, SQUISH improved by Siddharth Gupta (T-127) | $7.65 \times 10^{-3}$ | #481 (T-136, SQUISH) $8.48 \times 10^{-16}$ |
| 236 | 15.8678008394199166, SQUISH improved by Siddharth Gupta (T-127) | $3.85 \times 10^{-3}$ | #481 (T-136) $3.29 \times 10^{-16}$ |
| 258 | 16.5634480021391540, SQUISH (T-115) | $5.36 \times 10^{-12}$ | #470 (T-138) $4.21 \times 10^{-12}$ |
| 263 | 16.7404196795387766, SQUISH (T-116) | $7.25 \times 10^{-3}$ | #481 (T-136) $5.05 \times 10^{-13}$; #476 (T-134, Francisco Couzo) $7.25 \times 10^{-3}$ |
| 269 | 16.905967058583840911467960094275, Couzo improved by Evan Daniel (T-098) | $4.45 \times 10^{-3}$ | #481 (T-136) $6.73 \times 10^{-16}$; #476 $4.45 \times 10^{-3}$, equal to the case |
| 292 | 17.597249391156465040471442005510391858592626557, Couzo improved by Seth Rehwaldt (T-117) | $5.87 \times 10^{-3}$ | #481 (T-136) $2.03 \times 10^{-13}$ |
| 295 | 17.7042327915177043, Ryan Xu (T-125) | $7.82 \times 10^{-10}$ | none |
| 302 | 17.8813062180958085, SQUISH (T-116) | $9.28 \times 10^{-3}$ | #481 (T-136) $2.21 \times 10^{-17}$; #470 (T-138) $9.28 \times 10^{-3}$ |
| 303 | 17.9203123729203498, SQUISH (T-113) | $7.25 \times 10^{-3}$ | #481 (T-136) $4.48 \times 10^{-16}$; #488 (Francisco Couzo) $4.30 \times 10^{-3}$; #476 (T-134) $4.38 \times 10^{-3}$; #470 (T-138) $7.25 \times 10^{-3}$ |

At every count the certificate is the smallest side the record holds or has pending.
The least value it is below is the case ceiling at the five counts where Ryan Xu’s
packing is the smallest, by $7.90 \times 10^{-11}$ to $7.82 \times 10^{-10}$; T-137 at
70; T-138 at 103 and 258; and T-136 at the seven others, by $2.21 \times 10^{-17}$ to
$5.05 \times 10^{-13}$. That is lane L26’s triage, rederived here from the packets.
Issue #488’s side at 303 is a certificate its packet holds to its README’s print and no
register entry cites; it is listed because the record retains it.
A report the case already beats is not listed, such as T-098’s exact optima at the
counts other entries have since improved, or Mishapolk’s sides at 153, 236 and 263.

### Pose by Pose

The register would credit each certificate to the packing whose side it lies just below
(see [Credit and Licence](#credit-and-licence)). The third route measures how far each
is from that packing, square by square (`CREDITED`, `arrangement_gap`). Under each of
the box’s eight symmetries it matches every square to the nearest centre of the other,
keeps the symmetries where that is one to one, and reports the best. It is a
measurement, and decides nothing:

| n | Against | Symmetry | Squares moved beyond $10^{-9}$, $10^{-6}$, $10^{-3}$, $10^{-1}$ | Largest move | Turned beyond $10^{-6}$ |
| --- | --- | --- | --- | --- | --- |
| 70 | T-137 | identity | 20, 10, 10, 3 | 0.222 | 6 |
| 70 | T-125 | identity | 10, 10, 10, 3 | 0.222 | 6 |
| 102 | T-125 | quarter turn | 22, 22, 18, 6 | 0.169 | 1 |
| 103 | T-138 | three quarter turns | 16, 16, 15, 0 | 0.0738 | 1 |
| 123 | T-125 | none one to one | | | |
| 129 | T-125 | none one to one | | | |
| 146 | T-125 | identity | 25, 25, 25, 3 | 0.124 | 0 |
| 153 | T-136 | half turn | 109, 109, 80, 0 | 0.0652 | 25 |
| 236 | T-136 | identity | 96, 94, 53, 0 | 0.0681 | 15 |
| 258 | T-138 | identity | 72, 55, 48, 13 | 0.496 | 4 |
| 263 | T-136 | reflection, then a quarter turn | 162, 160, 132, 0 | 0.0488 | 30 |
| 269 | T-136 | three quarter turns | 69, 68, 54, 0 | 0.0880 | 18 |
| 292 | T-136 | none one to one | | | |
| 295 | T-125 | identity | 190, 148, 122, 37 | 0.138 | 0 |
| 302 | T-136 | identity | 256, 238, 198, 2 | 0.102 | 80 |
| 303 | T-136 | three quarter turns | 53, 35, 19, 1 | 0.135 | 7 |

Where a symmetry matches, it is the re-orientation the lists’ `orientation` column
states. The regularization then slides and turns squares at the same side, as the
method log says it does: gravity, symmetry, merged rotation groups and coincident faces.
So the measurement shows that each view differs from the credited certificate pose by
pose. It neither confirms nor refutes that it is the same packing, which is the
source’s path-test statement. At 123, 129 and 292 the slides are large enough that
nearest centres match one to one under no symmetry.
At 70 the view lies nearer Ryan Xu’s poses than Eric Deleeuw’s refinement of them: 60
squares within $10^{-9}$ of Xu’s and 50 of Deleeuw’s.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source makes three statements about them that are not replayed here.
First, each side is the exact optimum of the store’s best packing at its count.
Second, each regularized view is the same packing at that side, level 2 of the method
log’s scale, “traversable without expansion”, by a path test that rotates the changed
squares in steps of at most 0.01 degrees and re-solves translations at each step; the
log says the test samples the path and is not a continuous proof.
Third, every regularized packing is verified at 80 digits and accepted by both of the
source’s checkers.
Novelty, local or global optimality and rigidity are not established, and neither is
which earlier packing each certificate is the optimum of.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, whose provenance section says the work was produced by Claude (Anthropic)
under human direction.
As T-098 did for Evan Daniel’s first exact optima, the record credits each packing to
the finders it already credits for the side the certificate lies just below:

- Ryan Xu (ry-xu, issue #432) at 70, 102, 123, 129, 146 and 295; at 70 Eric Deleeuw
  had refined Ryan Xu’s packing (issue #483, T-137);
- Mishapolk (issue #470, T-138) at 103 and 258, whose packings there refine Ryan Xu’s
  and SQUISH’s;
- Nate Chaoweeraprasit’s SQUISH (issue #481, T-136) at 153, 236, 263, 269, 292, 302 and
  303, composed from pieces of Francisco Couzo’s, Ryan Xu’s and earlier packings.

Evan Daniel refreshed each packing from his store, solved it to the exact side stated,
regularized it for display at that side and wrote the certificate.
His site’s provenance file, `site/data/records2026.json`, which `122d0ba` generated from
this register at `af17208`, gives the same first postings: issue #432 at 70, 102, 103,
123, 129, 146 and 295, issue #401 (SQUISH) at 258 and issue #481 at the seven others.
It names issue #470 as a second posting at 103 and 258, and nothing of issue #483 at 70.
Its refiners are those whose sides the case records hold: Siddharth Gupta at 153 and
236, Evan Daniel at 269 and Seth Rehwaldt at 292.
His lists name another credit, the finder of the arrangement each record descends from:
Joe DeVincentis at 70; Francisco Couzo at 102, 103, 123, 236, 263, 269, 292, 302 and
303; David Ellsworth at 129 and 153; David W. Cantrell at 146; and no one at 258 and
295.
The method log says the regularized packings were made for this project’s poster, with
their orientations fitted to this project’s known-best witnesses, so the bibliography
records the source as building on this project.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-regularized-2026-10-10 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-regularized-2026-10-10 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-regularized-2026-10-10 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-regularized-2026-10-10 check --replay
uv run --frozen --all-extras --group dev python -m devtools.check_half_angle_area decide-imports --workers 2 --imports regularized
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.
`decide-imports` takes `--upstream evand-regularized-2026-10-10 CHECKOUT` with a
checkout at the pin, to hold the retained files to their upstream bytes.

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/regularize/lists/certs/n-070.cert.gz` | upstream | `60a792124352dd258aa88beaa3cb188d6e747083` | `65b1c4698129560857ad4f91ec9a7a12980de0ceb619bcc814e55a3fd9ef597d` |
| `source/search/regularize/lists/certs/n-070.json.gz` | upstream | `5a1748e08de9c009e61bc1ad315db36294e1999b` | `5beada6b9c23c2da7610ce22e3f00dbe2417432939a98ad2a7d52e8f2acacd1f` |
| `source/search/regularize/lists/certs/n-102.cert.gz` | upstream | `1d078c6b8a04bca1cb94778c18d9448eba2587d3` | `b0e9e73533eb6ea05e0a399366f735fd2bf1278b145363ecb77c5c1fcfc78d95` |
| `source/search/regularize/lists/certs/n-102.json.gz` | upstream | `0b2318ef424c1389cf3c5ab4b77e8ffef24b7fa8` | `c2a457fe72073d6040b8a4e8728308c3ded931c9614b53b83d4ae303cf67a587` |
| `source/search/regularize/lists/certs/n-103.cert.gz` | upstream | `aaec186b5ee99ec857f17bf67d2369dee5f5b956` | `d8f606b5173fffc0b75a09724f956019fcb03ba9ba976c5d15b29ab22bcf9d54` |
| `source/search/regularize/lists/certs/n-103.json.gz` | upstream | `3943f9a9ecfe2af7c7b29390349a8e1878f301d7` | `248b666a2a101f380e42a03c6e6e99b7bac57df51d68e480ff8979800f2e2e69` |
| `source/search/regularize/lists/certs/n-123.cert.gz` | upstream | `c1f8aa9773445d2ba660abeb6fbfcca4961e69ec` | `46139e2c6c476d422afe18b8d730e56f80f0d6e023a1470225d000296f3cc2a0` |
| `source/search/regularize/lists/certs/n-123.json.gz` | upstream | `f526ad809e05ea080271a620e97821de768e704b` | `fabea3e9e3688d5e742bc2210d2f4e2c394cb989e7902c4a4f56bfc5ded14ef6` |
| `source/search/regularize/lists/certs/n-129.cert.gz` | upstream | `0f50d318ee02a8fe683bdce82a1b328fcd52ca51` | `1c55cc2a293596bded4efdccca3c826e547517268db2e43be07b3f2f28e7f826` |
| `source/search/regularize/lists/certs/n-129.json.gz` | upstream | `a242620ab11f005d4b1ec7d3a54fa946f3ffe609` | `56edf7fea71529949188aee475e77ad972cd47a5e911fd8ea1cee183a4daa31f` |
| `source/search/regularize/lists/certs/n-146.cert.gz` | upstream | `343d4e24a370518eb89d1d80ca85ad48971342f3` | `31d7fdd68a1ed39849a7d994979dd39d361b393fc426066c627702f076cbbf0e` |
| `source/search/regularize/lists/certs/n-146.json.gz` | upstream | `29781051708d46fa470881b9489bf93c1a09a45f` | `7807640cd3b6be48d9bd7ee89c433b0c9b7ac8420227bf79e2abf83eaf34adbd` |
| `source/search/regularize/lists/certs/n-153.cert.gz` | upstream | `d171438370a93890201c7a33f340c03e1ab2e52a` | `46b76905c084e2fa120f8fe172a632d81c17c84b8c1dd384703f402498c6f11c` |
| `source/search/regularize/lists/certs/n-153.json.gz` | upstream | `4de3c82d0315c70abdb3f5c26bed234444ffec7b` | `0a0d2f590e01d3c2788abd4a46dec30cae305b67f873062d5e5acb5aba454e3b` |
| `source/search/regularize/lists/certs/n-236.cert.gz` | upstream | `13d009de92dbc66db401d2c6b2695dceab48f8c3` | `6a8bf850a4144273a26051be012a02d6052e7e43ecf90509c4f0d1c28f1635ed` |
| `source/search/regularize/lists/certs/n-236.json.gz` | upstream | `68ee9f02d9a61cf8dcf1f0d8c19b2678ef1195ec` | `52e9d7e303ae8f920a816d1dda74278aa5fe965dd7479a7298956427e09b5548` |
| `source/search/regularize/lists/certs/n-258.cert.gz` | upstream | `846aab5db2900595e459e191a02c235236de5a81` | `f51908c4740ec54b80b82a92311cb06bb58d772da7d8f2015247fe107a9d6b2f` |
| `source/search/regularize/lists/certs/n-258.json.gz` | upstream | `ed982fcba4dcb2ad64dfaf04b9e64452c99b9a05` | `44e9b588acc6b15f72e34645f7f65c00e639bd0b20b286c04d3dfaaec4d2aca6` |
| `source/search/regularize/lists/certs/n-263.cert.gz` | upstream | `98bb86d4e39a64d6264643016f169b0474949c80` | `22390c08e72e8954936517bb7af1e00bc7671afaf8c3840292243d843d251e6d` |
| `source/search/regularize/lists/certs/n-263.json.gz` | upstream | `f14f6b92b8c0b48b852e358867677a86c243d5d6` | `ae8e360efa29df30602edb590df367b211e56759ddff32fac3e77c1ff683f5e0` |
| `source/search/regularize/lists/certs/n-269.cert.gz` | upstream | `37608397425b6e6942b6111528583a1fb0e28928` | `5f2752d5a8fcd444815f531fd2361c15874814740e051363590b7cab459a5fd4` |
| `source/search/regularize/lists/certs/n-269.json.gz` | upstream | `bbfccd3d5acafe1fb47d94096d9730113d5b18e6` | `d67c0c3fff2cfe61123c2666b1003f523ba776629fb75c1a6a5f86ad2ba45b38` |
| `source/search/regularize/lists/certs/n-292.cert.gz` | upstream | `6c674658aa4496953d36ddacc52052003a5e9155` | `1dbf703d6a8fc2073448bcb799e3f331abd7e39e55c219406e813892cf76892e` |
| `source/search/regularize/lists/certs/n-292.json.gz` | upstream | `71deb9015e6a2e887c14c2078743aac28485f4a8` | `97ab03ec939ae08f9297bb98dd59fdc9a291b2ec4202c4dab045bd6c3d4a8ac8` |
| `source/search/regularize/lists/certs/n-295.cert.gz` | upstream | `d7f2d6c91dd20bc40c0b43d5d309880d4e33313c` | `601f04271a738e3e6897178684abd020f8916b5060dcc1bfa87fbce9710b6ba1` |
| `source/search/regularize/lists/certs/n-295.json.gz` | upstream | `a28f51e3d0bdbb1a124ee0a29d5e84bd7470ab6c` | `61ec60614e48116c77d4a9636716304d2502db2bc4d87eeced8a28ed1d2b9e3e` |
| `source/search/regularize/lists/certs/n-302.cert.gz` | upstream | `1ca3b5350798ea4f718301af6a835207b63dbf65` | `57b5d9ab93c32d845243eb9c53bd8e204e04eb0fe43be73a1130d0a40f87bb8e` |
| `source/search/regularize/lists/certs/n-302.json.gz` | upstream | `ccbeb2f8f5fa22d01cdd468507d81df0003cf6a9` | `f8f749388ba5689ac4c73223263036d9d6c74f723fdd8e3b15d4dc1c5055c967` |
| `source/search/regularize/lists/certs/n-303.cert.gz` | upstream | `0567150863dc075ddb9f4ce7b2fd417e02d12e28` | `62ea26fce6c5ec53b22cfc3ec76e929a630fdc079cb676c8d9176d7c199fa846` |
| `source/search/regularize/lists/certs/n-303.json.gz` | upstream | `525dbbe043428f63e8481fbda70408148a0e4675` | `52163910b9a2638d6b30978f1f2b42d12eba03bf21808af53d3eac96099c73e3` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
