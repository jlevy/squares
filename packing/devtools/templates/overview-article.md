<div class="site-hero">

{{HERO}}

</div>

<!-- The explainer has a section of this name, and an old explainer link to it must
     still reach the explainer (forward.js), so this heading keeps the overview's own id. -->

<h1 id="the-problem" class="site-title">The Square Packing Problem</h1>

<!-- The section's first two paragraphs are README's, read from its project-intro block
     (site_documents.overview_intro), so the problem is introduced in one text. Edit them
     in README.md. Only the site's own statement is written here, under its own
     heading, The Squares Project. -->

{{README_INTRO}}

## The Squares Project

Work on the square packing problem has exploded in the summer of 2026 thanks to
AI-powered research efforts.
This Squares Project was begun by [Joshua Levy](https://x.com/ojoshe) in August 2026
with some initial explorations that obtained
[new lower bounds](papers/n11-lower-bounds-explainer.html) for $n = 11, 17, 18, 19, 20$
and other low values.
Now several others have obtained results building on this work, including Kleddamag’s
[certified lower bound of 31/8](papers/n11-threshold-bound-review.html) and a
[landmark new proof](papers/n11-optimality-review.html) by Ahmed of the optimality of
the famous [case of 11 squares](cases/11.html).
Separately, Evan Daniel has proved the optimality of
[a whole infinite family](all-results.html#t-064), $s(k^2 - 3) = k$ for every $k \ge 6$,
along with exact values at [21](cases/21.html), [32](cases/32.html) and
[45](cases/45.html) squares.
This project now independently tabulates all known new results and does
[AI-assisted verification](all-results.html#verification-ladders) of the proofs and
certificates behind them, to encourage open collaboration on open questions and
formalizations of current proofs.

If you have new results or know of newer results, please
[file an issue]({{NEW_ISSUE_URL}}) to report them, and we will gladly incorporate them
and cite your work. We also have a group chat.
Contact [ojoshe](https://x.com/ojoshe) if you wish to join.

<!-- The two paragraphs above are the owner's words of 2026-10-03 (think-a7oa), each
     fact checked against the record: the project's first packing work is of
     2026-08-22; its own lower bounds are at
     n = 11, 12 and 17 to 21 (T-001 to T-034); the explainer the link names is n = 11's,
     and it lists the bounds at 12, 17 and 19 that its method gave; and the optimality
     of n = 11 is T-060, Ahmed's. On 2026-10-05 (think-92ar) the owner
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

{{PAGE_CARDS}}

<!-- This section's fragment was #the-atlas until 2026-10-01. The empty anchor in its
     heading keeps an old link landing here. -->

## The Atlas of Square Packings<a id="the-atlas"></a>

<!-- The atlas stood after Recent Results until 2026-10-04, when the owner moved it
     above the table. -->

Below are the best-known packings for each value of $n$ up to $324$. Each packing links
to the full details on the case and what is proven and currently known for that value of
$n$.

{{ATLAS_GRID}}

## Recent Results

<!-- The table first, with its legend under it, then its one action, then the headline
     of recent progress (the owner, 2026-10-02, think-tgjv; 2026-10-03, think-42dx). The
     paragraph's result ids are held to the register by check_results.READER_TIER, and
     it says where the filters start. The legend under the table (rung_legend) shows every
     mark a row carries and links the ladders; what each rung means, the ratings' kinds,
     statuses and dating rule are the Results page's, and this page no longer explains
     them (the owner, 2026-10-03). README carries its own fuller account of the same
     progress (site_documents, think-ekw5). -->

{{RECENT}}

<p class="site-action-row site-more"><a class="site-action" href="all-results.html">See all results{{ARROW_RIGHT}}</a></p>

Eleven squares is settled: $s(11) = 3.8770835\ldots$, the exact side of Trump’s 1979
packing, by [T-060](all-results.html#t-060). Seventeen squares is bracketed by
machine-checked bounds, [T-093](all-results.html#t-093) below and
[T-065](all-results.html#t-065) above, and [$n = 21$](cases/21.html),
[$32$](cases/32.html) and [$45$](cases/45.html) have new exact values.
The recent table includes results of significance S3 and up from the last 180 days,
excluding superseded results.
The [complete table](all-results.html) includes older results and offers all filters.

<!-- Verification Ladders stood here, between Recent Results and the atlas, until
     2026-10-02 (the owner, think-hqb3): the section is the Results page's, under its
     table, and the legend under Recent Results' table links it (think-42dx). Its two fragments,
     #verification-ladders and the older #verification-at-a-glance, are sent there by
     forward.js (overview/forward.js). -->

<!-- The Frontier Survey stood between the atlas and PDFs and Videos until
     2026-10-02 (the owner, think-ec5k): its account is the Frontier page's own prose,
     and its card to that page is one of the page cards under The Squares Project. Its
     two fragments, #the-frontier-survey and the older #the-survey, are sent to the
     Frontier page by forward.js (overview/forward.js). -->

<!-- The atlas as files and as a film: the two posters, each opening its PDF, and the
     film. The cards and their note stood under the grid, in The Atlas, until 2026-10-01,
     and The Frontier Survey stood between this section and the atlas from that day until
     2026-10-02. Recent Results stands between them since 2026-10-04, when the atlas
     moved above it. -->

## PDFs and Videos

{{ATLAS_CARDS}}

<p class="site-wide site-atlas-note">A shorter film shows the <a href="https://github.com/jlevy/squares/releases/download/v0.4.2/ascent-n1-100-1080p60-citations.mp4">ascent from 1 to 100</a> (2 m 20 s). Both films are on the <a href="https://github.com/jlevy/squares/releases/tag/v0.4.2">v0.4.2 release</a>, with a receipt recording each file and the page it was drawn from. Each poster is also an SVG (<a href="repo:packing/atlas/known-best/known-best-1-100.svg">1 to 100</a>, <a href="repo:packing/atlas/known-best/known-best-1-324.svg">1 to 324</a>), and the <a href="repo:packing/atlas/known-best/README.md">atlas README</a> describes them all.</p>

## Other Square Packing Projects

The first three cards are the catalogues of the record packings: David Ellsworth’s
Squares in Squares, which continues Erich Friedman’s original page, and Evan Daniel’s
Square Packing Atlas, which draws every record packing beside the proven floor beneath
it and keeps a page of
[open problems](https://evand.github.io/square-packing/problems.html) about the patterns
that span many $n$. After them come the projects and posts, on GitHub and elsewhere,
that the research frontier cites results from, ordered by the significance of those
results in the [register](all-results.html): most at S5 first, then S4, and so on down,
newest first among equals.
A card with registered results ends with a count that opens them.

{{OTHER_PROJECTS}}

## Squares Project Documentation

The code, the certificates, the literature archive and the documents that record all of
this live in the Squares Project’s [repository](https://github.com/jlevy/squares).

{{DOCUMENT_CARDS}}
