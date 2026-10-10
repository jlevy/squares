<h1 id="the-squares-project" class="site-title">The Squares Project</h1>

Work on the square packing problem has exploded in the summer of 2026 thanks to
AI-powered research efforts.
This Squares Project was begun by [Joshua Levy](https://x.com/ojoshe) in August 2026
with some initial explorations that obtained
[new lower bounds](papers/n11-lower-bounds-explainer.html) for $n = 11, 17, 18, 19, 20$
and other low values.

Now several others have obtained results building on this work, including Kleddamag’s
[certified lower bound of 31/8](papers/n11-threshold-bound-review.html) and a
[landmark new proof](papers/n11-optimality-review.html) by Queuingtheorydotcom of the
optimality of the famous [case of 11 squares](cases/11.html).

Separately, Evan Daniel has proved the optimality of
[a whole infinite family](all-results.html#t-064), $s(k^2 - 3) = k$ for every $k \ge 6$,
along with exact values at [21](cases/21.html), [32](cases/32.html) and
[45](cases/45.html) squares.

This project now independently tabulates all known new results and does
[AI-assisted verification](all-results.html#verification-ladders) of the proofs and
certificates behind them, to encourage open collaboration on open questions and
formalizations of current proofs.

<h1 id="contribute-your-results" class="site-title">Contribute Your Results!</h1>

If you have new results or know of newer results, please
[file an issue]({{NEW_ISSUE_URL}}) to report them, and we will gladly incorporate them
and cite your work.

We also have a group chat.
Contact [ojoshe](https://x.com/ojoshe) if you wish to join.

<!-- The introductory and contribution text above is the owner's words of 2026-10-03 (think-a7oa), each
     fact checked against the record: the project's first packing work is of
     2026-08-22; its own lower bounds are at
     n = 11, 12 and 17 to 21 (T-001 to T-034); the explainer the link names is n = 11's,
     and it lists the bounds at 12, 17 and 19 that its method gave; and the optimality
     of n = 11 is T-060, Queuingtheorydotcom's. On 2026-10-05 (think-92ar) the owner
     asked for the three n = 11 papers to be linked here: Kleddamag's T-037, also
     building on this project, joins the sentence with Part II, and "landmark new proof"
     links Part III. The sentence after it names the
     top-line results by others (the owner, 2026-10-03, think-nlyc), each checked the
     same way: s(k^2 - 3) = k for every k >= 6 is T-064, and s(21) = 5, s(32) = 6 and
     s(45) = 7 are T-052, T-051 and T-053, all four credited to Daniel after Burns,
     Massaccesi and all at V3/C3, T-064 by the full replay of the source's Valid7
     checker and the Lean reduction built here. The bibliography files their sources as
     independent of this project, so they stand in a sentence of their own and not
     among the results building on this work, and the sentence gives no significance
     score, since only n = 11's results are S5 and these are S4. "AI-assisted
     verification" links the ladders, which say how far each result is checked; the
     sentence does not say every result is checked, since some are recorded and not
     yet replayed here. -->

<h1 id="squares-project-documentation" class="site-title">Squares Project Documentation</h1>

{{DOCUMENTATION_BLOCK}}

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
