---
softschema:
  contract: squares.exact_paper_print:Experiment/v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
  envelope: experiment
experiment:
  id: exp-001
  hypotheses:
  - H-001
  measurement: experiments/exp-001-layout.json
  physical_measurement: experiments/exp-001-physical.json
  correctness: passed
  decision: baseline
  judgment: The dated PDF retains its checked content but has approximately 5.40-point summary
    data; portrait preflight identifies 150 pixels of exact-form-table overflow.
---
# Dated Print Baseline

The full raw receipts are retained beside this observation.
The HTML is the preserved 1666 publication; the preflight is the new renderer working
tree before any print-CSS change, using pinned Chromium 151.0.7922.34 on macOS. Its
576-pixel printable viewport has 726-pixel document width: the five-column exact-form
table causes 150 pixels of horizontal overflow.
The predicted scale is 0.793388. All 1,428 display equations pass fit and no inline-math
overhang is observed.

The separate hosted PDF is from run 37888714875, artifact 11597149165. It has 546 Letter
pages (455 portrait and 91 landscape).
The sampled summary body measures 5.3963 points from raw text size multiplied by its PDF
transformation matrix.
This is dated evidence, and does not qualify later source heads.
Seven selected full pages were visually checked; all 673 n=83 coefficient strings match
the dated JSON payload.
Coverage limits in the raw receipt remain in effect: this is not a full independent
reconstruction of every coefficient vector from the PDF.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
