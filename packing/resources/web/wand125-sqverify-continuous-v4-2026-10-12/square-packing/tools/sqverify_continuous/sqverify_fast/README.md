# sqverify-fast

A clean-room verifier for measure-capture lower-bound certificates: given a nonnegative
measure on $[0, L]^2$ of mass below $n$, it checks that every shrunk square of side $B$,
at each net direction (201 by default) and every centre, captures at least the threshold,
which proves $s(n) \ge L$. It is lane W2 of `think-gpe0`, written without reading the
authors’ checkers ([INDEPENDENCE.md](INDEPENDENCE.md)), with every lemma it relies on
proved in [SOUNDNESS.md](SOUNDNESS.md).

Milestones A and B are implemented: exact admission of formats T (Tokoharu’s rectangle
densities), M (rectangle rows, per-bin centre domain) and L (points, segments and
rectangles); the axis direction of a rectangle measure by an exact-event vertex sweep;
every other direction, and direction zero of a measure with points or segments, by
interval branch and bound.
Continuous-angle covers (formats D and P) are not.

## Use

From `packing/sqverify_fast/`, `cargo build --release`, then:

```bash
target/release/sqverify-fast --candidate PATH.json.gz --n N [--side P/Q] \
    [--directions all|a-b|r1,r2] [--threshold P/Q] [--threads K] \
    [--receipts DIR] [--confirm]
```

Standard output is one JSON receipt per direction and a summary line; the exit status is
0 only when every requested direction is verified (`VERIFIED` for the whole net,
`PARTIAL` for a subset), 1 when one is refused, and 2 on an admission refusal.
The default threshold is the certificate’s declared one, else 1.
A format M candidate may declare a finer uniform net as `proof_net: {"step": "1/1001",
"last": 415}`; admission checks the net premises for it (SOUNDNESS.md, Formats M and
L). `--confirm` evaluates a
refusal’s witness in exact rationals.
`--probe r,x,y[,dx,dy]` prints the certified centre (and box) bound and the
counterexample estimate beside the exact capture, for differential tests.
`--audit-every K` (default 1024) sets the release audit’s sampling, `1` audits every
box. `--inject-fault-at-node N` is a control: its run is never verified, and every
receipt records the injected box.
A direction’s verdict is `verified` or one of the refusals `counterexample-candidate`,
`unresolved`, `audit-failed`, `non-finite` (an enclosure that is not finite, which lemma
F3 rules out for an admitted certificate) and `fault-injected`; the axis sweep says
`refused` or `non-finite`.

## Checks

- `cargo test --release`: unit, property and exact-oracle tests.
- `packing-validate --only "measure verifier Rust"`: fmt, clippy, tests, docs, release
  build, then `devtools.check_sqverify_fast --quick` (differential against
  `sqpack.rectangle_density` and the mutation controls).
  Without `--quick` the check covers more certificates and directions.
- `devtools.sqverify_fast_census`: every replayed certificate at all 201 directions;
  results and the generated tables are in
  [`benchmarks/measure-verifier/census/`](../benchmarks/measure-verifier/census/)
  (format T) and
  [`benchmarks/measure-verifier/census-mixed/`](../benchmarks/measure-verifier/census-mixed/)
  (formats M and L, with the authors’ CPU on the directions they replayed).

## How to Resume

Everything needed is on the branch; nothing lives only in a session.

1. Read [SOUNDNESS.md](SOUNDNESS.md) (the obligations every change must keep) and the
   clean-room rule at the top of [INDEPENDENCE.md](INDEPENDENCE.md).
   Append to the independence record every file you read and every command you run.
2. The performance campaign is
   [`benchmarks/measure-verifier/`](../benchmarks/measure-verifier/): its README is the
   runbook (metric vector, accept rule, commands), `ideas.md` the idea board,
   `hypotheses/` the registry, `experiments/` one record per round, `results/` the raw
   JSONL. The standing best build is the one the latest accepted experiment produced,
   which is the committed source.
3. To run one round: build the control and the candidate, copy both binaries aside, then
   from `packing/` run `python -m benchmarks.bench_measure_verifier --arm
   fast:control=A --arm fast:candidate=B --callgrind --repeats 1 --cells
   rect_n32_L595@r1,rect_n32_L595@r100,rect_n61_L796@r100 --out results/exp-NNN.jsonl`,
   then the same without `--callgrind` and with `--repeats 2` for the CPU guard.
   Apply the accept rule and write the experiment record, whatever the verdict.
4. To extend the census, `python -m devtools.sqverify_fast_census --binary
   sqverify_fast/target/release/sqverify-fast --out benchmarks/measure-verifier/census
   --threads 2 --resume`, then `--report` to regenerate its table and `--check` to
   confirm every case; add `--family mixed` and `--out
   benchmarks/measure-verifier/census-mixed` for formats M and L.
5. Open work is in the beads under `think-gpe0`: `think-tgra` (this loop), `think-j1pd`
   (a reference timing route for `verify.cpp` at any direction).
   The release audit (`think-na5a`) and points and segments (`think-4vf7`) are done.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
