# Review Programs, 16 October 2026

These are the programs that the stage 4 review lane (W2) for issue #639 wrote and ran
for
[`review-2026-10-16-evand-exact-sides-639.md`](../../../../../../docs/project/reviews/review-2026-10-16-evand-exact-sides-639.md),
the review of the entry PR #651 registers (T-193 on that branch; bead `think-7qxm`),
with what they printed.
The lane was an AI agent (Claude, strong sub-agent tier, max reasoning).
It wrote the programs in the session’s scratch space and ran them there on 16 October,
from 10:37Z to 11:07Z, in a worktree of PR #651’s branch at `ef43dd02f`.
It ran one or two processes at a time, under `nice -n 10`, on a shared four-core host.
The programs read the exact forms, the register, the ledger and the facts as data. They
run only the repository’s interpreter and libraries (CPython 3.14.7, SymPy 1.14.0,
mpmath 1.3.0 with gmpy2 2.3.1), and they write nothing in the repository.

## What Decides What, and What Is Registered

Two programs decide something.
`independent_check.py` decides that each exact form is a packing at its side, and it
also decides the polynomials. `polynomials.py` decides the polynomials alone.
Neither is registered in `packing/frontier/verifiers.yaml`, and no evidence entry cites
their outputs yet (RE-9 of the review).
`replay_sample.sh` runs the source’s own checker, the registered `V-evand-verify-exact`,
unchanged.
`custody.sh` checks premises. `claims_and_credit.py` compares the claim’s printed cuts
and the standing sides with each side, exactly.
Its pose measurements and those of `lineage.py` decide nothing.

## The Programs

Each Python program runs from `packing/` with the project interpreter as
`.venv/bin/python3 -I resources/web/evand-exact-cur-2026-10-16/review/review-2026-10-16/programs/NAME ...`.
The shell scripts run from where each one says.
`PINNED` below is a directory holding the four pinned-only forms, fetched from
`evand/square-packing` at `7d1407a` and held to the packet’s manifest. `custody.sh`
fetches them.

- **`custody.sh DIR`**, run from the repository root, makes a blobless clone at the pin
  in `DIR`. It checks the tree against the acquisition record, every manifest line’s
  SHA-256, every retained file byte for byte, and the checker’s copy.
  It printed the tree `d6b9aae3…`, 35 manifest lines matching, 30 retained files equal
  and the checker equal ([`outputs/custody.log`](outputs/custody.log)).
- **`replay_sample.sh PINNED LOG`**, run from `packing/`, ran the retained
  `verify_exact.py` on 126, 266 and 267 under `python -I`, one at a time. Each printed
  `VALID` with the receipt’s line ([`outputs/replay-sample.log`](outputs/replay-sample.log)).
- **`independent_check.py FILES --controls --json OUT`** decides each form with mpmath
  intervals at 1,400 bits and exact SymPy arithmetic in $\mathbb{Q}[t]/f$. It checks
  the count, the field, the root’s isolation, every corner against the box, every pair
  by discs or a side line, and the side and its polynomial. It then runs three controls
  of $10^{-30}$ per form, which must be refused.
  Run on the 19 retained forms and on 204 and 267 from `PINNED`, it decided all 21
  packings and all 63 controls refused, as
  [`outputs/independent.json`](outputs/independent.json) and
  [`outputs/independent.log`](outputs/independent.log) record.
  Its exact incidences equal the checker’s identity counts at every form. It resumes
  from `OUT` if interrupted.
- **`polynomials.py FILES`** decides $f$ and $p$ alone: irreducible, squarefree, one
  root in the interval, and $p(S) = 0$ in the field. Run on 263 and 297, it found all of
  that true at both ([`outputs/polynomials.jsonl`](outputs/polynomials.jsonl)).
- **`claims_and_credit.py PINNED`** encloses each $S^\ast$ to width $10^{-170}$. It holds
  each 40-place cut in the register’s claim and the closed forms at 126 and 295 to that
  enclosure. It compares every member of the ledger’s `starts.yaml` and the `of`
  certificate’s side exactly, and measures poses against the `of`.
  All 16 cuts were correct and every side was below every member
  ([`outputs/claims.jsonl`](outputs/claims.jsonl)).
- **`lineage.py PINNED`** pairs each form with the case’s house and the entries its
  chain names, using `devtools.check_half_angle_area`’s `arrangement_gap`, `unmoved` and
  readers. It printed the measurements of the review’s Credit and Lineage
  ([`outputs/lineage.jsonl`](outputs/lineage.jsonl)).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
