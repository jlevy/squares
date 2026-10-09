---
title: H-349 — the kernel closes most of the standing flagged, uncertified selector classes
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-349
  kind: hypothesis
  claim: >-
    At least 56 of the 69 flagged, uncertified selector classes that
    devtools/census_n17_certified.py projects on the 60-entry ledger (in_ledger null;
    2,163 orbits and 16,900 states if all closed) close under devtools/check_n17_subpattern
    in mode A with SW9's adaptive rows within 30 minutes of production each, with
    certificates the standing kernel verifier passes in full; and their admission, net of
    overlap with H-341 and H-342, removes at least 1,000 further orbits from the residue.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Per class: arity, wall cells, best float penetration from the selector receipt,
      producer outcome, production wall time, certificate size, full-mode verdict; the
      census consumer's marginal orbits after each admission, with the overlap against
      H-341 and H-342 admissions counted, not assumed.
    direction: >-
      Confirm when at least 56 of 69 close within the ceilings and the net removal is at
      least 1,000 orbits. Fewer than 56 refutes the claim and the stall list, with the
      support diagnostics, says which flags are false or which crowds the kernel cannot
      reach; a net removal under 1,000 with 56 closures refutes only the overlap
      estimate.
    threshold: 56 of 69 closures; 30 minutes each; full-mode pass; at least 1,000 net orbits.
  instrument: >-
    devtools/census_n17_certified.py for the flag list and the marginals;
    devtools/check_n17_subpattern.py mode A with adaptive rows;
    devtools/verify_n17_kernel_certificate.py in full mode; devtools/diagnose_n17_flag.py
    on every stall.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; the 69 classes as the census tool lists them on main at
    6a0499ba4, frozen before the first launch; one production run per class; closures
    admitted only after a full-mode pass.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    Tens of CPU-hours at the issue-472 timings; about 6 agent-hours for the freeze,
    launches and admission rounds.
  prereqs: [H-267, H-341]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 9. The census tool's flagged projection is the standing list of
    selector flags without certificates; some overlap the issue-413 roster and the
    issue-472 batch, and some are the flags the uniform-row runs of Session 182 stalled
    on (flag 2 among them, diagnosed loss-limited on the west wall). The adaptive recipe
    and the kernel's measured behaviour on wall-anchored arity-8 and 9 crowds this week
    make the list worth running once as a batch, with every stall classified rather than
    retried.
---
# H-349: Run the Standing Flags Through the Engine That Works

**Mechanism.** A selector flag is a sub-pattern the float search cannot place; the
kernel certifies the ones whose infeasibility is pairwise-visible, which this week’s
twelve-for-twelve on wall-anchored crowds says most arity-8 and 9 flags are.
The census tool already projects what each flag would remove.

**Falsifier.** Fewer than 56 of 69 close within the ceilings.

**Expected information.** The kernel’s stall fraction on the current flags and about a
thousand orbits of residue, with a classified stall list for the rest.

**Limits.** Overlap with the contributor batches is measured after admission, not
assumed; a flag that stalls is not shown false.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
