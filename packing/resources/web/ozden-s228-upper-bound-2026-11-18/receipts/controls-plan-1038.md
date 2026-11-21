# Control plan, import of jlevy/squares#1038 (bead think-91fu, lane i1038)

Written 2026-11-20 before any replay or control of this plan ran. Certificate:
kenaznia-doga/s228-upper-bound-1559604311 at 46ab8bf425f5cad886a8bc4023bfff904f43af99,
n-228-candidate.yaml, SHA-256 1b816e2e9302ad58ca2d5bb5882f4f98b2c8fb4f9e5746a8ed3f823cfd4a3387,
n = 228, read by the witness-center-basis reader. Before this plan, the certificate was read
only by sha256sum and by two measurements: devtools.contraction_margin (T-301 against it, and
its own margin), which decided the certificate as given on both maintained routes, and
devtools.measure_identity. No control below has run.

Routes: exact_verify (sqpack rational witness verifier) and independent (the independent
rational corner checker), each job in its own process, by devtools.upper_bound_reports.

## Gross controls (certify)

1. The certificate at its own side: accepted on both routes.
2. Duplicate-square control: refused on both routes, failure overlap.
3. Outside-container control: refused on both routes, failure container.

## Sharp controls (sharp-controls), step epsilon = 1e-30

Let w be the least wall clearance and (i, j) the least-gap pair with gap g, as the replay
decides them. Branch W0: w = 0 (the author reports 0). Branch W+: w > 0. Branch G: g > 1e-30
(the author reports about 3.6e-23); if g <= 1e-30 the step does not lie below the pair margin
and the plan is void for the pair controls.

4. Side lowered to the extent (by w): accepted at contact, wall margin exactly 0; lowered by
   w + 1e-30: refused, failure container, wall margin exactly -1e-30.
5. Least-gap pair closed by its gap: accepted at contact, gap margin exactly 0; closed by
   g + 1e-30: refused, failure overlap, gap margin exactly -1e-30.
6. Every square moved toward its nearer near wall by w: accepted at contact, wall margin
   exactly 0; by w + 1e-30: refused, failure container, margin exactly -1e-30.
7. A square of the least-gap pair enlarged to its partner at contact: refused for its shape
   alone (failure shape), gap margin exactly 0; enlarged 1e-30 past: refused for overlap and
   shape, gap margin exactly -1e-30.
8. A square at the least wall clearance enlarged to its wall at contact: W0 (grown by 0):
   accepted, wall margin 0; W+ (grown by w): refused for shape alone. Enlarged 1e-30 past:
   refused for container and shape, wall margin exactly -1e-30.
9. A duplicated square: refused, failure overlap.

Every control is decided on both routes and the two routes must agree on every verdict and
margin. Any outcome other than stated is reported as a disagreement, not re-planned.

## Measurements (not controls)

The option D comparison (owner's decision, think-b0w5): the certificate's side against T-301
shrunk to first contact, devtools.contraction_margin, and pose-by-pose identity against T-301,
T-300 and the house witness, devtools.measure_identity. These decide nothing about
feasibility.
