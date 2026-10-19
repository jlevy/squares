# The Third Review’s Programs, 13 and 14 October 2026

These are the programs the
[mathematical-correctness review](../../../../../docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md)
of Overbeck’s candidate wrote and ran on 13 and 14 October 2026, kept as they ran, with
the two logs the lane kept in [`logs/`](logs/).
The review was the third of this candidate, by an AI agent, a Claude model at the
tbd-strong-max tier, reasoning max, prompted separately from the two earlier review
lanes and in a session of its own. It ran each program with the project interpreter
(Python 3.14.7, `python3 -I`) from outside a checkout of the pin, reading the checkout
as data; the release’s large files were not needed. No retained program imports or
evaluates source text. The predicate parser changed at retention, as recorded below.

At retention on 14 October 2026, none of the kept copies had been re-run. During PR
#592 closeout the retained `literal_checks.py` was run at the declared pin under
Python 3.14.7 with `-I -B`, reading JSON only; its
[stdout](logs/literal_checks.log) ends `FAILURES: 0`, with all 15,000 product atoms
matching and exit status 0. It printed 193 passing checks: 192 literal checks and the
partition check. The earlier review reported 194 literal checks; the retained output
states the current run’s count. The original lane kept
the output of two programs; the others’ results are the lines of the review’s section 8
table, and its sections 1 to 4 say what each establishes.

## What Its Authors Read

The review’s section 0 lists what the lane read in full: the statement, the proof text,
the premises, the certificate specification `SPEC_v3.0.md` and the Python tree checker’s
acceptance paths (`wxcheck_v30.py`, sections F to K), the post-check `h_report30.py`, the
capture checkers, the admission scripts `run_adm.py` and `adm.py`, the upper bound’s
`UPPER_FORMULAS.md` and the layout script `UPPER_LAYOUT.py.txt`, the case-partition
script `check_case_partition.py`, and the records of the rigidity part. It did not read
the author’s endpoint programs or the producer’s rigidity code. Its section 9 discloses
that, before writing its findings, it saw the second review’s verdict sentence, which
names a Krawczyk proof of the root box and a Gröbner-basis proof of the base-gap
identities, and the list of that review’s programs in this packet’s README.

So the root isolation, the seed check and the random test of the parallel-pair rows are
clean-room for what they decide: their authors read the statement, the proof text and
the certificate format, and none of the producer’s code for those computations. The
others are independent of the producer’s code, importing and copying none of it, and
not clean-room: their authors read the producer’s code for what they decide.

The source and this review share an AI system family: the edition’s README says it was
produced by Codex and Claude.

## The Programs

| Program | What it does | Reads from the checkout | Output |
| --- | --- | --- | --- |
| [`root_isolation.py`](programs/root_isolation.py) | An exact Krawczyk test on the statement’s isolating rectangle, a central-difference check of the hand-derived Jacobian, five refinements with outward rounding to $10^{-90}$, and $L$, $R$, $C$, $U$ and the 20-place bound compared | nothing: $F$, $G$, $t_0$, $b_0$ transcribed from `STATEMENT.md` | not kept; section 8: $K(X) \subset \operatorname{int} X$, $\lVert I - YJ \rVert \le 4.985 \times 10^{-11}$, $L$ to ninety places |
| [`root_box.py`](programs/root_box.py) | The enclosure of the root and of $L$, as a module the other checks import | nothing | — |
| [`seed_packing_check.py`](programs/seed_packing_check.py) | The rational seed at side $R$: 68 wall conditions and 136 pair separations, exactly | `upper-packing-certificate.json` | not kept; section 8: 68 walls at least 0, minimum exactly $\varepsilon$, 14 flush; 136 pairs separated, none touching |
| [`upper_at_L_check.py`](programs/upper_at_L_check.py) | The construction of `UPPER_FORMULAS.md` at the algebraic root: strict facts by interval arithmetic over `root_box.py`’s enclosure, equalities by reduction modulo a lex Gröbner basis of $(F, G)$ (SymPy) | nothing: the formulas transcribed | [`upper_at_L_check.log`](logs/upper_at_L_check.log), the run in P014’s convention (53 strict and 15 identity walls, 115 strict and 21 touching pairs); the first run’s counts are in the review’s section 2 |
| [`literal_checks.py`](programs/literal_checks.py) | 192 printed literal checks at 83 sites of the proof text’s sections 3 to 6 over the class files, and the case partition re-decided on the product atoms of the six case variables by a decision function of the lane’s own | the 98 capture statements’ `classes.json`, `upper-packing-certificate.json`, the design classes `C_L07.json` and `C_L08.json`, `EXACT_ENDPOINT_AND_CASES.json` | [`literal_checks.log`](logs/literal_checks.log), closeout replay: `FAILURES: 0` |
| [`geom_util.py`](programs/geom_util.py) | Exact convex-polygon helpers for the two programs above and below | — | — |
| [`admission_check.py`](programs/admission_check.py) | The admission of all eleven roots, seventeen labels each, in the lane’s own chart over its own enclosure of $L$, and the distinct parent profiles | the capture statements’ `classes.json`, the root files under `bigbox/join/`, `SELECTED_ORIGINAL_MAP.json`, the design classes | not kept; section 8: every root admitted, profiles distinct, smallest margin exactly 0 at label 1 |
| [`handover_check.py`](programs/handover_check.py) | The three hand-overs of the proof text’s section 8 between the stated EXPECT/JG regions; stored acceptance-report fields are printed for inspection, without deciding their status or comparing their windows | `EXPECT_G20S.json`, `EXPECT_HW.json`, `JG_exact_v2.json`, the two stored acceptance reports | not kept; section 8: `FAILURES: 0`, both cuts necessary |
| [`spec_lemmas_numeric.py`](programs/spec_lemmas_numeric.py) | Random floating-point tests of every lemma of `SPEC_v3.0.md`, seeded | nothing | not kept; section 8: `FAILURES: 0` after one test was moved inside Lemma Pk’s precondition |
| [`jq_leaf_check.py`](programs/jq_leaf_check.py) | A complete checker for the one-node tree certificate `JQ`, written from `SPEC_v3.0.md`: root conditions, the start store, every declaration’s precondition, the term rules, the centred remainder rule and acceptance, with the stored `zero_step_L` compared last | the `JQ` certificate, `upper-packing-certificate.json`, the author’s stored acceptance report of `JQ` | [`jq_leaf_check.log`](logs/jq_leaf_check.log): every condition holds, $\ell \approx 0.0069450 \ge 0.0062505$, $\ell$ equal to the stored value, 161 s |
| [`parallel_row_check.py`](programs/parallel_row_check.py) | A random floating-point test of the parallel-pair row derivation P100 to P106, seeded | nothing | not kept; section 8: 28,326 instances, no failure |
| [`dump_classes.py`](programs/dump_classes.py), [`summarize_obligations.py`](programs/summarize_obligations.py) | Reading aids: a compact print of the class files and of `OBLIGATIONS.json` | the capture statements; `OBLIGATIONS.json` | not kept: they decide nothing, and their output reprints the source, which this packet keeps no byte of |

**Changed at retention.** `literal_checks.py` decided the case partition by passing each
predicate of `EXACT_ENDPOINT_AND_CASES.json` to Python’s `eval`, which executes text from
the source. The record executes no upstream text, so the retained copy replaces that one
line with `holds()`, a parser of the one form the thirteen predicates take (clauses
joined by `and`, each a chain of the six case variables and rationals compared by `<`,
`<=`, `>` or `>=`) that refuses anything else. The change is marked in the file. It was
tested apart from the program, on 40,000 predicates of that form against direct
comparison, before the closeout replay recorded above. The exact replaced `eval` line
was not retained, so its arithmetic semantics and output equivalence are not established.
The closeout replay establishes the retained parser’s own result, recorded as `passed`; the lane’s copy as it ran has the
SHA-256 `4109a2c3c00e8e864ff82b9615af5de87bd605e584f232f498ce5f139a7ebbb4`. Every other
file is byte-identical to the lane’s.

## What They Decide

Each program that verifies something is in
[`verifiers.yaml`](../../../../frontier/verifiers.yaml) with its structured independence
record, and each run that decides or samples a part of the claim has an evidence entry
with its coverage. n-017’s case record cites the entries; T-153 does not, since none is
the complete replay its rungs wait on (epistemics.md, Every Run’s Code Is Kept).

| Program | Registered as | Evidence | Coverage |
| --- | --- | --- | --- |
| `jq_leaf_check.py`, with `spec_lemmas_numeric.py` and `seed_packing_check.py` as premise checks | `V-overbeck-review3-jq-tree-checker`, `V-overbeck-review3-spec-lemmas`, `V-overbeck-review3-seed-packing` | `E-n017-overbeck-jq-tree-review3` | a sample: 1 of the 13 tree certificates, in full |
| `root_isolation.py`, `root_box.py` | `V-overbeck-review3-root-isolation` | `E-n017-overbeck-endpoint-review3` | full: the statement’s rectangle and $L$ |
| `upper_at_L_check.py` | `V-overbeck-review3-upper-at-l` | `E-n017-overbeck-upper-construction-review3` | full: 68 walls and 136 pairs, the 36 contacts by ideal membership |
| `admission_check.py` | `V-overbeck-review3-admission` | `E-n017-overbeck-admission-review3` | full: 11 roots, 17 labels each |
| `literal_checks.py` | `V-overbeck-review3-literal-checks` | `E-n017-overbeck-literal-checks-review3` | full: the 192 printed literal checks over the class files, and the case partition |
| `handover_check.py` | `V-overbeck-review3-handovers` | `E-n017-overbeck-handovers-review3` | full: the three hand-overs |
| `parallel_row_check.py` | `V-overbeck-review3-parallel-rows` | none: a random floating-point test, which decides nothing | — |

## Commands

From `packing/`, with `CLONE` a checkout of the pin:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source kleddamag-n17-candidate-2026-10-12 --checkout CLONE
P=resources/web/kleddamag-n17-candidate-2026-10-12/review-3/programs
.venv/bin/python3 -I -B $P/root_isolation.py
.venv/bin/python3 -I -B $P/seed_packing_check.py CLONE
.venv/bin/python3 -I -B $P/upper_at_L_check.py
.venv/bin/python3 -I -B $P/literal_checks.py CLONE
.venv/bin/python3 -I -B $P/admission_check.py CLONE
.venv/bin/python3 -I -B $P/handover_check.py CLONE
.venv/bin/python3 -I -B $P/spec_lemmas_numeric.py
.venv/bin/python3 -I -B $P/jq_leaf_check.py CLONE
.venv/bin/python3 -I -B $P/parallel_row_check.py
```

`upper_at_L_check.py` needs SymPy, which the project’s environment holds; the others
need only the standard library. `jq_leaf_check.py` takes about three minutes, and the
rest take seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
