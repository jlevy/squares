# Lane Claim Records Retained for the Ledger

`gather` reads each lane’s claim record by path: the packet’s
`packing/resources/web/<packet>/acquisition/<record>` where the checkout holds it, else
the copy here at `lane-claims/<lane>/<packet>/<record>`. It never reads a commit.

This ledger reads one record, PR #622’s `claims.json` in
`packing/resources/web/pingyou-pr622-certificate-2026-10-15/acquisition/`, which this
branch holds, so no copy is retained here.
PR #574’s N29 side is transcribed in `../sources.yaml` from the 14 October ledger’s
transcription of that pull request’s own claim record, since the PR #574 packet does not
declare 29.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
