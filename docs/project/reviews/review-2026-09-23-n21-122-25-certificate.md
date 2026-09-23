# Review of the n21 Certificate at 122/25, 23 September 2026

A W2 factual review (Fable, max thinking) of the point certificate behind
[exp-229](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-229-h240-n21-point-certificate-122-25.md),
which
[H-240](../../../packing/campaign/hypotheses/H-240-n21-additive-certificate-at-4-88.md)
required before any register entry.
[Session 156](../../../packing/campaign/agent-sessions/session-156-w3-overnight-n11-settlement.md)
commissioned it after the certificate passed the retention gate.

## Verdict

**Accept.** The certificate is valid under the five-condition theorem T-020 and T-021
use, and it establishes `s(21) >= 122/25`, non-strictly, for $n=21$ only.
Three routes accepted the bytes (sha256
`b230f7cd6806343f115331caf53f02019cc634a8959359684581835a0cc7fb0f`) and nothing tried
refuted them.

| Route | Result |
| --- | --- |
| Stock `decide_certificate`, both routes | Interval enclosure $(250001/250000, 250001/250000)$ over 4,289,657 boxes, 0 stalled; exact least cell mass $250001/250000$; RETAINABLE |
| `cases/n11_fractional_certificate/verify_claim.py`, standard library only | All five conditions hold over 866,091,838 cells in 182 directions; VERIFIED |
| The registered replay module `cases.n20_fractional_certificate` | Five PASS lines; VERIFIED for every $m\ge21$ |

## Premises

| Condition | Value |
| --- | --- |
| D4-closed support | 1,228 distinct sites in 157 orbits; least weight $53/2000000>0$ |
| Mass below $n$ | $5036431/250000=20.145724<21$ |
| The net reaches $\pi/4$ | $t_K=207107/500000$, $t_K^2+2t_K-1=309449/250000000000>0$ |
| Net interpolation | $D=207107/90500000$, $B(1+D)=904984806539/905000000000<1$ |
| Least cell mass | $250001/250000$ at direction 0 |

The bound is the container side $L$ itself; $B$ rescales nothing.
The gate’s “ceiling 4.988500” is $\lceil\sqrt{21}\rceil B$, the largest side any
certificate with this $B$ can reach at $n=21$, and “certifies every $n\ge21$” comes from
the mass alone. The certificate says nothing about $n=20$, where T-021’s $97/20$ stands.

## Findings

| Severity | Finding |
| --- | --- |
| none | Declaring the least cell mass changed one field, from `null` to `250001/250000`; the decider treats it as a declaration to check, never an input. |
| none | The certificate has no degenerate seam. Set B’s interval stall came from 616 seams at direction 0, all from window rows exactly $B$ apart. |
| none | Every field is a rational string; floats never enter the decision. |
| minor | The run relaunched after commit `84e410691`, not `69dac09a`; the tool path is byte-identical across both, so either may be cited with that note. |
| minor | The retained certificate should join the fixed tuples in the certificate, reach and figure tests where retained certificates are enumerated. |

## Register Entry

`s(21) >= 122/25`, V4 and C4 by analogy with T-021, and C5 with this review retained;
significance S3; apparently novel.
No published bound for $n=21$ exceeds $4.7438$ (Friedman’s table), and the project’s own
were $4.80$ (T-020) and $4.85$ (T-021). The certificate was found unseeded, with no
windows, in 36 LP rounds and 691 s. C4 rests on the interval route, as it does for
T-021, since the standard-library verifier is a second implementation of the sweep’s
method.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
