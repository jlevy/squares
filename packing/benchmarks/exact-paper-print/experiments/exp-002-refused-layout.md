---
softschema:
  contract: squares.exact_paper_print:Experiment/v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
  envelope: experiment
experiment:
  id: exp-002
  hypotheses:
  - H-001
  measurement: experiments/exp-002-refused-layout.json
  physical_measurement: null
  correctness: failed
  decision: rejected
  judgment: The first layout candidate was refused for three overflowing exact-form fractions;
    the user then retired PDF packaging and selected complete web publication.
---
# Refused Print Candidate and Retired PDF Scope

The settled browser checked 6,012 cells and 1,428 display equations.
Document overflow, display-math overflow and inline overflow were zero, but the
exact-form cells at $n=68,292,105$ spilled 94.94, 26.05 and 15.45 pixels respectively.
The candidate was refused; no physical PDF was generated or accepted.
The raw receipt preserves the findings and their measurement limits.

The user subsequently requested the same complete content as a clean report on the
Papers page and stopped PDF packaging.
No second print trial will run.
`think-yon5` is canceled by that scope change; `think-ja78` owns responsive web
rendering, complete coefficient/source preservation and removal of PDF build
requirements. The stopped implementation is preserved in protected recovery evidence
outside scratch. This disposition does not turn the refused layout into a successful
readability result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
