# Frozen independent review plan — later issue 1038 attachment

The scientific inputs are the source README claim and only the original mathematical members n228_rational.json and n228_algebraic.json. The Witness/v2 schema supplies the interface. No contributor implementation, checks directory, benchmarks, old n228-witness.json, previous reviewer receipt or verdict will be used.

Exposure: I previously saw the earlier T-334 adoption metadata and attribution comments while integrating n232. The allowed source README itself states that other checkers accepted these new witnesses and describes its verification method. Those assertions are not evidence for this review. This is an independent implementation review with that exposure disclosed, not a claim of complete blindness to the source's assertions. The checker below is frozen before either new witness's geometry is opened.

For the rational witness, parse scalar strings through Fraction, then convert their integer numerator and denominator to exact GMP rationals. Validate 228 distinct square IDs, unit edge lengths, orthogonality and consistent square orientation. Convert the documented origin to lower-left coordinates. Require every corner to lie in the closed box. For every unordered pair, project all corners onto the two edge directions of each square and require at least one nonnegative interval separation. Retain exact minimum wall and maximal-axis pair gaps, equality counts and complete pair count.

Controls frozen in advance: duplicate the first square into the second slot; translate the first square by minus twice the container side; accept an exact two-square shared edge and exact unit-container equality; refuse a 1/100 inward pair shift and a 1/100 outward wall shift. Gross mutations use the same complete decision entry point and can stop at the first decisive violation. They are not represented as complete native project jobs.

One isolated worker, Python 3.14.7, -I -B, external temporary/cache directories, dedicated observe-only memory guard. Stop the owned group at 180 seconds, pressure2 or 0.30 GiB observed tree cost. No dependency installation, repository imports, checkout edits, network interaction or solver.

The degree-seven witness is a separate pricing phase. First inspect only its mathematical representation, coefficient sizes and field declaration. Plan exact quotient-ring arithmetic and certified sign decisions at the declared real root, including unit membership; time only a bounded sample before recommending any complete geometry run. Do not treat sample acceptance or decimal comparison as full algebraic feasibility.

Preserve original-byte/source-archive concordance, immutable plan/checker, controls, success or cap outcome, guard journal and an explicit scope statement. Authenticate neither historical priority nor a local/global minimum.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
