# Matched Exact Replay Diagnostic

[Exp290](../../experiments/exp-290-h299-matched-exact-replay.md) preserves its
initial12.202s process-sampling failure and a separately preregistered unchanged-regime
retry under attempt2. The retry completed221.938s supervised/cleanupcomplete; both fresh
NONE/PHASES runs returned COMPLETE fullPASS_STALL with identical exactmathematical
result and seed/node/cells byte identities.
All16boundaryobservations and custodyrechecks pass.

NONE replay109.465s and PHASES111.545s are diagnostic timings under overlapping host
activity, with no optimizationgain claimed.
Row checks consume97.113s; the remaining14.433s is unattributed.
The facetcache has zeroevictions, so raising that cap has no measuredmotivation.
Slowest observed stepowners are20,21,11,8. Stage attribution is a proposed next
diagnostic, not an implicit CALLGRAPH run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
