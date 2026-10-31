# Evan Daniel’s Certificates at 172, 204, 260 and 293 at d2d5dd9

This packet retains the four certificate sets Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d/search/packer/candidates)
adds at `d2d5dd96cfdbded476050f8ba8577773a91c6ac1` (committed 2026-10-29T04:33:59Z),
unchanged at the pin `0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d`, the head on 31 October
2026. Issue [#845](https://github.com/jlevy/squares/issues/845), opened 12 minutes 41
seconds after the commit, reports them.

## What the Source Claims

- search/packer/candidates/s172_1028.cert states s(172) <= 2723587139676283080823463207799/(2*10^29) = 13.617935698381415404...; issue #845 (opened 2026-10-29T04:46:40Z by evand) reports 13.617935698382, 1.05e-3 below the register's 13.618988956900 (Francisco Couzo), as an exact KKT point, a local minimum of S strict modulo 69 exact flat motions by numerical evidence at 80 digits, and a new packing (another local minimum from the register's) found from the s(199) record of Nate Chaoweeraprasit (itsnaka), improved by Siddharth Gupta, by an L-strip removal; s172_1028_regularized.cert is a regularized view at the same side.
- s204_1028.cert states s(204) <= 14807627471881579627471866771703/10^30 = 14.807627471881579627...; the issue reports 14.807627471882, 1.02e-3 below the register's 14.808642830514, a dilation certificate of s204_1028.input.txt (the exact solver did not converge), and a new packing found from Daniil Ostashev's s(176) packing (#575) used as a seed at 204.
- s260_1028.cert states s(260) <= 8316991251060941991251052624833/(5*10^29) = 16.633982502121883982...; the issue reports 16.633982502122, below #844's 16.637029558871 and the register's 16.645753250520, a dilation certificate, and a new packing whose binding block came from a search started from Kirill T (kirilltym)'s s(260) in his public Kaggle notebook 'Square Packing Lab | CPU/CUDA/MPS' (side 16.638543986, 26 October).
- s293_1028.cert states s(293) <= 8816991251061390991251052573823/(5*10^29) = 17.633982502122781982...; the issue reports 17.633982502123, 1.64e-4 below the register's 17.634146341464 (David Ellsworth's 723/41), a dilation certificate of the 260 packing plus one L-shaped strip (Friedman's L step), with the same credit as 260.
- The issue says the source's two exact checkers, search/exact/verify_cert.py (separating axes) and verify_cert2.py (polygon intersection), both report VALID on all five certificate files, and that they share an author and the certificate format; it quotes Kaggle per-puzzle leaderboard sides at 172, 204 and 293 below these, with no coordinates. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 25 files: 23 retained under [source/](source/) (351,622 bytes) and 2 pinned by digest.

| File | Bytes |
| --- | --- |
| `CREDITS.md` | 7,501 |
| `LICENSE` | 1,068 |
| `search/packer/candidates/s172_1028.cert` | 27,129 |
| `search/packer/candidates/s172_1028.exact.txt` | 27,661 |
| `search/packer/candidates/s172_1028.input.txt` | 9,180 |
| `search/packer/candidates/s172_1028.json` | 4,199 |
| `search/packer/candidates/s172_1028_prior.json` | 3,493 |
| `search/packer/candidates/s172_1028_regularized.cert` | 25,534 |
| `search/packer/candidates/s172_1028_regularized.json` | 23,639 |
| `search/packer/candidates/s172_1028_vs_prior.json.gz` | 2,970 |
| `search/packer/candidates/s204_1028.cert` | 30,271 |
| `search/packer/candidates/s204_1028.exact.txt` | 40,045 |
| `search/packer/candidates/s204_1028.input.txt` | 11,229 |
| `search/packer/candidates/s204_1028.json` | 4,544 |
| `search/packer/candidates/s204_1028_prior.json` | 1,839 |
| `search/packer/candidates/s260_1028.cert` | 36,826 |
| `search/packer/candidates/s260_1028.input.txt` | 12,967 |
| `search/packer/candidates/s260_1028.json` | 538 |
| `search/packer/candidates/s260_1028_prior.json` | 975 |
| `search/packer/candidates/s293_1028.cert` | 41,538 |
| `search/packer/candidates/s293_1028.input.txt` | 14,467 |
| `search/packer/candidates/s293_1028.json` | 542 |
| `search/packer/candidates/s293_1028_prior.json` | 8,485 |
| `search/exact/verify_cert.py` | 3,401, pinned by digest |
| `search/exact/verify_cert2.py` | 3,101, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **172:** exact side 13.6179356983814155…, below the case’s house (T-174) by 1.05e-03; below T-244 (#804) by 1.05e-03 (requested).
- **204:** exact side 14.8076274718815797…, below the case’s house (T-231) by 1.02e-03 (requested).
- **260:** exact side 16.6339825021218840…, below the case’s house (T-225) by 1.18e-02; below T-255, Couzo of 28 October (no issue) by 4.55e-03; below T-256 (#844) by 3.05e-03 (requested).
- **293:** exact side 17.6339825021227820…, below the case’s house (T-101) by 1.64e-04 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 172, 204, 260 and 293; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **172** ([measure/identity-n172.json](measure/identity-n172.json)): against T-174, no symmetry one to one; the optimal assignment (symmetry 0) moves 42 squares beyond 0.1 and 66 beyond 0.01 (largest 0.696591) and turns squares by up to 44.73 degrees. Tilted beyond 1 degree: #845 49, T-174 45.
- **204** ([measure/identity-n204.json](measure/identity-n204.json)): against T-231, no symmetry one to one; the optimal assignment (symmetry 0) moves 67 squares beyond 0.1 and 109 beyond 0.01 (largest 0.912662) and turns squares by up to 43.12 degrees. Tilted beyond 1 degree: #845 79, T-231 61.
- **260** ([measure/identity-n260.json](measure/identity-n260.json)): against T-225, no symmetry one to one; the optimal assignment (symmetry 0) moves 155 squares beyond 0.1 and 250 beyond 0.01 (largest 1.00585) and turns squares by up to 27.31 degrees; against T-256, no symmetry one to one; the optimal assignment (symmetry 3) moves 199 squares beyond 0.1 and 233 beyond 0.01 (largest 1.09528) and turns squares by up to 42.64 degrees. Tilted beyond 1 degree: #845 104, T-225 60, T-256 100.
- **293** ([measure/identity-n293.json](measure/identity-n293.json)): against T-101, no symmetry one to one; the optimal assignment (symmetry 6) moves 185 squares beyond 0.1 and 219 beyond 0.01 (largest 1.04837) and turns squares by up to 43.6 degrees. Tilted beyond 1 degree: #845 104, T-101 60.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 12 jobs, 671,160 pair decisions, 90.2 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it (`receipts/sharp-controls-nNNN.json`, one per count (4 files)). It lowered the side by the least far-wall clearance,
closed the least-gap pair by its gap, and moved every square toward the nearer near wall
by its least clearance: both routes accepted each at contact with margin 0 and refused
each past it. It enlarged one square to its pair and one to its wall: both routes refused
each at contact for its shape alone and 1e-30 past it for the overlap or the wall as
well. Both refused a duplicated square.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read each certificate through the `evand-cert`
reader. The source’s checkers were not run.

## What Is Not Established

- **No review yet.** The stage 4 mathematical review, by a strong-tier lane sharing no
  context with this one, has not run; it and the adoption are think-nkt1’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

MIT, copyright (c) 2026 Evan Daniel. `CREDITS.md` says the repository’s work was
“Produced by Claude (Anthropic) in a single session under human direction”, and the
commit carries a Co-Authored-By trailer naming Claude. The packings are Daniel’s, after
the starts the issue credits: Chaoweeraprasit and Gupta’s s(199) at 172, Ostashev’s
s(176) at 204, Kirill Tymchishin’s Kaggle s(260) at 260 and 293. The bibliography key is
**[Daniel issue 845 2026-10-29]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-issue845-2026-10-29 --checkout CHECKOUT
python -m devtools.acquire_source evand-issue845-2026-10-29 --check
python -m devtools.upper_bound_reports evand-issue845-2026-10-29 check-claims --write
python -m devtools.upper_bound_reports evand-issue845-2026-10-29 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-issue845-2026-10-29 check --replay
python -m devtools.upper_bound_reports evand-issue845-2026-10-29 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:evand-issue845-2026-10-29' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/evand-issue845-2026-10-29/measure/identity-nNNN.json
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s172_1028_vs_prior.json.gz` | upstream | `f9f555f2db7e8e205a692592d84ae6dc85e74040` | `d1f503c69d5f975f5677815c4cac170774d1ca6fdb54558641a95e1bcbf4e9a1` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
