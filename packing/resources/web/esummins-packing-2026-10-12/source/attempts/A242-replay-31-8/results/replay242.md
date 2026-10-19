# A242 -- replay of T-037 (Kleddamag, s(11) > 31/8): record

Pinned: https://github.com/Kleddamag/11-squares-certified-bound tag v1.0.2 (tag object 59dc5626, commit
6a733f339395c3514f2ab63d8c4aa64cf63c0b5a); every file's sha256 in `ext/PIN.json`; the clone (`ext/repo/`) is
git-ignored.  Certificate sha256 57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458 (matches the
release; NOT with core.autocrlf=true -- the clone was re-checked-out with autocrlf=false).

## Review (every script read before running)

| script | role | network / outside dir | run by A242 |
|---|---|---|---|
| check_integrity.py | sha256 of 54 pinned files | no | yes, twice: PASS 54 |
| verify_threshold_algebra.py | exhaustive k-of-m identity + budget for m = 3, 5 | writes threshold-algebra.json in repo | yes: PASS (CRLF rewrite, restored) |
| exact_mixed.py + integer_sweep.py | the exact sweep (validate, geometry, segment tree) | no (numba import) | yes, via code/rows242.py, all rows |
| replay_parallel.py | Pool driver of the above | no | replaced by rows242 (2-python cap, resumable) |
| independent_controls.py | stdlib containment quadratics + 16 rows of boundary samples | no | yes (after the shards) |
| prepare_secondary.py | downloads R038 upstream JS, applies byte edits | **urllib to raw.githubusercontent.com** | REFUSED |
| replay_secondary_parallel.py, verify.py | node BigInt scan; full launcher | call prepare_secondary (network) + node | REFUSED (node absent too) |

Nothing suspicious found: no shell-outs except node / sys.executable in the launchers, no writes outside the repo
except the user-chosen output paths, the only network access is the documented upstream fetch.

## Independent spot-check (code/spot242.py) -- PASS

See `spot242.json` / `spot242.jsonl`: (a) L/A = 31/8; (b) M = 10999479944 units (point 2247714156, 2-of-3
3188007592, 2-of-5 989672288, 3-of-5 4574085908), D4 invariance; (c) 3,240 exact poses, 0 failures, minimum charge
1000047518, never below the recorded row minimum; (d) 11 Gamma - M = 107864 units.

## Verdict (written by code/final242.py)

**PASS** -- replay PASS_REPLAY_PYTHON_ALL_ROWS, controls PASS_INDEPENDENT_EXACT_CONTROLS, spot-check PASS, integrity PASS (x2).

* rows replayed 12028 / 12028; minimum 999962528 (= Gamma), budget 10999479944, surplus 107864; slabs 86299918, cells 511649694680
* row-by-row against their evidence (minimum, cells, slabs): initial: 0 rows differ, histogram equal True, totals equal True; portable: 0 rows differ, histogram equal True, totals equal True
* runtime: shard wall [3935, 4164] s (pure-Python kernel, 2 shards in parallel, BelowNormal); CPU 8089.2 s summed
* controls: containment 48112; boundary samples 5586 centres, minimum 1000047518
