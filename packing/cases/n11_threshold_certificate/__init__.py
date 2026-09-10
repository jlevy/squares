"""The retained threshold certificates for `s(11)`: point atoms plus threshold atoms at 191/50.

These are of a different kind from the weighted fractional certificates in
`cases/n11_fractional_certificate`: besides point atoms they carry *threshold atoms*
`(S, k, w)`, which charge `w` to every core containing at least `k` points of `S` and
cost only `w floor(|S| / k)` of the budget. That is the rank-1 Chvatal--Gomory
strengthening of the one-body counting argument, and it is what carries this side past
the exact point-atom ceiling at `191/50`.

`certificate.json` is the retained rung, T-025's endpoint certificate on the 181-direction
net at shrink 9977/10000. Beside it are the same atoms re-certified on finer nets,
`certificate-191-50-net720.json` and `certificate-191-50-net1440.json` at shrink
249507/250000, whose dilation families give T-026's weak limit; their limit records are
`t-026-net720-dilation-limit-corollary.json` and `t-026-dilation-limit-corollary.json`.
The finer-net rungs prove the same side, 191/50, as the retained one: what they buy is
the larger shrink the dilation argument turns into a bound above it.

The theorem, the frozen premises and the two-route decision are written for a stranger in
`t-025-threshold-certificate-proof.md`, and the limit corollary in
`t-026-dilation-limit-proof.md`.
"""
