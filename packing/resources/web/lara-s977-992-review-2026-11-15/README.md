# Stage 4 Review of #992: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L174’s blind stage 4 review of
issue [#992](https://github.com/jlevy/squares/issues/992),
$s(977) \le 17 + 21/\sqrt2 \approx 31.8492424049$, credited to Miguel Lara and opened by
larasmiguel:
[`docs/project/reviews/review-2026-11-15-lara-992.md`](../../../../docs/project/reviews/review-2026-11-15-lara-992.md).

The source is [larasmiguel/square-s977](https://github.com/larasmiguel/square-s977) at
`26d5695abca2f8a005856e3c1ddc47171d661e9b` (2026-11-15T06:24:28Z), not retained here:
the repository states no licence.
This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `certificates/n977_certificate.md` | `b73d1946060625d550ee3e85b4cb6a3c28b3e67f9db676cc67ed5984c2e74129` |
| `certificates/n977_coordinates.csv` | `a939ed2c0126118c8f2ae3e5fe4914dd01425a7734713a87f55b8cd2cb465035` |
| `verification/verify_977.py` | `ab7a44f8732d85ea1355e0c265d45f536877a5b62aa6f847cf2c17eb76e4f8c1` |
| `verification/n977_verification.json` | `7ae76b44871bbb900b0dcedc8e0e51942b9f96a7e1255a78eb4506872b59955f` |
| `visualization/n977.svg` | `92b5ba93d428345b0470e8eba280078999f63d0d03b44962127522e61d70f9fe` |
| `README.md` | `ba122066381dc4d5b7efa61a8c34681d3d8f857ccf1703e04ebeb12d70339431` |
| `SUBMISSION.md` | `9d4f88ab3a9461c33ce85cbc2e22c8ada62813a70b2948b8b5c5ae8066568d46` |
| `requirements.txt` | `18e424904d71128904806dfe83f9b2c93a5f7ad27dd52d971519a83635561aec` |

There is no exact certificate in the source.
The review rebuilt the construction from the certificate’s argument as an exact file
over $\mathbb{Q}(\sqrt2)$ (`out/constructions/construction-K0.json`) and decided that
file.

## Layout

- `programs/`: the review’s programs, the controls plan, the CSV expectation, the issue
  as fetched.
- `frozen/`: the first freeze’s digest list (checker, construction, plan; 07:11:30Z),
  the findings’ digest list (07:15:34Z) and the frozen review text.
- `out/`: the receipts.
  `out/constructions/` holds the eight files decided before the findings were frozen;
  `out/after-freeze/` the three built and decided after.

## Programs

Every program is lane L174’s own, written for this review as a clean-room
implementation: none imports anything from the source, the deciding programs import
nothing from this repository, and none reuses code of an earlier review.
The review of #989 (lane L169) was the model; its text, packet README and frozen digest
lists were read, and its programs were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a worktree of
`main` at `588ccb226`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l174_reader.py` | the reading: canonical fractions, angles 0 or 45, ids and count | a construction file | nothing (a module) |
| `l174_construct.py` | nothing: builds the recipe of `n977_certificate.md` exactly, and seven variants | nothing | `out/constructions/construction-*.json` |
| `l174_method_a.py` | method A: separating axes on four fixed directions in $\mathbb{Z}[\sqrt2]$, signs by comparing squares | a reading | nothing (a module) |
| `l174_method_b.py` | method B: exact convex clipping in $\mathbb{Q}(\sqrt2)$ over `gmpy2.mpq`, both ways round, walls by outer half-planes, containment by area, unit squares by sides, diagonals and area; signs by Pell brackets | a reading | nothing (a module) |
| `l174_decide.py` | a file by both methods, every square, wall and pair, and their agreement | a construction file | `out/decide-*.json` |
| `l174_selftest.py` | both methods and the reader on hand-derived cases | nothing | `out/selftest.json` |
| `l174_make_plan.py` | nothing: states the controls and their outcomes from the indices | nothing | `programs/controls-plan.json`, `out/plan-facts.json` |
| `l174_compare.py` | each control’s receipts against the plan | plan, receipts | `out/controls.json` |
| `l174_csv_check.py` | nothing about the bound: matches the author’s CSV to the exact construction at 31.85, at $L$ and scaled | the CSV, K0, C7 | `out/csv-check.json` |
| `l174_after_freeze.py` | nothing: builds A981, G982 and G985 with the frozen `build`, and Göbel’s families with L-borders at 970 to 990 | `devtools.goebel_construction` | `out/after-freeze/construction-*.json`, `out/goebel-with-borders.json` |
| `l174_identity.py` | nothing geometric: K0 as a set of exact poses inside G985 and G982 | three construction files | `out/after-freeze/identity.json` |
| `l174_border_audit.py` | nothing about #992: where bordered Göbel members undercut the module, 325 to 2000, and the rows between | `devtools.goebel_construction`, `frontier/source-coverage.yaml` | `out/border-audit.json` |
| `l174_deletion.py` | nothing: the standing side at 325 to 982 against $17 + 21/\sqrt2$ | the same | `out/deletion.json` |

From `packing/`, with `S` the clone at `26d5695` and `R` this directory:

```bash
UV="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
$UV $R/programs/l174_selftest.py SCRATCH_DIR $R/out/selftest.json
$UV $R/programs/l174_make_plan.py $R/programs/controls-plan.json $R/out/plan-facts.json
$UV $R/programs/l174_construct.py $R/out/constructions
for c in K0 C1 C2 C3 C4 C5 C6 C7; do
  $UV $R/programs/l174_decide.py $R/out/constructions/construction-$c.json $R/out/decide-$c.json
done
$UV $R/programs/l174_compare.py $R/programs/controls-plan.json $R/out $R/out/controls.json
$UV $R/programs/l174_csv_check.py $S/certificates/n977_coordinates.csv \
  $R/out/constructions/construction-K0.json $R/out/constructions/construction-C7.json \
  $R/out/csv-check.json
# after the freeze
$UV $R/programs/l174_after_freeze.py $R/out/after-freeze
for c in A981 G982 G985; do
  $UV $R/programs/l174_decide.py $R/out/after-freeze/construction-$c.json $R/out/after-freeze/decide-$c.json
done
$UV $R/programs/l174_identity.py $R/out/constructions/construction-K0.json \
  $R/out/after-freeze/construction-G985.json $R/out/after-freeze/construction-G982.json \
  $R/out/after-freeze/identity.json
$UV $R/programs/l174_border_audit.py $R/out/border-audit.json
$UV $R/programs/l174_deletion.py $R/out/deletion.json
```

## What They Printed

| File | n | Methods agree | Touching | Overlapping | Wall contacts | Verdict |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| K0, the construction | 977 | yes | 3,540 | 0 | 120 | packing |
| C1, box $L - 10^{-6}$ | 977 | yes | 3,540 | 0 | 60 (60 crossing) | not a packing |
| C2, rebuilt at $L - 10^{-6}$ | 977 | yes | 3,484 | 56 | 120 | not a packing |
| C3, $BL(14,1)$ moved | 977 | yes | 3,536 | 1 | 120 | not a packing |
| C4, $D(10,10)$ moved | 977 | yes | 3,532 | 3 | 120 | not a packing |
| C5, $22 \times 22$ diamond | 1,020 | yes | 3,650 | 112 | 120 | not a packing |
| C6, diamond scaled $1 + 10^{-6}$ | 977 | yes | 3,484 | 56 | 120 | not a packing (441 non-unit) |
| C7, rebuilt at 31.85 | 977 | yes | 3,484 | 0 | 120 | packing |
| A981, K0 and four middle squares | 981 | yes | 3,540 | 0 | 124 | packing |
| G982, Göbel $(15, 21)$ and an L-border | 982 | yes | 3,532 | 0 | 122 | packing |
| G985, Göbel $(16, 21)$ taken literally | 985 | yes | 3,556 | 4 | 128 | not a packing |

The self-test passed; every control came out as `programs/controls-plan.json` stated
(`EVERY_CONTROL_AS_STATED`); the CSV matches C7 one to one to $2.9 \times 10^{-15}$.
Method A took under 0.2 s a file and method B 17 to 21 s.

## Freeze Digests

| File | SHA-256 |
| --- | --- |
| `frozen/freeze-1-checker-and-plan.txt` | `fdeb7c247bd5f95a5ff3b38efcb7a76c30a6b56b8eec4e4bc90a3525ec3f07f2` |
| `frozen/findings-frozen-digest.txt` | `80c57e109fc8f538a18a2fec32611148d7c84c201b8d3cefd12eaa5d42c4089d` |
| `frozen/review-2026-11-15-lara-992.frozen.md` | `be1eb0585a1d84f354c0b354dd38808f52fd0ea80fb7136f2cc2865bd5ca474d` |

The first was pushed as `2689e1d7b`, before any construction was decided, and the
findings as `56ea1fd3c`.
