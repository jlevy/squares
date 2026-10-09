---
title: H-276 — exact current-ledger n17 residue partition
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-276
  kind: hypothesis
  claim: >-
    The retained current-ledger stratifier partitions all surviving states of the
    unique-state n17 cover into disjoint D4 orbits and composition/distance strata,
    reproducing the standing certified census of 36784 states in 4685 orbits under
    58 admitted entries, with the endpoint surviving.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: exact_admitted_census_and_complete_partition
    direction: criterion_met
    threshold: All roster and stratum sums equal the independent census; endpoint survives.
  instrument: >-
    packing/devtools/stratify_n17_certified_residue.py, checked by the standing
    devtools.census_n17_certified count and independent synthetic orbit enumeration
    in packing/tests/test_stratify_n17_certified_residue.py. Freeze the source commit
    before running the real ledger, and retain the complete orbit roster.
  instrument_ready: true
  regime: >-
    Session184 on macOS, project Python3.14.7, one process. Ledger is
    packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml
    as committed at f3a13e3a217d2f8c17e96570c31ca1c9eda66c63, design
    ring-3-voronoi-8-tabbed-unique at U=1169/250. No optional producer receipts are
    supplied in the first control; every attempt diagnostic therefore remains
    untested_in_supplied_receipts. No missing hosted object is inferred to exist.
    Two-minute measurement ceiling, no exclusion search or admission mutation.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: Less than two minutes for one deterministic population control.
  prereqs: [H-266, H-267]
  replication: false
  registered: '2026-10-07'
  notes: >-
    This is instrument readiness for the actual admitted residue, replacing historical
    hypothetical arity-eight selector populations as a queue input. Six synthetic
    controls passed before registration, including rejection of an endpoint exclusion
    and conservative receipt joins. A pass establishes a partition under the already
    admitted ledger; it adds no geometric exclusion, bound, capture theorem or closure
    rate. A mismatch or refusal invalidates use of this roster until separately reviewed.
---
# H-276: Current Admitted Residue Partition

BC-432 needs the actual surviving population before Astra selects fresh tail work.
Historical selector strata are useful background but do not define the current
4,685-orbit queue. This control accepts only a complete partition agreeing with the
standing census.

The full roster, exact population and endpoint check are the output.
Without explicitly supplied, properly identified attempt receipts, the output does not
establish which orbits have ever been tested or why a producer stalled.
Hosted nodes are unnecessary for this census and remain necessary for certificate
replay.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
