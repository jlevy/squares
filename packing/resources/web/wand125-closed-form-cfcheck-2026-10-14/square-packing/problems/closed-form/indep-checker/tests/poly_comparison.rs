#[path = "support/poly_reference.rs"]
mod reference;
use cfcheck::{
    poly::Poly,
    rat::{int, Q},
};
use num_rational::BigRational;
fn old(p: &Poly) -> reference::Poly {
    reference::Poly::new(p.coefficients().iter().map(Q::big).collect())
}
fn same(p: &Poly, q: &reference::Poly) {
    assert_eq!(p.coefficients().iter().map(Q::big).collect::<Vec<_>>(), q.0);
}
#[test]
fn random_gcd_sturm_and_multiplicities() {
    let mut seed = 901u64;
    let mut next = || {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
        (seed >> 32) as i64
    };
    for case in 0..320 {
        let p = Poly::new(
            (0..2 + case % 6)
                .map(|_| cfcheck::rat::q(next() % 19 - 9, next() % 7 + 1))
                .collect(),
        );
        let q = Poly::new(
            (0..2 + case % 4)
                .map(|_| cfcheck::rat::q(next() % 13 - 6, next() % 5 + 1))
                .collect(),
        );
        let (a, b) = (old(&p), old(&q));
        same(&p.add(&q), &a.add(&b));
        same(&p.sub(&q), &a.sub(&b));
        same(&p.mul(&q), &a.mul(&b));
        same(&p.derivative(), &a.derivative());
        let x = cfcheck::rat::q(next() % 29 - 14, next() % 11 + 1);
        assert_eq!(p.eval(&x).big(), a.eval(&x.big()));
        assert_eq!(
            p.eval_sign(&x).cmp(&0),
            a.eval(&x.big()).cmp(&BigRational::from_integer(0.into()))
        );
        if !q.is_zero() {
            let (v, r) = p.div_rem(&q);
            let (ov, orr) = a.div_rem(&b);
            same(&v, &ov);
            same(&r, &orr);
            same(&p.mul(&q).exact_div(&q), &a);
        }
        let p = if case % 3 == 0 { p.mul(&q).mul(&q) } else { p };
        let (a, b) = (old(&p), old(&q));
        same(&p.gcd(&q), &a.gcd(&b));
        let sf = p.square_free();
        let osf = a.square_free();
        assert_eq!(sf.len(), osf.len());
        for ((p, m), (q, n)) in sf.iter().zip(&osf) {
            assert_eq!(m, n);
            same(p, q);
        }
        let seq = p.sturm();
        let oseq = a.sturm();
        assert_eq!(seq.len(), oseq.len());
        for (p, q) in seq.iter().zip(&oseq) {
            same(&p.monic(), &q.monic());
            assert_eq!(
                p.coefficients().last().map(Q::is_positive),
                q.0.last().map(|c| c > &BigRational::from_integer(0.into()))
            );
        }
        for (lo, hi) in [(-3, 2), (-1, 0), (0, 1)] {
            assert_eq!(
                p.roots_open(&int(lo), &int(hi)),
                a.roots_open(
                    &BigRational::from_integer(lo.into()),
                    &BigRational::from_integer(hi.into())
                )
            );
            assert_eq!(
                p.nonneg_open(&int(lo), &int(hi)),
                a.nonneg_open(
                    &BigRational::from_integer(lo.into()),
                    &BigRational::from_integer(hi.into())
                )
            );
        }
        cfcheck::poly::clear_caches();
    }
}
