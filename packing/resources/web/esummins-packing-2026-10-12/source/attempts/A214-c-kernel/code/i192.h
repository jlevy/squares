/* A214 -- signed 192-bit integers as three 64-bit limbs (two's complement, little-endian), enough for the two
   large exact tests of polycore.vertex_ok (A213 notes/int_polycore.md s.3: the endpoint value < 2^142, the
   discriminant < 2^183).  __int128 (clang on x86-64) carries the coefficients and the interior test; only the
   endpoint value and the discriminant need the third limb.  Every routine here is exact -- no truncation, no
   wrap-around inside the documented input envelope (which ckernel214.c checks before calling). */
#ifndef A214_I192_H
#define A214_I192_H

typedef unsigned long long u64;
typedef long long i64;
typedef unsigned __int128 u128;
typedef __int128 i128;

typedef struct { u64 l[3]; } i192;

static inline i192 i192_neg(i192 a)
{
    i192 r;
    u64 c = 1, t, s;
    for (int i = 0; i < 3; i++) {
        t = ~a.l[i];
        s = t + c;
        c = (s < t);
        r.l[i] = s;
    }
    return r;
}

static inline i192 i192_add(i192 a, i192 b)
{
    i192 r;
    u64 c = 0;
    for (int i = 0; i < 3; i++) {
        u64 s = a.l[i] + b.l[i];
        u64 c1 = (s < a.l[i]);
        u64 s2 = s + c;
        c1 |= (s2 < s);
        r.l[i] = s2;
        c = c1;
    }
    return r;
}

static inline i192 i192_sub(i192 a, i192 b) { return i192_add(a, i192_neg(b)); }

/* < 0 ?  (the only predicate the tests need: "A t^2 + B t + C >= 0" is "not negative") */
static inline int i192_neg_p(i192 a) { return (int)(a.l[2] >> 63); }

static inline u128 u128_abs(i128 v, int *neg)
{
    *neg = (v < 0);
    return (u128)(*neg ? -v : v);
}

/* |a| < 2^128, |b| < 2^64, |a b| < 2^192 */
static inline i192 mul_u128_u64(u128 a, u64 b)
{
    u64 a0 = (u64)a, a1 = (u64)(a >> 64);
    u128 p0 = (u128)a0 * b;
    u128 p1 = (u128)a1 * b;
    i192 r;
    u128 mid;
    r.l[0] = (u64)p0;
    mid = (p0 >> 64) + (u128)(u64)p1;
    r.l[1] = (u64)mid;
    r.l[2] = (u64)(p1 >> 64) + (u64)(mid >> 64);
    return r;
}

/* the product must fit 192 bits unsigned (the caller's envelope guarantees < 2^189) */
static inline i192 mul_u128_u128(u128 a, u128 b)
{
    u64 a0 = (u64)a, a1 = (u64)(a >> 64), b0 = (u64)b, b1 = (u64)(b >> 64);
    u128 p00 = (u128)a0 * b0, p01 = (u128)a0 * b1, p10 = (u128)a1 * b0, p11 = (u128)a1 * b1;
    i192 r;
    u128 mid;
    r.l[0] = (u64)p00;
    mid = (p00 >> 64) + (u128)(u64)p01 + (u128)(u64)p10;
    r.l[1] = (u64)mid;
    r.l[2] = (u64)(mid >> 64) + (u64)(p01 >> 64) + (u64)(p10 >> 64) + (u64)p11;
    return r;
}

static inline i192 imul_128_64(i128 a, i64 b)
{
    int na, nb;
    u128 ua = u128_abs(a, &na);
    u64 ub = (u64)(b < 0 ? -(i128)b : (i128)b);
    i192 r;
    nb = (b < 0);
    r = mul_u128_u64(ua, ub);
    return (na ^ nb) ? i192_neg(r) : r;
}

static inline i192 imul_128_128(i128 a, i128 b)
{
    int na, nb;
    u128 ua = u128_abs(a, &na), ub = u128_abs(b, &nb);
    i192 r = mul_u128_u128(ua, ub);
    return (na ^ nb) ? i192_neg(r) : r;
}

#endif /* A214_I192_H */
