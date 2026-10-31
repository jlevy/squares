# Francisco Couzo’s s(130) Certificate at 3a4d95c

This packet retains the certificate Francisco Couzo’s
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/712c6a6e9ef58a9521784e6b7e236af813422de7)
adds at `3a4d95c72083da3c3fd5acc4b1d0e94479c5422d` (committed 2026-10-27T19:42:09Z),
unchanged at the pin `712c6a6e9ef58a9521784e6b7e236af813422de7`, the head on 31 October
2026. Issue [#843](https://github.com/jlevy/squares/issues/843), opened 7 minutes 48
seconds after the commit, reports it.

## What the Source Claims

- certificates/n130.cert states s(130) <= 466915711841738962256077475351530705109199164124122993/39228601764570445403995003040207131754000000000000000 = 11.902430645984348558990...; issue #843 (opened 2026-10-27T19:49:57Z by franciscouzo) reports it rounded up at 12 places, 11.902430645985, 2.05e-3 below the register's 11.904483032516 (PingYou Ltd's PR #574 certificate), and prints its SHA-256 and that of n130.txt.
- The issue says both of the repository's exact checkers accept it in exact rational arithmetic: verify_bound_certificate.py (separating axes, projection test; valid and strictly valid, 1,624 candidate pairs) and exact_finish.py (exact corner replay); they are the repository's code and read the same format.
- The issue calls it a new packing found from PR #574's by thirteen successive improvements of the author's live searches of 24-25 October (ten by the web app's fq quench, two by its basin hopping, one by native SLP), matched one to one against PR #574's packing with the largest move 0.704, 11 squares beyond 0.1 and 26 beyond 0.01, 35 tilted squares against 32, and asks for credit to Francisco Couzo after the starting packing's credits (Nate Chaoweeraprasit (itsnaka); Siddharth Gupta; PingYou Ltd).
- The issue quotes Kaggle's staff per-puzzle leaderboard at 11.902430646006 for the team Cats and boxes (24 October 17:28 UTC), with no coordinates. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 8 files: 4 retained under [source/](source/) (35,517 bytes) and 4 pinned by digest.

| File | Bytes |
| --- | --- |
| `README.md` | 8,584 |
| `certificates/n130.cert` | 15,970 |
| `certificates/n130.json` | 5,314 |
| `n130.txt` | 5,649 |
| `BOUND_VERIFIER_LICENSE.txt` | 1,068, pinned by digest |
| `certificates/best/n130.cert` | 15,970, pinned by digest |
| `exact_finish.py` | 11,243, pinned by digest |
| `verify_bound_certificate.py` | 3,567, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **130:** exact side 11.9024306459843486…, below the case’s house (T-174) by 2.05e-03 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 130; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **130** ([measure/identity.json](measure/identity.json)): against T-174, no symmetry one to one; the optimal assignment (symmetry 7) moves 11 squares beyond 0.1 and 21 beyond 0.01 (largest 0.711415) and turns squares by up to 44.74 degrees. Tilted beyond 1 degree: #843 33, T-174 32.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 3 jobs, 50,310 pair decisions, 5.1 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every positive passed and every control was refused on both routes.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered the side by the least far-wall clearance,
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
  context with this one, has not run; it and the adoption are think-oy8d’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

The source states no licence for its data; the certificate is retained on the owner’s
presumption of permission from submission (think-cnn7; the licence follow-up is
think-m8f4) and as factual data. The packing is Francisco Couzo’s, found from PR #574’s
packing (Nate Chaoweeraprasit, improved by Siddharth Gupta and PingYou Ltd) by his
searches; the issue says Claude did the certification and the report at his direction.
The bibliography key is **[Couzo n130 2026-10-27]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue843-2026-10-28 --checkout CHECKOUT
python -m devtools.acquire_source couzo-issue843-2026-10-28 --check
python -m devtools.upper_bound_reports couzo-issue843-2026-10-28 check-claims --write
python -m devtools.upper_bound_reports couzo-issue843-2026-10-28 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports couzo-issue843-2026-10-28 check --replay
python -m devtools.upper_bound_reports couzo-issue843-2026-10-28 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:couzo-issue843-2026-10-28' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/couzo-issue843-2026-10-28/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
