---
title: H-349 — the kernel closes most of the flagged selector classes on no contributor roster
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-349
  kind: hypothesis
  claim: >-
    Of the 69 flagged, uncertified selector classes that devtools/census_n17_certified.py
    projects on the 60-entry ledger (in_ledger null), 34 are D4-identical to no pattern
    on a contributor roster (issue 472's twelve masks, issue 413's 38 rows, issue 358's
    C1 and C2). At least 28 of those 34 close under
    devtools/check_n17_subpattern in mode A with SW9's adaptive rows within 30 minutes of
    production each, with certificates the standing kernel verifier passes in full.
  lane: proof
  derived_from: [X-052]
  criterion:
    shape: determination
    metric: >-
      Per class: arity, wall cells, best float penetration from the selector receipt,
      producer outcome, production wall time, certificate size, full-mode verdict; the
      census consumer's marginal orbits after each admission, counted against whatever
      H-341, H-342 and H-332 have admitted by then.
    direction: >-
      Confirm when at least 28 of the 34 close within the ceilings with full-mode passes.
      Fewer than 28 refutes the claim, and the stall list, with the support diagnostics,
      says which flags are false or which crowds the kernel cannot reach. The net
      removal is recorded, not thresholded: projected exactly, all 34 remove 198 orbits
      after everything the contributors reported is admitted (2,343 to 2,145).
    threshold: 28 of 34 closures (at least 80 per cent); 30 minutes each; full-mode pass.
  instrument: >-
    devtools/census_n17_certified.py for the flag list and the marginals;
    devtools/check_n17_subpattern.py mode A with adaptive rows;
    devtools/verify_n17_kernel_certificate.py in full mode; devtools/diagnose_n17_flag.py
    on every stall.
  instrument_ready: true
  regime: >-
    n = 17; the H-266 cover at U; the 69 classes as the census tool lists them on main at
    6a0499ba4, less the 35 whose D4 orbit contains a pattern on the issue-472, issue-413
    (38-row) or issue-358 rosters; the remaining 34 frozen by canonical mask before the
    first launch; one production run per class; closures admitted only after a
    full-mode pass.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: >-
    At most 17 CPU-hours of production (34 classes at up to 30 minutes each) plus
    full-mode verification at the issue-472 timings; about 6 agent-hours for the freeze,
    launches and admission rounds.
  prereqs: [H-267, H-341]
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-052's direction 9, re-scoped the same day after the W2 review of X-052. The census
    tool's flagged projection is the standing list of selector flags without
    certificates. As first registered, the claim covered all 69 with a conjunct that
    their admission, net of H-341 and H-342, remove at least 1,000 further orbits; the
    review projected the overlap exactly and found that conjunct reachable only if
    H-342 largely failed. 35 of the 69 are D4-identical to contributor patterns: 7 are
    issue-472 masks, 23 are H-342-eligible issue-413 rows, 4 are rows 1 and 2 or C1 and
    C2 (H-332's), and 1 is row 5. After issue 472's twelve and every H-342-eligible row
    the residue is 2,353 orbits, and all 69 take it to 2,145, a net of 208; after
    everything reported (2,343 orbits) the 34 classes on no roster remove 198. The 1,491
    orbits the 69 remove after H-341 alone (3,636 to 2,145) are mostly the patterns
    H-342 targets. The kernel's measured behaviour on wall-anchored arity-8 and 9 crowds
    this week makes the 34 worth running once as a batch, with every stall classified
    rather than retried.
---
# H-349: Run the Standing Flags Through the Engine That Works

**Mechanism.** A selector flag is a sub-pattern the float search cannot place; the
kernel certifies the ones whose infeasibility is pairwise-visible, which this week’s
twelve-for-twelve on wall-anchored crowds says most arity-8 and 9 flags are.
The census tool already projects what each flag would remove.
Thirty-five of the 69 standing flags are already on a contributor roster: 7 are H-341’s,
23 are H-342’s, 4 are H-332’s, and one is issue 413’s row 5, an interior crowd left to
the branch and bound.
This hypothesis takes the 34 on no roster.

**Falsifier.** Fewer than 28 of 34 close within the ceilings.

**Expected information.** The kernel’s stall fraction on the flags no contributor has
run, at most about 200 orbits of residue (198 if all 34 close after everything reported
is admitted), and a classified stall list for the rest.

**Limits.** The net removal depends on what is admitted first and is recorded at each
admission, not assumed; a flag that stalls is not shown false.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
