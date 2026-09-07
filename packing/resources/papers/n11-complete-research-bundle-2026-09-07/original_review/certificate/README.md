# Exact fixed-support result from the eleven-square research review

## Result and scope

On the 60 distinct D4 images of the uploaded exact Trump construction, the
maximum almost-everywhere feasible total placement weight is exactly 11.
The seven necessary depth rows checked here prove the upper bound. The known
average of eight valid Trump packings, supplied in the research packet, proves
the matching lower bound.

The packet's candidate weights (1,0,2/5,1/10,0,1/10,3/10,0) are invalid:
their depth is 7/5 throughout a rational box of radius 1/100000 centered at
(97/50,71/50). This is a positive-area violation, not an edge-contact issue.

**This is not a proof that s(11) equals Trump's side, and it does not establish
existence or nonexistence of a full-pose mass-eleven covering density.**
It settles only the declared finite geometric support. It does not change the
historical finite-row result in exp-113 or the overweight-pair result in exp-115.

## Reproduction

Requires Python 3.10 or later and only its standard library:

```sh
python check_support_ceiling.py
python test_support_ceiling.py
python -O check_support_ceiling.py
```

Successful checker output states `EXACT NECESSARY-ROW UPPER BOUND 11; CANDIDATE
REFUTED`. A failed enclosure, row, or arithmetic identity raises a refusal.
The two JSON files are the output retained during this review. Normal and
optimized Python outputs were compared and found identical.

## Mathematical inputs

Source snapshot: 4d305597a505ebfbe85f1851fa7148374661e622 (6 September 2026).
The exact polygon formulas are transcribed from uploaded file
09-trump-construction-and-local-proof.md. The orbit order is supplied by
11-density-contract-candidate-and-results.md: original square representatives
(0,2,4,7,10,8,6,9), sizes (4,8,8,8,8,8,8,8).

The root u is uniquely determined in (36/100,37/100) by
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0.
The checker proves root existence and uniqueness using rational signs and a
100-interval derivative cover, then performs 80 rational bisections. All
geometry uses rational interval operations; no floating-point number decides
any geometric assertion or certificate identity.

Each row is certified on an entire positive-area box. A single necessary
point-depth inequality is justified because incidence is constant throughout
that box. Nonnegative multipliers combine the seven rows to exactly the orbit
size vector, with total multiplier mass 11. No complete arrangement enumeration
is needed for this upper-bound proof.

## Assurance boundary

The test suite uses a second center/projection membership assembly and mutation
controls. It shares the interval arithmetic, root enclosure, and source
geometry with the main checker. These checks are not an independent external
review or proof-assistant formalization. The supplied construction is an explicit
premise for the matching lower bound; this package does not rerun all 55 original
pair contacts or the project's omitted local-isolation computations.

The exploratory floating-point arrangement/LP search was used only to propose
rows and multipliers. It is not needed for verification and is not part of this
proof package.
