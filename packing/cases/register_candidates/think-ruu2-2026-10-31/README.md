# Certificates Below the Houses of 31 October 2026 (think-ruu2)

The adoption of 31 October 2026 (#852) made eight new house best packings.
Three packings below three of them were found the same day.
The house rule asks the record to register every exactly verified packing below a house,
however it was made
([result-import.md](../../../campaign/result-import.md#the-house-rule);
[Register Candidates](../../../../docs/project/guides/regularization-process.md#register-candidates)).
**The owner’s option D of 17 November 2026 decides all three (think-b0w5), and none is
registered yet.** This package retains what a registration would cite.

| n | Certificate | Side | Below the house | 12-place print | House |
| ---: | --- | --- | ---: | --- | --- |
| 130 | The run’s solve of the house, `certificates/n-130.cert` | 1487803830747751967474793359227/(1.25·10²⁹) | 2.500e-13 | …983, the house’s | T-259 |
| 293 | T-257’s 260 certificate with its 293’s L strip, `certificates/n-293.cert` | 8816991251060941991251052624833/(5·10²⁹) | 8.980e-13 | …122 against …123 | T-257 |
| 307 | The run’s solve of the house, `certificates/n-307.cert` | 4494812820921068365908930695861/(2.5·10²⁹) | 3.752e-12 | …685 against …689 | T-256 |

## Why They Are Held

The stage 4 review of 31 October
([review-2026-10-31-project-candidates-130-293-307.md](../../../../docs/project/reviews/review-2026-10-31-project-candidates-130-293-307.md))
found all three valid, and none a new arrangement.
Each is its house’s own packing, certified with less padding (RV-2):

- **130 and 307.** The solves move 2 squares beyond 1e-9 at each count, by at most
  4.1e-7 and 1.4e-4. Scaling each house’s own coordinates uniformly to first contact,
  with nothing re-solved, already removes 87% and 94% of the margins.
- **293.** The certificate is Daniel’s 293 re-assembled with its strip undilated.
  The margin is the strip’s share of T-257’s 1 + 1e-12 dilation, less a 1.02e-13
  difference between his two binary64 inputs.

The questions are the owner’s, and all three are held unregistered until they are
answered (31 October 2026), as the review proposes:

- **RV-3**: whether such a re-certification is a new result at any print, only across
  the print, or at none.
  The review recommends none.
- **RV-4** (293): whether s₂₆₀ + 1 is already issue 845’s own report, through its 260
  certificate and its stated recipe.
- **think-ikku’s RV-1** (130): whether the restatement ruling of 23 October reaches
  counts inside the corpus.

None has a register entry or an evidence entry, as T-253 and T-260 entered no replay
evidence while they were held.
A register entry would be confirmed (C3) from the day it was registered, as every
project result is, with this review listed as its accepted stage 4 review.
`devtools.select_houses` would then see it, and today it would raise a `KeyError` on the
entry’s missing `attribution`: think-4z8z teaches it and `upper_bound_houses` to read a
certificate this project made before any of the three is registered.
If the answers keep one, the registration cites this package’s certificate and receipts,
the review’s run as a second route, and the review itself.

## Option D

The owner answered RV-3 and RV-1 on 17 November 2026 with option D (think-b0w5): a
re-certification of a standing packing, with its padding removed or the same arrangement
re-solved to its exact local optimum, is a new result only if its side is below its
predecessor’s once the predecessor is shrunk until its squares first touch, measured
through any construction (`devtools.contraction_margin`). Lane w7-optd-1118 (think-8yyy)
measured each candidate against its house on 18 November 2026, both maintained routes
deciding each house certificate and its contraction (`measure/contraction-*.json`):

| n | Against | Margin | Gain | Share | Under option D |
| ---: | --- | ---: | ---: | ---: | --- |
| 130 | T-259 | 2.183057e-13 | 2.500188e-13 | 1.1453 | a new result, below the house that stands |
| 130 | T-254, Couzo’s #843 | 2.265559e-12 | 2.332819e-12 | 1.0297 | a new result |
| 293 | T-257 | 1.761685e-11 | 8.980000e-13 | 0.0510 | a restatement of T-257’s packing, Evan Daniel’s |
| 307 | T-256 | 3.528959e-12 | 3.751694e-12 | 1.0631 | a new result, but no candidate |

At 130 the candidate is below both T-259, the house, and Couzo’s certificate T-259
re-solves, each shrunk to first contact, so it is a smaller packing than the house: its
registration, stage 4 review and adoption, crediting Couzo’s packing and this project’s
re-solve with Evan Daniel’s regularizer, are think-4z8z’s, with the regularizer optimum
at 303 (`../../regularized_drawings/think-463r-2026-11-09/option-d/`). At 307 a later
house, Doğa Özden’s T-279, lies 2.03e-5 below T-256 since 9 November 2026, so the
candidate is no smaller packing and no candidate under the house rule.
At 293 the candidate restates Daniel’s certificate, and RV-4 falls with it.
Whether option D reaches T-259 itself, 0.9193 of T-254’s margin, is the owner’s question
(think-7k8p).

## What Is Retained

- **`certificates/`**: the certificate each entry registers.
  `devtools.register_candidates` pins each by the SHA-256 the review decided (RV-5).
  - At 130 and 307 it is the solve certificate, `n-N/solve/witness.cert` of the
    regularization run `adopt-2026-10-31-n130-307-evand` (`9d4b4c29…6524` and
    `f5474910…2884`). Every read holds its side to the solved side the run’s retained
    `report.json.gz` records.
  - At 293 it is the certificate the review wrote, `10eac4aa…0516`. Every read holds it,
    pose for pose, to T-257’s 260 certificate rebuilt from the
    `evand-issue845-2026-10-29` packet, with a column of 17 unit squares flush with the
    top wall and a row of 16 flush with the left wall.
- **`receipts/`**: the kernel’s three jobs on both maintained exact routes
  (`exact-certification-nNNN.json.xz`) and the six sharp controls
  (`sharp-controls-nNNN.json`).
- **`measure/`**: `devtools.measure_identity` against each house’s certificate, a
  measurement that decides nothing, and `devtools.contraction_margin` of each house’s
  certificate against the candidate (`contraction-nNNN-T.json`), which option D reads.
- **`review/`**: the review’s programs (`code/`, with its README), its receipts
  (`out/`), and the run files it read that the repository holds nowhere else
  (`inputs/`): the two drawn views and the two regularized certificates.
  The programs are kept verbatim and excluded from the lint floor in
  `packing/pyproject.toml`. No evidence entry cites them yet; at 293 they are the check
  of the lane that wrote the certificate, sharing its reader `qio.py`, not a clean-room
  route.

## Commands

From `packing/`, on 31 October 2026, at most two processes, `nice`:

```sh
B=think-ruu2-2026-10-31
python -m devtools.register_candidates $B retain --run-dir RUNS/adopt-2026-10-31-n130-307-evand \
  --review-out REVIEW/out
python -m devtools.register_candidates $B certify --jobs-dir SCRATCH/jobs --workers 2
python -m devtools.register_candidates $B controls
python -m devtools.measure_identity --n 130 candidate=evand-cert:cases/register_candidates/$B/certificates/n-130.cert \
  T-259=packet:mishapolk-issue846-2026-10-30 --out cases/register_candidates/$B/measure/identity-n130.json
python -m devtools.register_candidates $B check
```

The 293 and 307 identity measurements are taken the same way, against
`packet:evand-issue845-2026-10-29` and `packet:couzo-issue844-2026-10-28`. The receipts:
all nine jobs came out as required on both routes, 294,402 pair decisions a route in
83.5 route CPU seconds; and all 33 sharp-control decisions as expected, in 313 CPU
seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
