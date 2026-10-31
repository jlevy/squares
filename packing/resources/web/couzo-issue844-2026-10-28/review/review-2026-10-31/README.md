# Stage 4 Review Programs, 31 October 2026: Couzo’s #843, a5a5d76 and #844

This directory keeps the code of two stage 4 mathematical reviews of 31 October 2026,
with everything it printed:

- [review-2026-10-31-couzo-843-130.md](../../../../../../docs/project/reviews/review-2026-10-31-couzo-843-130.md),
  Francisco Couzo’s certificate at 130 (issue #843, packet `couzo-issue843-2026-10-28`);
- [review-2026-10-31-couzo-844-232-260-307.md](../../../../../../docs/project/reviews/review-2026-10-31-couzo-844-232-260-307.md),
  his certificates at 260 and 307 of commit a5a5d76 (packet `couzo-a5a5d76-2026-10-28`)
  and at 232, 260 and 307 of issue #844 (this packet).

Both were written by the review lane `bold-ritchie-rv-couzo` (beads think-oy8d and
think-dwzb): Claude (Anthropic), strong sub-agent tier (`tbd-strong`) at the xhigh
reasoning setting, prompted separately from the import lane that built the packets.
The runbook asks for the strongest tier; the deviation is disclosed in each review
(N-6) and recorded on the pass’s epic, think-3guf. The lane wrote in scratch space only,
and the records lane retained the programs and outputs here unchanged.

## What Its Authors Read

- **Before the checker decided:** the brief; the beads; the runbook’s stage 4 and house
  rule; three earlier Couzo reviews, for shape; the three packet READMEs; the register
  entries, their evidence entries and the pass’s ledger; issues #843 and #844; and the
  source’s credit records and manifest, as data. The certificate format is the comment
  line each certificate carries: a centre and $t = \tan(\theta/2)$.
- **After:** the maintained replay receipts, the command-line help of
  `devtools.upper_bound_reports` (run, its code not read) and the drafted replies.
- **Never read:** the source’s `verify_bound_certificate.py` and `exact_finish.py`, the
  maintained routes’ code, `sqpack`’s verifiers and `devtools.measure_identity`.

The source’s commits carry a Claude co-author trailer, so the authorship overlaps the
producer’s in system family; the prompts and the code are separate.

## Programs

Each runs under the project interpreter (CPython 3.14.7), reads only its arguments and
runs no other program. The certificate paths point at the packets’ retained `source/`
copies; on 31 October they pointed at a scratch worktree of #852’s head `e2adcd8f7`
(`…/rv-couzo/tree/packing/…`), which is why the outputs name that path.

| Program | Decides | What it does | Printed |
| --- | --- | --- | --- |
| `programs/check_certs.py` | yes | Reads a half-angle certificate (comment line, `n S`, `n` rows `x y t`) and decides it on two exact routes over ℚ: A, separating axes on every pair and support functions at every wall; B, exact corners at the walls and the exact clipped area of every pair whose centres are closer than √2. Builds ten controls in memory from the tightest pair and decides each on both routes. | `out/check-all.{txt,json}`: all six certificates accepted on both routes, every control as expected (60 CPU s); `out/check-130.{txt,json}`, the 130 run alone |
| `programs/agree.py` | no | Holds route A to a maintained replay receipt: side and poses literal for literal, both routes passed on every pair, and their least pair gap and least wall clearance equal route A’s exactly. | `out/agree.txt`: 10, 20 and 30 of 30 checks equal |
| `programs/identity.py` | no | Pairs two packings pose by pose under the eight symmetries of the square about the box centres (least summed squared centre distance), with one-to-one by nearest centres, the bottleneck, moves and turns modulo 90°. | `out/identity-130.txt`, `identity-130-parent.txt`, `identity-232-260-307.txt` and the `.json` beside them |
| `programs/sides.py` | no (orders only) | Reads the sides exactly, checks that each 12-place print rounds up, orders the reports at each count and compares each side with the house witnesses at the next 39 counts. | `out/sides.txt` |

The SHA-256 of each program as retained is in `programs.sha256`.

Run, from this directory:

```bash
python -I programs/check_certs.py LABEL=CERT... --out out/check-all.json
python -I programs/agree.py RECEIPT.json.xz CERT...
python -I programs/identity.py --n N A B
python -I programs/sides.py REPO_ROOT
```

## Inputs

The six certificates in the packets `couzo-issue843-2026-10-28`,
`couzo-a5a5d76-2026-10-28` and this one; the house witnesses
`packing/witnesses/known-best/n-130.yaml`, `n-232.yaml`, `n-260.yaml`, `n-307.yaml` and
those at the later counts; for comparison only, Polkovskyi’s #846 certificates at 130
and 260 and Daniel’s #845 certificate at 260 from their packets, and the source’s parent
certificate `certificates/parents/6f0e7dc0….cert` at `712c6a6`, read from a clone into
an empty scratch directory and never retained.

The maintained routes were re-run for both reviews with
`devtools.upper_bound_reports PACKET certify` and `check --replay`, into scratch; each
receipt equalled the committed one apart from its timings, and is not kept again here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
