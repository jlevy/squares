# Francisco Couzo’s Certificates at 232, 260 and 307 at 712c6a6

This packet retains the three certificates Francisco Couzo’s
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/712c6a6e9ef58a9521784e6b7e236af813422de7)
adds at `712c6a6e9ef58a9521784e6b7e236af813422de7` (committed 2026-10-28T15:57:20Z), the
head on 31 October 2026. Issue [#844](https://github.com/jlevy/squares/issues/844),
opened 5 hours 51 minutes after the commit, reports them.

## What the Source Claims

- certificates/best/n232.cert states s(232) <= 7617348902520572307222120733/483283363059000000000000000 = 15.7616617594813299...; issue #844 (opened 2026-10-28T21:48:31Z by franciscouzo) reports it as 15.761661759482, 2.51e-3 below the register's 15.764174317487 (Daniil Ostashev, #528).
- certificates/n260.cert states s(260) <= 104381051573626493618357957479/6274019722347000000000000000 = 16.6370295588709730...; the issue reports 16.637029558871, 8.72e-3 below the register's 16.645753250520.
- certificates/n307.cert states s(307) <= 2707897969116659515550794271467451840032974544063449693/150612387934832692306604131393579915999000000000000000 = 17.9792512836880252...; the issue reports 17.979251283689, 1.61e-3 below the register's 17.980862784055 (#593).
- The issue says none of the three packings is the author's construction: each starts from a packing another author published on Kaggle (232: Alex Chilton's notebook 'Fault-line DP + Basin Hopping - LB 22.2990', run 362691257, side 15.763381419802; 260 and 307: ntumlnoob's notebook 'First 22.268681355 Public Code With Explanation', version 3, run 362957087, sides 16.638533455862 and 17.979253973651), refined on his computers on 27-28 October by GPU basin hopping with the energy kernel of Vladislav Lavrentev's (lightningv08) Kaggle notebook 'CUDA Packing Search' (Apache-2.0), native basin hopping, an Evan Daniel fq polish, an Ellsworth-style structural move modelled on David Ellsworth's tools, the author's SLP and the web app's fq (an adaptation of Evan Daniel's fq, MIT); it calls 307 a refinement and leaves 232 and 260 to the record.
- The issue says both of the repository's exact checkers accept all three certificates (strictly valid, positive wall and pair margins), and quotes Kaggle's per-puzzle leaderboard sides below all three with no coordinates. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 12 files: 6 retained under [source/](source/) (165,857 bytes) and 6 pinned by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 8,584 |
| `certificates/best/n232.cert` | 29,164 |
| `certificates/n260.cert` | 33,474 |
| `certificates/n260.json` | 27,295 |
| `certificates/n307.cert` | 38,580 |
| `certificates/n307.json` | 28,760 |
| `BOUND_VERIFIER_LICENSE.txt` | 1,068, pinned by digest |
| `certificates/best/n260.cert` | 33,474, pinned by digest |
| `certificates/best/n307.cert` | 38,580, pinned by digest |
| `n260.txt` | 12,655, pinned by digest |
| `n307.txt` | 13,841, pinned by digest |
| `verify_bound_certificate.py` | 3,567, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **232:** exact side 15.7616617594813300…, below the case’s house (T-186) by 2.51e-03 (requested).
- **260:** exact side 16.6370295588709730…, below the case’s house (T-225) by 8.72e-03; below T-254, Couzo of 28 October (no issue) by 1.50e-03 (requested).
- **307:** exact side 17.9792512836880252…, below the case’s house (T-174) by 1.61e-03; below T-254, Couzo of 28 October (no issue) by 4.56e-12 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 232, 260 and 307; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **232** ([measure/identity-n232.json](measure/identity-n232.json)): against T-186, no symmetry one to one; the optimal assignment (symmetry 7) moves 91 squares beyond 0.1 and 123 beyond 0.01 (largest 1.08859) and turns squares by up to 45 degrees. Tilted beyond 1 degree: #844 81, T-186 61.
- **260** ([measure/identity-n260.json](measure/identity-n260.json)): against T-225, no symmetry one to one; the optimal assignment (symmetry 5) moves 192 squares beyond 0.1 and 210 beyond 0.01 (largest 1.08752) and turns squares by up to 27.09 degrees; against T-254, no symmetry one to one; the optimal assignment (symmetry 3) moves 172 squares beyond 0.1 and 216 beyond 0.01 (largest 1.07764) and turns squares by up to 44.42 degrees. Tilted beyond 1 degree: #844 100, T-225 60, T-254 104.
- **307** ([measure/identity-n307.json](measure/identity-n307.json)): against T-174, no symmetry one to one; the optimal assignment (symmetry 2) moves 91 squares beyond 0.1 and 138 beyond 0.01 (largest 1.1367) and turns squares by up to 34.04 degrees; against T-254, one to one by nearest centres (symmetry 4), 35 squares beyond 1e-3 and 40 beyond 1e-9, the largest move 1.667110e-2 and turn 0.5525 degrees. Tilted beyond 1 degree: #844 107, T-174 103, T-254 107.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 9 jobs, 644,622 pair decisions, 71.7 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it ([receipts/sharp-controls-n232.json](receipts/sharp-controls-n232.json), [receipts/sharp-controls-n260.json](receipts/sharp-controls-n260.json), [receipts/sharp-controls-n307.json](receipts/sharp-controls-n307.json)). It lowered the side by the least far-wall clearance,
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
  context with this one, has not run; it and the adoption are think-dwzb’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

Retained on the presumption of permission from submission (think-cnn7; think-m8f4) and
as factual data. The starting packings are Alex Chilton’s (232) and ntumlnoob’s (260,
307) Kaggle notebook packings; Couzo is credited with the refinements, by code the issue
names (lightningv08’s CUDA Packing Search, Evan Daniel’s fq, David Ellsworth’s tools).
The bibliography key is **[Couzo issue 844 2026-10-28]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue844-2026-10-28 --checkout CHECKOUT
python -m devtools.acquire_source couzo-issue844-2026-10-28 --check
python -m devtools.upper_bound_reports couzo-issue844-2026-10-28 check-claims --write
python -m devtools.upper_bound_reports couzo-issue844-2026-10-28 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports couzo-issue844-2026-10-28 check --replay
python -m devtools.upper_bound_reports couzo-issue844-2026-10-28 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:couzo-issue844-2026-10-28' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/couzo-issue844-2026-10-28/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
