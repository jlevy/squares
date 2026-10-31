# The Revised Geometric Manuscript of the n = 11 Proof, Pinned 2026-10-31

This packet retains the three commits of 8 October 2026 (local time) to
[Queuingtheorydotcom/11SquaresOptimal](https://github.com/Queuingtheorydotcom/11SquaresOptimal)
past `f9e0de7`, the commit the
[`n11-optimality-2026-09-29`](../n11-optimality-2026-09-29/README.md) packet retains
and T-060 cites.
They add `paper/`: a revised geometric manuscript of the proof that the known packing of
eleven unit squares is optimal, a companion on its geometric foundations, and a
self-contained verification supplement. A paragraph on them is added to `README.md`.
The certificates and checkers that T-060 rests on are unchanged.

It is new evidence for the claim T-060 cites, the author’s revision of its exposition,
and changes no rating.
Bead `think-3i74` owns it.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/Queuingtheorydotcom/11SquaresOptimal> |
| Revision | [`4262f07c7723428c1725bb757ed06d0c4d28be1a`](https://github.com/Queuingtheorydotcom/11SquaresOptimal/tree/4262f07c7723428c1725bb757ed06d0c4d28be1a), tree `9e90603c`, “Simplify ownership exclusions and publish exact component replays” |
| Committed | 2026-10-09T01:55:55Z (21:55:55 on 8 October in the commit’s −04:00), author and committer Queuingtheorydotcom (Manasseh Ahmed) |
| History | `2e4c4cd` (04:46:47Z), “Add geometric eleven-square proof and verification supplement”; `f49664b` (20:11:58Z), “Simplify the early geometric reduction and update the proof supplement”; then the pin |
| Retrieved | 2026-10-31T05:07Z, a full clone; `main` pointed at this commit |
| Licence | No licence file. `THIRD_PARTY_NOTICES.md`, unchanged since `f9e0de7`, asserts no blanket licence over the collection; each file keeps its own terms |
| Bibliography key | **[Ahmed n11 optimality 2026]**, the key of the earlier packet, under which T-060 cites the source |

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json); the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of the
six files the three commits change, and `--check` re-derives them.
Five are retained under [`11SquaresOptimal/`](11SquaresOptimal/): `README.md`,
[`paper/README.md`](11SquaresOptimal/paper/README.md), `paper/SHA256SUMS`,
`paper/eleven-squares-synthesis.tex` and `paper/eleven-squares-geometric-foundations.tex`.
No file is compressed.

One is pinned by size and digest only: the verification supplement
`paper/eleven-squares-publication.zip`, 5,426,101 bytes, SHA-256
`9ece0254a4c08cb3d68bd2332f4250b935cf5b6e02ce4c1bccabbff2914fba03`, which
`paper/SHA256SUMS` also lists. It holds 387 files, 26,360,481 bytes unpacked: the two
manuscripts, input and certificate data, and the standard-library checkers its
`verify.py` runs. It is bulk data kept out of Git
([OR-18](../../../../operating-rules.md)). Its member list was read here; nothing in it
was extracted or run.

## What the Commits Report

From `paper/README.md` and the paragraph added to `README.md`:

- **The manuscript.** “Eleven squares: owners, support chains, and angle penalties”
  combines a marker-based global reduction with a support-chain inequality that lets the
  tilted squares rotate independently. An early corridor, a virtual bottom row and a
  virtual right column replace several spatial exclusion chains, and the surviving
  ownership case has a 103-node dependency graph, down from 119.
- **The simplified exclusions.** Case 0 ends with an elementary three-point height bound
  and a blocking segment. Case 3 uses 12 point assertions instead of 62, and case 5
  uses 65 instead of 170. Cases 1, 2 and 4 keep their earlier exclusions.
  Quantitative nonoverlap penalties replace the late fine capture and the branched
  local-isolation endpoint.
- **The companion.** “Geometric foundations” gives direct proofs of the rectangle,
  triangle, wall and ownership rules.
- **What was run.** The commands are `python3 verify.py --check-inputs`, `--quick`,
  `--ownership`, `--early` and `--full`, tested with CPython 3.12.4’s standard
  library. The author reports that input verification, all 13 quick checks, the
  ownership replay and the early component replay passed in a clean extraction, and
  that “the portable full command has not yet been executed end to end”.
  `--early` checks the new components under stated parent inputs, so its result is
  conditional until those parents are freshly established, and neither `--early` nor
  `--quick` proves the global argument alone.

## What It Changes in the Record

Nothing yet. T-060 rests on the certificates and receipts at `f9e0de7`, which these
commits do not change.
A reading of the revised manuscript against the record’s review of the proof, and a run
of the supplement’s `--full` command, are `think-3i74`’s to schedule.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
