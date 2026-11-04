# Second checker: independent exact-integer replay

Written for the review of this claim by an OpenAI Codex agent, without using the lab's
checker or jlevy/squares' `sqverify-fast`. Exact `Fraction` admission and D4 expansion
(`independent.py`), then integer-only branch and bound over each direction's whole centre
domain (`intcheck_final.cpp`, fixed point with unit `2^-42`, directed rounding
throughout, exact rational directions). The argument and the integer-size limits are in
`INTEGER-SOUNDNESS.md`.

- `full.jsonl`: the full replay, 600/600 directions `VERIFIED`, 166.4 M nodes, minimum
  certified lower bound `4398046511113/2^42 = 1.0000000000020…`, 4,801 CPU-s on Apple
  arm64 (`platform.txt`).
- `full.premises.json`, `final_summary.json`: exact premises and the finaliser's summary.
- `GRADE.md`, `GRADE.json`: the reviewer's report (verdict SOUND), including mutant
  controls that are rejected by exact counterexamples. `exact_audit.py` and `finalize.py`
  are the reviewer's scripts as run in its grading directory (paths are relative to it).
- `test_kernels_final.py`, `kernel_probe_final.cpp`, `division_test.cpp`: the kernel and
  division tests described in `INTEGER-SOUNDNESS.md`.

Rerun: `sh run.sh` (all 600 directions) or `sh run.sh 0,144,599`. On x86-64 with g++ 13
directions 0, 144 and 599 give the same node counts and bounds as `full.jsonl`.
