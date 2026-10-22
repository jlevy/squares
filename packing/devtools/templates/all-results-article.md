<div class="site-hero">

<h1 id="every-result">Results</h1>

</div>

The result register lists individual contributions: bounds, proofs, constructions, and
methods. For the best-known bounds by number of squares, use the Atlas and its case
records.

<p class="site-action-row site-more"><a class="site-action" href="atlas.html">Atlas{{ARROW_RIGHT}}</a><a class="site-action" href="atlas.html#best-known-results">Best Known Bounds{{ARROW_RIGHT}}</a></p>

<nav aria-label="On this page"><a href="#all-results">Browse Results</a> · <a href="#recent-arrivals">Recent Arrivals</a> · <a href="#earlier-results-by-week-published">Earlier Publications</a> · <a href="#verification-ladders">Verification and Ratings</a> · <a href="#evidence-and-exactness">Evidence</a> · <a href="#results-and-credits">Credits</a> · <a href="#status-and-supersession">Status</a></nav>

<h2 id="all-results">Browse Results</h2>

{{RESULTS_TABLE}}

<a id="recent-arrivals"></a>

## Added in the Last {{ADDED_DAYS_TITLE}} Days

Every result that reached this site over {{ADDED_SPAN}} (its newest day and the
{{ADDED_DAYS}} before it), at any significance, by the day it arrived, newest first.
Each id leads to its row in the register table; S4 and S5 are marked, and a muted entry
says it has since been superseded.
[Browse these arrivals]({{ADDED_LINK}}) in the table, or open each day’s link for that
day; [what arrived in the last day]({{ADDED_LAST_DAY}}) counts whole days on the same
calendar as these dates.

{{RECENT_ADDED}}

<h2 id="earlier-results-by-week-published">Earlier Publications</h2>

Results at {{ROLLUP_FLOOR}} and above from the {{ROLLUP_WEEKS}} before {{ADDED_FIRST}},
by the week each was published (or established, for this project’s own), with who found
them. A result added above that was published earlier is listed here too.
A muted, underlined id has since been superseded.

{{RECENT_ROLLUP}}

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

<h2 id="results-and-credits">Result Types and Credits</h2>

A result’s kind is *lower bound*, *upper bound*, *optimality* (settling an exact value),
or a kind that bounds no case, such as *rigidity*, *case exclusion*, *simplification* (a
simpler proof of a value another result establishes) or *formalization* (a proof in a
proof assistant of a value another result establishes).

<div class="site-profile-prose">

Credits name the source’s authors; this project’s results are credited to Joshua Levy as
*Levy*. *X after Y* means X’s result rests directly on Y’s proof, method or tool.

</div>

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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
