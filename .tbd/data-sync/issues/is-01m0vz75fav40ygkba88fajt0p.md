---
type: is
id: is-01m0vz75fav40ygkba88fajt0p
title: "TUTORIAL: rebuild §9's vocabulary card on a stated discipline"
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T08:05:05.642Z
updated_at: 2026-08-25T08:05:05.642Z
---
§9 is titled "A Vocabulary Card" and says "[`SYNOPSIS.md`](SYNOPSIS.md#terminology) is
the authority; this is the short form." It has fourteen rows chosen by no stated rule,
and the omissions are not the marginal terms.

**On `basin` specifically.** It *is* there, as the compound row **basin / point-basin**.
But it is the document's most-used technical term — 26 occurrences in the body against
`quench`'s and `cell`'s far fewer — and the card gives it a definition that is circular
for a first reader (it is defined through "quench", and "polish" and "exploration" are
then defined through it). If any term deserves its own row and a worked sentence, it is
this one.

## Terms used in the body and absent from the card

Counts are body occurrences in `TUTORIAL.md`:

| Term | Uses | Where it matters |
| --- | ---: | --- |
| **proposer** | 6 | §8's open item 2 is "whether record packings are rare **under a named proposer**"; §7's whole strategy argument turns on it |
| **rigidity** | 5 | §3 and §4 both scope claims by it ("not by itself a rigidity proof"), and `SYNOPSIS.md` defines it carefully because contact counts are *not* it |
| **refiner** | 3 | The other half of the proposer/refiner pair, which `SYNOPSIS.md` names separately "because the measurement that matters is which one is failing" |
| **descriptor** | 3 | §7's steering section is built on it, and it is one of the four cartography deliverables |
| **polish failure** / **exploration failure** | 1 each | §3 introduces them as "the campaign's central diagnostic", and `SYNOPSIS.md` has a "Not used here" entry warning against the near-miss coinages "polish gap" / "exploration gap" |
| **quench map** | 1 | `SYNOPSIS.md`: "Say 'the quench map' where the distinction matters" — the card's single `quench` row merges the map and the component |

`analytic optimum` and `class bracketing` are used in `SYNOPSIS.md` and not in the
tutorial at all, which is a defensible choice but should be a choice.

## Rows that drift from the declared authority

- **gap** — the card says "always `best_side − standing_best`, signed", and §1's own
  table uses `gap` for upper bound minus lower bound. The card contradicts the document
  it sits in (also think-8hdt).
- **atlas / census** — these are two different deliverables with two different statuses,
  not a synonym pair, and compounding them into one row is a category error.
  The row also drops the caveat `SYNOPSIS.md` attaches to both: code exists, and it
  stores endpoint keys that are not certified terminal components.
  §6 makes that point; the card quietly unmakes it.
- **exploration** — `SYNOPSIS.md` marks exactly three words as carrying controlled
  multiple senses: **exploration**, **cell**, and **quench**, each with a stated rule for
  which form to write. The card handles `cell` correctly, handles `quench` partially, and
  does not flag `exploration` at all.
- **terminal component** is defined as "a connected component of the terminal set", and
  **terminal set** has no row.

## No stated ordering

The card is neither alphabetical nor dependency-ordered.
It opens in dependency order — configuration, cell, quench, basin — then drifts, so
`angle class` lands after `corner` even though the corner is a property of the
class-angle objective. Either order works; not choosing one makes the card hard to scan
and hard to extend correctly.

## Proposal

Give the card a stated discipline and hold it:

1. **A coverage rule.** Say what earns a row — every term the document uses in a narrow
   sense that a general reader would otherwise read loosely — and apply it, which adds
   the six terms above.
2. **A stated order**, dependency-first, so a reader can read the card top to bottom
   once instead of jumping.
3. **No compound rows for non-synonyms.** Keep `basin / point-basin` and `corner / kink`,
   which are genuine synonym pairs in this project; split `atlas` from `census`.
4. **Flag the three controlled-sense words** with their write-this-form rule, as
   `SYNOPSIS.md` does.
5. **Say what the card does not cover** — symbols live in the notation table
   (think-8hdt), and `SYNOPSIS.md#terminology` remains complete.

Terms stay short-form; anything needing a paragraph belongs in the body or the synopsis.
