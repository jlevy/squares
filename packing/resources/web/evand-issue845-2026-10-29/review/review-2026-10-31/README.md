# Stage 4 Review Programs, 31 October 2026: Daniel’s #845 and #824-Update Certificates

This directory keeps the code of two stage 4 mathematical reviews of 31 October 2026,
with everything it printed:

- [review-2026-10-31-daniel-845-172-204-260-293.md](../../../../../../docs/project/reviews/review-2026-10-31-daniel-845-172-204-260-293.md),
  Evan Daniel’s four certificates of issue #845 (this packet);
- [review-2026-10-31-daniel-824-299-update.md](../../../../../../docs/project/reviews/review-2026-10-31-daniel-824-299-update.md),
  his certificate of the 29 October update on issue #824 (packet
  `evand-n299-update-2026-10-29`) and the opening post’s certificate it continues
  (packet `evand-n299-2026-10-26`).

The same programs served both, so they are kept once, here.
They were written by the review lane `bold-ritchie-rv-daniel` (beads think-nkt1 and
think-8hjz): Claude (Anthropic), strong tier (`tbd-strong`) at the xhigh reasoning
setting, prompted separately from the import lane that built the packets.
The runbook asks for the strongest tier; the deviation is disclosed in each review (N-10
and N-7) and recorded on the pass’s epic, think-3guf. The lane wrote in scratch space
only, and the records lane retained the programs and outputs here unchanged.

## What Its Authors Read

The mathematics; the certificates’ format line (“rotation (c, s) = ((1-t^2)/(1+t^2),
2t/(1+t^2))”); issue #845, the #824 update comment and the commit messages; and, to
compare, the source’s binary64 inputs and 80-digit `.exact.txt` points.
Before the findings it also read beads think-nkt1, think-17wo and think-3xn9, the runbook’s
stage 4 and house rule, the ledger, the entries and the packets’ `sources.json`,
manifests and `report.json`. The entries’ notes state the maintained identity figures,
so the identity measurement was not blind to them.
It read none of Daniel’s `verify_cert.py`, `verify_cert2.py` or search code, nor the
maintained routes, `devtools.upper_bound_reports` or `devtools.measure_identity`; it
ran the maintained routes through their command line after its own results were in.

The source’s commits carry a Claude co-author trailer, so the authorship overlaps the
producer’s in system family; the prompts and the code are separate.

## Programs

Each runs under the project interpreter in isolated mode and reads only its arguments,
for example `packing/.venv/bin/python3 -I programs/exact_check.py CERT...`. On 31
October the certificate paths pointed at a scratch worktree of #852’s head `e2adcd8f7`
(`…/rv-daniel/tree/packing/…`), which is why the outputs name that path; the packets’
`source/search/packer/candidates/` hold the same bytes.

| Program | Decides | What it does | Printed |
| --- | --- | --- | --- |
| `programs/exact_check.py` | yes | Exact feasibility over ℚ by two methods sharing only the reader and the corner construction: separating axes on every pair with no distance filter, and exact clipped areas (Sutherland–Hodgman) | `out/check-*.json`: all seven certificates and the 172 regularized view valid by both methods, with clearances and pair gaps |
| `programs/controls.py` | yes (its controls) | Ten sharp mutations per certificate at $10^{-30}$, each decided by both methods against an outcome fixed in the program | `out/controls.txt`: 60 of 60 as expected |
| `programs/sides.py` | orders only | Exact comparison of each new side with the case records’ exact forms, the competing reports and $33/2 + \sqrt7/2$ | `out/sides.txt` |
| `programs/identity.py` | no | Binary64 pose-by-pose identity under the eight box symmetries (least summed distance), and subset fits for the L-strip lineages | `out/identity.jsonl` |
| `programs/kkt_consistency.py` | no | The certificate against the source’s 80-digit KKT point at 100 digits: dilation, contacts, rattlers, overlaps of the point | `out/kkt.jsonl` |
| `programs/dilation.py` | no | Each dilation certificate against its binary64 input | `out/dilation.txt` |
| `programs/tilts.py` | no | Tilt census | `out/tilts.txt` |

The SHA-256 of each program as retained is in `programs.sha256`.

`out/maintained/` holds the maintained routes’ receipts from
`devtools.upper_bound_reports PACKET decide-job --n N --control positive --output ...`,
run after the programs above, at 172, 204, 260, 293 and 299 (both certificates);
`out/custody.txt` lists every digest read upstream and in the packets.

## Inputs

`s172_1028.cert`, `s204_1028.cert`, `s260_1028.cert`, `s293_1028.cert` and
`s299_1028.cert` at evand/square-packing `d2d5dd9` and `0e76d9f`, with their
`.input.txt` and `.exact.txt` files and `s172_1028_regularized.cert`; T-248’s
`s299-1025.cert`; the known-best witnesses at 172, 176, 199, 204, 260, 293 and 299; and
#844’s and Couzo’s a5a5d76 certificates at 260 for comparison.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
