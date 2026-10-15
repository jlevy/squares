# Test fixtures

`intervals.json` is an unchanged copy of the published closed-form interval
metadata. It supplies the 34-interval coverage and closed-form regression tests;
no record bundle is needed. Its hashes refer to the full external assets.

CLI tests generate tiny synthetic families and two-root records in temporary
subdirectories of `tests/`, removing them afterwards. They cover mutation
refusals, partial results, deadlines, and checkpoint integrity and completion.
The full-bundle family, replay-prefix, scheduler, and historical-checkpoint
integration tests are omitted from this publication copy. Arithmetic, geometry,
leaf, tiling, and scheduler unit tests and polynomial comparison tests remain.
No extracted record or reduced checksum manifest is included.
