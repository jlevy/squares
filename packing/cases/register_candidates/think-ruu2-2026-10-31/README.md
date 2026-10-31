# Register Candidates Below the Houses of 31 October 2026 (think-ruu2)

The adoption of 31 October 2026 (#852) made eight new house best packings.
Three packings below three of them were found the same day, and each is registered here,
as the house rule asks of every exactly verified packing below a house, however it was
made ([result-import.md](../../../campaign/result-import.md#the-house-rule);
[Register Candidates](../../../../docs/project/guides/regularization-process.md#register-candidates)).

| n | Result | Certificate | Side | Below the house | 12-place print | House |
| ---: | --- | --- | --- | ---: | --- | --- |
| 130 | T-263, held | Evan Daniel’s regularizer’s KKT solve of the house | 1487803830747751967474793359227/(1.25·10²⁹) | 2.500e-13 | …983, the house’s | T-259 |
| 293 | T-262 | T-257’s 260 certificate plus one L strip | 8816991251060941991251052624833/(5·10²⁹) | 8.980e-13 | …122 against …123 | T-257 |
| 307 | T-261 | Evan Daniel’s regularizer’s KKT solve of the house | 4494812820921068365908930695861/(2.5·10²⁹) | 3.752e-12 | …685 against …689 | T-256 |

**130 is held for the owner.** Its side rounds up to its house’s 12-place print, which
makes it a sub-print re-certification in the words of the restatement ruling of 23
October (think-fwa9). The record applies that ruling beyond the corpus only.
Whether it reaches counts inside the corpus is the owner’s question on think-ikku, and
whether it reaches this project’s own regularized views no answer has said: T-155
registered such views at 5.4e-20 to 9.9e-15 below their ceilings, before the ruling.
T-263 is registered and no house moves at 130 until the owner answers.

**293 and 307 cross their prints**, so the ruling does not apply by its words.
Each waits for its stage 4 review, which ran in its own lane on 31 October, and then for
its adoption, which also needs `devtools.select_houses` and
`devtools.upper_bound_houses` to read a certificate this project made.

## Where Each Came From

- **130 and 307** are views of the regularization runs after the adoption
  ([think-3guf-2026-10-31](../../regularized_drawings/think-3guf-2026-10-31/README.md)):
  Evan Daniel’s driver, `regularize_evand run`, solved each new witness to a KKT point
  of the side, and the selection held each view at row 3 of the decision table as a
  register candidate. `register_candidates retain` copied each `view-solved.yaml` from
  the run directory, refusing it unless its Git blob and exact side are those the run’s
  retained `report.json.gz` records (`8a991c28` at 130, `6030dd50` at 307).
- **293** is the senior review of #852’s finding (A3): s(293) ≤ s₂₆₀ + 1, since T-257’s
  260 certificate in [0, S]² with 16 + 16 + 1 axis-aligned unit squares in
  [S, S+1]×[0, S+1] ∪ [0, S+1]×[S, S+1] is a packing of 293 at side S + 1. The
  certificate is rebuilt from the `evand-issue845-2026-10-29` packet’s 260 file, through
  that packet’s custody, wherever it is read, so no copy is kept here.

## What Was Decided

From `packing/`, on 31 October 2026, at most two processes, `nice`, on a four-core host
shared with other lanes:

```sh
B=think-ruu2-2026-10-31
python -m devtools.register_candidates $B retain --run-dir RUNS/adopt-2026-10-31-n130-307-evand
python -m devtools.register_candidates $B certify --jobs-dir SCRATCH/jobs --workers 2
python -m devtools.register_candidates $B controls
python -m devtools.register_candidates $B witness --n 293 --out SCRATCH/l-strip-n293.yaml
python -m devtools.measure_identity --n 130 view=witness-center-basis:cases/register_candidates/$B/views/n-130.yaml.gz \
  T-259=packet:mishapolk-issue846-2026-10-30 --out cases/register_candidates/$B/measure/identity-n130.json
python -m devtools.measure_identity --n 307 view=witness-center-basis:cases/register_candidates/$B/views/n-307.yaml.gz \
  T-256=packet:couzo-issue844-2026-10-28 --out cases/register_candidates/$B/measure/identity-n307.json
python -m devtools.measure_identity --n 293 l-strip=witness-center-basis:SCRATCH/l-strip-n293.yaml \
  T-257=packet:evand-issue845-2026-10-29 --out cases/register_candidates/$B/measure/identity-n293.json
python -m devtools.register_candidates $B check
```

- **Both routes.** The kernel’s three jobs at each count, on
  `sqpack.witness.exact_verify` and `devtools.check_rational_witness_independent`, every
  pair and every wall over Q: the positive accepted, a duplicated square and a square
  moved outside the box refused (`receipts/exact-certification-nNNN.json.xz`). These are
  the checkers the regularization run decided its views with, so for 130 and 307 the
  replay reproduces that decision with the producer’s code.
- **Sharp controls.** The six controls of `devtools.upper_bound_sharp_controls`, each
  accepted at exact contact and refused 1e-30 past it on both routes
  (`receipts/sharp-controls-nNNN.json`).
- **Identity.** A measurement, which decides nothing (`measure/identity-nNNN.json`). At
  130 and 307 nearest centres pair the view with its house one to one under the
  identity: 16 squares move beyond 1e-3 at 130, the largest by 0.0593, with five turned
  by up to 1.84°; 38 at 307, the largest by 0.328, with two turned by up to 0.552°. At
  293 no symmetry of the box pairs the construction with T-257’s 293 certificate square
  for square, so the record does not call it that packing re-dilated.

## Files

| Path | What it is |
| --- | --- |
| `views/n-130.yaml.gz`, `views/n-307.yaml.gz` | The views as the run wrote them, gzipped |
| `receipts/exact-certification-nNNN.json.xz` | The three jobs on both routes, per count |
| `receipts/sharp-controls-nNNN.json` | The six sharp controls on both routes, per count |
| `measure/identity-nNNN.json` | `devtools.measure_identity` against each house |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
