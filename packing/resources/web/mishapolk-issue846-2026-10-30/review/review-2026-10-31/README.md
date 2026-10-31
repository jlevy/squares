# Stage 4 Review Programs, 31 October 2026: Polkovskyi’s Certificates of 23 October and #846

This directory keeps the code of the stage 4 mathematical review
[review-2026-10-31-polkovskyi-846-and-23-oct.md](../../../../../../docs/project/reviews/review-2026-10-31-polkovskyi-846-and-23-oct.md),
with everything it printed.
It covers both of Mykhailo Polkovskyi’s packets of this pass: the nine certificates
first published in his commits of 23 October (`mishapolk-1023-refinements-2026-10-30`)
and the six of issue #846 (this packet). The programs are kept once, here, for both.

It was written by the review lane `bold-ritchie-rv-polk` (bead think-ikku): Claude
(Anthropic), strong sub-agent tier (`tbd-strong`) at the xhigh reasoning setting,
prompted separately from the import lane that built the packets.
The runbook asks for the strongest tier; the deviation is disclosed in the review
(RV-11) and recorded on the pass’s epic, think-3guf. The lane wrote in scratch space
only, and the records lane retained the programs and outputs here unchanged; the
lane’s pre-format draft of the review is not kept.

## What Its Authors Read

- **Before the checker ran:** both packet READMEs and declarations; the register text of
  both entries; the ledger README, `ledger.json` and `starts.yaml`; beads think-ikku,
  think-pg1y, think-fwa9 and think-oqjd; the runbook’s stage 4, its section on several
  reports at one count and the house rule; the headers and first rows of the
  certificates, as data; and the first 160 lines of the 22 October review of #719, as
  the brief’s model of the shape, which names the two methods this checker also uses.
- **After:** the outline, findings and rungs of the 23 October review of 204, the
  outline of the 24 October review of 268 and 304, T-195’s and T-170’s register text,
  the docstring and rule constants of `devtools/intake_ledger.py`, and `_root` in
  `devtools/check_half_angle_area.py` (for RV-10).
- **Never read:** the code of either maintained route, `sqpack`’s verifiers, the
  source’s `verify_bound_certificate.py` and any earlier review’s programs.

## Programs

Each is standard-library Python, run under the project interpreter in isolated mode,
and reads only its arguments. On 31 October the certificate paths pointed at a scratch
worktree of #852’s head `e2adcd8f7` (`…/rv-polk/tree/packing/…`), which is why the
outputs name that path; the packets’ `source/certificates/0000-0999/` hold the same
bytes. The digests are in `programs.sha256`, and as the lane recorded them in
`out/program-digests.sha256`; the two agree.

| Program | Decides | What it does | Run | Printed |
| --- | --- | --- | --- | --- |
| `programs/rv_check.py` | yes | Two exact routes over ℚ sharing only the reader: A, support functions at the walls and separating axes on every pair whose centres lie within 3/2; B, all four corners at the walls and the exact Sutherland–Hodgman clipped area of every pair whose bounding boxes overlap. `selftest` decides ten hand-built packings. | `rv_check.py selftest`; `rv_check.py check CERT...` on all 25 retained certificates (6 s) | `out/rv-check.jsonl`: 10 of 10 self-tests as required; 25 of 25 accepted on both routes |
| `programs/rv_controls.py` | yes (its controls) | Seven mutants of each certificate at exact contact and $10^{-60}$ past it, through both routes, on the whole packing and, for the pair mutant, the pair alone | the 15 counts (25 s) | `out/rv-controls.jsonl`: 105 of 105 as required |
| `programs/rv_identity.py` | no | Sides, 12-place prints, the best of the eight box symmetries by nearest centres, moves and turns modulo 90°, and the exact free play of each moved square in both packings | `rv_identity.py N CERT REF [cert]` at the 15 counts | `out/rv-identity.jsonl` |
| `programs/rv_gaps.py` | no | Near-contact gap distributions | both 130 certificates | in the review’s 130 paragraph |
| `programs/rv_claims.py` | no | Each register claim against its certificate header, exactly | both packets | in the review’s Claims Covered |

The maintained runs, through their command line: `acquire_source PACKET --check`
(`out/acq-*.txt`), `upper_bound_reports PACKET check-claims` (`out/claims-*`),
`upper_bound_reports PACKET check --replay`, all 81 jobs of both packets
(`out/replay-*.txt`, 243 and 340 CPU s), and `intake_ledger check` on the pass’s ledger
(`out/ledger-check.txt`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
