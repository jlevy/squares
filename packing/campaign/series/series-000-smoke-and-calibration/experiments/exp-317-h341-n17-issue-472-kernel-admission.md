---
title: "exp-317 — The twelve kernel certificates of issue 472: clean replay, Rust parity, custody and admission"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-317
  series: series-000
  title: The twelve n17 sub-pattern kernel certificates of issue 472, re-proved in full from a clean
    worktree under the listed standing verifier, checked by the Rust verifier, hosted under the ledger's
    data manifest and admitted to the census ledger
  date: '2026-10-09'
  hypotheses:
  - H-341
  tier: confirmatory
  subject:
    label: The twelve kernel certificates wand125 offered in issue 472 (eleven in its body, m4657489 in its
      first comment), D4 masks 214101, 14353473, 983396, 3869440, 5707072, 6177056, 7815200, 1000708,
      935012, 7799616, 5116178 and 4657489, on the unique-state 24-cell cover at U = 1169/250; their 24 seed
      and node objects at the sizes and SHA-256 digests that the contributor's two HostedData/v1 manifests
      pin (wand125/square-packing releases data/n17-kernel-batch1-v1 and data/n17-kernel-batch2-v1;
      411,682,476 bytes).
    engine: devtools.verify_n17_kernel_certificate in full mode, file blob 1ad706c21 (the kernel-streamed
      listing), from a clean worktree at 3213d651b; the n17_kernel_verify crate (n17-kernel-verifier) for
      parity on the same objects; devtools.hosted_data for custody; devtools.census_n17_certified and
      devtools.stratify_n17_certified_residue for the joins, the endpoint control and the counts
    engine_commit: 3213d651b880d7768bce8506efaf75c2089aeb4f
    assurance: verified
    method: exact-algebraic
    host_system: Linux x86_64 remote session container, 4 vCPU and 15 GiB, project Python 3.14.7, four
      verifications at a time
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: The census's endpoint-state control, which refuses an entry any D4 image of which lies in the
      family's state and must report the endpoint surviving. The contributor's own receipts (dirty true at
      the wrapper revision 14c25146, one hand-edited directory field per verification receipt) are kept as
      disclosed and admit nothing. A forward replay under main's unlisted kernel verifier (blob be8135f6e
      at 6a0499ba4) is recorded for the reader and admits nothing either.
    candidate: Each certificate's seed and node, fetched by digest, re-proved in full by the listed standing
      verifier from the clean worktree and checked a second time by the Rust verifier on the same objects.
    runs_per_condition: 1
    interleaved: false
    operator: claude-opus-5.5, a coordinator with sub-agent replay lanes in detached worktrees
    entry_point: packing/devtools/verify_n17_kernel_certificate.py
    command: 'With the 24 objects at their manifest paths in the clean worktree at 3213d651b, from its
      packing/: /usr/bin/time -v uv run --frozen --all-extras --group dev python -m devtools.verify_n17_kernel_certificate
      ../packing/campaign/explorations/X048-session-168-pilots/certificates/w125-k-mMASK --output OUT/w125-k-mMASK.json,
      four at a time; the same command from a worktree at 6a0499ba4 for the forward replay; target/release/n17-kernel-verifier
      CERT --output OUT/rust/w125-k-mMASK.json from packing/n17_kernel_verify at 6a0499ba4; then, in the
      admission checkout, python -m devtools.census_n17_certified and python -m devtools.stratify_n17_certified_residue.'
    budget: One full verification per certificate under each verifier, about 1.9 CPU-hours for each Python
      pass at the contributor's timings (6,794 s serial, longest 1,618 s); a Python verification still running
      at 5,400 s is recorded as incomplete and admits nothing. No producer re-run, no parameter change, and
      no retry of a refused certificate.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-317-issue-472-kernel-admission
    commit: 3213d651b880d7768bce8506efaf75c2089aeb4f
    dirty: false
  results: []
  verdict:
    decision: in-progress
    primary_criterion: H-341's threshold, unchanged; 12 of 12 certificates pass C1 to C4 below and the census
      after admission reports 3,636 orbits and 28,528 states with the endpoint surviving and the distance-2
      stratum at 94 orbits and 736 states. A certificate that fails C1 to C4 is not admitted, and the others
      are still admitted and counted.
    reason: Registered before any replay result is recorded here; the criteria are H-341's, registered at
      2ed894325 (17:51 UTC) before the listed replay launched at 18:57 UTC.
  lease:
    expires: '2026-10-10T19:00:00Z'
    host: Claude Code remote session container (session 01EJe2szKBAKM2ieJVGNVeLj)
---
# exp-317: Admitting the Twelve Kernel Certificates of Issue 472

[H-341](../../../hypotheses/H-341-n17-issue-472-kernel-admission.md), direction 1 of
[X-052](../../../explorations/X-052-n17-status-survey-and-completion-plan.md), asks
whether the twelve kernel certificates of
[issue 472](https://github.com/jlevy/squares/issues/472) replay in full under a listed
verifier, agree with the Rust verifier, and leave the projected residue once admitted.
The contributor made them with this repository’s producer (`check_n17_subpattern`, mode
A) and passed them with the listed verifier blob `1ad706c21`. Their receipts carry
`dirty: true` at a wrapper revision and one hand-edited `directory` field each.
This round replaces those receipts as the admitted evidence; it does not re-run the
producer.

The projection was read-only and reproduced by two independent agents: admitting all
twelve to the 60-entry ledger takes the certified residue from 4,683 orbits and 36,768
states to 3,636 and 28,528, and the distance-2 stratum from 95 orbits (744 states) to 94
(736), through `m935012` alone.
Before any replay result, a projection-only census on a scratch ledger holding the
twelve as `pending` entries reproduced 3,636 and 28,528 from the contributor’s producer
receipts and the drafted manifest.
That is a check of the joins, not a result.

## Frozen Criteria

These restate H-341’s threshold; nothing below loosens it.

| Id | Criterion, per certificate unless stated | Instrument |
| --- | --- | --- |
| C1 | Custody: each object’s size and SHA-256 equal the contributor’s manifest and the repository manifest; after upload, the bytes the release serves equal both | `sha256sum -c`, `hosted_data check`, `hosted_data publish` (which downloads and compares every served asset) |
| C2 | Listed full pass: a receipt of schema `n17-certificate-verification/v1`, `verifier: kernel`, `status: PASS`, `mode: full`, `closed: true`; `provenance.files` names only `packing/devtools/verify_n17_kernel_certificate.py` at blob `1ad706c21`, `dirty: false`, revision `3213d651b`; `directory` the certificate’s repository path as the verifier wrote it; `certificate` the manifest’s seed and node; `cells` the declared class | the receipt, read by `census_n17_certified` |
| C3 | Rust parity: `n17-kernel-verifier` returns PASS on the same objects, with every receipt field equal to C2’s except `provenance`, `directory` and `seconds` | field comparison of the two receipts |
| C4 | Endpoint control: the census refuses no entry, and the endpoint’s state survives | `census_n17_certified` |
| C5 | Count, for the round: the certified line after admission is 3,636 orbits and 28,528 states, and the distance-2 stratum 94 orbits and 736 states | `census_n17_certified`, `stratify_n17_certified_residue` |

The forward replay under `main`’s blob `be8135f6e` is information.
Its verdicts are recorded beside C2’s, and a disagreement is a finding for the review
that would list that blob.
It does not block admission.
The verdict is `accepted` when all twelve meet C1 to C4 and C5 holds exactly.
Otherwise H-341 is refuted: the certificates that meet C1 to C4 are admitted and
counted, the others stay out of the ledger, and the record gives the census they leave.

## Procedure

1. **Custody.** Fetch both releases, check `SHA256SUMS`, the manifests’ sizes and
   digests, and `hosted_data check` on both manifests; recompute each seed’s content id.
   Done on 9 October against `main` `6a0499ba4`, with no problem found.
2. **Listed replay.** Place each seed and node at its manifest path in a clean worktree
   at `3213d651b`, where the verifier’s blob is `1ad706c21`, and run the verifier in
   full on each directory, four at a time, under `/usr/bin/time -v`. Running inside the
   worktree makes the receipt’s `directory` field the repository path with no edit.
3. **Rust parity.** Build `packing/n17_kernel_verify` at `6a0499ba4` and run it on the
   same twelve directories; compare each receipt with C2’s.
4. **Forward replay.** The same as step 2 from a worktree at `6a0499ba4`.
5. **Hosting.** Upload the 24 objects to `data/n17-x048-session-168-certificates-v1`
   with `hosted_data publish --manifest hosted/n17-issue-472-kernel-certificates.yaml`,
   and list the same 24 in the ledger’s data manifest,
   `packing/hosted/n17-x048-session-168-certificates.yaml`. The census reads one data
   manifest, so the objects go on that manifest’s release, as Tail A’s and Tail B’s did.
6. **Admission.** Commit each listed receipt as its certificate directory’s
   `verification.json` and the contributor’s producer receipt beside it as
   `producer-receipt.json`; add the twelve entries to
   [the ledger](../../../explorations/X048-session-168-pilots/certified-sub-patterns.yaml)
   under `kernel-streamed`; run the census and the partition and retain both.

## Layout

| What | Path |
| --- | --- |
| Listed receipt, the ledger’s `verification.receipt` | `packing/campaign/explorations/X048-session-168-pilots/certificates/w125-k-m<mask>/verification.json` |
| Contributor’s producer receipt, the ledger’s `receipt` | `packing/campaign/explorations/X048-session-168-pilots/certificates/w125-k-m<mask>/producer-receipt.json` |
| Seed and node, git-ignored and hosted | `packing/campaign/explorations/X048-session-168-pilots/certificates/w125-k-m<mask>/{seed,node}-<id>.json.gz` |
| Listed replay’s timing and logs | `results/exp-317-issue-472-kernel-admission/listed/w125-k-m<mask>.{time,stdout,stderr}`, `runner.log` |
| Rust receipts and parity | `results/exp-317-issue-472-kernel-admission/rust/w125-k-m<mask>.json`, `parity.json` |
| Forward replay | `results/exp-317-issue-472-kernel-admission/forward-be8135f6e/w125-k-m<mask>.json` and logs |
| Contributor’s verification receipts, as received | `results/exp-317-issue-472-kernel-admission/contributor/w125-k-m<mask>/verification.json` |
| Custody inventory | `results/exp-317-issue-472-kernel-admission/custody.json` |
| Census and partition after admission | `results/exp-317-issue-472-kernel-admission/census.json`, `partition.json` |

The `results/` paths are under
`packing/campaign/series/series-000-smoke-and-calibration/`.

## Results

To be recorded when the replays finish.

| Certificate | #413 row | Listed replay | Rust parity | Forward replay | Alone | Margin |
| --- | --- | --- | --- | --- | --- | --- |
| `w125-k-m214101` | 25 |  |  |  |  |  |
| `w125-k-m14353473` | 36 |  |  |  |  |  |
| `w125-k-m983396` | 31 |  |  |  |  |  |
| `w125-k-m3869440` | 35 |  |  |  |  |  |
| `w125-k-m5707072` | 37 |  |  |  |  |  |
| `w125-k-m6177056` | — |  |  |  |  |  |
| `w125-k-m7815200` | 29 |  |  |  |  |  |
| `w125-k-m1000708` | 30 |  |  |  |  |  |
| `w125-k-m935012` | 23 |  |  |  |  |  |
| `w125-k-m7799616` | 34 |  |  |  |  |  |
| `w125-k-m5116178` | 24 |  |  |  |  |  |
| `w125-k-m4657489` | 38 |  |  |  |  |  |

## Disclosures

- **The listing’s version.** The ledger’s `kernel-streamed` listing records commit
  `601bbf110`, on PR 307’s branch.
  The replay commit `3213d651b` is on `main` and holds the same blob, `1ad706c21`. As
  for every listing, the census checks the receipt’s verifier path and uncommitted flag
  and does not resolve the version.
- **The producer receipts.** The ledger’s `receipt` for each entry is the contributor’s
  producer receipt, committed byte for byte.
  It records `dirty: true` at the wrapper revision `14c25146`, which is not an upstream
  commit, and its 16 tool blobs equal `f0ec5b663`’s. The census reads its closure
  status, cells, mask and object ids; the admission rests on the listed verifier’s
  receipt.
- **Timing.** The listed replay launched at 18:57:35 UTC, before this record was
  committed. Its criteria are H-341’s, registered earlier the same day.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
