# Pre-Geometry Parser Correction

The first frozen run stopped at `square orientation differs from declared class`, before
controls, wall checks or pair checks.
Its receipt and original code remain intact.
The wrong premise was the reviewer’s assumption that `m` indexes `classes`. A second
read of the original source showed all `m` values equal zero, with 137 squares having
`u=0`, 26 having `u=t`, and 16 having distinct rational `u` values.
No producer program or prior review was consulted to diagnose this mismatch.

The corrected replay treats each square’s own `u` as its half-angle parameter, as
already specified by the frozen mathematical model.
It groups equal `u` arrays only to reuse arithmetic.
It does not attach geometric meaning to `m` or `classes`. Each of the resulting 18
orientations must still prove its unit norms, perpendicularity and positive denominator
exactly. This removes an unsupported input-schema assumption, not a failed geometric
condition.

Every wall check, pair check, control, exact arithmetic method, acceptance condition and
the 300-second worker cap from `plan.md` is unchanged.
The corrected implementation is frozen before its first execution and before any
successful source-geometry outcome.
This second freeze is a disclosed amendment, not a replacement of the original freeze.

After run-01 the reviewer read only the standard Stage 4 procedure in
`packing/campaign/result-import.md` lines 841–1056. No prior review or verifier
implementation has been read.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
