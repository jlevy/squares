# C1092 MPPM: crosspoint transfer from a negative retaining successor, with genuine preceding-origin exclusion

Every terminating decimal is exact. All point owners and all support functions in this chapter belong to the same actual open squares. Exclusion includes equality at a face. The actual common side satisfies a>1; the original application retains 1<a<=1.001.

## 1. Local three-square theorem

Use the complete C,E inputs of Theorem 1 in C1092-MPPM-STEEP-POSITIVE-NEGATIVE-PROFILE.md. In particular C has positive angle p0<=p<=pi/4, strict M=(-.35,-.35),P=(-1,-.26), and

    U>=-c-s, A<=-.5c, H<=s.

E is negative, strictly owns M_E=(.35,-.35),B0=(.26,-1),B1=(.4,-1),I=(0,-.26), and excludes the actual corner Q0=(1,-1).

Retain an actual third square B, disjoint from C and E, whose closure lies in y>=-2 and which strictly owns

    O=(0,-1), Bm=(0,-1.086), F2=(-.4,-1).         (1)

The strict O supplies the E exclusion required in the profile theorem.

**Theorem 1.** These three actual squares cannot have pairwise disjoint interiors.

The profile theorem first gives 0<q<q0=atan(3/8), together with the simultaneous actual E faces

    K>=-d, J<=d+t, L<.26t, K<.26t-d,
    J>=a-.35(d-t).                               (2)

We retain these same faces in all subsequent supports.

## 2. The exhaustive actual boundary-source table

The strict comparisons P-Bm=(-1,.826) and M-F2=(.05,.65) show that a separating normal from B toward C satisfies

    n_y>0, n_x<.826n_y.                          (3)

Only C's northwest normal v=(-s,c) can lie in this cone. An actual northeast normal of B cannot separate either: the exact argument in Section 2 of C1092-MPPM-STEEP-POSITIVE-THREE-SQUARE-REDUCTION.md applies because its bounds A<=-.26c and H<=1.086s are weaker than the present bounds. It shows lower_C(n)<n dot F2<upper_B(n) for every northeast normal in (3).

From B toward E, the strict pairs O,B1 and O,I force both components of the normal to be positive. Only the actual E normal f=(t,d) is in this quadrant.

For B choose an actual side normal b=(h,r) in the closed first quadrant, with h=cos beta,r=sin beta, 0<=beta<=pi/2, and its northwest normal w=(-r,h). This represents both signs of every canonical boundary orientation. The complete remaining sources are therefore

| Actual pair | Remaining sources |
|---|---|
| B toward C | v or w |
| B toward E | f or b |

The strict cone excludes coordinate endpoints when necessary; retaining them in the scalar inequalities only enlarges the tested range.

## 3. Signed support caps for the same actual squares

Use all notation of C1092-MPPM-STEEP-POSITIVE-NEGATIVE-WALL-SCALARS.md, including FC,FE,C0,E0,kC,deltaC,kE,deltaE. Its unit-side caps are related to the actual faces by

    lower_C(v)<=C0-(a-1),
    lower_E(f)<E0,
    lower_C(w)<=FC-(a-1)(kC+|deltaC|).            (4)

The last assertion follows by the two coefficient signs w dot u=-deltaC and w dot v=kC>0. If deltaC>=0, use A>=a-c-s and V<=s-a. If deltaC<=0, use U<=-.5c-a and the same V cap. These are precisely the two formulas (2) in the scalar chapter.

For E's actual support along b, write

    alpha=dh-tr=-deltaE, mu=th+dr=kE>0,
    b=alpha e+mu f.

If beta<=Theta=pi/2-q, then alpha>=0. The strict I and B0 in (2) give

    lower_E(b)=alpha L+mu K
       <.26alpha t+mu(.26t-d)=FE.                (5)

If beta>=Theta, then alpha<=0. Retain the lower bound on the same actual upper face J in (2):

    lower_E(b)=alpha J+mu K
       <alpha[a-.35(d-t)]+mu(.26t-d)
       =FE-(a-1)deltaE.                          (6)

The two expressions meet at alpha=0. Every choice of a lower or upper face in (4)--(6) follows the sign of its exact coefficient; no point distance is used as a substitute for an opposite-face bound.

There is a useful direct reduction for beta<=pi/4. This interval is below Theta, so FE=-P h-Q r with P,Q from (4) of the scalar chapter. The actual strict O in B has projection -r. Since

    FE+r=-P h+(1-Q)r<=0,

by P>=1-Q and h>=r, (5) gives lower_E(b)<-r<upper_B(b). Thus B's own northeast normal cannot serve the E pair when beta<=pi/4. Whenever that source is chosen, its angle necessarily lies in the scalar chapter's required range beta>=pi/4.

## 4. Eliminate the center of the one actual B

Let (x_B,y_B) be B's actual center. Its real floor gives

    y_B>=-2+(a/2)(h+r).

For an upward unit normal n and B's unit-side width omega_B(n),

    upper_B(n)>=n_x x_B-2n_y
                      +(a/2)[n_y(h+r)+omega_B(n)]. (7)

Let m be the chosen actual source from B toward C and n the chosen source from B toward E. Both have positive vertical components, with m_x<=0 and n_x>0. Set Delta=n_x m_y-m_x n_y>0. Multiply the C separation by n_x and the E separation by -m_x. The terms in x_B cancel. The resulting necessary inequality is

    (a/2)[Delta(h+r)+n_x omega_B(m)-m_x omega_B(n)]
       -2Delta-n_x lower_C(m)+m_x lower_E(n)<=0.  (8)

The actual widths are omega_B(v)=WC, omega_B(f)=WE, and omega_B(b)=omega_B(w)=1. At a=1 the four expressions resulting from (4)--(6),(8) are exactly G00,G01,G10,G11 in the scalar chapter. The indexing records whether each selected source is central or supplied by B.

Keeping a rather than replacing it prematurely, the left side of (8) is at least Gij+(a-1)Hij, with

    H00=.5[ell(h+r)+t WC+s WE]+t;
    H01=.5[kC(h+r)+h WC+s]+h+s tauE;
    H10=.5[kE(h+r)+t+r WE]+t WC;
    H11=h+r+h WC+r tauE;
    tauE=max(deltaE,0).                          (9)

Each Hij is positive in the present actual domain t>0,s>0, including all possible weak-support equalities. This follows from the positive width terms; for H11 use h+r>=1. Therefore a>1 makes (8) require the corresponding Gij<0.

Theorem 1 of the scalar chapter proves G00,G10>=0 on the full domain and G01,G11>=0 whenever beta>=pi/4. The latter is precisely the actual range left by Section 3 whenever E's source comes from B. Every possible actual source pair contradicts (8). This proves Theorem 1.

The argument uses B's true floor only. It neither drops a boundary-center term with the wrong sign nor requires the original horizontal center sign of B.

## 5. Conditional strict crosspoint propagation in the original OOOO family

**Corollary 2.** Suppose an actual positive ordinary central C_i omits its forward point and genuinely excludes its preceding wall origin D. Suppose its actual successor is nonpositive and retains its own forward point. Then C_i strictly owns its local inner crosspoint X.

Normalize C_i=Q4 and its successor Q5. Suppose, to the contrary, that X=(1.5,2) is not strict in Q4. Its other three strict bands and the unconditional missing-positive profile force the bounds and steep positive angle used in the profile chapter. The exact original sources are

| Local datum | Literal original source |
|---|---|
| C's strict M,P | Q4 southwest marker and ordinary F0=(1,1.74) |
| U>=-c-s | Q4's unconditional missing-positive profile |
| A<=-.5c, p>p0 | The hypothetical non-strict position of (1.5,2), with its other three bands strict |
| H<=s | The explicitly stipulated exclusion of preceding D=(1,2) from Q4 |
| E's strict M_E,B0,B1,I | Actual Q5 southeast marker, G5, F6, and its retained forward F4 |
| E excludes Q0=(1,-1) | The strict inner corner point (3,1) in actual Q1 |
| B's strict Bm,F2 | The actual Q9 marker (2,.914) and original F2=(1.6,1) |
| B's strict O | Q4's missing-forward halfpoint, followed by the paired-corner transfer to Q9(2,1) |
| B's real floor | Original closure of Q9 in y>=0 |

The same actual Q9 owns all points in its row. Its strict origin supplies the E exclusion needed by the profile theorem. No auxiliary omitted by Q4 is assigned another owner.

Theorem 1 now contradicts the three actual squares. Thus X is strict in Q4. Rotate the full configuration and every source by R(x,y)=(4-y,x) to obtain all four sector versions.

In particular the genuine D exclusion in this corollary is available whenever the central immediately preceding C_i is nonpositive or omits its forward point: its own halfpoint gives the strict preceding actual wall origin. The corollary keeps this dependence explicit. It does not claim the same local conclusion if D may lie strictly inside C_i, and it does not yet treat a nonpositive successor which omits its own forward point.
