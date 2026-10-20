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
  the force-bearing subsystem and one free rattler at source index 11: `exactsolve.py`
  lines 1032–1033 build the variable set from only the 182 load-bearing squares and the
  side. The source also reports 86 wall and 897 square-square contact equations, 106
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
**think-1hmn**. Its original engineering estimate is 0.01–0.10 CPU-hours for the two
views and all planned routes, with a 360-second first-batch ceiling.
The primary batch below now has measured timings; regularized-view and source-checker
runs remain outside it.
The source report’s 12 seconds describes numerical production and does not price an
exact checker. No new environment or compiled tool is needed.

## Bounded Primary-Certificate Replay

The maintained `devtools.upper_bound_reports` importer ran one complete batch on the
original certificate, using the [primary-only declaration](acquisition/report.json).
Custody admission precedes parsing; `evand-cert` requires expected n = 183, exactly 183
pose rows and the declared exact rational side.
The declaration does not name the regularized view as `same_packing`.

Both repository geometry routes accepted the positive and rejected the duplicate-square
and outside-container controls.
Each route tested all 16,653 pairs in each of the three jobs: 99,918 pair decisions.
Both positives have wall clearance exactly `1/200000000000000000000 = 5e-21` and the
same strictly positive exact separating-axis projection gap, whose fraction is retained
in the native receipt and review.
That gap is not an exact shortest Euclidean distance.

The one-worker batch took 34.87 seconds wall time, within its 360-second ceiling; each
child had a 100-second deadline.
The receipt records 30.55 route CPU seconds, 31.27 summed job wall seconds and a longest
job of 10.79 seconds.
The subsequent `check --n 183` admitted all three jobs without deciding geometry again.

- [Complete native receipt](receipts/exact-certification.json.xz)
- [Batch declaration, commands, timings and outcomes](../../../campaign/issue-intake/intake-followup-20261019/n183-primary-replay.json)
- [Recovered certify invocation and historical environment-script output](receipts/certify-execution-provenance.json)

The two routes use `sqpack.witness.exact_verify` and
`devtools.check_rational_witness_independent`. Their geometry implementations differ;
they share the importer’s rational parser, half-angle conversion and Python runtime.
No upstream checker ran.
The original source generator was not rerun.

## Independent Mathematical Review, Registration and Adoption

The
[completed review](../../../../docs/project/reviews/review-2026-10-19-evand-n183-subgrid.md)
under **think-glg8** accepts the primary finite upper bound
`s(183) <= 13.999580178736252502081470897571 < 14` on the retained native replay.
Its reviewer is OpenAI Codex system family, strong tier, maximum reasoning.
The mapped file preserves the reviewer’s bytes and addendum, SHA-256
`6043c154990c386c28cb2fea0ae5e6e8743dce980efafbe4ff08c3efed5557da`. The reviewer ran
maintained receipt admission without `--replay` and reran no geometry.

The
[local evidence handoff](../../../campaign/issue-intake/intake-followup-20261019/n183-evidence-integration.yaml)
records M1–M4, program identities and source versions, exact scope and remaining
registration bindings.
M1 is corrected in the intake wording: the 27 numerical candidate modes concern the
182-square force-bearing subsystem, excluding free rattler index 11. M2 is discharged
for the primary replay by custody, strict parsing and admission of every complete
deciding input; the source parsers’ weaker behavior remains relevant if their separate
checkers run later. M3 and M4 retain the regularization, identity, priority and
missing-lineage limits.

The maintained implementations are independent of the producer’s programs in the sense
recorded by the conversion module’s read log; its author read both source checkers and
copied or imported none of their code.
The two routes share parsing, half-angle conversion, `Fraction`, runtime and the
separating-axis theorem.
This establishes neither a clean room nor distinct mathematical methods, humans or model
families.

The review proposed V3/C3 for the primary finite upper bound once the actual result
cited registered confirming evidence and the complete deciding and premise metadata.
The registration does so: [T-220](../../../frontier/RESULTS.md) cites the reported
evidence `E-evand-680-n183-report` and the confirming replay
`E-evand-680-n183-primary-exact-feasibility`, at V3/C3, with S3 endorsed by the review.
Regularized-certificate replay and source-checker execution remain separate optional
scope under **think-1hmn**; neither is needed to confirm this one original certificate.
Endpoint feasibility would not establish same-packing identity or a no-expansion path.

The same pull request adopted the original certificate as the case’s house on 19 October
2026 (**think-jh4w**): both upper lanes of [n-183.md](../../../frontier/n-183.md) moved
from the trivial 14 × 14 grid, which stays retained as history, and both strong
generators decided the new witness.

The custody premise is `V-acquire-source`. Its
[historical replay source](receipts/programs/acquire-source-replay-2026-10-19.py.txt) is
retained verbatim as text, SHA-256
`f2badc973c8aa3c1bc90e4ebf89836ba7c0fa74fa7527e7be7dc205d48d701e4`. The inherited #671
helper has different bytes and is recorded separately for current admission checks.
The archived text has not been executed.
The seven hashes in the evidence handoff retain the historical replay versions.
Five source files still match: `sqpack/witness.py`, `sqpack/verify.py`,
`check_rational_witness_independent.py`, `evand_arrangement_reports.py` and
`evand_exact_certificates.py`. The historical `upper_bound_reports.py` hash remains
`bc47273499dccbd59997bbdd4028176eb09621865b25854f511f9cf872ce1156`; today’s driver adds
the original n183 certificate to `HOUSES` for exact house selection and receipt
admission.
Current receipt admission uses that changed driver and custody helper; neither
changes the historical replay’s seven source hashes, batch or native receipt.

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
