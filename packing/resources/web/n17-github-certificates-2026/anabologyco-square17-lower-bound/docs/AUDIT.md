# Exact audit record

## Certificate arithmetic

```text
support_orbits=71
expanded_atoms=560
coordinate_grid=1/4000
weight_denominator=1000000000000
exact_mass_numerator=16994734834452
exact_mass=16.994734834452
exact_slack=0.005265165548
```

## Event regeneration

```text
family_A=165833
family_B=2240
family_C=1176801
primitive_union=1344862
regenerated_array_exactly_equal=true
raw_event_sha256=1574405fe33a5ccc7ed4a5b84ec59a00aab3f8c022ca9218a0476a953ce6e394
```

## Exact Bernstein prefilter

```text
raw_polynomials=1344862
exactly_discarded=1194331
filtered_polynomials=150531
maximum_absolute_Bernstein_numerator=279333690641532
int64_safety_factor=33019.19
```

## Exact event partition

```text
polynomial_root_incidences=149049
distinct_interior_root_gaps=148936
exact_gcd_checks=149049
common_root_in_every_gap=true
open_orientation_cells=148937
EXACT EVENT PARTITION PASS
```

The numerical seed initially represented the exact event \(t=1/3\) three times. Exact root counting identified two empty artificial gaps. Removing those two numerical duplicates produced the partition above; no algebraic root was deleted.

## Exact open-cell coverage

```text
orientation_cells=148937
subthreshold_runs=278950150
all_subthreshold_runs_excluded=true
minimum_arrangement_coverage=0
```

The zero minimum occurs in arrangement regions outside the feasible-center square. Every feasible region has coverage at least one.

The audit was run in 30 process-isolated ranges. Their exact union is `[0,148937)` with no gap or overlap. The sum of reported checker times is 400.9245 seconds.

## Exact endpoints

```text
exact_total_mass_numerator=16994734834452
theta_0_min_open_cell_coverage=1000300000011
theta_pi_over_4_subthreshold_runs=700
theta_pi_over_4_min_arrangement_coverage=0
EXACT ENDPOINT COVERAGE PASS
```

## Operational note

A long-lived inherited OpenMP process can stall nondeterministically after many cells. The arithmetic result is independent of this wrapper issue. Fresh process-isolated ranges terminate deterministically and agree on overlapping tests. The package therefore uses process isolation as the authoritative execution mode.
