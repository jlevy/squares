# Feature: The Exact-Side Register

**Date:** 2026-10-25 (last updated 2026-10-25)

**Author:** Claude (worker w-exact-sides-1025), for the owner (bead think-vgsw, tracker
[#811](https://github.com/jlevy/squares/issues/811))

**Status:** In Review

## Overview

The record states exact sides in several places, and nothing checks them together.
A case record writes an algebraic house as `root(p, low, high)`. T-193’s ledger and
T-244’s packet hold sides that are not houses yet.
T-246 holds s(29)’s degree-7213 polynomial only by a pinned archive, and n = 83’s case
record states a degree of 672 and nothing else.

This plan adds one generated register, `packing/frontier/exact-side-register.json`, that
lists each exact side fact the record can stand behind.
For each fact it records the degree, the polynomial inline or by a digest-pinned asset,
an isolating interval, who states it, and whether the fact is about the house or about a
named configuration.
`devtools.exact_side_register` derives it from main’s records, `select_houses`, the
intake ledgers and the retained packets.
It decides every inline polynomial again on each run, irreducibility and root isolation,
and a records-tier step fails when the register drifts from its inputs.

It supersedes the stack #403 → #435, which the owner declared out of date on 25 October
2026: “Begin a new polynomial PR with everything in mind, with the current code,
following our new best practices, and building on top of the polynomial reference for
Daniel’s n = 29.”

## Goals

- One register of exact side facts, generated, checked in the records tier, and written
  one record per line.
- Main’s notation throughout: `exact_sides.polynomial_text` for polynomials and the
  `root(p, low, high)` binding the case schema states.
- Every inline polynomial decided irreducible and its root isolated, on every check, in
  well under a second.
- A large polynomial held by its pinned reference and the facts measured from it, as
  T-246 holds s(29)’s.
- Later slices priced here, each with a bead under one epic that references #811.

## Non-Goals

- **Writing on case records.** The records keep what `adopt_houses` writes; derived
  facts live in the register (decision D2 below).
  No bound, house or result moves.
- **New results.** Nothing is registered, re-scored or re-graded.
- **Replaying T-246.** The source’s five-step replay is think-10m1’s, on an owner
  budget.
- **The site catalogue.** It is a later slice, rebuilt from this register.

## Background

### What Main Holds

| Count | Fact | Where | Rungs |
| --- | --- | --- | --- |
| 51, 70, 102, 123, 153, 207, 258, 259, 295, 302 | Algebraic houses of degree 2 to 8 | The case records’ `exact_form`, written by the house writer (think-ot5c, #756) | T-126, T-174, T-193 |
| 88, 126, 175, 199, 232, 266, 267, 292, 301 | T-193’s sides, the house under the house rule, adoption staged | `select_houses.PENDING_ADOPTION`; the 16 October ledger | V3/C3 |
| 204 | T-193’s side, now above Polkovskyi’s house (T-231) | The 16 October ledger | V3/C3 |
| 172, 263 | Kim’s KKT sides of degree 24 and 17, below T-174’s rational houses | T-244’s packet and the 25 October ledger | V0/C0 |
| 29 | Daniel’s degree-7213 side of the house’s configuration | T-246; the `evand-exact-data-2026-10-12` packet pins the 87 MB archive | V0/C0 |
| 83 | Degree 672, the catalogue’s statement | The reported lane; the picture that prints the polynomial is pinned by digest in the 5 October pictures receipt | reported |

Sixteen more houses are irrational but written in older notations: fifteen quadratic
closed forms such as n = 5’s `2 + (1/2)sqrt(2)`, and n = 11’s `root(P_trump11, …)`.
`exact_sides.read_form` reads none of them, and neither does this slice.

### Why the Stack Is Not Ported

The 25 October assessment (think-vt31) found 39 conflicting files in #403 and 59 in
#435. Main had run 11 more adoption passes and re-housed 15 of the stack’s counts.
The stack’s builder also refuses any adopted house that is not rational, so carrying it
forward would mean porting about 4,700 lines of register tooling.
The owner chose a fresh pull request.
The stack’s four design questions resolve as follows:

| Decision | Resolution |
| --- | --- |
| D1, notation | Main’s: `polynomial_text`, and `root(p, low, high)` with `p` bound to that text |
| D2, coverage | Records keep what `adopt_houses` writes; the register holds the derived facts |
| D3, `algebraic_source` | Not added. Each entry’s `stated_by` and its bases do that job, in the register |
| D4, storage | `sqpack.retained_json`, one record per line, no gzip |

What comes over is the idea of a register of decided facts, and n = 83’s polynomial.
That polynomial was measured again here from the same pinned picture, whose bytes still
match the 5 October digest, and not copied from the stack.
The catalogue view comes over in a later slice, rebuilt from this register.
Left behind: derived fields on 307 records, `algebraic_source`, gzip storage, the
per-pass prior archives, the 1,239-line SVG extractor and the stack’s validation
selector repairs, all measured against a surface main has since replaced.

## Design

### The Register

`exact-side-register.json` is a softschema record
(`packing.squares:ExactSideRegister/v1`, `exact-side-register.schema.yaml`) holding one
entry per fact, ordered by count and then by subject:

| Field | Holds |
| --- | --- |
| `n`, `subject` | `house` (the case’s verified upper bound is this side), `staged-house` (a validated side the house rule names, adoption staged), or `configuration` (the side of a named configuration that is not the house) |
| `configuration` | For a configuration, what it is, in one sentence |
| `stated_by` | The results with their kind and rungs, the source key and the evidence |
| `degree`, `polynomial` | The degree, and the minimal polynomial in `polynomial_text` notation, or null when it is held by reference |
| `reference`, `measured` | For a large polynomial: the pinned asset and its custody record, and the facts measured from it, with the receipt |
| `form`, `interval` | The side written as a case record writes it (`root(p, low, high)`, or the closed form of a quadratic), and its interval with a `basis` |
| `irreducible` | `decided`, `measured` or `reported` |
| `house` | The house’s results, and the side’s exact order against it (`is`, `below`, `above` or `undecided`) with the gap |
| `staged` | For a staged house, the bead that owes its adoption and why it waits |

A basis says how far the record checked the fact.
`decided` means the register’s check decides it on every run.
`measured` means it was decided once from the pinned asset, with a retained receipt.
`reported` means it is the source’s claim, not checked here.

### Deciding a Side

The check decides irreducibility over Q with SymPy’s factorization over Z, the route
T-193’s and T-244’s reviews used.
It decides isolation with Descartes’ rule of signs on the interval’s Möbius transform,
in exact integer arithmetic.
One sign change means exactly one root, and a piece with more is bisected until each
piece decides. Measured on 25 October, the 22 inline polynomials (degree 2 to 41) decide
in a quarter of a second.
Main’s Sturm route takes 14 s for T-193’s sixteen alone, 10 s of it at degree 41, which
is why the register does not lean on it.
Each `form` is written as `exact_sides.form` writes it, 40 places, doubled where they do
not isolate the side, and the tests hold the two writers to the same text up to degree
24\.

The two large polynomials are not decided on each run:

- **s(29), degree 7213.** The 87 MB archive stays outside Git (OR-18). The register
  copies the facts `release.json` measured (7,214 coefficients, a 325-digit leading
  coefficient, height 5,074 digits) and the source’s Krawczyk enclosure of the side, as
  `reported`. It decides that T-195’s rational house lies inside that enclosure, so the
  order is `undecided`.
- **n = 83, degree 672.** The Kingbird retention policy keeps no SVG.
  `devtools.kingbird_root_polynomial` fetches the picture, refuses bytes that do not
  match the pinned digest, and parses its `Root[…, 27]`. It measures the polynomial (673
  coefficients, primitive, height 724 digits) and isolates the one root within 10⁻⁹⁹ of
  the printed side by Descartes’ rule, in about 80 seconds with the fetch.
  It writes a receipt beside the pictures receipt.
  The register holds that root below the rational house by 9.635 × 10⁻²⁰.

### The Check

`--check` rebuilds the register from its inputs, deciding as it goes, and compares the
result entry by entry with the committed file.
It also checks that the inputs agree where two of them state one side:

- a house’s form reads back as its record writes it;
- the record’s reported `algebraic_degree` and `minimal_polynomial` match;
- T-193’s ledger states the same side as the record at its six houses;
- T-244’s packet and ledger state the same polynomial, and the ledger writes the same
  form;
- s(29)’s copied facts match `release.json` and the Krawczyk box;
- n = 83’s receipt measures the pinned picture and the record’s degree.

It runs as the records-tier step `exact-side register is current`, in about two seconds.
When a house moves, for example when think-ot5c adopts a staged T-193 count, the step
fails and names `--update`, and the adopting pull request regenerates the register.

## Implementation Plan

### Slice 1: The Register (This Pull Request, think-vgsw)

- [x] `devtools.exact_side_register`: sources, decisions, `--update`, `--check`, a
  table.
- [x] The register and its schema, with 24 entries: ten houses, nine staged houses and
  five configurations (29, 83, 172, 204, 263).
- [x] `devtools.kingbird_root_polynomial` and n = 83’s receipt.
- [x] The records-tier step, the schema corpus, tests and an integrity-ceremony entry
  for the one download boundary.
- [x] Release bookkeeping for the data path and the paper inputs the step touches.

### Later Slices

Each has a bead under the epic.
The prices are this session’s measurements and estimates.

| Slice | What it adds | Price |
| --- | --- | --- |
| 2. Stated polynomials | The sixteen houses in older notations; the catalogue polynomials in the reported lane (11, 17, 28, 37, 39, 41, 69, 87, 128, 205, 235, 300, degree 5 to 83); T-120 to T-123’s reported roots (102, 106, 152, 177); superseded algebraic certificates such as T-174’s at 302 | About 2 agent-hours; the twelve catalogue polynomials decide in 1.5 s (SymPy and Descartes, measured) |
| 3. Every count | Each remaining house as a degree-1 fact by reference to its record, and the numeric gaps at 55 and 71 as explicit absences, so the register covers 1 to 324 | About 2 agent-hours, a few seconds of check |
| 4. n = 83 completed | Irreducibility by factor-degree patterns modulo primes, the count of real roots below the side (Root index 27, think-chsu), and the 673 coefficients as a derived fact if the owner approves | About 3 agent-hours and a few CPU-minutes |
| 5. s(29) from its archive | The archive fetched against its digest, the polynomial streamed, its facts re-measured, and the sign change across the enclosure decided exactly | About 2 agent-hours and under 10 CPU-minutes; independent of think-10m1 |
| 6. The site catalogue | A page of each count’s exact facts in MathML, with no-JavaScript access, rebuilt from the register | About one agent-day, inside the site’s page budgets |

## Testing Strategy

`packing/tests/test_exact_side_register.py` holds the decision route to known answers:
`s^4 + 1` irreducible though it factors modulo every prime, a reducible quartic, two
roots 10⁻⁶⁰ apart told apart by bisection, and an end that is a root.
It checks Descartes’ count against SymPy’s real-root count, an independent route, at
every inline polynomial, and the writer against `exact_sides.form` up to degree 24. It
holds the committed register to its inputs, and refuses a tampered degree, polynomial,
interval or subject, a staged count the selection no longer stages, and a receipt that
disagrees with the record.
The parser of n = 83’s picture runs on a small synthetic `Root` fixture, which also
shows the refusal of bytes that are not the pinned ones.

## Rollout Plan

One draft pull request against main with the `project` label and S2. Hosted CI is the
gate. The register changes no published page, so the papers take a no-change record and
the data pin moves once.

## Open Questions

- Should slice 3 list every count, rational houses included, so the register is the one
  place a reader finds any count’s exact side?
  The alternative is to keep it to algebraic facts and leave rational houses to their
  records.
- Should n = 83’s 673 coefficients, 343 KB of text, be retained as a derived fact, as
  the Kingbird retention policy allows for facts, so that the catalogue can print them?

## References

- [#811](https://github.com/jlevy/squares/issues/811), the tracker; #403 and #435, the
  superseded stack, and the handoff on #435’s branch
  (`docs/project/handoffs/handoff-2026-10-10-polynomial-pr-stack.md`).
- [epistemics.md, Result Kinds](../../../../epistemics.md#result-kinds) for the exact
  side kind;
  [development.md, Retained JSON Is One Record per Line](../../../../development.md#retained-json-is-one-record-per-line).
- `packing/devtools/exact_sides.py`, `packing/devtools/select_houses.py` and
  [result-import.md, The House Rule](../../../../packing/campaign/result-import.md#the-house-rule).
- [The frontier README’s section on the register](../../../../packing/frontier/README.md#the-exact-side-register)
  and the n = 83 measurement in the
  [known-best packings README](../../../../packing/resources/web/known-best-packings/README.md#the-degree-672-polynomial-measured-25-october).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
