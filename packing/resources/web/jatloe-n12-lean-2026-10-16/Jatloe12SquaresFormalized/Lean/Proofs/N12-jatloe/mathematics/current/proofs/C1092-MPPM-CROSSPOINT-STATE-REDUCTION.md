# C1092 MPPM: the exact residual pattern when a positive crosspoint is missing

All points described as owned are strict interior points of the named actual open squares. An omitted point may lie on a face. Retain the original no-omission, all-four-ordinary MPPM entrance, its twelve actual owners, its original side range 1<a<=1.001, and the continuous theorems cited below. This chapter is a logical composition of those theorems; it introduces no numerical angle classification.

## 1. The actual cyclic points

Index the actual central squares C_0,C_1,C_2,C_3 as Q4,Q5,Q6,Q7. The next actual boundary squares B_0,B_1,B_2,B_3 are Q9,Q10,Q11,Q8. Simultaneous quarter turns R(x,y)=(4-y,x) cycle these owners. The relevant points are

| Actual central | Its forward point T_i | Its crosspoint X_i | Its next boundary origin P_i |
|---|---|---|---|
| Q4 | G3=(1.74,2) | (1.5,2) | (2,1) in Q9 |
| Q5 | F4=(2,1.74) | (2,1.5) | (3,2) in Q10 |
| Q6 | G6=(2.26,2) | (2.5,2) | (2,3) in Q11 |
| Q7 | F5=(2,2.26) | (2,2.5) | (1,2) in Q8 |

The preceding origin D_i in C_i's chart is the same physical point as P_(i-1). Indices in this chapter are taken modulo four. A central is called retaining if it strictly owns T_i and missing-forward if it does not. These two words concern only that designated actual central; they do not assign an omitted T_i to another owner.

## 2. The four previously proved inputs

We use the following precise consequences of the continuous support proofs.

1. Every retaining ordinary central, of either canonical sign, strictly owns X_i. For a positive central this is Theorem 2 of C1092-MPPM-POSITIVE-CROSSPOINT-SEEDS.md. For a nonpositive central it follows from its strict ordinary pair and T_i: in its negative frame u=(c,-s),v=(s,c), the lower-u band of X=(-.5,0) follows from G=(-1,-.4), its two upper bands from T=(-.26,0), and the lower-v band from the universal actual neighboring-marker cap H<=.35(c-s), since a-.35c-.15s>0. The zero-angle endpoint is included by strict ownership of the equal-projection anchors.

2. A positive missing-forward central followed by a positive central which strictly owns its X also strictly owns its own X. This is Corollary 2 of C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md. Its proof retains the same actual shared boundary and does not assume a preceding origin.

3. A positive missing-forward central followed by a nonpositive missing-forward central strictly owns X. This is Corollary 2 of C1092-MPPM-STEEP-POSITIVE-MISSING-NEGATIVE-CROSSPOINT.md. There is no preceding-origin or successor-crosspoint premise.

4. A positive missing-forward central followed by a nonpositive retaining central strictly owns X provided it excludes its own preceding origin D. This is the original-sector corollary in C1092-MPPM-STEEP-POSITIVE-NEGATIVE-CROSSPOINT-TRANSFER.md. In particular this exclusion of D is genuine whenever the preceding central is nonpositive or missing-forward: its proved outer halfpoint and the actual paired-corner transfer put that same origin strictly in the preceding actual boundary square. The unconditional nonpositive halfpoint is C1092-MPPM-ORDINARY-NEGATIVE-HALFPOINT.md; the missing-forward halfpoint is the ordinary-central reduction. No claim is made that D is automatically excluded after a positive retaining predecessor.

We also retain the already proved exclusion of an all-missing-forward ordinary cycle: summing the four unconditional strict missing-forward wall-center orders gives a contradiction. The full actual cyclic cancellation is Section 8 of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md; the later MISSING-POSITIVE-WALL-ORDER and MISSING-NEGATIVE-WALL-ORDER chapters remove the preceding-origin premise from every individual missing-forward sector. This uses the actual centers of Q8,Q9,Q10,Q11 and is independent of the central signs.

## 3. A missing positive crosspoint is isolated

**Theorem 1.** Suppose some positive ordinary C_i does not strictly own X_i. Then its immediate predecessor C_(i-1) is positive and retaining, and its immediate successor C_(i+1) is nonpositive and retaining. No two positive centrals which omit their own X can be consecutive.

**Proof.** Any positive central omitting X is missing-forward by input 1. Starting at the stipulated C_i, follow consecutive positive centrals which omit X. This run must terminate: otherwise all four centrals would be positive and missing-forward, contrary to the all-missing cycle exclusion.

Let C_j be the last central in the run, and inspect its actual successor. That successor cannot be positive, because the terminating condition would mean its X is strict, and input 2 would then put X_j strictly in C_j. It cannot be nonpositive and missing-forward, by input 3. Thus C_(j+1) is nonpositive and retaining.

Input 4 shows that the actual predecessor of C_j must be positive and retaining. Indeed, if that predecessor were nonpositive or missing-forward, its genuine halfpoint would put D_j strictly in the preceding boundary, making it foreign to C_j; input 4 would contradict the stipulated omission of X_j. These alternatives cover every predecessor except positive retaining.

If the run had length at least two, the predecessor of its last member C_j would itself be a positive missing-forward member of the run. This contradicts the conclusion just proved. Hence the run has length one, C_j=C_i. Its immediate predecessor and successor have precisely the asserted signs and memberships. The same reasoning applies to every positive central omitting X, proving the final statement. ∎

The proof uses the genuine preceding-origin premise exactly once, where its actual boundary owner has been supplied. It does not replace that premise by a statement about which central is supposed to own an auxiliary.

## 4. The exact four-sector residual alternatives

**Corollary 2.** If a positive X is missing, simultaneous quarter turns can place its four actual central states in one of the following two rows:

| First owner | Second owner | Third owner | Fourth owner |
|---|---|---|---|
| positive retaining | positive missing-forward, X omitted | nonpositive retaining | positive missing-forward, X strict |
| positive retaining | positive missing-forward, X omitted | nonpositive retaining | nonpositive missing-forward |

In the second row the fourth angle is in fact strictly negative, by the missing-negative profile. In both rows the first actual wall origin, the one between the first and second central sectors, is omitted by its actual boundary and is strictly owned by the second central.

**Proof.** Theorem 1 gives the first three states. Let Z be the fourth actual central. If Z were positive retaining, the third, nonpositive retaining owner followed by Z would violate Corollary 2 of C1092-MPPM-NEGATIVE-OWNED-POSITIVE-OWNED-EXCLUSION.md. If Z were nonpositive retaining, its successor, the first positive retaining owner, would violate that same theorem. Thus Z is missing-forward.

If Z is positive, its successor is positive retaining and therefore owns X. Input 2 puts Z's X strictly in Z, giving the first row. If Z is nonpositive, its missing-forward profile excludes the axial representative, giving the second row.

Finally the second central omits X, has a nonpositive retaining successor, and is positive missing-forward. By the contrapositive of input 4 it must itself strictly own its preceding D. This is the first sector's boundary origin, so that actual boundary omits it by disjoint interiors. All remaining statements concern the same actual points and actual owners as in Section 1. ∎

This chapter isolates the only possible failure of a universal positive-crosspoint conclusion. It does not yet exclude either displayed row. In particular a missing actual boundary origin is not silently restored inside the consecutive positive run.
