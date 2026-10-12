<div class="site-hero">

# Every Result

</div>

## Verification Ladders<a id="verification-at-a-glance"></a>

Each result has an identifier, a claim, and three ratings, defined in
[`epistemics.md`]({{EPISTEMICS_URL}}): **S**, its significance; **V**, the strongest
verification its original evidence supports; and **C**, what this repository has
confirmed independently.
For results by others, this repository assigns `V` and `C` under its
[review policy]({{EPISTEMICS_URL}}#results-by-others).
Each ladder links to its rubric; each rung has a tooltip with its full meaning.

{{VERIFICATION}}

## Evidence and Exactness

The ladders grade a result.
Its evidence carries an assurance label: *reported*, a named source’s claim not checked
here; *numerically checked*, a finite-precision calculation with its precision, rounding
and tolerance recorded; or *verified*, an exact check, rigorous interval certificate or
complete proof covering the claim and its preconditions.
A verified packing proves an upper bound; optimality also needs a matching verified
lower bound.

Finite precision is not enough where squares touch exactly.
A tolerance that accepts a true zero-gap contact also accepts a small overlap, so a
contact-heavy packing requires exact algebraic signs or outward-rounded intervals
([why](synopsis.html#why-exactness-is-not-optional)). Schadt’s $n = 29$ packing passes
its 300-digit numerical check, while the verified interval witness proves a slightly
weaker side. Trump’s $n = 11$ packing is verified exactly over a degree-eight number
field, including fourteen zero-gap contacts.

These checks also audit published work: T-004 and T-008 check Bentz’s 2010 Theorem 8,
including both halves of $s(46) = 7$, and T-011 checks Trump’s 1979 packing for eleven
squares. The theorem remains the source’s; this repository adds an exact machine check.

## Results and Credits

A result’s kind is *lower bound*, *upper bound*, *optimality* (settling an exact value),
or a kind that bounds no case, such as *rigidity*, *case exclusion* or *simplification*
(a simpler proof of a value another result establishes).

Credits name the source’s authors; this project’s results are credited to Joshua Levy as
*Levy*. *X after Y* means X’s result rests directly on Y’s proof, method or tool.

## Status and Supersession

A result’s status is *recorded* (registered from its source without review or replay
here), *reviewed* (its argument read here), *confirmed* (its certificate replayed
successfully) or *incomplete* (a known defect remains open).
{{STATUS_COUNTS}}
Status follows the confirmation rung and is never set by hand; the
[status policy]({{EPISTEMICS_URL}}#status) defines it.
*In analysis* marks a review or replay under way here; *waiting on* marks a request with
the source or another party.

A bound is *superseded* when no current case bound rests on it and the bounds recorded
for its cases match or beat it.
A better bound not yet adopted by its case records remains unmarked.
For other kinds, *superseded* means the register records a later result implying the
whole claim; *superseded in part* means it implies only part, so the original remains
current. The table names the most recent replacement, with “and others” when needed; the
full record lists every replacement.

The [overview](./#recent-results) highlights recent major results.

# All Results

{{RESULTS_TABLE}}

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
