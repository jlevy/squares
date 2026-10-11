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
  results:
  - shape: determination
    role: guard
    question: C1, custody. Does every one of the 24 objects match the contributor's manifests and the
      repository's two manifests by size and SHA-256, and does the release serve the same bytes after upload?
    outcome: criterion_met
    checked_by: Before the replay, sha256sum -c over both contributor SHA256SUMS files, the sizes and digests
      of both contributor manifests, hosted_data check on them and each seed's recomputed content id all
      agreed (custody.json, no problems). hosted_data check passes on hosted/n17-issue-472-kernel-certificates.yaml
      and hosted/n17-x048-session-168-certificates.yaml. hosted_data publish --manifest hosted/n17-issue-472-kernel-certificates.yaml
      printed "uploaded 24, already present 0" and "verified 24 served assets, 392.6 MiB" in 79.3 s; it downloads
      every served asset and compares it with the manifest. The release then held exactly 24 assets totalling
      411,682,476 bytes, and the digest GitHub reports for each equals both manifests. A separate download
      into an empty directory of the largest node (66,129,638 bytes), the smallest seed and one 27.6 MB node
      matched size and SHA-256; the logs are in the record directory's custody/.
  - shape: determination
    role: outcome
    question: C2, listed full pass. Does each certificate pass the listed kernel-streamed verifier (blob
      1ad706c21) in full mode from a clean worktree at 3213d651b, with the repository path as the receipt's
      directory and the manifest's seed and node?
    outcome: criterion_met
    checked_by: Twelve receipts, each with schema n17-certificate-verification/v1, verifier kernel, status
      PASS, mode full, closed true, failure null, provenance.files exactly {packing/devtools/verify_n17_kernel_certificate.py
      1ad706c21d04cc4a052af8a942c848cbca59fd76}, dirty false, revision 3213d651b880d7768bce8506efaf75c2089aeb4f,
      directory the repository path as written, and certificate ids equal to the contributor's. All twelve
      runs exited 0. Verifier seconds 108.1 to 1,384.0, 6,461.0 s in all; the longest wall was 1,389.6 s,
      under the 5,400 s ceiling; peak RSS 202 to 1,111 MB. census_n17_certified reads all twelve as verified
      under kernel-streamed.
  - shape: determination
    role: outcome
    question: C3, Rust parity. Does n17-kernel-verifier return PASS on the same objects, with every receipt
      field equal to C2's except provenance, directory and seconds?
    outcome: criterion_met
    checked_by: n17_kernel_verify at 6a0499ba4 (toolchain 1.98.0, source_sha256 3ae979c3b163...) returns
      PASS on all twelve in 16.6 to 148.3 s of wall. With provenance, directory and seconds removed, each Rust
      receipt is equal to the listed receipt under jq -S, and parity.json records all 26 compared fields
      agreeing with both the contributor's receipts and the listed replays. The comparison was ad hoc; see
      Disclosures.
  - shape: determination
    role: guard
    question: C4, endpoint control. Does the census refuse no entry and report the endpoint's state surviving?
    outcome: criterion_met
    checked_by: census_n17_certified on the admitted ledger accepts all 72 entries, refuses none, and reports
      endpoint_survives true; all twelve new entries' objects are present locally and match the data manifest.
  - shape: determination
    role: outcome
    question: C5, count. Is the certified line after admission 3,636 orbits and 28,528 states, with the distance-2
      stratum at 94 orbits and 736 states?
    outcome: criterion_met
    checked_by: census.json reports 72 admitted, 3,636 orbits and 28,528 surviving states, endpoint surviving
      (before, on the registration commit's ledger, 60 admitted, 4,683 orbits and 36,768 states). partition.json
      puts 94 orbits and 736 states at distance 2, down from 95 and 744; the one orbit removed is mask 1965787.
  - shape: determination
    role: mechanism
    question: Information only, not a criterion. Does main's unlisted kernel verifier (blob be8135f6e at 6a0499ba4)
      agree on the same twelve?
    outcome: criterion_met
    checked_by: All twelve PASS in full mode, closed, dirty false, revision 6a0499ba4, verifier seconds 94.8
      to 869.7 (4,432.2 s in all), and every field outside provenance, directory and seconds equals the listed
      receipt. It admits nothing.
  verdict:
    decision: accepted
    primary_criterion: H-341's threshold, unchanged; 12 of 12 certificates pass C1 to C4 below and the census
      after admission reports 3,636 orbits and 28,528 states with the endpoint surviving and the distance-2
      stratum at 94 orbits and 736 states. A certificate that fails C1 to C4 is not admitted, and the others
      are still admitted and counted.
    reason: All twelve pass the listed verifier in full from a clean worktree, agree with the Rust verifier
      outside provenance, directory and seconds, are served by the ledger's release at the manifest's digests,
      and once admitted leave exactly the projected 3,636 orbits and 28,528 states with the endpoint surviving
      and the distance-2 stratum at 94 orbits and 736 states.
    commit: 3213d651b880d7768bce8506efaf75c2089aeb4f
    needs_review: false
  effort:
    timebox: 5,400 s per Python verification (registered; the runner did not enforce it); one full verification
      per certificate under each verifier
    wall_seconds: 3337
    stopped_by: criterion
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
| Upload, served-bytes check and separate fetch | `results/exp-317-issue-472-kernel-admission/custody/{publish.log,publish.time,release-assets.json,clean-fetch.txt}` |
| Census and partition after admission | `results/exp-317-issue-472-kernel-admission/census.json`, `partition.json` |

The `results/` paths are under
`packing/campaign/series/series-000-smoke-and-calibration/`.

## Results

**Accepted.** All twelve meet C1 to C4, and C5 holds exactly.
The certified line moves from 60 entries, 4,683 orbits and 36,768 states to 72 entries,
3,636 orbits and 28,528 states, with the endpoint surviving.
The distance-2 stratum moves from 95 orbits (744 states) to 94 (736); the orbit removed
is mask 1965787, the one H-341’s projection attributes to `m935012`. This is an
exclusion count on the H-266 cover at U = 1169/250. It is not global capture, and it
says nothing about $s(17)$.

Listed replay: the verifier’s own `seconds`, the wall time and peak RSS from
`/usr/bin/time -v`, four at a time on four cores while the Rust runs shared the machine.
Rust: wall and peak RSS, one at a time with two threads under `nice -n 19`. Forward: the
verifier’s `seconds` under blob `be8135f6e`. Alone and margin are orbits / states from
`census.json`; the margin is what the entry excludes that none of the other 71 does.

| Certificate | #413 row | Closure (owner, step) | Listed replay | Rust parity | Forward replay | Alone | Margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `w125-k-m214101` | 25 | 4, 154 | PASS, 178.5 s; 179.1 s wall, 224 MB | PASS, equal; 31.0 s, 83 MB | PASS, 168.8 s | 7,869 / 62,560 | 463 / 3,620 |
| `w125-k-m14353473` | 36 | 16, 192 | PASS, 232.3 s; 233.0 s wall, 207 MB | PASS, equal; 41.5 s, 87 MB | PASS, 226.3 s | 4,656 / 36,952 | 138 / 1,092 |
| `w125-k-m983396` | 31 | 19, 383 | PASS, 1,026.5 s; 1,031.9 s wall, 255 MB | PASS, equal; 148.3 s, 100 MB | PASS, 619.5 s | 10,686 / 85,280 | 114 / 912 |
| `w125-k-m3869440` | 35 | 21, 23 | PASS, 1,196.2 s; 1,202.0 s wall, 1,085 MB | PASS, equal; 78.9 s, 751 MB | PASS, 665.9 s | 5,011 / 39,688 | 92 / 708 |
| `w125-k-m5707072` | 37 | 8, 37 | PASS, 1,384.0 s; 1,389.6 s wall, 1,111 MB | PASS, equal; 103.4 s, 764 MB | PASS, 799.8 s | 5,813 / 46,344 | 39 / 312 |
| `w125-k-m6177056` | — | 19, 253 | PASS, 1,276.3 s; 1,281.8 s wall, 411 MB | PASS, equal; 128.2 s, 153 MB | PASS, 869.7 s | 8,976 / 71,448 | 36 / 280 |
| `w125-k-m7815200` | 29 | 22, 191 | PASS, 180.2 s; 181.0 s wall, 202 MB | PASS, equal; 30.7 s, 87 MB | PASS, 174.4 s | 8,311 / 66,120 | 37 / 296 |
| `w125-k-m1000708` | 30 | 16, 44 | PASS, 108.1 s; 108.8 s wall, 264 MB | PASS, equal; 16.6 s, 149 MB | PASS, 94.8 s | 9,824 / 78,288 | 30 / 240 |
| `w125-k-m935012` | 23 | 10, 27 | PASS, 125.1 s; 125.6 s wall, 252 MB | PASS, equal; 18.5 s, 167 MB | PASS, 108.7 s | 10,514 / 83,868 | 33 / 260 |
| `w125-k-m7799616` | 34 | 21, 70 | PASS, 226.7 s; 227.4 s wall, 315 MB | PASS, equal; 33.2 s, 188 MB | PASS, 197.6 s | 4,923 / 39,160 | 10 / 80 |
| `w125-k-m5116178` | 24 | 8, 266 | PASS, 309.6 s; 310.6 s wall, 236 MB | PASS, equal; 52.6 s, 112 MB | PASS, 294.4 s | 10,424 / 83,092 | 1 / 8 |
| `w125-k-m4657489` | 38 | 16, 266 | PASS, 217.6 s; 218.3 s wall, 224 MB | PASS, equal; 36.5 s, 84 MB | PASS, 212.4 s | 5,844 / 46,568 | 11 / 88 |

Every closure is `all_parent_poses_forbidden`. The census and the partition were run on
the admitted ledger in this checkout: `census_n17_certified` in 9.7 s of wall at a peak
RSS of 175 MB, and `stratify_n17_certified_residue` in 2.9 s at 139 MB. Both record the
ledger as uncommitted at the registration commit, with the blob the admission commit
holds.

## Cost

- **Listed replay:** 6,461.0 s of verifier time and 4,860.7 s of CPU across the twelve,
  from 18:57:35 to 19:25:39 UTC, four at a time.
  The contributor reported 6,794 s serial.
  The first four launched shared the four cores with the Rust runs and a partial
  edit-tier check, and got 62 to 70 percent of a core each: `m983396` used 636 s of CPU
  in 1,032 s of wall. That is why three of them took longer than the contributor’s
  figures.
- **Rust:** 719.5 s of wall for all twelve, 18:59:54 to 19:11:54 UTC, after a
  `cargo build --release --locked` of 1 min 49 s.
- **Forward replay:** 4,432.2 s of verifier time, rerun in full from 19:34:03 to
  19:53:12 UTC.
- **Custody:** 411,682,476 bytes uploaded, then downloaded and compared, in 79.3 s; the
  separate three-object fetch moved another 93.7 MB.
- **Wall for the round:** 3,337 s, from the first launch at 18:57:35 to the last
  verification receipt at 19:53:12. Custody, the census and the partition add about 92
  seconds.

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
- **Timing.** The listed replay launched at 18:57:35 UTC, before this record’s
  registration commit `3d132c3e0` (19:08 UTC). Its criteria are H-341’s, registered at
  `2ed894325` (17:51 UTC), and nothing in them changed after the launch.
- **The ceiling was not enforced.** The record registers 5,400 s per verification, but
  the runner set no `timeout`. Every run finished under it: the longest listed run took
  1,389.6 s of wall, and the longest forward run 874.9 s.
- **The forward replay was run twice.** A container restart at about 19:33 UTC
  interrupted its first attempt, launched at 19:25:47, before any of the four running
  verifications wrote a receipt.
  It was rerun from scratch at 19:34:03, and the receipts kept are the rerun’s;
  `forward-be8135f6e/runner.log` shows both.
- **The forward command differs from the registered one.** It ran
  `.venv/bin/python3 -m devtools.verify_n17_kernel_certificate campaign/…/w125-k-m<mask>`
  from the `6a0499ba4` worktree’s `packing/`, not through `uv run` with a `../packing/`
  path. Its receipts still record the repository path as `directory`. It admits nothing.
- **The Rust receipts’ `directory`.** The Rust verifier ran on the staged copy of each
  certificate outside the worktree, so its receipts record an absolute scratch path.
  The objects there are the same files by SHA-256, and H-335’s rule leaves `directory`
  out of the comparison.
- **The parity comparison is not a committed tool.** It was made with an ad hoc script,
  which wrote `rust/parity.json`, and checked again with
  `jq -S 'del(.provenance,.directory,.seconds)'` and `diff` on each pair.
  OR-1 asks for a committed comparator; this is a declared deviation, and bead
  `think-n53s` tracks committing one with tests.
- **Custody of the ledger’s other objects.** The ledger’s release,
  `data/n17-x048-session-168-certificates-v1`, held no assets before this upload.
  It now holds these 24; the 204 objects the ledger’s manifest listed before remain
  unhosted (H-336). The census reports them as not in place, which never refuses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
