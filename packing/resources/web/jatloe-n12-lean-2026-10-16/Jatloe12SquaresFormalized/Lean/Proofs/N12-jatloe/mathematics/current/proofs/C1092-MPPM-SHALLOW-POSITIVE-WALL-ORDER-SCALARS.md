# C1092 MPPM: continuous scalars for the shallow positive wall order

Every terminating decimal is an exact rational number. The variables in this chapter range over complete real angle intervals. The polynomial identities below are symbolic identities, and their signs follow from the displayed inequalities; no list of sampled angles is a proof premise.

Throughout, put

    0<p<=2 atan(1/4), c=cos p, s=sin p, L=c+s,
    a>1, a<=c+.44s,
    B_a=a(3/2+cL/2), b(K)=(B_a-K-2c)/s.          (1)

Thus s>0, c>=15/17, s<=8/17 and c-s>=7/17. The notation B_a in (1) denotes a scalar, not a replacement boundary square.

## 1. The bottom-envelope scalars

Let 0<=phi<=pi/2, h=cos phi, t=sin phi, and define

    phi_C=pi/2-p,
    delta=st-ch, kappa=sh+ct,
    W_B=1+t^2+ht.

Consider the following two exact expressions on their indicated intervals:

    g_+(phi)=-h b(s)-2t+(a/2)W_B
                  -[delta(-s/2)+kappa(s-a)-a delta],
                         phi_C<=phi<=pi/2;       (2)

    g_-(phi)=(a/2)W_B+A_B h+B_B t,
                         0<=phi<=phi_C,          (3)

    A_B=a(L/2-1/s)+c/s-.44c^2,
    B_B=-as-1+.44cs.

**Lemma 1.** Both expressions are nonnegative on their complete indicated intervals. They vanish at phi_C. Moreover g_+(pi/2)>0 and g_-(phi)>0 on 0<=phi<=pi/4.

### 1.1. The upper interval

Expression (2) is a quadratic trigonometric term (a/2)W_B plus a linear combination of h,t. Consequently

    g_+''+g_+=(3a/2)h(h-t)<=0

on phi_C<=phi<=pi/2, since phi_C>pi/4. Direct substitution gives

    g_+(phi_C)=0,
    g_+(pi/2)=a(1+L)-2-cs+s^2/2
                >L-1-cs+s^2/2>0.                (4)

To verify the last strict sign exactly, put x=tan(p/2). Then

    L-1-cs+s^2/2=2x^3(2-x)/(1+x^2)^2>0.          (5)

The sine-concavity identity in Section 2.2 of C1092-MPPM-MISSING-POSITIVE-BOUNDARIES.md now proves g_+>=0 on the entire interval. That identity permits a zero endpoint, and its interval length here is less than pi.

### 1.2. The interval from zero to pi/4

Put z=tan(phi/2), so 0<=z<=sqrt(2)-1<5/12. Let

    F=xz+x+z-1.

Here x<=1/4 and z<1/2 give F<0. The exact coefficient of a in (3) is

    partial_a g_-=F Q(x,z)/[2x(1+x^2)(1+z^2)^2], (6)

where

    Q=(1+z+z^2+z^3)
       -x(1+z+5z^2+z^3)
       +x^2(z^3-z^2+5z-1)
       +x^3(z^3-z^2+z-1).

On x<=1/4,z<=1/2, direct grouping gives

    Q>=1-23/32-5/64-5/256=47/256>0.              (7)

For (7), bound the first bracket below by 1, the second bracket above by 23/8, and each of the last two brackets below by -5/4. Thus the coefficient (6) is negative. The intrinsic bound a<=c+.44s in (1) is therefore in the correct direction, and

    g_-(a)>=g_-(c+.44s)
      =-F P_B(x,z)/[25(1+x^2)^2(1+z^2)^2],      (8)

with the exact short polynomial decomposition

    P_B=b_0+x b_1+x^2 b_2+x^3 b_3,
    b_0=3-22z+53z^2-22z^3,
    b_1=50-3z+94z^2+47z^3,
    b_2=47-94z-3z^2-50z^3,
    b_3=22+53z+22z^2+3z^3.

Every coefficient is positive on 0<=z<=5/12. Explicitly,

    b_0>=(263/6)(z-66/263)^2+63/263>0,
    b_1>=195/4>0,
    b_2>=3193/864>0,
    b_3>=22>0.                                  (9)

For the first bound use -22z^3>=-(55/6)z^2 and complete the square. The second and third follow by putting z=5/12 in their negative terms and retaining their nonnegative terms. Hence (8) is strictly positive throughout this interval.

### 1.3. The remaining lower interval

On pi/4<=phi<=phi_C, (3) again gives

    g_-''+g_-=(3a/2)h(h-t)<=0.

The preceding subsection gives g_-(pi/4)>0, and direct substitution gives g_-(phi_C)=0. The same sine-concavity identity proves g_->=0 in between. This completes Lemma 1, including every aligned or coordinate endpoint. ∎

## 2. The two left-wall scalars with the same central face

Let 0<=beta<=pi/4 and put

    d=cos beta, r=sin beta,
    k=cos(beta-p)=cd+sr>0,
    tau=sin(beta-p)=cr-sd,
    W_L=1+r^2+rd.

Define

    Gamma_+=d/s [B_a-2c-(r-tau(a+s/2))/k]
                          -r+(a/2)W_L,
                           p<=beta<=pi/4;       (10)

    Gamma_-=d/s [B_a-2c-(r+tau(a-c-s))/k]
                          -r+(a/2)W_L,
                           0<=beta<=p.          (11)

**Lemma 2.** Both expressions are strictly positive throughout their complete indicated intervals.

First, the coefficients of a in (10),(11) are respectively

    d/s[3/2+cL/2+tau/k]+W_L/2>0,
    d/s[3/2+cL/2-tau/k]+W_L/2>0.                (12)

The signs follow from tau>=0 in (10) and tau<=0 in (11). It suffices to prove the strict inequalities at a=1. The intrinsic upper bound on a in (1) is not used in this lemma.

Set

    x=tan(p/2), z=tan(beta/2),
    D_*=x(1+x^2)(1+z^2)^2
              (1+xz-x+z)(1+xz+x-z)>0.           (13)

All factors are positive because 0<x<=1/4 and 0<=z<=sqrt(2)-1<1. The last two factors encode the same actual relative cosine k; no division by a zero projection occurs.

### 2.1. beta>=p

Put rho=z-x, so 0<=rho<1. Exact substitution into (10), with a=1, gives

    Gamma_+(1)=x(1-z) P_+(x,rho)/D_*,
    P_+=sum_{j=0}^5 C_j(x) rho^j,                (14)

where

| j | Exact coefficient C_j(x) |
|---|---|
| 0 | 2x^2(1+x^2)^4 |
| 1 | 2x(1+x^2)^2(5x^4+7x^2+4) |
| 2 | (1+x^2)(20x^6+34x^4+x^3+25x^2+x+3) |
| 3 | 20x^7+38x^5+5x^4+32x^3+6x^2+6x+1 |
| 4 | 10x^6+10x^4+7x^3+7x^2+3x-1 |
| 5 | 2x^5+3x^2+1 |

All coefficients other than C_4 are nonnegative, and C_0>0. The only potentially negative coefficient is handled without subdividing either angle:

    C_3 rho^3+C_4 rho^4
         >=rho^3(1-rho)>=0,                      (15)

because C_3>=1 and C_4>=-1. Hence P_+>0, and (14) proves Gamma_+(1)>0 on the complete ascending triangle, including rho=0.

### 2.2. beta<=p

Put rho=x-z, so 0<=rho<=1/4 and 0<=z<=1/4. The exact companion identity is

    Gamma_-(1)=(1-z) P_-(z,rho)/D_*,
    P_-=sum_{j=0}^6 E_j(z) rho^j,                (16)

with

| j | Exact coefficient E_j(z) |
|---|---|
| 0 | 2z^3(1+z^2)^4 |
| 1 | (1+z^2)^2(12z^6+3z^5+16z^4+3z^3+z^2+1) |
| 2 | (1+z^2)(30z^7+15z^6+51z^5+21z^4+14z^3+5z^2+z-1) |
| 3 | 40z^8+30z^7+84z^6+55z^5+43z^4+26z^3+8z^2+z+1 |
| 4 | 30z^7+30z^6+46z^5+39z^4+10z^3+8z^2+6z-1 |
| 5 | (1+z)(12z^5+3z^4+9z^3+3z^2-5z+2) |
| 6 | (1+z)(1+z^2)(2z^2+z-2) |

The displayed formulas give E_0>=0, E_1>=1, E_3>=0, E_5>0 and the simple uniform bounds

    E_2>=-17/16>-2, E_4>=-1,
    E_6>=-85/32>-3.                              (17)

For E_5, its inner bracket is at least 2-5z>=3/4. For E_6, use 2z^2+z-2>=-2 and (1+z)(1+z^2)<=85/64. Therefore

    P_->=E_0+rho(1-2rho-rho^3-3rho^5)
        >=E_0+(493/1024)rho.                     (18)

This is positive when rho>0. If rho=0, then z=x>0 and E_0>0. Thus (16) is strictly positive in every case, including beta=0 and beta=p. Equations (12) now prove both claims for a>1. This completes Lemma 2. ∎

The companion C1092-MPPM-SHALLOW-POSITIVE-WALL-ORDER.md derives these expressions from the actual simultaneous supports, including the additional strict-origin inequality that must use the same central upper face as the bottom envelope.
