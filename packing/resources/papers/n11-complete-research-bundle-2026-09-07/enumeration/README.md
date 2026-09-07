# Enumeration and elementary deduction controls

This directory is not a global packing solver. It supplies exact, standard-library
checks for the new addendum and a complete **discrete descriptor** catalogue.
All associated continuous packing cases remain unresolved by this code.

Run with Python 3.10 or later:

```sh
python enumeration_checks.py --write .
python test_enumeration.py
python -O enumeration_checks.py
```

`profile_catalogue.json` includes all 1,024 ordered positive multiplicity profiles
for eleven squares, grouped by number of distinct orientations, the 56 unordered
integer partitions for comparison, and all 78 three-bin occupancy profiles. It
also lists the 65 profiles left by the two elementary cuts at side at most 3.8771
and angular radius 1/500 radians. These are descriptors, not solved geometric cases.

`elementary_results.json` records the rational arithmetic, a twelve-disk packing
in side 18/5, and exact counterexamples to independent angle reflection and
rotation at unchanged side. `test_results.json` records known-answer and mutation
controls. The source 0/45-degree packing theorem is a mathematical premise. The
root-definition enclosure U < 3.8771 is checked here, but this is not a replay of
all contacts of the construction or of the 3.81 theorem.

The generic `robust_farkas_gap` helper implements only the displayed rational
box inequality in the addendum. Its caller must already supply valid interval
enclosures of every required branch coefficient. It does not produce those
geometric enclosures and does not certify a full packing case cover.

The controls have the same author as the implementation. Normal and optimized
Python executions agree. This is not independent external peer review.
