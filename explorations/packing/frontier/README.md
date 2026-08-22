# Frontier: what is known about `s(n)`, case by case

`s(n)` is the side of the smallest square holding `n` non-overlapping unit squares.
This folder is the structured record of what is known for each `n ≤ 100`: one artifact
per case, carrying the best known packing, the best proved lower bound, the provenance
of both, and links into the local literature archive — plus an editorial section on each
that says what the numbers do not.

## Why this is a folder and not a table

The research documents carry the narrative.
This folder carries the **facts**, in a form a tool can read, because a 65-row table
with seven columns per row is at the edge of what prose can hold accurately — and in
fact the first version of that table, written by hand into the research document, got a
headline claim wrong.
Building it as data caught the error immediately (see
[The next family to fall](#the-next-family-to-fall) below).

Each `n-NNN.md` is a [softschema](https://github.com/jlevy/softschema) artifact: YAML
frontmatter carrying the structured payload, validated against
[`square-packing-case.schema.yaml`](square-packing-case.schema.yaml), followed by a
Markdown body that is purely reader-facing.

**The frontmatter is authoritative.** A consumer reads the YAML and must not parse the
body prose for structured values.
The body is where judgement, history, and caveats live — the things that would be lies
if forced into a field.

```bash
# validate one case, or all of them
uvx softschema@latest validate n-011.md
for f in n-*.md; do uvx softschema@latest validate "$f" >/dev/null || echo "FAIL $f"; done
```

## Choosing a format per dataset

Not everything belongs in this shape, and the folder deliberately mixes two:

| Shape | Used for | Why |
| --- | --- | --- |
| One soft-schema artifact per record (`n-NNN.md`) | The per-`n` cases | Heterogeneous, and each carries real editorial content that no schema can hold |
| A single plain YAML file ([`asymptotic-waste-bounds.yaml`](asymptotic-waste-bounds.yaml)) | The `W(x)` exponent chain | Homogeneous rows, no per-row story; splitting eight bounds into eight files would add ceremony and subtract legibility |

The rule of thumb: **split into artifacts when each row has its own narrative**; keep
one file when the rows are a sequence and the narrative belongs to the sequence.
A Markdown table in a research document remains right when the table is small and its
job is to be read rather than queried.

## What is in a case

The payload fields are documented in the schema.
The ones that carry the most weight:

- `status` — `proved` or `open`. 35 of the 100 are proved.
- `upper_bound` — the best known packing: value, exact form, algebraic degree, minimal
  polynomial, whether it is rigid, whether it has been analytically optimized, how it
  was found, and by whom.
- `lower_bound` — the best proved bound and, crucially, **which argument supplies it**
  (`area`, `nagamochi`, `monotonicity`, `unavoidable_points`, `perfect_square`,
  `counting`). This is the field that shows where the proof machinery actually reaches.
- `resources` — citation keys with paths into [`../resources/`](../resources/README.md)
  and a `retrieved` flag.
- `verified_here` — claims independently re-derived in this repository, not taken on
  authority.

## What the corpus shows

Counts below are computed from the artifacts, not asserted.

**The lower-bound frontier is one theorem.** Of the 65 open cases, **63** have
Nagamochi’s general closed form as their best proved lower bound.
Exactly two — `n = 11` and `n = 12` — are governed by anything bespoke, and both trace
to Stromquist’s single 2003 argument.
Nothing in this table has been improved since 2005.

**The search frontier is much healthier.** Of the 65 open cases, 31 are still held by
the trivial grid, but the remaining 34 carry real constructions: 14 hand-built, 11 from
simulated annealing (all dated 2024–2026), 5 diagonal strips, 3 extensions of smaller
records. Records move monthly; bounds do not.

**Algebraic degree explodes past `n = 11`.** Degrees recorded in the catalogue for
`n ≤ 100` run 4, 5, 6, 8, 12, 18, 20, 24, 42, 44, 82. Every *proved* case is degree ≤ 2.
That gap between what is certifiable and what is conjectured is the subject’s central
obstruction.

### The next family to fall

Ranked by gap, the four smallest open cases at `n ≤ 100` are:

| `n` | gap | record | note |
| --- | --- | --- | --- |
| 97 | 0.0557 | grid | `10² − 3` |
| 78 | 0.0627 | grid | `9² − 3` |
| 61 | 0.0718 | grid | `8² − 3` |
| 11 | 0.0882 | Trump 1979 | the famous case |

Three of the four are consecutive unproved members of the family `s(m² − 3) = m`, which
is **proved exactly for `m = 3, 4, 5, 6, 7`** (that is
`s(6), s(13), s(22), s(33), s(46)`) and conjectured beyond.
Their gaps are small because Nagamochi’s bound is nearly tight there, and their
conjectured optima are **integers** — the case the existing proof technique is built
for.

They are, on this evidence, the most tractable unproved cases in the table, and they are
essentially undiscussed in the literature.

`n = 11` is the smallest gap among cases with a *non-trivial* record, and it is not
close: the next such case is `n = 19` at `0.4215`, nearly five times wider.
That is the correct form of a claim the research document originally overstated.

## Cross-references

- The narrative and the mathematics:
  [`../docs/project/research/research-2026-08-22-packing-11-unit-squares.md`](../docs/project/research/research-2026-08-22-packing-11-unit-squares.md)
- Algorithms, verification and tooling:
  [`../docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md`](../docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md)
- The literature archive these artifacts cite:
  [`../resources/README.md`](../resources/README.md)
- The exact verifier: [`../README.md`](../README.md)

## Provenance and regeneration

Upper bounds, degrees, minimal polynomials, rigidity flags, analytic status and
attributions were parsed from the archived record catalogue capture
(`../resources/web/kingbird-squares-in-squares.md`, retrieved 2026-08-22). Lower bounds
were computed from four sources and the strongest taken.
The proved set and its attributions come from the research document’s own analysis,
which is sourced to the individual papers.

Editorial bodies for `n = 5, 10, 11, 12, 13, 17, 22, 23, 46, 51, 100` are hand-written.
The rest are generated from the structured fields, and say only what those fields
support — they are accurate, not padded.
Adding editorial to a case is just editing its body; nothing regenerates over it.

**Known limits.** The catalogue is parsed as annotation text, so an entry phrased
unusually can be miscounted; `improved_by` in particular under-reports where the
catalogue uses “Refound”, “Optimized by”, or prose.
Tilt angles are recorded only for the handful of cases where this research established
them. Nothing here should be treated as more authoritative than the archived capture it
came from.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
