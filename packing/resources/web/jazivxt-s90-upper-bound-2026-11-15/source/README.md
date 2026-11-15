# Ninety unit squares in a square of side 9.998277166926

The enclosed arrangement proves the upper bound **s(90) ≤ 4999138583463/500000000000 = 9.998277166926**. The enclosing square is 0.001722833074 units narrower than a square of side 10.

![Ninety squares drawn from the exact certificate](n90.png)

Credit for the 90-square result goes to **jazivxt and GPT-6 Astra Ultra**. GPT-6 Astra Ultra was the AI collaborator on the geometric search and verification. The diagonal band comes from Joost de Winter’s earlier 157-square packing. [Joost de Winter’s exact 157-square coordinates](https://github.com/JoostdeWinter/square-packing/blob/c70defaf39af47db220d1e7c2922590637ffb664/n157/n157_exact.json)

The arrangement was found during the Squares in Squares optimization competition on Kaggle. [jazivxt’s public profile](https://www.kaggle.com/jazivxt) · [Competition overview](https://www.kaggle.com/competitions/squares-in-squares) · [The Squares Project’s N90 case record](https://squaremath.org/cases/90.html)

A rectangular crop about 12.993303 units wide and 9.353384 units high supplied the motif. Successive copies were offset horizontally by one unit, which let their edges fit together at a vertical pitch of 9.019403 units. A square window across two copies supplied 90 pieces. Fitting their centers and orientations yielded the arrangement above. Lighter squares in the figure have edges farther from horizontal or vertical.

## Coordinates and verification

[n90.cert](n90.cert) contains the exact geometry. The first line gives the number of unit squares and the enclosing side. Each subsequent line gives rational values for the center coordinates x and y and for t = tan(θ/2). The origin is the lower left corner and positive θ rotates counterclockwise. The [CSV](n90.csv) lists rounded centers and angles in degrees, in certificate order, numbered 1 through 90.

Francisco Couzo's exact verifier accepted this certificate with `--strict`, confirming positive clearance from each wall and separation between every pair of squares. A second exact check tested all 4,005 pairs, with minimum separating-axis clearance approximately 1.19448 × 10⁻¹². [Published verifier at the checked revision](https://github.com/franciscouzo/square-packing/blob/712c6a6e9ef58a9521784e6b7e236af813422de7/verify_bound_certificate.py)

[SHA256SUMS](SHA256SUMS) lists the SHA-256 digests of the certificate, coordinates, diagram and this note.
