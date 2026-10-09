---
softschema:
  contract: squares.exact_paper_print:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  status: enforced
  envelope: hypothesis
hypothesis:
  id: H-001
  claim: Contain the exact-form table and enlarge summary type so the complete PDF has readable
    table text without losing mathematical or source data.
  registered: '2026-10-09T07:33:30.584770+00:00'
  criterion: print_readability
  minimum_physical_font_pt: 8
  target_font_pt: 9
  maximum_overflow_px: 1
  current_records: 324
  historical_records: 175
  n83_coefficients: 673
  bead: think-yon5
---
# Readable Complete-Paper Tables

Register this criterion before changing print CSS. The retained baseline was measured
before registration and is observational evidence, not a retrospectively accepted trial.
Use the maintained renderer’s settled print preflight as the layout instrument; physical
font sizes come from a fresh hosted PDF, after applying each text transformation matrix.

The outcome is a deterministic determination: qualified, refused, or awaiting the hosted
PDF. A candidate qualifies only if summary data and headers measure at least 8 points in
the physical PDF (9 points is the CSS target), document and cell ink overflow stay
within the existing 1-pixel tolerance, and all display and inline math checks pass.
A legal named landscape page must be checked against its own printable measure.
Clipping or hiding cell ink cannot count as containment.

Independent guards retain the 324 current and 175 historical records, all coefficient
strings and source metadata, all 673 coefficients for n=83, and the four V0/C0 source
claims. Preserve the browser’s exact projection checks and inspect representative dense
summary, equation-continuation and long-coefficient PDF pages at full width.
A browser measurement alone cannot accept the physical PDF. No database admission, proof
label, byte cap, layout tolerance, CI ceiling or shared-paper CSS changes belong to this
trial.

Start with one bounded candidate: an explicit five-column print layout and 9-point
summary type. Split keyed tables are parked unless that candidate fails.
The outcome metric is physical readability; viewport shrink is a mechanism diagnostic,
not its substitute. This is not a timing or statistical performance claim.

## Candidate Plan Clarification, Before CSS Edits

At 2026-10-09T07:53:17.556514+00:00, the extended cell baseline identified an additional
ordinary six-column table: 594.28-pixel table width within a 544-pixel wrapper.
The same first candidate contains both ordinary-table causes, keeping explicit column
allocation for the five-column exact forms and the 9-point summary target.
The physical outcome, content guards, named-page measure and 1-pixel tolerance remain
those registered above.
No candidate CSS had been edited or measured when this clarification was recorded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
