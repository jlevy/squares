"""The retained threshold certificate for `s(11)`: point atoms plus threshold atoms at 191/50.

One certificate is retained here, and it is of a different kind from the weighted
fractional certificates in `cases/n11_fractional_certificate`: besides point atoms it
carries *threshold atoms* `(S, k, w)`, which charge `w` to every core containing at least
`k` points of `S` and cost only `w floor(|S| / k)` of the budget. That is the rank-1
Chvatal--Gomory strengthening of the one-body counting argument, and it is what carries
this side past the exact point-atom ceiling at `191/50`.

The theorem, the frozen premises and the two-route decision are written for a stranger in
`t-025-threshold-certificate-proof.md`.
"""
