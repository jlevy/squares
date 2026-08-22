<!-- Campaign idea board. HAND-WRITTEN: this is an input, not a generated view.
Its referential integrity with the registry is checked by ledger.py, not its content. -->

# Idea board — <campaign>

**Campaign question.** <one falsifiable sentence, copied from the runbook>

This page is the whole idea space on one screen.
Read it before the registry, the exploration reports, or the ledger — those are deep and
this is wide. Every idea anyone has had about this campaign appears here as one line,
whether or not it has been formalized, tried, or killed.

## How to use it

- **Arriving**: read this page, then the runbook, then only the rows you are about to
  work on. The exploration reports are the depth behind a row; open one when a row is not
  self-explanatory.
- **New idea**: add a row here first, `status: raw`. Formalizing comes later and does
  not always come.
- **Promoting**: when an idea can be stated so it could be wrong, the codifier writes
  `hypotheses/H-NNN-*.md` and fills in the `H` column.
  The row stays; it is now a pointer.
- **Killing**: never delete a row.
  Move it to Dead ends with the reason.
  A deleted idea gets reproposed in three weeks.

Both directions are enforced: every `H-NNN` named here must exist in the registry, and
every registered hypothesis must appear on this page.

## Status vocabulary

| Status | Means |
| --- | --- |
| `raw` | someone thought of it; not yet shaped into anything testable |
| `shaped` | it is clear what would test it, but no instrument exists yet |
| `registered` | it is in the registry as `H-NNN`; the ledger has its status from here on |
| `parked` | plausible, deliberately not now — the reason says what would change that |
| `dead` | killed on reading, without a round being spent — the reason is the value |

Once a row reaches `registered`, this page stops tracking it: the ledger owns its
outcome. That is what keeps this page from becoming a second, drifting record.

## Orientation

<Two or three paragraphs an arriving agent needs before any row makes sense: what is
already known, where the frontier is, what has already been ruled out, and what the
standing best is. Keep it current; this is the most-read text in the campaign.>

## <Lane or family> — <one line on why this family matters>

| # | Idea | Status | H | From | Why it might work, or not |
| --- | --- | --- | --- | --- | --- |
| 1 | <one line, no more> | registered | [H-004](hypotheses/H-004-....md) | [X-001](explorations/X-001-....md) | <the crux in a clause> |
| 2 | <one line> | shaped |  | [X-001](explorations/X-001-....md) | <needs an instrument that does not exist> |

## Open questions

Things worth knowing that are not claims, and so cannot be hypotheses.
Registered as `kind: open_question` when they are worth carrying formally.

- <question> — <why it matters, what would answer it>

## Dead ends

Killed without spending a round, with the reason.
This section is why the campaign does not rediscover its own mistakes.

- <idea> — <why it cannot work> (raised in [X-002](explorations/X-002-....md))
