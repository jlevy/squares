---
softschema:
  contract: squares.math-startup.exploration.v1
  schema: ../schemas/exploration.schema.yaml
  status: enforced
id: X-002
title: Separate parameter latency from layout diagnostics
proposes: [H-003]
---
# Separate Parameter Latency from Layout Diagnostics

The complete paired results in exp-004 meet the numerical threshold, but the observer
does substantially more range and layout work on prepared markup.
Its largest movement readings also begin before first contentful paint and concern
offscreen text. CSS visibility does not establish whether font-blocked ink has painted.
Those ranges are useful diagnostics, not a direct measure of visible page reflow.

A later process inspection found unrelated CPU-heavy work on the shared Mac during the
local window. Delegate idleness alone did not establish an idle host.
Do not terminate unrelated tasks or treat those observations as an isolated comparison.

The smaller mode observes the same fourteen correct, exposed parameters without
discovering prose, captions, or all-page ranges.
It stops sampling when that complete set first becomes readable and still checks final
correctness after settlement.
Retained controls must reject missing math and hooks and detect a known delay.
A fresh CI job provides the host for confirmation, with no other validation process
inside that runner. Both files are local, with fresh browser processes and uncontrolled
OS caches. The job retains its exact control and candidate HTML alongside the reports.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
