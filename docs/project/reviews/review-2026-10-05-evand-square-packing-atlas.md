# Evan Daniel’s Square Packing Atlas: Site Review and Import

**Date:** 2026-10-05. **Workflow:** W1, stages 1 to 3 of the
[result import runbook](../../../packing/campaign/result-import.md), with a citation
review of the site; bead `think-plrl`, and `think-kqc3` for the homepage link.
**Reviewer:** Claude (AI review; model unstated), the evand site lane of the 5 October
follow-up, separately prompted.
**Source:** the [Square Packing Atlas](https://evand.github.io/square-packing/) and its
[open-problems page](https://evand.github.io/square-packing/problems.html), as
[evand/square-packing](https://github.com/evand/square-packing/tree/7ff3b2113532889708a3baa4d56bc44294022e63)
builds them at `7ff3b211`, committed 2026-10-04T20:17:38Z. The pages and the claim files
are retained in the
[4 October evand packet](../../../packing/resources/web/evand-square-packing-2026-10-04/README.md),
cited as **[evand square packing atlas 2026-10-04]** and
**[evand square-packing 2026-10-04]**.

**In one line:** the site states this record’s results accurately where it states them
as verified here. Its floors table matches the verified lane at 99 of 100 counts and at
every count it marks verified.
Its new results since 3 October move no case of this record.
I found no defect that blocks anything here.
Seven non-blocking items concern the site’s currency or wording (§6), and one claim it
reports belongs to an import of its own (`think-1qms`).

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Pages | `site/www/index.html` (Overview), `explore.html`, `compare.html`, `bounds.html`, `proofs.html` (Proofs and results), `problems.html` (Open problems), `sources.html`, `k2m4/index.html`, and the `s12/docs/` pages the site serves at `/s12/`, `/s13/`, `/s21/`, `/s32/`, `/s45/`, `/s60/` and `/k2m3/` |
| Data | `site/www/data/lower_bounds.json` (the floors table, also `site/data/`), `timeline.json`, and the overview’s rule for ringed families in `site/www/js/overview.js` |
| Repository material since `2eb15455` | `s12/search/S20_LB.md`, the cover `s20lb_cover_4886.txt` and `s12/tasks/s20-review/REPORT.md`; `s12/search/CEILINGS_17_20.md` and its four supports; the Lean files `LebMass.lean`, `LebMass7.lean`, `ValidSplit7.lean` and `SpecChelokot.lean` with `notes/lean-leb-mass.md`; `s12/search/WISHLIST.md`, `FRIEDMAN.md` and the two literature notes; `s12/notes/jlevy-s17-techniques.md`; `s12/README.md`, the root `README.md` and `CREDITS.md` |
| Run here | [`devtools.compare_site_floors`](../../../packing/devtools/compare_site_floors.py) on the retained floors table, with the overview’s family rings; its receipt is [`site_floors_compare.json`](../../../packing/resources/web/evand-square-packing-2026-10-04/receipts/site_floors_compare.json). Lookups of the case records for the problems page’s tables (§5) |
| Not run | No certificate, checker or Lean file of the source was run. The deployed site was not fetched, since this session’s egress blocks `evand.github.io` |

## 2. What the Site Is

The Square Packing Atlas is a static site about $s(n)$, built by Evan Daniel in 2026. It
draws every record packing in David Ellsworth’s catalogue, which continues Erich
Friedman’s survey. It measures each packing’s angles, contacts, free squares, gaps and
symmetry with its own parser and rigidity analysis.
It charts how the records changed over time, and tabulates the proven floor for each
$n \le 100$. It presents Daniel’s 2026 computer-checked lower bounds and exact values.
Since 4 October it has an open-problems page about questions that span many $n$. The
packings are Ellsworth’s; the site says its analysis is its own and was written without
his code. The repository’s `CREDITS.md` says the work was produced by Claude (Anthropic)
in a single session under human direction.

The overview marks a count with a filled dot when it is proved optimal in the
literature, and with a ring when it was “proved in 2026, unrefereed, verified on
jlevy/squares”. That ring states something about this record, so §4 checks it.

## 3. Claim Map

Status is this record’s evidential status for the claim: **proved** (a published or read
proof), **computationally verified** (a certificate replayed here, or a proof assistant
build here), **best known** (a construction not proved optimal), or **asserted**
(reported, not verified here).

| # | Claim | Where | Status here | Register action | Id |
| --- | --- | --- | --- | --- | --- |
| 1 | $s(11) = 3.8770835900\ldots$, Trump’s packing optimal (Ahmed) | Overview, Proofs, Sources §5, floors table | Computationally verified | Already registered | `T-060` |
| 2 | $s(21) = 5$, $s(32) = 6$, $s(45) = 7$, $s(60) = 8$, $s(61) = 8$ | Overview cards, Proofs, Sources §5, `/s21/` to `/s60/` | Computationally verified | Already registered | `T-052`, `T-051`, `T-053`, `T-062`, `T-063` |
| 3 | $s(59) = 8$ and $s(77) = 9$ (wand125) | Floors table, Sources §5 | Computationally verified | Already registered | `T-066`, `T-067` |
| 4 | $s(k^2 - 3) = k$ for every $k \ge 6$ | Overview, Proofs, `/k2m3/` | Computationally verified for $k = 6$ to $18$, the reduction to every $k$ built here | Already registered | `T-064` |
| 5 | $s(k^2 - 4) = k$ for every $k \ge 5$ | Overview, Proofs, `/k2m4/` | Asserted for $k \ge 10$; $k = 5$ to $9$ are computationally verified by other entries | Already registered, reported; the replay of `ValidTilt9` continues there | `T-081` |
| 6 | $s(k^2 - 1) = k$ and $s(k^2 - 2) = k$, re-proved after the gap in Nagamochi’s Lemma 1 | Overview, Sources §3, problems §1 | $k^2 - 1$ proved (read and re-derived, `C1`); $k^2 - 2$ computationally verified (Lean built here) | Already registered | `T-084`, `T-086`, `T-085` |
| 7 | $s(12) \ge 15680000/3949423 = 3.9702$, the best floor | Proofs, Sources §5, floors table | Computationally verified | Already registered | `T-079` |
| 8 | $s(12) \ge 15680/3951$, $35/9$, $3920/997$ and $s(11) \ge 3040/797$, kernel-checked in Lean | Proofs, Sources §5, root `README.md` | Asserted; below the standing bounds | None; in earlier packets | `T-049` holds the first |
| 9 | Case-free $s(13) = 4$ | Proofs, `/s13/` | Proved (Bentz) and computationally verified | Already registered | `T-006` |
| 10 | $s(20) > 3 + 4\sqrt{2}/3$, so $s(19) < s(20)$, by a point cover at side $2443/500$ | `S20_LB.md`, `REPORT.md`, floors table note | Asserted; below the verified $1959/400$ | None; it stays in the packet, with a reported evidence entry the case record cites | `E-n020-evand-point-cover-4886-report` |
| 11 | No pure closed cover proves $s(17) \ge 4.660$ or $s(19) \ge 4.8856$: $\nu_f(4.660) \ge 17.0447$ and $\nu_f(4.8856) \ge 19.375$ | `CEILINGS_17_20.md` | Asserted (the source’s exact checks, not run here) | None; a method limit by others that the record does not act on | — |
| 12 | Lemmas U and K proved sound in Lean, all 689 LEB and 374 CAP leaves of the `ValidTilt7` run kernel-checked, and `bentz_of_validTilt7` | `LebMass*.lean`, `ValidSplit7.lean`, `lean-leb-mass.md` | Asserted (not built here) | Evidence update: a note in `next_rung`, `notes` and `artifacts` | `T-064` |
| 13 | chelokot’s `IsMinimumSide` equivalent to `minSide n = s` for $n \ge 1$ | `SpecChelokot.lean` | Asserted (not built here) | Evidence update: a note | `T-086` |
| 14 | Floors for every $n \le 100$, with 20 marked verified here | `lower_bounds.json`, Bounds | Computationally verified at 99 counts; at $n = 96$ asserted (`T-081`) | None; checked in §4 | receipt |
| 15 | Guzhou0806’s R070 and R071, $s(17) > 18641771/4000000$, in the table’s history | `lower_bounds.json`, Sources §5 | Asserted | An import of its own, from Guzhou0806’s repository | `think-1qms` |
| 16 | Kleddamag’s $s(17) > 46601/10000$ | Sources §5, table history | Asserted; below the verified $116511/25000$ | None; a packet note | — |
| 17 | Record packings, their dates and finders | Explore, Compare, Bounds | Best known (Ellsworth’s catalogue) | None; this record reads its own captures of the catalogue | — |
| 18 | Its rigidity analysis agrees with Ellsworth’s 30 rigid and non-rigid marks | `site/README.md`, Sources §7 | Asserted (not compared here) | None | — |
| 19 | Open problems and conjectures | `problems.html`, `WISHLIST.md` | Questions and conjectures, not results; §5 | None | — |

Claims 10, 11 and 12 are new since the 3 October packet.
Claims 1 to 9 restate results the register holds, and the site’s wording for each was
compared with its entry.
The $k^2 - 4$ family also gives $s(k^2 - 3) = k$ for every $k \ge 5$ by monotonicity;
the source now says so.
`T-081`’s notes already record that consequence, and that `T-064` names the route once
`T-081` is replayed.

## 4. What the Site Says About This Record

**The floors table.**
[`devtools.compare_site_floors`](../../../packing/devtools/compare_site_floors.py)
compares the table’s floor at each $n \le 100$ with the case records’ verified and
reported lower bounds.
It compares exactly where both sides write a rational, and to $10^{-9}$ otherwise.

| Relation of the site’s floor to this record | Counts |
| --- | --- |
| Equal to the verified and the reported bound | 73 |
| Equal to the verified bound, below a reported bound not replayed here | 25: $n = 20$, $42$ and 23 counts from $51$ to $95$, each below a reported wand125 certificate |
| Equal to the verified bound, which is above the reported one | 1 ($n = 12$, where the reported lane holds squarepacker’s $31360/7901$) |
| Above the verified bound, equal to the reported one | 1 ($n = 96$, Daniel’s $k^2 - 4$ family, `T-081`; not marked verified) |

All 20 floors marked `register: verified` are values the verified lane holds: $n = 11$,
21, 23, 32, 34, 45, 47, 48, 59 to 63, 77 to 80 and 97 to 99. Past the table, the
overview rings every $n \le 324$ in the families $s(k^2 - c) = k$ for $c = 1$ from
$k = 3$, $c = 2$ from $k = 2$ and $c = 3$ from $k = 6$. Each of those 24 counts has $k$
as its verified lower bound.
For $c = 4$ the site waits for `T-081`’s replay, and correctly so: the verified lane
holds $k$ at none of the eight counts from $n = 117$ to $320$.

**Agreements.** The site credits wand125 with $s(77) = 9$ first, Ahmed with $s(11)$, and
this record’s `T-079` with the best $s(12)$ floor.
It describes the $k^2 - 3$ family as independently re-checked by wand125’s checker, and
says the $k^2 - 4$ family has one implementation and waits for replay.
It says Nagamochi’s 2005 proof rests on a false lemma, and that Karakuş re-proved
$k^2 - 1$ and chelokot $k^2 - 2$. Each of these agrees with the register.
Daniel’s notes on this repository (`s12/notes/jlevy-s17-techniques.md`) list the rungs
of his entries as the register gives them on 3 October.
They also observe that R070, R071 and Kleddamag’s 4.6601 are not registered here, which
is true.

**Disagreements**, none of which moves a value; each is listed in §6:

- $n = 77$ is credited in the table to Daniel’s $k^2 - 4$ route and marked verified.
  The verified lane holds $s(77) = 9$ from wand125’s cover (`T-067`); Daniel’s route
  there is `T-081`, reported.
  The value is right and the route is not.
- The $n = 17$ note calls `T-043` “`V4/C3`”. Since the ladder change of 30 September it
  is `V3/C3` ([epistemics.md](../../../epistemics.md#what-changed-on-2026-09-30)).
- Sources §5 says Ahmed’s proof was “replayed independently by jlevy/squares”.
  The register’s confirmation of `T-060` is a re-implementation sharing the producer’s
  components, not an independent one.
- Sources §5 dates `T-079` to 3 October, its registration.
  Its `established` date is 2 October.
- The overview rings $k^2 - 1$ as register-verified on Karakuş’s re-proof.
  `T-084`, that re-proof, stands at `C1`, read and re-derived but not machine-checked.
  The rung on those values comes from other routes, such as the $k^2 - 3$ family by
  monotonicity. The marks are right; the attribution in the overview’s comment is not
  quite.

## 5. The Open-Problems Page

[problems.html](https://evand.github.io/square-packing/problems.html) states questions,
not results, and labels each one: *conjecture* (someone has predicted the answer),
*question*, or *known* (context).
It names who stated each, and “stated here” where the source found no earlier statement.
Its working list is `s12/search/WISHLIST.md`, with literature checks in two dated notes.
None of these is a result the register acts on, so none is registered.
They stay in the packet, with the checks below.

| Section | Items | Checked here |
| --- | --- | --- |
| §1 Friedman’s staircase | $c^*(k)$, the largest $c$ with $s(k^2 - c) = k$; Friedman’s Conjecture 1 (monotone $c^*$), unbounded $c^*$, unit steps, the last $k$ with $s(k^2 - k) = k$ | The “proved” row agrees with the register for $k = 2$ to $9$, where each cell is a verified exact value ($s(59) = 8$ gives $c^*(8) \ge 5$). Its cells $c^*(k) \ge 4$ at $k = 10$, 11 and 12 rest on `T-081`, reported, and the page says that result is the source’s own and unrefereed. The “best packings” row agrees with the record’s reported upper bounds at the counts it names. The argument for $c^*(k+1) \le c^*(k) + 2$ (an L-shaped border holds $2k - 1$ squares) and $c^*(k) = O(k^{3/5})$ from the waste bound were re-derived and hold |
| §2 Wasted space | $W(s) = O(s^{1/2})$ (Friedman’s Conjecture 2; Erdős and Graham) | Context from the literature; not checked |
| §3 Plateaus | A non-integer plateau, finitely many | The claim that proved bounds rule out a plateau for $n < 18$, the first open case being $s(18) = s(19)$, agrees with the record. The verified $s(18) \ge 939/200$ exceeds $s(17) \le 4.6756$, and the verified $s(19) \ge 1927/400$ is below $s(18) \le (7 + \sqrt{7})/2$ |
| §4 Complexity | Algebraic degree, number of angles, symmetry | The degrees it cites, 8 for $s(11)$ and 6 for the best $s(28)$, agree with the case records. The Galois group it gives is not checked |
| §5 Small $n$ meets large $n$ | Families that beat Göbel’s strips, where many-angle packings start, where table patterns break | Questions on the catalogue’s data; not checked |
| §6 Local optimality | Plateau-optimal packings, alternatives, stability; an exploratory model of 149 squares in which more than 470 pairings fit | The model is labelled by the source as exploratory, not a theorem; not checked |
| §7 Single values | $s(12) = 4$; targets $s(90) < 10$, the “next borderline cases”, members of fixed-shape families, $s(147)$ | The margins table $k - s(k^2 - c)$ agrees with the record’s upper bounds to its three decimals except one entry, and the list of borderline cases includes $s(211) < 15$, which is known (§6, S-1) |
| §8 Neighbouring problems | Rectangles, Erdős Problem 106, cubes | Not checked |

## 6. Defects

None blocks anything in this record: no register value, rung or case bound rests on the
site. Items S-1 to S-6 are about the source and go to its author with this review.
R-1 is this record’s.

- **S-1, non-blocking: the page lists a settled target.** §7 of the open-problems page
  names $s(211) < 15$ among the next borderline cases.
  Joost de Winter published a packing of 211 squares at side $14.99796\ldots$ on 16
  September 2026, and this register holds it as `T-057`, confirmed by an independent
  re-implementation here.
  The site reads Ellsworth’s catalogue, which does not list it, and lacks Francisco
  Couzo’s 49 smaller packings (`T-056`) for the same reason.
  The one visible effect on the margins table is at $k = 12$, $c = 13$, where Couzo’s
  $s(131) \le 11.95492$ gives $0.045$ against the table’s $0.043$.
- **S-2, non-blocking: one floor is credited to the wrong route.** The table’s $n = 77$
  floor is Daniel’s $k^2 - 4$ family, marked verified.
  The verified $s(77) = 9$ here is wand125’s cover (`T-067`), which the site credits as
  first elsewhere.
- **S-3, non-blocking: stale rung.** The $n = 17$ note gives `T-043` as `V4/C3`; it is
  `V3/C3` since 30 September.
- **S-4, non-blocking: the kind of confirmation.** Sources §5 calls the `T-060` replay
  independent. The register records it as re-implemented, sharing the producer’s
  components.
- **S-5, non-blocking: credit for the gap in Nagamochi’s Lemma 1.** §1 and §8 of the
  open-problems page credit the gap to Karakuş alone.
  The register’s `T-085` credits chelokot, whose counterexample is dated 4 September
  2026, and Karakuş. The site’s Sources §3 and floors table name both.
- **S-6, non-blocking: the repository’s front page is behind the site.** The root
  `README.md` still calls $s(12) \ge 15680/3951$ the best lower bound for twelve
  squares, below `T-078` and `T-079`. It also says the $k^2 - 3$ certificate is not yet
  independently re-implemented, although wand125’s checker exists.
  `s12/README.md` and the site are current on both.
- **S-7, non-blocking, the source’s own finding: a latent gap in a checker.** The
  source’s `s(20)` review finds that `zeromargin.roots()` takes `int(m / pitch)` with no
  divisibility assert.
  A `--full` run at a pitch that does not divide the half side would skip a strip of
  centres and still print `VERIFIED`. The $s(20)$ run does not reach it, and neither
  does the one replay here that runs `zeromargin.py`: the $s(32)$ sweep
  (`E-n032-evand-closed-cover-source-run`) takes its roots from `zm_d4_sweep.py`, which
  calls `d4_roots`, not `roots()`, at side 6. The other replays of Daniel’s covers here
  ran `zmx2` and `qx2_zm.py`.
- **R-1, non-blocking: the record lacked a citation for the site.** The only key for it
  was **[evand atlas explorer 2026-10-02]**, an unretained dated reference.
  **[evand square packing atlas 2026-10-04]** now cites the retained pages, and the
  homepage links the site and its open-problems page.

## 7. Out of Scope

- **Replays.** Nothing of the source was run.
  The $s(20)$ cover asks for no work; the ceilings bound a method, not a case; the Lean
  files are not built.
  `ValidTilt9`’s replay for `T-081` continues under `think-4uir`.
- **Upper bounds.** The site’s packings and their history are Ellsworth’s catalogue as
  the site parsed it. This record reads its own captures of that catalogue, and the
  Kingbird intake of the same day covers them; the timeline was not compared.
- **R070 and R071.** Guzhou0806’s two $s(17)$ certificates above the verified floor are
  an import of their own from Guzhou0806’s repository (`think-1qms`), not from this
  site.
- **chelokot’s archive.** `SpecChelokot.lean` cites chelokot’s Lean proofs of $s(10)$,
  $s(13)$, $s(22)$ and $s(33)$ as well as $s(6)$. Each of those values is already proved
  here; whether any of them warrants a simplification entry is chelokot’s import, not
  this one.
- **The rigidity analysis** of the catalogue’s packings, which the site says agrees with
  Ellsworth’s 30 marks, was not compared with this record’s rigidity assessments.

## 8. Verdict

The site is a faithful secondary source for this record’s results.
Every count it marks as verified here is verified here, and every family it rings is
held in the verified lane.
Where it reports something this record has not verified, it labels the claim as
unrefereed or as waiting for this record’s replay.
Its new results since 3 October are below a standing bound (claim 10), bound a method
(claim 11), or advance a formalization without discharging a premise (claims 12, 13), so
the register gains no entry.
The site and its open-problems page are cited and linked from the homepage.
The non-blocking items S-1 to S-6 go to Evan Daniel with this review when the owner
replies.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
