# How the candidate was found (not an input to the checks)

- The measure is a nonnegative combination of axis-parallel rectangles (each averaged over the 8 images of the container's
  symmetry group), found by linear programming over sampled poses of a square of side B=0.9977 in the container of side
  L = 5.73351 = 5.745 x 0.998, followed by net rounds (adding violated poses at 201 half-angle directions, step 83/40000)
  and repair LPs until a floating-point check at the 201 directions found no violation.
- Search cost: about 42 CPU hours (31 hours wall time, of which about 27 hours were repair LPs).
- The coarse net is only a search device.  The two continuous-pose verifiers below check every orientation in
  t = tan(theta/2) in [0, sqrt(2)-1] (continuously, not at a net), with a core of side 499/500 and the container side L above.
