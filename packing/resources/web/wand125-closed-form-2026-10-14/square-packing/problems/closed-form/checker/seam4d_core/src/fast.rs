//! Optimized bound(): store vertices as integer homogeneous coordinates (X, Y, W), with W > 0 and gcd(X, Y, W) = 1, representing (X/W, Y/W).
//!
//! Points and predicate signs exactly match the Python reference and its direct port, bound_straight:
//! - Scale half-planes a.x <= b by positive factors to integer (α, β), preserving signs and intersections t = fp / (fp − fq).
//! - Sutherland–Hodgman intersections use (fp·Xq − fq·Xp, fp·Yq − fq·Yp, fp·Wq − fq·Wp),
//!   equivalent to Python's P + t (Q − P) over a common denominator. Normalize W > 0 and divide by the gcd for a unique form.
//! - Hull orientation is the sign of a 3×3 determinant (cross scaled by Wo·Wa·Wb > 0); sort and deduplicate by value.
//! - Sum areas and masses exactly as rationals (rug::Rational) at the end.
//! Vertex sequences match the direct port, including order, duplicates, and degeneracies, so results agree.

use super::*;

#[derive(Clone, PartialEq, Eq)]
pub(crate) struct H {
    x: Integer,
    y: Integer,
    w: Integer,
}

impl H {
    fn from_q(p: &Pt) -> H {
        let mut w = Integer::from(p.0.denom());
        w.lcm_mut(p.1.denom());
        let x = Integer::from(p.0.numer() * Integer::from(&w / p.0.denom()));
        let y = Integer::from(p.1.numer() * Integer::from(&w / p.1.denom()));
        H { x, y, w }
    }
    fn xq(&self) -> Q {
        Q::from((self.x.clone(), self.w.clone()))
    }
    fn yq(&self) -> Q {
        Q::from((self.y.clone(), self.w.clone()))
    }
    /// Make W > 0 and divide by gcd(X, Y, W).
    fn normalize(&mut self) {
        if self.w.cmp0() == Ordering::Less {
            self.x = Integer::from(-&self.x);
            self.y = Integer::from(-&self.y);
            self.w = Integer::from(-&self.w);
        }
        let mut g = Integer::from(self.x.gcd_ref(&self.y));
        g.gcd_mut(&self.w);
        if g != 1 {
            self.x.div_exact_mut(&g);
            self.y.div_exact_mut(&g);
            self.w.div_exact_mut(&g);
        }
    }
    /// (x + dx, y + dy)
    fn shift(&self, dx: &Q, dy: &Q) -> H {
        let mut l = Integer::from(dx.denom());
        l.lcm_mut(dy.denom());
        let ddx = Integer::from(dx.numer() * Integer::from(&l / dx.denom()));
        let ddy = Integer::from(dy.numer() * Integer::from(&l / dy.denom()));
        let mut r = H {
            x: Integer::from(&self.x * &l) + Integer::from(&ddx * &self.w),
            y: Integer::from(&self.y * &l) + Integer::from(&ddy * &self.w),
            w: Integer::from(&self.w * &l),
        };
        r.normalize();
        r
    }
    /// Compare values by x, then y, matching Python tuple order.
    fn cmp_xy(&self, o: &H) -> Ordering {
        let a = Integer::from(&self.x * &o.w);
        let b = Integer::from(&o.x * &self.w);
        match a.cmp(&b) {
            Ordering::Equal => Integer::from(&self.y * &o.w).cmp(&Integer::from(&o.y * &self.w)),
            c => c,
        }
    }
}

/// Integer half-plane a0·x + a1·y <= b.
pub(crate) struct Hp {
    a0: Integer,
    a1: Integer,
    b: Integer,
}

impl Hp {
    fn from_q(a: &(Q, Q), b: &Q) -> Hp {
        let mut l = Integer::from(a.0.denom());
        l.lcm_mut(a.1.denom());
        l.lcm_mut(b.denom());
        let f = |v: &Q| -> Integer { Integer::from(v.numer() * Integer::from(&l / v.denom())) };
        Hp { a0: f(&a.0), a1: f(&a.1), b: f(b) }
    }
    /// Python's half-plane for edge P→Q: a = (Qy − Py, Px − Qx), b = a·P. Scale by Wp²·Wq > 0 to obtain integers.
    fn from_edge(p: &H, q: &H) -> Hp {
        let a0 = Integer::from(&q.y * &p.w) - Integer::from(&p.y * &q.w);
        let a1 = Integer::from(&p.x * &q.w) - Integer::from(&q.x * &p.w);
        let b = Integer::from(&a0 * &p.x) + Integer::from(&a1 * &p.y);
        let mut h = Hp { a0: Integer::from(&a0 * &p.w), a1: Integer::from(&a1 * &p.w), b };
        let mut g = Integer::from(h.a0.gcd_ref(&h.a1));
        g.gcd_mut(&h.b);
        if g > 1 {
            h.a0.div_exact_mut(&g);
            h.a1.div_exact_mut(&g);
            h.b.div_exact_mut(&g);
        }
        h
    }
    /// W·(a·p − b), with the same sign as a·p − b.
    fn eval(&self, p: &H) -> Integer {
        let mut f = Integer::from(&self.a0 * &p.x);
        f += Integer::from(&self.a1 * &p.y);
        f -= Integer::from(&self.b * &p.w);
        f
    }
}

fn clip_poly_h(poly: &[H], hp: &Hp) -> Vec<H> {
    let n = poly.len();
    let f: Vec<Integer> = poly.iter().map(|p| hp.eval(p)).collect();
    let mut out = Vec::with_capacity(n + 2);
    for i in 0..n {
        let j = (i + 1) % n;
        let (p, q) = (&poly[i], &poly[j]);
        let sp = f[i].cmp0();
        let sq = f[j].cmp0();
        if sp != Ordering::Greater {
            out.push(p.clone());
        }
        if (sp == Ordering::Less && sq == Ordering::Greater) || (sq == Ordering::Less && sp == Ordering::Greater) {
            let (fp, fq) = (&f[i], &f[j]);
            let mut r = H {
                x: Integer::from(fp * &q.x) - Integer::from(fq * &p.x),
                y: Integer::from(fp * &q.y) - Integer::from(fq * &p.y),
                w: Integer::from(fp * &q.w) - Integer::from(fq * &p.w),
            };
            r.normalize();
            out.push(r);
        }
    }
    out
}

fn clip_to_h(poly: Vec<H>, vs: &[H]) -> Vec<H> {
    let k = vs.len();
    let mut poly = poly;
    for i in 0..k {
        let hp = Hp::from_edge(&vs[i], &vs[(i + 1) % k]);
        poly = clip_poly_h(&poly, &hp);
        if poly.is_empty() {
            return poly;
        }
    }
    poly
}

fn area_h(poly: &[H]) -> Q {
    let n = poly.len();
    let mut s = Q::new();
    for i in 0..n {
        let p = &poly[i];
        let q = &poly[(i + 1) % n];
        let num = Integer::from(&p.x * &q.y) - Integer::from(&q.x * &p.y);
        if num.cmp0() != Ordering::Equal {
            s += Q::from((num, Integer::from(&p.w * &q.w)));
        }
    }
    s / 2u32
}

/// sign(cross(o, a, b))
fn orient(o: &H, a: &H, b: &H) -> Ordering {
    let t1 = Integer::from(&a.y * &b.w) - Integer::from(&b.y * &a.w);
    let t2 = Integer::from(&a.x * &b.w) - Integer::from(&b.x * &a.w);
    let t3 = Integer::from(&a.x * &b.y) - Integer::from(&b.x * &a.y);
    let d = Integer::from(&o.x * &t1) - Integer::from(&o.y * &t2) + Integer::from(&o.w * &t3);
    d.cmp0()
}

/// Python reference hull: monotone chain on sorted(set(pts)). Inputs need not be normalized; outputs are normalized.
fn hull_h(mut pts: Vec<H>) -> Vec<H> {
    pts.sort_by(|a, b| a.cmp_xy(b));
    pts.dedup_by(|a, b| a.cmp_xy(b) == Ordering::Equal);
    if pts.len() < 3 {
        for p in pts.iter_mut() {
            p.normalize();
        }
        return pts;
    }
    let mut lo: Vec<&H> = Vec::new();
    for p in pts.iter() {
        while lo.len() >= 2 && orient(lo[lo.len() - 2], lo[lo.len() - 1], p) != Ordering::Greater {
            lo.pop();
        }
        lo.push(p);
    }
    let mut up: Vec<&H> = Vec::new();
    for p in pts.iter().rev() {
        while up.len() >= 2 && orient(up[up.len() - 2], up[up.len() - 1], p) != Ordering::Greater {
            up.pop();
        }
        up.push(p);
    }
    lo.pop();
    up.pop();
    lo.into_iter()
        .chain(up)
        .map(|p| {
            let mut q = p.clone();
            q.normalize();
            q
        })
        .collect()
}

fn outer_hull_h(u0: &Q, u1: &Q, cx: &Q, cy: &Q, rx: &Q, ry: &Q) -> Vec<H> {
    let (c0, s0) = cs(u0);
    let (c1, s1) = cs(u1);
    let mut base: Vec<Pt> = Vec::with_capacity(12);
    let h = qf(1, 2);
    for (ex, ey) in [(1i64, 1i64), (-1, 1), (-1, -1), (1, -1)] {
        let (ex, ey) = (qi(ex), qi(ey));
        let v0 = (
            half(&sub(&mul(&c0, &ex), &mul(&s0, &ey))),
            half(&add(&mul(&s0, &ex), &mul(&c0, &ey))),
        );
        let v1 = (
            half(&sub(&mul(&c1, &ex), &mul(&s1, &ey))),
            half(&add(&mul(&s1, &ex), &mul(&c1, &ey))),
        );
        let det = sub(&mul(&v0.0, &v1.1), &mul(&v0.1, &v1.0));
        base.push(v0.clone());
        base.push(v1.clone());
        if det.cmp0() != Ordering::Equal {
            let tx = div(&sub(&mul(&h, &v1.1), &mul(&v0.1, &h)), &det);
            let ty = div(&sub(&mul(&v0.0, &h), &mul(&h, &v1.0)), &det);
            base.push((tx, ty));
        }
    }
    // Corner offsets (±rx, ±ry) as (Ox, Oy, Ow): point + offset = (Xb·Ow + Ox·Wb, Yb·Ow + Oy·Wb, Wb·Ow).
    let mut ow = Integer::from(rx.denom());
    ow.lcm_mut(ry.denom());
    let ox = Integer::from(rx.numer() * Integer::from(&ow / rx.denom()));
    let oy = Integer::from(ry.numer() * Integer::from(&ow / ry.denom()));
    let nox = Integer::from(-&ox);
    let noy = Integer::from(-&oy);
    let mut all = Vec::with_capacity(base.len() * 4);
    for p in base.iter() {
        let b = H::from_q(&(add(&p.0, cx), add(&p.1, cy)));
        let bx = Integer::from(&b.x * &ow);
        let by = Integer::from(&b.y * &ow);
        let bw = Integer::from(&b.w * &ow);
        for sx in [&nox, &ox] {
            for sy in [&noy, &oy] {
                all.push(H {
                    x: Integer::from(&bx + Integer::from(sx * &b.w)),
                    y: Integer::from(&by + Integer::from(sy * &b.w)),
                    w: bw.clone(),
                });
            }
        }
    }
    hull_h(all)
}

/// Cover.mass_convex(poly, polys=False), matching the direct port's segment selection and integer Cyrus–Beck steps.
fn mass_convex_h(segs: &[Seg], poly: &[H], poly_area: Option<&Q>) -> Q {
    if poly.len() < 3 {
        return qi(0);
    }
    let mut ix = (0usize, 0usize);
    let mut iy = (0usize, 0usize);
    for (k, p) in poly.iter().enumerate() {
        if Integer::from(&p.x * &poly[ix.0].w) < Integer::from(&poly[ix.0].x * &p.w) {
            ix.0 = k;
        }
        if Integer::from(&p.x * &poly[ix.1].w) > Integer::from(&poly[ix.1].x * &p.w) {
            ix.1 = k;
        }
        if Integer::from(&p.y * &poly[iy.0].w) < Integer::from(&poly[iy.0].y * &p.w) {
            iy.0 = k;
        }
        if Integer::from(&p.y * &poly[iy.1].w) > Integer::from(&poly[iy.1].y * &p.w) {
            iy.1 = k;
        }
    }
    let (lx, hx, ly, hy) = (poly[ix.0].xq(), poly[ix.1].xq(), poly[iy.0].yq(), poly[iy.1].yq());
    let lo_cell = |v: &Q| -> i64 {
        if v.cmp0() != Ordering::Less {
            trunc_i64(v)
        } else {
            trunc_i64(v) - 1
        }
    };
    let (qx0, qx1, qy0, qy1) = (lo_cell(&lx), trunc_i64(&hx), lo_cell(&ly), trunc_i64(&hy));
    let n = poly.len();
    let iedges: Vec<Hp> = (0..n).map(|i| Hp::from_edge(&poly[i], &poly[(i + 1) % n])).collect();
    // Prefilter: for counterclockwise convex polygons of positive area, segments with disjoint bboxes contribute 0.
    let prefilter = match poly_area {
        Some(a) => a.cmp0() == Ordering::Greater,
        None => area_h(poly).cmp0() == Ordering::Greater,
    };
    let mut m = qi(0);
    for s in segs {
        if s.gx1 < qx0 || s.gx0 > qx1 || s.gy1 < qy0 || s.gy0 > qy1 {
            continue;
        }
        if prefilter && (s.bx1 < lx || s.bx0 > hx || s.by1 < ly || s.by0 > hy) {
            continue;
        }
        let mut t0n = Integer::from(0);
        let mut t0d = Integer::from(1);
        let mut t1n = Integer::from(1);
        let mut t1d = Integer::from(1);
        let mut empty = false;
        for e in iedges.iter() {
            let mut num = Integer::from(&s.k * &e.b);
            num -= Integer::from(&e.a0 * &s.ak.0);
            num -= Integer::from(&e.a1 * &s.ak.1);
            let mut den = Integer::from(&e.a0 * &s.dk.0);
            den += Integer::from(&e.a1 * &s.dk.1);
            match den.cmp0() {
                Ordering::Equal => {
                    if num.cmp0() == Ordering::Less {
                        empty = true;
                        break;
                    }
                }
                Ordering::Greater => {
                    if Integer::from(&num * &t1d) < Integer::from(&t1n * &den) {
                        t1n = num;
                        t1d = den;
                    }
                }
                Ordering::Less => {
                    num = -num;
                    den = -den;
                    if Integer::from(&num * &t0d) > Integer::from(&t0n * &den) {
                        t0n = num;
                        t0d = den;
                    }
                }
            }
            if Integer::from(&t0n * &t1d) > Integer::from(&t1n * &t0d) {
                empty = true;
                break;
            }
        }
        if !empty && Integer::from(&t1n * &t0d) > Integer::from(&t0n * &t1d) {
            let num = Integer::from(&t1n * &t0d) - Integer::from(&t0n * &t1d);
            let den = Integer::from(&t1d * &t0d);
            m += Q::from(&s.w * Q::from((num, den)));
        }
    }
    m
}

impl FamilyCore {
    fn mass_v_h(&self, poly: &[H], poly_area: &Q, delta: &Q) -> Q {
        if poly.len() < 3 {
            return qi(0);
        }
        let xr = add(&qi(crate::w0()), delta);
        let mut segs = Vec::new();
        for (xl, y, rho) in self.v.iter() {
            if xr > *xl {
                segs.push(((xl.clone(), y.clone()), (xr.clone(), y.clone()), mul(rho, &sub(&xr, xl))));
            }
        }
        mass_convex_h(&make_group(segs), poly, Some(poly_area))
    }

    /// Same value as seam4d.bound(), optimized.
    #[allow(clippy::too_many_arguments)]
    pub fn bound_fast(&self, x0: Q, x1: Q, y0: Q, y1: Q, u0: Q, u1: Q, e0: Q, e1: Q) -> Option<Q> {
        let lo = half(&wmin(&u0, &u1));
        let x0 = if lo > x0 { lo.clone() } else { x0 };
        let y0 = if lo > y0 { lo } else { y0 };
        if x0 > x1 || y0 > y1 {
            return None;
        }
        let cx = half(&add(&x0, &x1));
        let cy = half(&add(&y0, &y1));
        let rx = half(&sub(&x1, &x0));
        let ry = half(&sub(&y1, &y0));
        let big = qi(2);
        let nbig = qi(-2);
        let mut p: Vec<H> = vec![
            H::from_q(&(nbig.clone(), nbig.clone())),
            H::from_q(&(big.clone(), nbig.clone())),
            H::from_q(&(big.clone(), big.clone())),
            H::from_q(&(nbig.clone(), big.clone())),
        ];
        for (a, b) in angular_core_halfplanes(&u0, &u1) {
            let mut nb = b;
            nb -= mul(&absq(&a.0), &rx);
            nb -= mul(&absq(&a.1), &ry);
            p = clip_poly_h(&p, &Hp::from_q(&a, &nb));
            if p.is_empty() {
                break;
            }
        }
        let zero = qi(0);
        let mut p: Vec<H> = p.iter().map(|v| v.shift(&cx, &cy)).collect();
        let mut pa = if p.len() >= 3 { area_h(&p) } else { qi(0) };
        if p.len() >= 3 && pa.cmp0() == Ordering::Less {
            p.reverse();
            pa = -pa;
        }
        let mut m = if p.len() >= 3 { mass_convex_h(&self.f, &p, Some(&pa)) } else { qi(0) };
        if p.len() >= 3 {
            let ne0 = neg(&e0);
            let p0: Vec<H> = p.iter().map(|v| v.shift(&ne0, &zero)).collect();
            let pt = if e0 != e1 {
                let ne1 = neg(&e1);
                let p1: Vec<H> = p.iter().map(|v| v.shift(&ne1, &zero)).collect();
                clip_to_h(p0, &p1)
            } else {
                p0
            };
            if pt.len() >= 3 {
                m += mass_convex_h(&self.t, &pt, None);
            }
            m += self.mass_v_h(&p, &pa, &e0);
        }
        let uh: Vec<H> = self.u.iter().map(H::from_q).collect();
        let o = outer_hull_h(&u0, &u1, &cx, &cy, &rx, &ry);
        let inner = if p.len() >= 3 { clip_to_h(p, &uh) } else { Vec::new() };
        let a_in = if inner.len() >= 3 { area_h(&inner) } else { qi(0) };
        let a_o = area_h(&o);
        let oc = clip_to_h(o, &uh);
        let a_oc = if oc.len() >= 3 { area_h(&oc) } else { qi(0) };
        let a_out = sub(&qi(1), &sub(&a_o, &a_oc));
        m += if a_out > a_in { a_out } else { a_in };
        Some(m)
    }
}
