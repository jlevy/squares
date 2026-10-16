Version: v1.2 (2026-10-15), source SHA-256 f3629c29d682a9dd3c7acc42770207bfd1f2386cd6c38f0328cc755175e3c86e (see VERSION.json; v1.2 renames the candidate format label to `mixed`, v1.1 added --resume). Kernel from Guzhou0806/n40-square-packing (MIT), commit 71c97d0.

# Deviations and adjustments from SPEC.md

- **Axis density scale:** x28 needs density denominator 10^8 instead of the
  upstream generator's 10^9 to satisfy the unchanged total-coefficient guard.
  Coordinates still use the required 10^9 grid. Densities are rounded downward;
  the kernel already supports separate coordinate and density denominators.
  n40 retains 10^9 for both and reproduces the frozen inputs byte for byte.
- **Control execution:** the axis patch runs first. Both reduced-mass controls
  are REFUSED there, so their continuous slabs are skipped. No x28 main run
  was performed. All other requested work is implemented.

# Continuous-pose rectangle-density checker

This is independent input generation and orchestration around the MIT kernel
from Guzhou0806/n40-square-packing, commit `71c97d0`. All work and inputs stay
inside this folder. See [PROVENANCE.md](PROVENANCE.md),
[CHANGES.md](CHANGES.md), and the supplied [proof](upstream/PROOF.md).

For an exact D4-symmetric rectangle measure on `[0,L]^2`, the checker proves
that every contained closed square of side B, at every center and angle,
captures at least tau. With exact `n*tau > M` this excludes n interior-disjoint
unit squares in a square of side L/B. Compactness gives the strict claim
`s(n) > L/B`. Rectangle boundaries have zero mass.

Both the Guzhou rectangles/weights format and the mixed rectangle format are
parsed with exact rational arithmetic, including JSON decimals. Each
representative mass is divided among all eight D4 images, retaining
multiplicity. Negative masses, incorrect totals, unsupported nonempty points,
and invalid supports are refused. The candidate's old B and proof-net metadata
are ignored. Optional Guzhou parameters cross-check L, n, and total mass;
command-line B and tau determine the new check.

## Reproduce on Ubuntu

Install Python 3.10 or later and a C++17 compiler:

```sh
sudo apt-get update
sudo apt-get install python3 build-essential
python3 tests/run.py
python3 check.py --candidate upstream/certificate/certified_candidate.json --params upstream/certificate/parameters.json --n 40 --core 199529/200000 --tau 4999/5000 --workers 2 --label n40
python3 make_control.py
python3 check.py --candidate inputs/n40.mass0985.json --n 40 --core 199529/200000 --tau 4999/5000 --workers 2 --label n40-control
python3 check.py --candidate inputs/x28-57425-b9977-net05.mass0985.json --n 28 --core 499/500 --tau 1 --workers 2 --label x28-control
```

There are no Python dependencies. Kernels build into `build/` using
`c++ -O2 -std=c++17 -fno-fast-math -ffp-contract=off`. Source, compiler, flags,
and binary changes invalidate the build cache. Assertions remain enabled.
Controls intentionally exit 1; a successful proof is the only exit-0 result.
Each invocation has an overall 2,400-second deadline and at most two workers.
The axis grid uses at most 5.76 GB for coefficient arrays, below the 8 GB limit;
it runs before the slab workers. The supplied cases need less than the cap.

Exact x28 main command (intentionally **not run** here):

```sh
python3 check.py --candidate inputs/x28-57425-b9977-net05.json --n 28 --core 499/500 --tau 1 --workers 2 --node-budget 1000000000 --timeout 2400 --label x28-main
```

Its target claim is `s(28) > 22917169/3992000`. The timeout may refuse this large
case; the expected result is not treated as evidence of verification.

## Inputs and receipts

`--node-budget` limits each slab (default 30,000,000). `--endpoints` accepts
strictly increasing integer numerators over 1,000,000, separated by spaces or
commas. For example, inserting 250 into the default sequence refines the first
slab. The default is `1,500,10000,20000,...,410000,415000` (43 slabs).
`--label` selects `runs/<label>/`; rerunning a label replaces its artifacts.
`--timeout` can reduce, but not exceed, the 40-minute cap.

The standalone generator can be invoked as:

```sh
python3 generator.py --candidate inputs/x28-57425-b9977-net05.json --core 499/500 --tau 1 --out runs/x28-inputs
```

Generated `certificate_input.txt` encloses coordinates, density, L and B
outward in binary64. The shared kernel uses these intervals conservatively
for lower capture bounds. `axis_input.txt` rounds support inward and density
downward. Coordinates use the 10^9 grid; the density denominator starts at
10^9 and is reduced by powers of ten only as needed to retain the unchanged
coefficient and signed-128-bit guards (10^8 for x28). The integer capture scale
is `density_denominator * 10^18`. A is a strictly smaller even grid side satisfying
`B - A*(1+2*epsilon-epsilon^2)/(1+epsilon^2) > 0` exactly. On the supported
near-axis interval this bounds cos(theta)+sin(theta), with
`theta = 2*atan(t)`. The frozen n40 A is reproduced exactly.

`manifest.json` contains the certificate and optional parameter SHA-256,
both generated input hashes, exact masses and the containment margin.
`receipt.json` binds the manifest and includes exact premises, the proposed
claim, build identities, raw kernel outputs, slab nodes/leaves/timing/minimum
bounds, and unresolved normalized pose boxes if emitted. An unresolved box
is diagnostic, not a proved counterexample. REFUSED can mean failed coverage,
invalid input, exhausted budget, or timeout; it never certifies the claim.
A REFUSED receipt may still contain its *proposed* claim.

Acceptance requires all of the following:

- Exact positive counting and geometry margins: `n*tau-M > 0` and `L^2-2B^2 > 0`.
- Contiguous slabs from epsilon to last_t, with
  `last_t^2+2*last_t-1 >= 0`, hence `last_t >= tan(pi/8)`.
- Every slab exits successfully and reports verified, echoes its actual
  arguments and input hash, has `nodes == 2*leaves-1`, and reports a finite
  lower bound at least tau. Depth and split counts are also checked.
- The axis kernel proves the full breakpoint grid, reconciles its minimum by
  direct summation, matches its input hash and arguments, and gives an exact
  minimum at least tau. Integer safety guards and symmetry checks must pass.
- The exact near-axis containment margin is positive; generated inputs and
  certificate hashes remain unchanged through acceptance.

Unsupported exact inputs fail closed: L must have an even integer representation
on the 10^9 grid, positive expanded rectangle count must be at most 20,000,
L must be below 12, and the axis threshold numerator and denominator must be
at most 1,000,000. Epsilon must be at most 1/1000. These conservative bounds
include all supplied inputs. Soundness still depends on the shared mathematical
kernel, compiler, and IEEE binary64 semantics; this is not a formal proof assistant.

## Recorded results

All runs used at most two kernel workers and a 2,400-second cap. The regression
completed in about 12.1 minutes; each control completed in under one second.

| Run | Result | Evidence |
| --- | --- | --- |
| n40 regression | VERIFIED | All 43 slabs; 61,860,927 nodes; 30,930,485 leaves; exact claim `s(40) > 1340000/199529` |
| n40 mass × 0.985 | REFUSED | Axis minimum below `4999/5000`; no slabs required |
| x28 mass × 0.985 | REFUSED | Axis minimum below `1`; no slabs required |
| Unit tests | PASSED | 11 tests, zero failures and errors |

The n40 node and leaf counts match the upstream run exactly. Its exact axis
minimum is `249950896232809301864786207/250000000000000000000000000`, on a
2213 × 2213 grid. The positive counting margin is `1/500`; the near-axis
containment margin is `589499411/125000000000125000`.

The n40 control's exact rounded-measure axis minimum is
`984806531155579583867044528/1000000000000000000000000000`.
The x28 control's is
`98701424597232956334739053/100000000000000000000000000`, on a
3586 × 3586 grid. Both kernels returned `AXIS_TEST_REFUSED`, with successful
minimizer direct-sum reconciliation and matching argument/input identities.
These are actual coverage-check refusals, not parse failures or budget timeouts.
The control minima refer to the conservatively rounded axis measure; no
counterexample to the continuous-pose claim is inferred from them.

The unit tests cover both supplied formats, synthetic D4 multiplicity and
mass, missing-mass CLI refusal, unsupported points, invalid inputs, exact
outward rounding, frozen n40 input hashes, heavy mixed-measure density scaling, and
rejection of malformed/tampered slab receipts.

### Copied receipt summaries

[n40 receipt](runs/n40/receipt.json):

```json
{
  "claim": "s(40) > 1340000/199529",
  "errors": [],
  "leaves": 30930485,
  "nodes": 61860927,
  "seconds": 727.9606603340071,
  "slabs_completed": 43,
  "status": "VERIFIED"
}
```

[n40-control receipt](runs/n40-control/receipt.json):

```json
{
  "claim": "s(40) > 1340000/199529",
  "errors": [
    "Axis coverage refused"
  ],
  "leaves": 0,
  "nodes": 0,
  "seconds": 0.5220002499991097,
  "slabs_completed": 0,
  "status": "REFUSED"
}
```

[x28-control receipt](runs/x28-control/receipt.json):

```json
{
  "claim": "s(28) > 22917169/3992000",
  "errors": [
    "Axis coverage refused"
  ],
  "leaves": 0,
  "nodes": 0,
  "seconds": 0.5470065830013482,
  "slabs_completed": 0,
  "status": "REFUSED"
}
```

[Unit-test summary](runs/unit-tests.json), [full log](runs/unit-tests.log):

```json
{
  "errors": 0,
  "failures": 0,
  "seconds": 1.1074628329952247,
  "status": "PASSED",
  "tests": 11
}
```
