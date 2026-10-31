# Evan Daniel’s Updated s(299) Certificate at 0e76d9f

This packet retains the certificate set Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d/search/packer/candidates)
adds at `0e76d9fe5e48fc2a614e3c132a0a3fd67e0a6a8d` (committed 2026-10-29T04:44:41Z), the
head on 31 October 2026. His update comment on issue #824
([issuecomment-6488202753](https://github.com/jlevy/squares/issues/824#issuecomment-6488202753)),
posted 2 minutes 8 seconds after the commit, reports it, 2.46e-3 below the opening
post’s certificate (T-248, the [evand-n299-2026-10-26](../evand-n299-2026-10-26/README.md)
packet).

## What the Source Claims

- search/packer/candidates/s299_1028.cert states s(299) <= 17801238549388584084680137655023/10^30 = 17.801238549388584084680137655023; Evan Daniel's update comment on issue #824 (issuecomment-6488202753, 2026-10-29T04:46:49Z) reports it rounded up at 12 places, 17.801238549389, 2.46e-3 below the opening post's 17.803695435333 (T-248), and prints its SHA-256.
- The comment calls it an exact KKT certificate whose 80-digit point s299_1028.exact.txt is a local minimum of S strict modulo 119 exact flat motions, with no corner-corner MILP descent, 64 corner-corner contacts and 33 rattlers, by numerical evidence at 80 digits and not interval proofs; and a new packing found from the opening post's packing by four generations of refill and an exact descent, with the credit request of the opening post unchanged (Chris Deotte for the method and the start).
- The comment says verify_cert.py and verify_cert2.py both report VALID, and quotes Kaggle's per-puzzle leaderboard at 17.793636991 for Cats and boxes, below this, with no coordinates. Those statements are the author's; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 10 files: 8 retained under [source/](source/) (165,585 bytes) and 2 pinned by digest.

| File | Bytes |
| --- | --- |
| `CREDITS.md` | 7,501 |
| `LICENSE` | 1,068 |
| `search/packer/candidates/s299_1028.cert` | 50,626 |
| `search/packer/candidates/s299_1028.exact.txt` | 60,137 |
| `search/packer/candidates/s299_1028.input.txt` | 16,573 |
| `search/packer/candidates/s299_1028.json` | 5,995 |
| `search/packer/candidates/s299_1028.predescent.txt` | 15,325 |
| `search/packer/candidates/s299_1028_prior.json` | 8,360 |
| `search/exact/verify_cert.py` | 3,401, pinned by digest |
| `search/exact/verify_cert2.py` | 3,101, pinned by digest |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record. The packet
is well under a megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `3978a7f61` on 31 October
2026):

- **299:** exact side 17.8012385493885841…, below the case’s house (T-101) by 2.16e-02; below T-248 (#824) by 2.46e-03 (requested).

## Report Order

The [ledger of 31 October for this pass](../../../campaign/issue-intake/upper-bounds-843-846-20261031/README.md) walks every report at these
counts in the order it reached this repository, from starts frozen at `main` `3978a7f61`,
and records this packet’s claims at 299; its README
gives each count’s verdicts and what holds the others.

## Pose by Pose

`devtools.measure_identity` measured each recorded certificate against the packing the
ledger compares it with, and wrote the receipts under [measure/](measure/). A
measurement for credit; it decides nothing.

- **299** ([measure/identity.json](measure/identity.json)): against T-248, no symmetry one to one; the optimal assignment (symmetry 0) moves 78 squares beyond 0.1 and 166 beyond 0.01 (largest 0.801914) and turns squares by up to 36.64 degrees; against T-101, no symmetry one to one; the optimal assignment (symmetry 6) moves 134 squares beyond 0.1 and 246 beyond 0.01 (largest 1.13312) and turns squares by up to 30.75 degrees. Tilted beyond 1 degree: update 87, T-248 83, T-101 38.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in its
own child process: 3 jobs, 267,306 pair decisions, 37.2 route CPU seconds
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
  context with this one, has not run; it and the adoption are think-8hjz’s.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
- **The lineage** the source states, beyond what the measurements above show.

## Credit and Licence

MIT, copyright (c) 2026 Evan Daniel; Claude assistance disclosed, as for the opening
post. The packing is Daniel’s, found from his T-248 packing by refill and an exact
descent, with the opening post’s credit to Chris Deotte for the method and the start.
The bibliography key is **[Daniel n299 update 2026-10-29]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-n299-update-2026-10-29 --checkout CHECKOUT
python -m devtools.acquire_source evand-n299-update-2026-10-29 --check
python -m devtools.upper_bound_reports evand-n299-update-2026-10-29 check-claims --write
python -m devtools.upper_bound_reports evand-n299-update-2026-10-29 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-n299-update-2026-10-29 check --replay
python -m devtools.upper_bound_reports evand-n299-update-2026-10-29 sharp-controls
python -m devtools.measure_identity --n N 'VIEW=packet:evand-n299-update-2026-10-29' 'HOUSE=packet:HOUSE_PACKET' \
  --out resources/web/evand-n299-update-2026-10-29/measure/identity-nNNN.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
