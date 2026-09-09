---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-005
title: First hosted parameter-only comparison
kind: comparison
hypotheses: [H-003]
measurements:
  - runs/ci-34270137119/startup-1280.json.gz
  - runs/ci-34270137119/startup-390.json.gz
correctness: failed
judgment: The observations pass the registered instrumentation checks, but the desktop confidence interval fails the speed criterion and the same candidate fails independent geometry checks. Retain both widths without replacing observations or adding pairs.
---
# First Hosted Parameter-Only Comparison

[Pages dispatch 34270137119](https://github.com/jlevy/squares/actions/runs/34270137119)
tested the clean source `25e66d7bfe4170a6e2166b95df9ff0f407606629` on a dedicated Linux
runner. Its twelve interleaved pairs at each width use the retained `33cd4760` control
and the same prepared candidate as the browser correctness jobs.
The [candidate HTML](../fixtures/candidate-25e66d7b.html.gz) and
[measurement controls](../runs/ci-34270137119/controls.json.gz) are retained.
Artifact identity and the complete pairing were checked before interpreting results.

All forty-eight observations are instrument-valid, including the ten-percent sampler
bound. The desktop interval does not establish the registered improvement; the mobile
interval does. The hypothesis requires both widths, so its numerical result is rejected.
The candidate also fails the independent geometry experiment, exp-006. Neither the
mobile result nor a later repaired candidate replaces this result.

The raw trace distinguishes late issuance of font promises from decoding time.
Interactive values appear before the eight static panel labels, which are submitted in
the later whole-document typesetting batch.
The next candidate must address that scheduling path and the geometry failures before a
new confirmatory comparison.
H-005 registers that comparison separately.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
