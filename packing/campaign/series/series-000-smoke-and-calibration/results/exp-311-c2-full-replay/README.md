# Unsampled C2 replay: incomplete monitor stop

All 161 published objects were acquired and checked against their declared sizes and
hashes in 78.944 seconds.
The subsequent unsampled standing verifier stopped after 480.468 seconds because the RSS
monitor could not complete its one-second process query.
The owned group was terminated and cleanup completed.
The last progress observation was 18,000 checked nodes; no FULL receipt was produced.

The [compact summary](mechanical-summary.json) retains the exact failure, source and
cleanup scope. All nine imported source observations match immutable recovery commit
`e72c7f3c6d59b25a002c54d6f04c8fb34e4d2aee`. The [result directory](.) retains the
original phase journal, launch, logs and acquisition receipts.
The journal still says running because its runner was interrupted; it was not rewritten
to fabricate closure.

No ordinary exclusion was admitted and no census or bound changed.
This unchanged replay was not retried.
See the [experiment](../../experiments/exp-311-h-319-c2-full-replay.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
