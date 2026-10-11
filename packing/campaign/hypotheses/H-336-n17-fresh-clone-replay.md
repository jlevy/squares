---
title: H-336 — every admitted certificate is hosted and one of each kind replays from a fresh clone
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-336
  kind: hypothesis
  claim: >-
    All objects named by the n17 hosted-data manifests (the 204 objects of the
    session-168 manifest, 2,167,361,631 bytes with Session 184's four tail objects
    included, and the other session-184 manifests) are
    published as release assets whose digests match the manifests, and a fresh clone of
    the repository with no other state fetches them with the documented command and
    replays one kernel certificate (W7) and one branch-and-bound certificate (A) end to
    end, in full mode, within 4 hours on one worker.
  lane: proof
  derived_from: [X-051]
  criterion:
    shape: determination
    metric: >-
      hosted_data check on every manifest against the published assets; the fetch log of
      the fresh clone; the full-mode receipts of the two replays with wall time and RSS.
    direction: >-
      Confirm when every digest matches and both replays pass within 4 hours. A missing
      asset, a digest mismatch or a failed replay refutes it and names the object.
    threshold: every manifest object present with matching digest; 2 of 2 replays pass; 4 hours.
  instrument: >-
    sqpack.hosted_data and the release tooling under plan-2026-10-01-release-assets-
    on-demand; the standing verifiers; a scripted fresh-clone replay recorded as a
    receipt.
  instrument_ready: true
  regime: >-
    The repository at the registration commit; a fresh container with the bootstrap
    steps of AGENTS.md; network access to the release assets; nothing copied from any
    existing host.
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: The upload (2.3 GB, blocked on egress from the cloud hosts and on an owner decision); about 3 hours of replay; 4 agent-hours.
  prereqs: []
  replication: false
  registered: '2026-10-09'
  notes: >-
    X-051's route J. Today no admitted n17 certificate can be verified from a fresh
    clone, because the objects exist only on hosts that no longer have them or on one
    Mac. OR-18 keeps bulk data out of Git; the manifests are in Git and the assets are
    not published. The owner's decision on hosting (think-jhgi) is the prerequisite;
    this record states the acceptance test for whatever hosting is chosen.
---
# H-336: Replay From Nothing

**Mechanism.** A proof whose certificates cannot be fetched is a proof by assertion.
The manifests already name every object by digest; publishing the assets and replaying
two of them from a clean container is the test that the rest can be replayed.

**Falsifier.** A missing or mismatched asset, or a replay that fails or exceeds the
ceiling.

**Expected information.** Replay portability, which the assurance ladder’s `C5` needs
and every reader needs sooner.

**Limits.** One replay of each kind is a sample; the full-collection replay is a
separate, larger obligation with its own CPU budget, and child receipts that pin parent
timing fields (the n11 pattern) would need rebinding, which the n17 receipts should
avoid.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
