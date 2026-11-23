# Independent general five-tile path classification

The independent checker classifies all 29,008 local rank/sign profiles for five-tile
forward chains in the one-axis problem at `0 < tan(theta/2) <= 1/24`. It checks all
67,626 normal choices using 417 distinct physical bounds.
It excludes 23,286 profiles from a strict board `S < 5`; the remaining 5,722 are **not
certified by this test**. They are not asserted feasible.

All twenty predeclared controls pass.
The single-jump cases reproduce the accepted bridge result: 3,488 positive-cost
exclusions and 15,696 normal choices.

| Transverse jumps | Profiles | Excluded | Not certified |
| ---: | ---: | ---: | ---: |
| 0 | 560 | 560 | 0 |
| 1 | 3,584 | 3,488 | 96 |
| 2 | 9,408 | 8,392 | 1,016 |
| 3 | 10,752 | 7,976 | 2,776 |
| 4 | 4,704 | 2,870 | 1,834 |
| Total | 29,008 | 23,286 | 5,722 |

## Conditional local result

The local premises are five consecutive forward ranks, transverse rank steps in
`{-1,0,1}`, at most one aligned tile, the reviewed near-grid rank-error intervals, and a
forward separating normal on each of the four pairs.
The checker includes all 259 rank walks and all 112 sign vectors, even profiles that a
particular vacancy pattern cannot realize.

For every normal choice it reconstructs the physical span bound, maximizes rank error
over all 32 box vertices, and obtains a degree-at-most-six polynomial by exact
interpolation after clearing a positive denominator.
Nonnegative Bernstein coefficients on the whole closed interval imply span at least
five, which contradicts a strict board `S < 5`. A failed coefficient test means only
that this sufficient test does not certify the path.

The favorable mixed-diagonal prerequisite is checked strictly over the closed interval.
The scalar calculations include t=0; the positive-angle global reduction and the fully
aligned endpoint remain separate.

The reviewer had already read the producer’s proof, path generator and positivity
program. This checker reuses the first-party arithmetic and physical formulas of the
independently implemented [bridge checker](../review-one-axis-bridges/README.md).
It imports no producer code.
It is not a blind review or a second implementation independent of that first-party
bridge arithmetic.

The [full receipt](general-path-catalogue.json.gz) retains every profile, every
normal-choice reference, every failed choice index, and all bound polynomials with exact
Bernstein coefficients.
Its canonical profile-roster SHA-256 is
`3af5c8ac3620ce9d6f37bade289efd8f4e67a9dc1cb423737cda799ebb33fc32`. The
[retention record](retention.json) binds the original and compressed bytes.

## Frozen inputs and execution

The [specification](general-path-spec.json), [frozen plan](frozen-plan.md),
[freeze](freeze.json), and [checker](checker.py.txt) retain the predeclared coverage,
controls and caps. The freeze’s prepared-only status describes the moment before
execution. The checker bytes are unchanged; their original name was
`check_one_axis_general_paths.py`.

The coordinator ran the isolated project interpreter.
The worker completed in 3.594 supervised seconds, with 2.174 seconds inside the checker
and 69,795,840 bytes peak worker RSS (66.6 MiB). Worker and observer both exited zero.
The three guard samples have maximum pressure 1 and maximum sampled process-tree cost
0.05 GiB; those samples are distinct from the worker peak measurement.
No cap or intervention occurred.

[Supervisor result](execution.run.json), [preflight](execution.preflight.json),
[guard journal](execution.jsonl), [observer log](execution.guard.stderr).

From this directory with Python 3.14 and an external supervisor:

```bash
"$PYTHON" -I -B checker.py.txt --spec general-path-spec.json \
  --output "$OUT/general-path-catalogue.json"
```

Use a new output path, external scratch/cache directories and one worker.
Retain the frozen 60-second outer ceiling, 0.25 GiB sampled process-tree cost ceiling,
pressure-level-2 stop and 55-second internal work ceiling.
The checker also caps distinct bound records and total normal choices.

The 14,993,939-byte original receipt is stored as a 444,111-byte deterministic gzip.
Retention used a 64 KiB streaming buffer, an empty gzip filename and `mtime=0`; it did
not rerun the mathematical checker.

## Remaining global work

This result supplies a complete local catalogue for the exact path criterion.
Applying those exclusions to every occupied-cell path, constructing the Boolean clauses
with correct horizontal/vertical polarity, enumerating all separation graphs, extracting
their geometric rules and proving graph-to-bank coverage are still open.

In particular, the source’s 273,584 graphs and 566 used certificates are still producer
reports. The 5,722 profiles not certified by this test must remain available when global
graph choices are enumerated.
Nothing in this packet asserts that they represent feasible packings.

The one-axis theorem has not cleared Stage 4. No angular-diversity theorem, unrestricted
lower bound, registered result or drawing changes here.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `general-path-catalogue.json.gz` | receipt | `ed24a599b04023febdd50708c7b584fb7f326a9c` | `a60f45a70cb57d4e1a1e58bcbe01b1f9cf1c527fc80c0e931d7e856af22b33bb` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
