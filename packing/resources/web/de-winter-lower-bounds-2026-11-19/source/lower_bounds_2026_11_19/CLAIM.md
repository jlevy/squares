# Claimed lower bounds

This folder supports a registration request for the 48 lower bounds in `followup/best_by_count.csv`. The other results in the folder are not claimed: the 67 corner bounds in `corners/` (they inherit the global coverage of Hosono's T-180 measures), the 16 edge-strip refinements (gains near 1e-11) and the packings in `upper/` and `followup/upper/` (precision refinements of existing layouts).

Previous values: the SquareMath frontier at jlevy/squares 1015fc1, the bounds submitted in issue #1039, and monotonicity from smaller counts.

| n | Previous lower bound (source) | New lower bound | Gain | Method |
|---:|---:|---:|---:|---|
| 50 | 7.411863947 (#1039) | 7417/1000 = 7.417 | 0.0051 | standalone certificate |
| 52 | 7.550000000 (SquareMath) | 7561/1000 = 7.561 | 0.0110 | standalone certificate |
| 54 | 7.685000000 (SquareMath) | 7693/1000 = 7.693 | 0.0080 | standalone certificate |
| 57 | 7.872500000 (SquareMath) | 197/25 = 7.88 | 0.0075 | standalone certificate |
| 58 | 7.935000000 (SquareMath) | 3971/500 = 7.942 | 0.0070 | standalone certificate |
| 65 | 8.355003729 (#1039) | 209/25 = 8.36 | 0.0050 | standalone certificate |
| 67 | 8.492844105 (#1039) | 8497/1000 = 8.497 | 0.0042 | standalone certificate |
| 68 | 8.539124419 (#1039) | 1068/125 = 8.544 | 0.0049 | standalone certificate |
| 69 | 8.632841535 (#1039) | 8639/1000 = 8.639 | 0.0062 | standalone certificate |
| 70 | 8.670340847 (#1039) | 347/40 = 8.675 | 0.0047 | standalone certificate |
| 71 | 8.726003928 (#1039) | 8731/1000 = 8.731 | 0.0050 | standalone certificate |
| 72 | 8.772838965 (#1039) | 8777/1000 = 8.777 | 0.0042 | standalone certificate |
| 73 | 8.825837992 (#1039) | 1104/125 = 8.832 | 0.0062 | standalone certificate |
| 74 | 8.872504007 (#1039) | 8879/1000 = 8.879 | 0.0065 | standalone certificate |
| 75 | 8.945011507 (#1039) | 179/20 = 8.95 | 0.0050 | standalone certificate |
| 84 | 9.432755240 (#1039) | 18867/2000 = 9.4335 | 0.0007 | standalone certificate |
| 85 | 9.485321759 (#1039) | 9489/1000 = 9.489 | 0.0037 | standalone certificate |
| 86 | 9.537888278 (#1039) | 47693/5000 = 9.5386 | 0.0007 | standalone certificate |
| 87 | 9.585002876 (#1039) | 9591/1000 = 9.591 | 0.0060 | standalone certificate |
| 88 | 9.643021316 (#1039) | 1206/125 = 9.648 | 0.0050 | standalone certificate |
| 89 | 9.690002913 (#1039) | 4849/500 = 9.698 | 0.0080 | standalone certificate |
| 91 | 9.798217705 (#1039) | 9799/1000 = 9.799 | 0.0008 | standalone certificate |
| 93 | 9.880000000 (SquareMath) | 4943/500 = 9.886 | 0.0060 | standalone certificate |
| 103 | 10.302362742 (from n = 102) | 10309/1000 = 10.309 | 0.0066 | standalone certificate |
| 104 | 10.413093677 (#1039) | 10433/1000 = 10.433 | 0.0199 | standalone certificate |
| 107 | 10.595001907 (#1039) | 53/5 = 10.6 | 0.0050 | standalone certificate |
| 109 | 10.697466050 (#1039) | 2141/200 = 10.705 | 0.0075 | standalone certificate |
| 112 | 10.782475680 (#1039) | 2159/200 = 10.795 | 0.0125 | standalone certificate |
| 113 | 10.793947881 (#1039) | 5431/500 = 10.862 | 0.0681 | standalone certificate |
| 114 | 10.807801611 (#1039) | 10887/1000 = 10.887 | 0.0792 | standalone certificate |
| 115 | 10.807801611 (from n = 114) | 10889/1000 = 10.889 | 0.0812 | standalone certificate |
| 128 | 11.328203914 (SquareMath) | 11431/1000 = 11.431 | 0.1028 | standalone certificate |
| 129 | 11.374281585 (SquareMath) | 5733/500 = 11.466 | 0.0917 | standalone certificate |
| 130 | 11.420164834 (SquareMath) | 2299/200 = 11.495 | 0.0748 | standalone certificate |
| 131 | 11.465856100 (SquareMath) | 2311/200 = 11.555 | 0.0891 | standalone certificate |
| 132 | 11.511357773 (SquareMath) | 5809/500 = 11.618 | 0.1066 | standalone certificate |
| 133 | 11.556672194 (SquareMath) | 583/50 = 11.66 | 0.1033 | standalone certificate |
| 134 | 11.601801655 (SquareMath) | 11699/1000 = 11.699 | 0.0972 | standalone certificate |
| 135 | 11.646748405 (SquareMath) | 11751/1000 = 11.751 | 0.1043 | standalone certificate |
| 136 | 11.691514643 (SquareMath) | 2967/250 = 11.868 | 0.1765 | standalone certificate |
| 137 | 11.736102527 (SquareMath) | 59406523/5000000 = 11.8813046 | 0.1452 | four translated regions |
| 138 | 11.780514173 (SquareMath) | 59410049/5000000 = 11.8820098 | 0.1015 | four translated regions |
| 161 | 12.800000000 (SquareMath) | 6429/500 = 12.858 | 0.0580 | standalone certificate |
| 162 | 12.800000000 (from n = 161) | 2576221/200000 = 12.881105 | 0.0811 | four translated regions |
| 188 | 13.738202295 (SquareMath) | 6929/500 = 13.858 | 0.1198 | periodic central strips |
| 189 | 13.775918047 (SquareMath) | 13881/1000 = 13.881 | 0.1051 | periodic central strips |
| 217 | 14.756577429 (SquareMath) | 1857/125 = 14.856 | 0.0994 | corner reweighting and periodic strips |
| 218 | 14.791605928 (SquareMath) | 7433/500 = 14.866 | 0.0744 | periodic central strips |

Check: `python3 followup/verify.py` from this folder (Python 3.10+, C++17 compiler for replays).
