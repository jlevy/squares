<div class="site-hero">

# Every Result

</div>

<!-- The title stood over a subtitle, "A survey of all reviewed results", until
     2026-10-02 (the owner, think-wz9d). -->

Each result has an identifier, a claim, and three ratings, **S**, **V** and **C**, the
rungs of the [Verification Ladders](#verification-ladders) under the table.
Every credit names people: a result by others is credited to its authors as their source
states it, and this project’s results to Joshua Levy, as *Levy*. *X after Y* means that
X’s result rests directly on Y’s proof, method or tool, so the credit also says which
results build on this project’s.

<!-- The kinds, the statuses and the dating rule are defined here and nowhere else on
     the site: the homepage's Recent Results names them and links this page
     (2026-10-02). When a bound by others counts as verified is the Frontier page's,
     under Reported and verified. -->

Under its rungs each result shows its kind, which says what it is: a *lower bound*, an
*upper bound*, an *optimality* result, which settles an exact value, or one of the kinds
that bound no case, such as a *rigidity*, a *case exclusion* or a *simplification*, a
second and simpler proof of a value another result holds.

Its status, in a column of its own, is how far the work on it here has gone: *recorded*,
registered from its source with nothing here yet read or replayed; *reviewed*, its
argument read here; *confirmed*, a replay of its certificate passed; or *incomplete*, a
defect found in it still open.
{{STATUS_COUNTS}}
The status follows the confirmation rung and is never set by hand;
[`epistemics.md`]({{EPISTEMICS_URL}}#status) defines it.
Beside it, *in analysis* marks a replay or review under way here and *waiting on* a
request that is with the source or another party.
A bound that no case bound rests on now is marked *superseded*, followed by the bounds
its cases rest on instead.
A result of another kind is marked *superseded* when the register records that a later
result implies all of it, and *superseded*, *in part*, when a later result implies only
some of it; either way the mark names the later result, and a result superseded in part
stays current.

{{STAR_LEGEND}}
Open a row for the full claim and its novelty label, and follow its details, a link to a
line, to the case file, the evidence, the retained source and the review.
The newest, and the ones that matter most, are on the [overview](./#recent-results).

The table starts with every result showing, newest first.
A result by others is dated by its publication, and this project’s by the day it was
established. The filters narrow it by rating, kind, status, source, case and age, and
they combine.

{{RESULTS_TABLE}}

<!-- The ladders were the homepage's Verification Ladders section until 2026-10-02 (the
     owner, think-hqb3). They stand under the table so a reader meets the table first;
     the opening paragraph points here, and the homepage's Recent Results says what the
     chips indicate and links here. The heading keeps the empty anchor of the section's
     older fragment, #verification-at-a-glance, and forward.js sends both fragments here
     from the homepage. The lead defines the three ratings once, for the page; the
     paragraphs after the diagram say what it does not show, the assurance labels on
     evidence and where finite precision falls short. -->

## Verification Ladders<a id="verification-at-a-glance"></a>

The three ratings on every row are rungs of three ladders, defined in
[`epistemics.md`]({{EPISTEMICS_URL}}): **S**, how significant the result is; **V**, how
it was originally verified, the strongest verification its own evidence supports; and
**C**, how it has been confirmed, what this repository has checked itself.
The `V` and `C` of a result by others are this repository’s own verification of it,
under the policy [`epistemics.md`]({{EPISTEMICS_URL}}#results-by-others) states.
Each ladder’s name links its section of the rubric, and a chip’s title is the rubric’s
full meaning of the rung.

{{VERIFICATION}}

The ladders grade a result; the evidence under it carries one of three assurance labels:
*reported*, a named source’s claim not checked here; *numerically checked*, a
finite-precision calculation with its precision, rounding and tolerance recorded; and
*verified*, an exact check, rigorous interval certificate or complete proof covering the
claim and its preconditions.
A verified packing proves an upper bound only; calling it optimal needs a matching
verified lower bound.

Finite precision is not enough where squares touch exactly.
A tolerance that accepts a true zero-gap contact also accepts a small overlap, so a
contact-heavy packing is verified only with exact algebraic signs or outward-rounded
intervals ([why](synopsis.html#why-exactness-is-not-optional)). Schadt’s $n = 29$
packing passes its 300-digit numerical check, while the interval witness that is
verified proves a slightly weaker side; Trump’s $n = 11$ packing is verified exactly
over a degree-eight number field, fourteen zero-gap contacts included.

The same checks audit published work, where the theorem stays the source’s and this
repository adds an exact machine check: T-004 and T-008 check Bentz’s 2010 Theorem 8,
both halves of $s(46) = 7$ included, and T-011 checks Trump’s 1979 packing for eleven
squares.
