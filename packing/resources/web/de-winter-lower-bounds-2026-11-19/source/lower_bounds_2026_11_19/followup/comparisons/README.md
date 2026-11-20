# Comparing the strongest earlier lower bounds

Run `python3 followup/comparisons/benchmark.py` from the extracted archive. For every claimed count the script recomputes the maximum of the earlier inputs, including all smaller square counts by monotonicity. Irrational earlier bounds are rounded upwards before comparison.

The registry interval table and the three other inputs in `inputs/prior56` come from Joost de Winter’s attachment to [SquareMath issue 1039](https://github.com/jlevy/squares/issues/1039). The registry revision was 1015fc175fa4e2c01f912d915d784100e36d3bab. The two tables in `inputs/earlier` come from the earlier project search and its companion comparisons. The preceding four-hour search supplies the root-level lower_bounds.csv and the two corner-family tables. The calculation evaluates all 34 intervals of Hiroaki Hosono’s closed form using the archived rational coefficients.
