"""A242 offline stand-in for numba (not installed in the lab; pip would reach the network).
`njit` is the identity, so integer_sweep.py's kernels run as the SAME Python source, uncompiled.
Semantics are unchanged: all accumulations are numpy int64 with |sum| < 2**50 (checked by expand())."""
def njit(*args, **kwargs):
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return args[0]
    return lambda f: f
