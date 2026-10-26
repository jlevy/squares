# C1092 MMMP: the actual top square cannot own the left upper auxiliary

All terminating decimals are exact rational numbers. Strict points lie in their named actual open squares. Excluded points and separating supports may be tangent. The only size restriction beyond a>1 is the original bound a≤1001/1000.

## 1. A two-square theorem with no angle premise

**Theorem 1.** Let N and T be disjoint open squares of common side

    1<a≤1.001.

Suppose N strictly owns

    O=(0,0), A=(−.5,0), M=(−.35,.35), D=(0,.5).

Suppose T strictly owns

    P=(0,1.086), G=(−1,.4),

and excludes

    E=(−1,.39), K=(−1,1).

Then these two actual squares cannot exist.

The theorem places no wall, center or angle restriction on either square. It retains the complete T, rather than its segment PG. Indeed the proof excludes every direction in a strict separating cone, so it does not require a separate classification of N's angle.

## 2. The strict separating cone and the two whole angle bounds

Suppose a separator existed, and orient a unit normal n from N toward T. The strict points O,P imply n_y>0. The strict points D,G imply

    −n_x−.1n_y>0.

Thus write

    n=(−k,l), k,l>0, k²+l²=1, k>.1l.             (1)

The complete upper support of N consequently satisfies

    upper_N(n)>.5 max(k,l)≥1/(2sqrt(2))>.35,       (2)

using its two strict points A,D.

Choose either canonical sign for T, with absolute components b≥t≥0 and b²+t²=1. Its lower face coordinates are p,q. The difference P−G=(1,.686) gives strict projection spans.

For the positive frame

    u_T=(b,t), v_T=(−t,b),

the span on u_T is b+.686t<a≤1.001. This forces

    t<.01, b>.99.                                  (3)

Here is a full-interval verification. The concave function sqrt(1−t²)+.686t, on [.01,1/sqrt(2)], has its minimum at an endpoint. At .01 it is greater than .9999+.00686=1.00676, and at 1/sqrt(2) it equals 1.686/sqrt(2)>1.001. The latter comparison follows by squaring positive quantities. Thus no point of that entire interval is possible.

For the negative frame

    u_T=(b,−t), v_T=(t,b),

the strict v_T span is t+.686b<a≤1.001. This forces

    t<.4, b>.9.                                    (4)

Indeed t+.686sqrt(1−t²) is concave on [.4,1/sqrt(2)]. Its first endpoint is greater than .4+.686(.9)=1.0174, and its other endpoint is again 1.686/sqrt(2)>1.001. These two continuous arguments include every canonical angle outside the stated ranges; no angular subdivision is hidden in (3) or (4).

## 3. The positive sign is impossible

The strict G and weak exclusions E,K show that T's nonempty vertical chord at x=−1 is contained in .39≤y≤1. Its length is therefore at most .61.

An axial T has chord length a>1 and is immediately impossible. We may assume t>0 in this section. Let X_T be its center abscissa. Strict ownership of P, whose abscissa is zero, gives

    X_T>−a(b+t)/2>−1,

because a≤1.001 and 1.001sqrt(2)<2. The line x=−1 thus lies strictly left of T's center. Its chord cannot be on the plateau, where the length is a/b>1. It is on the left sloping portion. For the positive frame, the upper endpoint there lies on the upper v_T face and has ordinate

    (q+a−t)/b.

Since this endpoint is at most 1,

    q+a≤b+t, hence q<t.                            (5)

For completeness, this face identification follows directly from intersecting the four inequalities p<bx+ty<p+a and q<−tx+by<q+a with x=−1. On the left sloping portion their active endpoints are the lower u_T and upper v_T faces, respectively. The standard chord plateau has length a/b and halfwidth a(b−t)/2; these formulas also follow from those four intersections.

The components of n in the positive T frame are

    e=−kb+lt<−.099l+.01l<0,
    f=kt+lb>0, f≤1,                               (6)

by (1), (3) and unit length. Strict P ownership gives p+a>u_T(P)=1.086t≥0. The exact full lower support therefore obeys

    lower_T(n)=e(p+a)+fq<ft≤t<.01.                 (7)

This contradicts the necessary separation upper_N(n)≤lower_T(n), in view of (2). Thus no positive canonical T, including its axial limit, is possible.

## 4. The negative sign is impossible

Give T the negative frame, and retain (4). The n-components are

    e=−kb−lt<0, h=lb−kt.

There are only two relative-component cases.

### 4.1. The case h≥0

The strict anchors P,G give

    p+a>−1.086t, q<−t+.4b.

Consequently its complete lower support satisfies

    lower_T(n)=e(p+a)+hq
       <1.086t(kb+lt)+(lb−kt)(.4b−t)
       =kF+lG_0,                                  (8)

where

    F=.686bt+t²,
    G_0=.4+.686t²−bt.                             (9)

The inequality is strict even when h=0, since e<0 and P is strict.

The point Z=(−F,G_0) belongs to the convex hull of O,A,M,D, and is thus a strict point of the same actual N. Here is a direct rational verification on the entire interval (4). We have F≥0 and G_0≥.4−t>0. The other two bounding lines of that convex quadrilateral are

    7F+3G_0≤3.5, 3F+7G_0≤3.5.

Their left sides expand exactly as

    7F+3G_0=1.2+9.058t²+1.802bt
       <1.2+9.058(.16)+1.802(.4)
       =3.37008<3.5,                              (10)

    3F+7G_0=2.8+7.802t²−4.942bt
       =2.8+t(7.802t−4.942b)≤2.8<3.5,            (11)

because 7.802t−4.942b<7.802(.4)−4.942(.9)=−1.327. At t=0 the displayed conclusion in (11) remains valid with equality at 2.8. The four inequalities F≥0,G_0≥0,(10),(11) describe exactly the convex quadrilateral with vertices (F,G_0)=(0,0),(.5,0),(.35,.35),(0,.5).

Therefore upper_N(n)>n·Z=kF+lG_0, contradicting (8) and the proposed separation. Strict ownership of a convex combination of strict points remains strict, including when Z lies on an edge of their convex hull.

### 4.2. The case h≤0

Both coefficients e,h are nonpositive, and e<0. Strict P ownership gives

    lower_T(n)=e(p+a)+h(q+a)<n·P=1.086l.           (12)

But h≤0 means l/k≤t/b<.4/.9=4/9. Therefore

    lower_T(n)<1.086(4/9)k<.5k<upper_N(n),        (13)

where the exact strict middle comparison is 1.086(4/9)=181/375<1/2. This is again impossible. At h=0 either case is valid; if t=0 the present case cannot occur because l>0, so the first case already covers that endpoint.

Every normal in (1) has been excluded for both canonical signs of T. Disjoint open convex squares would possess such a weak support separator, so this contradiction proves Theorem 1. ∎

## 5. Exact MMMP owner mapping and remaining top label

**Corollary 2.** In every original C1092 MMMP configuration,

    G1=(1,2.4) is excluded from Q11.

Thus Q11's exact original auxiliary label is 16392, consisting of F3=(1.6,3) and G4=(1.74,3).

Translate the original coordinates by (−2,−2), and apply Theorem 1 to the actual owners N=Q7,T=Q11. Every hypothesis has the following original source:

| Theorem datum | Original point | Actual source |
|---|---|---|
| O,A,D strict in N | (2,2),(1.5,2),(2,2.5) | Full MMMP center and crosspoint chapters |
| M strict in N | (1.65,2.35) | Original Q7 marker |
| P strict in T | (2,3.086) | Original Q11 marker |
| G strict in T | G1=(1,2.4) | Present contrary hypothesis |
| E excluded from T | (1,2.39) | Actual Q8 wall-sign chord |
| K excluded from T | (1,3) | Actual original paired corner Q3 |
| Common side and size | 1<a≤1001/1000 | Original MMMP entrance |

The full center theorem is `C1092-MMMP-FULL-INWARD-CENTER.md`, and the triangle is `C1092-MMMP-CENTER-CROSSPOINTS.md`. Both apply to every original MMMP alternative before this corollary. The short bar was obtained directly from the original closed wall sign in `C1092-WALL-SIGN-CHORD.md`.

The resulting contradiction excludes G1 from Q11. The already proved core-owner theorem leaves precisely its two possible exact labels 16392 and 18440, with the latter adding G1. Hence only 16392 remains. This is a direct actual-owner consequence; no old mask-removal history or chosen twelve-owner vector is assumed. A final whole-MMMP contradiction remains a separate obligation.
