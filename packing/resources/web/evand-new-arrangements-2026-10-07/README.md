# Evan Daniel’s Three New Arrangements: Reported Intake

[Issue #399](https://github.com/jlevy/squares/issues/399) reports arrangements for n =
266, 270 and 272 from [evand/square-packing](https://github.com/evand/square-packing) at
`7eef24f7221b8c3371d6171dd664b52541bbd479`, committed on 7 October 2026. The three exact
rational certificates, two source checkers, format explanation, licences and attribution
are retained unchanged under `source/`. The acquisition record and manifest bind this
selected scope to that source tree.
Certificate aliases elsewhere in the upstream repository are not duplicated.

## Scope and Remaining Work

The source claims exact feasibility and new arrangements.
The certificate’s full side fraction, rather than an issue’s rounded decimal, determines
any improvement. At this checkpoint, no deciding checker has run and no case bound or
pose has been adopted from these files.
The import must parse exactly the declared roster, convert its half-angle parameters
without rounding, check every wall and pair by both project geometry routes, and reject
complete-roster duplicate and outside controls before confirming feasibility.

Arrangement novelty, numerical stationarity, Hessian and local-minimum statements remain
source reports. Feasibility alone proves no local or global optimum.
The earlier issue #375 packet, its T-098/T-101 results and their historical poses retain
their original source meanings.
This packet must be adopted separately; changing an old source side without changing its
geometry would be invalid.
The n = 17 work remains with its existing owner.

## Credit and Licence

Evan Daniel authored the source.
The original MIT licences and `s12/CREDITS.md` are retained, including the source’s
credits for the packing records and tools it builds on.
This packet makes no independent novelty attribution beyond the report.

## Check Retained Bytes

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-new-arrangements-2026-10-07 --check
```

This checks source custody; it does not decide packing feasibility.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
