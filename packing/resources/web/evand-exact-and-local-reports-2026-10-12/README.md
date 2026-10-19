# Evan Daniel’s s(29) Minimal Polynomial and Grade-C Local Minima

Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/ad86d42d0f743076d735036702ba04a41ce24a8c)
reported two exact results on 11 and 12 October 2026, neither a new bound.
`169a827` (2026-10-11T23:01:11Z) reports the minimal polynomial of the side of the
$s(29)$ record configuration, of degree 7213. `0d0146e` and `e493eea`
(2026-10-12T02:29:22Z and 02:38:47Z) add `search/exact/gradec.py`, a certificate of
local minimality for configurations with exact flat motions (“grade C”), and report it
VALID for 233 of the source’s 250 configurations of field degree at most 4.
No issue reports either.
Lane W of the 12 October intake read the 26 commits from `2b89650` to `ad86d42` past
the `675a5ea` read, found no new upper bound in them, and retains these two reports.

The packet pins the branch head when the sources were retrieved,
`ad86d42d0f743076d735036702ba04a41ce24a8c` (tree
`660a967d5c5727eaa73e1eefa06348d33101f92b`, committed 2026-10-12T04:39:01Z).
`7ea600b` (2026-10-12T04:24:53Z) was the last commit to change a retained file; the
two after it change the packer and the site only.
The sources were retrieved at 2026-10-12T08:40Z.

## The Two Reports

### The minimal polynomial of the s(29) record side

`search/exact/homotopy/N29.md` reports that the side of the record configuration,
$\sigma = 5.93383346267692918968946061635201913843383418107788697463882591508025\ldots$,
is a root of an irreducible integer polynomial $p$ of degree 7213, with a 325-digit
leading coefficient and height of 5074 digits, so $p$ is its minimal polynomial.
The source found it by homotopy continuation on five consistency polynomials in the
five tilted class angles. 44,448 polyhedral paths gave 7,209 regular roots, and four
more, near the singular $S = 5$ grid, were recovered algebraically from a lattice
reduction of the coefficients.
The write-up rates its steps as follows:

| Step | Script | Status the source gives |
| --- | --- | --- |
| $p$ irreducible over $\mathbb{Q}$ (degree patterns modulo 12 primes near $2^{61}$) | `irred.py` | rigorous |
| one zero $t^\ast$ of the eliminated system in a box of radius $10^{-50}$ (Krawczyk, ball arithmetic) | `krawczyk.py` | rigorous |
| shape-lemma parametrization of the angles by $S$ | `param.py` | numerical reconstruction |
| $F_k(\tau) = 0$ and $S_n(\tau) = x S_d(\tau)$ in $\mathbb{Q}[x]/(p)$ | `verify_mod.py` | Monte Carlo, 50 random 62-bit primes |
| the full 152-row contact system consistent at $\tau$ | `contacts_mod.py` | Monte Carlo, 21 random 62-bit primes |
| a root of $p$ whose $\tau$ lies in the Krawczyk box | `link.py` | rigorous |

It says that the non-overlap of the squares at the exact point is not checked, and that
the record’s rational certificate covers validity at a side slightly above.
The coefficients, `work/n29_poly_q4.json` (27 MB), and the parametrization are
gitignored and not published; the write-up names a backup on the author’s own drive.
`7ea600b`’s pickup section plans a grade-C certificate for this configuration next and
says none is written.

### Grade-C local minima at 233 configurations

`tasks/exact-minpoly/grade-C.md` states Theorem C with a paper proof.
A configuration is a local minimum of the side, in the sense of `IsLocalMinPacking`
(no packing in a smaller square within a pose-space ball, the squares matched by index
and angles taken modulo 90 degrees), if three conditions hold. Every row is valid near
it with a margin. Positive multipliers balance the forces along the whole family of
exact flat motions. The reduced Hessian is positive definite on a complement of the
flat directions in the null space.
`gradec.py` checks the three exactly in the number field of the configuration, with
signs by interval arithmetic, and certifies the force balance along the family with
affine null vectors.
Its batch ran over the 250 configurations of field degree at most 4 in
`search/exact/minpoly/results.json`, with 8 jobs and a 30-minute cap on each:

- 231 VALID with every load-bearing incidence as a row;
- 230 and 261 VALID with `GRADEC_DROPZERO=1`, which drops 24 rows that carry zero force
  in every multiplier vector; dropping constraints only relaxes the problem;
- 17 timeouts: 174, 201, 204, 231, 234, 257, 262, 274, 275, 295, 296, 299 and 308 to
  312.

`gradec_runs/_status.txt` and `_dropzero_status.txt` give each run’s exit code.
The certificates `minpoly/solve/n-N.gradec.json`, their `n-N.contacts.json` inputs and
the logs are gitignored and not published.
The note reports that the mutation tests are rejected with the option on.

## Against the Record

Compared on 12 October 2026 with the case records of local branch `l4` (layer 4 of the
2026-10-11 stack, which carries `T-147` to `T-152`) and the register there.

**$n = 29$.** The case holds Kingbird’s $5.93383346267692$, Thomas Schadt’s packing
improved by David Ellsworth, and the verified rational ceiling
$5.93383346267692918974379895098$ from an interval enclosure.
$\sigma$ is below that ceiling by $5.43 \times 10^{-20}$, as an outward-rounded
enclosure’s endpoint must be. The case record says no minimal polynomial is known “in
the literature or here”, and holds `algebraic_degree: null`.
The report is the first algebraic degree for this side.
It bounds nothing below the ceiling, because the source does not decide the packing at
$\sigma$.

**The grade-C roster.** `T-124` holds Evan Daniel’s reported non-strict local minima
for 178 configurations, with Lean proofs. 169 of the 233 grade-C counts are in its
scope; 64 are not.
At 222 of the 233 counts the roster’s exact side equals the case’s reported upper bound
within $10^{-9}$.
At eleven it is above it, by $7.1 \times 10^{-4}$ to $1.2 \times 10^{-2}$: 70, 84, 86,
127, 153, 175, 176, 232, 258, 261 and 267. There the roster, last changed on 7 October,
holds a configuration the record has since superseded.
That leaves 53 counts at which grade C reports local minimality of the case’s current
packing and `T-124` holds nothing: 5, 10, 18, 19, 26, 27, 38, 40, 50, 52, 53, 54, 65, 66,
67, 82, 85, 89, 101, 104, 107, 109, 122, 124, 125, 145, 147, 148, 149, 150, 151, 170,
171, 173, 178, 197, 198, 200, 202, 203, 226, 227, 229, 230, 233, 260, 264, 265, 290,
291, 293, 294 and 298. Two of them, 5 and 10, are proved cases.
The configurations themselves are not published, so “equals” here compares sides, not
poses.

**$n = 230$ and $261$.** The retained inputs give exact sides $643/41$ and $684/41$.
At 230 that is the case ceiling, $15 + 28/41$.
At 261 the case holds Robert Barnett’s refinement of Ryan Xu’s packing, `T-150`,
$16.678779875343207747\ldots$; $684/41 = 16.682926829\ldots$ is above it by
$4.15 \times 10^{-3}$. So the grade-C result at 261 concerns a superseded configuration
and says nothing about `T-150`’s packing.

## What Is Not Established

Nothing here was run.
The minimal polynomial cannot be checked from what is published: the polynomial, the
parametrization and the roots are not in the repository.
The grade-C certificates and their contact inputs are not published either, so the
VALID verdicts are the source’s statements.
`gradec.py` is the source’s own generator and checker in one program, its Theorem C has
a paper proof and no formal one, and its rows, null vectors and Hessian minors were not
inspected here.
Neither report bears on a bound, on global optimality or on rigidity.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
48 files, 320,519 bytes.

Retained: `search/exact/homotopy/` (the write-up, its Python and Julia scripts and the
Julia environment); `gradec.py`, `gradec_explore.py` and `gradec_runs/`; the modules
`gradec.py` imports from its directory, `localmin.py`, `verify_exact.py` and `geom.py`,
with `env.sh`; the roster `minpoly/results.json`, stored compressed; the inputs at 230
and 261, `minpoly/data/n-230.minpoly.json.gz` and `n-261.minpoly.json.gz`, as the
upstream gzip files they are; the task notes `tasks/exact-minpoly/grade-C.md` and
`README.md`; `LICENSE` and `CREDITS.md`. That is 47 files and 296,637 bytes.

One file is pinned by digest only:

| Upstream path | Bytes | SHA-256 | Why |
| --- | --- | --- | --- |
| `search/exact/homotopy/install.log` | 23882 | `7ec598e12c04ca57c819de059f6e9ce728949f0c658e4d0f6ba74b43e7c4bae8` | The log of installing the Julia packages the retained manifest pins |

The other minpoly inputs and the rest of the tree are pinned by the commit alone.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, whose provenance section says the work was produced by Claude (Anthropic)
under human direction. Every commit read here is co-authored by Claude Opus 5.5.
The $s(29)$ configuration is Thomas Schadt’s, improved by David Ellsworth; the minimal
polynomial and its computation are Evan Daniel’s.
Theorem C, `gradec.py` and the batch are Evan Daniel’s; each configuration keeps the
credit its case record gives.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-exact-and-local-reports-2026-10-12 --check
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/exact/minpoly/results.json.gz` | upstream | `d2224d16af950cc6d7b956a157cafe99ca9946b1` | `779a43419c1ba68739f07d3c3191273b91c2ad8da0d612619ddae122dc11a7ba` |

## Original Gzip Files

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `source/search/exact/minpoly/data/n-230.minpoly.json.gz` | upstream | `def71b5fcd450fd50bc9c2d8fc2d61e506f3c8b7` | `9579351d00f7869a572bd91a2fa9c87c12f5a8daa48cca740917ab1f4f05206a` |
| `source/search/exact/minpoly/data/n-261.minpoly.json.gz` | upstream | `9353bfc2ab2254e8f6062e38766079d838cc91cc` | `5b6fb045e27f354570e6a0dd2fef276b0ad911c38e153f13cf2c1b2957948756` |
