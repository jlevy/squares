# Daniil Ostashev’s Record Packings at c3d17ab

[Issue #501](https://github.com/jlevy/squares/issues/501) reports new packings of 155,
156 and 211 unit squares from
[dostashev/square-packing](https://github.com/dostashev/square-packing/tree/c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49)
and names no revision. This packet pins the repository’s `main` at
`c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49` (tree
`b06d6805b55111d3d911e14e33d629a4a45d7d72`, committed 2026-10-11T13:21:30Z), retrieved
at 2026-10-11T20:35Z.

| n | The issue prints (41019fb) | The README prints (c3d17ab) | Rounded up at 16 places | Issue print less the exact side |
| --- | --- | --- | --- | --- |
| 155 | 12.952425406986414 | 12.952425406958457 | 12.9524254069584562 | $2.80 \times 10^{-11}$ |
| 156 | 12.979172613722533 | 12.979172613644427 | 12.9791726136444261 | $7.81 \times 10^{-11}$ |
| 211 | 14.996336737028043 | 14.996336721336316 | 14.9963367213363157 | $1.57 \times 10^{-8}$ |

Each certificate, `records/n0NNN.sqcert`, gives a rational side and, for every unit
square, a rational centre in $[0, S]^2$ and a rational $t = \tan(\theta/2)$.
The exact sides are fractions whose numerators have 118 and 119 digits; the claim record
keeps them whole.

## Which Revision

The issue was filed at 2026-10-11T07:13Z, when the head was
`41019fb5808e6b62b50dfc7b5bcb0c0f880d5314` (06:16:17Z); its three sides are that
README’s. Three later commits changed the records:

- `662a13d` (11:01:30Z) and `a31a747` (12:24:14Z) lowered 211 twice, by $1.10 \times 10^{-8}$
  and $4.39 \times 10^{-9}$, “same arrangement”.
- `c3d17ab` (13:21:30Z), “155, 156, 211 at the exact optima of their contact topologies”,
  replaced all three certificates and their decimal packings and added step 5 of the
  README’s method.

So each issue side is above the side of the certificate retained here, and the issue’s
$s(n) \le v$ follows from it. Each certificate is admitted at the side the README at the
pin prints, rounded up at 15 places, and was first committed in the pinned commit.
Whether the author wants the record to carry the later sides is one of the questions in
the acknowledgement.

## Retained Here

The repository is MIT-licensed (`LICENSE`, Copyright (c) 2026 Daniil Ostashev, added in
`c6893aa`), and its README says the licence covers the verification code and the record
packings and certificates. `devtools.acquire_source` wrote the packet from a checkout at
the pin, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json), and retains every file of
the tree but `.gitignore` byte-identical under `source/`, with the licence beside them:
38 files, 449,392 bytes. [acquisition/sources.json](acquisition/sources.json) is the
acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256)
the manifest, each file bound to its Git blob at the pin.

| Upstream path | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `records/n0155.sqcert` | 77556 | `6c6949e837513e2b9257b70f5a6b6cb864e16f825c5997a62b1903cb9a69bf7b` | The n = 155 certificate |
| `records/n0156.sqcert` | 81191 | `694dcbf9f20ddb1ef19678fcbf7905736658834b0f2b31312d6d67380ca2534a` | The n = 156 certificate |
| `records/n0211.sqcert` | 108179 | `4b2275abb50f2fed96bd7014f0cee1661cb737c9c878403cf74e1fd79ad5d6c4` | The n = 211 certificate |
| `records/n0NNN.sqpk` | 73269 | in the manifest | The 60-digit decimal packings the certificates were built from |
| `verify/`, `tools/`, `verify_all.sh` | | in the manifest | The author’s C++ GMP checker, mpmath cross-check and driver, not run |
| `README.md`, `LICENSE` | | in the manifest | Author prose and the licence |

## The Format

`.sqcert` is the author’s: lines beginning with `#` are comments, then `n N`, `s S` and
`N` lines `x y t`, every number an integer or `p/q`. It is Evan Daniel’s format with the
header split over two labelled lines. The header comments name the decimal packing,
`claimed_s` (the 60-digit side) and `delta: 1e-60`: the certificate’s centres and side
are the 60-digit optimum multiplied by $1 + 10^{-60}$, and each $t$ is rounded to 70
places. `devtools.upper_bound_reports` reads the format through its `sqcert` adapter,
which reads the comments as labels and believes nothing in them; a test holds each
retained side to its `claimed_s` times $1 + 10^{-60}$.

## Exact Replay

Only the retained certificates enter geometry decisions, through the maintained two-route
kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and
the independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion. Each count ran a positive job, a
duplicate-square control and an outside-container control, each in its own child
process, on one worker.

All three positives pass both routes, and both routes refuse all six controls, each on
the overlap or the wall it was built to break. In every positive the two routes find the
same least wall clearance and the same least pair gap, each between
$4.99 \times 10^{-21}$ and $5.01 \times 10^{-21}$, which comes from the $1 + 10^{-20}$ scaling of the load-bearing
squares that the README describes and is far above the $10^{-60}$ dilation. The nine jobs made 277,080 pair decisions
in 280.98 route CPU seconds and 595.29 job wall seconds, summed; the longest, the 211
positive, took 118.47 seconds. The one-worker run took 10 minutes 22 seconds of wall
time with the machine at a load of 9 to 16. A fresh serial `check --replay` decided all
nine jobs again, equal to the retained rows apart from timing, in 10 minutes 34 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and the third exact route
(`devtools.check_half_angle_area`) has not read these certificates.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at `main` `3a5a91a90` (11 October 2026); `check-claims` rebuilds it, each case
ceiling from its holder’s own packet and T-128’s side from its own packet.

| n | Case ceiling, holder | Below it by | Other pending reports | Smallest |
| --- | --- | --- | --- | --- |
| 155 | 12.9525032026045129, SQUISH (Nate Chaoweeraprasit, T-115) | $7.78 \times 10^{-5}$ | T-128 (#451), Francisco Couzo’s refinement of SQUISH’s packing, above by $7.35 \times 10^{-5}$ | this certificate |
| 156 | 12.9820826985168931, Evan Daniel’s exact optimum of Francisco Couzo’s packing (T-098) | $2.91 \times 10^{-3}$ | none | this certificate |
| 211 | 14.9979607049673616, Evan Daniel’s exact optimum of Joost de Winter’s packing (T-098) | $1.62 \times 10^{-3}$ | none | this certificate |

The previous bests the issue names are these, and its improvements agree with the
distances above. None of the other reports of 11 October (#500, #503 to #506) names any
of these counts.

## What Is Not Established

The README states that each side is the exact optimum of its packing’s contact topology,
solved to 60 digits with nonnegative KKT multipliers. That is the author’s report of
local optimality, not a bound, and nothing here checks it. Neither the author’s C++
checker nor the mpmath cross-check ran here. The certificates establish finite upper
bounds only.

## Credit

The README credits Daniil Ostashev with the packings, constructed from scratch: “No
existing record geometry is used.” It names the methods it used: a V-shaped tilted band
built at a chosen angle with aligned corner blocks chosen by an integer program,
re-hardening on a GPU by Yohei Nakajima’s soft-to-rigid method, the fixed-angle linear
program it calls the “cell” idea of this project, and rational certificates that follow
Ryan Xu’s construction. It cites a write-up, *Square Packing* (Daniil Ostashev, October
2026), that the repository does not hold. Neither the repository nor the issue says
whether AI tools assisted.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source dostashev-records-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-records-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-records-2026-10-11 check --replay
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
