# Evan Daniel’s n183 Sub-grid Certificate

This packet retains the upper-bound report in
[issue #680](https://github.com/jlevy/squares/issues/680) at
`3a9948c781be668b1547cc2bf64a0d1e614f9bca`. It records source custody and triage.
No source checker, numerical solver or search ran during acquisition.

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Pin | `3a9948c781be668b1547cc2bf64a0d1e614f9bca` |
| First certificate commit | 2026-10-19T05:20:24Z, the UTC date used for this packet and the claim |
| Issue published | 2026-10-19T05:24:01Z |
| Author-local date | 18 October 2026; the source commit is dated at UTC−06:00 |
| Licence | MIT, copyright 2026 Evan Daniel; [LICENSE](source/LICENSE) retained |
| Custody | [Declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256) |

The source was fetched as one depth-one blobless commit into an existing external object
store. A separate sparse worktree reused those objects.
The packet retains 17 files, 326,398 logical bytes.
The general `search/packer/PACKER.md` history, 447,273 bytes, is pinned by digest only;
its H183 section at lines 4128–4175 was read.
The declaration names the retained scope.
Unrelated certificates, search runs, databases, site assets and numerical dependency
closures remain outside it.

## Claim Inventory

The reported finite upper bound is
`s(183) <= 13999580178736252502081470897571/1000000000000000000000000000000`, exactly
`13.999580178736252502081470897571`. The issue prints `13.999580178737`, rounded upward
at twelve decimal places.

| Certificate | Role | SHA-256 |
| --- | --- | --- |
| [s183_h183b.cert](source/search/packer/candidates/s183_h183b.cert) | Original rational certificate | `279e70d1c7fb0bc181e3e9d313e7350b672d85e223296f252b92f2916d6e5df5` |
| [s183_h183b_regularized.cert](source/search/packer/candidates/s183_h183b_regularized.cert) | Same-side display certificate | `67b2b26205f53915bb1a10a703a2700994a9ad16ea9ddd427bda232716f40d58` |

Both headers declare 183 squares and the same rational side.
Source metadata calls the second a conservative level-2 regularization, traversable
without expansion, reducing 19 angle groups to 18. Those identity and path
classifications have not been measured here.
The two files report one bound.

The source also asserts:

- Both retained exact checkers accept both certificates.
  They share an author and certificate format; their different geometry tests do not
  establish outside independent authorship.
- This is the first public packing of 183 squares below side 14, compared on 18 October
  with this project at `804eff36`, issues through #678, the Kingbird catalogue and the
  monotone envelope. The acquisition establishes no priority claim.
- The 80-digit numerical point has side `13.999580178736252501941…`, smaller than the
  rational certificate side.
  The source calls it a local minimum strict modulo 27 flat motions.
  More precisely, these are numerical KKT diagnostics with 27 candidate flat modes in
  the force-bearing subsystem and one free rattler: `exactsolve.py` lines 1032–1033
  build the variable set from only the 182 load-bearing squares and the side.
  The source also reports 86 wall and 897 square-square contact equations, 106
  corner-corner contacts, no corner-corner MILP descent, and 73 tilted squares, 72
  load-bearing. These are numerical diagnostics, without interval proofs or a
  local-optimality theorem for the full 183-square configuration.
- The prior comparison calls it a distinct minimum from the grid.
  No exact local or global optimality theorem, rigidity claim or measured arrangement
  identity follows from the retained numerical report.

The H183 log describes an earlier `13.9998051157950716…` hit and several intervening
sub-grid minima. Issue #680 submits only the final bound above; the intermediate values
remain source search history.
The five preceding commits at this head report numerical rational-angle, symmetry,
alternate/core and strip-slack experiments with no new record.
Their scope is inventoried in the
[intake continuation](../../../campaign/issue-intake/intake-followup-20261019/README.md).

## Credit and Lineage

Credit Evan Daniel, after Francisco Couzo’s n182 packing, as the issue requests.
The author describes a non-record n182 descendant at `13.990326`, after 17 explorer
moves from Couzo’s witness; one-square insertion; a tilt-angle swap and two two-parent
crossovers; then symmetric-kick refinement in twelve 40-minute explorer runs.
The source did not log a crossover mate.
It states that the six starting packings all descend from public n182 packings.
The retained prior-grid comparison is a comparison target, not that donor’s exact
custody record. Replaying the final geometry would not resolve the missing lineage.

[CREDITS.md](source/CREDITS.md) discloses Claude under human direction and states no
peer review. The source commit names Claude Opus 5.5 as co-author.
The retained `h183.py`, `explore.py` and `exactsolve.py` describe numerical production;
their dependency closures and unlogged run state are not reproduced by this packet.

## Validation Price and Owners

The standalone `search/exact/verify_cert.py` uses exact rational separating axes;
`verify_cert2.py` uses polygon containment and closed-edge intersection.
Both import only `sys` and `fractions` and skip pairs only where exact squared centre
distance exceeds 2. Their source text was read, without executing it.

Full replay and sensitive duplicate-square and outside-wall controls are owned by
**think-1hmn**. The engineering estimate is 0.01–0.10 CPU-hours for the two views and
all planned routes, with a 360-second first-batch ceiling; it is not a measured checker
timing. The source report’s 12 seconds describes numerical production and does not price
an exact checker. No new environment or compiled tool is needed.

Independent mathematical review is **think-glg8**, separate from replay.
It reviews the finite feasibility implication and both certificate views, preserves the
numerical and lineage limits above, and runs only its own retained code.
Result ID allocation, reviewed Stage 4 integration, house adoption and the project’s
strong regularization runs remain subsequent steps.
A source display certificate alone does not discharge the house-regularization
obligation.

To check custody from `packing/`, with the project interpreter and external scratch:

```bash
python -m devtools.acquire_source evand-n183-subgrid-2026-10-19 --check
```

This command binds retained bytes and metadata.
It decides no geometry or optimality.

## Compressed Files

Files over 1,000 lines are retained as deterministic gzip.
Their decompressed bytes match the upstream blob and digest below.

| Stored path | Origin | Git blob of decompressed bytes | SHA-256 of decompressed bytes |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s183_h183b_vs_prior.json.gz` | upstream | `97c7fb9efc0d927227072aa5125579149b287ea7` | `d78bb0d35ca51b486311bd4b11d8b9528e9eb42aa5552a3a24b5c5cc2e828216` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
