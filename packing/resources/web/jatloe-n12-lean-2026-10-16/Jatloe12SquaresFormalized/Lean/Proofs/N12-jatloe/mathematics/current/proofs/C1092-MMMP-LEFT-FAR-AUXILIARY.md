# C1092 MMMP: the actual left wall must own its far upper auxiliary

Every terminating decimal is an exact rational. The squares are the original actual open squares, have common side 1<a<=1.001, and have disjoint interiors. Owned points are strict. Missing points, wall contacts and face exits may be equality.

**Theorem.** In the entire original MMMP family,

    G1=(1,2.4) belongs strictly to the actual Q8.

Consequently the entire segment {1} x [2,2.4] belongs strictly to that same square. This theorem uses no top-wall origin.

## 1. The genuine wide wall under the contrary hypothesis

Suppose G1 is absent from Q8. The original G-covering row for Q8 requires a member of {G0,G1,G3}. The core-owner theorem has already put G3=(1.74,2) strictly in the different actual Q7. Thus the row forces G0=(1,1.6) into Q8.

The direct wall-sign chord and the wall-transfer theorem give the strict endpoint (1,2.39) and origin (1,2) in Q8. Convexity with G0 therefore gives the entire strict bar

    {1} x [1.6,2.39] in actual Q8.                    (1)

Apply Theorem 1 of `MIXED-WALL-HALFANGLE-CROSSING.md` under the simultaneous half-turn chart

    (xi,eta)=(2-x,2-y).

Every one of its premises has the following actual source:

| Standard datum | Original datum | Actual source |
|---|---|---|
| S=(1.086,0) strict in W | (.914,2) | Original Q8 marker |
| T=(1,-.39) strict in W | (1,2.39) | Direct wall-sign chord in Q8 |
| B=(1,.4) strict in W | G0=(1,1.6) | Original covering row under the contrary hypothesis |
| E=(1,-.4) excluded from W | G1=(1,2.4) | The contrary hypothesis |
| M=(.35,.35) excluded from W | (1.65,1.65) | Original marker strictly in Q4 |
| Closure in xi<=2 | Original x>=0 | Actual container wall for Q8 |
| Center eta<=0 | Original Y8>=2 | Original closed MMMP sign |

Hence Q8 has the strictly negative canonical frame in the original chart as well. Write

    u=(d,-t), v=(t,d), d>t>0, d^2+t^2=1,
    h=d+t>5/4.                                      (2)

The half-turn preserves the canonical sign. Its lower-v face bound in the cited theorem will also be used explicitly below.

## 2. The new northwest point and both actual wall faces

Translate now to (X,Y)=(x-1,y-2). Denote Q8's upper u and v face coordinates by J,B. Its lower faces are J-a,B-a. The half-turn chart of Section 1 is (xi,eta)=(1-X,-Y), so its v projection equals t-v(X,Y). The bound H>=t-.4d in the cited wall theorem therefore becomes

    B<=.4d.                                         (3)

The proved theorem `C1092-MMMP-UPPER-STRICT-POINTS.md` puts (1.19,2.2) strictly in actual Q7. Thus

    Z=(.19,.2)

is genuinely excluded from Q8 in the translated chart. Its lower u-band follows from Q8's strict marker S0=(-.086,0), because

    u(Z)-u(S0)=.276d-.2t>=.076d>0.

Its lower v-band follows from the strict origin (0,0), because .19t+.2d>0. Its upper v-band follows from the already strict point (0,.39), because

    v(0,.39)-v(Z)=.19(d-t)>0                         (4)

by (2). Therefore Z must exit through upper u, and

    J<=.19d-.2t.                                    (5)

These are bounds on the faces of the same actual Q8. Its least X coordinate is exactly

    d(J-a)+t(B-a).

The genuine left container wall gives a lower bound of -1 for this coordinate. Using (3),(5), and a>1, yields

    -1 <= d(J-a)+t(B-a)
        <= .19d^2+.2dt-a(d+t)
        < .19d^2+.2dt-h.

Consequently a necessary condition would be

    h<1+.19d^2+.2dt.                                (6)

## 3. A uniform scalar contradiction

Since d^2<=1 and 2dt=h^2-1, the right side of (6) is at most

    1.09+.1h^2.

On 5/4<=h<=sqrt(2), the function f(h)=h-1.09-.1h^2 is strictly increasing: f'(h)=1-h/5>0. Its value at the lower endpoint is exactly

    f(5/4)=3/800>0.

Thus (2) gives

    h-[1+.19d^2+.2dt]>=f(h)>3/800,

contradicting (6). The contrary missing G1 hypothesis is impossible, proving the theorem. Convexity with the already strict origin gives the whole stated bar.

All angle restrictions used here are conclusions of the complete continuous wall theorem. The scalar estimate covers its entire resulting interval. Every absent point was allowed to touch a face, and no unowned auxiliary was assigned a new owner except through the explicitly stated original covering row. The top-wall origin remains a separate actual-owner obligation. The ordinary wall-advance theorem cannot yet be invoked from G1 alone, because it has an additional exclusion premise.
