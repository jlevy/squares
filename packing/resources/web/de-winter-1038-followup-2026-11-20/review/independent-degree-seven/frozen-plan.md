# Independent Full-Corpus Degree-Seven Review

This successor covers all 228 squares, all 3,648 corner-wall inequalities and all 25,878
unordered pairs of distinct source square IDs.
Pair enumeration uses all two-element combinations of the sorted original squares, whose
IDs are checked for uniqueness during input parsing.
It evaluates all four axes for every pair, giving 103,512 source pair-axis decisions.
The original eleven controls accompany this complete positive coverage.

The predecessor sample at checker SHA-256
1548cbb144dc2dc6149e81a3530ace4515e3b81bd0286c4be2ff14e831f59268 completed its declared
32-square, 512-wall, 256-pair sample and eleven controls.
Its checker elapsed time was 0.389 seconds and supervised worker time 1.062 seconds.
The pair loop took 0.312 seconds, with a slowest individual pair of 0.0597 seconds.
Pressure was 1 at the single guard observation.

The original arithmetic, geometric predicates and controls are preserved.
Static comparison confirms exact AST equality for all 32 definitions outside the
coverage driver and main mode/reporting code.
The changed coverage driver selects the complete corpus and enumerates every pair,
checks the expected wall and pair totals, and reports completion only after the full
source pass and original controls return.
Scope, mode and success fields identify a full-corpus verdict.
The limits remain identical to the sample.
The saved diff and delta audit identify every code change.

The independent predicates use quotient arithmetic over seven rational coefficients,
reduction modulo the source polynomial, a fresh modulo-3 Rabin irreducibility check, an
exact rational Sturm root count, and rational interval sign refinement.
Zero remainders decide exact equality.
Unit membership and corner-wall checks use exact field arithmetic.
The four-axis projected-center/support-radius predicate decides interior disjointness of
every pair, with touching accepted.
This successor reuses the already frozen independent predicates.

The author’s prior exposure includes the independent rational review and code, earlier
T-334 attribution metadata, the source README’s claimed method and acceptance, source
field metadata and several constant coordinate rows, an encoding census of the complete
JSON, and maintained algebraic outcome/field-certificate metadata.
The author also read the successful independently implemented sample’s receipt.
The choice of modulo-3 irreducibility was visible in prior metadata and is independently
recomputed.

The entire original geometry was parsed by the authorized predecessor sample after that
predecessor’s freeze.
Preparation of this successor did not reopen original source geometry.
The successor’s complete run will open the original mathematical member after this
freeze. No producer or maintained geometry implementation was read or reused in this
assignment.

The pair-loop mean gives a linear projection of 31.56 seconds for all pairs.
Multiplying the slowest observed pair by the full pair count gives 1,545.62 seconds,
about 25.8 minutes. These are two projections from the sample.
That sample contains pairs between a constant square and an algebraic square, with
minimum best gap exactly 1 and no root refinements.
Algebraic/algebraic pairs, touching configurations and refinement tails remain unpriced.
The fixed 165-second internal ceiling permits a bounded full attempt and can return an
incomplete verdict.

Peak RSS was not measured by the sample.
Its single guard observation recorded rounded tree cost 0.0 GiB, which supplies no
useful process-wide peak estimate.
The larger pair lists, timing values and serialized pair IDs add approximately 3–6 MiB
by object-count analysis, with additional sign-cache growth determined at runtime.
The unchanged sampled-tree stop is 0.30 GiB.

The coordinator must supervise one worker with the memory guard, require pressure 1 to
start, and stop at pressure 2, 0.30 GiB observed tree cost, unavailable telemetry or 180
seconds outer wall. The program’s internal limit is 165 seconds, at most 256 root
refinements per sign and 1,024 in total, and at most 100,000 cached signs.
Run with Python 3.14.7 and -I -B, with external TMPDIR, UV_CACHE_DIR and a task-specific
CARGO_TARGET_DIR.

A successful run requires all source unit, wall and pair checks plus all eleven controls
to finish. Only then may the result report candidate_accepted=true and
full_geometry_completed=true.
A refusal, unresolved sign, resource stop or code failure yields no accepted full-corpus
verdict.
Registration and the project’s assurance decisions depend on the actual complete
result and its independent review.

This successor has passed a syntax parse and static preservation audit.
It has not been imported, tested or executed on mathematical data.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
