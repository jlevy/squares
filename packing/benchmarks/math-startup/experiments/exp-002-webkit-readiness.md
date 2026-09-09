---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-002
title: Intermediate prepared page exposes a pending WebKit relation
kind: geometry
hypotheses: [H-001]
measurements:
  - runs/webkit-readiness-failure.json.gz
correctness: failed
judgment: Reject this intermediate runtime; the geometry guard caught visible math before a required font transfer completed.
---
# Intermediate Prepared Page Exposes a Pending WebKit Relation

The real-transfer control held thirteen math-font requests.
Geometry stayed within its tolerance, but a lone `\ge` became visible too soon.
The complete raw diagnostic is retained without alteration.
This is an exploratory failure, not a complete matrix or a normal-startup timing
measurement.

The input was `/tmp/squares-prepared-candidate-final.html`, stamped
`DRAFT v0.2.4-db81233e`. Its bundled runtime matched KPress `206d585` byte for byte.
It contained the then-uncommitted geometry, default-figure visibility, and native/print
fallback changes, before the later heat-map settlement and bullet adjustments.
This earlier probe did not yet attach automatic browser-version and process provenance;
the final probe does.
The missing provenance is not reconstructed as measured data.

The diagnostic returned `check=true` and an empty font-list load result while the
relation’s fallback transfer was pending.
A later minimal fixture also reproduced an incorrect single-family `check()` result.
KPress is being changed to await actual single-family load promises, with required-font
rejection and timeout still fatal.
`think-zh5u` tracks the fix.
The final candidate must pass the unchanged real-transfer visibility guard before
latency is measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
