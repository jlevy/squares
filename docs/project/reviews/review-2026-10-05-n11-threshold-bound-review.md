# Eleven-Square Threshold-Bound Paper: Exposition Reviews and Their Disposition

**Date:** October 5, 2026\
**Author:** Claude Code, recording two sub-agent reviews; human oversight pending\
**Subject:** Part II,
[the review of Kleddamag’s certified lower bound](../../../packing/devtools/templates/n11-threshold-bound-review-article.md),
at Draft v0.1.0, and the series edits to Parts I and III, under
[the series plan](../specs/done/plan-2026-10-05-n11-explainer-series.md)\
**Tracking:** `think-n5dh` (slice S8 of the plan)\
**Status:** the exposition review that
[stage 6 of the result import process](../../../packing/campaign/result-import.md#stage-6-explain)
requires. Two reviews returned 90 findings, none blocking.
Commit `c67c89281` applied 86 of them, one was already resolved, and three were
rejected.

## What Was Reviewed

Both reviewers read the article sources at commit `08c953ddd`; the three article
templates did not change between that commit and `35b4cb09a`, the commit the findings
were applied to.

- **Part II**, `n11-threshold-bound-review`, Draft v0.1.0: the new paper on T-037, read
  from its article source and from its rendered Markdown edition for the filled caption
  values.
- **Part I**, `n11-lower-bounds-explainer`, v0.4.4: the series’ Further Reading item and
  the renderer’s frontier update.
- **Part III**, `n11-optimality-review`, v0.1.5: the define-before-use and notation
  changes of the plan’s §7.2 and §3, the lineage paragraph, and the bound ladder added
  to its lineage section.

Neither reviewer edited the repository.
Their reports and the one-line-per-finding disposition are session files and are not
retained; this record replaces them.

## The Two Reviews

**Fable 5.1, adversarial review of Part II.** Its scope was the mathematics, the credit,
the numbers and define-before-use.
It checked each lemma against the source proof, its checkers and the
[mathematical audit of 2026-09-22](review-2026-09-22-kleddamag-n11-mathematics.md).
It recomputed every number in the rendered edition from the retained certificate, the
evidence files, the native and T-059 row journals and the register.
It checked the credit statements against the source’s attribution and notice files and
against the plan’s §4 inventory.
Counts: 0 blocking, 6 significant, 15 minor.

**Opus 5.5, series review of Part II and the Part I and III changes.** Its scope was
clarity, duplication, the guidelines and the reader path.
It applied common-doc-guidelines, the practical-prose expression and form rules, the
AI-prose corrections, `paper-design.md`, the plan, `conventions.md`, the intuition
review of 2026-09-30 and the
[adversarial review of 2026-10-03](review-2026-10-03-n11-optimality-paper-adversarial.md).
It mapped every fact Part II states more than once, audited each caption, and read the
series in order, I to II to III. Counts: 13 significant, 40 minor, 16 nits.

## Verdict

The proof chain is complete, and neither review has a blocking finding.
Every lemma Fable checked is correct as stated except one premise.
The Boundary lemma assumed that dropped zero-area rectangles lie on event lines, which
the code does not guarantee (Fable S1); the conclusion survives because those rectangles
have zero area. The text closes the six gaps G1–G6 that the plan’s §5.4 lists in the
source, G6 once S1 is applied.
Fable recomputed the arithmetic $L_0/A=31/8$, the surplus of 107,864 units and the
rendered numbers, and every one matches its source except one caption that called a
1,440-step net “1,440 net directions” (Fable S4). Credit was accurate except for the
statements in Fable S2, S3 and M4 to M6. Opus’s significant findings are internal
contradictions, duplication, captions and spelling.
The one false mathematical statement it found, that squares with disjoint interiors hold
disjoint sets of sites, was in an informal paragraph deleted under its S1.

## Findings and Dispositions

“Applied” means applied in `c67c89281`. Where the reviews raised the same point, the
change was made once and both findings count as applied.

### Fable: Mathematics, Credit, Numbers, Define-Before-Use

| Class | Findings | Disposition |
| --- | --- | --- |
| Mathematics and the certificate’s description | 6: S1, M2, M3, M7, M8, M15 | All applied. A generic center is a center in an open y-cell that lies on no dropped rectangle, and the signed sum is the charge there. The Boundary lemma uses the envelope’s positive area. A row has $t\in[0,1)$ and $0<B<A$. The lemma uses the limit superior. A charge orbit has eight or fewer images. The file lists one site per site orbit and every image set per charge orbit. |
| Credit | 7: S2, S3, S5, M1, M4, M5, M6 | All applied, M6 by deletion. The k-of-m charge is Part I’s threshold atom under the series’ name, since Part I already defines it for any $k$ and $m$. T-025’s proof sums budgets over shared sites without remarking on it, and the source states the rule. T-061’s reweighting is named in the claim that this is the furthest the charge method reached. The ceiling claim holds on T-025’s core domain. T-038 added 2-of-3 charges to older point charges over parent-angle intervals. The continuation’s additions are Mira’s, by Mira’s own attribution. |
| Numbers in context | 2: S4, M14 | Applied. Figure 1 reads “1,440-step net of directions”. For M14 the gap clause about T-026 was deleted rather than extended with T-033’s gap, and Figure 2’s caption names T-033 as the bound in force when T-037 appeared. |
| Define before use | 6: S6, M9, M10, M11, M12, M13 | Applied. The preamble says the result is registered as T-037. Figure 4 names its charge by its index in the source’s list and no longer uses “orbit” or “row”. Figure 1 uses only defined terms. The tight row is named as row 11962, where $\Gamma$ is attained. The legal centers are described before the Envelope section defines them. The glossary says half-tangents. |

### Opus: Clarity, Duplication, Guidelines, Reader Path

| Class | Findings | Disposition |
| --- | --- | --- |
| Duplication | 23: S1, S9, S11, M1–M13, M15, M16, M28, N1, N2, N9, N11 | All applied. The k-of-m charge is defined once, in From Points to k-of-m Charges, which now precedes What Is New. Each verification fact is stated once. Part III’s lineage links Part II instead of restating its three changes. |
| Accuracy and internal contradiction | 10: S2, S3, S4, S5, S10, S13, M14, M22, M31, M32 | All applied, S2 to S4 and M31 together with the matching Fable findings. The unsupported “in order of importance” and a false lead sentence were deleted, and two bridge facts were rewritten. Part III’s Strict-core cross-reference names the independent control. |
| Define before use and terms | 14: S7, M18–M21, M25, M26, M29, M30, M38–M40, N10, N12 | All applied. “y-cell” is used throughout, glossed as Part I’s event cell. “k-of-m charge” replaces the synonym “threshold charge”, on the Papers card too. Part III’s “threshold certificate” is unbolded under the series term. The inventory links each forward-used term to its section. |
| Figures and captions | 9: S6, S8, M34, M36, M37, N6, N7, N13, N15 | 7 applied, 2 rejected (below). The roadmap paragraph was deleted, and Figure 3’s cards carry the section headings. Figure 10’s caption describes its own drawing. Part III’s captions set $T$ as math, and both papers say “The series bound ladder”. |
| Guidelines and register | 10: S12, M17, M23, M24, M27, M33, N3, N4, N5, N8 | All applied. Part II is spelled American, with the heading and anchor “Every Legal Center Collects Enough Charge”; “catalogue” stays because its heading is fixed. The paragraph on T-037’s former V4/C4 keeps the fact and the ladder link and drops the internal roles. The paper no longer cites a bead id. |
| Reader path | 3: M35, N14, N16 | M35 was already resolved: the infrastructure merge `f8430b6fc` added the series strip, and the review read a worktree without it. N14 rejected (below). N16 applied: Part I’s frontier update names Part II before Part III. |

### Applied in Another Form

- **Fable M6.** The reviewer proposed saying that no site carrying point weight lies
  within $10^{-3}$ of a T-026 site.
  That would be a new number computed outside any retained check, so the bullet instead
  follows the source attribution’s own account and drops “moved”.
- **Fable M10.** The gloss “(Part I’s atoms)” was not added to Figure 1, because the
  plan allows “atom” only at the point charge’s definition.
- **Opus M24.** The audit review records V4/C3 and the native review V4/C4, so the
  paragraph keeps “It held V4/C4 under the ladder in force until 2026-09-30”, which is
  the register’s note, and says the same-project question is not yet decided.

### Rejected

| Finding | Proposal | Reason |
| --- | --- | --- |
| Opus M34 | Delete Part III’s Figure 3, which redraws Part II’s bound ladder | Removing it changes Part III’s `FIGURE_KEYS` and renderer contract, which the brief for applying the reviews ruled out, and the plan’s owner default places the ladder in Part III’s lineage section. N13 gives the two captions one name instead. |
| Opus N14 | Rename “Parents, Cores and the Angle Catalogue” and “Parents and the One Inequality” | The brief keeps the first heading exactly, and Part III links its anchor. |
| Opus N15 | Cite Figures 1–11 in the prose | Placement already meets the figure rule, and the standard prefers deletions to additions. The one citation added is the row of Figure 4’s cores. |

## What Remains Open

- **Human oversight and confirmation.** T-037 stays S5/V3/C3 with its review record
  pending, as Part II says; these two agent reviews are not the human oversight record.
- **`think-yf6t`.** Whether a same-project review of another author’s certificate counts
  toward confirmation is not decided.
- **`think-4lye`.** It is open.
  The plan’s S8 asks to close it together with Part II’s credit section and to add the
  lineage Part II states to T-037’s register note; that note is not yet in
  `results.yaml`.
- **`think-n5dh`.** This record is the disposition S8 asks for.
  The slice stays open until the full checkpoint and every pull-request CI job pass.
- **Footnote links and the formatter.** The pinned flowmark-rs 0.4.0 rewrites a
  reference-style link inside a footnote definition into a private placeholder token.
  The six such links in Part II’s footnotes reached `c67c89281` broken, and `1e4f6f50b`
  restored them as inline links.
  No bead tracks the formatter defect.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
