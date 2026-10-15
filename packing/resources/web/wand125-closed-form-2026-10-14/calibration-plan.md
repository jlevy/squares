# Evidence-Update Plan: the replay4d Calibration

This is the plan the records lane applies to T-180, wand125’s closed-form lower bound,
as the 14 October records PR #602 registers it (head `429aa0b6`), for bead think-au7j.
The validation lane `vcheap` wrote it on 14 October 2026 and changed no register.
Every number comes from the [README](README.md#the-calibration-replay) and
[`receipts/calibration/calibration.json`](receipts/calibration/calibration.json).
It moves no rung: two of 136 records are a sample, and the replay is the producer’s own
code re-run.

## T-180’s Unfinished Confirmation

In the first `unfinished_confirmations` item, the complete replay by replay4d, keep
`cpu_hours: 4294` and replace the basis’s last sentence, from “Not calibrated here”,
with:

> Calibrated here on 14 October 2026
> (wand125-closed-form-2026-10-14/receipts/calibration/): replay4d 0.1.0, built with
> rustc 1.86.0 from the retained crates, replayed the two smallest records, interval 26
> and interval 14 top, REPLAY OK, in 0.672 CPU-hours against the source’s 0.55. That is
> a ratio of 1.223, 1.20 to 1.25 at the source’s two decimals, measured at nice 10 on
> four cores shared under load.
> At that ratio the complete replay is about 5,250 CPU-hours on this host.

## `V-wand125-replay4d`

Replace the note’s first sentence, “Not built or run here.”, with:

> Built here on 14 October 2026 with rustc 1.86.0 and the locked Cargo.lock, from the
> retained crates (0.1.0, binary d52b8d88…) and the 1c661b7 revision’s (0.1.1, binary
> fb84677b…); each passed its 28 tests and printed the source hash its packet
> recomputes. 0.1.0 replayed two records of the 136 and refused a truncated record and a
> relabelled leaf (wand125-closed-form-2026-10-14/receipts/calibration/).

Add the 0.1.1 binary to the version rows that the
[1c661b7 plan](../wand125-closed-form-source-hash-2026-10-14/evidence-plan.md) adds.

## An Optional Evidence Entry

The records lane may register the calibration as a sample, as the cfcheck plan does for
its own sample. It derives no rung, since `devtools.check_results` counts no entry whose
coverage is a sample.

```yaml
- id: E-wand125-closed-form-replay4d-sample
  claim: lower-bound
  scope: {n_values: [<the 264 values of E-wand125-closed-form-report>]}
  assurance: verified
  method: exact-algebraic
  performed_by: repository
  relationship_to_generator: same-implementation
  independence:
    coverage: {extent: sample, unit: region records of the closed-form certificate, checked: 2, of: 136}
  origin: replayed-here
  novelty: previously-published
  source_key: '[wand125 closed form 2026-10-14]'
  certificate: packing/resources/web/wand125-closed-form-2026-10-14/receipts/calibration/calibration.json
  replay: >-
    Restore problems/closed-form/checker/ in scratch from this packet and match it to the
    manifest; cargo +1.86.0 test --locked --release -p seam4d_core -p replay4d and cargo
    +1.86.0 build --locked --release -p replay4d; download interval_0.495_0.5.tar.gz and
    interval_0.435_0.44.tar.gz of closed-form-v1, check them against ASSET.json and
    SHA256SUMS, and unpack them; run the commands receipts/calibration/*.log record,
    through devtools.replay_receipt, and bind them with devtools.audit_wand125_closed_form
    calibrate. Both records must end REPLAY OK with intervals.json's counts, and the
    three controls must be refused or accepted as calibration.json records.
  replay_status: passed
  verifiers: [V-wand125-replay4d]
  limitations: >-
    Run here on 14 October 2026 from the retained crates, replay4d 0.1.0 (source hash
    92002e0e...), rustc 1.86.0, one thread per record, B3_PLAIN_RF unset, on four cores
    shared with other agents. Interval 26 [0.495, 0.5] top (4,158 roots, 32,828 leaves)
    and interval 14 [0.435, 0.44] top (3,861 roots, 91,343 leaves), the two smallest of the
    136 records, each REPLAY OK with the family digest, record digest, roots and leaves
    of every kind of intervals.json, in 1,178.9 and 1,241.7 CPU-seconds. The first two
    roots alone and a leaf relabelled from CORE1:Tx to CORE were refused. The producer's
    own code re-run on 124,171 of the certificate's 187,183,108 leaves; a sample decides the
    records it replayed and nothing about the others, and it sets no rung.
  source_reviewed: '2026-10-14'
```

## think-wu73

The full-replay bead’s Cost line can read: “4,294 CPU-h by the source’s receipt; about
5,250 CPU-h on this host by the calibration of think-au7j (ratio 1.223, measured under
load).” Its proposed subset, interval 24 at 18.32 CPU-hours by the source, is about 22.4
here, inside the owner’s 40-hour cap.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
