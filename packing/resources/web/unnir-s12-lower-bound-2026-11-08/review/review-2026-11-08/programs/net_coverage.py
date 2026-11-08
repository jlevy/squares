"""Exact check of how the half-angle-tangent net theta_k = 2 arctan(k/N) covers
[0, 45 deg] and [0, 90 deg].

theta_k >= 45 deg  <=>  k/N >= tan(22.5 deg) = sqrt(2) - 1  <=>  (k + N)^2 >= 2 N^2.
theta_k >= 90 deg  <=>  k >= N.
Also bounds the widest bin, in radians, by 2/N (d theta / dt = 2/(1+t^2) <= 2).

Usage: python -I net_coverage.py N
"""

import json
import math
import sys


def main():
    n = int(sys.argv[1])
    # smallest k with theta_k >= 45 deg
    k45 = next(k for k in range(n + 1) if (k + n) ** 2 >= 2 * n * n)
    out = {
        "N": n,
        "first_k_with_theta_ge_45deg": k45,
        "bins_needed_for_0_to_45deg": k45,           # bins k = 0 .. k45-1
        "last_bin_index_for_45deg": k45 - 1,
        "theta_last_bin_lo_deg": math.degrees(2 * math.atan((k45 - 1) / n)),
        "theta_last_bin_hi_deg": math.degrees(2 * math.atan(k45 / n)),
        "exact": {
            f"(k45-1+N)^2 - 2N^2 (must be < 0)": (k45 - 1 + n) ** 2 - 2 * n * n,
            f"(k45+N)^2 - 2N^2 (must be >= 0)": (k45 + n) ** 2 - 2 * n * n,
        },
        "bins_for_0_to_90deg": n,
        "max_bin_width_rad_upper_bound": 2 / n,
        # theta_{k45-1} + theta_{k45} vs 90 deg: tan of half-sum
        # (t1 + t2)/(1 - t1 t2) >= 1  <=>  half-sum >= 45 deg
        "last_bin_reflection": {
            "theta_lo + theta_hi >= 90deg": (k45 - 1) * n + k45 * n >= n * n - (k45 - 1) * k45,
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
