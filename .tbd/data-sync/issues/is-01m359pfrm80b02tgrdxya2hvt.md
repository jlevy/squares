---
type: is
id: is-01m359pfrm80b02tgrdxya2hvt
title: "CI repair: mutation-control snapshot 479 KB over the 160 MiB cap on PR 218"
kind: bug
status: closed
priority: 1
version: 6
labels: []
dependencies: []
created_at: 2026-09-22T19:32:46.975Z
updated_at: 2026-09-22T20:28:21.489Z
closed_at: 2026-09-22T20:28:21.488Z
close_reason: "Done in 48f929d3f: agenda-041's retained output pruned (10.6 MB), snapshot 157.6 MB against the unchanged 160 MiB cap, 167 controls fire."
resolution: null
duplicate_of: null
---
The suite-b job fails test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots: snapshot_source_bytes() is 168,221,736 against SNAPSHOT_MAX_BYTES = 160 MiB (167,772,160). Answer it by pruning generated output no mutation control reads, per the standing instruction at SNAPSHOT_MAX_BYTES in packing/devtools/run_negative_controls.py, not by raising the cap. Related: think-t1lk.

## Notes

Resolved by pruning, cap unchanged at 160 MiB. A second, unrelated defect was found by
running the controls and fixed in the same file.

CAP BREACH. Measured with `snapshot_source_bytes()`:
- before: 168,251,525 against 167,772,160, over by 479,365 (hosted `suite-b` read
  168,221,736 on a tree without this session's untracked probe sources)
- after: 157,640,483, 9.66 MiB of headroom

The register's nominated candidate cannot pay. `README.md` links both composite vectors
inline, and the root README is one of the documents `linked_pruned_targets` scans, so
pruning `known-best-1-324.svg` (6,197,909), `known-best-1-100.svg` (2,332,836), or both
leaves `snapshot_source_bytes()` at exactly 168,251,525. Four `check_readme` controls
depend on that copy-back: `check_synopsis.check_links` refuses any relative link whose
target does not exist. No control drives an atlas step at all.

What paid: `campaign/series/.../results/agenda-041` joins `PRUNE` for a net 10,624,188
bytes. Same retained-output class as agendas 031 and 033--035. Nothing outside the
directory names any of it; its eight receipts and three linked companions (202,755
bytes) still reach every worker. Agendas 036--040 examined and excluded: tests read 038
and 040, and `devtools/check_class_record_claims.py` names 040's directory. 036 and 039
are 421,136 bytes together.

BLINDED CONTROLS (separate, branch-introduced, found by running the controls). Commit
a4bdfae4c registered `packing/resources/bibliography.yaml` as a validated dataset at
`devtools/validate_schemas.py:297` while `packing/resources` stayed in `PRUNE`, so
`python3 -m devtools.validate_schemas` raised FileNotFoundError in every worker and all
ten controls driving it were scored as failing. Reproduced identically with and without
the agenda-041 prune, so it is not a consequence of this repair. Fixed by rescuing that
one path into `COPY_SEPARATELY`, which `clone_tree` now copies and
`snapshot_source_bytes` now counts from the same tuple. Structural gap filed as
think-rb73.

Files changed (uncommitted; coordinator owns the commit):
packing/devtools/run_negative_controls.py, packing/tests/test_negative_controls.py.
packing/devtools/controls.yaml needed no change.

think-t1lk narrowed, not closed.
