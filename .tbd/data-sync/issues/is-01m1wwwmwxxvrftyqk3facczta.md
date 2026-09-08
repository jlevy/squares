---
type: is
id: is-01m1wwwmwxxvrftyqk3facczta
title: Re-encode Burns's 268-atom certificate as a repository control with row minimum 10003/10000
kind: task
status: closed
priority: 2
version: 4
labels:
  - n17
  - controls
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T02:59:20.093Z
updated_at: 2026-09-07T03:36:04.788Z
closed_at: 2026-09-07T03:36:04.788Z
close_reason: control-burns-4-4811.json rebuilt from the note's constants by build_burns_control.py (--check); exact sweep accepts at least mass 10003/10000; interval route certifies 360/361 directions and stalls at direction 0 on the seam 1/2 + (L-1)/7 = B (recorded in E-n017-burns-control-decision and tested); python -m cases.n17_fractional_certificate --burns-control replays it.
resolution: null
duplicate_of: null
---
BC-115, H-061 and agenda-017 all name 'the retained Burns certificate (268 atoms, total 169476/10000, minimum 10003/10000, so a verifier that only reports 1/1 is caught)' as a positive control, but no fixture encodes it: grep for 10003, 169476 or burns in packing/src, packing/tests and packing/cases finds only docstring attributions and the Massaccesi control. Build it the way packing/cases/n11_fractional_certificate/thirdparty/build_n17_control.py rebuilds Massaccesi's: L = 44811/10000, B = 9973/10000, T = 207107/500000, KMAX = 180, 29-point grid with step (L - 1)/28 from 1/2, the 37 D4 orbit seeds from the note, weights /10000. Run the general exact sweep and the interval decision (sqpack.fractional) on it, retain the outputs, and confirm the least covered mass is 10003/10000 rather than 1 under both verifiers. This is the control whose minimum is not 1, which the Massaccesi control cannot supply.

## Notes

2026-09-07: built packing/cases/n17_fractional_certificate/build_burns_control.py and control-burns-4-4811.json (268 atoms, total 42369/2500 = 169476/10000, declared least 10003/10000, --check confirms the shipped file). Exact sweep via cases.n17_fractional_certificate.__main__.replay: Conditions 1-5 PASS, least cell mass 10003/10000 at direction 0, VERIFIED s(17) >= 44811/10000, 6.9 s wall on CPython 3.14.0rc2. Interval decision pending.
