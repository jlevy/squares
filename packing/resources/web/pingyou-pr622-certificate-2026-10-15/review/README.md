# Review Programs for PR #622’s s(29) Certificate

These are the programs written for the stage 4 review
[review-2026-10-16-pingyou-n29.md](../../../../../docs/project/reviews/review-2026-10-16-pingyou-n29.md)
of PingYou Ltd’s exact rational certificate for $s(29)$
([jlevy/squares#622](https://github.com/jlevy/squares/pull/622)), with everything they
printed. The reviewer is Claude, strong sub-agent tier, max reasoning.

- **Written here:** `programs/n29_exact_review.py`, standard library only;
  `programs/third_route.py`, a driver that only hands the certificate to this
  repository’s third route; and the run script `programs/run_review.sh`. Every decision
  is made in `fractions.Fraction`; floats appear only in the identity measurement, which
  decides nothing.
- **One program of this repository’s ran, at the coordinator’s request.** The review
  lane runs only code it writes
  ([`result-import.md`](../../../../campaign/result-import.md#stage-4-validate), “Who
  reviews, and when”). The coordinator of `think-30n2` asked on 16 October for
  `devtools.check_half_angle_area`, the third exact route, to be run on the witness, so
  that the record could say whether a third route decided it. `third_route.py` runs it
  unchanged, and the route’s readers, decision and controls were read before it ran.
  Nothing of the source’s ran or was read: `VERIFY.py`, `exact_sat.py`,
  `exact_polygon.py`, `build_comparison.py`, `external_inputs.py`,
  `native/convert_witness.py` and `native/replay_upstream.py` are in the asset and were
  left unopened. Nothing of the replay lane’s ran.
- **Order of writing.** The decision (`axes`, `square`, `clearances`, `gap`, `decide` and
  the strict certificate reader) was written from the geometry statement in the asset’s
  `README.txt` and the certificate’s JSON layout. It decided the certificate, and the
  controls ran, at `918b0bd30`, before any of the replay’s code was read. `receipt`,
  `identity`, and the T-009 and source-comparison parts of `sides` came after the
  replay’s receipt, its fact’s layout and its kernel’s control code had been read
  (`devtools/evand_arrangement_reports.py`, `job_input` and the receipt check). They
  read data only, and they decide through the same `decide`.

## What Each Program Does

| Subcommand of `n29_exact_review.py` | Reads | Does |
| --- | --- | --- |
| `certificate ASSET [--member M]` | the release asset, by member, with `zipfile`; nothing is extracted | holds the asset to its pinned size and SHA-256 and the member to its digest; parses `n`, `s_exact` and the 29 poses strictly, each value an integer or a fraction of integers; decides every wall (116) and every pair (406) over Q by separating axes on the squares’ own axes; lists the exact contacts and the least positive slack. With `--member`, it decides a baseline certificate in the same layout |
| `controls ASSET` | the certificate | four mutated copies, each decided in full: square 1 replaced by square 0; square 0 moved by $(-1, 0)$; the touching pair’s second square moved $10^{-3000}$ towards the first along their touching axis; the box shrunk by $10^{-3000}$. Each is held to the violations its mutation must cause, and no others |
| `fact ASSET FACT` | the certificate and the replay’s derived fact, `facts/n-029.yaml.gz` | the fact’s side, centres and axes equal to the certificate’s, square for square, read by a strict line reader of the fact’s layout |
| `native ASSET` | the certificate and the source’s corners witness, `n29-certificate/native/pingyou-20261015-n29-rational.yaml` | the source’s corners equal to the corners computed here, as a set per square, and its side equal to $S$ |
| `sides ASSET REPO` | `packing/frontier/n-029.md`, `packing/frontier/results.yaml` (T-155), the 14 October ledger’s `sources.yaml` (PR #574’s N29 row), T-009’s witness, the house witness at 29, the asset’s three baselines and its `COMPARISON.json` | $S$ against each comparator, exactly; the catalogue print read as a truncation, as rounded to nearest and as rounded up; $S$ against T-009’s Krawczyk enclosure of $s$; and the source’s stated sides and exact gains against the differences computed here |
| `identity ASSET REPO` | the certificate, T-009’s witness, T-155’s view (`packing/cases/regularized_bounds/views/n-029.yaml.gz`) and the house witness (`packing/witnesses/known-best/n-029.yaml`) | the register’s identity measurement: under each of the box’s eight symmetries, nearest-centre pairing, squares moved beyond $10^{-3}$, $10^{-9}$ and $10^{-30}$, the largest move, and the largest turn modulo 90°, the turn taken from exact cross and dot products where the reference gives a rational direction. It measures and decides nothing |
| `receipt ASSET RECEIPT` | the certificate and the replay’s receipt, `receipts/exact-certification.json.xz` | each retained job decided again from its own checker input: the positive held to the certificate, each control held to the one square its mutation changes and the one reason it must be refused for, and each route’s recorded least pair gap and wall clearance held to this program’s |

| `third_route.py ASSET` | the certificate, the derived fact and the source’s corners witness | hands them to `devtools.check_half_angle_area`, unchanged: its own readers (`read_pingyou_json`, `read_fact`, `read_witness_corners`) must give one packing, and its `verdict` decides the fact with its six controls. The route has no `decide-imports` roster for #622, so the driver calls the functions that command calls, and changes none of them |

`run_review.sh WORK ASSETS` runs all of them, and the three baselines, into
`WORK/outputs`, then compares each output with the one kept here.

## How They Were Run

On 2026-10-16, on a shared four-core x86-64 container, one process at a time under
`nice -n 10`, with Python 3.14.7 isolated (`python3.14 -I`). The asset was downloaded
from the release URL below into a scratch directory of its own at about 21:54Z. It came
to 430,075 bytes with SHA-256
`0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537`, the pin, and the
tag `data/pingyou-n29-certificate-2026-10-15-v1` resolved to `318ab94e…` (`git
ls-remote`). The script was then run again through the project interpreter
(`uv run --frozen --all-extras --group dev --project packing python -I`). That run
reproduced every output, field for field apart from CPU and wall times, in about two
minutes. `third_route.py` always runs through the project interpreter, since the route
imports the project’s packages; it took 30 s.

## Reproduce

```sh
A=$(mktemp -d) W=$(mktemp -d)
curl -L -o "$A/pingyou-n29-certificate-2026-10-15.zip" \
  https://github.com/BuddenPing/square-packing-certificates/releases/download/data/pingyou-n29-certificate-2026-10-15-v1/pingyou-n29-certificate-2026-10-15.zip
packing/resources/web/pingyou-pr622-certificate-2026-10-15/review/programs/run_review.sh "$W" "$A"
```

The program refuses an asset that is not the pinned bytes. Set `PYTHON` to a Python 3.14
to run without `uv`.

## What They Printed

Every output is in `outputs/`, as written.

| Output | Result |
| --- | --- |
| `certificate.json` | accepted: 116 walls and 406 pairs decided over Q, no violation, 12 CPU s; $S$ a fraction of 2,399 and 2,398 digits; squares 0 to 14 axis-aligned; one touching pair, 23 and 24 along square 23’s axis $u$; 18 touching walls; least positive pair gap $1.04 \times 10^{-800}$ and wall clearance $1.67 \times 10^{-800}$ |
| `controls.json` | all four refused, each for exactly the expected violations: pair (0, 1); square 0’s left wall; pair (23, 24) alone; the ten top and right wall contacts alone |
| `fact.json` | the replay’s derived fact equals the certificate: side, 29 centres and 29 axes |
| `native.json` | the source’s corners witness equals the corners computed here, and its side equals $S$ |
| `sides.json` | T-155 − $S$ = 1.566165818922113e-36; PR #574’s N29 − $S$ = 7.324826736065141e-90 (the ledger’s side and the asset’s baseline agree); Evan Daniel’s certificate − $S$ = 5.933833462698086e-20; $S$ − 5.93383346267692 = 0.919 of a unit in the print’s last place. $S$ lies inside T-009’s Krawczyk box for $s$, 1.08e-45 above its lower end, and the box shows the catalogue print to be a truncation. $S$ is 2.99e-100 below the house witness’s 100-place numerical side. The source’s side and its three exact gains equal the differences computed here |
| `identity.json` | against T-009’s witness: one to one by index under $y \to L - y$, no square moved beyond $10^{-9}$, largest move 7.685e-20, largest turn 3.255e-38°. Against T-155’s view: three squares moved, by at most 0.01241. Against the house witness: largest move 8.776e-100 |
| `receipt.json` | the positive job’s input is the certificate exactly; each control changes only square 1 or square 0 and is refused here for the one expected reason, at least gap −1 and least clearance −3; both routes’ recorded least gap and clearance equal this program’s in all three jobs |
| `third-route.json` | the route’s three readers give one packing: the fact equals the certificate, and the corners witness holds the same squares. Its verdict: passed, 406 pairs, 54 of them clipped exactly, none overlapping, none outside; least and far-wall clearance 0, 18 wall contacts, closest pair (23, 24) at distance 0. All six controls reach their required outcomes. The route prints a zero distance as `0.000000e+6`, a quirk of its `_root` |
| `baseline-*.json` | the asset’s three baseline certificates (PR #574’s v2, PR #549’s, Evan Daniel’s) each accepted, 406 pairs |

Figures in scientific notation are truncated to 16 significant digits, never rounded up.

## Registration

`third_route.py` decides nothing itself. The run it drives is
`V-check-half-angle-area`’s, already registered, and the exit can cite it in the replay’s
evidence entry, as T-174’s cites its third route.

`certificate`, `controls` and `receipt` decide. Every Run’s Code Is Kept
([epistemics.md](../../../../../epistemics.md#every-runs-code-is-kept)) registers a
deciding program in [`verifiers.yaml`](../../../../frontier/verifiers.yaml) with its
`independence` record, and cites each run from an evidence entry with its coverage.
This lane’s brief leaves the register to the stage 4 exit. Until the exit registers
them, these programs are kept here and no evidence entry cites them. The record the exit
can write:

- `read`: `certificate-format`, `specification` (the asset’s `README.txt` geometry
  statement), and `producer-output` (the source’s `COMPARISON.json` and corners witness,
  read after the decision, to compare);
- `clean_room: true`: the authors never read the producer’s code, and the program shares
  none of it;
- `shares`: none;
- `written_by`: Claude (Anthropic), the stage 4 review lane, strong sub-agent tier, max
  reasoning;
- `overlaps_producer`: `unknown`, since the source names no system behind the PY agentic
  offering; `separate_prompt` and `separate_code` both true. The replay’s routes are
  also Claude lanes’ work, a system-family overlap with the replay and not with the
  producer as far as the record knows;
- coverage `full`: the one certificate, every wall and every pair.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
