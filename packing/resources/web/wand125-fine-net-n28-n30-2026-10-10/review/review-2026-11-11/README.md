# The Mathematical Review’s Programs, 11 November 2026

These are the programs the
[mathematical review of 11 November 2026](../../../../../../docs/project/reviews/review-2026-11-11-wand125-fine-net-n28-n30.md)
of wand125’s `mixed_n28_L57425` ($s(28) \ge 2297/400$) and `mixed_n30_L58925`
($s(30) \ge 2357/400$) wrote and ran, kept as they ran, with what each wrote in
[`outputs/`](outputs/). The review was lane L93 of bead think-4ul6, under the import
think-i85v: Claude (Anthropic), at the `tbd-strong-max` tier and maximum reasoning,
prompted separately from the replay lane and sharing none of its context.

Each program ran under the project interpreter (CPython 3.14.7, `python3 -I`, numpy
2.5.2, `OPENBLAS_NUM_THREADS=1`), at `nice -n 19` and at most two at a time, from a
scratch copy outside the packet that is byte for byte these files
([`outputs/program-digests.sha256`](outputs/program-digests.sha256)). They read the
packet’s retained candidates and the source’s check2 receipts, run logs, control logs and
pre-publication receipts beside them under `../../release/certificates/`, as data.
No program imports or runs anything of the source, of this repository’s `sqverify_fast`
crate, of `sqpack` or of `devtools`. The standard library does the deciding arithmetic;
numpy holds a float index that only discards images far from a core, the binary64 matrix
product of the axis decision (under the a priori bound below), and the search’s float
estimates, which decide nothing.

## What Its Authors Read

Before writing these programs the lane read the mathematics and the format (the
source’s `SPEC.md`, sections 2 to 5, as the 2026-10-06 check2 packet retains it, byte
for byte the bundles’ copy by digest), the declared-net soundness review of the
maintained crate (6 October), and the n = 31 and #446 fine-net reviews of 23 October.
Those reviews describe the maintained crate’s admission, per-bin domain and quadrant in
words; none reproduces its code. The source’s receipts and logs were read to compare,
never to decide. The lane did not read the source’s adapted crate (pinned, unopened),
its check script, this repository’s `packing/sqverify_fast/` source, the census driver,
or any program of `devtools` or `sqpack`; for the review’s judgment of #892’s axis rule
it read that rule’s description only (the module docstring of
`devtools/sqverify_fast_axis.py` and its `VERIFIERS.md` summary), after these programs
were written. So they are clean-room with respect to the producer’s checker, this
repository’s crate adapted. Each source commit names Claude as co-author, and these
programs were written by a Claude agent: the authorship overlaps the producer’s at the
system family.

## The Programs

| Program | What it does | Decides |
| --- | --- | --- |
| `fnlib.py` | The shared library: a strict reader (one gzip member, no float token, no duplicate key, rationals as `p/q` or decimals), the $D_4$ expansion with coincident images merged, the net’s exact cosines, sines, $r(t)$, $a_j$ and $U_j$, the exact capture of a closed core by clipping each image in fractions, a second exact capture by vertical chords integrated exactly, and a binary64 estimate for the search | through the programs below |
| `premises.py` | Every exact premise of both candidates: identity and the source’s `candidate_digest`, the claim, the rows, the expansion and its invariance, lemma N0’s (a) to (e), the sharp extent, the last bin, and the containment and centre domain at both ends of all 2,073 bins | premises |
| `receipts_check.py` | The source’s receipts, run logs and 197/200 controls read as data and held to the exact evaluator: completeness, totals, the summary’s premises, the exact capture at every rotated direction’s least-bound centre, at the axis argmins and at every control witness | poses |
| `axis_decide.py` | Net index 0 of each certificate, completely: the capture is bilinear on the event grid’s cells, so the least value over the closed quadrant is at a vertex; the vertex values by one binary64 matrix product of exact int64 overlaps under the bound $(1 + \gamma_K)(1 + 2^{-53})^3$, the 64 smallest again in fractions by two methods; with `--factor 99/100`, the mutant | direction 0 |
| `direction_sample.py` | A seeded search for the least capture at 33 rotated directions of each net, every end point evaluated exactly, with the 99/100 mutant’s witness at each | poses |
| `selftest.py` | The two exact methods against each other and the float estimate, the reading against wrong readings at the source’s control witnesses, and the reader and premises against mutated files | nothing (a test) |

## How to Run Them

From the repository root:

```bash
PKT=packing/resources/web/wand125-fine-net-n28-n30-2026-10-10
R=$PKT/review/review-2026-11-11
REL=$PKT/release/certificates
PY="packing/.venv/bin/python3 -I"
export OPENBLAS_NUM_THREADS=1
$PY $R/programs/premises.py --release $REL --out $R/outputs/premises.json
$PY $R/programs/receipts_check.py --release $REL --premises $R/outputs/premises.json \
  --out $R/outputs/receipts-check.json
$PY $R/programs/axis_decide.py --release $REL --out $R/outputs/axis-decision.json
$PY $R/programs/axis_decide.py --release $REL --factor 99/100 \
  --out $R/outputs/axis-decision-99_100.json
$PY $R/programs/direction_sample.py --release $REL --receipts $R/outputs/receipts-check.json \
  --out $R/outputs/direction-sample.json
$PY $R/programs/selftest.py --release $REL --out $R/outputs/selftest.json
```

Each exits 0 and prints its verdict. `selftest.py` writes a mutated candidate beside its
output for a moment and deletes it. The two outputs over 1,000 lines are kept here
gzip-compressed, as `receipts-check.json.gz` and `direction-sample.json.gz`, by
`devtools.retained_data compress`, the packet’s rule for retained data; each decompresses
to the bytes its program wrote (the packet README’s Compressed Files table gives their
digests), and a rerun writes them plain.

## What They Printed

The final pass ran from 11:25:55Z to 11:29:48Z on 11 November 2026
([`outputs/final-pass-utc.txt`](outputs/final-pass-utc.txt)), on a shared four-core
Linux host, and took 255 CPU-seconds; each program’s printed lines are in its
`outputs/*.stdout.txt`.

| Program | Printed | CPU (s) |
| --- | --- | ---: |
| `premises.py` | `PREMISES_HOLD` at both | 0.6 |
| `receipts_check.py` | `ALL_CONSISTENT`: complete logs, 4,144 least-bound centres at or above their bounds, 62 of 62 oblique control fractions equal | 115.8 |
| `axis_decide.py` | `AXIS_DIRECTION_DECIDED`: least axis captures $1.0014141499363902$ and $1.001752883525335$ (rigorous) | 3.7 |
| `axis_decide.py --factor 99/100` | `AXIS_DIRECTION_DECIDED`: the mutant refused at both, exact witnesses $0.99140000843726$ and $0.99173535469025$ | 3.9 |
| `direction_sample.py` | `NO_COUNTEREXAMPLE_IN_SAMPLE`: least found $1.0007906$ (n = 28, direction 1703) and $1.0007095$ (n = 30, direction 2038); a 99/100 witness at all 66 directions | 112.8 |
| `selftest.py` | `PASS` | 18.5 |

The earlier passes, with earlier versions of `fnlib.py`, `premises.py` and
`receipts_check.py`, printed the same verdicts and the same value for every figure both
computed; with them, the trials and two timing probes, the lane used about 11
CPU-minutes.

**What failed along the way.**

- The worktree’s first `uv` environment failed to build: its `vendor/kpress` submodule
  was not checked out. `git submodule update --init` fixed it.
- One line of a control log was read with the `python3` on `PATH` rather than the
  project interpreter, to see the axis row’s format. It decided nothing; every program
  here ran under the project interpreter.
- `selftest.py` first required every wrong reading to reproduce none of the 31 control
  fractions. At n = 28 a wrong step reproduced one and three, all at witnesses where the
  density is constant across the core, so the angle cannot matter. The test now counts
  only angle-sensitive witnesses and checks which they are.
- `direction_sample.py` first used a $33 \times 33$ grid and six starts; it was widened
  to $65 \times 65$, ten starts and the axis argmin’s two before the recorded runs. The
  trial outputs are not kept.
- `receipts_check.py` first counted the 99/100 witnesses at the least-bound centres by a
  float comparison with a margin; it counts them exactly now.
- A check that the source’s public copy of its verifier (wand125/square-packing-tools
  at `5fba675`) exists was refused: GitHub access to that repository is not enabled for
  the session. It was not retried, and the review leaves it as a question.

This review’s runs decide index 0 of each net and evaluate poses; they set no rung. The
complete replay is the census of the replay lane.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
