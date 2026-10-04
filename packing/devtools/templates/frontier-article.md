<div class="site-hero">

# The Frontier Survey

</div>

<!-- The title stood over a subtitle, "A survey of everything known for cases n = 1,
     …, 324", until 2026-10-02 (the owner, think-wz9d). -->

<!-- What the survey records, how a bound comes to count, the audit of its sources, the
     recent counts and the seventeen-square history stood on the homepage, in The
     Frontier Survey, until 2026-10-02; they are this page's own prose now. The
     homepage's section went the same day (think-ec5k), and one of its page cards leads
     here. Every count is filled from the record (render_frontier_page.frontier_markdown).
     The survey's account comes first, and the key to the table's columns last, beside
     the table. -->

For each number $n$ of unit squares, $s(n)$ is the side of the smallest square that
holds them without overlap.
The frontier survey records the best-known packing and the strongest verified lower
bound for each of the {{COUNT}} cases the project tracks, with its provenance:
{{PROVED}} have a proved optimum and {{OPEN}} are open.
Every row is read from the case’s record, `packing/frontier/n-NNN.md`, when the page is
built; nothing on it is typed by hand.

**Audited sources.** The survey audits what it records.
The earliest published proof of $s(7) = 3$ carries four recorded defects in its printed
route, so the [record for seven squares](cases/7.html) rests the case on independent
later proofs. The [literature archive]({{ARCHIVE_URL}}) keeps each primary source, a
cleaned transcription and the unedited extraction it was checked against, and the
[evidence inventory]({{INVENTORY_URL}}) shows what each claim rests on and who did the
work.

**Recent results.** A star marks a recent verified lower bound, one proved since
{{RECENT_SINCE}}, when this project’s work began.
{{SURVEY_COUNTS}}
{{CORRECTIONS}}

**Seventeen squares.** Before this project’s work began, seven authors had published
lower bounds for seventeen squares, some also for eighteen, all independently:
Brandwijk’s $89/20$ (18 July), Burns’s $4.4811$ (6 August), MacIver’s $4.4502\ldots$ (8
August), Mira’s and Fort’s sixteen-point sets (10 and 11 August), anabologyco-maker’s
$4.57$ and $9141/2000$ (13 and 16 August), and Massaccesi’s $4.5058$ (21 August),
replayed here as [T-015](all-results.html#t-015) and [T-016](all-results.html#t-016).
The [seventeen-square record](cases/17.html) lists them all; each has since been
superseded.

**Reported and verified.** The *best known packing* and the *reported lower* bound are
what the published sources say, credited to whoever found or proved them.
The *verified* columns hold only exact formal bounds: a complete proof, an exact
algebraic replay, or a rigorous certificate.
An external certificate counts once it is replayed here in full and its mathematical
assumptions are discharged, and each record says who ran the checks and how independent
they were. Where the verified bound is the reported one, the cell says *✓ same*, meaning
verified here at the reported value.
A finite-precision result is numerically checked and never enters a verified column.

**The other columns.** *Recent* holds the star.
The *gap* is the verified upper bound minus the verified lower bound, exact where both
are closed forms and zero where the case is solved.
*Records* links each case file.
Values that are roots of a polynomial are shown as decimals, cut rather than rounded.

**A row’s details.** Open a row for its case record: the best packing known drawn large,
the number line of its bounds, then how its packing was built, the polynomial behind a
decimal, the sources, how its bounds were verified and the evidence entries behind them.
The same record opens from the overview’s atlas, and has an address of its own to share.

Click a column heading to sort; the filters narrow the rows.

{{TABLE}}
