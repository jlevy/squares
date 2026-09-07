# Exact lower bound `s(17) > 4.456575`

The sixteen rational points in [`points.json`](points.json) are strictly
unavoidable in the square

```text
L = 4456575/1000000 = 4.456575.
```

The proof interface is the same as in `Mira-acc/17squares`: a deterministic
subdivision generator produces an untrusted certificate tree, and three exact
checkers validate every leaf claim. The Boost and Python arbitrary-integer
checkers independently reimplement the theorem-critical arithmetic rather than
reusing the generator's helper routines.

The resulting tree has **21,696,657 nodes** and maximum depth **68**.

Certificate SHA-256:

```text
5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550
```

The certified statement is:

> Every unit square contained in `[0,4456575/1000000]^2`, at every orientation,
> contains one of the 16 listed rational points strictly in its interior.

Seventeen pairwise interior-disjoint unit squares would require 17 distinct
interior witnesses but only 16 points are available. Thus no such packing exists
at this side length. As in the original proof, compactness makes the lower bound
strict:

```text
s(17) > 4.456575.
```

## Certificate statistics

```text
nodes       = 21,696,657
split       = 10,848,328
covered     = 10,594,408
infeasible  =    253,921
max_depth   = 68
```

Witness-leaf counts (points 1 through 16):

```text
1464,41000,457171,706152,164898,215542,1555534,3078,
2571,353271,1365069,2338656,268080,861347,2128732,131843
```

## Reproduction

From the root of this response package:

```bash
bash ./verify_4p456575.sh
```

Expected final marker:

```text
ALL_EXACT_CHECKS_PASSED_4P456575
```
