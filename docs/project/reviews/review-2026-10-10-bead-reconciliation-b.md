# Bead Reconciliation Review: Lane B

Date: October 10, 2026

This review covers all 512 nonclosed beads and all 26 specification files assigned to
lane B in the reconciliation inventory.
The companion
[`review-2026-10-10-bead-reconciliation-b.json`](review-2026-10-10-bead-reconciliation-b.json)
contains one explicit disposition for every assigned bead and specification.

## Method

The review compared the lane inventory with the full bead snapshot, a fresh bulk
`tbd show` of all 512 assigned beads, the assigned specifications, and the relevant
merged or open pull requests.
It read the current descriptions and notes for all 108 `in_progress` records and
screened every assigned record for explicit completion, delivery, merge, retirement,
supersession, pause, block, and deferral language.
A bead stayed open unless the evidence showed that its own acceptance conditions were
complete. Age, a complete checklist, or closed children alone did not establish
completion.

The inventory list does not establish whether an omitted delegate is absent.
Delegate preconditions appear only where a fresh `tbd show` returned one.
Each proposed bead mutation includes `expected_version` and `expected_status`, plus
`expected_delegate` whenever the fresh record returned one.
The coordinator should re-read each record and skip any mutation whose precondition no
longer matches.

## Bead Dispositions

| Action | Count | Basis |
| --- | ---: | --- |
| Close | 3 | Acceptance complete and integrated |
| Update | 60 | 59 exact stale-path repairs and one explicit paused hold |
| Retain | 400 | Current scope, accurate existing holds, or concurrent activity remains |
| Needs evidence | 49 | Unresolved paths or inconsistent parent and follow-up state |

Three closures are supported:

- `think-ny3r`: [PR #477](https://github.com/jlevy/squares/pull/477) merged on October
  10, all four children are closed, and the task was specifically to resolve the
  conflicts and merge that pull request.
- `think-rs0t`: the request ledger and offline checker landed through merged
  [PR #298](https://github.com/jlevy/squares/pull/298), which is the close condition in
  the fresh notes.
- `think-r7yt`: the fresh notes account for all ten certificate groups at V3/C3 and
  transfer the later n82 follow-up to `think-4qga`; the mixed, linear, and rectangle
  groups are supported by [PR #298](https://github.com/jlevy/squares/pull/298),
  [PR #327](https://github.com/jlevy/squares/pull/327), and
  [PR #382](https://github.com/jlevy/squares/pull/382), respectively.

The 59 updates remove the obsolete literal `explorations/packing/` prefix when the
resulting repository-relative path exists exactly.
They change only `spec_path` and preserve each bead’s status and hold.
The affected beads are:

`think-i50h`, `think-iwlr`, `think-jxx8`, `think-jygr`, `think-kmn2`, `think-kmwb`,
`think-l4z5`, `think-lcfd`, `think-lpse`, `think-lwao`, `think-m79h`, `think-mli0`,
`think-mn9j`, `think-nt5w`, `think-opzu`, `think-osyp`, `think-ouf0`, `think-owm0`,
`think-p76j`, `think-qk9w`, `think-qqvh`, `think-qv90`, `think-r1yl`, `think-r33j`,
`think-r45s`, `think-rrht`, `think-siui`, `think-sk15`, `think-ta07`, `think-thhk`,
`think-tow1`, `think-trkj`, `think-tuke`, `think-tx0b`, `think-tz4b`, `think-u83z`,
`think-u97a`, `think-uvmb`, `think-v2m1`, `think-v9bp`, `think-va53`, `think-vbk5`,
`think-vcnx`, `think-vk3t`, `think-w6on`, `think-wbra`, `think-wbx5`, `think-wd31`,
`think-wfz1`, `think-xd7c`, `think-xzew`, `think-y37w`, `think-y91x`, `think-ydus`,
`think-yi6x`, `think-z3g5`, `think-zcx4`, `think-zt29`, and `think-zvxw`.

Three beads changed from `open` to `in_progress` after the snapshot: `think-y321`,
`think-sjz7`, and `think-nx5z`. Their dispositions preserve the concurrent work.

The hold axis already represents six paused or blocked records accurately: `think-ldq2`
is paused, while `think-trkj`, `think-v3u5`, `think-nbhe`, `think-jhgi`, and
`think-w5tm` are blocked.
`think-lhyk` alone needs a `paused` hold: PR #347 has merged, and its fresh notes say
the remaining slice waits on the owner.
The review retains `think-jogv`, `think-nymu`, and `think-qqzs` without a hold change
because their historical authorization, network, and predecessor conditions need current
evidence.

Several records with all current children closed remain open for specific reasons:

- `think-izep` still requires a verified lawful Plakhta copy.
- `think-tx0b` still covers pure-Python hangs, aggregate duration, detached daemons, and
  Windows behavior. Its only proposed change is the exact path repair.
- `think-kk7w` still requires ordinary-U parity and adoption after PR #410.
- `think-ykt7` has remaining work listed in its fresh notes.
- `think-vqio` remains delegated, and PR #490 is open.

Forty-five missing paths have no exact target established by this review after the 59
repairs. Forty-four receive a path-specific `needs_evidence` disposition; `think-izep`
has a more specific source-access issue that takes precedence in the JSON. `think-segb`
also needs proof that every child and the required disposition reply are complete, while
`think-jtlq` needs proof that the beyond-horizon claims were registered after PR #479.
`think-sb9c` delivered its parent review in merged PR #473, but one child remains open;
that child should be reparented or dispositioned before the parent closes.
`think-xgjo` likewise has a merged correction and a fresh validation backlog with four
open children.

## Specification Dispositions

Five specifications have direct completion evidence and moved to `done`:

- `plan-2026-09-13-n11-bc329-runset-verifier.md`
- `plan-2026-09-13-pr157-integrated-calibration-launch-supplement.md`
- `plan-2026-09-30-n11-optimality-illustrations.md`
- `plan-2026-10-01-release-assets-on-demand.md`
- `plan-2026-10-01-result-kinds.md`

The stale status text in the first two and last two was corrected in place.
The illustrations specification already reports `implemented`.

The numeric-symbolic round-trip plan moved to `draft` because it says `Draft` and has no
linked or mentioned beads.
The generalized-motion lab moved to `paused` because its status says Phase 2 is paused
pending explicit semantics.
Its four nonclosed linked or mentioned beads remain visible through the companion
disposition.

The October 10 three-block session remains active as the selected prepared launch
pointer. Although it says it was not launched, seven mentioned agenda beads remain open;
moving the plan would obscure the current next-entry plan.

Five specifications need evidence before a move: the August 26 constructive run, the
symbolic-promotion document, the post-381 sequence, and the October 6 and October 7
fixed-duration N17 session plans.
Fourteen specifications remain active because their own status or governing bead set
still shows open work.
The moves include their inbound and outbound links, document-map entries, generated
SYNOPSIS rows, and math-markup registry paths.
Frozen baseline and reconciliation JSON keep the original paths as the reviewed
snapshot.

## Files Changed

This lane corrected four specification status passages, moved seven specifications,
updated their repository links and map entries, and created this review plus its
companion JSON. It did not mutate beads, commit, or push.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
