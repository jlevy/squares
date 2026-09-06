# BC-230 Post-Freeze Control Review

Status: **pass at control-contract scope; accepted by the max-reasoning coordinator.**

This is the source-distinct review of the BC-230 control matrix after the four defects
in the frozen T+2 review were repaired.
The bounded implementation reviewer was `/root/bc230_postfreeze_review` at `xhigh`. The
coordinator made the mathematical disposition at `max`. No adaptive verifier or
candidate exists yet, so this receipt opens only the separately gated BC-231
implementation cell.

## Bound bytes

| Artifact | SHA-256 |
| --- | --- |
| Frozen theorem contract | `7530f32b568c7b0b3b8b7fc28a56b3f2fe1c34c65ee0646b5ae2fd6a1579cee9` |
| Frozen T+2 control matrix | `262029bf695937bf0af98e0b92cb7d94e714578861a0c128205164d6cfdc49b7` |
| Reconciled post-freeze control matrix | `4911b76161f62c8ece32b3fd7eb8866f2f2bd18dbf2d003ea94f29aaab30535d` |
| Reconciled matrix, self-normalized digest | `7b856c12bdf6b0eced0ba0bb89382f2049fb67ea6b5850b7814680b369a6533d` |

The theorem bytes and scientific acceptance rule did not change.
Only test reachability and oracle strength changed after T+2.

## Finding dispositions

### P5 — closed-boundary oracle

**Pass.** P5 now requires direct exact closed-square membership, equality with the union
of every incident open-cell membership set, equality with the boundary evaluator, and a
boundary mass at least the maximum incident open-cell mass.
It no longer uses the weaker minimum-based comparison.

### F4 and F5 — reachable refusal branches

**Pass.** F4 calls the pure cover validator while bypassing serialized and derived-field
validation. Its `2/5` and `1/4` mutations preserve valid endpoints and reach the gap and
overlap refusals separately.

F5 calls the pure endpoint validator and recomputes every dependent declaration after
mutating the final seam.
Exact recomputation gives

- `t_179 = 37072153/90000000`, whose bracket polynomial is negative;
- `t_180 = 1/2`, whose bracket polynomial is `1/4`; and
- `q_K = 164144306/142927847 > 1`.

Parsing, half-tangent ordering, bracket checks, and derived-field equality can therefore
pass before the intended final-seam refusal fires.

### T10 — premise-preserving lightening mutation

**Pass.** T10 changes all eight distinct images of one generic D4 orbit.
The arithmetic is `7/32 - 1/10000 = 4373/20000`, with updated total `119367/10000`. A
standard-library direct-membership check at center `(119/220, 119/220)` gives exact mass
`4999/5000`. Direction `0` and every earlier scalar premise remain valid; only Condition
5 fails.

### P2 — frozen scalar direction

**Pass.** P2 requires the scalar result to become a literal test-data oracle before the
adaptive comparison.
The actual retained value to freeze is direction `0`, attaining `12501/12500`; the
matrix does not invent a replacement literal.

## Coordinator disposition

The reconciled matrix is an executable specification for BC-231. The BC-230 theorem,
specialization, and controls are complete at their declared scope, with no residual
matrix blocker. BC-231 remains behind BC-220 and must implement and execute every
positive and negative control through its three decision routes.
This review does not predict those results or promote an adaptive lower-bound
certificate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
