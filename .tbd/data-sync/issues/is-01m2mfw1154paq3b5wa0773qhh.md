---
type: is
id: is-01m2mfw1154paq3b5wa0773qhh
title: "PR #181 senior review: script path suffix check trusts a decoy nested literal"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T06:53:34.627Z
updated_at: 2026-09-16T06:58:01.205Z
closed_at: 2026-09-16T06:58:01.204Z
close_reason: "Completed at PR #181 head 8cc783ec: script path checking follows the effective outer expression, rejects decoy .js literals overwritten by .with_suffix('.txt'), requires every alternative to be checked source, and retains positive pathlib coverage."
resolution: null
duplicate_of: null
---
Novel reproducible bypass in packing/devtools/check_no_embedded_js.py lines 584-598. _names_a_script_file returns true when any descendant literal ends in a checked suffix. Therefore page.add_init_script(path=Path('actual.js').with_suffix('.txt')) produces zero sites although the actual loaded file is .txt and outside Biome/tsc. This is a missed post-fix case beyond closed think-tqd8. Fix with a conservative outer-expression path/suffix analysis that recognizes the final effective suffix, and add a negative control watched failing on the current implementation.
