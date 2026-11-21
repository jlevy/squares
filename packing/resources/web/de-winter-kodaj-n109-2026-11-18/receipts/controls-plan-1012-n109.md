# Control plan: jlevy/squares#1012, n = 109 (lane c7-pointers, bead think-wvr8)

Written 2026-11-20 before any program of this repository decides the certificate.

Certificate: n109_kaggle/n109_tomkodaj.yaml at JoostdeWinter/square-packing aae089c
(SHA-256 56b4655fada7dfd5d54c1483b021d5b700ecb5c41beba2865a6a8ef7e223b3fb), a corner
Witness/v2 of 109 unit squares at side 547464479047171949843/50000000000000000000, read by
the `witness-corners` adapter of devtools.upper_bound_reports.

Positive: both maintained exact routes (sqpack exact verifier; independent rational corner
checker) accept the certificate as given.

Gross controls (certify): duplicate square, square moved outside the box. Both routes
refuse each.

Sharp controls (devtools.upper_bound_reports PACKET sharp-controls), on both routes:
1. side-lowered-past-wall-contact: box at the packing's extent accepted, margin exactly 0;
   1e-30 below the extent refused with margin exactly -1e-30. If the certificate touches
   its top or right wall (least clearance 0), the control is the touching-wall branch.
2. tightest-pair-closed-past-contact: exact contact accepted (margin 0); 1e-30 past refused.
3. squares-moved-past-near-wall-contact: at contact accepted; 1e-30 past refused.
4. square-enlarged-past-pair-contact: refused at contact for shape alone (margin 0); past
   contact refused with the pair margin within the window.
5. square-enlarged-past-wall-contact: as 4, at the wall.
6. duplicate-square: refused.
Expectation: every control behaves as stated on both routes; any other verdict is a
failure recorded as such, and the import stops there.

Measurements (decide nothing about the bound): measure_identity against the house at 109
(T-101's certificate, packet evand-square-packing-2026-10-05 n-109.cert) and against
Samanyu-dev/squares_in_squares 53551d7 best_fit_101_500.csv's 109 rows if reachable;
contraction_margin of this certificate, and of Samanyu-dev's 109 (option D, think-b0w5)
with this certificate as --against.
