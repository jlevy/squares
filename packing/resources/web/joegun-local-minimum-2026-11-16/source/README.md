# Upper bounds for s(127), s(204), s(232), s(264) and s(305)

Exact rational packings of unit squares in a square, filed with [jlevy/squares](https://github.com/jlevy/squares) as a registration request.
Each one is a public Kaggle packing by Tomáš Kodaj that we improved further.
They are upper bounds. We make no optimality claim.
Four of the five are local minima by a numerical check, and none is rigid (see Local minimum check).

Reported by JoeGun ([@JonathanGun](https://github.com/JonathanGun)).

## **Claim**

| n | side (exact, rounded up at 12 places) | jlevy/squares record at `31ddae6` | lower by | Kodaj's public side | our part |
|---|---|---|---|---|---|
| 127 | 11.801753890487 | 11.8108787875891799 | 9.1249e-3 | 11.801765635430 | 1.174e-5 |
| 204 | 14.802646843107 | 14.8043613836518588 | 1.7145e-3 | 14.802646907234 | 6.41e-8 |
| 232 | 15.759531627557 | 15.7614096448817244 | 1.8780e-3 | 15.759531732104 | 1.045e-7 |
| 264 | 16.773807598002 | 16.7747351323878329 | 9.275e-4 | 16.773891500852 | 8.390e-5 |
| 305 | 17.945762359659 | 17.9504664821377123 | 4.7041e-3 | 17.946298110350 | 5.358e-4 |

"Our part" is Kodaj's side minus ours. The rest of each gain is his.

## **Files**

| file | what |
|---|---|
| `n-NNN-candidate.yaml` | the packing as a `packing.squares:Witness/v2` file with rational corners |
| `n-NNN-decimal-pose.yaml` | the f64 pose (centre and turn in radians) that the witness was made from |
| `make-pose.py` | writes a pose file from rows of centre x, centre y and turn in radians |
| `packing-witness-verify.txt` | output of `packing-witness verify` from jlevy/squares `main` at `31ddae6` |
| `check.py` | our own exact checker, written apart from the registry's code |
| `check-output.txt` | its output |
| `local-minimum/` | input, log and output of the local minimum check for each count |
| `LICENSE-evand-square-packing.txt` | Evan Daniel's MIT notice, for his quench code and his `exactsolve.py` |

SHA-256 of the witnesses:

```
9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0  n-127-candidate.yaml
1daa0e09b5b403e4e47048104c760f3d8a9b6997d77d26a30930bf1e257ea90c  n-204-candidate.yaml
93d856c25c9f75842ca5e36552ccb726e87884440689c9ce4100d2a58d5a279d  n-232-candidate.yaml
14fef8f163b2cdb9062f714cdd41d81dce2447691a2de55e3797810cdcd676ee  n-264-candidate.yaml
14d2e37e22218defb238e0b0e657f139bab0c2873cc3d05f781b0f3b13a75494  n-305-candidate.yaml
```

The `softschema.schema` field names `packing/witnesses/witness.schema.yaml` of jlevy/squares. This repository has no copy of it.

## **Rerun**

```bash
# the registry's verifier, from a jlevy/squares checkout
cp n-127-candidate.yaml <squares>/packing/witnesses/known-best/zz-cand.yaml
cd <squares>/packing
uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify witnesses/known-best/zz-cand.yaml

# our checker, from this repository (needs pyyaml)
python3 check.py n-*-candidate.yaml
```

We ran `packing-witness` from a sparse checkout of `31ddae6`. It held `packing/src`, the project files, the witness schema, and one file under each folder that the tool's layout check looks for.
`PACKING_PROJECT_ROOT` pointed at it, and the witness files stayed in this folder.
The tool's code was not changed.

## **How the exact coordinates were made**

- Our search keeps each packing as f64 centres and turns.
- Before export, every centre is pushed away from the centroid by a factor of at least 1 + 1e-12. This keeps touching squares apart as doubles.
- `n-NNN-decimal-pose.yaml` is that pose, written with the shortest decimal that reads back as the same double.
- `packing-witness promote --strategy robust-rational --max-side-increase 1e-11` (jlevy/squares at `31ddae6`) turned it into rational corners. It reports `center_dilation: '1'` and 36 rational digits for all five.

## **Checking**

- `packing-witness verify` says `VERIFIED` for all five, method exact-algebraic. It tested 8,001, 20,706, 26,796, 34,716 and 46,360 pairs.
- `check.py` says `VALID` for all five. It works in `Fraction` arithmetic with no tolerance and no distance filter. It checks that every square is a unit square, that every corner is inside the box, and that every pair is separated along one of its four edge directions.
- `check.py` refused three broken copies of the n = 127 witness:
  - the side lowered by 1e-30
  - square 2 placed on square 1
  - one corner moved by 1e-30
- Each exact side minus the record's exact side is negative in `Fraction` arithmetic.

The promotion used the registry's own tool. Therefore `packing-witness verify` does not check the rounding independently. `check.py` shares only the definitions (unit square, box, disjoint interiors) and the YAML file.

## **Local minimum check**

We ran `exactsolve.py` from [evand/square-packing](https://github.com/evand/square-packing) (MIT, at `6067db5`) on all five packings. It gave a result for four of them.

| n | KKT point | local minimum | rigid | flat motions | least contact force | side at the exact point |
|---|---|---|---|---|---|---|
| 127 | yes | yes | no | 52 | 6.66e-8 | 11.801753890364738880 |
| 204 | no result | no result | no result | | | |
| 232 | yes | yes | no | 110 | 7.28e-7 | 15.759531623540125992 |
| 264 | yes | yes | no | 155 | 6.75e-7 | 16.773807597982933201 |
| 305 | yes | yes | no | 132 | 2.55e-6 | 17.945762359467513364 |

The tool works in 80-digit arithmetic. Its steps:

- It lists the contacts of the input (corner on side, corner on wall).
- It solves for the nearby point where those contacts are exact. The Newton residual ends below 1e-70.
- It looks for contact forces that are all above zero and balance every square. That is the KKT condition.
- It checks the reduced Hessian of the Lagrangian on the directions that the contacts leave free.
- It tests every corner-on-corner touch as a choice between separating lines (MILP).

How to read the table:

- **KKT point.** The contact forces are positive and the balance residual is 0.
- **Local minimum.** The tool's verdict is "local minimum of S, strict modulo N exact flat motions". A flat motion is a slide of some squares that keeps the side the same. No small move makes the side shorter.
- **Rigid.** No. The flat motions mean that the packing can move, so it is not isolated.
- **n = 204.** Its load rests on 30 corner-on-corner touches. The tool found no smooth equilibrium, and its Newton step diverged. There is no result in either direction.

Limits of this check:

- It is a numerical check at 80 digits. It is not a proof.
- The result is about the exact touching point in `local-minimum/n-NNN-input.exact.txt`. The witnesses above are loosened copies of that point. Their sides are larger by 1.9e-11 to 4.0e-9.
- The tool wrote its own rational certificate for each exact point (`n-NNN-input.cert`, its exact check says `VALID`). We do not claim those lower sides here.
- At n = 232 the tool moved 22 loose squares into the contact system. The least gap between pairs that do not touch is 1.5e-12 there.
- One tool by one author made this check. We did not run the `local_rigidity` code of jlevy/squares.

To rerun, from a checkout of evand/square-packing at `6067db5`:

```bash
PYTHONPATH=search/exact:search/packer uv run --python 3.13 \
  --with numpy==2.4.2 --with scipy==1.17.0 --with mpmath==1.3.0 --with sympy==1.14.0 \
  python search/exact/exactsolve.py <this repository>/local-minimum/n-127-input.txt --out out/
```

`local-minimum/make-input.py` writes the input file from a pose file. The package versions are the ones that the tool's own `env.sh` pins.

## **Lineage and credit**

- **Tomáš Kodaj** published all five parent packings in his Kaggle notebook [Squares in Squares | [22.1636]](https://www.kaggle.com/code/tomkodaj/squares-in-squares-22-1636). Its last run was 2026-11-13 09:48 UTC. We downloaded it at 10:17 UTC that day. We did not trace what his packings build on.
- **Our steps** on top of his packings:

| n | step | when (UTC) | side after |
|---|---|---|---|
| 127 | fault-line DP | 2026-11-13 10:42 | 11.80175389 |
| 204 | fault-line DP | 2026-11-13 10:42 | 14.80264684 |
| 232 | fault-line DP | 2026-11-13 10:42 | 15.75953163 |
| 264 | quench, 600 s | 2026-11-14 09:42 | 16.77380760 |
| 305 | quench, two runs | 2026-11-13 13:41 | 17.94578855 |
| 305 | fault-line DP | 2026-11-13 23:40 | 17.94576236 |

- **Fault-line DP** is our own method. It cuts pieces out of other packings along lines that no square crosses. A dynamic programme then joins the pieces into a packing of the wanted count. The donor packings are our own and public Kaggle ones. We did not record which donors the winning pieces came from.
- **The quench** is Evan Daniel's code from [evand/square-packing](https://github.com/evand/square-packing) (MIT, at `6067db5`). His notice is in `LICENSE-evand-square-packing.txt`.

Suggested credit: Tomáš Kodaj as finder at all five counts, improved by JoeGun. At 204 and 232 our part is below 2e-7, so credit to Kodaj alone is fair there.

## **Not done**

- No local minimum result at n = 204.
- No proof of the local minimum results. They are numerical.
- No proof-assistant check and no human review outside this project.
- No measurement of the least pair margin or of the contraction margin.
- The licence of Kodaj's notebook was not checked.

## **Other public values**

The Kaggle per-puzzle leaderboard (read 2026-11-16 04:38 UTC) lists side-only entries below ours at all five counts. They state no packing, so we could not check them.

| n | leaderboard side | team |
|---|---|---|
| 127 | 11.800793726617 | nubx |
| 204 | 14.802436041464 | Luka Cvetkovic |
| 232 | 15.758852775266 | Robson |
| 264 | 16.770127228405 | Shadoks |
| 305 | 17.945755838742 | Shadoks |

Kodaj's notebook also holds n = 270 at 16.927469594094, below the record's 16.928148603343. We did not improve it, so it is not claimed here.

## **AI assistance**

AI agents wrote and ran the search code, the checker and this filing. They also ran the local minimum check. JoeGun directed the work.

## **Licence**

See `LICENSE.md`. The witnesses, poses, outputs and text are CC BY 4.0. The scripts are MIT.
