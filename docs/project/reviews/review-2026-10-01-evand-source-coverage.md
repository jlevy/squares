# Evan Daniel’s October Proof Pages: Source Coverage and Intake

**Reviewed:** 2026-10-01. **Workflow:** W1 external-source research and citation audit,
tracked by `think-a0fj`. **Source revision:**
[`evand/square-packing` at `08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5),
committed 2026-10-01 04:17:47 UTC. GitHub’s compare API reports this commit 54 commits
ahead of the
[2026-09-28 local intake](../../../packing/resources/web/evand-square-packing-2026-09-28/README.md)
at `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3`, with no commits behind it.
The earlier
[2026-09-26 intake](../../../packing/resources/web/evand-square-packing-2026-09-26/README.md)
is at `167d842cd27ba1451cb2833773ea930c80b9e65b`. The selected new source bytes and a
Git-blob manifest are retained in the
[October packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md).

The October 1 pin dates this intake snapshot, not first publication of either claim.
The
[first `s60` bundle commit](https://github.com/evand/square-packing/commit/cdd9b2a4fde0dfed7a3dcff455fab7cfa66230c2)
is timestamped 2026-09-29 01:13:36 UTC, September 28 in Pacific time.
Its README already states the $s(61) = 8$ monotonicity corollary.
The pinned
[`k2m3` README](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3/README.md)
also dates the $s(60) = 8$ result to September 28. The
[first public family write-up](https://github.com/evand/square-packing/commit/d9f79bc1beb52a38854b675c330fd25a6d37eeee)
and
[first full `k2m3` bundle](https://github.com/evand/square-packing/commit/69999aff04bfecef4181ce5c7dbebe9914df0b92)
both entered the source on 2026-09-30 14:47:52 UTC. These dates supply
`attribution.published` for T-062 through T-064; the later snapshot supplies
`source_date` for the October coverage entry.

Evan Daniel’s live
[Proofs and Results](https://evand.github.io/square-packing/proofs.html) and
[Sources](https://evand.github.io/square-packing/sources.html) pages announce two
substantial additions to this record: $s(60) = 8$ from a mixed cover, and
$s(k^2 - 3) = k$ for every $k \ge 6$ from a periodic segment and area measure.
The first has two source checkers; the second rests on one exact checker for the
$7 \times 7$ cover and a Lean theorem conditional on that cover.
The packet is partial: its covers, checker sources and the `k2m3` leaf record are
present, while the `s60` root logs and complete upstream build are not.
None of the new claims has been replayed here.
The live pages are mutable; the commit links below pin what was inspected.
Nothing in this review upgrades a reported claim to local verification.

## Claim and Citation Matrix

The comparison baseline below is `origin/main` at the start of this task, not the
working branch, whose in-progress result-rung changes must not be treated as settled.
On that main baseline
[T-049, T-051, T-052 and T-053](../../../packing/frontier/RESULTS.md) each stand at
`V3/C3`; [T-060](../../../packing/frontier/n-011.md) stands at `V3/C3/S5` pending mapped
human review. The [source coverage map](../../../packing/frontier/source-coverage.yaml)
has entries for the September 26 and 28 packets, but none for the new bundles.

| Claim on the live pages | Pinned primary source and its stated check | State here; intake need |
| --- | --- | --- |
| $s(11) \ge \frac{3040}{797}$, and $s(12) \ge \frac{35}{9}$, $\frac{3920}{997}$, $\frac{15680}{3951}$ | [Twelve and Eleven Squares](https://evand.github.io/square-packing/s12/) and the [source `s12/` directory](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12). The site reports unconditional Lean covering checks for all four, though the largest $s(12)$ theorem takes about seven CPU-hours and generated data. | The strongest $s(12)$ bound is already `T-049`, `V3/C3` on main; the weaker claims move no case. The source’s reported Lean upgrade has not been built here. See [n = 12](../../../packing/frontier/n-012.md). |
| $s(11)$ equals Trump’s side | [Ahmed’s source](https://github.com/Queuingtheorydotcom/11SquaresOptimal) is named on Proofs and the [n = 12 page](https://evand.github.io/square-packing/s12/), but lacks its own entry in Sources §5. | The result is already `T-060`, `V3/C3/S5` on main, with a mapped review pending; [n = 11](../../../packing/frontier/n-011.md) is solved. This is a citation gap on Daniel’s site, not a missing local intake. |
| Case-free $s(13) = 4$ | [Rung-two bundle](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/rung2); two exact source checkers and a source-reported unconditional Lean check. | The value was already proved by Bentz and is verified here from him. The case-free alternative is a report (`E-n013-evand-casefree-cover-report`), not a separately replayed local theorem; [n = 13](../../../packing/frontier/n-013.md). |
| $s(21) = 5$, $s(32) = 6$, $s(45) = 7$ | [Mixed `s(21)`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s21), [point `s(32)`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s32), and [mixed `s(45)`](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s45). The site distinguishes unconditional Lean for $s(32)$, a conditional top theorem for $s(21)$, and no Lean for $s(45)$. | These exact values are already local `T-052`, `T-051`, and `T-053`. The September [review](review-2026-09-28-evand-s21-s45-mixed-covers.md) states which source checker runs were replayed. New source changes include a guard and repeated `zm_mixed` records for $s(21)$ and $s(45)$; a later intake can assess whether they affect the older evidence, without re-opening the values automatically. |
| $s(60) = 8$; hence $s(61) = 8$ | [New `s60` bundle](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/s60): 23,744 weighted points and 5,216 grid-line segments; mass $\frac{748233441}{12500000} = 59.85867528$. Its README reports `zm_mixed.py` on all 102,400 D4 roots and `zmx2` on 6,400 D4 and 51,200 full-space roots, all accepted. The two checkers have different implementations; neither is formally verified. There is no $s(60)$ Lean data or top theorem. The $s(61)$ statement follows by monotonicity. | [n = 60](../../../packing/frontier/n-060.md) and [n = 61](../../../packing/frontier/n-061.md) still say open on main. The covers and source code are in the new partial packet, but no replay is recorded. Record $s(60)$ as reported and $s(61)$ as its derived reported consequence. The old reported floors $\frac{397}{50}$ and $\frac{199}{25}$ remain prior evidence. |
| $s(k^2 - 3) = k$ for all integers $k \ge 6$ | [New `k2m3` bundle](https://github.com/evand/square-packing/tree/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3): a 1/5-grid, periodic wall measure plus Lebesgue interior, with total $k^2 - 4D$, $D = \frac{423621306389}{500000000000}$, so $4D = 3.388970451112 > 3$. `Valid7` uses 800 segments and one area square; source run V3 records 9,800 accepted roots, 32,079 leaves, zero uncertified. The source’s exact Python checker is one implementation, though six AI-agent reviews and mutation controls are reported. [Lean `Bentz.lean`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/lean/Sqpack/Bentz.lean) proves `Valid7 → ∀ k ≥ 6, minSide (k² − 3) = k`; Lean does **not** establish `Valid7`. | The family is absent from the local source map and results register. Known individual cases $k = 6, 7$ remain proved through Bentz and $k = 8$ would also follow from the separate $s(60)$ result. [n = 78](../../../packing/frontier/n-078.md), [n = 97](../../../packing/frontier/n-097.md), and larger instances still say open. Intake needs a family-scoped result and per-case consequences, with a local checker/reduction review before promotion. |

The `k2m3` checker’s
[README](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/certificates/k2m3/README.md)
states that its short `verify.sh` checks hashes, data and every recorded leaf’s
coverage, then regenerates the Lean data; `--full` repeats about 81,000 CPU-seconds of
exact checking. Re-reading a source-generated record is useful for completeness and
corruption checks, but it does not supply a second implementation of the mass bounds.
For $s(60)$, the source says its short `verify.sh` includes a fresh `zmx2` full-space
run, while the long tier also repeats the `zm_mixed.py` sweep (about 19.6 CPU-hours).
Those are source statements; this review ran neither tier.

## Citation and Provenance Corrections

1. [Sources §5](https://evand.github.io/square-packing/sources.html) lists Daniel’s new
   $s(60) = 8$ certificate but has no $k^2 - 3$ entry, despite the result’s prominence
   on [Proofs](https://evand.github.io/square-packing/proofs.html) and its own
   [write-up](https://evand.github.io/square-packing/k2m3/). Its $s(60)$ line also says
   the $k^2 - 3$ family was proved only through $k = 7$, which describes the state
   before the new family.
   Add a dated, pinned citation for the `k2m3` bundle and separate the single-checker
   `Valid7` claim from the conditional Lean reduction.
   [Proofs](https://evand.github.io/square-packing/proofs.html) lists two Lean-checked
   $s(12)$ bounds but omits the strongest $15680/3951$ bound, which the
   [n = 12 write-up](https://evand.github.io/square-packing/s12/) and pinned
   [`LADDER.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/lean/LADDER.md)
   say is fully kernel checked.
   This is a page-summary omission; no Lean build was run here.
2. The [n = 12 write-up](https://evand.github.io/square-packing/s12/) §06 says an exact
   fractional packing at side $3.99$ has normalized mass $12.0282$. That is the newer
   value $48112643084/3999999987 \approx 12.028160810092$ in
   [`CLIQUE_CONTINUUM.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/CLIQUE_CONTINUUM.md)
   §3; the older
   [`DUAL_EXACT.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/DUAL_EXACT.md)
   value is $12.00823078252$. The newer note cites `runs/cqx_PURE99_support.txt`, absent
   from the pinned public tree; the older note’s `runs/dual_exact_3.99_support.txt` is
   also absent. The number on the site is consistent with the newer note, but neither
   exact side-3.99 witness can be replayed from the public support files.
   The distinct
   [side-4 obstruction](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/COVER4.md)
   is stated as $24537607710/1999999999 \approx 12.2688038611$ and its
   [`cover4_exact_support.txt`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/cover4_exact_support.txt)
   is public. The headline $12.27$ on Proofs is consistent with that source.
3. [Proofs](https://evand.github.io/square-packing/proofs.html) credits Ahmed for
   $s(11)$ and [Sources §5](https://evand.github.io/square-packing/sources.html)
   promises to list the 2026 computer-checked work, yet omits that source as an item.
   The local [bibliography](../../../packing/resources/bibliography.yaml) and
   [n = 11](../../../packing/frontier/n-011.md) record already pin and distinguish its
   independent proof from Daniel’s weaker $s(11)$ certificate.
4. Sources §5 gives Guzhou0806’s R067 $s(17) > 4.66018$ as the last named rung.
   This record already holds the later
   [R068 `4.66044`](../../../packing/frontier/n-017.md).
   The page warns that its dated values can lag rapidly changing repositories, so this
   is a refresh item, not an attribution dispute.
   Its list of wand125’s bounds likewise predates that author’s separate
   [point-only `s(61) = 8` source](https://github.com/wand125/square-packing-bounds/tree/f8846cec9661773dbd0cc7cbeee7d01ddb12a2b8/point_n61_L8),
   whose
   [secondary evand replay manifest](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/s61_wand125/MANIFEST.txt)
   is now in this pinned tree.
   That is an independent route to $s(61)$, not part of Daniel’s $s(60)$ certificate.

The first four sections of Sources are mainly catalogue provenance and older papers.
The page says its drawings and finder attributions derive from Ellsworth’s SVGs and
wording rather than an independent discovery audit; this is an appropriate limit for the
[retained Ellsworth source](../../../packing/resources/web/kingbird-squares-in-squares.md).
Its separate account of Nagamochi’s lemma defect, Bentz’s corrected point sets, and the
2020 asymptotic exponent correction is contextual bibliography.
This pass checked their presence and links, not their mathematical proofs.
No new local result depends on the page’s finder-count table or on those asymptotic
claims.

## Research Leads and Disposition

**Verify the new finite premise first.** A source-distinct implementation or a focused
mathematical audit of `Valid7` would address the family’s single-checker risk.
The specific obligations are the exact zero-tilt limit enumeration, the positive-tilt
Lemma E and area lower bounds, the D4 and pose-space coverage argument, and the mapping
between the box file and the Lean data.
A short hash and record pass can be run first; the 81,377 CPU-second source run belongs
to a selected research gate.
The separate $s(60)$ bundle offers a smaller intake with two implementations and a
full-space run; its $s(61)$ consequence can be recorded without implying that it
independently checks the general family.

**Test the next deficit with its own threshold.** The pinned
[`FRIEDMAN.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/FRIEDMAN.md)
proves an insertion lemma for periodic cover bands and identifies an $F_4$ target:
$s(k^2 - 4) = k$ for all $k \ge 5$, since the individual $k = 5, 6, 7, 8$ instances now
have source certificates.
Its proposed $w = R = 3$ family is still a float LP, with estimated saving
$D \approx 1.154$ per corner before exactness costs; no $F_4$ proof or certificate
exists. The same note’s proposed $F_5$ route needs more than a band extrapolation:
$s(20)$ and $s(31)$ are open threshold cases, and this record’s
[n = 20](../../../packing/frontier/n-020.md) verified floor is $97/20$. Its
translation-descent experiment fails on the $n = 89$ record, so the proposed insertion
method proves values for a chosen deficit, not Friedman’s general implication.
The note expressly corrects an earlier Roth–Vaughan inference: the published waste bound
does not establish that $c^{\ast}(k) \to \infty$.

**Keep the $s(12)$ obstruction precise.** The side-4 public dual support is useful
evidence that a single weighted point cover cannot prove $s(12) = 4$ in the closed
model. It says nothing against a branch or multi-square argument.
The pinned
[`n12-gap.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/notes/n12-gap.md)
separates exact dual witnesses from measured LP leaf values; preserve that split if
these ideas enter
[X-048](https://github.com/jlevy/squares/blob/d7b77066424ab0d94b57f700659425e18ecb7080/packing/campaign/explorations/X-048-n17-optimality-after-n11.md)
or the n12 and n20 hypothesis registry.

## Proposed Survey Units and Next Evidence

The current [results schema](../../../packing/frontier/results.schema.yaml) accepts
finite `n_values` or a finite `n_min`–`n_max` interval, not a family with unbounded
parameter $k$. A finite list of family instances must not silently stand for
$\forall k \ge 6$. The following units are proposed for the source-intake survey; their
identifiers and final rubric scores belong to the registry editor.
A source-read entry begins at `V0/C1` only if it has a qualifying, dated external
review; otherwise it begins at `V0/C0`. Source-reported checker passes and AI reviews do
not by themselves make a local `V4/C3` replay.
The `S` assessments apply the [epistemics rubric](../../../epistemics.md) and are
judgments, not gate predicates.

| Result unit | Existing ID or addition | Suggested significance and required evidence |
| --- | --- | --- |
| $s(60) = 8$ from Daniel’s mixed cover | New reported result. This is a new exact-value claim for still-open [n = 60](../../../packing/frontier/n-060.md), not an update to `T-053`. | `S3` for a substantive case and a larger, two-checker mixed cover; consider `S4` only if a reusable advance beyond the earlier $s(21)$/`s(45)` method is established. Cite the pinned `s60` bundle and credit; retain source checker descriptions separately from any actual replay. For a higher rung, acquire omitted root logs and run at least the fast full-space `zmx2` tier with an exact result receipt. |
| $s(61) = 8$ inferred from Daniel’s $s(60) = 8$ | New derived result, distinct from the $s(60)$ certificate. Its lower half uses monotonicity; its upper half is the $8 \times 8$ grid with three squares omitted. | `S1` as a routine consequence of the substantive $s(60)$ result. A `composition` statement and evidence link must name the $s(60)$ premise; its verification and confirmation cannot exceed that premise. Do not label the source’s corollary an independent checker of $s(60)$. |
| $s(61) = 8$ from wand125’s point-only cover | New independent reported route, with separate [pinned primary bundle](https://github.com/wand125/square-packing-bounds/tree/f8846cec9661773dbd0cc7cbeee7d01ddb12a2b8/point_n61_L8). The [evand replay manifest](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/s61_wand125/MANIFEST.txt) is secondary evidence. | `S3` for a distinct single-case method, with separate source attribution and a reported-evidence atom before local source retention/replay. Its independence may later strengthen confirmation of the *value* at $n = 61$, but does not confirm $s(60)$ or `Valid7`. |
| $s(k^2 - 3) = k$ for every integer $k \ge 6$ | New family-level reported result. Extend the scope schema for a parameterized infinite family, or hold the all-`k` statement in a separately linked theorem record until that schema exists. Finite instances $n = 33, 46, 61, 78, 97, \ldots$ may be materialized only with their derivation and source family named. $n = 33$ and $46$ already have Bentz-era values; $n = 61$ also has the two routes above. | `S4` for a bound family, potentially `S5` if the project separately judges broad significance. The lower half depends on `Valid7`, checked by one exact source implementation; the Lean theorem proves its implication, not the premise. Retain and audit the leaf record, exact checker and conditional Lean mapping, then select a bounded full rerun or independent implementation. Scope and composition must prevent the conditional theorem from being mistaken for a kernel check of the computational premise. |
| New Lean proof-assistant claims for older bounds | Evidence updates to existing `T-049`, `T-051`, and `T-052`, not new values. The pinned [`LADDER.md`](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/lean/LADDER.md) describes n12 theorem coverage; Proofs distinguishes the n21 conditional top theorem and n32 unconditional theorem. | Keep the main baseline `V3/C3` until the claimed Lean builds and exact certificate interfaces are mapped. A source statement about a kernel check is a reported proof claim, not a local `V5` build. The [September review](review-2026-09-28-evand-s21-s45-mixed-covers.md) remains the replay evidence for the old numerical certificates. |
| Side-4 and side-5 fractional-dual obstructions; side-3.99 exact witness | Research evidence, not new square-packing values. [COVER4](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/COVER4.md) has public exact side-4 support; [S21_KILL](https://github.com/evand/square-packing/blob/08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5/s12/search/S21_KILL.md) has public side-5 support, obstructing additive-cover budgets below about $20.648$ there, but its mass remains below 21. The side-3.99 support is absent. | Track as method/obstruction research, with exact-versus-measured labels. Replay the public supports in a portable wrapper and inspect the `--n`/support invariants before registering a negative-method result. Do not infer $s(12) = 4$ or $s(20) = 5$ from these LP duals. |

**Integration disposition, 2026-10-01.**
[PR 267](https://github.com/jlevy/squares/pull/267) registers Daniel’s $s(60) = 8$ as
T-062 (`V0/C1/S3`), its $s(61) = 8$ corollary as T-063 (`V0/C1/S1`), and the finite
$n \le 324$ projection of the square-minus-three family as T-064 (`V0/C1/S4`). The
source’s all-`k ≥ 6` theorem remains explicit in T-064’s claim and review while
`think-kqi1` tracks an infinite-family scope type.
The reported case lane changes; verified bounds do not.
`think-e7xa` tracks the `s60` replay, `think-4k80` the `Valid7` premise and Lean
reduction review, `think-hxrz` the independent wand125 primary-source intake, and
`think-q5tt` the public dual support replay.
No older `T-049`/`T-051`/`T-052` Lean claim was promoted by this intake.
`think-e8qx` tracks those source Lean changes, and `think-2z60` tracks the auxiliary
clique-lemma repair identified in the mathematical-transfer review.

For W2, retrieve the omitted `s60` run logs and the full source/Lean build only for
chosen checks, using the pinned commit and separate receipts for each tier actually run.
The
[October packet](../../../packing/resources/web/evand-square-packing-2026-10-01/README.md)
already retains the smaller source and support subset for W1. Register the new reported
results and source coverage before any verified-bound promotion.
Review changes to the old `s21`, `s32` and `s45` bundles against the September archive
separately, including the new `s21`/`s45` guard and repeated-checker records and the
`s12`/`s32` Lean claims.
GitHub’s 54-commit comparison shows new logs and code there, but this pass did not
establish that old local verdicts changed.
Leave the September packets and their evidence intact.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
