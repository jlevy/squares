# `n = 19–21` Lower-Bound Literature Audit, 2026

This receipt records the source check used to describe the `24/5` certificate for
`n = 19`, `20`, and `21`. Its conclusion is deliberately bounded: no retained or
directly checked source below reaches `24/5`. It does not establish absolute priority.

## Sources checked

- The repository's cleaned 2009 transcription of Friedman's dynamic survey,
  [`friedman-ds7-packing-unit-squares-in-squares.md`](../../papers/friedman-ds7-packing-unit-squares-in-squares.md),
  especially the `n = 19` discussion, Figure 34, and Table 2.
- The retained original 2009 survey HTML,
  [`friedman-ds7-survey-2009-html.html`](../friedman-ds7-survey-2009-html.html).
- The Electronic Journal of Combinatorics
  [DS7 article record](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS7),
  its version history, and the official
  [July 2000 edition](https://www.combinatorics.org/files/Surveys/ds7/ds7v2-2000/ds7-2000.html).
- Nagamochi's 2005 paper and its retained extraction, the retained Burns–Massaccesi
  `n = 17` source packet, and this repository's T-019 record.

The 1998 survey version does not contain Table 2. The case-specific entries below are
therefore dated no earlier than the July 2000 edition.

## Findings

| Case | Earlier source claim | Evidence retained here | Status before T-020 |
| ---: | --- | --- | --- |
| 19 | `s(19) ≥ 6√2 − 4 ≈ 4.485281`, in DS7 by 2000 | Figure 34 and a graphical unavoidable-set proof sketch, but no coordinates or replay | Reported historically; later passed by Massaccesi's `4.5058` and T-019's verified `4.59` |
| 20 | `s(20) ≥ 6√2 − 4`, grouped with `n = 19` in DS7 by 2000 | The table entry and monotonicity from `n = 19`; no bespoke certificate | Reported historically; later passed by Nagamochi's verified `1 + √13` |
| 21 | `s(21) ≥ 4.7438` in DS7 by 2000 | A four-decimal table entry only; no exact form, figure, derivation, or underlying citation was located | Strongest located report; Nagamochi's `1 + √14 ≈ 4.741657` remained the strongest replayed proof |

The source record therefore does **not** support saying that `n = 20` or `n = 21` had
never had a case-listed lower bound. It supports the narrower statement that T-020 is a
new independently replayable `24/5` bound and that no source checked here reaches it.

## Comparisons with T-020

The `24/5 = 4.8` certificate improves the immediately preceding verified register by:

- `0.21` at `n = 19`, over T-019's `4.59`;
- `19/5 − √13 ≈ 0.194449` at `n = 20`; and
- `19/5 − √14 ≈ 0.058343` at `n = 21`.

Against the stronger but unexplained DS7 report at `n = 21`, the improvement is only
approximately `4.8 − 4.7438 = 0.0562`. The two comparisons answer different questions
and are kept separate in the frontier record.

## Search boundary

The local pass searched the retained papers, web captures, case pages, results register,
and evidence register for `n = 19`, `n = 20`, `n = 21`, `4.8`, `24/5`, `4.7438`, and
`6√2 − 4`, then checked the journal's versioned survey pages directly. The broader
[finite-case query log](../finite-case-literature-audit-2026/README.md) covers recent
papers but did not originally include `n = 20` or `n = 21`; it cannot carry this history
claim by itself.

This was not a systematic search of every journal, language, preprint server, private
communication, or uncatalogued result. Accordingly, T-020 remains
`apparently-novel`, meaning novel relative to the recorded search, not confirmed first
publication.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
