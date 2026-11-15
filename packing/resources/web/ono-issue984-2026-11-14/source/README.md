# Squares in a square: a verifiable open-problem benchmark for coding agents

**Question:** what is the smallest square that holds *n* unit squares?
The side length is s(n). For most *n* the optimum is unknown, and the best known packings
are strange: tilted squares at odd angles, found by hand or by search over decades and
tabulated publicly (Erich Friedman's *Packing Center*). Improving one of those records is a
small but genuine open-problem result.

This repo is a **model-agnostic harness** for asking a frontier coding agent to try.
Any agent (Codex, Claude Code, Gemini CLI, ...) gets the same prompt, the same rules
(`AGENTS.md`), the same budget, and the same judge.

## Why this problem

Most "can the model solve open problems?" demos are hard to grade: a plausible-looking
answer is cheap, and checking it is expensive. Here grading is free and exact:

- **Exact verifier.** `verify.py` uses only rational arithmetic (no floats in the decision
  path). Rotations are encoded by rational t = tan(θ/2), so every vertex is rational, and
  overlap is decided by the separating-axis theorem. Rational rotations are dense, so any
  packing with strict slack has an exact certificate.
- **Sound certification.** `certify.py` converts a floating-point packing into an exact
  certificate, repairing rounding by scaling centres apart. This can never create an
  overlap, because for convex bodies the set of forbidden offsets is convex and contains 0.
- **Cross-checked.** The overlap test agrees with an independent exact polygon-clipping
  implementation on 6,000 random pairs, including exact-contact cases.
- **Hard to game.** The verifier and its tests are frozen and hash-pinned
  (`VERIFIER.sha256`). Records must be sourced. The protocol forces a calibration phase
  (reproduce known records from scratch) before any attack, and it treats an honest null
  result as a valid outcome.

## Protocol

| phase | what the agent must do |
|---|---|
| 0. orient | run integrity check and tests, read the verifier |
| 1. state of the art | build a sourced `records.json` for n ≤ 100, rank targets with reasons |
| 2. calibrate | rediscover 3 irregular known records to within 1e-6, from scratch, certified |
| 3. attack | search for improvements on its targets; log every attempt |
| 4. report | per-n results vs. records, candidate claims with a falsification checklist |

## Running a model

```bash
git clone --branch harness-v1 https://github.com/RobertoOno/squares-in-square
cd squares-in-square
python3 -m unittest discover -s tests && sha256sum -c VERIFIER.sha256   # macOS: shasum -a 256 -c
scripts/new_run.sh <model-label> "<agent harness>" "8 hours"
# then paste runs/<date>_<model>/PROMPT.md into the agent, started at the repo root
```

For a fair comparison, every run starts from a fresh clone of the same harness tag, on the
same machine, with the same budget and no human messages after the opening prompt.
`RUN.md` in each run directory records model, harness, machine, timing and any
intervention.

## Auditing a run

1. `sha256sum -c VERIFIER.sha256`, and `git diff harness-v1 -- verify.py tests/` is empty
2. review the sources in `runs/<run>/records.json`, above all for any *n* with a claim.
   A record transcribed too high is the subtle way to fake an improvement
3. re-run `python3 verify.py <cert> --compare runs/<run>/records.json` on every certificate

## Status

Harness ready; no runs yet. Results will land in `runs/`, one directory per model.

## License

MIT
