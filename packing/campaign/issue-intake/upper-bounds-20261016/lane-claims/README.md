# Lane Claim Records Retained for the Ledger

`gather` reads each lane’s claim record by path: the packet’s
`packing/resources/web/<packet>/acquisition/<record>` where the checkout holds it, else
the copy here at `lane-claims/<lane>/<packet>/<record>`. It never reads a commit.

This ledger reads one record, PR #574’s `claims.json` in
`packing/resources/web/pingyou-pr574-certificates-2026-10-13/acquisition/`, which `main`
holds, so no copy is retained here.
Issue #639’s sides are transcribed in `../sources.yaml` from `../exact-sides.json`,
which `../review/exact_sides.py` computes from the evand-exact-cur-2026-10-16 packet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
