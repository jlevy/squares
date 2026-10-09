---
type: is
id: is-01m4h4p5qnt2c3wmz4hkc2z01w
title: Handle rectangular witness sides in atlas web scaling
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
created_at: 2026-10-09T20:11:48.843Z
updated_at: 2026-10-09T20:11:48.843Z
---
Current-main integration exposed atlas_enclosing_sides converting rectangular witness side arrays to decimal scalar strings. Normalize to the same square enclosing side as the maintained renderer, preserve exact/fraction scalar semantics, add a rectangular regression and rerun affected web/consumer checks. Source and metadata remain unchanged.
