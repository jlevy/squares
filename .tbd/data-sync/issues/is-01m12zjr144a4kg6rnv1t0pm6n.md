---
type: is
id: is-01m12zjr144a4kg6rnv1t0pm6n
title: "[epic] Make the packing atlas records say what is known, and how we know it"
kind: epic
status: open
priority: 1
version: 14
labels: []
dependencies: []
child_order_hints:
  - is-01m12x4038aw59q7c3zp2xb07p
  - is-01m12vwrn7p99ehaxxasqkh9c5
  - is-01m12y4vf6c8t5mb3f268nm1kx
  - is-01m12p9067k1y4fp2bqb9zd1f2
  - is-01m12vws2trz68we4d26g56pr4
  - is-01m12vwsf0abpedfd6843zg6nj
  - is-01m12vxez6kp1jmed6feg61eam
  - is-01m12vxegxtck202jga5gjbkk4
  - is-01m12zhp8rh3dfdnyecaa0ezww
  - is-01m12vxfaqfj6stwvg6rx70p91
  - is-01m12vxft8bexsm4b4vkbakb6p
  - is-01m12y4vwnsqpm4se8xwqmy8dm
created_at: 2026-08-28T01:26:06.101Z
updated_at: 2026-08-28T01:33:56.053Z
---
The atlas records are the repository's representation of best-known knowledge about s(n), and downstream work reads them that way. A session spent building the n=1..100 composite figure surfaced a connected set of defects in HOW those records encode knowledge. None of them is an upstream problem: the retained sources are sound. Every defect is in our transcription, our schema, or our tooling.

THE ROOT DEFECT (think-18mu)

Every optional field is typed 'value or null' with no vocabulary for why a value is absent. Null collapses at least five states: transcribed from the source; MISSED in transcription; the source is silent; genuinely unknown to mathematics; not applicable. A reader cannot tell them apart, so absence of evidence renders as evidence of absence. Two live errors came directly from this and both reached a published figure before anyone noticed.

WHAT WENT WRONG CONCRETELY

- n=54 had exact_form: null while Kingbird prints s = 7 - (1/2)sqrt(2) + sqrt(1+sqrt(2)). It is the only n<=100 entry rendered as a multi-line block rather than the single-line pattern the transcriber handled. Verified to the witness's full 29 digits, and independently re-derived from the decimal alone by a second method. FIXED in the data.
- n=11 had rigid: null while three retained sources call it rigid; a migration commit flipped it. FIXED in the data.
- rigid is non-null exactly where catalogue_pictured is true, so false means 'the catalogue did not say' while READING as 'not rigid'. Taken literally the records claim n=1 is not rigid: one unit square exactly filling a 1x1 container. n=4 and n=9 likewise; n=16..100 are null though equally trivially rigid.
- algebraic_degree is absent for all 84 records that carry an exact form, though every one is derivable from the radical in seconds (65 rational, 18 quadratic, 1 quartic). n=40 is degree 2, s^2-8s+8=0, which is evident by inspection.
- Nothing re-reads any of these fields from the retained sources, so a second transcription miss would be equally invisible.
- Witness coordinate precision is decorative: the coordinates were generated from the rounded side, so usable digits are 30-100, not the apparent 100+.

CHILDREN, roughly in dependency order

  think-18mu  P1  provenance vocabulary for every optional fact -- do this first, the rest encode against it
  think-k5z2  P1  reparse exact forms and degrees from the catalogue so misses are caught
  think-kj6n  P1  derive and record the 84 missing algebraic degrees
  think-d1qd  P1  rename claim.assurance; it reads as a claim about the mathematics
  think-n3j4  P1  n=11 rigid regression -- value restored, the audit that would have caught it is not written
  think-de1s  P2  split rigid into catalogue transcription and first-party computed property
  think-ah2c  P2  retrieve the Ellsworth rigid-packings page, which the repo cites but does not hold
  think-fsi5  P2  sound one-sided escape screen; certifies play for 25 records, cannot certify rigidity
  think-wy6z  P2  re-refine witness sides at 500-2000 digits; unblocks exact recovery for n=29, 55, 71
  think-ecqk  P2  n=68/69 witness geometry is self-inconsistent at 1e-8 and blocks all contact work
  think-je8y  P2  n=29: eliminate the retained six-equation system for an exact side
  think-93u2  P2  render_research_tables flattens smart quotes in a doc it regenerates

HANDOFF NOTES

Read docs/project/specs/active/spec-2026-08-27-composite-figure-fact-sourcing.md first. It records which field backs each statement in the figure, how to verify one by hand, and the two transcription traps.

The governing rule: report what is known about the packing, never how this repository stores it. The figure was wrong precisely where it broke that rule.

Do not treat a failed integer-relation search as evidence a value is not algebraic. The same search that finds nothing for n=29 also finds nothing for n=51, whose degree-12 polynomial we hold. It measures our retained precision, nothing more.

Two point fixes already landed in the data (n=54 exact_form, n=11 rigid). The composite figure derives rigidity from perfect-square geometry plus catalogue annotation rather than trusting the stored flag, and labels the badge 'rigid (established)' so absence reads as not-established. That is a mitigation in the renderer, not a fix in the records.

## Notes

START HERE: explorations/packing/atlas/known-best/FIGURE-PLAYBOOK.md

It sits next to the figure it describes and covers the rebuild command, where
each fact on the figure comes from, how to verify one by hand, the two
transcription traps, and the five steps to reach n = 200.

CONVENTION NOTE for think-kj6n: rationals have algebraic degree 1, not 0. The
minimal polynomial of 2 is s - 2 and [Q(a):Q] = 1; a degree-0 polynomial is a
nonzero constant with no root, so no number has degree 0. The integer sides look
degree-less but are degree 1. See that bead's notes for the full distribution and
the open display question.
