# C1092 MPPM: an unconditional crosspoint before a missing-forward negative successor

Every terminating decimal is exact. All supports are those of the same actual open squares, with common side a>1. Strict anchors are interior points; face exclusions and square-to-square separators may have equality. Real walls constrain the full closed squares.

## 1. Local theorem and simultaneous faces

Let C have positive frame

    u=(c,s), v=(-s,c), c=cos p,s=sin p,
    p0=2 atan(1/3)<=p<=pi/4,

with lower faces U,V and upper faces A=U+a,H_C=V+a. Suppose it strictly owns

    M=(-.35,-.35), P=(-1,-.26)

and satisfies

    U>=-c-s, A<=-.5c, H_C<=1.086s.              (1)

Let E have negative frame

    e=(d,-t), f=(t,d), d=cos q,t=sin q,
    q0=2 atan(7/18)<=q<=pi/4,

with lower faces L,K and upper faces J=L+a,D=K+a. Suppose E strictly owns

    M_E=(.35,-.35), B1=(.4,-1)

and has the simultaneous actual bounds

    L>=.26t, J<=d+t,
    K>=-d, D<=t-.56d.                           (2)

Finally let B be an actual square disjoint from C and E, strictly owning

    O=(0,-1), Bm=(0,-1.086), F2=(-.4,-1),        (3)

and with closure in y>=-2.

**Theorem 1.** These three actual squares cannot satisfy all the stated hypotheses.

There is no preceding-origin premise in (1). In particular the larger cap 1.086s is retained throughout the proof.

## 2. The complete actual normal cones

Direct a separator from B toward C. Strict pairs P,Bm and M,F2 give

    -n_x+.826n_y>0, .05n_x+.65n_y>0.

Thus n_y>0 and n_x<.826n_y. Only the actual C normal v lies in this cone. No northeast normal of B can separate either. The actual signed-face computation is

    lower_C(n)-n dot F2
      <n_x[-c+s+.14-.826s^2]
             +n_y[1-c-s+.826cs]<0              (4)

for every northeast normal in this cone. To obtain (4), use the weaker A<=-.26c together with (1) and a>1. The first bracket increases with p and at pi/4 is -.273; the second is negative because c+s-1>.826cs. The strict F2 in B then excludes this source. This is the same direct calculation as Section 2 of C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md, with all its literal C hypotheses present.

Direct a separator from B toward E. The strict pairs O,B1 and O,M_E imply

    n_x>0, n_y>-(7/13)n_x.                     (5)

The downward actual E normal e cannot lie in (5), since t/d>=252/275>7/13. Its other possible right-facing normal is f, which is upward.

It remains to exclude a downward actual B normal n=(xi,-eta), xi>0,eta>=0 satisfying (5). Put

    alpha=d xi+t eta>0,
    mu=t xi-d eta>0.

The second sign follows from eta/xi<7/13<t/d. Using the two actual upper-face bounds in (2),

    lower_E(n)<=alpha(d+t-a)+mu(t-.56d-a).

After lowering a to 1 in the positive coefficient alpha+mu, this is strictly less than A1 xi-B1' eta, where

    A1=1-d-t+.44dt<-.19,
    B1'=t-d-.56-.44t^2>-1.

For the latter bound, d-t<.062 and t^2<=.5 give B1'>-.842. Since n dot O=eta,

    lower_E(n)-n dot O
      <A1 xi-(1+B1')eta<0.                     (6)

The strict O in B therefore excludes every such downward B source, including its horizontal endpoint.

Choose the actual B side normal b=(h,r) in the closed first quadrant and its northwest normal w=(-r,h), with 0<=beta<=pi/2. This represents every square orientation. The exhaustive remaining sources are

| Actual pair | Remaining actual normal |
|---|---|
| B toward C | v or w |
| B toward E | f or b |

Every listed source is upward in any actual use. Endpoint sources outside a strict cone are simply unavailable; keeping them in the scalar theorem is harmless.

## 3. Signed supports and the common side

Use the notation of C1092-MPPM-STEEP-POSITIVE-MISSING-NEGATIVE-WALL-SCALARS.md with epsilon=.086. In particular FC,FE,C0,E0 are its unit-side expressions, and WC,WE are the exact widths of B in directions v,f.

The simultaneous face bounds give

    lower_C(v)<=C0+epsilon s-(a-1),
    lower_E(f)<=E0-(a-1).                      (7)

For w dot u=-deltaC and w dot v=kC>0, the appropriate coefficient signs give

    lower_C(w)<=FC+epsilon s kC-(a-1)WC.        (8)

If deltaC>=0, use the lower bound A>=a-c-s and V<=1.086s-a. If deltaC<=0, use U<=-.5c-a and that same V cap. These are the two formulas defining FC, with precisely the additional epsilon s kC.

For b=alpha e+mu f, alpha=dh-tr and mu=th+dr>0, use the same actual E faces (2). If alpha>=0,

    lower_E(b)=alpha L+mu K
      <=alpha(d+t-a)+mu(t-.56d-a)
       =FE-(a-1)WE.                            (9)

If alpha<=0, the lower bound J>=a+.26t instead gives

    lower_E(b)=alpha J+mu K
      <=alpha(a+.26t)+mu(t-.56d-a)
       =FE-(a-1)WE.                           (10)

Thus all signed supports retain the appropriate lower or upper face of the same actual square. The formulas agree at alpha=0 and permit weak face equalities.

## 4. Elimination of the one actual boundary center

Let (x_B,y_B) be the actual center of B. The real floor gives

    y_B>=-2+(a/2)(h+r).

Consequently, for an upward unit normal n with unit-side B width omega_B(n),

    upper_B(n)>=n_x x_B-2n_y
                     +(a/2)[n_y(h+r)+omega_B(n)]. (11)

Let m be its selected separator toward C and n the selected separator toward E. Put Delta=n_x m_y-m_x n_y>0. Multiply the C separation by n_x and the E separation by -m_x. The actual x_B terms cancel exactly, and the necessary inequality is

    (a/2)[Delta(h+r)+n_x omega_B(m)-m_x omega_B(n)]
       -2Delta-n_x lower_C(m)+m_x lower_E(n)<=0. (12)

Here omega_B(v)=WC, omega_B(f)=WE and omega_B(b)=omega_B(w)=1. Substituting (7)--(10), the left side of (12) is at least

    Gij*+(a-1)Hij,

with the four Gij* exactly as in the scalar theorem and

    H00=.5[ell(h+r)+t WC+s WE]+t+s;
    H01=.5[kC(h+r)+h WC+s]+h+s WE;
    H10=.5[kE(h+r)+t+r WE]+t WC+r;
    H11=h+r+h WC+r WE.                          (13)

Every coefficient Hij is positive, including at all possible normal alignments. Since a>1, (12) requires the corresponding Gij* to be strictly negative. The complete continuous scalar theorem proves all four strictly positive. This contradicts every possible actual separator pair and proves Theorem 1.

The proof never bounds an upward support by dropping a positive vertical-center contribution. It uses the actual floor in (11) with its valid direction and then cancels the same actual horizontal center in (12).

## 5. Literal original crosspoint theorem

**Corollary 2.** In the retained no-omission OOOO MPPM entrance, suppose a positive ordinary central omits its designated forward point and its successor is nonpositive and also omits its designated forward point. Then the positive central strictly owns its local crosspoint X.

Normalize the two actual centrals as C=Q4 and E=Q5 and translate by (-2,-2). Suppose X=(1.5,2) were not strict in Q4. The unconditional positive caps and the other three strict bands at X give (1), with p>p0. No preceding origin is used.

Since Q4 omits forward G3, its proved outer halfpoint (1,1.5) and the actual paired-corner transfer put O=(2,1) strictly in Q9. The negative missing-forward Q5 therefore genuinely excludes its own preceding origin. Apply Lemma 1 of C1092-MPPM-MISSING-NEGATIVE-BOUNDARIES.md after the actual quarter turn. That lemma supplies q>q0 and all four faces (2); its additional V bound is (3) in its proof. In particular the axial representative is excluded.

The complete actual ledger is

| Local input | Actual original source |
|---|---|
| C strict M,P | Q4 marker and ordinary F0=(1,1.74) |
| U>=-c-s, H_C<=1.086s | The unconditional positive missing-forward profile |
| A<=-.5c, p>p0 | The hypothetical non-strict X, with its other three bands strict |
| E strict M_E,B1 and its other ordinary anchor | Q5 marker, ordinary F6=(2.4,1), and G5=(2.26,1) |
| E's own forward omitted | F4=(2,1.74) omitted by actual Q5 |
| E's own outer halfpoint strict | (2.5,1), the already proved missing-forward ordinary halfpoint |
| E's preceding origin excluded | Actual Q9 strictly owns (2,1), supplied by Q4's omission |
| E's corner excluded | Actual Q1 strictly owns (3,1) |
| E's complete foreign far bar | Actual Q10 owns the segment from (3,1.44) to (3,1.74) |
| Source of that Q10 advance | Actual ordinary Q6 owns F9, as in NONORDINARY-ISOLATION, Section 5 |
| B strict Bm,F2,O | The same actual Q9 owns its marker, F2=(1.6,1), and the derived (2,1) |
| Real B floor | Original closure of Q9 in y>=0 |

The missing-negative profile's rotated U,J,K,V bounds are respectively K>=-d, D<=t-.56d, L>=.26t and J<=d+t in the common physical frame used here. Thus there is no ambiguity from rotating a canonical negative representative.

All hypotheses of Theorem 1 now hold for the same three actual squares, a contradiction. This proves strict ownership of X. Simultaneous quarter turns give the other three sector versions.

This result does not require the negative successor to own its own crosspoint, and does not require the positive central to exclude its preceding origin. It complements the separately proved positive-successor transfer and the conditional retaining-negative-successor transfer; it does not assign any omitted forward auxiliary to another owner.
