# Review Programs, 16 October 2026

These are the programs that the stage 4 review lane (W2) of the 16 October intake wrote
and ran for
[`review-2026-10-16-upper-bound-imports-506-607.md`](../../../../../../docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md),
the review of T-185 to T-190 (bead `think-tdna`), with what they printed.
The lane was an AI agent (Claude, strong sub-agent tier, max reasoning).
It wrote the programs in the session’s scratch space and ran them there on 16 October,
from 05:27Z to 06:28Z, against a worktree of `main` at `e2e018f32`.
The addressing agent of PR #648 (Claude, moderate sub-agent tier) copied them here in
the review’s fix round, which answered finding A1 of review A on that pull request.
They live in this packet because its `review/compare_lineage.py` is the import lanes’
shared program for the same six packets.
The review covers six packets, and its programs read all six:

| Key | Packet | Entry | Counts |
| --- | --- | --- | --- |
| `#506-n175` | `couzo-certificates-2026-10-11` | T-185 | 175 |
| `70a033f` | `mishapolk-kkt-refinements-2026-10-14` | T-186 | 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304 |
| `#606` | `evand-n146-2026-10-14` | T-187 | 146 |
| `487b058` | `couzo-verified-bounds-2026-10-14` | T-188 | 211 |
| `#607` | `couzo-certificates-2026-10-14` | T-189 | 237 |
| `4e4c8ce` | `couzo-n237-2026-10-15` | T-190 | 237 |

## What Decides What, and What Is Registered

Only one program here decides a certificate.
`third_route_1016.py` runs `devtools.check_half_angle_area`, which is registered as
`V-check-half-angle-area`.
The driver adds the six packets to that module’s tables in its own process: the keys,
rosters, credit lines and credit readers that a roster commit would add.
It then calls the module’s own `decide-imports`, and it adds no reader and changes no
decision.
`custody.py` checks premises: the pinned trees and files against the packets’
acquisition records.
It decides no certificate.
`adoption_table.py` compares exact sides with the case ceilings, and the other programs
sum or print.
None of those decides anything.

No evidence entry cites any of these programs or outputs yet, and none is in
[`verifiers.yaml`](../../../../../frontier/verifiers.yaml) on its own.
The review’s RT-8 says how the third route’s decision would be cited: its roster lands
in `devtools.check_half_angle_area` with tests, a run writes
`receipts/third-route-2026-10-16.json.xz`, and the confirming evidence lists
V-check-half-angle-area.
The 14 October roster took that path.
Until then, the confirming evidence of T-185 to T-190 rests on the maintained replay,
whose receipts are the import lanes’, and these files are the review’s record of what it
ran.

## Programs

Run each one from `packing/` with the project interpreter.
`P` is this directory’s `programs/`, and `SCRATCH` is a directory outside the repository:

```sh
P=resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/programs
uv run --frozen --all-extras --group dev python -I $P/custody.py SCRATCH \
    couzo-n237-2026-10-15 evand-n146-2026-10-14 mishapolk-kkt-refinements-2026-10-14 \
    couzo-certificates-2026-10-14 couzo-verified-bounds-2026-10-14 couzo-certificates-2026-10-11
uv run --frozen --all-extras --group dev python -I $P/third_route_1016.py --workers 1 \
    --json OUT.json \
    --upstream couzo-certificates-2026-10-11 SCRATCH/couzo-certificates-2026-10-11/tree \
    --upstream mishapolk-kkt-refinements-2026-10-14 SCRATCH/mishapolk-kkt-refinements-2026-10-14/tree \
    --upstream evand-n146-2026-10-14 SCRATCH/evand-n146-2026-10-14/tree \
    --upstream couzo-verified-bounds-2026-10-14 SCRATCH/couzo-verified-bounds-2026-10-14/tree \
    --upstream couzo-certificates-2026-10-14 SCRATCH/couzo-certificates-2026-10-14/tree \
    --upstream couzo-n237-2026-10-15 SCRATCH/couzo-n237-2026-10-15/tree
uv run --frozen --all-extras --group dev python -I $P/summarize_third_route.py OUT.json
uv run --frozen --all-extras --group dev python -I $P/adoption_table.py ADOPTION.json
PYTHONPATH=. uv run --frozen --all-extras --group dev python $P/receipt_totals.py PACKET...
PYTHONPATH=. uv run --frozen --all-extras --group dev python $P/receipt_subsets.py
```

| Program | What it does | What it read | What it printed | Kept output |
| --- | --- | --- | --- | --- |
| `custody.py SCRATCH PACKET...` | Makes one blobless Git clone per source repository over HTTPS, under `SCRATCH/clones/`. This host’s proxy refused the codeload tarballs that the 14 October review fetched. It then holds each packet’s pinned scope to the source at its pin: the pinned commit’s tree must be the recorded `git_tree`, every manifest line’s blob must have its SHA-256, every `pinned_only` entry must have its SHA-256 and byte count, and every retained file under the packet’s `source/` must equal its blob byte for byte. It writes the pinned files to `SCRATCH/PACKET/tree/` for the third route’s `--upstream`. It runs no program of the source. | each packet’s `acquisition/sources.json` and `acquisition/upstream-subtree.sha256`, its `source/` directory, and the six source repositories at their pins | one JSON line per packet: the pin, the tree, 13, 13, 40, 52, 599 and 85 manifest lines (802 in all), 752 `pinned_only` entries and 50 retained files, and no problem, between 05:37:13Z and 05:37:23Z | `outputs/custody.json` |
| `third_route_1016.py` | Adds the six keys above to `devtools.check_half_angle_area`’s tables (`ALL_IMPORTS`, `IMPORTS_1014` and `REGISTERED`, `ROSTERS`, `CREDITED`, `CREDITED_READERS` for T-182, T-183 and T-189, and `ALSO_MEASURED` with #593 for four keys) and runs its `decide-imports`. That command decides each certificate with six controls, compares every side, pose and margin with the maintained routes’ retained inputs, holds each side to the frozen claim record and the citing entry’s claim, makes the `--upstream` checks, and makes the credit measurements (`arrangement_gap`, `unmoved`). | the six packets’ certificates, derived facts, receipts and claim records; `packing/frontier/results.yaml`; the pinned files `custody.py` wrote | 17 certificates passed, 422,712 pairs (8,138 clipped), 102 of 102 controls at their required outcome, 32 upstream checks, no problem; exit 0, 179.76 s, 05:53:37Z to 05:56:37Z | `outputs/third-route-2026-10-16.json.xz` (the `--json` report, 2,036,044 bytes before compression) and `outputs/replay/third-route.log` |
| `summarize_third_route.py REPORT` | Prints the report as the review’s tables, The Third Route and Credit and Lineage. It decides nothing. | the JSON report | per certificate, the least wall clearance, least distance, pairs and controls; per credit line, the symmetry, the squares moved beyond each threshold and the largest move | `outputs/fix-round/third-route-summary.txt`, printed in the fix round from the kept report |
| `adoption_table.py OUT` | Reads each case record’s verified ceiling and each packet’s exact side through `upper_bound_reports.import_side`, with PR #574’s held sides at the counts T-174 shares. It compares them exactly and prints each count’s sides smallest first, rounded up at sixteen places. It decides nothing. | `packing/frontier/n-NNN.md` at the fifteen counts; the six packets; `pingyou-pr574-certificates-2026-10-13` | the comparisons of the review’s Adoption per Count | `outputs/adoption-table.json`; `outputs/fix-round/adoption-table-rerun.txt` is what it printed in the fix round |
| `receipt_totals.py PACKET...` | Sums each packet’s receipt with `upper_bound_reports.receipt_summary`, whole and per count. It decides nothing. | each packet’s `receipts/exact-certification*.json.xz` | the jobs, pair decisions, route CPU seconds and job wall of each receipt (17,256.12 route CPU seconds over the six) | `outputs/fix-round/receipt-totals.txt`, printed in the fix round |
| `receipt_subsets.py` | The same sums over the counts the review names: the cited ones, and #506’s and #607’s uncited remainders. It decides nothing. | the same receipts | at #607’s 22 uncited counts 66 jobs, 31,218,948 pair decisions and 12,382.15 s; at #506’s 14, 42 jobs, 5,142,756 and 2,484.89 s | `outputs/fix-round/receipt-subsets.txt`, printed in the fix round |
| `compare_reports.py ORIGINAL RERUN` | Written in the fix round. It compares two third-route reports field by field, apart from each run’s own `wall_seconds`, `started_utc` and `finished_utc`. It decides nothing. | the kept report and the fix round’s re-run | the number of differing fields | `outputs/fix-round/third-route-comparison.txt` |
| `run_serial.sh`, `chain_inscope.sh`, `chain2.sh` | The shell scripts that ran every heavy command. `run_serial.sh` ran each one niced under one lock file and logged its UTC start, end, wall and exit status. The two chains ran the maintained replays (`upper_bound_reports PACKET check --replay`, with `--n` where the review says), the six `check-claims` and the third route, in that order. Kept as run: they name the lane’s scratch directory and its worktree `review-185`, so they are a record of the commands, not scripts to run here. | | the logs | `outputs/replay/` |

`outputs/replay/` holds one log per command, as `run_serial.sh` wrote it: a start line
with the command, then its output, then an end line with the exit status and wall.
`SUMMARY.txt` lists them all.
`couzo-506-other14.log` is the replay of #506’s 14 uncited counts, which was stopped
unfinished at 06:28:24Z (exit 143).
The review says why, and it claims no reproduction from that run.

## What the Copy Changes

`custody.py`, `summarize_third_route.py`, `receipt_totals.py`, `receipt_subsets.py` and
the three shell scripts are byte for byte the files that ran.
In `third_route_1016.py` and `adoption_table.py`, the copy finds `packing/` from the
file’s own location instead of the review worktree’s absolute path, and their
docstrings name the kept location.
Nothing else changed.

## The Fix Round’s Re-runs

The fix round ran the kept copies again, from the PR branch at `9bd813b2b`.
At that commit `packing/frontier/` and the six packets equal `main` at `e2e018f32`.
The third route read the same pinned trees that `custody.py` wrote on 16 October.

- `third_route_1016.py` exited 0 after 221.15 s, from 07:47:09Z to 07:50:56Z, at a load
  average of about 12. `compare_reports.py` finds its report equal to the kept one in
  every field but the run’s times: 17 certificates, the same 102 controls, 32 upstream
  checks, credit measurements and receipt totals, and no problem
  (`outputs/fix-round/third-route-comparison.txt`, `third-route-rerun.log` and
  `third-route-rerun.json.xz`).
- `adoption_table.py`: its JSON output is identical to `outputs/adoption-table.json`.
- `receipt_totals.py` and `receipt_subsets.py` print the totals the review states.

`custody.py` was not run again: it needs the network and the clones, and the file is
the one that ran.

## Not Kept

- `fetch.sh` tried the codeload tarballs of the six pins. The proxy refused every one
  with HTTP 403, so it fetched nothing and decided nothing; `custody.py` replaced it.
- `claim_docs_readback.py` checked the site cut’s five regenerated claim documents
  against `main` through `git show`. That is the pull request’s release bookkeeping, not
  a run on any result, and kept code may not read Git history
  ([OR-18](../../../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)).
  Its result is in the pull request’s description.
- The clones and the pinned files that `custody.py` wrote are other authors’ bytes, and
  `custody.py` fetches them again at the pins.
  Each packet retains what its source’s licence allows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
