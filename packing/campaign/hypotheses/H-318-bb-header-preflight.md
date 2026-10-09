---
title: H-318 — Original-Cell Joint-Certificate Header Preflight
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-318
  kind: hypothesis
  claim: Original-Cell Joint-Certificate Header Preflight
  lane: proof
  derived_from:
  - X-048
  criterion:
    shape: determination
    metric: n17-bb-header-preflight
    direction: criterion_met
    threshold: 'Primary BOTH exact retained C1/C2 manifests complete HEADER_ONLY_PASS with complete original-cell
      halfplane enclosure, all21 pair roster, complete shifted closed-angle chart and exact input custody.
      This is header-only computational scope, NEVER FULL/tree/trig verification or ordinary admission.
      Prospectively C2 is evaluated first: its individual HEADER_ONLY_PASS selects ONE bounded FULL C2
      replay even if separate C1 subsequently refuses; C2 refusal/resource exhaustion stops C2 acquisition/replay
      without unchanged retry. No actual header has yet been evaluated.'
  instrument: packing/devtools/check_n17_bb_header.py
  instrument_ready: true
  regime: 'Primary BOTH exact retained C1/C2 manifests complete HEADER_ONLY_PASS with complete original-cell
    halfplane enclosure, all21 pair roster, complete shifted closed-angle chart and exact input custody.
    This is header-only computational scope, NEVER FULL/tree/trig verification or ordinary admission.
    Prospectively C2 is evaluated first: its individual HEADER_ONLY_PASS selects ONE bounded FULL C2 replay
    even if separate C1 subsequently refuses; C2 refusal/resource exhaustion stops C2 acquisition/replay
    without unchanged retry. No actual header has yet been evaluated.'
  instance:
    axis: n
    point: 17
  priority: 1
  cost_estimate: 30s cooperative perheader; one C2 then one C1 phase, outerTERM60/KILL70, sampled4GiB
    currentRSS perliveprocess;1MiBcompressed/10MiBdecoded/4096usedrationalbits/1MiBoutput percase; externalTMP
    snapshot; no tree/trig assets.
  prereqs:
  - H-317
  replication: false
  notes: 'SoleAstra source mathematical CLEAR after NEW wrapper hardening: every original source-cell
    vertex lies left/on every declared edge; duplicates/zero edges refuse. Real pentagram regression demonstrates
    standing local positive turns plus set equality is insufficient and hardened wrapper refuses.23authorPASS5.24s
    and23independentROOTpeerPASS1.26s; Ruff/format/BasedPyright0. Earlier formatter startup interruption143/zeroassertions
    retained. Standing FULL checker untouched. Actual309 metadata positive current union21/148 but bothzero95-tail;
    potentialonly.'
  registered: '2026-10-07'
---
# Original-Cell Joint-Certificate Header Preflight

Primary BOTH exact retained C1/C2 manifests complete HEADER_ONLY_PASS with complete
original-cell halfplane enclosure, all21 pair roster, complete shifted closed-angle
chart and exact input custody.
This is header-only computational scope, NEVER FULL/tree/trig verification or ordinary
admission. Prospectively C2 is evaluated first: its individual HEADER_ONLY_PASS selects
ONE bounded FULL C2 replay even if separate C1 subsequently refuses; C2 refusal/resource
exhaustion stops C2 acquisition/replay without unchanged retry.
No actual header has yet been evaluated.

SoleAstra source mathematical CLEAR after NEW wrapper hardening: every original
source-cell vertex lies left/on every declared edge; duplicates/zero edges refuse.
Real pentagram regression demonstrates standing local positive turns plus set equality
is insufficient and hardened wrapper refuses.23authorPASS5.24s
and23independentROOTpeerPASS1.26s; Ruff/format/BasedPyright0. Earlier formatter startup
interruption143/zeroassertions retained.
Standing FULL checker untouched.
Actual309 metadata positive current union21/148 but bothzero95-tail; potentialonly.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
