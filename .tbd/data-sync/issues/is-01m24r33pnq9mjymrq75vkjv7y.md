---
type: is
id: is-01m24r33pnq9mjymrq75vkjv7y
title: Parametrise the bin count in devtools/owner_footprints.py
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T04:09:24.436Z
updated_at: 2026-09-10T04:09:24.436Z
---
OR-1: build the tool; never leave a measurement in one-off code.

Agenda-034 lane X4 needed owner-sector footprints at sixteen bins and at the singleton-ray
limit. `packing/devtools/owner_footprints.py` hard-codes eight bins in four places:

  * `owner_branch_manifest` iterates `range(8)`;
  * `_sector_contains` rejects `sector >= 8`;
  * `triangle_footprint` rejects `sector >= 8`;
  * `endpoint_footprint` rejects `sector >= 8`.

The lane parametrised the bin count in a scratch copy rather than touching the tracked
module. That copy is retained as
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-nbins.py.txt`
and it produced a refutation (H-157, exp-154) and two theorems, so it has earned promotion.

What to build. A bin-count parameter `n` on those four entry points, defaulting to 8 so
every existing caller is unchanged. Sector `j` of `n` bins is the closed cone
`[j*2pi/n, (j+1)*2pi/n]`; its two boundary rays are exact elements of `Q[sqrt 2]` for every
`n` dividing 16, so membership stays an exact sign decision on `a + b sqrt 2` and no float
enters a verdict. The scratch copy has the rational wedge vectors for `n = 16` already.

The test is already written and it is an equivalence control, not a new assertion.
`lane-x4-verify-eight.py.txt` checks the parametrised module against the tracked one at
`bins = 8` on four surfaces, at zero disagreements:

  * the membership predicate over 1444 signed rays x 8 sectors, against `_sector_contains`;
  * `sector_endpoint_rays` over 8 sectors;
  * `endpoint_footprint` polygons over all 16 classes, vertex for vertex;
  * class ids and their reflection pairing.

Port it into `packing/tests/` as the promotion's regression: a parametrised module that
disagrees with the tracked eight-bin behaviour anywhere is a broken promotion.

One thing to fix while in there. The lane had to import
`devtools.screen_corner_dual_salvage.screen_footprint` DIRECTLY, bypassing the module's own
entry point, to get around D-489: `_source_receipt` requires the source family's
`verify_ceiling` receipt to carry `failures == ["K3 total weight at least n"]` exactly,
which admits only a family whose total weight is BELOW n and refuses every proved ceiling
family. Any lane that wants to screen against the mass-eleven ceiling family has to do the
same import until D-489 is fixed (carried as think-rm5c). Note the dependency; do not
paper over it here.

Done when the tracked module takes a bin count, the equivalence control runs in the test
suite, and no lane needs a scratch copy of it again.
