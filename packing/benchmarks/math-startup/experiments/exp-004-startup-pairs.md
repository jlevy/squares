---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-004
title: First paired startup comparison with full anchor sampling
kind: comparison
hypotheses: [H-002]
measurements:
  - runs/startup-pairs-1280.json.gz
  - runs/startup-pairs-390.json.gz
correctness: passed
needs_review: true
judgment: The registered numerical criterion passes in this instrumented regime, but differential observer overhead and pre-paint text measurements require an instrumentation audit before a reader-latency claim.
---
# First Paired Startup Comparison with Full Anchor Sampling

The twelve interleaved pairs at each width use the frozen deployed `33cd4760` control
and prepared `dc2eb681` candidate with KPress `345b9eb`. All delegate browsers and heavy
checks were idle throughout both windows.
Both complete reports are retained, including all observations and source/process
provenance. A later process inspection found unrelated CPU-heavy work on the shared Mac.
Delegate idleness did not establish the intended isolated host regime.
No invalid observations were removed and no pairs were added after looking at the
result. The independent correctness matrix passed before timing.

The sampling overhead is material and differs between arms: full-page anchor discovery
and range measurements do more work on the prepared DOM. Some recorded text movement
also starts before first contentful paint, so it cannot be described as entirely visible
reflow.
These limitations do not alter the raw data, but they prevent a clean attribution
of the primary timing difference to ordinary reading.
The next bounded investigation must separate visible prose-font movement from pre-paint
geometry and assess the observer’s cost.
Preserve this result even if a corrected probe changes the conclusion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
