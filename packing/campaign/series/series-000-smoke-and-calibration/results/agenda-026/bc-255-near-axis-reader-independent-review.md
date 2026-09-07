# BC-255 Near-Axis Reader Independent Review

**Verdict: GO for instrument readiness at the frozen H-106 scope.** The independent
rectangle reader has no remaining mathematical or control blocker.
This authorizes the coordinator to freeze the proposed experiment; it supplies no H-106
result. No actual target geometry, original-source geometry, LP, or producer target
invocation ran during this review.
H-036 remains unresolved.

The review covers the retained
[reader](../../../../../devtools/check_angle_near_axis_control.py) and
[tests](../../../../../tests/test_check_angle_near_axis_control.py), including the
coordinator’s completion frozen at 02:29:22 UTC on 2026-09-07. The reviewer did not
author or edit either file.
The baseline checkout was `codex/post-381-four-hour-research` at
`b379bfc60922124e65263018b1f2e0aa5a705fb0`; these files were uncommitted additions.
This delegated review inherits Session 090’s pipeline-improvement phase and
`think-3xaz`. It began at 02:23:47 UTC with a ten-minute cap ending at 02:33:47 UTC. The
mathematical and control decision was complete at 02:30:46 UTC, after 419 seconds.
Final documentation verification completed at 02:32:54 UTC, after 547 seconds.

## Mathematical Assessment

Let $D=1+t^2$, $C=1-t^2$, $S=2t$, and let $\sigma$ be the sign of the closed half-angle
slab.
On the admitted range $|t|<1$, the support radius is $r=(C+\sigma S)/(2D)$. The map

$$
F_t(z)=\bigl(qz_x+(1-2z_x)r,\ qz_y+(1-2z_y)r\bigr)
$$

maps the full closed parameter square onto the centers of every contained closed unit
square at angle $2\arctan(t)$. The width is strictly positive for the frozen $q>2$:
$2r=\cos\theta+|\sin\theta|\leq2<q$. The reader’s generic nonnegative-width check
therefore causes no weakening of the fixed-target premise.
A zero-width toy box would also remain covered by the affine map.

For a point $p$, define $A_x=2D(p_x-qz_x)-(1-2z_x)(C+\sigma S)$ and similarly $A_y$. The
two rotated coordinate numerators are $U=CA_x+SA_y$ and $V=-SA_x+CA_y$. The reader
constructs the four quartics $D^2-U$, $D^2+U$, $D^2-V$, and $D^2+V$. Each equals $2D^2$
times its signed point-membership margin.
The clearing factor is strictly positive.
This agrees with a direct rotation calculation in the source-free toy controls.

For fixed $t$, each margin is affine in $z$. Its four rectangle corners suffice for the
whole closed rectangle.
All 18 rectangles are reconstructed from the complete six-by-three grid, so their union
includes every edge, vertex, and seam.
Both closed slabs are checked, including $-T$, $0$, and $T$. This yields 36
slab-rectangles, 144 corners, and 576 signed quartics.
The producer’s 864 triangle-vertex obligations are admission metadata; the reader does
not reuse their algebra or truth values.

The power-to-Bernstein transform correctly substitutes $t=a+(b-a)z$ and then uses
$z^j=\sum_{i=j}^n {\binom{i}{j}}/{\binom{n}{j}}\,B_i^n(z)$. Nonnegative coefficients
certify a whole closed interval, including zero contacts.
Depth-12 exact bisection preserves the shared child endpoint.
A negative endpoint or depth exhaustion returns only an uncertified obligation.
This sufficient test cannot turn incomplete evidence into a disproof or a positive
result.

The four seed formulas and the independent horizontal/vertical reflections agree with
the definition in
[H-106](../../../../hypotheses/H-106-continuous-near-axis-ten-point-cover.md).
They are reconstructed in numeric lexicographic order, deduplicated, and checked to give
ten contained points.
This was a source-code comparison; the actual point set was not constructed.
The rational endpoint binding matches the [design](bc-255-angle-instrument-design.md):
$T=110880/50803079$. The elementary outward angle comparison remains an external
mathematical premise; this reader binds the exact rational endpoint and does not prove a
statement about pi.

## Controls and Findings

The initial five retained toy tests passed.
The initial scoped Ruff check reported seven findings, and BasedPyright reported three
unused imports. The retained suite had not yet exercised the new file/CLI adapter.
The coordinator completed only formatting, the diagnostic wording, and source-free tests
before the final freeze.

- **R1, Medium, resolved:** the initial lint and type findings in
  `packing/devtools/check_angle_near_axis_control.py` and
  `packing/tests/test_check_angle_near_axis_control.py`. Fix: apply the configured
  formatter, remove unused imports, and narrow the exception assertion.
  Independent final Ruff, format, and BasedPyright checks pass.
- **R2, High, resolved:** missing controls for the new reader’s file admission, exit
  status, incomplete-producer, and timeout adapter.
  Fix: exercise those paths with target construction forbidden or replaced by a rational
  toy. Independent final replay passes all 16 tests with zero skips.

The final controls verify shifted-interval quartic identities, both rotation signs,
closed contacts, a displacement of $2^{-200}$ that must fail, an interior negative
polynomial, strict packet mutations, and complete 576-inequality toy replay.
They also verify duplicate JSON keys, floats, NaN, malformed UTF-8/JSON, oversized
bytes, symlinks, missing files, missing dispatch, forbidden cap overrides, unresolved
completed prefixes, and reordered, duplicate, or unchecked failure coordinates.
Timeout injection verifies the unresolved exit, alarm arming and cancellation, and
restoration of the previous signal handler.
It does not measure a real ten-second alarm expiry.

Three additional existing source-free controls passed for the shared bounded JSON loader
and its tighter byte cap.
They support the reused loader, while the final new controls exercise this reader’s own
adapter. Every geometry execution used toy inputs; the test fixture forbids an unmocked
`target_input` call.

## Commands and Costs

Commands ran from `packing/` with the existing Python 3.14.7 environment.
The first `uv run --frozen --all-extras --group dev pytest` launch failed during cache
initialization before collecting tests.
The direct project interpreter then ran the controls.
This was an environment recovery, with no scientific invocation repeated.

| Reviewer command | Result | Outer wall seconds | CPU seconds |
| --- | --- | ---: | ---: |
| `.venv/bin/python3 -m pytest -q tests/test_check_angle_near_axis_control.py`, initial retained files | 5 passed in 0.22 seconds | 0.55 | 0.45 |
| `.venv/bin/ruff check` on the two retained files, initial | 7 findings | 0.10 | 0.03 |
| `.venv/bin/basedpyright` on the two retained files, initial | 3 findings | 1.03 | 1.66 |
| Three selected shared-loader tests in `tests/test_check_angle_grid_source_control.py` | 3 passed in 0.06 seconds | 0.36 | 0.27 |
| `.venv/bin/python3 -m pytest -q tests/test_check_angle_near_axis_control.py`, final freeze | 16 passed in 0.34 seconds | 0.58 | 0.55 |
| `.venv/bin/ruff check` on the two final files | Pass | 0.01 | 0.00 |
| `.venv/bin/basedpyright` on the two final files | 0 errors, 0 warnings | 0.92 | 1.70 |

The separate final Ruff format check reports both files already formatted.
These are single verification timings, not performance comparisons.
CPU is the sum of the `/usr/bin/time -p` user and system values.
No full repository gate or CI result is claimed by this delegated review; those remain
with the coordinator.
The documentation pass used the pinned Flowmark 0.4.0 with `--no-cache` after its default
cache path was denied; the completed pass and the scoped whitespace check exited zero.

## API and Independence Limits

The file entry point requires an absolute packet path and `--target-control`. It admits
exactly nine keys, binds canonical fixed-side and slab strings before rational parsing,
requires the frozen labels and complete producer inventory for positive admission, and
then independently checks the geometry.
The maximum file size is 262144 bytes.
The receipt is stdout, costs are stderr, and exit codes are 0 for proved, 1 for
unresolved, and 2 for refused.
Neither a positive packet nor a positive receipt overrides a nonzero actual process
exit.

The reader has its own point construction, rectangle enumeration, quartic construction,
and Bernstein arithmetic.
It shares Python’s `Fraction` and the bounded JSON loader.
That loader’s module imports project field and geometry definitions transitively; the
reviewed path does not invoke their source builders or use their geometry/sign routines.
This is implementation independence for the proof calculation, not a different language,
runtime, or formally verified kernel.
No materially better small replacement was found; the separate rectangle derivation
provides a useful check of the triangle producer.

The internal ten-second alarm covers admission and geometry.
Imports, argument parsing, and final stream publication lie outside it, so the
experiment dispatcher must retain the independently declared external process cap and
both actual exit statuses.
Direct Python calls to the toy helpers have no wall or rational-bit cap and are not the
bounded wire interface.
The prospective experiment, its source freeze, and any H-106 acceptance remain separate
coordinator work.
A failed sufficient assignment or an escape confined to the added outer
angle sliver cannot reject H-106.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
