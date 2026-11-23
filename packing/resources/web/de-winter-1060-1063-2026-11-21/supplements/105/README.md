# Sharp controls for the 105-square rational enclosure

Both maintained exact routes returned the expected verdict and margin for all
eleven sharp controls on the [original 105-square enclosure](candidate.json.gz).
The run used explicit GMP rational arithmetic for the verifier routes. Exact
Fraction arithmetic still plans each perturbation.

The worker completed in 48.93 seconds under the memory guard, with 95.9 MiB
peak RSS measured inside the worker. It wrote each completed row to external
scratch before moving to the next control. The worker and guard exited zero.
An earlier combined Fraction run reached its 300-second ceiling before a
complete roster was available.

[Complete standard receipt](sharp-controls.json),
[source binding and stage timings](sharp-control-execution.json)

This controls the original 105-square input supplied on
[issue 1063](https://github.com/jlevy/squares/issues/1063).
The separate independent feasibility check passed all 5,460 pairs and ten
declared controls. Registration and drawing selection remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
