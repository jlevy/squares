---
type: is
id: is-01m1yex4abjf79dwc50e4f2nrs
title: "Future: Greek sizing inside the composite (scale KaTeX Greek to PT Serif's x-height)"
kind: feature
status: closed
priority: 3
version: 3
spec_path: vendor/kpress/docs/math-text-face.plan.md
labels:
  - kpress
  - future
dependencies: []
parent_id: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T17:33:24.682Z
updated_at: 2026-09-07T17:44:00.672Z
closed_at: 2026-09-07T17:44:00.671Z
close_reason: Moved to the kpress tracker as kpr-c2tr (the feature lives in vendor/kpress on squares/page-fixes; see vendor/kpress/docs/math-text-face.plan.md).
resolution: canceled
duplicate_of: null
---
Deferred by the owner on 2026-09-07. Keep KaTeX's Greek glyphs but give the Greek ranges of KaTeX_Math-Italic and KaTeX_Main their own faces inside KPress Math Text with a small size-adjust and matching metrics, so theta and pi sit at PT Serif's x-height beside PT Serif letters. Judge on the montage; not to be started until the PT Serif feature has shipped.

## Notes

Prototyped 2026-09-07 as route J on the recommended page: KaTeX_Math-Italic Greek range at size-adjust 113.4% (x-height match) and KaTeX_Main Greek capitals at 102.5% (cap-height match), metrics scaled by the same factors. Reads as an improvement: theta, pi and mu reach PT Serif's letter height and nearly its weight. Two @font-face rules plus a generator parameter; can be pulled into the feature's single phase if the owner agrees.
