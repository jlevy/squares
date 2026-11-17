---
type: is
id: is-01m7f0q9yjvhyn57fk6sbrxd3n
title: "sqpack.field NumberField.decimal drops the exponent of a small value: exact_verify prints a pair gap of -sqrt(2) x 10^-30 as '-1.41421356237309504880168872420969807856967187537'"
kind: bug
status: open
priority: 3
version: 1
labels:
  - verification
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-15T07:11:08.242Z
updated_at: 2026-11-15T07:11:08.242Z
---
Found in lane L175 (think-ud9e, #992) running a sharp control over Q(sqrt 2): the 441 turned squares of the 977 construction moved by (-10^-30, -10^-30) give a least pair gap of -sqrt(2) x 10^-30, which devtools.check_algebraic_witness_independent prints as -1.414214e-30 and sqpack.witness.exact_verify prints, through _number and NumberField.decimal (src/sqpack/field.py), as '-1.41421356237309504880168872420969807856967187537'. decimal() returns the shared prefix of the two enclosure endpoints' str(Decimal) texts; for a value of this size the endpoints differ in the mantissa before their identical 'E-30' suffix, so the suffix is cut and the print reads about 10^30 times too large. Verdicts are unaffected (signs are exact); only printed margins in receipts and reports (minimum_best_pair_gap, minimum_containment_clearance) can mislead. Reproduce: devtools.diamond_staircases' S2 control on its small test recipe. Fix: format the certain digits with an exponent (or as scientific notation), and add a test at 10^-30.
